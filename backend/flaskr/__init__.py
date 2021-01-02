import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    '''
    function to paginate the responses
    '''
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*":{"origins":'*'}})

  @app.after_request
  def after_request(response):
    #response.
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  # @app.route('/')
  # def hello():
  #   return jsonify({'message':'Hello Yang'})

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    all_categories = [category.format() for category in categories]

    if len(all_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': all_categories,
      'total_categories': len(categories)
    }),200
    

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_question():
    '''
    endpoint for get all questions
    '''
    # get questions
    questions = Question.query.order_by(Question.id).all()
    
    # abort if no questions
    if len(questions) == 0:
      abort(404)
    
    # paginate questions
    question_nr = len(questions)
    selected_questions = paginate_questions(request, questions)

    # Get all categories
    categories = Category.query.order_by(Category.id).all()
    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type
    
    # get current categories
    current_category_ids=[]
    for question in selected_questions:
      if question['category'] not in current_category_ids:
        current_category_ids.append(question['category'])
    
    current_category = [categories_dict[id] for id in current_category_ids]
  
    return jsonify({
      'success': True,
      'questions': selected_questions,
      'total_questions':question_nr,
      'current_categories':current_category,
      'categories': categories_dict
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    '''
    endpoint to 'delete' a specific question
    '''
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
          abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
          'success': True,
          'deleted': question_id,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
      })

    except:
      # abort if error happens
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_a_question():
    # get the data from request
    body = request.get_json()

    try:
      # check if there is None value in the input
      if None in [body.get('question'), body.get('answer'), 
                  body.get('category'), body.get('difficulty')]:
        abort(422)
      
      # create a Question object
      new_question = Question(
        question=body.get('question'),
        answer=body.get('answer'), 
        category=body.get('category'),
        difficulty=body.get('difficulty'))
      # insert to database
      new_question.insert()

      # get all questions and paginate
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)

      # return data to view
      return jsonify({
          'success': True,
          'created': new_question.id,
          'question_created': new_question.question,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
      })

    except:
      # if error happens, abort
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    '''
    endpoint that returns questions from a search term. 
    '''

    # Get search term
    body = request.get_json()
    search_term = body.get('searchTerm', '')

    # Return 422 status if no search item
    if search_term == None:
      abort(422)

    try:
      # get all questions
      search_questions = Question.query.filter(
          Question.question.ilike(f'%{search_term}%')).all()

      # if there are no questions abort with 404
      if len(search_questions) == 0:
          abort(404)

      # paginate
      current_questions = paginate_questions(request, search_questions)

      # return response if successful
      return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
      }), 200

    except:
      # if error happens, abort with 404
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    '''
    Endpoint: GET requests for getting questions based on category.
    '''

    # get the category by id
    category = Category.query.filter_by(id=id).one_or_none()

    # abort 400 if category isn't found
    if (category is None):
      abort(400)

    try: 
      # get the matching questions
      selection = Question.query.filter_by(category=category.id).all()

      # paginate the selection
      paginated = paginate_questions(request, selection)

      # return the results
      return jsonify({
        'success': True,
        'questions': paginated,
        'total_questions': len(Question.query.all()),
        'question_in_category':len(selection),
        'current_category': category.type
      })
    except:
      # if error happened, abort with 422
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quizzes():
    '''
    Endpoint that handles get random questions as quizzes
    '''
    # get information
    body = request.get_json()
    pre_question = body.get('previous_questions')
    category = body.get('quiz_category')

    # return 400 error if empty
    if None in [pre_question,category]:
      abort(400)

    try:

      # get all questions by category
      if (category['id'] == 0):
        questions = Question.query.all()
      else:
        questions = Question.query.filter_by(
          category=category['id']).all()

      # get a random next question  
      def random_question():
        while True:
          next_q = questions[random.randint(0, len(questions)-1)]
          if next_q.id not in pre_question:
            break
        return next_q
      
      next_question = random_question()

      return jsonify({
          'success': True,
          'question': next_question.format(),
      }), 200
    
    except:
      # if error
      abort(422)
    
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request error'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422
  
  return app

    
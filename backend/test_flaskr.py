import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

def create_a_question():
  '''
  This function adds a new mock question
  and return the question ID
  '''
  question = Question(
        question='This is a test question',
        answer='test answer',
        difficulty=1,
        category='1')
  question.insert()

  return question.id


class TriviaTestCase(unittest.TestCase):
  """This class represents the trivia test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.username = 'postgres'
    self.password = '123456'
    self.database_name = "trivia_test"
    self.database_path = "postgres://{}:{}@{}/{}".format(self.username,self.password,'localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

  def tearDown(self):
    """Executed after reach test"""
    pass

  """
  TODO
  Write at least one test for each test for successful operation and for expected errors.
  """

  def test_get_categories(self):
    '''
    test get_categories
    '''
    # get data
    response = self.client().get('/categories')
    data = json.loads(response.data)
    
    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['categories'])
    self.assertEqual(len(data['categories']), 6)

  def test_get_question(self):
    '''
    test get_questions
    '''
    # get data
    response = self.client().get('/questions')
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['categories'])
    self.assertTrue(data['total_questions'])
    self.assertTrue(data['questions'])
    self.assertEqual(len(data['questions']), 10)
  
  def test_get_question_outbound_page_number(self):
    '''
    test get_questions when the page number exceed the max pages
    '''
    # get data
    response = self.client().get('/questions?page=100')
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Not found')

  def test_delete_question(self):
    '''
    test delete_question
    '''
    # get the total question numbers
    questions_nr = len(Question.query.all())

    # add a new question
    new_question_id = create_a_question()

    # delete the created question. 
    response = self.client().delete('/questions/{}'.format(new_question_id))
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['deleted'], new_question_id)
    self.assertEqual(data['total_questions'], questions_nr)

  def test_delete_if_id_not_exist(self):
    '''
    test the delete response if the provided id does not exist
    '''
    # delete a question out of range. 
    response = self.client().delete('/questions/{}'.format(1000))
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')
  
  def test_create_a_question(self):
    '''
    test to create a new question
    '''
    # get the total question numbers before inserting
    questions_nr = len(Question.query.all())

    # mock question
    data = {
      'question': 'new question',
      'answer': 'new answer',
      'difficulty': 1,
      'category':1
    }

    # test to add a new question
    response = self.client().post('/questions',json = data)
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['question_created'], 'new question')
    self.assertEqual(data['total_questions'], questions_nr+1)
  
  def test_create_a_question_not_enough_input(self):
    '''
    test to create a new question
    '''
    # get the total question numbers before inserting
    questions_nr = len(Question.query.all())

    # mock question
    data = {
      'question': None,
      'answer': None,
      'difficulty': 1,
      'category':1
    }

    # test to add a new question
    response = self.client().post('/questions',json = data)
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')
  
  def test_search_questions(self):
    '''
    test to search question
    '''
    # prepare search data
    search_data = {
      'searchTerm': 'first ever soccer World Cup in 1930',
    }

    # make request and process response
    response = self.client().post('/questions/search', json=search_data)
    data = json.loads(response.data)

    # Assertions
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(len(data['questions']), 1)

  def test_search_questions_not_found(self):
    '''
    test to search question
    '''
    # prepare search data
    search_data = {
      'searchTerm': 'eafdadcaatea',
    }

    # make request and process response
    response = self.client().post('/questions/search', json=search_data)
    data = json.loads(response.data)

    # Assertions
    self.assertEqual(response.status_code,404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Not found')
  
  def test_get_by_category(self):
    '''
    test get_by_category
    '''
    
    # define category and get correct answer
    category_id = 2
    selection = Question.query.filter_by(category=category_id).all()

    # make request and process response
    response = self.client().get('/categories/{}/questions'.format(category_id))
    data = json.loads(response.data)

    # Assertions
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['question_in_category'], len(selection))
  
  def test_invalid_category_id(self):
    '''
    Test for invalid category id
    '''

    # define an invalid category id
    category_id = 100

    # request with invalid category id
    response = self.client().get('/categories/{}/questions'.format(category_id))
    data = json.loads(response.data)

    # Assertions to check error 404
    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Not found')
  
  def test_get_quizzes(self):
    '''
    Test the get quizzes function
    '''

    # define input data
    request_data = {
      'previous_questions': [16,17],
      'quiz_category':{
        'type':'Art',
        'id':2
      }
    }

    # the available questions ids that the reponse should be in.
    questions = Question.query.filter_by(category=2).all()
    ids = [question.id for question in questions]
    available_id = [id for id in ids if id not in [16,17]]

    # get response
    response = self.client().post('/quizzes', json = request_data)
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
    self.assertIn(data['question_id'], available_id)

  def test_get_quizzes_not_valid_input(self):
    '''
    test get_quizzes when invalid input
    '''
    # define input data
    request_data = {
      'previous_questions': [16,17],
      'quiz_category': None
      }
    
    # get response
    response = self.client().post('/quizzes', json = request_data)
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code,400)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Bad request error')

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()
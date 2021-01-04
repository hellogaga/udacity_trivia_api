# Full Stack Trivia

## Introduction
Udacity invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game. The created frontend is in the `\frontend` folder. 

The frontend is designed to work with backend API. The purpose of this project is to provide a functional API, which is located in the `\backend` folder. The backend API is capable of:
1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Table of contents
  - [Overview](#Overview)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview))
  - [Project Structure](#project-structure)
  - [How to use the application](#how-to-use-the-application)
  - [Backend API documentation](#backend-api-documentation)
  - [Authors](#authors)

## Overview
### Backend Dependencies
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-CORS** the extension to handle cross origin requests from our frontend server. <br>

More detailed information can be found in the  [readme file](./backend/README.md) in the backend folder. 
### Frontend Dependencies
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. <br>
More detailed information can be found in the  [readme file](./frontend/README.md) in the frontend folder. 

## Project Structure
```sh
  ├── README.md
  ├── backend
      ├── flaskr -- the main application
      ├── models.py -- database model
      ├── README.md -- readme file for backend. It contains the document for APIs. 
      ├── requirements.txt -- The dependencies to run the backend
      ├── test_flaskr.py -- Use python unittest to test the API
      ├── trivia.psql -- Postsql database file to restore a database
  ├── frontend
      ├── public
      ├── src
          ├── components -- folder contain javascript that define the interactions between API and backend
          ├── ...
      ├── package-lock.json
      ├── packages.json -- dependencies to run the frontend
  ```

Overall:
* The backend application and databases are in the `backend` folder, where we mainly define the APIs. APIs are further called in the front end. 
* The `frontend` directory contains a complete React frontend to consume the data from the Flask server. The frontend uses the APIs provided by the backend to have interactions with the application user.  

## How to use the application
1. Understand the Project Structure (explained above) and where important files are located.
2. git clone this repo to your local folder using `https://github.com/hellogaga/udacity_trivia_api.git`
3. Install all the dependencies (both frontend and backend) according to the instructions. 
4. Create a database and restore it by the instruction provided in backend [readme file](./backend/README.md).
5. Navigate to **backend/models.py** and revise the file with your own PostgreSQL username and password. 
6. Navigate to folder `backend`, Start the backend using the following commands (linux environment):
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
7. Open a **new** bash console. Navigate to folder `frontend` and run the following commands. They will start the front end. 
```bash
npm install \*only need to execute once*\
npm start
```
8. Navigate to project homepage [http://127.0.0.1:3000/](http://127.0.0.1:3000/) or [http://localhost:3000](http://localhost:3000) 
9. Enjoy the application.

### Test the backend
To test the backend:
1. Create a test database and restore it using trivia.psql
2. Provide the right username, password and test database name in `backend/test_flaskr.py`.
3. navigate to folder `backend`
4. run `python test_flaskr.py`. 

## Backend API documentation
Detailed API documentation is provided in the backend [readme file](./backend/README.md). 


## Authors
* Hellogaga used the starting code from [udacity](www.udacity.com) to finish the API and test code.
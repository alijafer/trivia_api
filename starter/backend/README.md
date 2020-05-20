# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup (REQUER)
Install [PostgreSQL](https://www.postgresql.org/download/) in your system and Create database using `psql` terminal
```bash
Create database trivia;
```
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia [<username>]< trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:
for Windows 
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```
for linux or macOS
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

The app will be work server on http://127.0.0.1:5000/ 

## API Reference

### Getting Started
- Backend Base URL: http://127.0.0.1:5000/
- Frontend Base URL: http://localhost:3000

## Testing
To run the tests, run
```bash
dropdb trivia_test [<username>]
createdb trivia_test [<username>]
psql trivia_test [<username>] < trivia.psql
python test_flaskr.py
```


## Endpoints


- ### GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: all categories
- Response Arguments:
    - dictionary of all `categories` 

- sample: `curl http://127.0.0.1:5000/categories` or 
` curl http://127.0.0.1:5000/category`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "test"
  },
  "success": true
}
```

- ### GET /questions
- Fetches a dictionary of questions 
- Fetches a dictionary of categories 
- Request Arguments: None
- Returns: 10 questions in each page
- Response Arguments:
    - dictionary `categories` 
    - dictionary `questions`

sample: `curl http://127.0.0.1:5000/questions` or 
` curl http://127.0.0.1:5000/question`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "test"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "totalQuestions": 20
}
```
- ### DELETE '/question/` <int:question_id> `'
- delete question by id 
- Request Arguments: None
- Response Arguments: 
    - `delete_id` 
    - `message` 
- Sample: 
`curl http://127.0.0.1:5000/questions/27 -X DELETE`
```
{
  "delete_id": 27,
  "message": "Question successfully deleted",
  "success": true
}
```
- ### POST /questions
- Create new question and add in database
- Request Arguments:
    - `question`
    - `answer`
    - `difficulty` 
    - `category`
- Response Arguments:
     - `question`
    - `answer`
    - `difficulty` 
    - `category
- Sample:
`curl -L -X POST 'http://127.0.0.1:5000/questions' -H 'Content-Type: application/json' --data-raw '{
    "question": "What is the #1 search engine used today?",
    "answer": "Google",
    "difficulty": 1,
    "category": 5
}'`
```
{
  "answer": "Google",
  "category": 5,
  "difficulty": 1,
  "question": "What is the #1 search engine used today?",
  "success": true
}
```
- ### POST /questions/search
- Returns search result for questions
- Request Arguments: `searchTerm` search term
- Response Arguments: `current_category` and `totalQuestions
- Sample: `curl -L -X POST 'http://127.0.0.1:5000/questions/search' -H 'Content-Type: application/json' --data-raw '{
	"searchTerm": "search engine"}
' `
```
{
  "current_category": 5,
  "questions": [
    {
      "answer": "Google",
      "category": 5,
      "difficulty": 1,
      "id": 28,
      "question": "What is the #1 search engine used today?"
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```

- ### GET /categories/`<int:category_id>`/questions
- get questions based on category
- Request Arguments: 
    - `category_id` ID of category
- Response Arguments: 
    - `questions` get maximum 10 questions
    - `totalQuestions` total question
    - `categories` type of category

- Sample: `curl http://127.0.0.1:5000/categories/2/questions`


```
{
  "categories": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "totalQuestions": 4
}
```

- ### POST /quizzes
- Fetches a unique question for the quiz on selected or unselected category
- Request Arguments: 
   - `previous_questions` list of id of previous questions
   - `quiz_category` id of category
- Response Arguments:
   - `question` Random question
- Sample: `curl -L -X POST 'http://127.0.0.1:5000/quizzes' -H 'searchTerm: a' -H 'Content-Type: application/json' --data-raw '{
    "previous_questions": [
        3,
        4,
        10,
        12,
        11,
        5
    ],
    "quiz_category": "0"
}'`


```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```


## Error Handling
Errors are returned in the following json format:
```
{
  "error": 400,
  "message": "bad request",
  "success": false
}
```
HTTP response status codes currently returned are:
- 404 : resource not found
- 422 : unprocessable
- 400 : bad request
- 500 : Internal Server Error


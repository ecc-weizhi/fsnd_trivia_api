# Backend - Full Stack Trivia API

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in
   the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This
   keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment
   for your platform can be found in
   the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to
   the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

4. **Key Dependencies**

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle
  requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite
  database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests
  from our frontend server.

### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks

These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data.
The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats
already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or
you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint
   should return a list of questions, number of total questions, current category, categories.


3. Create an endpoint to handle GET requests for all available categories.


4. Create an endpoint to DELETE question using a question ID.


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty
   score.


6. Create a POST endpoint to get questions based on category.


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search
   term is a substring of the question.


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question
   parameters and return a random questions within the given category, if provided, and that is not one of the previous
   questions.


9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## API reference

### Questions

#### GET `/questions`

Fetches a paginated list of questions.

##### Parameters

Name | Type | In | Description
---|---|---|---
page | integer | query | which page number to request

##### Response

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is love?",
      "answer": "Baby don't hurt me no more",
      "category": "2",
      "difficulty": 4
    },
    {
      "id": 2,
      "question": "What is the average air speed velocity of a laden swallow?",
      "answer": "24 miles per hour",
      "category": "2",
      "difficulty": 4
    },
    ...
  ],
  "total_questions": 19,
  "categories": [
    {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    }
  ]
}
```

#### POST `/questions` (search)

Search for question by text (case-insensitive). The result is a list of all matching questions.

##### Parameters

Name | Type | In | Description
---|---|---|---
searchTerm | string | body | Case-insensitive terms to look for

##### Response

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is love?",
      "answer": "Baby don't hurt me no more",
      "category": "2",
      "difficulty": 4
    },
    {
      "id": 2,
      "question": "What is the average air speed velocity of a laden swallow?",
      "answer": "24 miles per hour",
      "category": "2",
      "difficulty": 4
    },
    ...
  ],
  "total_questions": 2
}
```

#### POST `/questions` (add question)

Add a new question.

##### Parameters

Name | Type | In | Description
---|---|---|---
question | string | body |
answer | string | body |
category | string | body |
difficulty | integer | body |

##### Response

```json
{
  "success": true
}
```

#### DELETE `/questions/{question_id}`

Delete question.

##### Parameters

Name | Type | In | Description
---|---|---|---
question_id | integer | path |

##### Response

```json
{
  "success": true,
  "deleted_question_id": 23
}
```

### Categories

#### GET `/categories`

Fetches a list of all categories

##### Response

```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### GET `/categories/{category_id}/questions`

Fetches all questions from a category.

##### Parameters

Name | Type | In | Description
---|---|---|---
category_id | integer | path |

##### Response

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is love?",
      "answer": "Baby don't hurt me no more",
      "category": "2",
      "difficulty": 4
    },
    {
      "id": 2,
      "question": "What is the average air speed velocity of a laden swallow?",
      "answer": "24 miles per hour",
      "category": "2",
      "difficulty": 4
    },
    ...
  ],
  "total_questions": 2
}
```

### Quizzes

#### POST `/quizzes`

Fetches next question in quiz mode.

##### Parameters

Name | Type | In | Description
---|---|---|---
previous_questions | array | body | an integer array where the elements are id of questions that has appeared in quiz before
quiz_category | integer | path | Quiz category id, or 0 for all category.

##### Response

```json
{
  "success": true,
  "questions": {
    "id": 1,
    "question": "What is love?",
    "answer": "Baby don't hurt me no more",
    "category": "2",
    "difficulty": 4
  }
}
```

## API errors

Here are the possible client errors along with examples of how the response looks like.

### `400` Bad request

```json
{
  "success": false,
  "message": "Problems parsing JSON"
}
```

### `404` Not found

```json
{
  "success": false,
  "message": "questions with id 2 not found"
}
```

### `422` Not found

```json
{
  "success": false,
  "message": "Required field(s) missing from request body: [question, category]"
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

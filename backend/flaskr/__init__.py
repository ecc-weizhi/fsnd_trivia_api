import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db
from sqlalchemy.exc import SQLAlchemyError

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)

        start_index_inclusive = (page - 1) * QUESTIONS_PER_PAGE
        end_index_exclusive = start_index_inclusive + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        formatted_categories = {}
        categories = Category.query.all()
        for category in categories:
            formatted_categories[category.id] = category.type

        return jsonify({
            "success": True,
            "questions": formatted_questions[start_index_inclusive:end_index_exclusive],
            "total_questions": len(formatted_questions),
            "categories": formatted_categories,
        })

    @app.route('/questions', methods=['POST'])
    def post_questions():
        data_string = request.data
        request_json = json.loads(data_string)

        if "searchTerm" in request_json:
            # performing a search
            return search_questions(request_json)
        else:
            # performing add question
            return add_question(request_json)

    def search_questions(request_json):
        raw_search_term = request_json["searchTerm"]
        search_term = "%{}%".format(raw_search_term)

        questions = Question.query \
            .filter(Question.question.ilike(search_term)) \
            .all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
        })

    @app.route('/questions', methods=['POST'])
    def add_question(request_json):
        question = Question(
            request_json["question"],
            request_json["answer"],
            request_json["category"],
            request_json["difficulty"]
        )

        try:
            db.session.add(question)
            db.session.commit()
            is_success = True
        except SQLAlchemyError:
            is_success = False

        if is_success:
            return jsonify({
                "success": is_success,
            })
        else:
            abort(500)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            Question.query.filter_by(id=question_id).first_or_404().delete()
            db.session.commit()
            is_success = True
        except SQLAlchemyError:
            is_success = False

        if is_success:
            return jsonify({
                "success": is_success,
            })
        else:
            abort(500)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
        })

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        id_to_type_map = {}
        for category in categories:
            id_to_type_map[category.id] = category.type

        return jsonify({
            "success": True,
            "categories": id_to_type_map,
        })

    @app.route('/quizzes', methods=['POST'])
    def get_next_question():
        data_string = request.data
        data_dictionary = json.loads(data_string)
        previous_questions = data_dictionary["previous_questions"]
        quiz_category = data_dictionary["quiz_category"]

        query = Question.query

        # filter by category
        if quiz_category != 0:
            query = query.filter(Question.category == quiz_category["id"])

        # filter by id
        for previous_question_id in previous_questions:
            query = query.filter(Question.id != previous_question_id)

        question = query.first()

        return jsonify({
            "success": True,
            "question": question.format() if question else None,
        })

    return app


'''
@TODO: 
Create an endpoint to handle GET requests 
for all available categories.
'''

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

'''
@TODO: 
Create an endpoint to DELETE question using a question ID. 

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page. 
'''

'''
@TODO: 
Create an endpoint to POST a new question, 
which will require the question and answer text, 
category, and difficulty score.

TEST: When you submit a question on the "Add" tab, 
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.  
'''

'''
@TODO: 
Create a POST endpoint to get questions based on a search term. 
It should return any questions for whom the search term 
is a substring of the question. 

TEST: Search by any phrase. The questions list will update to include 
only question that include that string within their question. 
Try using the word "title" to start. 
'''

'''
@TODO: 
Create a GET endpoint to get questions based on category. 

TEST: In the "List" tab / main screen, clicking on one of the 
categories in the left column will cause only questions of that 
category to be shown. 
'''

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

'''
@TODO: 
Create error handlers for all expected errors 
including 404 and 422. 
'''

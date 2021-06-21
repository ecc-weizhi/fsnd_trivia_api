from flask import Flask
from flask_cors import CORS

from .ErrorHandler import ErrorHandler
from .categories_blueprint import categories_blueprint
from .client_error_exceptions import ClientErrorException, NotFound, UnprocessableEntity, BadRequest
from .models import setup_db, Question, Category, db
from .questions_blueprint import questions_blueprint
from .quizzes_blueprint import quizzes_blueprint

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(questions_blueprint)
    app.register_blueprint(categories_blueprint)
    app.register_blueprint(quizzes_blueprint)
    setup_db(app)
    CORS(app)
    error_handler = ErrorHandler()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.errorhandler(ClientErrorException)
    def client_error(error):
        return error_handler.handle_client_error(error)

    @app.errorhandler(500)
    def internal_server_error(error):
        return error_handler.handle_internal_server_error(error)

    return app

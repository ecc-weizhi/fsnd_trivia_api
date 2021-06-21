import json
from json import JSONDecodeError

from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import SQLAlchemyError

from .client_error_exceptions import BadRequest, UnprocessableEntity, NotFound
from .models import Category, Question, db

questions_blueprint = Blueprint('questions', __name__, url_prefix='')
QUESTIONS_PER_PAGE = 10


@questions_blueprint.route('/questions', methods=['GET'])
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


@questions_blueprint.route('/questions', methods=['POST'])
def post_questions():
    data_string = request.data
    try:
        request_json = json.loads(data_string)
    except JSONDecodeError:
        raise BadRequest()

    if "searchTerm" in request_json:
        # performing a search
        return _search_questions(request_json)
    else:
        # performing add question
        return _add_question(request_json)


def _search_questions(request_json):
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


def _add_question(request_json):
    # error checking
    field_question = request_json.get("question", None)
    field_answer = request_json.get("answer", None)
    field_category = request_json.get("category", None)
    field_difficulty = request_json.get("difficulty", None)

    missing_field = []
    if not field_question:
        missing_field.append("question")
    if not field_answer:
        missing_field.append("answer")
    if not field_category:
        missing_field.append("category")
    if not field_difficulty:
        missing_field.append("difficulty")

    if missing_field:
        raise UnprocessableEntity(missing_field)

    question = Question(
        field_question,
        field_answer,
        field_category,
        field_difficulty
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


@questions_blueprint.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            raise NotFound("questions", question_id)
        question.delete()
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

import json
from json import JSONDecodeError

from flask import Blueprint, request, jsonify

from .client_error_exceptions import BadRequest, UnprocessableEntity
from .models import Question

quizzes_blueprint = Blueprint('quizzes', __name__, url_prefix='')


@quizzes_blueprint.route('/quizzes', methods=['POST'])
def get_next_question():
    data_string = request.data
    try:
        request_json = json.loads(data_string)
    except JSONDecodeError:
        raise BadRequest()

    # error checking
    field_previous_questions = request_json.get("previous_questions", [])
    field_quiz_category = request_json.get("quiz_category", None)

    missing_field = []
    if not field_quiz_category:
        missing_field.append("quiz_category")
    elif not field_quiz_category.get("id", None):
        missing_field.append("quiz_category.id")

    if missing_field:
        raise UnprocessableEntity(missing_field)

    query = Question.query

    # filter by category
    if field_quiz_category["id"] != 0:
        query = query.filter(Question.category == field_quiz_category["id"])

    # filter by id
    for previous_question_id in field_previous_questions:
        query = query.filter(Question.id != previous_question_id)

    question = query.first()

    return jsonify({
        "success": True,
        "question": question.format() if question else None,
    })

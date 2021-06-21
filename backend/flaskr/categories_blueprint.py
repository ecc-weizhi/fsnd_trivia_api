from flask import Blueprint, jsonify

from .models import Category, Question

categories_blueprint = Blueprint('categories', __name__, url_prefix='')


@categories_blueprint.route('/categories/<int:category_id>/questions', methods=['GET'])
def get_questions_by_category(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    formatted_questions = [question.format() for question in questions]

    return jsonify({
        "success": True,
        "questions": formatted_questions,
        "total_questions": len(formatted_questions),
    })


@categories_blueprint.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    id_to_type_map = {}
    for category in categories:
        id_to_type_map[category.id] = category.type

    return jsonify({
        "success": True,
        "categories": id_to_type_map,
    })

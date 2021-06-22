import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.user_name = "weizhi"
        self.password = "test1234"
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.user_name,
                                                               self.password,
                                                               'localhost:5432',
                                                               self.database_name)
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

    def test_no_page_argument_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_page_one_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_page_two_get_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_page_thousand_get_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'], [])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_exist_search_questions(self):
        res = self.client().post('/questions', json={"searchTerm": "xer's original nam"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 1)

    def test_not_exist_search_questions(self):
        res = self.client().post('/questions', json={"searchTerm": "what if this doesnt exist"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'], [])
        self.assertEqual(data['total_questions'], 0)

    def test_malformed_json_post_questions(self):
        res = self.client().post('/questions', data='{"foo":"bar":"hello"}')

        self.assertEqual(res.status_code, 400)

    def test_add_questions(self):
        res = self.client().post('/questions', json={
            "question": "this is question",
            "answer": "this is answer",
            "category": "2",
            "difficulty": "3",
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_missing_fields_add_questions(self):
        res = self.client().post('/questions', json={
            "question": "this is question",
            "category": "2",
            "difficulty": "3",
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_delete_question(self):
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_non_existing_question(self):
        res = self.client().delete('/questions/1000')

        self.assertEqual(res.status_code, 404)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["questions"])
        self.assertEqual(data['total_questions'], len(data["questions"]))

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["categories"])

    def test_post_quizzes(self):
        res = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"id": 2, "type": "Art"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_malformed_json_post_quizzes(self):
        res = self.client().post('/quizzes', data='{"foo":"bar":"hello"}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_missing_field_post_quizzes(self):
        res = self.client().post('/quizzes', json={"previous_questions": []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

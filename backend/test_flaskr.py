import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        DB = 'postgres'
        DB_pass= 'desmond25'
        DB_host = 'localhost:5432'
        self.database_path = "postgresql://{0}:{1}@{2}/{3}".format(DB, DB_pass, DB_host, self.database_name)
        setup_db(self.app, self.database_path)
        self.new_questions = {
             'question': 'What is the name if the longest river',
             'answer': 'River Nile',
             'difficulty': '2',
             'category': '3'
        }

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
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual( res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue( len(data['questions']) )
        self.assertTrue( len(data['categories']) )

    def test_delete_question(self):
        res = self.client().delete('/questions/20')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 20).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(question, None)

    def test_post_questions(self):
        res = self.client().post('/questions', json=self.new_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
                



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
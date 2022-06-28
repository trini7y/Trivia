import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


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
        res = self.client().delete('/questions/13')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 13).one_or_none()

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
                

    def test_search_questions(self):
        res = self.client().post('/questions', json={
            'searchTerm': 'title'
        })
        data = json.loads(res.data)

        db.session.query(Question).filter(db.func.lower(Question.question).like(
            f"%{'title'.lower()}%")).order_by(Question.id).all()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    
    def test_get_question_by_categories(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total'])

    def test_quizzes(self):
        res = self.client().post('/quizzes', json={
            'previous_questions':[],
            'quiz_category': {
                'type': 'click',
                'id': 0
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
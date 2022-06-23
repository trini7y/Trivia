import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

app = Flask(__name__)
setup_db(app)

"""
 @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
"""
cors = CORS(app, resources={
    r"/api/":{'origins':"*"}
})

# Pagination function
def paginate_questions(request, selection):
    page  = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    question = [quest.format() for quest in selection]
    current_question = question[start:end]
    return current_question

"""
 @TODO: Use the after_request decorator to set Access-Control-Allow
"""
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

"""
@TODO:
Create an endpoint to handle GET requests
for all available categories.
"""
@app.route('/categories', methods=['GET'])
def getCategories():
    categories = Category.query.all()
    # db.session.query(Category.id).all()
    getData = {}
    for category in categories:
            getData[str(category.id)] = category.type

    return jsonify({
        'success': True,
        'categories': getData
    })
"""
@TODO:
Create an endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions.
"""
@app.route('/questions', methods=['GET'])
def questions():
    question = Question.query.order_by(Question.id).all()
    currentQuestions = paginate_questions(request, question)
    categories = Category.query.all()
    currentCategory = Category.query.filter(Question.category == Category.id).first()
    getData = {}
    for category in categories:
            getData[str(category.id)] = category.type

    return jsonify({
        'success': True,
        'questions': currentQuestions,
        'total_questions': len(question),
        'categories':getData,
        'current_category': currentCategory.format()
    })

"""
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
"""

@app.route('/questions/<int:question_id>', methods=['DELETE'])

def delete_question(question_id):
    try:
        question = Question.query.filter( Question.id == question_id).first()
        if question is None:
            abort(404)

        question.delete()

        question = Question.query.order_by(Question.id).all()
        currentQuestions = paginate_questions(request, question)
        categories = Category.query.all()
        currentCategory = Category.query.filter(Question.category == Category.id).first()
        getData = {}
        for category in categories:
                getData[str(category.id)] = category.type

        return jsonify({
            'success': True,
            'questions': currentQuestions,
            'total_questions': len(question),
            'categories':getData,
            'current_category': currentCategory.format()
        })
    except:
        abort(404)


"""
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
"""
@app.route('/questions', methods=['POST'])
def add_question():
    data = request.get_json()
    
    new_question = data.get('question', None)
    new_answer = data.get('answer', None)
    new_difficulty = data.get('difficulty', None)
    new_category = data.get('difficulty',  None)

    try:
        quest = Question(question = new_question, answer = new_answer, 
                    difficulty = new_difficulty, category = new_category)
        quest.insert()
        return jsonify({
        'success': True,
    })
    except:
        abort(404)



"""
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
"""

"""
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
"""

@app.route('/categories/<int:id>/questions', methods=['GET'])
def getCategoriesById(id):
    questions = Question.query.filter(id == Question.category).all()
    currentCategory = None
    quest = []
    print(questions)
    for question in questions:
        currentCategory = Category.query.filter(question.category == Category.id).first()
        quest.append( {
            'id': question.id,
            'question': question.question,
            'answer': question.answer,
            'difficulty': question.difficulty,
            'category': question.category
        } )

    print(quest)
    return jsonify({
        'success':True,
        'questions': quest,
        'total': len(quest),
        'currentCategory':  currentCategory.format()
    })



"""
@TODO:
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
"""

"""
@TODO:
Create error handlers for all expected errors
including 404 and 422.
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
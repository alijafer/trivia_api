import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, paginate_questions


QUESTIONS_PER_PAGE = 10




def create_app():
    '''
    create and configure the Flask application
    return Flask application
    '''
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})         #Set up CORS. Allow '*' for origins
  
    @app.after_request
    def after_request(response):
      '''
      after_request is access control for response to set Access-Control-Allow to Headers
      parameter response: HTTP Response
      return response: Add HTTP headers
      '''
      response.headers.add('Access-Control-Allow-Headers',\
                         'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',\
                         'GET,PUT,POST,DELETE,OPTIONS,PATCH')
      return response
    


    @app.route('/categories', methods=['GET'])
    @app.route('/category', methods=['GET'])
    def getAllCategories():
        '''
        Get all categories/category endpoint
        This endpoint returns all categories or
        status code 500 if there is a server error
        '''
        try:
            categories = {}
            category_query = Category.query.all()
            for category in category_query:
                categories[category.id] = category.type.format()
            return jsonify({
                'success': True,
                'categories': categories
            })
        except Exception:
            abort(500)
       

    @app.route('/question', methods=['GET'])
    @app.route('/questions', methods=['GET'])
    def getQuestions():
        '''
      An endpoint to handle GET requests for questions, 
      including pagination (every 10 questions). 
      return a list of questions, number of total questions,
              current category, categories.
      and return 404 if not found page
      QUESTIONS_PER_PAGE = 10 global define var 
     
        '''
        try:
            questions = Question.query.order_by(Question.id).all()
            total_questions = len(questions)
            category_query = Category.query.order_by(Category.id).all()

            current_questions = paginate_questions(
                request, questions,
                QUESTIONS_PER_PAGE)
            if (len(current_questions) is 0):
                abort(404)
            categories = {}
            for category in category_query:
                categories[category.id] = category.type.format()
            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': total_questions,
                'categories': categories
            })
        except Exception:
            abort(500)
    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def deleteQuestion(question_id):
        '''
        An endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
      '''
        try:
            question= Question.query.get(question_id)
            question.delete()
            return jsonify({
              'success': True,
              'message': "Question successfully deleted",
              'delete_id': question_id

            })
        except Exception:
            abort(422)
    

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
  Error handlers for all expected errors 
  including 404, 422, 400, and 500. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
      "success": False, 
      "error": 500,
      "message": "Internal Server Error"
      }), 500
    return app

    
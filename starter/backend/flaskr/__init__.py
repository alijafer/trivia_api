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
            if (len(current_questions) == 0):
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
    @app.route('/question/<int:question_id>', methods=['DELETE'])
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
    

    @app.route('/questions', methods=['POST'])
    def createQuestion():
        '''
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
        '''
        questionData = ''
        questionData = request.get_json()
        question = questionData.get('question')
        answer = questionData.get('answer')
        difficulty = questionData.get('difficulty')
        category = questionData.get('category')
        if not (question or answer or difficulty or category):
           abort(422)
        try:
            questionInsert= Question(
              question = question.format(),
              answer = answer.format(),
              difficulty = difficulty.format(),
              category = category.format() 
            )
            questionInsert.insert()
            return jsonify({
              'success': True,
              'question': questionInsert
            })
        except Exception:
          abort(422)
        
  
    @app.route('/questions/search', methods=['POST'])
    def searchQuestion():
    
        '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
    Try using the word "title" to start. 
        '''
        searchTerm = '' 
        searchData = request.get_json()
        searchTerm = searchData.get('searchTerm', '') 
        #print(searchTerm)
        if searchTerm == '':
          print("sear")
          abort(422)
        try:
            question1 = ''
            question1 = Question.query.filter(
                Question.question.ilike(f'%{searchTerm}%')).all()
            #print(question1)
            print(type(question1))
            if question1 == 0:
                abort(404)
            else:
                current_questions = paginate_questions(
                  request, question1,
                  QUESTIONS_PER_PAGE) 
              
                
                for category in current_questions:
                      current_category = category['category']
                    
                return jsonify({
                  'success': True,
                  'question': current_questions,
                  'totalQuestions': len(current_questions),
                  'current_category': current_category
                })

        except Exception:
          print("excep")
          abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def getQuestionsOnCategory(category_id):
          
        '''
 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
        '''
        try:
            category_query = Category.query.filter_by(id=category_id).one_or_none()

            questions = Question.query.filter_by(category=category_id).all()
            total_questions = len(questions)
            current_questions = paginate_questions(
                request, questions,
                QUESTIONS_PER_PAGE)
            
            
            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': total_questions,
                'categories': category_query.type
            })
        except Exception:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def quizPlay():
      '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
      '''
      quizData = request.get_json()
      previous_questions = quizData.get('previous_questions', '') 
      quiz_category = quizData.get('quiz_category', '') 
      if ((quiz_category is None) or (previous_questions is None)):
          abort(400)
      
      
      category_id = int(quiz_category)
      if category_id == 0:
          questions = Question.query.all()
      else:
          questions = Question.query.filter_by(
                category=category_id).all()

      
      def getRandomQuestions():
          randomQuestions = questions[random.randint(0, len(questions)-1)]
          if not randomQuestions.id in previous_questions:
              return randomQuestions 
          else:
              print(".")
              return getRandomQuestions()
          
      
      nextQ = getRandomQuestions()
      
             
      return jsonify({
            'success': True,
            'question': nextQ.format()
      })
      
      print(Question.query.all())
      
      

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

    
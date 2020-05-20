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
        after_request is access control for response \
             to set Access-Control-Allow to Headers
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
      return a list of questions, number of total questions,\
          current category, categories.
      and return 404 if not found page
      QUESTIONS_PER_PAGE = 10 global define var 
      Two routes if use in traminal you can use single or collection sentence
     
        '''
        
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
        


    @app.route('/question/<int:question_id>', methods=['DELETE'])
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def deleteQuestion(question_id):
        '''
        An endpoint to DELETE question using a question ID. 
        if any erorr expet send 422 
        Two routes if use in traminal you can use single or collection sentence
    
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
     An endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    if question or answer text, category,
     or difficulty score not exit get 422 unprocessable.

    return and insert: question and answer text, 
    category, and difficulty score 
 
        '''
        questionData = ''
        questionData = request.get_json()
        question = questionData.get('question')
        answer = questionData.get('answer')
        difficulty = questionData.get('difficulty')
        category = questionData.get('category')
        print(question)
        
        if ((question == '') or (answer=='') or 
                (difficulty=='') or (category=='')):
            abort(422)
        
        try:
            questionInsert= Question(
              question = question,
              answer = answer,
              difficulty = difficulty,
              category = category
            )
            
            questionInsert.insert()
            return jsonify({
              'success': True,
              'question': question,
              'answer': answer,
              'difficulty': difficulty,
              'category': category
            })
        except Exception:
            abort(422)
        
  

    @app.route('/questions/search', methods=['POST'])
    def searchQuestion():
    
        '''
  A POST endpoint to get questions based on a search term. 
    return any questions for whom the search term is a substring of the question,\
        totalQuestions and current_category
    if search term return 422 
    if not exit return 404 not found
   
        '''
        searchTerm = '' 
        searchData = request.get_json()
        searchTerm = searchData.get('searchTerm', '') 
        
        if searchTerm == '':
            print("sear")
            abort(422)
        try:
            question1 = ''
            question1 = Question.query.filter(
                Question.question.ilike(f'%{searchTerm}%')).all()
            
            
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
                  'questions': current_questions,
                  'totalQuestions': len(current_questions),
                  'current_category': current_category
                })

        except Exception:
          abort(404)



    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def getQuestionsOnCategory(category_id):
          
        '''
        A GET endpoint to get questions based on category. 
        return: return 'success': True, get maximum 10 questions,\
            totalQuestions, type of category
        if any problem like category not exit except 404 
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
  A POST endpoint to get questions to play the quiz. 
  This endpoint take category and previous question parameters from POST requset
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  if quiz_category empty or previous_questions empty return 400 bad request

   
      '''
      quizData = request.get_json()
      previous_questions = quizData.get('previous_questions', '') 
      quiz_category = quizData.get('quiz_category', '') 
      if ((quiz_category is None) or (previous_questions is None)):
          abort(400)
      
      
      category_id = int(quiz_category['id'])
      if category_id == 0:
          questions = Question.query.all()
      else:
          questions = Question.query.filter_by(
                category=category_id).all()

      
      def getRandomQuestions():
          '''
          find the random question that not in the previous questions
          random the <int:id> of question 
          if exit in previous questions recall self until found elamunt not exit
          return random question not exit in previous questions
          
          '''
          randomQuestions = questions[random.randint(0, len(questions)-1)]
          if not randomQuestions.id in previous_questions:
              return randomQuestions 
          else:
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

    
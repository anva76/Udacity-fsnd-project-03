import os
import json
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_cors import CORS
from database.models import db_drop_and_create_all, Drink, db
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
CORS(app)


def config_and_init_db():
    app.config.from_object('config.DevConfig')
    db.init_app(app)

    #with app.app_context():
        #db_drop_and_create_all()


'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

# Error response with a specific message
def error_response(message, code):
    return jsonify({
        'success': False,
        'error': code,
        'message': message
    }), code


# GET /drinks endpoint
# -----------------------------------------------------------------------
@app.get('/drinks')
def get_drinks():
    drinks = [
        x.short()
        for x in Drink.query.all()
    ]

    return jsonify({
        'success': True,
        'drinks': drinks,
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.get('/drinks-detail')
def get_drinks_detailed():
    drinks = [
        x.long()
        for x in Drink.query.all()
    ]

    return jsonify({
        'success': True,
        'drinks': drinks,
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

# Validate a new or patched drink
# -----------------------------------------------------------
def validate_drink(request, patched=False):
    body = request.get_json()
    print(body)

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if not all([title, recipe]) and not patched:
        return None, None, None
    
    if title:
        title = title.strip()
        if len(title) == 0:
            return None, None, None            

    if recipe:
        if not all([isinstance(recipe, list), len(recipe)]):
            return None, None, None        

        # check the ingredients
        for ingred in recipe:
            if not isinstance(ingred, dict):
                return None, None, None
            
            if not all([
                        'parts' in ingred, 
                        'color' in ingred, 
                        'name' in ingred
                        ]):
                return None, None, None     

            ingred['color'] = ingred['color'].strip()
            ingred['name'] = ingred['name'].strip()
            
            if not all([len(ingred['color']), len(ingred['name'])]):
                return None, None, None       

            # assert 'parts' is an integer
            try: 
                ingred['parts'] = int(ingred['parts'])
            except ValueError:
                return None, None, None
    
    return True, title, recipe

# Add a new drink
# -----------------------------------------------------------
@app.post('/drinks')
def post_drinks():
    error = False
    result, title, recipe = validate_drink(request)
    if result is None:
        abort(400)

    drink = Drink()
    drink.title = title
    drink.recipe = json.dumps(recipe)

    try:
        drink.insert()
    except Exception as e:
        error = True
        db.session.rollback()
        print(str(e))

    if error:
        return error_response(
                'Server error. New drink could not be created.',
                500
                )
    else:
        return jsonify({
          'success': True,
          'drink': drink.long()
        })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

# Patch a drink
# ---------------------------------------------------------------------
@app.patch('/drinks/<int:drink_id>')
def patch_drinks(drink_id):
    error = False
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)

    result, title, recipe = validate_drink(request, patched=True)
    if result is None:
        abort(400)

    if title:
        drink.title = title

    if recipe:
        drink.recipe = json.dumps(recipe)

    try:
        drink.update()
    except Exception as e:
        error = True
        db.session.rollback()
        print(str(e))

    if error:
        return error_response(
                f'Server error. Drink id:{drink_id} could not be updated.',
                500
                )
    else:
        return jsonify({
          'success': True,
          'drink': drink.long()
        })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.delete('/drinks/<int:drink_id>')
def delete_drinks(drink_id):
    error = False
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)

    try:
        drink.delete()
    except Exception as e:
        error = True
        db.session.rollback()
        print(str(e))

    if error:
        return error_response(
                f'Server error. Drink id:{drink_id} could not be deleted.',
                500
                )
    else:
        return jsonify({
            'success': True,
            'delete': drink_id
        })    

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "entity not found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Invalid request',
    }), 400


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error',
    }), 500


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

if __name__ == '__main__':
    config_and_init_db()
    app.run()
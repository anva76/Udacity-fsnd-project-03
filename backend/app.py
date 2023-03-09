import os
import json
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_cors import CORS
from sqlalchemy import func as fn
from database.models import db_drop_and_create_all, Drink, db
from auth.auth import AuthError, requires_auth, get_token_from_auth_header

app = Flask(__name__)
CORS(app)


def config_and_init_db():
    app.config.from_object('config.DevConfig')
    db.init_app(app)
    with app.app_context():
        db_drop_and_create_all()


# Error response with a specific message if necessary
def error_response(message, code):
    return jsonify({
        'success': False,
        'error': code,
        'message': message
    }), code


# get drinks
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


# get detailed drinks
# -----------------------------------------------------------------------
@app.get('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detailed():
    drinks = [
        x.long()
        for x in Drink.query.all()
    ]

    return jsonify({
        'success': True,
        'drinks': drinks,
    })


# Check if the drink title is unique
# ___________________________________________________________
def confirm_drink_title_unique(new_title, current_title=None, patched=False):
    if patched:
        drink = Drink.query.filter(
                fn.lower(Drink.title) == fn.lower(new_title),
                fn.lower(Drink.title) != fn.lower(current_title)
            ).one_or_none()
        if drink:
            return False
    else:
        drink = Drink.query.filter(
                fn.lower(Drink.title) == fn.lower(new_title)
             ).one_or_none()
        if drink:
            return False

    return True


# Validate a new or patched drink
# -----------------------------------------------------------
def validate_drink(request, patched=False):
    body = request.get_json()
    # print(body)

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
@requires_auth('post:drinks')
def post_drinks():
    error = False
    result, title, recipe = validate_drink(request)
    if result is None:
        abort(400)

    if not confirm_drink_title_unique(title):
        return error_response('This drink title already exists.', 400)

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
          'drinks': [drink.long()]
        })


# Patch a drink
# ---------------------------------------------------------------------
@app.patch('/drinks/<int:drink_id>')
@requires_auth('patch:drinks')
def patch_drinks(drink_id):
    error = False
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)

    result, title, recipe = validate_drink(request, patched=True)
    if result is None:
        abort(400)

    if not confirm_drink_title_unique(title, drink.title, True):
        return error_response('This drink already exists.', 400)

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
          'drinks': [drink.long()]
        })


@app.delete('/drinks/<int:drink_id>')
@requires_auth('delete:drinks')
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
# -----------------------------------------------------------------------
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


@app.errorhandler(403)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Access denied',
    }), 403


@app.errorhandler(401)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized',
    }), 401


# AuthError handler
# ---------------------------------------------------------
@app.errorhandler(AuthError)
def handle_auth_error(e):
    return jsonify({
        'success': False,
        'error': e.status_code,
        'message': e.error['description'],
        'message_code': e.error['code']
    }), e.status_code


if __name__ == '__main__':
    config_and_init_db()
    app.run()

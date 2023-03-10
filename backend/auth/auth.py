import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from config import AuthConfig

AUTH0_DOMAIN = AuthConfig.AUTH0_DOMAIN
ALGORITHMS = AuthConfig.ALGORITHMS
API_AUDIENCE = AuthConfig.API_AUDIENCE


# AuthError Exception
# Note: This code is based on examples provided by Auth0.com
# -----------------------------------------------------------------------
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Extract token from http authentication header
# Note: This code is based on examples provided by Auth0.com
# ----------------------------------------------------------------------
def get_token_from_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


# Check the scope of permissions
# Note: This code is based on examples provided by Auth0.com
# ----------------------------------------------------------------------
def check_permissions(requested_permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_payload',
            'description': 'Invalid payload.'
        }, 401)

    token_permissions = payload['permissions']
    # print(token_permissions, requested_permission)

    if requested_permission not in token_permissions:
        raise AuthError({
            'code': 'access_denied',
            'description': 'Access denied.'
        }, 403)

    return True


# Validate and decode JWT token
# Note: This code is based on examples provided by Auth0.com
# ----------------------------------------------------------------------
def validate_jwt_token(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Audience or issuer may be incorrect.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


# Authentication decorator to protect Flask app routes
# Note: This code is based on examples provided by Auth0.com
# ----------------------------------------------------------------------
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print('====> inside @requires_auth')
            token = get_token_from_auth_header()
            payload = validate_jwt_token(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator

from flask import request, make_response
import hashlib
import jwt
import datetime

def hash_password(password: str, username: str) -> str:
    hash_string = (username + password)
    hash_string = hash_string.encode("utf8")
    result = hashlib.sha256(hash_string).hexdigest()
    return result


def get_token() -> str:
    return request.headers.get('Authorization')


def set_token(token: str):
    response = make_response()
    response.set_cookie("token", value = token, max_age = None, expires = None, path = '/', domain = None,
                        secure = None, httponly = True)
    return response



def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ",
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

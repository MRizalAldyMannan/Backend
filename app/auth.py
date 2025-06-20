import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User

def generate_tokens(user_id):
    """Generate access and refresh tokens for a user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
        'iat': datetime.datetime.utcnow(),
        'type': 'access'
    }
    
    access_token = jwt.encode(
        payload, 
        current_app.config['JWT_SECRET_KEY'], 
        algorithm='HS256'
    )
    
    refresh_payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
        'iat': datetime.datetime.utcnow(),
        'type': 'refresh'
    }
    
    refresh_token = jwt.encode(
        refresh_payload, 
        current_app.config['JWT_SECRET_KEY'], 
        algorithm='HS256'
    )
    
    return access_token, refresh_token

def verify_token(token):
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(
            token, 
            current_app.config['JWT_SECRET_KEY'], 
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    """Get current user from token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(' ')[1]  # Bearer <token>
    except IndexError:
        return None
    
    payload = verify_token(token)
    if not payload or payload.get('type') != 'access':
        return None
    
    user = User.query.get(payload['user_id'])
    return user

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_user_from_token(f):
    """Decorator to get user from token and pass to function"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        return f(user, *args, **kwargs)
    return decorated_function 
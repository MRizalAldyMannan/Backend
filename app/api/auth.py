from flask import jsonify, request
from app import db
from app.models import User
from app.api import bp
from app.auth import generate_tokens
from marshmallow import Schema, fields, ValidationError

class LoginSchema(Schema):
    """Login request schema"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class RegisterSchema(Schema):
    """Register request schema"""
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)

login_schema = LoginSchema()
register_schema = RegisterSchema()

@bp.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    access_token, refresh_token = generate_tokens(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

@bp.route('/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Generate tokens for the new user
    access_token, refresh_token = generate_tokens(user.id)
    
    return jsonify({
        'message': 'Registration successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 201

@bp.route('/auth/me', methods=['GET'])
def get_current_user_info():
    """Get current user information"""
    from app.auth import get_current_user
    
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }), 200 
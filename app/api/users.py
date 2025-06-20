from flask import jsonify, request
from app import db
from app.models import User
from app.api import bp
from marshmallow import Schema, fields, ValidationError
from app.auth import login_required

class UserSchema(Schema):
    """User serialization schema"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@bp.route('/users', methods=['GET'])
@login_required
def get_users():
    """Get all users (requires authentication)"""
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@bp.route('/users/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    """Get a specific user (requires authentication)"""
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user))

@bp.route('/users', methods=['POST'])
@login_required
def create_user():
    """Create a new user (requires authentication)"""
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user_schema.dump(user)), 201

@bp.route('/users/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    """Update a user (requires authentication)"""
    user = User.query.get_or_404(id)
    
    try:
        data = user_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    for field, value in data.items():
        setattr(user, field, value)
    
    db.session.commit()
    return jsonify(user_schema.dump(user))

@bp.route('/users/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    """Delete a user (requires authentication)"""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204 
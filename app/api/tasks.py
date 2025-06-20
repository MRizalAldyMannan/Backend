from flask import jsonify, request
from app import db
from app.models import Task, User
from app.api import bp
from app.auth import login_required, get_user_from_token
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

class TaskSchema(Schema):
    """Task serialization schema"""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    status = fields.Str(validate=lambda x: x in ['pending', 'in_progress', 'completed'])
    priority = fields.Str(validate=lambda x: x in ['low', 'medium', 'high'])
    due_date = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)  # Now automatically set from token

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@bp.route('/tasks', methods=['GET'])
@login_required
@get_user_from_token
def get_tasks(user):
    """Get all tasks for the authenticated user with optional filtering"""
    # Query parameters for filtering
    status = request.args.get('status')
    priority = request.args.get('priority')
    
    query = Task.query.filter(Task.user_id == user.id)
    
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    
    tasks = query.all()
    return jsonify(tasks_schema.dump(tasks))

@bp.route('/tasks/<int:id>', methods=['GET'])
@login_required
@get_user_from_token
def get_task(user, id):
    """Get a specific task (only if owned by authenticated user)"""
    task = Task.query.filter_by(id=id, user_id=user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task_schema.dump(task))

@bp.route('/tasks', methods=['POST'])
@login_required
@get_user_from_token
def create_task(user):
    """Create a new task for the authenticated user"""
    try:
        data = task_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Set user_id from authenticated user
    data['user_id'] = user.id
    
    task = Task(**data)
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task_schema.dump(task)), 201

@bp.route('/tasks/<int:id>', methods=['PUT'])
@login_required
@get_user_from_token
def update_task(user, id):
    """Update a task (only if owned by authenticated user)"""
    task = Task.query.filter_by(id=id, user_id=user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        data = task_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Ensure user_id cannot be changed
    if 'user_id' in data:
        del data['user_id']
    
    for field, value in data.items():
        setattr(task, field, value)
    
    db.session.commit()
    return jsonify(task_schema.dump(task))

@bp.route('/tasks/<int:id>', methods=['DELETE'])
@login_required
@get_user_from_token
def delete_task(user, id):
    """Delete a task (only if owned by authenticated user)"""
    task = Task.query.filter_by(id=id, user_id=user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    return '', 204

@bp.route('/tasks/<int:id>/status', methods=['PATCH'])
@login_required
@get_user_from_token
def update_task_status(user, id):
    """Update task status (only if owned by authenticated user)"""
    task = Task.query.filter_by(id=id, user_id=user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    if data['status'] not in ['pending', 'in_progress', 'completed']:
        return jsonify({'error': 'Invalid status'}), 400
    
    task.status = data['status']
    db.session.commit()
    
    return jsonify(task_schema.dump(task)) 
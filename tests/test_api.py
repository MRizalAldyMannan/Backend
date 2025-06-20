import pytest
from app import create_app, db
from app.models import User, Task
from config import TestingConfig

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test runner"""
    return app.test_cli_runner()

def test_get_users_empty(client):
    """Test getting users when none exist"""
    response = client.get('/api/users')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_user(client):
    """Test creating a new user"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    response = client.post('/api/users', json=user_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'
    assert 'id' in data

def test_create_user_duplicate_username(client):
    """Test creating user with duplicate username"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    # Create first user
    client.post('/api/users', json=user_data)
    
    # Try to create second user with same username
    user_data2 = {
        'username': 'testuser',
        'email': 'test2@example.com'
    }
    response = client.post('/api/users', json=user_data2)
    assert response.status_code == 400

def test_get_tasks_empty(client):
    """Test getting tasks when none exist"""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_task(client):
    """Test creating a new task"""
    # First create a user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    user_response = client.post('/api/users', json=user_data)
    user_id = user_response.get_json()['id']
    
    # Create task
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'priority': 'high',
        'user_id': user_id
    }
    response = client.post('/api/tasks', json=task_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['title'] == 'Test Task'
    assert data['description'] == 'Test Description'
    assert data['priority'] == 'high'
    assert data['user_id'] == user_id

def test_create_task_invalid_user(client):
    """Test creating task with non-existent user"""
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'priority': 'high',
        'user_id': 999  # Non-existent user
    }
    response = client.post('/api/tasks', json=task_data)
    assert response.status_code == 404

def test_update_task_status(client):
    """Test updating task status"""
    # Create user and task
    user_data = {'username': 'testuser', 'email': 'test@example.com'}
    user_response = client.post('/api/users', json=user_data)
    user_id = user_response.get_json()['id']
    
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'user_id': user_id
    }
    task_response = client.post('/api/tasks', json=task_data)
    task_id = task_response.get_json()['id']
    
    # Update status
    status_data = {'status': 'completed'}
    response = client.patch(f'/api/tasks/{task_id}/status', json=status_data)
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'completed' 
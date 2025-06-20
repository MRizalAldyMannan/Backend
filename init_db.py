#!/usr/bin/env python3
"""
Database initialization script
Creates the database and adds sample data
"""

from app import create_app, db
from app.models import User, Task
from datetime import datetime, timedelta

def init_db():
    """Initialize the database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create sample users
        user1 = User(username='john_doe', email='john@example.com')
        user2 = User(username='jane_smith', email='jane@example.com')
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        # Create sample tasks
        tasks = [
            Task(
                title='Complete project documentation',
                description='Write comprehensive documentation for the new feature',
                status='pending',
                priority='high',
                due_date=datetime.utcnow() + timedelta(days=7),
                user_id=user1.id
            ),
            Task(
                title='Review code changes',
                description='Review pull request #123 for the authentication module',
                status='in_progress',
                priority='medium',
                due_date=datetime.utcnow() + timedelta(days=3),
                user_id=user1.id
            ),
            Task(
                title='Setup development environment',
                description='Install and configure all required tools and dependencies',
                status='completed',
                priority='low',
                user_id=user2.id
            ),
            Task(
                title='Write unit tests',
                description='Create comprehensive test coverage for the API endpoints',
                status='pending',
                priority='high',
                due_date=datetime.utcnow() + timedelta(days=5),
                user_id=user2.id
            )
        ]
        
        for task in tasks:
            db.session.add(task)
        
        db.session.commit()
        
        print("Database initialized successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Task.query.count()} tasks")

if __name__ == '__main__':
    init_db() 
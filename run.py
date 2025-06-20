from app import create_app, db
from app.models import User, Task

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Make shell context for Flask CLI"""
    return {
        'db': db,
        'User': User,
        'Task': Task
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 
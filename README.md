# Task Management Backend

A Flask-based REST API for task management with JWT authentication, clean architecture, and best practices.

## Features

- **JWT Authentication**: Secure login/register with bearer token authentication
- **User Management**: Create, read, update, and delete users (authenticated)
- **Task Management**: Full CRUD operations for tasks with user-specific access
- **Database**: SQLAlchemy ORM with SQLite (configurable for production)
- **API Documentation**: RESTful API with proper error handling
- **Validation**: Request validation using Marshmallow schemas
- **CORS Support**: Cross-origin resource sharing enabled
- **Password Security**: Secure password hashing with Werkzeug

## Project Structure

```
backend-task-management/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── auth.py              # JWT authentication utilities
│   ├── api/                 # API blueprints
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── users.py         # User endpoints (authenticated)
│   │   ├── tasks.py         # Task endpoints (authenticated)
│   │   ├── health.py        # Health check endpoint
│   │   └── errors.py        # API error handlers
│   └── errors/              # Global error handlers
│       ├── __init__.py
│       └── handlers.py
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── init_db.py              # Database initialization script
├── Makefile                # Development commands
├── .gitignore              # Git ignore rules
├── Task_Management_API.postman_collection.json    # Postman collection
├── Task_Management_API.postman_environment.json   # Postman environment
└── README.md               # This file
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///app.db
FLASK_APP=run.py
FLASK_ENV=development
```

### 4. Initialize Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5001`

**Note**: The application runs on port 5001 to avoid conflicts with macOS AirPlay service on port 5000.

## Postman Collection

This project includes a complete Postman collection for easy API testing and documentation.

### Import Postman Collection

1. **Download Postman** (if not already installed) from [postman.com](https://www.postman.com/downloads/)

2. **Import Collection**:
   - Open Postman
   - Click "Import" button
   - Select `Task_Management_API.postman_collection.json`
   - Click "Import"

3. **Import Environment**:
   - Click "Import" again
   - Select `Task_Management_API.postman_environment.json`
   - Click "Import"

4. **Select Environment**:
   - In the top-right dropdown, select "Task Management API Environment"

### Using the Postman Collection

The collection includes:

#### 🔐 **Authentication Flow**
- **Register User**: Creates account and automatically saves tokens
- **Login User**: Authenticates and automatically saves tokens
- **Get Current User**: Retrieves authenticated user info

#### 👥 **Users Endpoints** (All require authentication)
- Get All Users
- Get User by ID
- Create User
- Update User
- Delete User

#### 📋 **Tasks Endpoints** (All require authentication)
- Get All Tasks
- Get Tasks with Filters
- Get Task by ID
- Create Task
- Update Task
- Update Task Status
- Delete Task

#### 🎯 **Smart Features**
- **Auto-token management**: Tokens are automatically saved after login/register
- **Auto-ID tracking**: Task IDs are automatically saved after creation
- **Environment variables**: All URLs use `{{base_url}}` variable
- **Proper headers**: All authenticated requests include Bearer token
- **Example data**: Realistic request bodies for testing

### Quick Start with Postman

1. **Start your Flask server**: `python run.py`
2. **Test Health Check**: Run "Check API Health" to verify server is running
3. **Register/Login**: Run "Register User" or "Login User" to get tokens
4. **Test Protected Endpoints**: All other endpoints will now work with saved tokens

### Environment Variables

The collection automatically manages these variables:
- `base_url`: http://localhost:5001
- `access_token`: Auto-populated after login/register
- `refresh_token`: Auto-populated after login/register
- `user_id`: Auto-populated after login/register
- `task_id`: Auto-populated after creating a task

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Most endpoints require a valid bearer token.

### Authentication Flow

1. **Register** or **Login** to get access and refresh tokens
2. Include the access token in the `Authorization` header for protected endpoints
3. Use refresh token to get new access token when it expires

### Token Format

```
Authorization: Bearer <access_token>
```

## API Endpoints

### Health Check
- `GET /api/health` - Check API and database status

### Authentication (Public)

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info (authenticated)

### Users (Authenticated)

- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get specific user
- `POST /api/users` - Create new user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user

### Tasks (Authenticated)

- `GET /api/tasks` - Get user's tasks (with optional filtering)
- `GET /api/tasks/<id>` - Get specific task (user's own)
- `POST /api/tasks` - Create new task (assigned to user)
- `PUT /api/tasks/<id>` - Update task (user's own)
- `DELETE /api/tasks/<id>` - Delete task (user's own)
- `PATCH /api/tasks/<id>/status` - Update task status (user's own)

### Query Parameters for Tasks

- `status`: Filter by status (pending, in_progress, completed)
- `priority`: Filter by priority (low, medium, high)

## Example API Usage

### Check API Health

```bash
curl http://localhost:5001/api/health
```

### Register a New User

```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Login

```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "password123"
  }'
```

### Create a Task (Authenticated)

```bash
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the project",
    "priority": "high",
    "status": "pending"
  }'
```

### Get User's Tasks (Authenticated)

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  "http://localhost:5001/api/tasks?status=pending"
```

### Get All Users (Authenticated)

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  http://localhost:5001/api/users
```

### Update Task Status (Authenticated)

```bash
curl -X PATCH http://localhost:5001/api/tasks/1/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"status": "completed"}'
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
```

### Linting

```bash
flake8
```

### Using Makefile

```bash
make install    # Install dependencies
make run        # Run the application
make test       # Run tests
make init-db    # Initialize database
make format     # Format code
make lint       # Run linting
make clean      # Clean cache files
```

## Database Models

### User Model

- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password using Werkzeug
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Task Model

- `id`: Primary key
- `title`: Task title
- `description`: Task description
- `status`: Task status (pending, in_progress, completed)
- `priority`: Task priority (low, medium, high)
- `due_date`: Due date (optional)
- `user_id`: Foreign key to User (automatically set from token)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Configuration

The application supports different configuration environments:

- **Development**: Debug mode enabled, SQLite database
- **Production**: Debug disabled, configurable database URL
- **Testing**: In-memory SQLite database

### JWT Configuration

- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `JWT_ACCESS_TOKEN_EXPIRES`: Access token expiration (default: 1 hour)
- `JWT_REFRESH_TOKEN_EXPIRES`: Refresh token expiration (default: 30 days)

## Security Features

- **Password Hashing**: Passwords are securely hashed using Werkzeug
- **JWT Tokens**: Secure token-based authentication
- **User Isolation**: Users can only access their own tasks
- **Token Expiration**: Automatic token expiration for security
- **Input Validation**: All inputs validated using Marshmallow schemas

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (missing or invalid token)
- `404`: Not Found
- `500`: Internal Server Error

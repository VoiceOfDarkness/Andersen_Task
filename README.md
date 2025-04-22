# TODO list API

An asynchronous REST API for task management built with FastAPI, SQLAlchemy, and PostgreSQL.

## 📋 Overview

TODO list API is a task management system that allows users to create, update, delete, and track tasks. Built on
FastAPI's asynchronous framework, it provides high-performance API endpoints with automatic validation, serialization,
and documentation.
<p align="center">
  <img src="https://github.com/VoiceOfDarkness/Andersen_Task/blob/main/images/img.png" alt="Project Logo" width="200"/>
</p>
## ✨ Features

- **User Authentication**: Secure JWT-based authentication with token refresh mechanism
- **Task Management**: Full CRUD operations for tasks
- **Pagination**: Efficient handling of large datasets with pagination support
- **Filtering**: Filter tasks by status
- **Dependency Injection**: Clean architecture using dependency containers
- **Documentation**: Auto-generated API documentation
- **Docker Support**: Easy deployment with Docker and Docker Compose

## 🛠️ Tech Stack

- **Python 3.13**: Modern Python features and syntax
- **FastAPI**: High-performance async web framework
- **Dependecy Injector**: For dependency injection
- **SQLAlchemy (Async)**: ORM for database interactions
- **PostgreSQL**: Robust relational database
- **Poetry**: Dependency management
- **Docker**: Containerization
- **JWT**: Authentication mechanism

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/VoiceOfDarkness/Andersen_Task.git
cd Andersen_Task
```

2. Create a `.env` file in the project root with the following variables:

```
# Database settings
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=taskmaster
POSTGRES_HOST=database
POSTGRES_PORT=5432

# Application settings
SECRET_KEY=your-secret-key
```

3. Build and start the Docker containers:

```bash
docker-compose up --build -d
```

4. The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📝 Project Structure

```
├── app
│   ├── api                    # API endpoints and routing
│   │   ├── deps.py            # Dependency functions
│   │   ├── main.py            # API initialization
│   │   └── v1                 # API version 1
│   │       └── routes         # Route definitions
│   │           ├── auth.py    # Authentication routes
│   │           ├── task.py    # Task management routes
│   │           └── user.py    # User management routes
│   ├── core                   # Core application modules
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection
│   │   ├── di.py              # Dependency injection container
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── security.py        # Security utilities
│   ├── main.py                # Application entry point
│   ├── models                 # SQLAlchemy ORM models
│   │   ├── base.py            # Base model class
│   │   ├── task.py            # Task model
│   │   └── user.py            # User model
│   ├── repository             # Data access layer
│   │   ├── base_repository.py # Base repository pattern
│   │   ├── task_repository.py # Task repository
│   │   └── user_repository.py # User repository
│   ├── schemas                # Pydantic schemas for validation
│   │   ├── auth.py            # Authentication schemas
│   │   ├── pagination.py      # Pagination schemas
│   │   ├── task.py            # Task schemas
│   │   └── user.py            # User schemas
│   └── services               # Business logic layer
│       ├── auth_service.py    # Authentication service
│       ├── base_service.py    # Base service pattern
│       ├── task_service.py    # Task service
│       └── user_service.py    # User service
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker build instructions
├── poetry.lock                # Poetry lock file
├── pyproject.toml             # Poetry configuration
├── README.md                  # Project documentation
└── tests                      # Test suite
    ├── conftest.py            # Test fixtures
    └── unit                   # Unit tests
        ├── endpoints          # API endpoint tests
        │   ├── test_auth_endpoints.py
        │   ├── test_task_endpoints.py
        │   └── test_user_endpoints.py
        └── test_database.py   # Database tests
```

## 🔐 Authentication Flow

The API uses JWT tokens stored in HTTP-only cookies for authentication:

1. **Registration**: Create a new user account
2. **Login**: Authenticate and receive access token
3. **Access Protected Routes**: Use the token for authentication
4. **Token Refresh**: Refresh expired tokens automatically

### Authentication Endpoints

- `POST /auth/register`: Register a new user
- `POST /auth/login`: Login and receive authentication tokens
- `POST /auth/refresh`: Refresh an expired access token

## 📡 API Endpoints

### Authentication

- `POST /auth/register`: Register a new user
    - Request Body: `UserCreate` schema
    - Response: User data with authentication tokens in cookies

- `POST /auth/login`: Login an existing user
    - Request Body: `LoginRequest` schema
    - Response: User data with authentication tokens in cookies

- `POST /auth/refresh`: Refresh authentication token
    - Uses refresh token from cookies
    - Response: New authentication tokens in cookies

### Tasks

- `POST /user/task`: Create a new task
    - Request Body: `TaskCreate` schema
    - Response: Created task data

- `DELETE /user/task`: Delete a task
    - Query Parameters: `task_id` (UUID)
    - Response: 204 No Content on success

- `PATCH /user/task`: Update a task
    - Query Parameters: `task_id` (UUID), optional `status`
    - Request Body (optional): `TaskUpdate` schema
    - Response: Updated task data

- `GET /user/tasks`: List user's tasks
    - Query Parameters:
        - `page`: Page number (default: 1)
        - `page_size`: Items per page (default: 10)
        - `status`: Filter by task status (optional)
    - Response: `PaginationResponse` with task data

## 📊 Data Models

### User Model

```python
class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    password = Column(String(255), nullable=False)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
```

### Task Model

```python
class Task(Base):
    __tablename__ = "task"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="tasks")
```

## 🧪 Testing

The project includes a test suite:

```bash
# Run all tests
docker-compose exec api poetry run pytest

# Run specific test file
docker-compose exec api poetry run pytest tests/unit/endpoints/test_auth_endpoints.py
```

## 📧 Contact

For questions and support, please contact [abil.samedov502@gmail.com](abil.samedov502@gmail.com).
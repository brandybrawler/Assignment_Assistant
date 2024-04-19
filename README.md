# Web Application Documentation

## Overview
NB:Instructions to run the LLM are in the LLM folder as README.md. You need to run it in a seperate terminal.
This documentation provides detailed information about a web application that allows users to register, login, communicate via chat, and manage job tasks. It uses FastAPI as the backend framework, HTML with TailwindCSS for the frontend, and PostgreSQL for data management, all running within Docker containers.

## Technology Stack
- **Backend Framework**: FastAPI
- **Frontend**: HTML, TailwindCSS
- **Database**: PostgreSQL
- **Messaging Queue**: RabbitMQ
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest

## System Requirements
- Docker and Docker Compose
- Python 3.8 or newer
- PostgreSQL server

## Installation and Setup

### Clone the repository
Clone the code repository from GitHub or your preferred version control system:
```bash
git clone [git@github.com:brandybrawler/Assignment_Assistant.git]
```

### Build and Run with Docker
Navigate to the project directory and run:
```bash
docker-compose up --build
```
This command builds the Docker image and starts all the services defined in `docker-compose.yml`.

### Install Python Dependencies
If you need to run the application outside Docker for development:
```bash
pip install -r requirements.txt
```

## Architecture

### Backend
The backend is structured into several key components:

#### `database.py`
Sets up the database connection using SQLAlchemy. It manages the session creation and base model definition:
```python
engine = create_engine('postgresql://username:password@host:port/database')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

#### `models.py`
Defines data models using SQLAlchemy, which map Python classes to database tables:
```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
```

#### `routes.py`
Contains all the API routes/endpoints that handle HTTP requests and responses:
```python
@router.post("/register")
async def register_user(user: UserIn):
    # registration logic
```

#### `jobs.py`
Manages job-related functionalities, including interactions with RabbitMQ for message queuing:
```python
def process_job(job_data):
    print("Processing job:", job_data)
```

### Frontend
The frontend uses HTML files styled with TailwindCSS. It interacts with the backend through AJAX calls for dynamic content updates without page reloads.

#### `login.html`
Provides user authentication interface.

#### `signup.html`
Allows new users to register.

#### `chat.html`
Supports real-time messaging between user and an external Ai.

#### `jobs.html`
Enables job management, allowing users to submit and view jobs.

## API Documentation
Detailed description of each API endpoint, including URL, request type, expected parameters, and response format.

### User Authentication
- **Register**: `POST /api/register` - Registers a new user.
- **Login**: `POST /api/login` - Authenticates a user and returns a token.

### Job Management
- **Create Job**: `POST /api/jobs` - Submits a new job.
- **Get Jobs**: `GET /api/jobs` - Retrieves a list of jobs.

## Testing
The `test.py` script contains automated tests that validate the functionality of user registration, login, and job creation.

## Conclusion
This documentation provides a comprehensive guide to setting up, understanding, and operating the web application. For further assistance, consult the source code or contact the development team.

---

This documentation can be adapted as needed to fit additional requirements or changes in the application. Let me know if you need further details or modifications!
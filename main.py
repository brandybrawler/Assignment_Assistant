from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from models import User
import models
from database import SessionLocal, engine
from pydantic import BaseModel
import os
import pika
import time
from sqlalchemy.exc import OperationalError
import json

class JobCreate(BaseModel):
    description: str


app = FastAPI()

# Set up JWT configurations using environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key")  # Use a fallback if not set
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer is a class that provides a mechanism for the client
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def retry_operation(operation, retries=5, delay=10):
    """Retry an operation with a delay between retries."""
    for attempt in range(retries):
        try:
            operation()
            print("Database is ready and tables are created.")
            break
        except OperationalError as e:
            if attempt < retries - 1:
                print(f"Database not ready, retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Database connection failed after several retries.")
                raise
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, credentials_exception, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


@app.post("/register/")
async def register(user_details: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_details.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = User.get_password_hash(user_details.password)
    new_user = User(
        username=user_details.username,
        email=user_details.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}
@app.post("/jobs/")
async def submit_job(job: JobCreate, current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    # Create a new Job instance
    new_job = models.Job(description=job.description, owner=current_user)
    db.add(new_job)
    db.commit()

    # Send job to RabbitMQ queue
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=pika.PlainCredentials('123', '123')))
    channel = connection.channel()
    channel.queue_declare(queue='job_queue')
    channel.basic_publish(exchange='', routing_key='job_queue', body=json.dumps({"job_id": new_job.id, "description": new_job.description}))
    connection.close()

    return {"message": "Job submitted successfully", "job_id": new_job.id}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/")
async def read_users_me(current_user: str = Depends(verify_token)):
    return {"user": current_user}

if __name__ == "__main__":
    from models import Base
    from database import engine

    def init_db():
        Base.metadata.create_all(bind=engine)

    retry_operation(init_db)
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
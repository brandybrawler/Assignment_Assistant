from fastapi import HTTPException, Depends, APIRouter
from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models import User, Job, Notification
import models
from database import SessionLocal
from pydantic import BaseModel
import os
import pika
import json
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class JobCreate(BaseModel):
    description: str
    priority: str

SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register/")
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

@router.post("/jobs/")
async def submit_job(job: JobCreate, current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    # Check if the user has enough credits
    if current_user.credits < 10:  # Assuming each job costs 10 credits
        raise HTTPException(status_code=400, detail="Insufficient credits")

    # Create a new Job instance
    new_job = Job(description=job.description, priority=job.priority, owner=current_user)
    current_user.credits -= 10  # Deduct credits
    db.add(new_job)
    db.commit()

    # Send job to RabbitMQ queue with priority included in the message
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=pika.PlainCredentials('123', '123')))
    channel = connection.channel()
    channel.queue_declare(queue='job_queue')
    channel.basic_publish(
        exchange='',
        routing_key='job_queue',
        body=json.dumps({"job_id": new_job.id, "description": new_job.description, "priority": new_job.priority})
    )
    connection.close()

    return {"message": "Job submitted successfully", "job_id": new_job.id, "remaining_credits": current_user.credits}


@router.post("/token")
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

@router.get("/notifications/")
async def get_notifications(current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == current_user.id).all()
    return notifications

@router.put("/notifications/{notification_id}/read")
async def mark_notification_as_read(notification_id: int, current_user: User = Depends(verify_token), db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == current_user.id).first()
    if notification:
        notification.read = True
        db.commit()
        return {"message": "Notification marked as read"}
    raise HTTPException(status_code=404, detail="Notification not found")

@router.get("/users/me/")
async def read_users_me(current_user: str = Depends(verify_token)):
    return {"user": current_user}


router.mount("/static", StaticFiles(directory="templates"), name="static")
@router.get("/", response_class=HTMLResponse)
async def root():
    path = "templates/jobs.html"
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/login", response_class=HTMLResponse)
async def login_page():
    path = "templates/login.html"
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@router.get("/signup", response_class=HTMLResponse)
async def signup_page():
    path = "templates/signup.html"
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@router.get("/chat", response_class=HTMLResponse)
async def login_page():
    path = "templates/chat.html"
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

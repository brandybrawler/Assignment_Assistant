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

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

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
    models.Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

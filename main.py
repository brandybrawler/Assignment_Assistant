from fastapi import Depends ,FastAPI, HTTPException, status
from pydantic import BaseModel
import models
# from typing import List, Annotated
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

# openssl rand -hex 32
SECRET_KEY = "56ae073f24c230c68b849857315d0c963cc77cdcca7cfb25a7d1799a86ef100e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# class User(BaseModel):
#     id: int
#     username: str
#     email: str
#     password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db_dependency = Annotated(Session, Depends(get_db))



@app.get("/")
async def home():
    # users = models.User.query.all()
    # message = {"message": "Hello World"}
    return "hello worlddd!"




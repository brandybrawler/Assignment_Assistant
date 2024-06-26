from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
import datetime

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    credits = Column(Integer, default=0)
    jobs = relationship("Job", back_populates="owner")

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Using datetime module correctly
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default='pending')  # e.g., pending, completed, failed
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="jobs")
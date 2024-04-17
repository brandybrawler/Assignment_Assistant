from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# ... (your existing imports and settings)

# Create a SessionLocal class to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database URL
DATABASE_URL = settings.DATABASE_URL

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a Session class to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare a base class for database models
Base: DeclarativeMeta = declarative_base()
def get_db() -> Session:
    """Provide a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    credits_balance = Column(Integer, default=0)

# Example usage to create database tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

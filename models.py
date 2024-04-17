from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
# from sqlalchemy.ext.declarative import declarative_base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))

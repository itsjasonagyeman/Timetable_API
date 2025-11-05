from sqlalchemy import Column, Integer, String
from database.db_setup import Base

class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
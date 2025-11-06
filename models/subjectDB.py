from sqlalchemy import Column, Integer, String, String, Time
from database.db_setup import Base

class SubjectDB(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    day = Column(String, nullable=False)
    time = Column(Time, nullable=False)
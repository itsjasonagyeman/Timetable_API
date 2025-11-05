from pydantic import BaseModel
from datetime import date, time

class Subject(BaseModel):
    id: int
    name: str
    date: date
    time: time
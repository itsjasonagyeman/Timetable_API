from pydantic import BaseModel
from datetime import time

class Subject(BaseModel):
    name: str
    day: str
    time: time

class SubjectResponse(Subject):
    id: int

    class Config():
        from_attributes= True

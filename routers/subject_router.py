from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db_setup import SessionLocal
from models.subject import Subject, SubjectResponse
from models.subjectDB import SubjectDB
from typing import List
from database.db_setup import engine
import pandas as pd


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/subject', response_model=SubjectResponse)
def add_subject(subject: Subject, db: Session = Depends(get_db)):
    existing_subject = db.query(SubjectDB).filter(SubjectDB.name == subject.name, SubjectDB.day == subject.day, SubjectDB.time == subject.time).first()
    if existing_subject:
        raise HTTPException(status_code=401, detail='Subject has already been added')
    
    new_subject = SubjectDB(
        name = subject.name,
        day = subject.day,
        time = subject.time
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    

    return new_subject

@router.get('/subject', response_model=List[SubjectResponse])
def get_all_subjects(db: Session = Depends(get_db)):
    subjects = db.query(SubjectDB).all()

    return subjects

@router.get('/subject/{subject_id}', response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(SubjectDB).filter(SubjectDB.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=401, detail='Subject does not exist')

    return subject

@router.delete('/subject/{subject_id}')
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(SubjectDB).filter(SubjectDB.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=401, detail='Subject does not exist')
    
    db.delete(subject)
    db.commit()

    return {'message': 'Subject Deleted'}

@router.put('/subject/{subject_id}', response_model=SubjectResponse)
def update_subject(subject_id:int, updated_subject:Subject, db: Session = Depends(get_db)):
    subject = db.query(SubjectDB).filter(SubjectDB.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=401, detail='Subject does not exist')
    
    subject.name = updated_subject.name
    subject.day = updated_subject.day
    subject.time = updated_subject.time

    db.refresh(subject)
    db.commit()
    

    return subject

@router.get('/export-subjects')
def change_to_spreadsheet():
    df = pd.read_sql("SELECT * FROM subjects", engine)
    df.to_excel("subjects.xlsx", index=False)
    return {'message': 'Created Spreadsheet'}
    
    

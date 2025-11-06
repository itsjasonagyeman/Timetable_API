from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db_setup import SessionLocal
from models.subject import Subject
from models.subjectDB import SubjectDB

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router.post('/subject')
def add_subject(subject: Subject, db: Session = Depends(get_db)):
    existing_subject = db.query(SubjectDB).filter(SubjectDB == subject).first()
    if existing_subject:
        raise HTTPException(status_code=401, detail='Subject has already been added')
    
    new_subject = SubjectDB(
        name = subject.name,
        date = subject.date,
        time = subject.time
    )

    db.add(new_subject)
    db.refresh()
    db.commit(new_subject)

    return new_subject

router.get('/subject')
def get_all_subjects(db: Session = Depends(get_db)):
    subjects = db.query(SubjectDB).all()

    return subjects

router.get('/subject/{subject_id}')
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(SubjectDB).filter(SubjectDB.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=401, detail='Subject does not exist')

    return subject

router.delete('/subject/{subject_id}')
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(SubjectDB).filter(SubjectDB.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=401, detail='Subject does not exist')
    
    db.delete(subject)
    db.refresh()

    return {'message': 'Subject Deleted'}

router.put('/subject/{subject_id}')
def update_subject(subject_id:int, updated_subject:Subject, db: Session = Depends(get_db)):
    subject = db.query(SubjectDB).filter(SubjectDB.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=401, detail='Subject does not exist')
    
    subject.name = updated_subject.name
    subject.date = updated_subject.date
    subject.time = updated_subject.time

    db.commit(subject)
    db.refresh()

    return subject
    
    

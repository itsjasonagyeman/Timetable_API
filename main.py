from fastapi import FastAPI
from database.db_setup import Base, engine
from routers.subject_router import router as subject_router

app = FastAPI()

app.include_router(subject_router)
Base.metadata.create_all(bind= engine)
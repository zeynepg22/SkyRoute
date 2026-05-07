from fastapi import FastAPI
from core.database import create_db_and_tables
import models.db_models

from routers.courses import router as courses_router
from routers.lessons import router as lessons_router

from routers.enrollments import router as enrollments_router
from routers.progress import router as progress_router

app = FastAPI(title="SkyRoute API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "SkyRoute API is running"}

app.include_router(courses_router) 
app.include_router(lessons_router)
app.include_router(enrollments_router)
app.include_router(progress_router)
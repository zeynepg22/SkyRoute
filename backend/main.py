from fastapi import FastAPI
from core.database import create_db_and_tables
import models.db_models

from routers import courses, lessons, enrollments, progress

from routers.auth_router import router as auth_router
from routers.admin_router import router as admin_router

from middleware.security import setup_security

app = FastAPI(
    title="SkyRoute API",
    description="Online Course Platform — Mini Udemy",
    version="1.0.0",
)

setup_security(app)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(enrollments.router)
app.include_router(progress.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "SkyRoute API is running"}

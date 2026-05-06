from fastapi import FastAPI
from core.database import create_db_and_tables
import models.db_models

app = FastAPI(title="SkyRoute API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "SkyRoute API is running"}

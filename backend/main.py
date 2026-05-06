from fastapi import FastAPI
from database import create_db_and_tables
import models

app = FastAPI(title="SkyRoute API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "SkyRoute API is running"}

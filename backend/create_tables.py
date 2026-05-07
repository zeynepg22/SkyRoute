from sqlmodel import SQLModel
from core.database import engine

from models.db_models import *

SQLModel.metadata.create_all(engine)

print("Database tables created successfully.")
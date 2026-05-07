from typing import Optional
from sqlmodel import SQLModel, Field


class CourseCreate(SQLModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)
    category: str = Field(min_length=2, max_length=100)
    instructor_id: int
    is_published: bool = True


class CourseUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=150)
    description: Optional[str] = Field(default=None, min_length=10)
    category: Optional[str] = Field(default=None, min_length=2, max_length=100)
    is_published: Optional[bool] = None
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from core.database import engine
from models.db_models import Lesson, Course

router = APIRouter(
    prefix="/lessons",
    tags=["Lessons"]
)


@router.post("/")
def create_lesson(lesson: Lesson):
    with Session(engine) as session:

        course = session.get(Course, lesson.course_id)

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        session.add(lesson)
        session.commit()
        session.refresh(lesson)

        return lesson


@router.get("/course/{course_id}")
def get_course_lessons(course_id: int):
    with Session(engine) as session:

        course = session.get(Course, course_id)

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        lessons = session.exec(
            select(Lesson).where(Lesson.course_id == course_id)
        ).all()

        return lessons
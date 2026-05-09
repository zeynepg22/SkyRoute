from fastapi import Depends
from auth.dependencies import require_role
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from core.database import engine
from models.db_models import Lesson, Course
from models.db_models import User

router = APIRouter(
    prefix="/lessons",
    tags=["Lessons"]
)


@router.post("/")
def create_lesson(
    lesson: Lesson,
    current_user: User = Depends(require_role("instructor", "admin"))
):
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
from fastapi import Depends
from auth.dependencies import get_current_user
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from core.database import engine
from models.db_models import (
    Lesson,
    LessonProgress,
    Course,
    User
)

router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)


@router.post("/complete/{lesson_id}")
def complete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user)
):
    student_id = current_user.id

    with Session(engine) as session:

        lesson = session.get(Lesson, lesson_id)

        if not lesson:
            raise HTTPException(
                status_code=404,
                detail="Lesson not found"
            )

        existing = session.exec(
            select(LessonProgress).where(
                LessonProgress.user_id == student_id,
                LessonProgress.lesson_id == lesson_id
            )
        ).first()

        if existing:
            return {
                "message": "Lesson already completed"
            }

        progress = LessonProgress(
            user_id=student_id,
            lesson_id=lesson_id,
            is_completed=True
        )

        session.add(progress)
        session.commit()

        return {
            "message": "Lesson completed successfully"
        }


@router.get("/{course_id}")
def get_course_progress(
    course_id: int,
    current_user: User = Depends(get_current_user)
):
    student_id = current_user.id

    with Session(engine) as session:

        course = session.get(Course, course_id)

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        lessons = session.exec(
            select(Lesson).where(
                Lesson.course_id == course_id
            )
        ).all()

        total_lessons = len(lessons)

        if total_lessons == 0:
            return {
                "progress": 0
            }

        lesson_ids = [lesson.id for lesson in lessons]

        completed = session.exec(
            select(LessonProgress).where(
                LessonProgress.user_id == student_id,
                LessonProgress.lesson_id.in_(lesson_ids),
                LessonProgress.is_completed == True
            )
        ).all()

        progress_percentage = (
            len(completed) / total_lessons
        ) * 100

        return {
            "course_id": course_id,
            "progress": round(progress_percentage, 2)
        }
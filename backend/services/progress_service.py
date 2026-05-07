from sqlmodel import Session, select
from models.db_models import Lesson, LessonProgress


def calculate_course_progress(session: Session, user_id: int, course_id: int) -> float:
    lessons = session.exec(
        select(Lesson).where(Lesson.course_id == course_id)
    ).all()

    total_lessons = len(lessons)

    if total_lessons == 0:
        return 0.0

    lesson_ids = [lesson.id for lesson in lessons]

    completed_lessons = session.exec(
        select(LessonProgress).where(
            LessonProgress.user_id == user_id,
            LessonProgress.lesson_id.in_(lesson_ids),
            LessonProgress.is_completed == True
        )
    ).all()

    progress = (len(completed_lessons) / total_lessons) * 100
    return round(progress, 2)
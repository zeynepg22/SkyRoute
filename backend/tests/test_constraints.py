import pytest
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from core.database import engine
from models.db_models import Enrollment, LessonProgress


def test_duplicate_enrollment_is_not_allowed():
    with Session(engine) as session:
        duplicate_enrollment = Enrollment(
            user_id=3,
            course_id=1,
        )

        session.add(duplicate_enrollment)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()


def test_duplicate_lesson_progress_is_not_allowed():
    with Session(engine) as session:
        duplicate_progress = LessonProgress(
            user_id=3,
            lesson_id=1,
            is_completed=True,
        )

        session.add(duplicate_progress)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()
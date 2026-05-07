from sqlmodel import Session
from core.database import engine
from services.progress_service import calculate_course_progress


def test_calculate_course_progress():
    with Session(engine) as session:
        progress = calculate_course_progress(
            session=session,
            user_id=3,
            course_id=1,
        )

        assert progress == 66.67
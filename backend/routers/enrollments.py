from fastapi import Depends
from auth.dependencies import get_current_user
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from core.database import engine
from models.db_models import Enrollment, User, Course

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)


@router.post("/{course_id}")
def enroll_student(
    course_id: int,
    current_user: User = Depends(get_current_user)
):
    student_id = current_user.id

    with Session(engine) as session:

        student = session.get(User, student_id)

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        course = session.get(Course, course_id)

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        existing = session.exec(
            select(Enrollment).where(
                Enrollment.user_id == student_id,
                Enrollment.course_id == course_id
            )
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Student already enrolled"
            )

        enrollment = Enrollment(
            user_id=student_id,
            course_id=course_id
        )

        session.add(enrollment)
        session.commit()
        session.refresh(enrollment)

        return {
            "message": "Enrollment successful",
            "enrollment_id": enrollment.id
        }
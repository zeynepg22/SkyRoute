from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from core.database import engine
from models.db_models import Course, User
from schemas.course_schema import CourseCreate, CourseUpdate

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.get("/")
def get_courses():
    with Session(engine) as session:
        courses = session.exec(select(Course)).all()
        return courses


@router.get("/{course_id}")
def get_course(course_id: int):
    with Session(engine) as session:
        course = session.get(Course, course_id)

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        return course


@router.post("/")
def create_course(course: CourseCreate):
    with Session(engine) as session:
        instructor = session.get(User, course.instructor_id)

        if not instructor:
            raise HTTPException(
                status_code=404,
                detail="Instructor not found"
            )

        new_course = Course(
            title=course.title,
            description=course.description,
            category=course.category,
            instructor_id=course.instructor_id,
            is_published=course.is_published
        )

        session.add(new_course)
        session.commit()
        session.refresh(new_course)

        return new_course


@router.put("/{course_id}")
def update_course(course_id: int, updated_course: CourseUpdate):
    with Session(engine) as session:
        course = session.get(Course, course_id)

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        if updated_course.title is not None:
            course.title = updated_course.title

        if updated_course.description is not None:
            course.description = updated_course.description

        if updated_course.category is not None:
            course.category = updated_course.category

        if updated_course.is_published is not None:
            course.is_published = updated_course.is_published

        session.add(course)
        session.commit()
        session.refresh(course)

        return course


@router.delete("/{course_id}")
def delete_course(course_id: int):
    with Session(engine) as session:
        course = session.get(Course, course_id)

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Course not found"
            )

        session.delete(course)
        session.commit()

        return {"message": "Course deleted successfully"}
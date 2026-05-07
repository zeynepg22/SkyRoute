from sqlmodel import Session, select
from passlib.context import CryptContext

from core.database import engine
from models.db_models import (
    Role,
    User,
    Course,
    Lesson,
    Enrollment,
    LessonProgress,
    SocialAccount,
    TwoFactorMethod,
    BackupCode,
    AuditLog,
)
from services.progress_service import calculate_course_progress


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def seed_database():
    with Session(engine) as session:
        existing_roles = session.exec(select(Role)).first()

        if existing_roles:
            print("Seed data already exists. Skipping...")
            return

        student_role = Role(name="student")
        instructor_role = Role(name="instructor")
        admin_role = Role(name="admin")

        session.add(student_role)
        session.add(instructor_role)
        session.add(admin_role)
        session.commit()

        session.refresh(student_role)
        session.refresh(instructor_role)
        session.refresh(admin_role)

        admin = User(
            full_name="Admin User",
            email="admin@skyroute.com",
            password_hash=hash_password("Admin123!"),
            role_id=admin_role.id,
            is_active=True,
        )

        instructor = User(
            full_name="SkyRoute Instructor",
            email="instructor@skyroute.com",
            password_hash=hash_password("Instructor123!"),
            role_id=instructor_role.id,
            is_active=True,
        )

        student = User(
            full_name="Student User",
            email="student@skyroute.com",
            password_hash=hash_password("Student123!"),
            role_id=student_role.id,
            is_active=True,
        )

        session.add(admin)
        session.add(instructor)
        session.add(student)
        session.commit()

        session.refresh(admin)
        session.refresh(instructor)
        session.refresh(student)

        course_1 = Course(
            title="React JS - Complete Guide",
            description="Learn React JS from beginner to advanced level with practical examples.",
            category="Development",
            instructor_id=instructor.id,
            is_published=True,
        )

        course_2 = Course(
            title="Python for Data Science",
            description="Learn Python, data analysis, visualization, and data science fundamentals.",
            category="Data Science",
            instructor_id=instructor.id,
            is_published=True,
        )

        course_3 = Course(
            title="UI/UX Design Fundamentals",
            description="Learn user interface design, user experience principles, and modern design basics.",
            category="Design",
            instructor_id=instructor.id,
            is_published=True,
        )

        course_4 = Course(
            title="Digital Marketing Masterclass",
            description="Learn SEO, branding, social media marketing, and digital campaign strategies.",
            category="Marketing",
            instructor_id=instructor.id,
            is_published=True,
        )

        course_5 = Course(
            title="Business Strategy Basics",
            description="Learn business planning, strategy, leadership, and growth fundamentals.",
            category="Business",
            instructor_id=instructor.id,
            is_published=True,
        )

        course_6 = Course(
            title="Personal Growth Bootcamp",
            description="Improve mindset, focus, productivity, and personal development skills.",
            category="Growth",
            instructor_id=instructor.id,
            is_published=True,
        )

        session.add_all([
            course_1,
            course_2,
            course_3,
            course_4,
            course_5,
            course_6,
        ])

        session.commit()

        for course in [
            course_1,
            course_2,
            course_3,
            course_4,
            course_5,
            course_6,
        ]:
            session.refresh(course)

        lessons = [
            Lesson(
                course_id=course_1.id,
                title="Introduction to React",
                content="Learn the basics of React components and JSX.",
                video_url="https://www.youtube.com/embed/SqcY0GlETPk",
                order_index=1,
            ),
            Lesson(
                course_id=course_1.id,
                title="React Hooks",
                content="Learn useState and useEffect hooks.",
                video_url="https://www.youtube.com/embed/O6P86uwfdR0",
                order_index=2,
            ),

            Lesson(
                course_id=course_2.id,
                title="Python Basics",
                content="Introduction to Python programming.",
                video_url="https://www.youtube.com/embed/kqtD5dpn9C8",
                order_index=1,
            ),
            Lesson(
                course_id=course_2.id,
                title="Data Analysis Fundamentals",
                content="Learn NumPy and pandas basics.",
                video_url="https://www.youtube.com/embed/r-uOLxNrNk8",
                order_index=2,
            ),

            Lesson(
                course_id=course_3.id,
                title="UI Design Basics",
                content="Learn layout, colors, and typography.",
                video_url="https://www.youtube.com/embed/c9Wg6Cb_YlU",
                order_index=1,
            ),
            Lesson(
                course_id=course_3.id,
                title="UX Principles",
                content="Learn user-centered design principles.",
                video_url="https://www.youtube.com/embed/Ovj4hFxko7c",
                order_index=2,
            ),

            Lesson(
                course_id=course_4.id,
                title="Marketing Fundamentals",
                content="Learn the basics of digital marketing.",
                video_url="https://www.youtube.com/embed/nU-IIXBWlS4",
                order_index=1,
            ),
            Lesson(
                course_id=course_4.id,
                title="SEO and Branding",
                content="Learn search engine optimization and branding.",
                video_url="https://www.youtube.com/embed/DvwS7cV9GmQ",
                order_index=2,
            ),

            Lesson(
                course_id=course_5.id,
                title="Business Planning",
                content="Learn strategic business planning.",
                video_url="https://www.youtube.com/embed/81ghhGjpMVQ",
                order_index=1,
            ),
            Lesson(
                course_id=course_5.id,
                title="Leadership Skills",
                content="Learn team management and leadership.",
                video_url="https://www.youtube.com/embed/18Uq3m7qTSo",
                order_index=2,
            ),

            Lesson(
                course_id=course_6.id,
                title="Mindset and Focus",
                content="Improve your productivity and focus.",
                video_url="https://www.youtube.com/embed/ZXsQAXx_ao0",
                order_index=1,
            ),
            Lesson(
                course_id=course_6.id,
                title="Building Better Habits",
                content="Learn consistency and growth habits.",
                video_url="https://www.youtube.com/embed/75d_29QWELk",
                order_index=2,
            ),
        ]

        session.add_all(lessons)
        session.commit()

        for lesson in lessons:
            session.refresh(lesson)

        enrollment = Enrollment(
            user_id=student.id,
            course_id=course_1.id,
        )

        session.add(enrollment)
        session.commit()

        progress_1 = LessonProgress(
            user_id=student.id,
            lesson_id=lessons[0].id,
            is_completed=True,
        )

        progress_2 = LessonProgress(
            user_id=student.id,
            lesson_id=lessons[1].id,
            is_completed=True,
        )

        session.add(progress_1)
        session.add(progress_2)

        session.commit()

        progress_percentage = calculate_course_progress(
            session=session,
            user_id=student.id,
            course_id=course_1.id,
        )

        print("Seed data inserted successfully.")
        print(f"Student progress for course '{course_1.title}': {progress_percentage}%")


if __name__ == "__main__":
    seed_database()
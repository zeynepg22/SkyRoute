from sqlmodel import Session, select
from passlib.context import CryptContext

from database import engine
from models import (
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
from services import calculate_course_progress


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
            full_name="Instructor User",
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
            title="Full-Stack Web Development with FastAPI and React",
            description="Learn how to build a modern full-stack web application using FastAPI, PostgreSQL, and React.",
            category="Web Development",
            instructor_id=instructor.id,
            is_published=True,
        )

        course_2 = Course(
            title="Database Design Fundamentals",
            description="Learn relational database design, normalization, SQLModel relationships, and PostgreSQL basics.",
            category="Database",
            instructor_id=instructor.id,
            is_published=True,
        )

        session.add(course_1)
        session.add(course_2)
        session.commit()

        session.refresh(course_1)
        session.refresh(course_2)

        lessons = [
            Lesson(
                course_id=course_1.id,
                title="Introduction to Full-Stack Architecture",
                content="This lesson explains how frontend, backend, and database layers work together.",
                video_url="https://www.youtube.com/embed/0sOvCWFmrtA",
                order_index=1,
            ),
            Lesson(
                course_id=course_1.id,
                title="Building REST APIs with FastAPI",
                content="This lesson introduces REST API development with FastAPI.",
                video_url="https://www.youtube.com/embed/7t2alSnE2-I",
                order_index=2,
            ),
            Lesson(
                course_id=course_1.id,
                title="Connecting React to Backend APIs",
                content="This lesson explains how React fetches data from backend endpoints.",
                video_url="https://www.youtube.com/embed/w7ejDZ8SWv8",
                order_index=3,
            ),
            Lesson(
                course_id=course_2.id,
                title="Relational Database Concepts",
                content="This lesson explains tables, primary keys, foreign keys, and relationships.",
                video_url="https://www.youtube.com/embed/HXV3zeQKqGY",
                order_index=1,
            ),
            Lesson(
                course_id=course_2.id,
                title="Normalization and Data Integrity",
                content="This lesson explains normalization, constraints, and database consistency.",
                video_url="https://www.youtube.com/embed/GFQaEYEc8_8",
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

        social_accounts = [
            SocialAccount(
                user_id=student.id,
                provider="google",
                provider_user_id="google_student_001",
            ),
            SocialAccount(
                user_id=student.id,
                provider="github",
                provider_user_id="github_student_001",
            ),
            SocialAccount(
                user_id=student.id,
                provider="discord",
                provider_user_id="discord_student_001",
            ),
            SocialAccount(
                user_id=student.id,
                provider="facebook",
                provider_user_id="facebook_student_001",
            ),
        ]

        two_factor_methods = [
            TwoFactorMethod(
                user_id=student.id,
                method_type="totp",
                is_enabled=True,
                secret_value="sample_totp_secret",
            ),
            TwoFactorMethod(
                user_id=student.id,
                method_type="email_otp",
                is_enabled=True,
                secret_value="student@skyroute.com",
            ),
            TwoFactorMethod(
                user_id=student.id,
                method_type="backup_codes",
                is_enabled=True,
                secret_value=None,
            ),
            TwoFactorMethod(
                user_id=student.id,
                method_type="trusted_device",
                is_enabled=True,
                secret_value="sample_device_fingerprint",
            ),
        ]

        backup_codes = [
            BackupCode(user_id=student.id, code_hash=hash_password("BACKUP-001")),
            BackupCode(user_id=student.id, code_hash=hash_password("BACKUP-002")),
            BackupCode(user_id=student.id, code_hash=hash_password("BACKUP-003")),
        ]

        audit_logs = [
            AuditLog(
                user_id=admin.id,
                action="CREATE_ROLE",
                entity_type="role",
                entity_id=admin_role.id,
            ),
            AuditLog(
                user_id=instructor.id,
                action="CREATE_COURSE",
                entity_type="course",
                entity_id=course_1.id,
            ),
            AuditLog(
                user_id=student.id,
                action="ENROLL_COURSE",
                entity_type="course",
                entity_id=course_1.id,
            ),
            AuditLog(
                user_id=student.id,
                action="COMPLETE_LESSON",
                entity_type="lesson",
                entity_id=lessons[0].id,
            ),
        ]

        session.add_all(social_accounts)
        session.add_all(two_factor_methods)
        session.add_all(backup_codes)
        session.add_all(audit_logs)
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
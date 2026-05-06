from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=50)

    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100)
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str
    role_id: int = Field(foreign_key="roles.id", index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)

    role: Optional[Role] = Relationship(back_populates="users")
    courses: List["Course"] = Relationship(back_populates="instructor")
    enrollments: List["Enrollment"] = Relationship(back_populates="user")
    lesson_progress: List["LessonProgress"] = Relationship(back_populates="user")
    social_accounts: List["SocialAccount"] = Relationship(back_populates="user")
    two_factor_methods: List["TwoFactorMethod"] = Relationship(back_populates="user")
    backup_codes: List["BackupCode"] = Relationship(back_populates="user")
    audit_logs: List["AuditLog"] = Relationship(back_populates="user")


class Course(SQLModel, table=True):
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=150)
    description: str
    category: str = Field(index=True, max_length=100)
    instructor_id: int = Field(foreign_key="users.id", index=True)
    is_published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)

    instructor: Optional[User] = Relationship(back_populates="courses")
    lessons: List["Lesson"] = Relationship(back_populates="course")
    enrollments: List["Enrollment"] = Relationship(back_populates="course")


class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"
    __table_args__ = (
        UniqueConstraint("course_id", "order_index", name="uq_lesson_order_per_course"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    title: str = Field(max_length=150)
    content: str
    video_url: Optional[str] = Field(default=None, max_length=500)
    order_index: int = Field(index=True)

    course: Optional[Course] = Relationship(back_populates="lessons")
    progress_records: List["LessonProgress"] = Relationship(back_populates="lesson")


class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_user_course_enrollment"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    course_id: int = Field(foreign_key="courses.id", index=True)
    enrolled_at: datetime = Field(default_factory=utc_now)

    user: Optional[User] = Relationship(back_populates="enrollments")
    course: Optional[Course] = Relationship(back_populates="enrollments")


class LessonProgress(SQLModel, table=True):
    __tablename__ = "lesson_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    lesson_id: int = Field(foreign_key="lessons.id", index=True)
    is_completed: bool = Field(default=True)
    completed_at: datetime = Field(default_factory=utc_now)

    user: Optional[User] = Relationship(back_populates="lesson_progress")
    lesson: Optional[Lesson] = Relationship(back_populates="progress_records")


class SocialAccount(SQLModel, table=True):
    __tablename__ = "social_accounts"
    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id", name="uq_provider_user"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    provider: str = Field(index=True, max_length=50)
    provider_user_id: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=utc_now)

    user: Optional[User] = Relationship(back_populates="social_accounts")


class TwoFactorMethod(SQLModel, table=True):
    __tablename__ = "two_factor_methods"
    __table_args__ = (
        UniqueConstraint("user_id", "method_type", name="uq_user_2fa_method"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    method_type: str = Field(index=True, max_length=50)
    is_enabled: bool = Field(default=False)
    secret_value: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)

    user: Optional[User] = Relationship(back_populates="two_factor_methods")


class BackupCode(SQLModel, table=True):
    __tablename__ = "backup_codes"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    code_hash: str
    is_used: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)
    user: Optional[User] = Relationship(back_populates="backup_codes")


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    action: str = Field(index=True, max_length=100)
    entity_type: str = Field(index=True, max_length=100)
    entity_id: Optional[int] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=utc_now)

    user: Optional[User] = Relationship(back_populates="audit_logs")
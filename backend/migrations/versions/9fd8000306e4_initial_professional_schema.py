"""initial professional schema

Revision ID: 9fd8000306e4
Revises: 
Create Date: 2026-05-06 22:34:51.601607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fd8000306e4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False, unique=True),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("instructor_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "lessons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id"), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("video_url", sa.String(length=500)),
        sa.Column("order_index", sa.Integer(), nullable=False),
    )

    op.create_table(
        "enrollments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id"), nullable=False),
        sa.Column("enrolled_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "lesson_progress",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("lesson_id", sa.Integer(), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("is_completed", sa.Boolean(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "social_accounts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("provider_user_id", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "two_factor_methods",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("method_type", sa.String(length=50), nullable=False),
        sa.Column("is_enabled", sa.Boolean(), nullable=False),
        sa.Column("secret_value", sa.String()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "backup_codes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("code_hash", sa.String(), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_unique_constraint(
        "uq_user_course_enrollment",
        "enrollments",
        ["user_id", "course_id"],
    )

    op.create_unique_constraint(
        "uq_user_lesson_progress",
        "lesson_progress",
        ["user_id", "lesson_id"],
    )

    op.create_unique_constraint(
        "uq_lesson_order_per_course",
        "lessons",
        ["course_id", "order_index"],
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("backup_codes")
    op.drop_table("two_factor_methods")
    op.drop_table("social_accounts")
    op.drop_table("lesson_progress")
    op.drop_table("enrollments")
    op.drop_table("lessons")
    op.drop_table("courses")
    op.drop_table("users")
    op.drop_table("roles")

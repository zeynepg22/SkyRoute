# SkyRoute – Online Course Platform

SkyRoute is a modern full-stack online learning platform inspired by systems such as Udemy and Coursera.

The platform allows students to enroll in courses, watch lessons, track progress, and manage learning activities while instructors and administrators manage platform content and users.

---

# Project Goals

The main goal of this project is to demonstrate:

- Full-stack web application development
- Professional backend architecture
- PostgreSQL relational database design
- REST API development with FastAPI
- Authentication and authorization systems
- Role-based access control
- Secure software engineering practices
- Automated testing workflows
- Deployment-ready project structure

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLModel |
| Authentication | JWT + OAuth |
| Testing | Pytest + Playwright |
| Migrations | Alembic |
| Deployment | Railway / Vercel |
| Version Control | Git + GitHub |

---

# System Architecture

```text
Frontend (React + Vite)
        ↓
FastAPI REST API
        ↓
Business Logic Layer
        ↓
SQLModel ORM
        ↓
PostgreSQL Database
```

---

# Main Features

## Student Features

- User registration and login
- Browse available courses
- Enroll in courses
- Watch lesson videos
- Track course progress
- Complete lessons
- Personal dashboard

---

## Instructor Features

- Create and manage courses
- Create lessons
- Organize lesson order
- Manage course content
- View enrolled students

---

## Admin Features

- Manage users
- Change user roles
- Monitor platform activity
- Manage courses and lessons
- Access admin dashboard

---

# Authentication & Security Features

## Authentication Methods

- Email & password authentication
- JWT authentication
- OAuth social login support

---

## Supported Social Login Providers

- Google
- GitHub
- LinkedIn
- Facebook

---

## Two-Factor Authentication Support

- TOTP (Google Authenticator)
- Email OTP
- Backup recovery codes
- Trusted device authentication

---

## Security Features

- Password hashing
- JWT validation
- Role-based authorization
- Audit logging
- Environment variable protection
- Secure database credentials
- Protected API routes

---

# Database Design

## Main Tables

| Table | Purpose |
|---|---|
| `roles` | Stores user roles |
| `users` | Stores platform users |
| `courses` | Stores courses |
| `lessons` | Stores lesson content |
| `enrollments` | Stores student enrollments |
| `lesson_progress` | Stores completed lessons |
| `social_accounts` | Stores social login data |
| `two_factor_methods` | Stores 2FA methods |
| `backup_codes` | Stores recovery codes |
| `audit_logs` | Stores activity logs |

---

# Backend Structure

```text
backend/
├── core/
│   └── database.py
├── models/
│   └── db_models.py
├── services/
│   └── progress_service.py
├── routers/
├── schemas/
├── tests/
├── migrations/
├── main.py
├── seed.py
├── requirements.txt
└── pytest.ini
```

---

# Database Migration System

The project uses Alembic for database migrations.

## Run Migrations

```bash
cd backend
alembic upgrade head
```

---

# Seed Data

The project includes development seed data.

## Included Seed Data

- Roles
- Users
- Courses
- Lessons
- Enrollments
- Lesson progress
- Social login accounts
- Two-factor authentication methods
- Audit logs

## Run Seed Data

```bash
cd backend
python seed.py
```

---

# Progress Tracking System

The platform calculates student course completion percentage.

## Formula

```text
Progress = completed lessons / total lessons × 100
```

---

# Automated Testing

The backend includes automated tests using Pytest.

## Test Coverage Includes

- Progress calculation
- Unique constraints
- Enrollment validation
- Lesson progress validation

## Run Tests

```bash
cd backend
pytest
```

Expected result:

```text
3 passed
```

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/zeynepg22/SkyRoute.git
cd SkyRoute
```

---

## Backend Setup

```bash
cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside `backend/`.

```env
DATABASE_URL=postgresql://skyroute_user:skyroute123@localhost:5432/skyroute_db
```

---

## Run Database Migrations

```bash
alembic upgrade head
```

---

## Seed Database

```bash
python seed.py
```

---

## Start Backend Server

```bash
python -m uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Deployment Targets

| Layer | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Railway |
| Database | Railway PostgreSQL |

Alternative deployment infrastructure may also be used.

---

# Team Responsibilities

| Area | Responsibility |
|---|---|
| Backend APIs | FastAPI routes and business logic |
| Database Layer | PostgreSQL + SQLModel architecture |
| Frontend | React + Vite interface |
| Authentication | JWT + OAuth + 2FA |
| Testing | Pytest + Playwright |
| Deployment | CI/CD and cloud deployment |

---

# Future Improvements

- Video upload support
- AI-powered course recommendations
- Real-time notifications
- Payment integration
- Live classroom system
- Course certificates
- Advanced analytics dashboard
- Chat and discussion system

---

# Repository Security

Sensitive files are ignored using `.gitignore`.

Ignored files include:

```gitignore
venv/
backend/venv/
__pycache__/
.env
backend/.env
.pytest_cache/
*.pyc
.DS_Store
.sixth/
```

---

# Project Status

## Current Status

```text
Backend Database Architecture Completed
```

Completed components:

- PostgreSQL database schema
- SQLModel ORM models
- Alembic migration system
- Progress calculation logic
- Seed data
- Automated tests
- Modular backend structure
- Security-oriented authentication tables

---

# Contributors

Project developed collaboratively as part of a software engineering and full-stack development course project.

---

# License

This project is created for educational and academic purposes.

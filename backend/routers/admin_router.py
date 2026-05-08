"""
Admin router.
Endpoints for user management: list users, change roles, activate/deactivate.
All endpoints require the 'admin' role.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from core.database import get_session
from models.db_models import User, Role, AuditLog
from auth.dependencies import require_role
from schemas.auth_schemas import UserResponse, ChangeRoleRequest, ChangeStatusRequest

router = APIRouter(prefix="/admin", tags=["Admin"])


# ===================================================================
# LIST ALL USERS
# ===================================================================
@router.get("/users", response_model=list[UserResponse])
def list_users(
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()
    result = []
    for u in users:
        role = session.get(Role, u.role_id)
        result.append(UserResponse(
            id=u.id,
            full_name=u.full_name,
            email=u.email,
            role_id=u.role_id,
            role_name=role.name if role else None,
            is_active=u.is_active,
            created_at=u.created_at,
        ))
    return result


# ===================================================================
# GET SINGLE USER
# ===================================================================
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = session.get(Role, user.role_id)
    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role_id=user.role_id,
        role_name=role.name if role else None,
        is_active=user.is_active,
        created_at=user.created_at,
    )


# ===================================================================
# CHANGE USER ROLE
# ===================================================================
@router.put("/users/{user_id}/role", response_model=UserResponse)
def change_user_role(
    user_id: int,
    body: ChangeRoleRequest,
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot change your own role")

    new_role = session.exec(select(Role).where(Role.name == body.role_name)).first()
    if not new_role:
        raise HTTPException(
            status_code=400,
            detail=f"Role '{body.role_name}' does not exist. Valid roles: student, instructor, admin",
        )

    old_role = session.get(Role, user.role_id)
    user.role_id = new_role.id
    session.add(user)

    session.add(AuditLog(
        user_id=admin.id,
        action=f"CHANGE_ROLE_{old_role.name.upper()}_TO_{new_role.name.upper()}" if old_role else f"CHANGE_ROLE_TO_{new_role.name.upper()}",
        entity_type="user",
        entity_id=user.id,
    ))

    session.commit()
    session.refresh(user)

    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role_id=user.role_id,
        role_name=new_role.name,
        is_active=user.is_active,
        created_at=user.created_at,
    )


# ===================================================================
# CHANGE USER STATUS
# ===================================================================
@router.put("/users/{user_id}/status", response_model=UserResponse)
def change_user_status(
    user_id: int,
    body: ChangeStatusRequest,
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id and not body.is_active:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")

    user.is_active = body.is_active
    session.add(user)

    action = "ACTIVATE_USER" if body.is_active else "DEACTIVATE_USER"
    session.add(AuditLog(
        user_id=admin.id,
        action=action,
        entity_type="user",
        entity_id=user.id,
    ))

    session.commit()
    session.refresh(user)

    role = session.get(Role, user.role_id)
    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role_id=user.role_id,
        role_name=role.name if role else None,
        is_active=user.is_active,
        created_at=user.created_at,
    )


# ===================================================================
# AUDIT LOGS
# ===================================================================
@router.get("/audit-logs")
def get_audit_logs(
    limit: int = 50,
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    logs = session.exec(
        select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    ).all()

    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]

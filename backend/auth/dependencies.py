"""
FastAPI dependency functions for authentication and authorization.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session, select

from core.database import get_session
from models.db_models import User, Role
from auth.utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from the JWT access token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        user_id_str: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if user_id_str is None or token_type != "access":
            raise credentials_exception

        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    user = session.get(User, user_id)

    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    return user


def require_role(*allowed_roles: str):
    """
    Return a dependency that restricts the endpoint to specific roles.

    Usage:
        @router.post("/courses", dependencies=[Depends(require_role("instructor", "admin"))])
    """

    def dependency(
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ) -> User:
        role = session.get(Role, user.role_id)
        role_name = role.name if role else ""

        if role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role_name}' does not have permission. Required: {', '.join(allowed_roles)}",
            )

        user._role_name = role_name  # type: ignore[attr-defined]
        return user

    return dependency

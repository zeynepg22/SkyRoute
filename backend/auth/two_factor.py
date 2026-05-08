"""
Two-factor authentication service.
Supports: TOTP (Google Authenticator), Email OTP, Backup recovery codes, Trusted device.
"""

import os
from datetime import datetime, timedelta, timezone

import pyotp
from sqlmodel import Session, select

from models.db_models import TwoFactorMethod, BackupCode, User
from auth.utils import hash_password, verify_password, generate_otp, generate_backup_codes, generate_device_token


# ---------------------------------------------------------------------------
# Cached email OTPs  (in production use Redis or DB)
# ---------------------------------------------------------------------------
_email_otp_store: dict[int, dict] = {}


# ---------------------------------------------------------------------------
# TOTP  (Google Authenticator)
# ---------------------------------------------------------------------------
def setup_totp(session: Session, user: User) -> dict:
    """Create or overwrite a TOTP secret for the user. Returns secret + provisioning URI."""
    secret = pyotp.random_base32()
    provisioning_uri = pyotp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name="SkyRoute",
    )

    existing = session.exec(
        select(TwoFactorMethod).where(
            TwoFactorMethod.user_id == user.id,
            TwoFactorMethod.method_type == "totp",
        )
    ).first()

    if existing:
        existing.secret_value = secret
        existing.is_enabled = True
    else:
        session.add(TwoFactorMethod(
            user_id=user.id,
            method_type="totp",
            is_enabled=True,
            secret_value=secret,
        ))

    session.commit()
    return {"secret": secret, "provisioning_uri": provisioning_uri}


def verify_totp(session: Session, user_id: int, code: str) -> bool:
    method = session.exec(
        select(TwoFactorMethod).where(
            TwoFactorMethod.user_id == user_id,
            TwoFactorMethod.method_type == "totp",
            TwoFactorMethod.is_enabled == True,
        )
    ).first()

    if not method or not method.secret_value:
        return False

    totp = pyotp.TOTP(method.secret_value)
    return totp.verify(code, valid_window=1)


# ---------------------------------------------------------------------------
# Email OTP
# ---------------------------------------------------------------------------
def setup_email_otp(session: Session, user: User) -> None:
    """Enable email OTP for the user."""
    existing = session.exec(
        select(TwoFactorMethod).where(
            TwoFactorMethod.user_id == user.id,
            TwoFactorMethod.method_type == "email_otp",
        )
    ).first()

    if existing:
        existing.is_enabled = True
        existing.secret_value = user.email
    else:
        session.add(TwoFactorMethod(
            user_id=user.id,
            method_type="email_otp",
            is_enabled=True,
            secret_value=user.email,
        ))
    session.commit()


def send_email_otp(user_id: int, email: str) -> str:
    """
    Generate and 'send' an OTP to the user's email.
    In development: prints to console.
    In production: integrate with fastapi-mail or SMTP.
    """
    code = generate_otp(6)
    _email_otp_store[user_id] = {
        "code": code,
        "expires": datetime.now(timezone.utc) + timedelta(minutes=5),
    }

    smtp_host = os.getenv("SMTP_HOST")
    if smtp_host:
        print(f"[EMAIL] OTP sent to {email}")
    else:
        print(f"[DEV EMAIL OTP] User {user_id} ({email}): {code}")

    return code


def verify_email_otp(user_id: int, code: str) -> bool:
    stored = _email_otp_store.get(user_id)
    if not stored:
        return False
    if datetime.now(timezone.utc) > stored["expires"]:
        _email_otp_store.pop(user_id, None)
        return False
    if stored["code"] != code:
        return False
    _email_otp_store.pop(user_id, None)
    return True


# ---------------------------------------------------------------------------
# Backup Recovery Codes
# ---------------------------------------------------------------------------
def create_backup_codes(session: Session, user_id: int) -> list[str]:
    """Generate new backup codes, replace any existing ones."""
    old_codes = session.exec(
        select(BackupCode).where(BackupCode.user_id == user_id)
    ).all()
    for code in old_codes:
        session.delete(code)

    method = session.exec(
        select(TwoFactorMethod).where(
            TwoFactorMethod.user_id == user_id,
            TwoFactorMethod.method_type == "backup_codes",
        )
    ).first()
    if not method:
        session.add(TwoFactorMethod(
            user_id=user_id,
            method_type="backup_codes",
            is_enabled=True,
        ))
    else:
        method.is_enabled = True

    plain_codes = generate_backup_codes(8)
    for plain in plain_codes:
        session.add(BackupCode(
            user_id=user_id,
            code_hash=hash_password(plain),
            is_used=False,
        ))

    session.commit()
    return plain_codes


def verify_backup_code(session: Session, user_id: int, code: str) -> bool:
    codes = session.exec(
        select(BackupCode).where(
            BackupCode.user_id == user_id,
            BackupCode.is_used == False,
        )
    ).all()

    for bc in codes:
        if verify_password(code, bc.code_hash):
            bc.is_used = True
            session.add(bc)
            session.commit()
            return True

    return False


# ---------------------------------------------------------------------------
# Trusted Device
# ---------------------------------------------------------------------------
def setup_trusted_device(session: Session, user: User) -> None:
    """Enable trusted device method."""
    existing = session.exec(
        select(TwoFactorMethod).where(
            TwoFactorMethod.user_id == user.id,
            TwoFactorMethod.method_type == "trusted_device",
        )
    ).first()
    if existing:
        existing.is_enabled = True
    else:
        session.add(TwoFactorMethod(
            user_id=user.id,
            method_type="trusted_device",
            is_enabled=True,
        ))
    session.commit()


def create_trusted_device_token(session: Session, user_id: int) -> str:
    """Create a new trusted device token stored in the DB."""
    token = generate_device_token()
    method = session.exec(
        select(TwoFactorMethod).where(
            TwoFactorMethod.user_id == user_id,
            TwoFactorMethod.method_type == "trusted_device",
        )
    ).first()

    if method:
        method.secret_value = hash_password(token)
        session.add(method)
    else:
        session.add(TwoFactorMethod(
            user_id=user_id,
            method_type="trusted_device",
            is_enabled=True,
            secret_value=hash_password(token),
        ))

    session.commit()
    return token


def verify_trusted_device(session: Session, user_id: int, token: str) -> bool:
    method = session.exec(
        select(TwoFactorMethod).where(
            TwoFactorMethod.user_id == user_id,
            TwoFactorMethod.method_type == "trusted_device",
            TwoFactorMethod.is_enabled == True,
        )
    ).first()

    if not method or not method.secret_value:
        return False

    return verify_password(token, method.secret_value)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def get_enabled_2fa_methods(session: Session, user_id: int) -> list[str]:
    """Return list of enabled 2FA method names for a user."""
    methods = session.exec(
        select(TwoFactorMethod).where(
            TwoFactorMethod.user_id == user_id,
            TwoFactorMethod.is_enabled == True,
        )
    ).all()
    return [m.method_type for m in methods]


def has_any_2fa(session: Session, user_id: int) -> bool:
    return len(get_enabled_2fa_methods(session, user_id)) > 0

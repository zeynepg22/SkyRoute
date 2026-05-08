import os
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import RedirectResponse
from middleware.security import limiter
from sqlmodel import Session, select

from core.database import get_session
from models.db_models import User, Role, SocialAccount, AuditLog
from auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    create_temp_token,
    decode_token,
)
from auth.dependencies import get_current_user
from auth.two_factor import (
    setup_totp,
    verify_totp,
    setup_email_otp,
    send_email_otp,
    verify_email_otp,
    create_backup_codes,
    verify_backup_code,
    setup_trusted_device,
    create_trusted_device_token,
    verify_trusted_device,
    get_enabled_2fa_methods,
    has_any_2fa,
)
from auth.oauth import (
    build_authorize_url,
    exchange_code_for_token,
    fetch_user_info,
    get_or_create_social_user,
)
from schemas.auth_schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    TwoFactorRequiredResponse,
    RefreshRequest,
    Verify2FARequest,
    TOTPSetupResponse,
    BackupCodesResponse,
    TrustedDeviceResponse,
    MeResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ===================================================================
# REGISTER
# ===================================================================
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
@limiter.limit("10/minute")
def register(request: Request, body: RegisterRequest, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == body.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    student_role = session.exec(select(Role).where(Role.name == "student")).first()
    if not student_role:
        raise HTTPException(status_code=500, detail="Default role 'student' not found. Run seed first.")

    user = User(
        full_name=body.full_name,
        email=body.email,
        password_hash=hash_password(body.password),
        role_id=student_role.id,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    session.add(AuditLog(user_id=user.id, action="REGISTER", entity_type="user", entity_id=user.id))
    session.commit()

    access_token = create_access_token(user.id, student_role.name)
    refresh_token = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# ===================================================================
# LOGIN
# ===================================================================
@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, body: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == body.email)).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    role = session.get(Role, user.role_id)
    role_name = role.name if role else "student"

    methods = get_enabled_2fa_methods(session, user.id)
    if methods:
        temp_token = create_temp_token(user.id)
        return TwoFactorRequiredResponse(
            requires_2fa=True,
            temp_token=temp_token,
            available_methods=methods,
        )

    session.add(AuditLog(user_id=user.id, action="LOGIN", entity_type="user", entity_id=user.id))
    session.commit()

    access_token = create_access_token(user.id, role_name)
    refresh_token = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# ===================================================================
# VERIFY 2FA
# ===================================================================
@router.post("/verify-2fa", response_model=TokenResponse)
@limiter.limit("5/minute")
def verify_2fa(request: Request, body: Verify2FARequest, session: Session = Depends(get_session)):
    try:
        payload = decode_token(body.temp_token)
        if payload.get("type") != "2fa_temp":
            raise HTTPException(status_code=401, detail="Invalid temp token")
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired temp token")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    verified = False

    if body.method == "totp":
        verified = verify_totp(session, user_id, body.code)
    elif body.method == "email_otp":
        verified = verify_email_otp(user_id, body.code)
    elif body.method == "backup_code":
        verified = verify_backup_code(session, user_id, body.code)
    elif body.method == "trusted_device":
        verified = verify_trusted_device(session, user_id, body.code)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown 2FA method: {body.method}")

    if not verified:
        raise HTTPException(status_code=401, detail="Invalid 2FA code")

    role = session.get(Role, user.role_id)
    role_name = role.name if role else "student"

    session.add(AuditLog(user_id=user.id, action="LOGIN_2FA", entity_type="user", entity_id=user.id))
    session.commit()

    access_token = create_access_token(user.id, role_name)
    refresh_token = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# ===================================================================
# SEND EMAIL OTP
# ===================================================================
@router.post("/send-email-otp")
@limiter.limit("3/minute")
def send_otp_endpoint(request: Request, body: dict, session: Session = Depends(get_session)):
    """Send an email OTP. Expects {"temp_token": "..."}."""
    temp_token = body.get("temp_token", "")
    try:
        payload = decode_token(temp_token)
        if payload.get("type") != "2fa_temp":
            raise HTTPException(status_code=401, detail="Invalid temp token")
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired temp token")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    send_email_otp(user.id, user.email)
    return {"message": "OTP sent to your email"}


# ===================================================================
# REFRESH TOKEN
# ===================================================================
@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshRequest, session: Session = Depends(get_session)):
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = session.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or deactivated")

    role = session.get(Role, user.role_id)
    role_name = role.name if role else "student"

    new_access = create_access_token(user.id, role_name)
    new_refresh = create_refresh_token(user.id)
    return TokenResponse(access_token=new_access, refresh_token=new_refresh)


# ===================================================================
# ME
# ===================================================================
@router.get("/me", response_model=MeResponse)
def get_me(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    role = session.get(Role, current_user.role_id)
    socials = session.exec(
        select(SocialAccount).where(SocialAccount.user_id == current_user.id)
    ).all()

    return MeResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        role_name=role.name if role else "student",
        is_active=current_user.is_active,
        has_2fa=has_any_2fa(session, current_user.id),
        social_providers=[s.provider for s in socials],
    )


# ===================================================================
# 2FA SETUP ENDPOINTS
# ===================================================================
@router.post("/2fa/setup/totp", response_model=TOTPSetupResponse)
def setup_totp_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    result = setup_totp(session, current_user)
    session.add(AuditLog(user_id=current_user.id, action="SETUP_TOTP", entity_type="user", entity_id=current_user.id))
    session.commit()
    return TOTPSetupResponse(secret=result["secret"], provisioning_uri=result["provisioning_uri"])


@router.post("/2fa/setup/email-otp")
def setup_email_otp_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    setup_email_otp(session, current_user)
    session.add(AuditLog(user_id=current_user.id, action="SETUP_EMAIL_OTP", entity_type="user", entity_id=current_user.id))
    session.commit()
    return {"message": "Email OTP enabled"}


@router.post("/2fa/setup/trusted-device", response_model=TrustedDeviceResponse)
def setup_trusted_device_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    setup_trusted_device(session, current_user)
    token = create_trusted_device_token(session, current_user.id)
    session.add(AuditLog(user_id=current_user.id, action="SETUP_TRUSTED_DEVICE", entity_type="user", entity_id=current_user.id))
    session.commit()
    return TrustedDeviceResponse(device_token=token, message="Save this token. It will be used to skip 2FA on this device.")


@router.post("/2fa/backup-codes", response_model=BackupCodesResponse)
def generate_backup_codes_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    codes = create_backup_codes(session, current_user.id)
    session.add(AuditLog(user_id=current_user.id, action="GENERATE_BACKUP_CODES", entity_type="user", entity_id=current_user.id))
    session.commit()
    return BackupCodesResponse(codes=codes)


@router.get("/2fa/methods")
def get_2fa_methods(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    methods = get_enabled_2fa_methods(session, current_user.id)
    return {"methods": methods}


# ===================================================================
# SOCIAL LOGIN
# ===================================================================
SUPPORTED_PROVIDERS = ["google", "github", "discord", "facebook"]


@router.get("/social/{provider}")
def social_login_redirect(provider: str):
    """Redirect user to the OAuth provider's login page."""
    if provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")
    url = build_authorize_url(provider)
    return RedirectResponse(url=url)


@router.get("/callback/{provider}")
async def social_callback(
    provider: str,
    code: str = Query(...),
    session: Session = Depends(get_session),
):
    """Handle OAuth callback from the provider."""
    if provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")

    try:
        access_token = await exchange_code_for_token(provider, code)
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token from provider")
        user_info = await fetch_user_info(provider, access_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

    if not user_info.get("email"):
        raise HTTPException(status_code=400, detail="Email not provided by the provider")

    user = get_or_create_social_user(
        session=session,
        provider_name=provider,
        provider_user_id=user_info["provider_user_id"],
        email=user_info["email"],
        full_name=user_info.get("name", ""),
    )

    role = session.get(Role, user.role_id)
    role_name = role.name if role else "student"

    session.add(AuditLog(user_id=user.id, action=f"SOCIAL_LOGIN_{provider.upper()}", entity_type="user", entity_id=user.id))
    session.commit()

    jwt_access = create_access_token(user.id, role_name)
    jwt_refresh = create_refresh_token(user.id)

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return RedirectResponse(
        url=f"{frontend_url}/auth/callback?access_token={jwt_access}&refresh_token={jwt_refresh}"
    )

"""
Pydantic request / response schemas for authentication endpoints.
"""

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


# ---------------------------------------------------------------------------
# Register / Login
# ---------------------------------------------------------------------------
class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class TwoFactorRequiredResponse(BaseModel):
    requires_2fa: bool = True
    temp_token: str
    available_methods: list[str]


class RefreshRequest(BaseModel):
    refresh_token: str


# ---------------------------------------------------------------------------
# 2FA
# ---------------------------------------------------------------------------
class Verify2FARequest(BaseModel):
    temp_token: str
    method: str = Field(description="totp | email_otp | backup_code | trusted_device")
    code: str


class Enable2FARequest(BaseModel):
    method: str = Field(description="totp | email_otp | trusted_device")


class TOTPSetupResponse(BaseModel):
    secret: str
    provisioning_uri: str


class BackupCodesResponse(BaseModel):
    codes: list[str]


class TrustedDeviceResponse(BaseModel):
    device_token: str
    message: str


# ---------------------------------------------------------------------------
# Social Login
# ---------------------------------------------------------------------------
class SocialAuthStart(BaseModel):
    redirect_url: str


class SocialCallbackRequest(BaseModel):
    code: str
    state: str | None = None


# ---------------------------------------------------------------------------
# User / Admin
# ---------------------------------------------------------------------------
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role_id: int
    role_name: str | None = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ChangeRoleRequest(BaseModel):
    role_name: str = Field(description="student | instructor | admin")


class ChangeStatusRequest(BaseModel):
    is_active: bool


class MeResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role_name: str
    is_active: bool
    has_2fa: bool
    social_providers: list[str]

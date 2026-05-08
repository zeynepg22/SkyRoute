"""
Social login (OAuth 2.0 Authorization Code Flow).
Providers: Google, GitHub, Discord, Facebook.
"""

import os
from dataclasses import dataclass

import httpx
from sqlmodel import Session, select

from models.db_models import User, SocialAccount, Role
from auth.utils import hash_password


@dataclass
class OAuthProvider:
    name: str
    client_id: str
    client_secret: str
    authorize_url: str
    token_url: str
    userinfo_url: str
    scopes: str
    redirect_uri: str


def _env(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def get_provider(name: str) -> OAuthProvider:
    base_redirect = _env("OAUTH_REDIRECT_BASE", "http://localhost:8000")

    providers = {
        "google": OAuthProvider(
            name="google",
            client_id=_env("GOOGLE_CLIENT_ID"),
            client_secret=_env("GOOGLE_CLIENT_SECRET"),
            authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
            token_url="https://oauth2.googleapis.com/token",
            userinfo_url="https://www.googleapis.com/oauth2/v2/userinfo",
            scopes="openid email profile",
            redirect_uri=f"{base_redirect}/auth/callback/google",
        ),
        "github": OAuthProvider(
            name="github",
            client_id=_env("GITHUB_CLIENT_ID"),
            client_secret=_env("GITHUB_CLIENT_SECRET"),
            authorize_url="https://github.com/login/oauth/authorize",
            token_url="https://github.com/login/oauth/access_token",
            userinfo_url="https://api.github.com/user",
            scopes="user:email",
            redirect_uri=f"{base_redirect}/auth/callback/github",
        ),
        "discord": OAuthProvider(
            name="discord",
            client_id=_env("DISCORD_CLIENT_ID"),
            client_secret=_env("DISCORD_CLIENT_SECRET"),
            authorize_url="https://discord.com/api/oauth2/authorize",
            token_url="https://discord.com/api/oauth2/token",
            userinfo_url="https://discord.com/api/users/@me",
            scopes="identify email",
            redirect_uri=f"{base_redirect}/auth/callback/discord",
        ),
        "facebook": OAuthProvider(
            name="facebook",
            client_id=_env("FACEBOOK_CLIENT_ID"),
            client_secret=_env("FACEBOOK_CLIENT_SECRET"),
            authorize_url="https://www.facebook.com/v18.0/dialog/oauth",
            token_url="https://graph.facebook.com/v18.0/oauth/access_token",
            userinfo_url="https://graph.facebook.com/me?fields=id,name,email",
            scopes="email public_profile",
            redirect_uri=f"{base_redirect}/auth/callback/facebook",
        ),
    }

    if name not in providers:
        raise ValueError(f"Unsupported provider: {name}")

    return providers[name]


def build_authorize_url(provider_name: str, state: str | None = None) -> str:
    """Build the redirect URL that sends the user to the provider login page."""
    p = get_provider(provider_name)
    params = {
        "client_id": p.client_id,
        "redirect_uri": p.redirect_uri,
        "response_type": "code",
        "scope": p.scopes,
    }
    if state:
        params["state"] = state
    if provider_name == "discord":
        params["prompt"] = "consent"

    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{p.authorize_url}?{query}"


async def exchange_code_for_token(provider_name: str, code: str) -> str:
    """Exchange the authorization code for an access token."""
    p = get_provider(provider_name)

    data = {
        "client_id": p.client_id,
        "client_secret": p.client_secret,
        "code": code,
        "redirect_uri": p.redirect_uri,
    }

    headers = {"Accept": "application/json"}

    if provider_name in ("google", "facebook", "discord"):
        data["grant_type"] = "authorization_code"

    async with httpx.AsyncClient() as client:
        resp = await client.post(p.token_url, data=data, headers=headers)
        resp.raise_for_status()
        token_data = resp.json()

    return token_data.get("access_token", "")


async def fetch_user_info(provider_name: str, access_token: str) -> dict:
    """Fetch user profile from the provider using the access token."""
    p = get_provider(provider_name)
    headers = {"Authorization": f"Bearer {access_token}"}

    if provider_name == "github":
        headers["Accept"] = "application/vnd.github+json"

    async with httpx.AsyncClient() as client:
        resp = await client.get(p.userinfo_url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    if provider_name == "google":
        return {
            "provider_user_id": str(data["id"]),
            "email": data.get("email", ""),
            "name": data.get("name", ""),
        }
    elif provider_name == "github":
        email = data.get("email", "")
        if not email:
            email = await _fetch_github_email(access_token)
        return {
            "provider_user_id": str(data["id"]),
            "email": email,
            "name": data.get("name") or data.get("login", ""),
        }
    elif provider_name == "discord":
        return {
            "provider_user_id": str(data["id"]),
            "email": data.get("email", ""),
            "name": data.get("username", ""),
        }
    elif provider_name == "facebook":
        return {
            "provider_user_id": str(data["id"]),
            "email": data.get("email", ""),
            "name": data.get("name", ""),
        }

    return data


async def _fetch_github_email(access_token: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
        )
        if resp.status_code == 200:
            emails = resp.json()
            for e in emails:
                if e.get("primary") and e.get("verified"):
                    return e["email"]
            if emails:
                return emails[0].get("email", "")
    return ""


def get_or_create_social_user(
    session: Session,
    provider_name: str,
    provider_user_id: str,
    email: str,
    full_name: str,
) -> User:
    """Find existing user by social account link, or by email, or create new."""
    social = session.exec(
        select(SocialAccount).where(
            SocialAccount.provider == provider_name,
            SocialAccount.provider_user_id == provider_user_id,
        )
    ).first()

    if social:
        user = session.get(User, social.user_id)
        if user:
            return user

    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user:
        student_role = session.exec(
            select(Role).where(Role.name == "student")
        ).first()

        user = User(
            full_name=full_name or email.split("@")[0],
            email=email,
            password_hash=hash_password(os.urandom(32).hex()),
            role_id=student_role.id if student_role else 1,
            is_active=True,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    session.add(SocialAccount(
        user_id=user.id,
        provider=provider_name,
        provider_user_id=provider_user_id,
    ))
    session.commit()

    return user

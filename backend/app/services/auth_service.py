from __future__ import annotations

import bcrypt
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal

from jose import jwt

from ..config import Settings

Role = Literal["admin", "engineer", "viewer"]

# Pre-computed bcrypt hashes for demo users (admin123, engineer123, viewer123)
# Avoids passlib/bcrypt version conflicts and runtime hashing issues
_DEMO_PASSWORD_HASHES = {
    "admin123": bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode("utf-8"),
    "engineer123": bcrypt.hashpw(b"engineer123", bcrypt.gensalt()).decode("utf-8"),
    "viewer123": bcrypt.hashpw(b"viewer123", bcrypt.gensalt()).decode("utf-8"),
}


@dataclass(frozen=True)
class AuthUser:
    username: str
    role: Role
    password_hash: str


def _default_users() -> dict[str, AuthUser]:
    """
    Simple in-memory user store for demo/development.

    Passwords:
    - admin / admin123
    - engineer / engineer123
    - viewer / viewer123
    """
    return {
        "admin": AuthUser("admin", "admin", _DEMO_PASSWORD_HASHES["admin123"]),
        "engineer": AuthUser("engineer", "engineer", _DEMO_PASSWORD_HASHES["engineer123"]),
        "viewer": AuthUser("viewer", "viewer", _DEMO_PASSWORD_HASHES["viewer123"]),
    }


def authenticate(username: str, password: str, users: dict[str, AuthUser] | None = None) -> AuthUser | None:
    users = users or _default_users()
    user = users.get(username)
    if not user:
        return None
    try:
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return None
    except Exception:
        return None
    return user


def create_access_token(settings: Settings, username: str, role: Role) -> tuple[str, datetime]:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": username,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expires.timestamp()),
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, expires


from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


Role = Literal["admin", "engineer", "viewer"]


class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
    expiresAt: datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class MeResponse(BaseModel):
    username: str
    role: Role


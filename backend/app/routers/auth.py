from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ..config import Settings
from ..dependencies import User, get_settings_dep, get_current_user
from ..models.auth import LoginRequest, MeResponse, TokenResponse
from ..services.auth_service import authenticate, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, settings: Settings = Depends(get_settings_dep)):
    user = authenticate(body.username, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token, expires_at = create_access_token(settings, username=user.username, role=user.role)
    return TokenResponse(accessToken=token, expiresAt=expires_at)


@router.get("/me", response_model=MeResponse)
def me(current_user: User = Depends(get_current_user)):
    return MeResponse(username=current_user.username, role=current_user.role)


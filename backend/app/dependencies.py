from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .config import Settings, get_settings
from .services.plant_loader import get_plant_loader
from .models.auth import Role


class User:
    def __init__(self, username: str, role: Role):
        self.username = username
        self.role = role


def get_settings_dep() -> Settings:
    return get_settings()


def get_repo_root() -> Path:
    # backend/app -> backend -> repo root
    return Path(__file__).resolve().parents[2]


def get_plantdata(settings: Settings = Depends(get_settings_dep)):
    loader = get_plant_loader(
        repo_root=get_repo_root(),
        openoa_example_zip_path=settings.openoa_example_zip_path,
        data_dir=settings.data_dir,
    )
    return loader.get_plant()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    settings: Settings = Depends(get_settings_dep),
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username = payload.get("sub")
        role = payload.get("role")
        if not username or role not in ("admin", "engineer", "viewer"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return User(username=username, role=role)  # type: ignore[arg-type]
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def require_role(required_role: str):
    def dependency(user: User = Depends(get_current_user)) -> User:
        # Very basic role check placeholder
        role_order = {"viewer": 0, "engineer": 1, "admin": 2}
        if role_order.get(user.role, -1) < role_order.get(required_role, 0):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return dependency


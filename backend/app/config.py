from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    api_v1_prefix: str = "/api"
    # CORS: env BACKEND_CORS_ORIGINS as comma-separated string (e.g. "http://localhost:3000,http://127.0.0.1:3000")
    backend_cors_origins: str = "http://localhost:3000"

    # Auth
    jwt_secret_key: str = "CHANGE_ME_SUPER_SECRET_KEY"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 8

    # OpenOA / data
    openoa_example_zip_path: str = "examples/data/la_haute_borne.zip"
    data_dir: str = "backend_data"

    def get_cors_origins_list(self) -> List[str]:
        return [x.strip() for x in self.backend_cors_origins.split(",") if x.strip()] or ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


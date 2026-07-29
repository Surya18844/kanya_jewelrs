"""
Centralized application configuration.
All secrets / environment-specific values are read from environment
variables (via a .env file in development). Never hard-code secrets.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/kanya_jewelers"

    # JWT
    jwt_secret_key: str = "insecure-dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 120

    # Default admin (seeded once on first run)
    default_admin_username: str = "admin"
    default_admin_password: str = "admin123"

    # CORS
    allowed_origins: str = "http://localhost:5500,http://127.0.0.1:5500"

    # Cloudinary (optional)
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    # Local fallback storage
    backend_base_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def cloudinary_enabled(self) -> bool:
        return bool(self.cloudinary_cloud_name and self.cloudinary_api_key and self.cloudinary_api_secret)


settings = Settings()

# backend/app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "InvoMatch"
    APP_VERSION: str = "1.0.0"
    ENV: str = "production"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = "change-me-in-production-use-a-long-random-string"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Database — Render gives postgres://, we fix it to postgresql:// in database.py
    DATABASE_URL: str = "postgresql://invo_match:devpass@localhost/invo_match"

    # Redis — optional
    REDIS_URL: Optional[str] = None

    # SMTP — optional
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM: str = "noreply@invomatch.io"

    # Pagination
    DEFAULT_PAGE_LIMIT: int = 20
    MAX_PAGE_LIMIT: int = 100

    @property
    def db_url(self) -> str:
        """Always returns a SQLAlchemy-compatible URL."""
        if self.DATABASE_URL.startswith("postgres://"):
            return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return self.DATABASE_URL

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

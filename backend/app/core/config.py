from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings and configuration."""

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 240  # 4 hours

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:4200"]

    # Application
    PROJECT_NAME: str = "Leather Accessories Store"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # Email/SMTP Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_TLS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

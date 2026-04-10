"""
Application configuration module using Pydantic Settings.
Loads environment variables from .env file with proper validation.
"""

from typing import Optional
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """FastAPI application settings with environment variable support."""

    # =========================
    # APPLICATION SETTINGS
    # =========================
    APP_NAME: str = "Aura Gallery"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # =========================
    # DATABASE CONFIGURATION
    # =========================
    DATABASE_URL: str = "sqlite:///./aura_gallery.db"
    DATABASE_ECHO: bool = False  # Set to True for SQL logging in debug mode
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # =========================
    # SECURITY CONFIGURATION
    # =========================
    SECRET_KEY: SecretStr = Field(default="your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # =========================
    # CLOUDINARY CONFIGURATION
    # =========================
    CLOUDINARY_CLOUD_NAME: str = Field(default="", description="Cloudinary cloud name")
    CLOUDINARY_API_KEY: str = Field(default="", description="Cloudinary API key")
    CLOUDINARY_API_SECRET: str = Field(default="", description="Cloudinary API secret")

    # =========================
    # GOOGLE OAUTH CONFIGURATION
    # =========================
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, description="Google OAuth client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, description="Google OAuth secret")
    GOOGLE_REDIRECT_URI: Optional[str] = Field(default=None, description="Google redirect URI")

    # =========================
    # CORS CONFIGURATION
    # =========================
    CORS_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # =========================
    # PYDANTIC MODEL CONFIGURATION
    # =========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


# Global settings instance
settings = Settings()
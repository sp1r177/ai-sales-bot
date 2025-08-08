from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    # App
    APP_ENV: str = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # CORS
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,https://vk.com"

    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # LLM
    LLM_PROVIDER: str = "gigachat"  # gigachat | yandexgpt
    LLM_API_URL: str | None = None  # MUST be set based on provider official docs
    LLM_API_KEY: str | None = None
    LLM_MODEL: str = "gigachat"
    LLM_TIMEOUT_SECONDS: int = 30

    # VK
    VK_APP_ID: int | None = None
    VK_SERVICE_KEY: str | None = None
    VK_SECURE_KEY: str | None = None

    # Frontend
    VITE_API_BASE: str = "http://localhost:8000"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]
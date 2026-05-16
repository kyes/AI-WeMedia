"""Application configuration using pydantic-settings."""
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────
    app_name: str = "AI智能自媒体运营平台"
    app_version: str = "0.1.0"
    app_env: Literal["development", "testing", "production"] = "development"
    app_debug: bool = True
    app_secret_key: str = "changeme-in-production-at-least-32-chars!!"
    app_allowed_hosts: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ── Database ─────────────────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://wemedia:wemedia123@localhost:5432/wemedia_db"
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # SQLite fallback for tests / local dev without Postgres
    @property
    def effective_database_url(self) -> str:
        return self.database_url

    # ── Redis / Celery ───────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_ttl: int = 3600
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # ── JWT ──────────────────────────────────────────────────────────────
    jwt_secret_key: str = "changeme-jwt-secret-32-chars-minimum!!"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 30

    # ── AI Models ────────────────────────────────────────────────────────
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    baidu_wenxin_api_key: str = ""
    baidu_wenxin_secret_key: str = ""
    tongyi_api_key: str = ""
    default_ai_provider: Literal["openai", "anthropic", "wenxin", "tongyi"] = "openai"

    # ── Notifications ────────────────────────────────────────────────────
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    wechat_work_webhook: str = ""

    # ── Storage ──────────────────────────────────────────────────────────
    storage_backend: Literal["local", "s3"] = "local"
    local_storage_path: str = "./storage"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_s3_bucket: str = ""
    aws_s3_region: str = "ap-east-1"

    # ── Rate Limiting ────────────────────────────────────────────────────
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    @field_validator("app_allowed_hosts", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v: str | list) -> list[str]:
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_testing(self) -> bool:
        return self.app_env == "testing"


@lru_cache
def get_settings() -> Settings:
    return Settings()

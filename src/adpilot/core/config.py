"""Application configuration and environment validation."""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(str, Enum):
    """Supported deployment environments."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class LogFormat(str, Enum):
    """Supported logging formats."""

    JSON = "json"
    CONSOLE = "console"


class AdPilotConfig(BaseSettings):
    """Application configuration loaded from environment variables and .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # Core Application & Environment
    app_name: str = Field(default="ADPilot Pro", alias="APP_NAME")
    app_version: str = Field(default="2.0.0", alias="APP_VERSION")
    environment: str = Field(default=AppEnvironment.DEVELOPMENT.value, alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")

    # API Versioning Prefixes
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    api_legacy_prefix: str = Field(default="/api", alias="API_LEGACY_PREFIX")

    # LLM Providers & Models
    llm_provider: str = Field(default="openrouter", alias="LLM_PROVIDER")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", alias="OPENAI_MODEL")
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_model: str = Field(default="openrouter/free", alias="OPENROUTER_MODEL")
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        alias="OPENROUTER_BASE_URL",
    )
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-5-sonnet-latest", alias="ANTHROPIC_MODEL")
    ollama_base_url: str = Field(default="http://localhost:11434/v1", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="qwen3:8b", alias="OLLAMA_MODEL")
    hf_token: str = Field(default="", alias="HF_TOKEN")
    hf_model: str = Field(default="deepseek-ai/DeepSeek-R1", alias="HF_MODEL")
    hf_base_url: str = Field(default="https://router.huggingface.co/v1", alias="HF_BASE_URL")
    temperature: float = Field(default=0.2, alias="TEMPERATURE")

    # Third-party Integrations
    serpapi_api_key: str = Field(default="", alias="SERPAPI_API_KEY")
    cloudinary_cloud_name: str = Field(default="", alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(default="", alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(default="", alias="CLOUDINARY_API_SECRET")

    # Database Settings
    database_url: str = Field(default="sqlite+aiosqlite:///./adpilot.db", alias="DATABASE_URL")
    db_pool_size: int = Field(default=5, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=10, alias="DB_MAX_OVERFLOW")
    db_pool_timeout: float = Field(default=30.0, alias="DB_POOL_TIMEOUT")
    db_pool_recycle: int = Field(default=1800, alias="DB_POOL_RECYCLE")
    db_echo: bool = Field(default=False, alias="DB_ECHO")

    # Redis Settings
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    redis_max_connections: int = Field(default=10, alias="REDIS_MAX_CONNECTIONS")
    redis_socket_timeout: float = Field(default=5.0, alias="REDIS_SOCKET_TIMEOUT")
    redis_enabled: bool = Field(default=True, alias="REDIS_ENABLED")

    # Background Worker Settings
    worker_concurrency: int = Field(default=10, alias="WORKER_CONCURRENCY")
    worker_queue_name: str = Field(default="adpilot:tasks", alias="WORKER_QUEUE_NAME")
    worker_poll_delay: float = Field(default=0.5, alias="WORKER_POLL_DELAY")

    # Memory & Vector Storage
    memory_backend: str = Field(default="memory", alias="MEMORY_BACKEND")
    mongodb_url: str = Field(default="mongodb://localhost:27017", alias="MONGODB_URL")
    qdrant_mode: str = Field(default="local", alias="QDRANT_MODE")
    qdrant_path: str = Field(default="./storage/qdrant", alias="QDRANT_PATH")
    qdrant_url: str = Field(default="", alias="QDRANT_URL")
    qdrant_api_key: str = Field(default="", alias="QDRANT_API_KEY")

    # Structured Logging & Observability
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default=LogFormat.JSON.value, alias="LOG_FORMAT")
    correlation_id_header: str = Field(default="X-Request-ID", alias="CORRELATION_ID_HEADER")

    # Security & CORS
    api_key: str = Field(default="", alias="ADPILOT_API_KEY")
    allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:3001,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173,https://adpilot-pro-app.vercel.app",
        alias="ALLOWED_ORIGINS",
    )

    @field_validator("environment", mode="before")
    @classmethod
    def normalize_environment(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @property
    def is_production(self) -> bool:
        """Return True if running in production."""
        return self.environment == AppEnvironment.PRODUCTION.value

    @property
    def is_testing(self) -> bool:
        """Return True if running in test mode."""
        return self.environment == AppEnvironment.TEST.value

    @property
    def model_name(self) -> str:
        """Backward-compatible alias for older code/tests."""
        return self.openai_model

    def validate_environment(self) -> List[str]:
        """Verify configuration completeness and return a list of warnings or errors."""
        warnings: List[str] = []

        if self.is_production:
            if not self.api_key:
                warnings.append("ADPILOT_API_KEY is not set in production environment.")
            if "sqlite" in self.database_url:
                warnings.append("SQLite is configured for DATABASE_URL in production. PostgreSQL is recommended.")
            if not any([self.openai_api_key, self.openrouter_api_key, self.anthropic_api_key, self.hf_token]):
                warnings.append("No cloud LLM provider API key (OpenAI, OpenRouter, Anthropic, HF) is set in production.")

        return warnings


@lru_cache(maxsize=1)
def get_config() -> AdPilotConfig:
    """Return cached application settings singleton."""
    return AdPilotConfig()


def clear_config_cache() -> None:
    """Clear cached settings for testing."""
    get_config.cache_clear()

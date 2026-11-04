"""Runtime configuration.

Every credential is read from the environment (or `agent/.env` in development).
Nothing secret is hardcoded. Settings are validated once at import time; the
service refuses to start if a required value is missing or invalid.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: Literal["development", "test", "production"] = "development"
    log_level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    host: str = "0.0.0.0"  # noqa: S104 - bound inside container/private network only
    port: int = 8000

    agent_service_token: SecretStr = Field(min_length=32)

    gemini_api_key: SecretStr = Field(min_length=1)
    gemini_model_tier1: str = Field(min_length=1)
    gemini_model_tier2: str = Field(min_length=1)
    gemini_embedding_model: str = Field(min_length=1)

    qdrant_url: str = Field(min_length=1)
    qdrant_api_key: SecretStr = Field(min_length=1)
    qdrant_collection: str = Field(min_length=1)
    qdrant_score_threshold: float = Field(ge=0.0, le=1.0, default=0.72)

    redis_url: SecretStr = Field(min_length=1)

    langfuse_host: str = "https://cloud.langfuse.com"
    langfuse_public_key: SecretStr | None = None
    langfuse_secret_key: SecretStr | None = None

    agent_max_steps: int = Field(default=5, ge=1, le=5)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached accessor so settings are parsed once and can be overridden in tests."""
    return Settings()  # type: ignore[call-arg]

import logging
import warnings
from functools import lru_cache
from typing import Any

from google import genai
from qdrant_client import QdrantClient
import redis.asyncio as aioredis

from app.core.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_gemini_client() -> genai.Client | None:
    try:
        settings = get_settings()
        api_key = settings.gemini_api_key.get_secret_value()
        if not api_key:
            logger.warning("Gemini API key is not configured.")
            return None
        return genai.Client(api_key=api_key)
    except Exception as exc:
        logger.warning("Failed to initialize Gemini client: %s", exc)
        return None


@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient | None:
    try:
        settings = get_settings()
        api_key = (
            settings.qdrant_api_key.get_secret_value()
            if settings.qdrant_api_key
            else None
        )
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module="qdrant_client")
            return QdrantClient(
                url=settings.qdrant_url,
                api_key=api_key,
                timeout=3.0,
                check_compatibility=False,
            )
    except Exception as exc:
        logger.warning("Failed to initialize Qdrant client: %s", exc)
        return None


@lru_cache(maxsize=1)
def get_redis_client() -> aioredis.Redis | None:
    try:
        settings = get_settings()
        return aioredis.from_url(
            settings.redis_url.get_secret_value(),
            socket_connect_timeout=2.0,
            socket_timeout=2.0,
            decode_responses=True,
        )
    except Exception as exc:
        logger.warning("Failed to initialize Redis client: %s", exc)
        return None


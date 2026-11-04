"""Test bootstrap: NON-SECRET placeholder env so Settings validates without real services."""

import os

_TEST_ENV = {
    "APP_ENV": "test",
    "AGENT_SERVICE_TOKEN": "test-only-agent-token-not-used-anywhere-000000",
    "GEMINI_API_KEY": "test-placeholder",
    "GEMINI_MODEL_TIER1": "test-tier1",
    "GEMINI_MODEL_TIER2": "test-tier2",
    "GEMINI_EMBEDDING_MODEL": "test-embedding",
    "QDRANT_URL": "http://localhost:6333",
    "QDRANT_API_KEY": "test-placeholder",
    "QDRANT_COLLECTION": "test_collection",
    "REDIS_URL": "redis://localhost:6379",
}

for key, value in _TEST_ENV.items():
    os.environ.setdefault(key, value)

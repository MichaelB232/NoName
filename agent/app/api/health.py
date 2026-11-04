from datetime import UTC, datetime

from fastapi import APIRouter

from app.schemas.envelope import SuccessEnvelope

router = APIRouter(tags=["health"])


@router.get("/health", response_model=SuccessEnvelope[dict[str, str]])
async def health() -> SuccessEnvelope[dict[str, str]]:
    """Liveness probe. Public, no secrets, no external calls."""
    return SuccessEnvelope(
        data={"service": "agent", "status": "UP", "timestamp": datetime.now(UTC).isoformat()},
    )

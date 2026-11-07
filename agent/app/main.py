import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.api import audits, health
from app.core.config import get_settings
from app.schemas.envelope import ErrorBody, ErrorEnvelope

settings = get_settings()
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("agent")

app = FastAPI(
    title="Compliance-Agent AI Service",
    version="0.1.0",
    # Interactive docs only outside production (internal service).
    docs_url=None if settings.app_env == "production" else "/docs",
    redoc_url=None,
)

app.include_router(health.router)
app.include_router(audits.router)


def _error(status_code: int, code: str, message: str, details: list[object] | None = None) -> JSONResponse:
    body = ErrorEnvelope(error=ErrorBody(code=code, message=message, details=details or []))
    return JSONResponse(status_code=status_code, content=body.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return _error(400, "VALIDATION_ERROR", "Invalid input provided", list(exc.errors()))


@app.exception_handler(HTTPException)
async def http_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict) and "code" in exc.detail:
        return _error(exc.status_code, str(exc.detail["code"]), str(exc.detail.get("message", "")))
    return _error(exc.status_code, "HTTP_ERROR", str(exc.detail))


@app.exception_handler(Exception)
async def unhandled_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unexpected agent error", exc_info=exc)
    message = "An internal error occurred" if settings.app_env == "production" else str(exc)
    return _error(500, "INTERNAL_SERVER_ERROR", message)

"""Service-to-service authentication.

The agent service is internal: only the backend may call it. Requests must carry
`Authorization: Bearer <AGENT_SERVICE_TOKEN>`; the token lives in env only.
"""

import hmac
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings

_bearer = HTTPBearer(auto_error=False)


async def require_service_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    expected = settings.agent_service_token.get_secret_value()
    provided = credentials.credentials if credentials else ""
    # Constant-time comparison to avoid timing attacks.
    if not hmac.compare_digest(provided.encode(), expected.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "Invalid service token", "details": []},
        )

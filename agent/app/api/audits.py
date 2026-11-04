import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import require_service_token
from app.schemas.envelope import SuccessEnvelope
from app.schemas.report import AuditJobAccepted, AuditJobRequest

router = APIRouter(prefix="/v1/audits", tags=["audits"], dependencies=[Depends(require_service_token)])


@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=SuccessEnvelope[AuditJobAccepted])
async def start_audit(payload: AuditJobRequest) -> SuccessEnvelope[AuditJobAccepted]:
    """Accept an audit job. Progress is published to Redis; the backend relays it as SSE."""
    # Tenant isolation: the S3 object must live under this organization's prefix.
    if not payload.s3_key.startswith(f"org_{payload.organization_id}/"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "s3_key is outside the tenant prefix", "details": []},
        )

    job_id = str(uuid.uuid4())
    # TODO(phase-3): enqueue build_audit_graph().ainvoke(...) as a background task.
    return SuccessEnvelope(
        data=AuditJobAccepted(
            job_id=job_id,
            contract_id=payload.contract_id,
            progress_channel=f"audit-progress:{payload.organization_id}:{payload.contract_id}",
        ),
        message="Audit job accepted",
    )

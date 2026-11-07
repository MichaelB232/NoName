import asyncio
import logging
from typing import Any

from app.core.clients import get_redis_client
from app.graph.builder import build_audit_graph
from app.graph.state import AuditState
from app.schemas.report import (
    AuditJobRequest,
    AuditProgressEvent,
    ComplianceAuditReport,
    ComplianceMatrixItem,
)

logger = logging.getLogger(__name__)

STAGE_METADATA = {
    "clause_parser": {
        "progress": 25,
        "message": "Mengekstrak dan membedah klausul kontrak...",
    },
    "compliance_auditor": {
        "progress": 50,
        "message": "Mengaudit kepatuhan regulasi OJK & UU PDP dengan Qdrant RAG...",
    },
    "risk_evaluator": {
        "progress": 75,
        "message": "Menghitung deterministik risiko suku bunga dan potensi denda...",
    },
    "legal_drafter": {
        "progress": 100,
        "message": "Menyusun draf klausul perbaikan patuh hukum...",
    },
}


async def publish_progress(
    channel: str,
    event: AuditProgressEvent,
    redis_client: Any | None = None,
) -> None:
    """Mengirim event progres audit ke Redis Pub/Sub channel."""
    try:
        client = redis_client if redis_client is not None else get_redis_client()
        if client:
            payload = event.model_dump_json()
            async with asyncio.timeout(1.0):
                await client.publish(channel, payload)
    except Exception as exc:
        logger.warning("Gagal mengirim event progres ke Redis: %s", exc)


def calculate_compliance_score(findings: list[ComplianceMatrixItem]) -> float:
    """Menghitung persentase klausul yang patuh."""
    if not findings:
        return 100.0
    compliant_count = sum(1 for item in findings if item.status == "COMPLIANT")
    return round((compliant_count / len(findings)) * 100.0, 2)


async def run_audit_background(job_id: str, payload: AuditJobRequest) -> None:
    """Fungsi worker latar belakang untuk mengeksekusi pipeline LangGraph dan streaming progres."""
    channel = f"audit-progress:{payload.organization_id}:{payload.contract_id}"

    # 1. Publikasikan status inisialisasi awal
    await publish_progress(
        channel,
        AuditProgressEvent(
            current_node="INITIALIZING",
            progress=5,
            status="IN_PROGRESS",
            message="Memulai proses audit kepatuhan kontrak...",
        ),
    )

    state: AuditState = {
        "contract_id": payload.contract_id,
        "organization_id": payload.organization_id,
        "s3_key": payload.s3_key,
        "raw_text": payload.raw_text or "",
        "clauses": [],
        "findings": [],
        "step_count": 0,
        "status": "INIT",
    }

    try:
        graph = build_audit_graph()
        final_state: dict[str, Any] = state

        # 2. Jalankan graph LangGraph dan streaming setiap node selesai
        async for step_output in graph.astream(state):
            for node_name, updated_data in step_output.items():
                if isinstance(updated_data, dict):
                    final_state.update(updated_data)

                stage_info = STAGE_METADATA.get(
                    node_name,
                    {
                        "progress": 90,
                        "message": f"Selesai memproses tahap {node_name}...",
                    },
                )

                await publish_progress(
                    channel,
                    AuditProgressEvent(
                        current_node=node_name,
                        progress=stage_info["progress"],
                        status="IN_PROGRESS",
                        message=stage_info["message"],
                    ),
                )

        # 3. Kompilasi hasil laporan akhir
        findings: list[ComplianceMatrixItem] = final_state.get("findings", [])
        total_clauses = len(final_state.get("clauses", []))
        score = calculate_compliance_score(findings)

        report = ComplianceAuditReport(
            contract_id=payload.contract_id,
            organization_id=payload.organization_id,
            total_clauses=total_clauses,
            compliance_score=score,
            matrix=findings,
        )

        # 4. Publikasikan status selesai dengan payload laporan lengkap
        await publish_progress(
            channel,
            AuditProgressEvent(
                current_node="legal_drafter",
                progress=100,
                status="COMPLETED",
                message="Audit kepatuhan selesai dengan sukses.",
                data=report.model_dump(),
            ),
        )

    except Exception as exc:
        logger.exception("Audit background task gagal untuk job %s: %s", job_id, exc)
        await publish_progress(
            channel,
            AuditProgressEvent(
                current_node="FAILED",
                progress=0,
                status="FAILED",
                message=f"Audit gagal diproses: {exc}",
            ),
        )

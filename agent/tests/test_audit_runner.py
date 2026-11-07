from app.graph.builder import NODE_ORDER
from app.schemas.report import AuditJobRequest, AuditProgressEvent, ComplianceMatrixItem
from app.services.audit_runner import (
    STAGE_METADATA,
    calculate_compliance_score,
)


def test_calculate_compliance_score_empty() -> None:
    assert calculate_compliance_score([]) == 100.0


def test_calculate_compliance_score_ratio() -> None:
    items = [
        ComplianceMatrixItem(
            clause_number="Pasal 1",
            topic="Umum",
            original_text="text",
            status="COMPLIANT",
            severity="CLEAN",
            legal_rationale="Patuh",
        ),
        ComplianceMatrixItem(
            clause_number="Pasal 2",
            topic="Bunga",
            original_text="text",
            status="VIOLATION",
            severity="HIGH",
            legal_rationale="Melanggar",
        ),
    ]
    assert calculate_compliance_score(items) == 50.0


def test_audit_progress_event_serialization() -> None:
    event = AuditProgressEvent(
        current_node="clause_parser",
        progress=25,
        status="IN_PROGRESS",
        message="Mengekstrak klausul...",
        data={"clauses_count": 5},
    )
    dumped = event.model_dump()
    assert dumped["current_node"] == "clause_parser"
    assert dumped["progress"] == 25
    assert dumped["status"] == "IN_PROGRESS"
    assert dumped["data"]["clauses_count"] == 5


def test_all_graph_nodes_have_stage_metadata() -> None:
    for node_name in NODE_ORDER:
        assert node_name in STAGE_METADATA
        meta = STAGE_METADATA[node_name]
        assert "progress" in meta
        assert "message" in meta
        assert 0 <= meta["progress"] <= 100


def test_audit_job_request_supports_raw_text() -> None:
    req = AuditJobRequest(
        contract_id="c-123",
        organization_id="org-456",
        s3_key="org_org-456/contracts/contract.pdf",
        raw_text="Pasal 1 Ketentuan Umum",
    )
    assert req.contract_id == "c-123"
    assert req.raw_text == "Pasal 1 Ketentuan Umum"

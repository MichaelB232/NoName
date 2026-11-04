"""LangGraph state shared by every node (ADR-0002)."""

from typing import TypedDict

from app.schemas.report import ComplianceMatrixItem


class AuditState(TypedDict):
    contract_id: str
    organization_id: str
    s3_key: str
    raw_text: str
    clauses: list[dict[str, str]]
    findings: list[ComplianceMatrixItem]
    step_count: int
    status: str

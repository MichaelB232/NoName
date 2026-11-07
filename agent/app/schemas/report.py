from typing import Literal

from pydantic import BaseModel, Field


class LegalCitation(BaseModel):
    regulator: Literal["OJK", "BI", "KOMINFO"]
    regulation_name: str = Field(description="e.g. POJK No. 10/POJK.05/2022")
    article: str = Field(description="e.g. Pasal 29 ayat (2)")
    article_quote: str = Field(description="Exact snippet from the retrieved Qdrant chunk")
    verified: bool = Field(
        description="False when no Qdrant chunk met the score threshold → UNVERIFIED_CITATION",
    )

class ComplianceMatrixItem(BaseModel):
    clause_number: str = Field(description="e.g. Pasal 5.2")
    topic: str
    original_text: str
    status: Literal["COMPLIANT", "VIOLATION", "AMBIGUOUS", "UNVERIFIED_CITATION"]
    violated_regulation: LegalCitation | None = None
    severity: Literal["HIGH", "MEDIUM", "LOW", "CLEAN"]
    penalty_estimate_idr: int = Field(default=0, ge=0, description="Computed by deterministic tools only")
    suggested_revision: str | None = None
    legal_rationale: str


class ComplianceAuditReport(BaseModel):
    contract_id: str
    organization_id: str
    total_clauses: int = Field(ge=0)
    compliance_score: float = Field(ge=0.0, le=100.0)
    matrix: list[ComplianceMatrixItem]


class AuditJobRequest(BaseModel):

    contract_id: str = Field(min_length=1)
    organization_id: str = Field(min_length=1)
    s3_key: str = Field(min_length=1, description="Must start with the tenant prefix org_<organization_id>/")


class AuditJobAccepted(BaseModel):
    job_id: str
    contract_id: str
    progress_channel: str = Field(description="Redis pub/sub channel the backend relays as SSE")

from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator


class LegalCitation(BaseModel):
    regulator: Literal["OJK", "BI", "KOMINFO"]
    regulation_name: str = Field(description="e.g. POJK No. 10/POJK.05/2022")
    article: str = Field(description="e.g. Pasal 29 ayat (2)")
    article_quote: str = Field(description="Exact snippet from the retrieved Qdrant chunk")
    verified: bool = Field(
        description="False when no Qdrant chunk met the score threshold → UNVERIFIED_CITATION",
    )


class LLMAuditResult(BaseModel):
    """Structured LLM output for single clause evaluation against retrieved statutory chunks."""

    status: Literal["COMPLIANT", "VIOLATION", "AMBIGUOUS", "UNVERIFIED_CITATION"] = Field(
        default="COMPLIANT", description="COMPLIANT, VIOLATION, AMBIGUOUS, or UNVERIFIED_CITATION"
    )
    severity: Literal["HIGH", "MEDIUM", "LOW", "CLEAN"] = Field(
        default="CLEAN", description="HIGH, MEDIUM, LOW, or CLEAN (must be CLEAN if compliant)"
    )
    topic: str | None = Field(default="Ketentuan Umum", description="Short topic of the clause")
    violated_chunk_index: int | None = Field(
        default=None, description="0-based index of the retrieved regulation chunk that is violated, or None"
    )
    legal_rationale: str = Field(
        default="Klausul telah dianalisis dan dinyatakan patuh.",
        description="Detailed explanation in formal Indonesian legal language (Bahasa Hukum Indonesia baku)",
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_llm_dict(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        # Normalize status
        raw_status = str(data.get("status") or "").strip().upper()
        if raw_status in ("COMPLIANT", "VIOLATION", "AMBIGUOUS", "UNVERIFIED_CITATION"):
            data["status"] = raw_status
        elif "VIOLAT" in raw_status:
            data["status"] = "VIOLATION"
        elif "AMBIG" in raw_status:
            data["status"] = "AMBIGUOUS"
        else:
            data["status"] = "COMPLIANT"

        # Normalize severity
        raw_severity = data.get("severity")
        if isinstance(raw_severity, str):
            sev_upper = raw_severity.strip().upper()
            if sev_upper in ("HIGH", "MEDIUM", "LOW", "CLEAN"):
                data["severity"] = sev_upper
            elif sev_upper in ("NONE", "N/A", "NULL", "ZERO", "NO", ""):
                data["severity"] = "CLEAN"
            else:
                data["severity"] = "HIGH" if data["status"] == "VIOLATION" else "CLEAN"
        else:
            if data["status"] == "VIOLATION":
                data["severity"] = "HIGH"
            elif data["status"] == "AMBIGUOUS":
                data["severity"] = "LOW"
            else:
                data["severity"] = "CLEAN"

        return data


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

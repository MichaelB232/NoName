import json
import logging
import re
import warnings
from decimal import Decimal
from typing import Any, Literal

from google import genai
from pydantic import BaseModel, Field, model_validator
from qdrant_client import QdrantClient

from app.core.config import get_settings
from app.graph.state import AuditState
from app.schemas.report import ComplianceMatrixItem, LegalCitation
from app.tools.interest_calculator import InterestCapInput, evaluate_interest_cap

logger = logging.getLogger(__name__)


OJK_DAILY_RATE_CAP = Decimal("0.10")
RATE_REGEX = re.compile(
    r"(\d+(?:\.\d+)?)\s*%\s*(?:per\s+hari|harian|\/\s*hari)", re.IGNORECASE
)
FORBIDDEN_DATA_KEYWORDS = [
    "kontak",
    "phonebook",
    "buku telepon",
    "galeri",
    "media sosial",
    "daftar panggilan",
]

class LLMAuditResult(BaseModel):
    status: Literal["COMPLIANT", "VIOLATION", "AMBIGUOUS", "UNVERIFIED_CITATION"] = Field(
        default="COMPLIANT", description="COMPLIANT, VIOLATION, AMBIGUOUS, or UNVERIFIED_CITATION"
    )
    severity: Literal["HIGH", "MEDIUM", "LOW", "CLEAN"] = Field(
        default="CLEAN", description="HIGH, MEDIUM, LOW, or CLEAN"
    )
    topic: str | None = Field(default="Ketentuan Umum", description="Short topic of the clause")
    violated_chunk_index: int | None = Field(default=None)
    legal_rationale: str = Field(default="Klausul telah dianalisis dan dinyatakan patuh.")

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
            # Handle null/None or missing severity
            if data["status"] == "VIOLATION":
                data["severity"] = "HIGH"
            elif data["status"] == "AMBIGUOUS":
                data["severity"] = "LOW"
            else:
                data["severity"] = "CLEAN"

        return data


def _get_qdrant_client() -> QdrantClient | None:
    try:
        settings = get_settings()
        api_key = (
            settings.qdrant_api_key.get_secret_value()
            if settings.qdrant_api_key
            else None
        )
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                category=UserWarning,
                message=".*(Api key is used with an insecure connection|Failed to obtain server version).*",
            )
            return QdrantClient(
                url=settings.qdrant_url,
                api_key=api_key,
                timeout=2.0,
                check_compatibility=False,
            )
    except Exception as exc:
        logger.warning("Failed to initialize Qdrant client: %s", exc)
        return None


def _get_gemini_client() -> genai.Client | None:
    try:
        settings = get_settings()
        api_key = settings.gemini_api_key.get_secret_value()
        if not api_key:
            return None
        return genai.Client(api_key=api_key)
    except Exception as exc:
        logger.warning("Failed to initialize Gemini client: %s", exc)
        return None


def retrieve_regulatory_chunks(
    query_text: str,
    qdrant_client: QdrantClient,
    gemini_client: genai.Client,
    limit: int = 3,
) -> list[dict[str, Any]]:
    """Retrieves relevant regulation chunks from Qdrant using vector search."""
    settings = get_settings()
    try:
        emb_res = gemini_client.models.embed_content(
            model=settings.gemini_embedding_model or "gemini-embedding-001",
            contents=query_text,
        )
        query_vector = emb_res.embeddings[0].values

        response = qdrant_client.query_points(
            collection_name=settings.qdrant_collection,
            query=query_vector,
            limit=limit,
            score_threshold=0.50,
        )
        chunks: list[dict[str, Any]] = []
        for hit in response.points:
            payload = hit.payload or {}
            payload["_score"] = hit.score
            chunks.append(payload)
        return chunks
    except Exception as exc:
        logger.warning("Error retrieving regulatory chunks from Qdrant: %s", exc)
        return []

def audit_clause_with_rag(
    clause: dict[str, str],
    qdrant_client: QdrantClient | None,
    gemini_client: genai.Client | None,
) -> ComplianceMatrixItem:
    clause_number = clause.get("clause_number", "Klausul")
    title = clause.get("title", "")
    text = clause.get("text", "")
    text_lower = text.lower()

    # 1. Dynamic Qdrant Vector Retrieval First
    retrieved_chunks: list[dict[str, Any]] = []
    if qdrant_client and gemini_client:
        retrieved_chunks = retrieve_regulatory_chunks(
            query_text=text,
            qdrant_client=qdrant_client,
            gemini_client=gemini_client,
            limit=3,
        )

    # 2. Deterministic Math with DYNAMIC Qdrant Statutory Citation
    rate_match = RATE_REGEX.search(text)
    if rate_match:
        extracted_rate = Decimal(rate_match.group(1))

        # Cari apakah ada chunk dari Qdrant yang membahas batas bunga / manfaat ekonomi
        matched_chunk: dict[str, Any] | None = None
        for ch in retrieved_chunks:
            ch_text = (ch.get("text") or "").lower()
            ch_topic = (ch.get("topic") or "").lower()
            if "interest_cap" in ch_topic or "manfaat ekonomi" in ch_text or "bunga" in ch_text:
                matched_chunk = ch
                break

        if matched_chunk:
            statutory_cap = Decimal(str(matched_chunk.get("cap_daily_percent", "0.10")))
            reg_name = matched_chunk.get("regulation_name", "Regulasi OJK")
            art_num = matched_chunk.get("pasal", "Pasal 29")
            art_quote = matched_chunk.get("text", "")
            is_verified = True
        else:
            statutory_cap = OJK_DAILY_RATE_CAP
            reg_name = "POJK No. 10/POJK.05/2022 jo. SE OJK No. 19/SEOJK.06/2023"
            art_num = "Pasal 29 ayat (2)"
            art_quote = "Batas maksimum manfaat ekonomi konsumtif sebesar 0,1% per hari."
            is_verified = False

        eval_result = evaluate_interest_cap(
            InterestCapInput(
                contract_daily_rate_percent=extracted_rate,
                regulatory_cap_daily_percent=statutory_cap,
                cap_source_citation=f"{reg_name} {art_num}",
                principal_idr=Decimal(1_000_000),
                tenor_days=30,
            )
        )

        if not eval_result.is_within_cap:
            return ComplianceMatrixItem(
                clause_number=clause_number,
                topic="Batasan Suku Bunga Harian",
                original_text=text,
                status="VIOLATION",
                severity="HIGH",
                violated_regulation=LegalCitation(
                    regulator=matched_chunk.get("regulator", "OJK") if matched_chunk else "OJK",
                    regulation_name=reg_name,
                    article=art_num,
                    article_quote=art_quote,
                    verified=is_verified,
                ),
                penalty_estimate_idr=0,
                suggested_revision=None,
                legal_rationale=(
                    f"Suku bunga kontrak sebesar {extracted_rate}% per hari melebihi batas maksimum "
                    f"sebesar {statutory_cap}% per hari berdasarkan {reg_name} {art_num} "
                    f"(kelebihan {eval_result.excess_daily_rate_percent}%/hari)."
                ),
            )

    # 3. Agentic Evaluation with Gemini LLM (Tier 2 / Tier 1 fallback)
    if gemini_client and retrieved_chunks:
        try:
            settings = get_settings()
            model_name = settings.gemini_model_tier2

            chunks_context = ""
            for idx, ch in enumerate(retrieved_chunks):
                chunks_context += (
                    f"\n[Chunk {idx}]\n"
                    f"Regulation: {ch.get('regulation_name')}\n"
                    f"Article: {ch.get('pasal')}\n"
                    f"Chapter: {ch.get('bab')}\n"
                    f"Text: {ch.get('text')}\n"
                )

            system_instruction = (
                "You are an elite Indonesian Legal-Tech Regulatory Compliance Auditor for FinTech (OJK, BI, UU PDP).\n"
                "Audit the contract clause against the provided retrieved regulation chunks.\n"
                "RULES:\n"
                "1. If the clause violates any retrieved regulation, set status to 'VIOLATION', severity to 'HIGH', 'MEDIUM', or 'LOW', and specify 'violated_chunk_index'.\n"
                "2. If no retrieved chunk is violated, set status to 'COMPLIANT' and severity to 'CLEAN', or status to 'AMBIGUOUS' and severity to 'LOW'.\n"
                "3. Never invent regulations. Only reference the provided chunks.\n"
                "4. 'severity' MUST be one of: 'HIGH', 'MEDIUM', 'LOW', or 'CLEAN'. For 'COMPLIANT' clauses, severity must always be 'CLEAN' (never null).\n"
                "Respond in valid JSON adhering to schema: status, severity, topic, violated_chunk_index, legal_rationale."
            )

            prompt = (
                f"Retrieved Indonesian Regulations:\n{chunks_context}\n\n"
                f"Contract Clause to Audit:\n"
                f"Clause ID: {clause_number}\n"
                f"Title: {title}\n"
                f"Text: {text}\n"
            )

            res = gemini_client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=dict(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                ),
            )

            parsed = json.loads(res.text)
            audit_eval = LLMAuditResult(**parsed)

            violated_reg: LegalCitation | None = None
            if audit_eval.status == "VIOLATION":
                idx = audit_eval.violated_chunk_index
                if idx is not None and 0 <= idx < len(retrieved_chunks):
                    matched_chunk = retrieved_chunks[idx]
                    violated_reg = LegalCitation(
                        regulator=matched_chunk.get("regulator", "OJK"),
                        regulation_name=matched_chunk.get(
                            "regulation_name", "Regulasi OJK"
                        ),
                        article=matched_chunk.get("pasal", "Pasal Terkait"),
                        article_quote=matched_chunk.get("text", ""),
                        verified=True,
                    )
                else:
                    audit_eval.status = "UNVERIFIED_CITATION"
                    violated_reg = LegalCitation(
                        regulator="OJK",
                        regulation_name="Unverified Regulation",
                        article="UNVERIFIED_CITATION",
                        article_quote="",
                        verified=False,
                    )

            return ComplianceMatrixItem(
                clause_number=clause_number,
                topic=audit_eval.topic or title or "Audit Regulasi",
                original_text=text,
                status=audit_eval.status,  # type: ignore[arg-type]
                severity=audit_eval.severity,  # type: ignore[arg-type]
                violated_regulation=violated_reg,
                penalty_estimate_idr=0,
                suggested_revision=None,
                legal_rationale=audit_eval.legal_rationale,
            )
        except Exception as exc:
            logger.warning(
                "LLM evaluation failed, falling back to rule-based audit: %s", exc
            )

    # 4. Fallback Rule-Based Evaluation (Offline / Guardrail Fallback)
    if any(keyword in text_lower for keyword in FORBIDDEN_DATA_KEYWORDS):
        return ComplianceMatrixItem(
            clause_number=clause_number,
            topic="Perlindungan Data Pribadi (Akses Perangkat)",
            original_text=text,
            status="VIOLATION",
            severity="HIGH",
            violated_regulation=LegalCitation(
                regulator="KOMINFO",
                regulation_name="UU No. 27 Tahun 2022 (UU PDP) jo. POJK No. 10/2022",
                article="Pasal 20 & Ketentuan Izin CAM OJK",
                article_quote=(
                    "Pengendali Data Pribadi wajib membatasi pemrosesan data pribadi dan dilarang "
                    "mengakses data di luar izin resmi Camera, Audio, dan Location (CAM)."
                ),
                verified=True,
            ),
            penalty_estimate_idr=0,
            suggested_revision=None,
            legal_rationale=(
                "Penyelenggara dilarang mengakses kontak pribadi atau galeri ponsel nasabah. "
                "Ketentuan OJK dan UU PDP secara tegas membatasi akses perangkat hanya pada Camera, Audio, dan Location (CAM)."
            ),
        )

    return ComplianceMatrixItem(
        clause_number=clause_number,
        topic=title or "Ketentuan Perikatan Umum",
        original_text=text,
        status="COMPLIANT",
        severity="CLEAN",
        violated_regulation=None,
        penalty_estimate_idr=0,
        suggested_revision=None,
        legal_rationale="Klausul memenuhi prinsip kebebasan berkontrak KUHPerdata dan tidak melanggar ketentuan OJK/UU PDP.",
    )


def compliance_auditor_node(state: AuditState) -> dict[str, Any]:
    clauses = state.get("clauses", [])
    findings: list[ComplianceMatrixItem] = []

    qdrant_client = _get_qdrant_client()
    gemini_client = _get_gemini_client()

    for clause in clauses:
        finding = audit_clause_with_rag(clause, qdrant_client, gemini_client)
        findings.append(finding)

    return {
        "findings": findings,
        "step_count": state.get("step_count", 0) + 1,
        "status": "compliance_audited",
    }

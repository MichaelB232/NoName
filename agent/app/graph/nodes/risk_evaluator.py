from decimal import Decimal
import re
from typing import Any

from app.graph.state import AuditState
from app.schemas.report import ComplianceMatrixItem
from app.tools.interest_calculator import InterestCapInput, evaluate_interest_cap

OJK_DAILY_RATE_CAP = Decimal("0.10")
UU_PDP_STATUTORY_MAX_FINE = 5_000_000_000  # Maksimal Rp 5 Miliar (Pasal 67 UU PDP)
RATE_REGEX = re.compile(
    r"(\d+(?:\.\d+)?)\s*%\s*(?:per\s+hari|harian|\/\s*hari)", re.IGNORECASE
)


def calculate_clause_risk(item: ComplianceMatrixItem) -> int:
    if item.status != "VIOLATION":
        return 0

    text = item.original_text
    topic_lower = item.topic.lower()
    rate_match = RATE_REGEX.search(text)
    if rate_match or "bunga" in topic_lower or "interest" in topic_lower:
        extracted_rate = Decimal(rate_match.group(1)) if rate_match else Decimal("0.45")
        calc_result = evaluate_interest_cap(
            InterestCapInput(
                contract_daily_rate_percent=extracted_rate,
                regulatory_cap_daily_percent=OJK_DAILY_RATE_CAP,
                cap_source_citation="SE OJK No. 19/SEOJK.06/2023",
                principal_idr=Decimal(1_000_000),
                tenor_days=30,
            )
        )
        return int(calc_result.excess_interest_idr)

    if any(k in topic_lower or k in text.lower() for k in ("data pribadi", "kontak", "galeri", "pdp", "kominfo")):
        return UU_PDP_STATUTORY_MAX_FINE

    return 0


def risk_evaluator_node(state: AuditState) -> dict[str, Any]:
    findings = state.get("findings", [])
    updated_findings: list[ComplianceMatrixItem] = []

    for item in findings:
        if item.status == "VIOLATION" and item.penalty_estimate_idr == 0:
            item.penalty_estimate_idr = calculate_clause_risk(item)
        updated_findings.append(item)

    return {
        "findings": updated_findings,
        "step_count": state.get("step_count", 0) + 1,
        "status": "risk_evaluated",
    }

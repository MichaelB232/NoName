import re
from typing import Any
from app.graph.state import AuditState

CLAUSE_PATTERN = re.compile(
    r"(?P<clause_id>(?:Pasal|PASAL|Klausul|Article)\s+[\d\.]+)(?:\s*[:\-\—]?\s*)(?P<title>[^\n\r]*)"
)
def parser_clauses_from_text(raw_text: str) -> list[dict[str, str]]:
    matches = list(CLAUSE_PATTERN.finditer(raw_text))

    if not matches:
        return [
            {
                "clause_number": "General",
                "title": "General Terms",
                "text": raw_text.strip(),
            }
        ]

    clauses: list[dict[str, str]] = []
    for i, match in enumerate(matches):
        clause_id = match.group("clause_id").strip()
        title = match.group("title").strip() or "Ketentuan"

        start_idx = match.end()
        end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(raw_text)
        clause_body = raw_text[start_idx:end_idx].strip()

        full_text = (
            f"{clause_id} {title}: {clause_body}".strip()
            if title
            else f"{clause_id}: {clause_body}".strip()
        )

        clauses.append({"clause_number": clause_id, "title": title, "text": full_text})
    return clauses


def clause_parser_node(state: AuditState) -> dict[str, Any]:
    raw_text = state.get("raw_text", "")
    extracted_clauses = parser_clauses_from_text(raw_text)
    return {
        "clauses": extracted_clauses,
        "step_count": state.get("step_count", 0) + 1,
        "status": "clauses_parsed",
    }


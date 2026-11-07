import json
import logging
import re
from typing import Any

from app.core.clients import get_gemini_client
from app.core.config import get_settings
from app.graph.state import AuditState

logger = logging.getLogger(__name__)

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


def parse_clauses_with_gemini(raw_text: str) -> list[dict[str, str]] | None:
    gemini_client = get_gemini_client()
    if not gemini_client:
        return None

    try:
        settings = get_settings()
        model_name = settings.gemini_model_tier1

        system_instruction = (
            "You are an expert legal document parser for Indonesian and commercial contracts.\n"
            "Segment the provided raw contract into discrete, numbered clauses or articles.\n"
            "Format: Return a JSON array of objects with keys:\n"
            "- 'clause_number': e.g. 'Pasal 1', 'Pasal 7.1', 'Article 2'\n"
            "- 'title': short title of the clause\n"
            "- 'text': verbatim full text of that clause\n"
            "Do not omit any clauses."
        )

        prompt = f"Contract Text to Segment:\n{raw_text}"

        res = gemini_client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=dict(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.0,
            ),
        )

        parsed = json.loads(res.text)
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed
        if isinstance(parsed, dict) and "clauses" in parsed:
            return parsed["clauses"]
    except Exception as exc:
        logger.warning("Tier-1 Flash clause parsing failed, falling back to regex: %s", exc)

    return None


def clause_parser_node(state: AuditState) -> dict[str, Any]:
    raw_text = state.get("raw_text", "")
    clauses = parse_clauses_with_gemini(raw_text)
    if not clauses:
        clauses = parser_clauses_from_text(raw_text)

    return {
        "clauses": clauses,
        "step_count": state.get("step_count", 0) + 1,
        "status": "clauses_parsed",
    }

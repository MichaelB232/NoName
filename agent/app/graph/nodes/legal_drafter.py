from typing import Any

from app.core.clients import get_gemini_client
from app.core.config import get_settings
from app.graph.state import AuditState
from app.schemas.report import ComplianceMatrixItem

FALLBACK_INTEREST = (
    "Suku bunga pinjaman disepakati sebesar 0,1% per hari kalender dari sisa pokok pinjaman, "
    "dengan ketentuan total seluruh manfaat ekonomi tidak melebihi 100% dari pokok pinjaman "
    "sesuai POJK No. 10/POJK.05/2022 dan SE OJK No. 19/SEOJK.06/2023."
)
FALLBACK_PDP = (
    "Pemberi Layanan hanya memproses data pribadi Peminjam dengan persetujuan tegas. "
    "Akses perangkat dibatasi hanya pada fitur Camera, Audio, dan Location (CAM) sesuai UU PDP No. 27/2022."
)


def draft_clause_with_ai(finding: ComplianceMatrixItem) -> str:
    gemini_client = get_gemini_client()
    if not gemini_client:
        return FALLBACK_INTEREST if "Suku Bunga" in finding.topic else FALLBACK_PDP

    settings = get_settings()
    model_name = settings.gemini_model_tier2 or settings.gemini_model_tier1

    try:
        system_instruction = (
            "Anda adalah Senior Legal Counsel Indonesia spesialis Hukum Perbankan dan FinTech.\n"
            "Tugas Anda: Menulis ulang (redraft) klausul kontrak yang melanggar agar 100% PATUH pada regulasi terkait.\n"
            "ATURAN MUTLAK:\n"
            "1. Pertahankan gaya bahasa, struktur kalimat, dan istilah para pihak dari klausul aslinya.\n"
            "2. Sesuaikan substansi yang melanggar dengan ketentuan undang-undang yang dilanggar.\n"
            "3. Keluarkan HANYA teks klausul hasil revisi final dalam Bahasa Indonesia hukum baku tanpa kalimat pengantar atau basa-basi."
        )

        reg_info = ""
        if finding.violated_regulation:
            reg_info = (
                f"Regulasi yang Dilanggar: {finding.violated_regulation.regulation_name} "
                f"({finding.violated_regulation.article})\n"
                f'Rujukan Bunyi Aturan: "{finding.violated_regulation.article_quote}"\n'
            )

        prompt = (
            f'Klausul Asli Kontrak:\n"{finding.original_text}"\n\n'
            f"{reg_info}"
            f"Catatan Pelanggaran: {finding.legal_rationale}\n\n"
            f"Tuliskan draf klausul perbaikan yang patuh:"
        )

        response = gemini_client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=dict(
                system_instruction=system_instruction,
                temperature=0.2,
            ),
        )

        redrafted_text = response.text.strip().strip('"')
        return redrafted_text

    except Exception as e:
        print(f"⚠️ Drafter LLM fallback: {e}")
        return FALLBACK_INTEREST if "Suku Bunga" in finding.topic else FALLBACK_PDP


def legal_drafter_node(state: AuditState) -> dict[str, Any]:
    findings = state.get("findings", [])
    updated_findings: list[ComplianceMatrixItem] = []

    for item in findings:
        if item.status == "VIOLATION":
            item.suggested_revision = draft_clause_with_ai(item)
        updated_findings.append(item)

    return {
        "findings": updated_findings,
        "step_count": state.get("step_count", 0) + 1,
        "status": "legal_drafter",
    }

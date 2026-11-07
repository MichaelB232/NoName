import re
from typing import Any
from pydantic import BaseModel, Field

BAB_REGEX = re.compile(r"^(BAB\s+[IVXLCDM]+)\s*\n?([^\n\r]*)", re.MULTILINE)

PASAL_REGEX = re.compile(r"^Pasal\s+(\d+)", re.MULTILINE)


class LegalChunk(BaseModel):
    chunk_id: str
    regulation_name: str
    bab: str = Field(
        description="Nomor dan Judul BAB, e.g. 'BAB V PENYELENGGARAAN PENDANAAN'"
    )
    pasal: str = Field(description="Nomor Pasal, e.g. 'Pasal 29'")
    header_context: str = Field(
        description="Context prefix yang disematkan ke embedding"
    )
    body_text: str = Field(
        description="Bunyi lengkap ayat dan huruf dalam pasal tersebut"
    )
    full_embed_text: str = Field(
        description="Teks lengkap siap embedding (Header + Body)"
    )


def chunk_indonesian_regulation(
    raw_text: str, regulation_name: str
) -> list[LegalChunk]:
    chunks: list[LegalChunk] = []

    bab_matches = list(BAB_REGEX.finditer(raw_text))

    def get_current_bab(pos: int) -> str:
        current_bab = "KETENTUAN UMUM"
        for bm in bab_matches:
            if bm.start() <= pos:
                bab_num = bm.group(1).strip()
                bab_title = bm.group(2).strip()
                current_bab = f"{bab_num} {bab_title}".strip()
            else:
                break
        return current_bab

    pasal_matches = list(PASAL_REGEX.finditer(raw_text))

    if not pasal_matches:
        return [
            LegalChunk(
                chunk_id=f"{regulation_name}-full",
                regulation_name=regulation_name,
                bab="UMUM",
                pasal="Umum",
                header_context=f"[{regulation_name}]",
                body_text=raw_text.strip(),
                full_embed_text=f"[{regulation_name}]\n{raw_text.strip()}",
            )
        ]
    for i, match in enumerate(pasal_matches):
        pasal_num = f"Pasal {match.group(1)}"
        start_idx = match.start()
        end_idx = (
            pasal_matches[i + 1].start()
            if i + 1 < len(pasal_matches)
            else len(raw_text)
        )

        pasal_raw_body = raw_text[start_idx:end_idx].strip()

        body_cleaned = re.sub(r"^Pasal\s+\d+\s*\n*", "", pasal_raw_body).strip()

        parent_bab = get_current_bab(start_idx)

        header_context = f"[{regulation_name} | {parent_bab} | {pasal_num}]"
        full_embed_text = f"{header_context}\n{body_cleaned}"

        chunk = LegalChunk(
            chunk_id=f"{regulation_name}-{pasal_num}".replace(" ", "_"),
            regulation_name=regulation_name,
            bab=parent_bab,
            pasal=pasal_num,
            header_context=header_context,
            body_text=body_cleaned,
            full_embed_text=full_embed_text,
        )
        chunks.append(chunk)
    return chunks

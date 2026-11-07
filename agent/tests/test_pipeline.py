import sys
from pathlib import Path

# Daftarkan folder 'agent' ke sys.path
agent_dir = Path(__file__).resolve().parent.parent
if str(agent_dir) not in sys.path:
    sys.path.insert(0, str(agent_dir))

from app.graph.nodes.clause_parser import clause_parser_node
from app.graph.nodes.compliance_auditor import compliance_auditor_node
from app.graph.nodes.risk_evaluator import risk_evaluator_node
from app.graph.nodes.legal_drafter import legal_drafter_node

SAMPLE_CONTRACT = """
Pasal 1 Ketentuan Umum
Peminjam adalah Warga Negara Indonesia yang cakap secara hukum.

Pasal 7.1 Suku Bunga Pinjaman
Peminjam sepakat dikenakan suku bunga pinjaman sebesar 0.45% per hari kalender dari total pokok pinjaman.

Pasal 12 Akses Data Pribadi
Penyelenggara berhak mengakses seluruh kontak telepon nasabah dan galeri media sosial untuk keperluan penagihan.
"""


def main():
    print("=== MEMULAI AUDIT MULTI-AGENT COMPLIANCE (100% DINAMIS) ===")

    # 1. Node 1: Parser (Gemini Flash)
    state = {"raw_text": SAMPLE_CONTRACT, "step_count": 0}
    parse_res = clause_parser_node(state)
    state.update(parse_res)
    print(f"\n[Node 1: Clause Parser] Berhasil mengekstrak {len(state['clauses'])} pasal:")
    for c in state["clauses"]:
        print(f"  - {c.get('clause_number', 'Pasal')}: {c.get('title', '')}")

    # 2. Node 2: Auditor (Qdrant Vector RAG + Gemini Pro/Flash)
    audit_res = compliance_auditor_node(state)
    state.update(audit_res)
    print(f"\n[Node 2: Compliance Auditor] Hasil Evaluasi Regulasi:")
    for f in state["findings"]:
        print(f"  - {f.clause_number}: [{f.status}] {f.topic}")

    # 3. Node 3: Risk Evaluator (Deterministic Math Tool)
    risk_res = risk_evaluator_node(state)
    state.update(risk_res)
    print(f"\n[Node 3: Risk Evaluator] Perhitungan Risiko Finansial:")
    for f in state["findings"]:
        print(f"  - {f.clause_number}: Estimasi Risiko = Rp {f.penalty_estimate_idr:,}")

    # 4. Node 4: Legal Drafter (Gemini Pro/Flash Dynamic Redrafting)
    draft_res = legal_drafter_node(state)
    state.update(draft_res)
    print(f"\n[Node 4: Legal Drafter] Usulan Revisi Klausul (AI Git-Style Redline):")
    for f in state["findings"]:
        if f.status == "VIOLATION":
            print(f"\n>>> Pelanggaran di {f.clause_number} ({f.topic}):")
            print(f"    [MERAH - Teks Asli Melanggar]:\n    {f.original_text}")
            print(f"    [HIJAU - Draf Usulan Patuh (AI Generated)]:\n    {f.suggested_revision}")
            if f.violated_regulation:
                print(
                    f"    [Dasar Hukum]:\n    {f.violated_regulation.regulation_name} - {f.violated_regulation.article}"
                )

    print("\n=== SELURUH PIPELINE SELESAI DENGAN SUKSES! ===")


if __name__ == "__main__":
    main()

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.graph.nodes.clause_parser import parser_clauses_from_text
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
    print("=== MEMULAI AUDIT MULTI-AGENT COMPLIANCE ===")

    # 1. Node 1: Parser
    clauses = parser_clauses_from_text(SAMPLE_CONTRACT)
    print(f"\n[Node 1: Clause Parser] Berhasil mengekstrak {len(clauses)} pasal:")
    for c in clauses:
        print(f"  - {c['clause_number']}: {c['title']}")

    # 2. Node 2: Auditor
    audit_res = compliance_auditor_node({"clauses": clauses, "step_count": 1})
    print(f"\n[Node 2: Compliance Auditor] Hasil Evaluasi Regulasi:")
    for f in audit_res["findings"]:
        print(f"  - {f.clause_number}: [{f.status}] {f.topic}")

    # 3. Node 3: Risk Evaluator
    risk_res = risk_evaluator_node(audit_res)
    print(f"\n[Node 3: Risk Evaluator] Perhitungan Risiko Finansial:")
    for f in risk_res["findings"]:
        print(f"  - {f.clause_number}: Estimasi Risiko = Rp {f.penalty_estimate_idr:,}")

    # 4. Node 4: Legal Drafter
    draft_res = legal_drafter_node(risk_res)
    print(f"\n[Node 4: Legal Drafter] Usulan Revisi Klausul (Git-Style Redline):")
    for f in draft_res["findings"]:
        if f.status == "VIOLATION":
            print(f"\n>>> Pelanggaran di {f.clause_number} ({f.topic}):")
            print(f"    [MERAH - Teks Asli Melanggar]:\n    {f.original_text}")
            print(f"    [HIJAU - Draf Usulan Patuh]:\n    {f.suggested_revision}")
            print(
                f"    [Dasar Hukum]:\n    {f.violated_regulation.regulation_name} - {f.violated_regulation.article}"
            )

    print("\n=== SELURUH PIPELINE SELESAI DENGAN SUKSES! ===")


if __name__ == "__main__":
    main()

# PRD-0001: Autonomous FinTech Contract Compliance Copilot

| Metadata | Details |
| :--- | :--- |
| **Product Name** | Compliance-Agent (Codename) |
| **Document Version** | 1.0.0 |
| **Status** | Approved / Ready for Implementation |
| **Target Launch** | Phase 1 MVP |
| **Key Stakeholders** | In-House Legal Counsel, Compliance Officers, FinTech Product Managers |

---

## 1. Problem Definition & Market Opportunity

Indonesian financial technology (FinTech) platforms, peer-to-peer (P2P) lending providers, and digital banks face stringent and evolving regulatory oversight from:
- **OJK (Otoritas Jasa Keuangan):** Strict interest rate ceilings (e.g., POJK 10/2022 and SEOJK 19/2023), late payment penalty caps, debt collection ethics, and consumer rights.
- **UU No. 27 Tahun 2022 (UU PDP):** Heavy criminal and administrative penalties for unlawful data processing, device permission abuse (only Camera, Audio, Location / CAM allowed).
- **Bank Indonesia (BI):** Payment processing and AML/APU-PPT rules.

Current manual legal reviews of 50–100+ page credit and loan agreements take days or weeks, delay product launches, and risk multi-billion IDR fines or license revocation due to human oversight.

---

## 2. Product Vision & Goals

**Vision**: Provide an autonomous, zero-hallucination contract compliance copilot inspired by modern legal canvases (like Harvey AI) with automated auditing, quantitative risk calculation, and one-click Git-style redrafting.

### 2.1 Measurable Goals (KPIs)
- **Review Speed**: Reduce contract audit turnaround from ~3 days to < 2 minutes.
- **Hallucination Rate**: 0% hallucinated regulatory citations (verified against indexed government gazettes).
- **Audit Coverage**: 100% clause parsing completeness for standard Indonesian loan and credit agreements.

---

## 3. User Personas & Core Journeys

### Persona A: Retno (Senior Compliance Officer at P2P Lending)
- **Goal**: Ensure new borrower loan terms strictly conform to OJK interest caps and late fee ceilings.
- **Pain Point**: Spends hours manually calculating tiered daily interest rates and checking clauses against multiple POJK circular letters.

### Persona B: Budi (FinTech Product Manager)
- **Goal**: Rapidly launch a digital BNPL feature without failing internal compliance review.
- **Pain Point**: Receives vague legal rejection notes without actionable clause revisions.

---

## 4. Key Functional Features (MVP Scope)

### 4.1 Document Ingestion & Clause Parsing
- Supports PDF and DOCX contract uploads.
- Autonomous parsing using PyMuPDF and Gemini Flash to chunk text into structured, numbered clauses with metadata (Clause Title, Number, Paragraphs).

### 4.2 Regulatory Knowledge Indexing (Agentic RAG)
- Pre-indexed Qdrant vector collection of Indonesian regulatory frameworks:
  - POJK No. 10/POJK.05/2022 & SEOJK No. 19/SEOJK.06/2023 (FinTech P2P Lending).
  - UU No. 27 Tahun 2022 (UU Pelindungan Data Pribadi).
- Hybrid search (Dense Embeddings + Sparse BM25) with payload filtering.

### 4.3 Deterministic Risk & Penalty Quantification
- When an agent flags interest rates exceeding OJK ceilings (e.g., > 0.3% or 0.1% per day), a deterministic Python math calculator computes:
  - Daily rate variance.
  - Potential regulatory administrative fine tier.
- Eliminates numerical hallucinations by LLMs.

### 4.4 Automated Clause Redrafting (Git-Style Diff)
- Generates legally compliant clause alternatives while preserving original commercial intent.
- Outputs structured diffs (Original $\rightarrow$ Strikethrough Red, Suggested Revision $\rightarrow$ Green).

### 4.5 Split-Screen Collaborative Canvas
- **Left (60%)**: Interactive document reader (Tiptap) with inline highlighting and audit status markers.
- **Right (40%)**: Compliance Matrix & Executive Summary.
- **Bi-directional Navigation**: Clicking an issue on the matrix scrolls the editor directly to the offending clause with a visual alert.

---

## 5. Non-Functional Requirements

- **Security & Multi-Tenancy**: Complete data isolation via `organization_id` on all database records, vector points, and S3 paths.
- **Latency**: Streaming responses via Server-Sent Events (SSE) so users see agent thoughts and findings progressively within 2–5 seconds of ingestion.
- **Audit Trail & Observability**: Every agent decision step (Thought $\rightarrow$ Action $\rightarrow$ Observation) logged to Langfuse.
- **Compliance & Privacy**: Temporary processing files deleted after indexing; client documents encrypted at rest (AES-256) and in transit (TLS 1.3).

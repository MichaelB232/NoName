# ADR-0004: Service Separation Pattern (Backend API Gateway vs Autonomous AI Agent Core)

| Metadata | Details |
| :--- | :--- |
| **Status** | Accepted |
| **Date** | 2026-11-04 |
| **Deciders** | Architecture & AI Engineering Team |
| **Consulted** | FinTech Regulatory & Security Guild |

---

## 1. Konteks & Pertanyaan Desain: "Apakah Agent Harus Dipisah atau Digabung?"

Dalam membangun platform **Compliance-Agent**, muncul pertanyaan arsitektural krusial:
> *Apakah Multi-Agent pipeline (LangGraph + Gemini + PyMuPDF) sebaiknya disatukan ke dalam satu monolit backend yang sama dengan API aplikasi, atau dipisah menjadi microservice / subsystem tersendiri?*

Ada dua pendekatan yang dipertimbangkan:
1. **Pilihan A (All-in-One Monolith Python):** FastAPI menangani API autentikasi, database PostgreSQL, CRUD kontrak, sekaligus menjalankan LangGraph agent secara langsung dalam satu process runtime.
2. **Pilihan B (Separated Service / Polyglot Multi-Service):**
   - **`backend/` (TypeScript / Express.js / Node.js 20+):** Bertindak sebagai API Gateway, menangani session cookie, autentikasi multi-tenant, CRUD transaksi, pembuatan Presigned URL S3/MinIO, dan relay SSE.
   - **`agent/` (Python 3.11+ / FastAPI / LangGraph):** Berjalan sebagai sub-service internal (private network) khusus komputasi AI, vector retrieval Qdrant, deterministic math execution, dan LangGraph state machine.
   - **`frontend/` (Next.js 15 / React 19 / TypeScript):** UI workspace split-screen, Tiptap canvas, dan client viewer.

---

## 2. Keputusan Arsitektural (Decision)

Kami memutuskan untuk **MEMISAHKAN AGENT SEBAGAI SUB-SERVICE TERSENDIRI (`agent/`)** yang terisolasi dari API Gateway (`backend/`).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js 15)                           │
│     Split-Canvas Tiptap • Audit Matrix • Bi-directional Navigation     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS + httpOnly Cookie
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   BACKEND API GATEWAY (Express / TS)                   │
│   • Multi-Tenant Isolation (organization_id)                           │
│   • RBAC Guard & Session Management (JWT in httpOnly Cookie)           │
│   • S3/MinIO Presigned URL Issuance (Max 25MB, 600s TTL)               │
│   • Drizzle ORM (PostgreSQL ACID Transactions)                         │
│   • Rate Limiting & Audit Trail Event Logger                           │
└───────────────────────┬──────────────────────────┬─────────────────────┘
                        │ Service-to-Service       │ Pub/Sub
                        │ (Bearer Secret Token)    │ Progress Channel
                        ▼                          ▼
┌──────────────────────────────────────┐     ┌───────────────────────────┐
│     AI AGENT SERVICE (Python 3.11)   │     │          REDIS            │
│  • LangGraph Stateful Workflow Graph │     │  • SSE Real-Time Channel  │
│  • Two-Tier Gemini Routing (Flash/Pro│     │  • Ephemeral Cache        │
│  • Qdrant Hybrid RAG Retrieval       │     └───────────────────────────┘
│  • PyMuPDF Clause Structurer         │                   ▲
│  • Deterministic Math Calculators    │───────────────────┘
└──────────────────────────────────────┘
```

---

## 3. Rationale & Alasan di Balik Pemisahan Service

1. **Ecosystem & Library Affinity:**
   - AI, RAG, dan pemrosesan PDF di industri modern didominasi oleh pustaka native Python (`langgraph`, `google-genai`, `pymupdf` / `fitz`, `qdrant-client`). Memaksakan AI pipeline di Node.js sering kali terkendala minimnya dukungan bindings native untuk dokumen legal.
   - Di sisi lain, ekosistem web backend (Drizzle ORM, Zod, Express/Next.js) memberikan *end-to-end type safety* yang sangat kuat bersama TypeScript di frontend.
2. **Resource Allocation & Independent Autoscaling (CPU vs I/O Bound):**
   - **Backend API Gateway** bersifat *I/O bound* (ringan, melayani ribuan request per detik untuk metadata, session, dan static routes).
   - **AI Agent Service** bersifat *compute & memory bound* (membutuhkan streaming I/O berat, parsing dokumen 100+ halaman, embedding vector, dan menunggu inferensi LLM 2–5 detik).
   - Dengan pemisahan ini, `agent/` dapat di-scale secara horizontal (misal: 10 worker pods) saat lonjakan audit dokumen terjadi tanpa membebani respon API login atau dashboard.
3. **Security Boundary & Zero-Trust Internal Network:**
   - Layanan `agent/` **TIDAK TERBUKA KE INTERNET PUBLIK**. Hanya backend yang dapat memanggilnya via internal network menggunakan `AGENT_SERVICE_TOKEN` berotasi (constant-time token comparison).
   - Kredensial sensitif LLM (`GEMINI_API_KEY`, `LANGFUSE_SECRET_KEY`) hanya berada di dalam container `agent/`, tidak pernah terekspos ke layer API publik atau frontend browser.
4. **Independent Testing & Fast Developer Feedback:**
   - Seperti yang sudah kita bahas sebelumnya: AI/RAG Engineer dapat menguji dan mengotak-atik agent secara *headless* (via CLI / Swagger UI `agent/docs` / Pytest) tanpa memerlukan frontend atau database web yang sedang dikembangkan oleh tim lain.

---

## 4. Pola Komunikasi Antar-Layanan (Inter-Service Contract)

1. **Job Dispatch (Backend $\rightarrow$ Agent):**
   - Backend memanggil `POST /v1/audits` pada layanan agent membawa payload `{ contract_id, organization_id, s3_key }`.
   - Agent memverifikasi `s3_key` diawali prefix `org_<organization_id>/` (Hard Multi-Tenancy Boundary).
   - Agent mengembalikan `HTTP 202 Accepted` beserta ID channel Redis Pub/Sub: `audit-progress:<orgId>:<contractId>`.
2. **Progress Relay (Agent $\rightarrow$ Redis $\rightarrow$ Backend $\rightarrow$ Frontend):**
   - Selama LangGraph mengeksekusi tahapan node, agent mem-publish event ke Redis.
   - Backend me-relay stream ini ke browser via endpoint Server-Sent Events (SSE) `GET /api/v1/contracts/:id/stream`.
3. **Result Persistence:**
   - Setelah LangGraph mencapai `END`, agent mengembalikan structured `ComplianceAuditReport` (Pydantic v2).
   - Backend menyimpan hasil audit ke tabel PostgreSQL `audit_matrix_items` menggunakan transaksi Drizzle ORM.

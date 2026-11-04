# Compliance-Agent

> **Autonomous Regulatory Compliance Copilot for Indonesian FinTech Contracts**  
> Mengotomasi audit kepatuhan hukum kontrak pinjaman (P2P lending), SLA perbankan digital, dan kebijakan privasi terhadap regulasi **OJK (POJK No. 10/2022, SEOJK No. 19/2023)**, **Bank Indonesia (BI)**, dan **UU No. 27 Tahun 2022 (UU PDP)** dengan *zero-hallucination guarantee*.

---

## 1. Arsitektur Monorepo & Pembagian Layanan

Projek ini menerapkan pemisahan tugas secara tegas (*Separation of Concerns*):

```
no-name/
├── frontend/               # Next.js 15 (React 19, TypeScript, Tailwind v4, Zustand)
│                           # Split-canvas Tiptap, compliance matrix, live SSE streaming.
├── backend/                # Express.js (TypeScript, Drizzle ORM, Zod, S3 Presigned URLs)
│                           # API Gateway, multi-tenant isolation (organization_id), RBAC.
├── agent/                  # Python 3.11+ (FastAPI, LangGraph, Gemini 2.0/1.5, Qdrant)
│                           # RAG engine, clause chunking PyMuPDF, deterministic math tools.
├── docs/                   # Dokumentasi arsitektur, PRD, dependensi, dan environment.
│   ├── adr/                # Architecture Decision Records (ADR 0001 - 0004).
│   ├── prd/                # Product Requirement Document.
│   ├── dependencies.md     # Katalog seluruh dependensi & rationale.
│   └── environment-variables.md # Daftar lengkap variabel environment & keamanan.
├── .agents/                # Panduan agent, spesifikasi sistem, dan workspace skills.
│   ├── AGENTS.md           # Aturan operasional & zero-hallucination directives.
│   ├── SPEC.md             # Spesifikasi teknis projek.
│   └── skills/             # 8 Skill modular Antigravity.
└── docker-compose.yml      # Infrastruktur lokal: Postgres 16, Qdrant, Redis, MinIO.
```

---

## 2. Kenapa Layanan Agent Dipisah dari Backend?

Berdasarkan keputusan pada [ADR-0004](docs/adr/0004-service-separation-and-template-structure.md):
1. **Afinitas Library:** Python memimpin ekosistem AI/RAG (`langgraph`, `google-genai`, `pymupdf`), sementara TypeScript di Backend & Frontend memberikan *end-to-end type safety* untuk API dan UI.
2. **Karakteristik Resource & Autoscaling:** Backend bersifat *I/O bound* (ringan, melayani session dan web traffic cepat), sementara Agent bersifat *compute bound* (ekstraksi PDF puluhan halaman dan evaluasi AI). Keduanya dapat di-scale secara terpisah.
3. **Keamanan & Isolasi Rahasia:** Layanan `agent/` berjalan di jaringan internal privat. Kredensial AI (`GEMINI_API_KEY`, `LANGFUSE_SECRET_KEY`) tidak pernah menyentuh layer web atau browser.
4. **Independensi Pengujian:** Tim AI dapat menguji dan mengotak-atik agent secara *headless* (via CLI / Pytest) tanpa menunggu fitur UI atau database web selesai.

---

## 3. Quickstart: Menjalankan Projek

### Langkah 1: Siapkan Konfigurasi Lingkungan (`.env`)
Salin semua template environment yang telah disediakan (ingat: **JANGAN PERNAH HARDCODE KREDENSIAL**):

```bash
# 1. Konfigurasi infrastruktur docker
cp .env.example .env

# 2. Konfigurasi backend API
cp backend/.env.example backend/.env

# 3. Konfigurasi agent AI
cp agent/.env.example agent/.env

# 4. Konfigurasi frontend web
cp frontend/.env.example frontend/.env.local
```

Buka dan isi nilai-nilai rahasia (seperti `POSTGRES_PASSWORD`, `JWT_SECRET`, `GEMINI_API_KEY`, dll.) pada masing-masing file `.env`.

### Langkah 2: Jalankan Infrastruktur Lokal
Pastikan Docker Desktop aktif, lalu jalankan:

```bash
pnpm infra:up
```
Ini akan menyalakan container:
- **PostgreSQL** di port `5432`
- **Redis** di port `6379`
- **MinIO (S3)** di port `9000` (API) & `9001` (Dashboard)
- **Qdrant Vector DB** di port `6333`

### Langkah 3: Jalankan Backend API Gateway
Di terminal terpisah:

```bash
cd backend
pnpm install
pnpm db:migrate    # Menjalankan migrasi skema tabel Drizzle
pnpm dev           # Berjalan di http://localhost:4000
```

### Langkah 4: Jalankan AI Agent Service
Di terminal terpisah:

```bash
cd agent
# Buat virtual environment (opsional via uv atau venv)
python -m venv .venv
source .venv/bin/activate  # atau .venv\Scripts\activate di Windows
pip install -e .
uvicorn app.main:app --reload --port 8000   # Berjalan di http://localhost:8000
```
Dokumentasi interaktif Swagger UI agent tersedia di: `http://localhost:8000/docs`.

### Langkah 5: Jalankan Frontend Web Canvas
Di terminal terpisah:

```bash
cd frontend
pnpm install
pnpm dev           # Berjalan di http://localhost:3000
```

---

## 4. Menjalankan Pengujian Otomatis

* **Uji Coba Backend (Vitest & Supertest):**
  ```bash
  pnpm test:backend
  ```
* **Uji Coba Agent & Kalkulator Deterministik (Pytest):**
  ```bash
  pnpm test:agent
  ```

---

## 5. Dokumentasi Terkait
* [ADR-0001: Arsitektur Inti & Tech Stack](docs/adr/0001-system-architecture-and-tech-stack.md)
* [ADR-0002: Orkestrasi Multi-Agent LangGraph & Model Tiering](docs/adr/0002-multi-agent-orchestration-and-model-tiering.md)
* [ADR-0003: Multi-Tenant Data Storage & Qdrant Vector Search](docs/adr/0003-data-storage-and-vector-search.md)
* [ADR-0004: Pemisahan Layanan Backend API vs AI Agent Core](docs/adr/0004-service-separation-and-template-structure.md)
* [Katalog Dependensi Lengkap](docs/dependencies.md)
* [Kamus Variabel Environment](docs/environment-variables.md)
* [Spesifikasi Desain Harvey Legal-Tech](DESIGN.md)

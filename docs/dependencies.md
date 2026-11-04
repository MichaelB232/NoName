# Dependency Inventory & Technical Stack Catalog

Dokumen ini mencatat seluruh dependensi teknis, pustaka pihak ketiga, tujuan fungsional, analisis keamanan/vulnerabilitas, dan alasan pemilihan teknologi yang digunakan di dalam projek **Compliance-Agent**.

---

## 1. Local Infrastructure (`docker-compose.yml`)

Layanan pendukung lokal dijalankan via Docker untuk menjamin reproduktibilitas tanpa instalasi manual di sistem host pengembang.

| Layanan | Image & Versi | Port Host | Fungsi & Rationale |
| :--- | :--- | :--- | :--- |
| **PostgreSQL** | `postgres:16-alpine` | `5432` | Basis data relasional utama. Mendukung UUIDv4, JSONB, foreign key cascades, dan isolasi tenant dengan ACID guarantees. |
| **Redis** | `redis:7-alpine` | `6379` | In-memory message broker & cache. Digunakan untuk Pub/Sub relay Server-Sent Events (SSE) antara Agent dan Backend serta distributed rate-limiting. |
| **MinIO** | `minio/minio:latest` | `9000` (API)<br>`9001` (Web) | S3-compatible object storage. Menyimpan berkas kontrak PDF/DOCX asli, aset halaman, dan laporan audit secara terisolasi per prefix tenant. |
| **Qdrant** | `qdrant/qdrant:latest` | `6333` | Vector Database berspesialisasi dalam hybrid search (dense embedding + sparse lexical filtering) untuk regulasi FinTech (POJK, UU PDP, BI). |

---

## 2. Backend API Gateway (`backend/`)

* **Runtime:** Node.js v20.11+ LTS  
* **Package Manager:** `pnpm` (v9+)  
* **Pola Arsitektur:** Vertical Slice Architecture (Modul berbasis fitur di `src/modules/`)

### A. Production Dependencies (`dependencies`)

| Package | Versi | Status Keamanan & Alasan Penggunaan |
| :--- | :--- | :--- |
| **`jose`** *(Pengganti jsonwebtoken)* | `^5.9.6` | **HARDENED ALTERNATIVE.** Menggantikan pustaka legacy `jsonwebtoken`. Dibuat oleh tim Auth0/OpenID Foundation, **zero-dependencies**, menggunakan native Web Crypto API, anti-*algorithm confusion* (enforce HS256), bebas dari CVE historis `jws`/`jwa`. |
| **`express`** | `^5.0.1` | Rilis resmi Express 5 stabil. Sudah memuat patch terhadap kerentanan Path Traversal (CVE-2024-43796) dan Prototype Pollution (CVE-2024-43799) pada versi terdahulu. |
| **`drizzle-orm`** | `^0.39.3` | Headless TypeScript ORM. Mengombinasikan kecepatan query SQL murni dengan 100% type safety tanpa overhead runtime berat seperti Prisma. |
| **`pg`** | `^8.13.3` | PostgreSQL connection pooling client versi stabil dan teruji untuk Drizzle ORM. |
| **`zod`** | `^3.24.2` | Single source of truth untuk validasi runtime input (body, query, params) dan inferensi tipe data TypeScript otomatis. |
| **`@aws-sdk/client-s3`**<br>**`@aws-sdk/s3-request-presigner`** | `^3.750.0` | Menghasilkan Presigned URL upload/download S3/MinIO berdurasi pendek (max 600s) agar berkas biner tidak membebani server backend. |
| **`cookie-parser`** | `^1.4.7` | Membaca cookie autentikasi yang dikirimkan oleh browser Next.js secara aman. |
| **`cors`** | `^2.8.5` | Mengatur daftar origin browser yang diizinkan mengakses API (whitelist origin berbasis env). |
| **`helmet`** | `^8.0.0` | Menyuntikkan HTTP security headers standar (X-Content-Type-Options, Frameguard, HSTS). |
| **`express-rate-limit`** | `^7.5.0` | Melindungi endpoint sensitif (autentikasi dan presign upload) dari abuse dan brute force. |
| **`ioredis`** | `^5.5.0` | Client Redis berkinerja tinggi untuk mengonsumsi channel SSE progress agent dari worker AI. |
| **`pino`**<br>**`pino-http`** | `^9.6.0`<br>`^10.4.0` | Logger JSON berkecepatan tinggi dengan fitur redaksi otomatis untuk field sensitif (token, password, cookie). |

### B. Development Dependencies (`devDependencies`)

| Package | Versi | Fungsi |
| :--- | :--- | :--- |
| **`typescript`** | `^5.7.3` | Kompiler bahasa dengan pengaturan `"strict": true`, `"noImplicitAny": true`. |
| **`tsx`** | `^4.19.3` | Eksekusi TypeScript langsung pada development mode (`pnpm dev`) dengan hot-reload kilat. |
| **`drizzle-kit`** | `^0.30.4` | CLI otomatisasi migrasi database SQL (`db:generate`, `db:migrate`, `db:studio`). |
| **`vitest`** | `^3.0.5` | Test runner modern berkecepatan tinggi, kompatibel dengan Vite dan ESM. |
| **`supertest`** | `^7.0.0` | HTTP testing harness untuk menguji endpoint Express tanpa mengikat port jaringan fisik. |
| **`pino-pretty`** | `^13.0.0` | Pemformat log berwarna yang mudah dibaca saat lokal development. |

---

## 3. Autonomous AI Agent Service (`agent/`)

* **Runtime:** Python 3.11+  
* **Package/Env Manager:** `uv` atau `pip` / `venv`  
* **Pola Arsitektur:** Stateful LangGraph Workflow Graph dengan Pydantic v2 Contract Envelopes

### A. Core AI & Service Dependencies

| Library | Versi | Peran dalam Compliance-Agent |
| :--- | :--- | :--- |
| **`fastapi`** | `>=0.115` | Framework microservice asinkron (`async def`) berkecepatan tinggi dengan auto-generated OpenAPI. |
| **`uvicorn[standard]`** | `>=0.34` | ASGI web server produksi berkinerja tinggi berbasis `uvloop` dan `httptools`. |
| **`langgraph`** | `>=0.4` | Orkestrator state machine siklik untuk tahapan agent (*Parser $\rightarrow$ Auditor $\rightarrow$ Evaluator $\rightarrow$ Drafter*). Enforce `MAX_STEPS = 5`. |
| **`google-genai`** | `>=1.20` | SDK resmi Google Gemini untuk Two-Tier Routing: Tier 1 (`gemini-2.0-flash`) & Tier 2 (`gemini-1.5-pro`). |
| **`qdrant-client`** | `>=1.14` | Client vector DB untuk semantic & hybrid search regulasi perbankan/fintech Indonesia (POJK, UU PDP). |
| **`pymupdf`** (`fitz`) | `>=1.25` | Engine ekstraksi teks dan struktur PDF berperforma tinggi dari berkas kontrak multi-halaman. |
| **`pydantic`**<br>**`pydantic-settings`** | `>=2.10`<br>`>=2.7` | Validasi skema input/output data ketat dan pembacaan konfigurasi environment terisolasi. |
| **`redis`** | `>=5.2` | Mempublikasikan status progres agent per klausul ke channel Redis untuk diteruskan ke frontend. |
| **`httpx`** | `>=0.28` | Asynchronous HTTP client untuk interaksi webhook dan health checks. |
| **`langfuse`** | `>=3.0` | Observabilitas LLMOps lengkap: tracing langkah demi langkah, tracking biaya token, dan latensi inferensi. |

### B. Code Quality & Testing

| Tool | Versi | Fungsi |
| :--- | :--- | :--- |
| **`pytest`**<br>**`pytest-asyncio`** | `>=8.3`<br>`>=0.25` | Pengujian unit kalkulator deterministik denda OJK dan integrasi state LangGraph. |
| **`ruff`** | `>=0.11` | Linter dan formatter Python super cepat pengganti Flake8, Black, dan isort. |
| **`mypy`** | `>=1.15` | Static type checker ketat dengan plugin pydantic. |

---

## 4. Web Canvas Frontend (`frontend/`)

* **Framework:** Next.js 15 (App Router, React 19)  
* **Styling Engine:** Tailwind CSS v4  
* **Design Philosophy:** Institutional Legal-Tech (Harvey AI Inspired)

| Package | Versi | Status Keamanan & Alasan Penggunaan |
| :--- | :--- | :--- |
| **`next`** | `^15.1.7` | **PATCHED VERSION.** Menggunakan versi yang telah menambal kerentanan kritis SSRF pada Server Actions (CVE-2024-34351), cache key poisoning (CVE-2024-46982), dan DoS pada middleware routing. |
| **`react`**<br>**`react-dom`** | `^19.0.0` | Library antarmuka reaktif versi stabil resmi. |
| **`tailwindcss`**<br>**`@tailwindcss/postcss`** | `^4.0.8` | Versi rilis stabil Tailwind v4; menggunakan blok `@theme` di `globals.css`. |
| **`zustand`** | `^5.0.3` | State management client ringan untuk mengelola koordinat klausul aktif dan navigasi *bi-directional jump*. |
| **`@tanstack/react-query`** | `^5.66.0` | Manajemen data fetching, caching, dan sinkronisasi status kontrak server versi stabil. |
| **`lucide-react`** | `^0.475.0` | Ikonografi minimalis monokromatik bergaya institusional firma hukum. |
| **`clsx`**<br>**`tailwind-merge`** | `^2.1.1`<br>`^3.0.1` | Utilitas penggabung class Tailwind dinamis tanpa risiko konflik style (konvensi shadcn/ui). |
| **`zod`** | `^3.24.2` | Validasi payload event SSE sebelum diproses oleh komponen UI. |
| **`server-only`** | `^0.0.1` | Penjaga arsitektur: mencegah berkas modul server-side terimport secara tidak sengaja ke browser client bundle. |

# Environment Variables & Secret Management Reference

Panduan ini mencatat seluruh variabel konfigurasi lingkungan di projek **Compliance-Agent**.

> **ATURAN MUTLAK KEAMANAN (Zero-Hardcode Directive):**
> 1. Dilarang keras menuliskan API key, password database, atau token rahasia secara langsung di dalam kode program (`git commit`).
> 2. Semua file `.env` asli telah didaftarkan ke dalam [`.gitignore`](file:///d:/MikeStuff/Project/no-name/.gitignore).
> 3. Pengembang baru wajib menyalin file template `*.env.example` ke `*.env` masing-masing sebelum menjalankan layanan.
> 4. Seluruh variabel diverifikasi secara otomatis saat proses *boot* aplikasi menggunakan **Zod** (Backend & Frontend) dan **Pydantic-Settings** (Agent). Aplikasi akan langsung menolak berjalan (*fail-fast*) jika ada konfigurasi wajib yang kosong.

---

## 1. Root Environment (`.env`) — Local Infrastructure

Digunakan secara eksklusif oleh [`docker-compose.yml`](file:///d:/MikeStuff/Project/no-name/docker-compose.yml).

| Variabel | Sensitivitas | Deskripsi & Contoh Nilai |
| :--- | :---: | :--- |
| `POSTGRES_USER` | Publik | Username admin PostgreSQL (default: `compliance`). |
| `POSTGRES_PASSWORD` | **RAHASIA** | Password basis data PostgreSQL lokal. |
| `POSTGRES_DB` | Publik | Nama basis data utama (default: `compliance_agent`). |
| `POSTGRES_PORT` | Konfigurasi | Port host PostgreSQL (default: `5432`). |
| `REDIS_PASSWORD` | **RAHASIA** | Password proteksi instance Redis. |
| `REDIS_PORT` | Konfigurasi | Port host Redis (default: `6379`). |
| `MINIO_ROOT_USER` | **RAHASIA** | Root access key MinIO (S3 lokal). |
| `MINIO_ROOT_PASSWORD` | **RAHASIA** | Root secret key MinIO (S3 lokal, minimal 8 karakter). |
| `MINIO_API_PORT` | Konfigurasi | Port S3 API MinIO (default: `9000`). |
| `MINIO_CONSOLE_PORT`| Konfigurasi | Port Web UI Dashboard MinIO (default: `9001`). |
| `QDRANT_API_KEY` | **RAHASIA** | Kunci API untuk mengamankan instance Qdrant. |
| `QDRANT_HTTP_PORT` | Konfigurasi | Port HTTP REST API Qdrant (default: `6333`). |

---

## 2. Backend API Gateway Environment (`backend/.env`)

Diverifikasi oleh [`src/config/env.ts`](file:///d:/MikeStuff/Project/no-name/backend/src/config/env.ts).

| Variabel | Tipe Data | Sensitivitas | Deskripsi & Validasi |
| :--- | :---: | :---: | :--- |
| `NODE_ENV` | Enum | Standar | `development` \| `test` \| `production`. |
| `PORT` | Integer | Standar | Port server HTTP Express (default: `4000`). |
| `LOG_LEVEL` | Enum | Standar | Level log Pino: `debug`, `info`, `warn`, `error`. |
| `CORS_ORIGINS` | String | Konfigurasi | Daftar URL origin browser dipisah koma (contoh: `http://localhost:3000`). |
| `DATABASE_URL` | URL | **RAHASIA** | Format: `postgres://USER:PASSWORD@HOST:PORT/DB`. |
| `REDIS_URL` | URL | **RAHASIA** | Format: `redis://:PASSWORD@HOST:PORT`. |
| `JWT_SECRET` | String | **RAHASIA** | Kunci penandatangan JWT session (minimal 32 karakter). |
| `JWT_EXPIRES_IN` | String | Konfigurasi | Durasi masa berlaku sesi (default: `8h`). |
| `AUTH_COOKIE_NAME` | String | Standar | Nama cookie `httpOnly` (default: `ca_session`). |
| `S3_ENDPOINT` | URL | Konfigurasi | Endpoint S3 (`http://localhost:9000` lokal, atau AWS S3 URL). |
| `S3_REGION` | String | Konfigurasi | Wilayah bucket (contoh: `ap-southeast-3`). |
| `S3_BUCKET` | String | Konfigurasi | Nama bucket penyimpanan kontrak (default: `compliance-contracts`). |
| `S3_ACCESS_KEY_ID` | String | **RAHASIA** | Kunci akses IAM S3 / MinIO. |
| `S3_SECRET_ACCESS_KEY`| String | **RAHASIA** | Kunci rahasia IAM S3 / MinIO. |
| `S3_FORCE_PATH_STYLE` | Boolean | Konfigurasi | Wajib `true` untuk MinIO lokal, `false` untuk AWS S3 virtual-hosted. |
| `S3_PRESIGN_TTL_SECONDS`| Integer | Keamanan | Durasi link upload sementara (maksimal 600 detik / 10 menit sesuai skill). |
| `UPLOAD_MAX_BYTES` | Integer | Keamanan | Batas ukuran berkas maksimum (default: `26214400` = 25 MB). |
| `AGENT_SERVICE_URL` | URL | Internal | Alamat internal layanan AI Agent (default: `http://localhost:8000`). |
| `AGENT_SERVICE_TOKEN`| String | **RAHASIA** | Token rahasia otentikasi internal antar-layana (wajib sama dengan di Agent). |

---

## 3. AI Agent Service Environment (`agent/.env`)

Diverifikasi oleh [`app/core/config.py`](file:///d:/MikeStuff/Project/no-name/agent/app/core/config.py).

| Variabel | Tipe Data | Sensitivitas | Deskripsi & Validasi |
| :--- | :---: | :---: | :--- |
| `APP_ENV` | Enum | Standar | `development` \| `test` \| `production`. |
| `LOG_LEVEL` | Enum | Standar | Level log Uvicorn/Python: `DEBUG`, `INFO`, `WARNING`, `ERROR`. |
| `PORT` | Integer | Standar | Port server ASGI FastAPI (default: `8000`). |
| `AGENT_SERVICE_TOKEN`| String | **RAHASIA** | Token rahasia otentikasi panggilan dari Backend API Gateway. |
| `GEMINI_API_KEY` | String | **RAHASIA** | Kunci otentikasi Google Gemini API. |
| `GEMINI_MODEL_TIER1` | String | Model Routing | Model Tier 1 untuk parsing & tool calling (default: `gemini-2.0-flash`). |
| `GEMINI_MODEL_TIER2` | String | Model Routing | Model Tier 2 untuk audit hukum mendalam (default: `gemini-1.5-pro`). |
| `GEMINI_EMBEDDING_MODEL`| String | AI Config | Model embedding vector RAG (default: `text-embedding-004`). |
| `QDRANT_URL` | URL | Konfigurasi | Alamat server vector database (default: `http://localhost:6333`). |
| `QDRANT_API_KEY` | String | **RAHASIA** | API Key otentikasi cluster Qdrant. |
| `QDRANT_COLLECTION` | String | Konfigurasi | Nama koleksi regulasi (default: `indonesia_financial_regulations`). |
| `QDRANT_SCORE_THRESHOLD`| Float | AI Guardrail | Ambang batas kemiripan kosinus (0.72). Di bawah ini dianggap unverified. |
| `REDIS_URL` | URL | **RAHASIA** | Format: `redis://:PASSWORD@HOST:PORT` untuk SSE streaming channel. |
| `LANGFUSE_PUBLIC_KEY` | String | Opsional | Kunci publik tracing observabilitas Langfuse. |
| `LANGFUSE_SECRET_KEY` | String | **RAHASIA** | Kunci rahasia tracing observabilitas Langfuse. |
| `LANGFUSE_HOST` | URL | Konfigurasi | Endpoint Langfuse (default: `https://cloud.langfuse.com`). |
| `AGENT_MAX_STEPS` | Integer | AI Guardrail | Batas siklus refleksi LangGraph (default: `5`, maksimal 5). |

---

## 4. Frontend Web Canvas Environment (`frontend/.env.local`)

Diverifikasi oleh [`src/lib/env.ts`](file:///d:/MikeStuff/Project/no-name/frontend/src/lib/env.ts) dan [`src/lib/serverEnv.ts`](file:///d:/MikeStuff/Project/no-name/frontend/src/lib/serverEnv.ts).

| Variabel | Cakupan | Sensitivitas | Deskripsi & Validasi |
| :--- | :---: | :---: | :--- |
| `NEXT_PUBLIC_API_BASE_URL` | Browser Publik | Publik | URL API Gateway yang diakses oleh browser klien (contoh: `http://localhost:4000/api/v1`). |
| `BACKEND_INTERNAL_URL` | Server Only | Internal | URL API Gateway untuk React Server Components di dalam jaringan privat Docker/Kubernetes. |

> ⚠️ **Catatan Penting Keamanan Frontend:**
> Variabel dengan prefix `NEXT_PUBLIC_` akan dikompilasi langsung ke dalam bundle JavaScript browser pengguna. **JANGAN PERNAH** menaruh secret, API key pihak ketiga, atau password pada variabel berawalan `NEXT_PUBLIC_`. Frontend tidak menyimpan token sesi; otentikasi ditangani via cookie `httpOnly` yang dikelola browser.

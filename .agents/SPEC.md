# PROJECT SPECIFICATION: COMPLIANCE-AGENT (CODENAME)
**Autonomous Regulatory & FinTech Contract Compliance Copilot**

---

## 1. Executive Summary & Business Case

### 1.1 Problem Statement
In modern financial institutions, digital banks, P2P lending platforms, and fintech startups, launching new credit or financial products is constantly delayed by regulatory compliance bottlenecks. Compliance Officers and In-House Legal Counsels must manually review 50–100+ pages of complex loan agreements, terms & conditions (T&C), and privacy policies against volatile regulations issued by:
- **OJK (Otoritas Jasa Keuangan):** Daily interest rate caps, late payment fee caps, consumer protection, collection ethical boundaries.
- **Bank Indonesia (BI):** Payment system standards, APU-PPT (anti-money laundering).
- **UU No. 27 Tahun 2022 (UU PDP):** Personal data protection and strict limitations on mobile device permissions (CAM: Camera, Audio, Location only).

A single overlooked clause exposes financial institutions to severe administrative fines, reputational ruin, or outright revocation of their operational licenses.

### 1.2 The Solution
An enterprise-grade B2B SaaS platform inspired by the collaborative legal canvas model (e.g., Harvey AI). It enables Product and Compliance teams to upload contracts and leverages an autonomous Multi-Agent AI system to:
1. Parse contracts into granular, traceable clauses.
2. Cross-audit clauses against indexed OJK and UU PDP regulations using Agentic RAG.
3. Quantify risk scores and calculate financial penalties via deterministic math tools.
4. Provide verifiable legal citations with zero-hallucination guarantees.
5. Offer one-click, Git-style diff redrafting within a collaborative split-screen editor.

---

## 2. System Architecture & Tech Stack

```
[ FRONTEND ] ──── Next.js 15 (TypeScript) + Tailwind + Shadcn UI + Tiptap Canvas
     │
     ▼ (REST & Server-Sent Events / SSE)
[ BACKEND API & MULTI-AGENT ] ──── FastAPI (Python 3.11+) + LangGraph + Pydantic v2
     │
     ├── [ OBJECT STORAGE ] ───── MinIO / S3 (Raw Contract PDFs/DOCX)
     ├── [ PRIMARY DATABASE ] ─── PostgreSQL (Multi-tenant schema with organization_id)
     ├── [ VECTOR DATABASE ] ──── Qdrant (Semantic search for POJK & UU PDP regulations)
     ├── [ CACHE & SESSION ] ──── Redis (Regulation cache, session state, rate limiting)
     └── [ LLMOPS TRACING ] ───── Langfuse (Step-by-step agent telemetry, token cost & latency)
```

### 2.1 Technology Decisions & Rationale
- **Backend & AI Core (Python 3.11+ / FastAPI):** Selected for unmatched AI SDK maturity, asynchronous I/O (`uvloop`), and robust PDF/tabular document extraction libraries (`PyMuPDF`, `pdfplumber`).
- **Multi-Agent Orchestration (LangGraph):** Employs a stateful, cyclical graph architecture (*State Machine*) enforcing deterministic agent transitions and strict step guardrails (`MAX_STEPS = 5`) to prevent infinite looping.
- **Frontend (Next.js 15 / React / TypeScript):** High-performance dashboard rendering with rich-text editor integration (**Tiptap**) for document interaction, live inline annotations, and SSE streaming.
- **Multi-Tenant Relational DB (PostgreSQL):** Stores accounts, role-based access control (RBAC), contract metadata, and structured audit findings. Enforces data isolation via `organization_id`.
- **Vector DB (Qdrant):** Dedicated vector storage utilizing hybrid search (dense semantic embeddings + sparse BM25) and payload filtering for rapid clause retrieval (<20ms).
- **Object Storage (MinIO / S3):** Ensures cloud-native, stateless application servers by offloading binary document storage.
- **LLMOps Observability (Langfuse):** Complete visibility into agent reasoning trajectories (*Thought $\rightarrow$ Action $\rightarrow$ Observation*), latency bottlenecks, and token expenses.

---

## 3. AI Model Tiering Strategy

To balance cost efficiency, speed, and complex legal reasoning, the system uses a **Two-Tier Model Architecture** using Google Gemini API:

| Tier | Model | Tasks Assigned | Rationale |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Fast & High Volume)** | **Gemini 1.5 / 2.0 Flash** | • Contract parsing & JSON formatting<br>• Code/Math tool execution<br>• Initial classification | High throughput, sub-second latency, ultra-low token consumption. |
| **Tier 2 (Deep Reasoning)** | **Gemini 1.5 Pro** | • Regulatory compliance cross-analysis<br>• Risk level adjudication<br>• Contextual legal clause redrafting | Deep context evaluation, superior nuanced reasoning over Indonesian legal statutes, zero-hallucination compliance. |

---

## 4. Multi-Agent Lifecycle & Workflow

```
[ Upload Contract PDF ]
          │
          ▼
┌──────────────────────────────────────────────┐
│ AGENT 1: Clause Parser & Structurer          │ (Gemini Flash)
│ Splits continuous PDF text into discrete,    │
│ numbered clause objects with metadata.       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ AGENT 2: Regulatory Compliance Auditor (RAG) │ (Gemini Pro)
│ Queries Qdrant for POJK & UU PDP articles,   │
│ cross-examines clauses against legal caps.   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ AGENT 3: Risk & Penalty Evaluator            │ (Gemini Flash)
│ Runs Python calculator tools to quantify     │
│ interest overages & OJK penalty exposure.    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ AGENT 4: Clause Redrafter                    │ (Gemini Pro)
│ Synthesizes clean, legally compliant drafted │
│ alternative clauses (Git-style diff output). │
└──────────────────────────────────────────────┘
```

---

## 5. UI/UX Specifications: Collaborative Split-Screen Canvas

1. **Split-Screen Workspace:**
   - **Left Canvas (60%):** Interactive contract document viewer powered by Tiptap.
   - **Right Panel (40%):** Executive Compliance Summary & Interactive Audit Matrix.
2. **Bi-directional Jump Navigation:**
   - Clicking a **Clause Number** on the matrix scrolls the left canvas to the exact paragraph, applying a pulsing red/amber border.
   - Clicking a **Regulation Tag** (e.g., `POJK No. 10/2022 Art. 29 para. (2)`) slides out the official government statute drawer with verbatim source text highlighted.
3. **One-Click Git-Style Diff Remediation:**
   - Problematic sentences show red strikethrough; AI recommendations appear in green.
   - Authorized reviewers click `[Accept]` to apply changes directly into the live document state.

---

## 6. Database Schema (PostgreSQL DDL)

```sql
-- 1. Tenants / Organizations
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users & RBAC
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'LEGAL_OFFICER', -- 'ADMIN', 'SENIOR_LEGAL', 'LEGAL_OFFICER', 'PRODUCT_TEAM'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Contract Documents
CREATE TABLE contracts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    uploaded_by UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    file_s3_key VARCHAR(500) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING', -- 'PENDING', 'PROCESSING', 'AUDITED', 'APPROVED'
    overall_compliance_score INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Clause Audit Findings (Matrix Rows)
CREATE TABLE clause_audit_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id UUID NOT NULL REFERENCES contracts(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    clause_title VARCHAR(255) NOT NULL,
    original_text TEXT NOT NULL,
    is_compliant BOOLEAN NOT NULL,
    violated_rule VARCHAR(255),
    risk_level VARCHAR(20), -- 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    audit_explanation TEXT,
    suggested_revision TEXT,
    status VARCHAR(50) DEFAULT 'OPEN', -- 'OPEN', 'ACCEPTED', 'REJECTED'
    reviewed_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7. Phased Implementation Roadmap

- [ ] **Phase 1: Project Scaffolding & Infrastructure**
  - Setup directory structure, virtual environment, and `docker-compose.yml` (Postgres, Qdrant, MinIO, Redis).
  - Setup Pydantic contracts and Gemini API connection.
- [ ] **Phase 2: Ingestion & Vector DB Seeding**
  - Index core financial regulations (POJK No. 10/2022 on P2P Lending, UU No. 27/2022 UU PDP).
  - Build PDF clause extraction parser.
- [ ] **Phase 3: Multi-Agent Logic Implementation**
  - Implement LangGraph workflow (Clause Parser $\rightarrow$ Auditor $\rightarrow$ Risk Evaluator $\rightarrow$ Drafter).
  - Enforce structured output generation for the Compliance Matrix.
- [ ] **Phase 4: Backend API & Streaming Gateway**
  - Build FastAPI endpoints for document upload, job queue handling, and SSE streaming.
- [ ] **Phase 5: Frontend Canvas & Navigation Sync**
  - Build Next.js UI with split-screen Tiptap editor and interactive Audit Matrix with bi-directional jumps.

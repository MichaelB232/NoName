# ADR-0001: System Architecture and Core Tech Stack Selection

| Status | Accepted |
| :--- | :--- |
| **Date** | 2026-11-04 |
| **Deciders** | Architecture Team |
| **Consulted** | Legal & Engineering |

---

## 1. Context and Problem Statement

Building an enterprise-grade contract compliance audit tool requires:
1. High-throughput document parsing and text extraction (PDFs, DOCX).
2. Stateful, multi-step asynchronous AI agent execution with tool calling.
3. Interactive, rich-text split-screen UI for legal professionals with live bi-directional navigation.
4. Strict multi-tenant data isolation and low latency.

We need to choose a backend framework, frontend stack, primary database, and object storage that satisfy these criteria.

---

## 2. Decision

We have decided to adopt the following foundational stack:

1. **Backend API & Multi-Agent Core**: **FastAPI (Python 3.11+)**
   - *Rationale*: Python provides first-class support for AI/LLM ecosystems (LangGraph, Google GenAI SDK) and high-performance document parsing libraries (`PyMuPDF`, `pdfplumber`). FastAPI offers native asynchronous support, auto-generated OpenAPI documentation, and high throughput with `uvloop`.
2. **Frontend Canvas & Dashboard**: **Next.js 15 (React 19 / TypeScript) with Tailwind CSS & Shadcn UI**
   - *Rationale*: Rapid UI assembly using Shadcn UI primitives, full TypeScript safety, and optimal streaming support for Server-Sent Events (SSE).
   - *Editor Canvas*: **Tiptap** chosen for headless, customizable legal document rendering and inline annotation/diff capabilities.
3. **Primary Relational Database**: **PostgreSQL (Multi-tenant)**
   - *Rationale*: ACID compliance, robust UUID/JSONB support, and mature row/column level multi-tenancy enforcement via `organization_id`.
4. **Object Storage**: **MinIO (Local/Self-hosted) / AWS S3 (Production)**
   - *Rationale*: Keeps application servers stateless by storing binary contract files in S3-compatible storage.
5. **Observability**: **Langfuse**
   - *Rationale*: Dedicated open-source LLMOps observability for tracking agent execution trees, token costs, and prompt variations.

---

## 3. Consequences

### Positive
- Unified Python ecosystem for AI, RAG, and document processing.
- Clean separation of concerns between API gateway, agent state machine, and frontend visualization.
- Production-ready observability out of the box with Langfuse.

### Trade-offs / Mitigations
- **Monorepo / Multi-language overhead**: Requires managing both Node.js (frontend) and Python (backend) environments.
  - *Mitigation*: Dockerized development setup (`docker-compose.yml`) for seamless local onboarding.

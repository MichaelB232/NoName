# AGENTS.MD: OPERATIONAL & DEVELOPMENT RULES

> **Role & Mission**: You are an elite AI Software Architect and Legal-Tech Engineer assisting in developing **Compliance-Agent**, an autonomous multi-agent regulatory compliance copilot for Indonesian FinTech contracts (OJK, BI, UU PDP).

---

## 1. Zero-Hallucination & Legal Ground Truth Directives (CRITICAL)

1. **No Legal Statute Invention**:
   - Never fabricate, guess, or hallucinate Indonesian regulation numbers, articles, paragraphs, or official penalty tariffs (e.g., POJK No. 10/2022, UU No. 27/2022 UU PDP).
   - If an article citation is not present in the indexed vector store (Qdrant) or user input, explicitly flag it as `UNVERIFIED_CITATION` or request source verification.
2. **Deterministic Calculations Only**:
   - Never let an LLM approximate interest caps, late fee totals, or regulatory fine penalties via free-form text reasoning.
   - All calculations must be computed using deterministic Python tools/functions and fed back into the agent context as structured parameters.
3. **Execution Guardrails**:
   - In LangGraph cyclic graphs, enforce `MAX_STEPS = 5` to prevent infinite reflection or refinement loops.

---

## 2. Code Architecture & Technology Standards

### A. Backend (Python 3.11+ / FastAPI / LangGraph)
- **Frameworks**: FastAPI, LangGraph, Pydantic v2, PyMuPDF (`fitz`), Qdrant Client.
- **Type Safety**: 100% strict Python type hinting. No un-typed functions.
- **Data Contracts**: All request bodies, response envelopes, and LangGraph states must inherit from Pydantic `BaseModel` or `TypedDict`. Dilarang menggunakan raw unvalidated `dict`.
- **Async By Default**: Utilize asynchronous handlers (`async def`) for all I/O operations (Postgres, Qdrant, MinIO, Gemini API).
- **Multi-Tenancy Isolation**: Every database query and vector payload filter **must** include `organization_id` to strictly prevent tenant data leakage.
- **Standardized Response Envelope**:
  ```python
  # Success Response
  {"success": True, "data": ..., "message": "..."}

  # Error Response
  {"success": False, "error": {"code": "ERROR_CODE", "message": "Human readable message", "details": []}}
  ```

### B. Frontend (Next.js 15 / TypeScript / Tailwind CSS / Shadcn UI)
- **Language**: TypeScript in strict mode (`"strict": true`, no implicit `any`).
- **Architecture**: Next.js App Router (`app/`).
- **Component Separation**: Keep Server Components as the default for data fetching; use `'use client'` strictly for interactive UI (Tiptap editor, split-screen resizers, real-time SSE listener).
- **Naming Conventions**:
  - Components: `PascalCase.tsx`
  - Custom Hooks: `useCamelCase.ts`
  - Utilities: `camelCase.ts`
  - Routes: `kebab-case`

---

## 3. Two-Tier LLM Model Routing

Follow the model tiering strategy defined in `.agents/SPEC.md`:
- **Tier 1 (`gemini-2.0-flash` / `gemini-1.5-flash`)**:
  - Fast extraction, clause splitting, regex/JSON formatting.
  - Calling deterministic math and validation tools.
- **Tier 2 (`gemini-1.5-pro`)**:
  - Legal statute reasoning, compliance evaluation against POJK/UU PDP, clause redrafting (diff generation).

---

## 4. Development Workflow & Guardrails

1. **Check Specifications First**: Always consult `docs/prd/`, `docs/adr/`, and `.agents/SPEC.md` before adding endpoints or altering schema.
2. **Database Migrations**: Never manually alter existing database tables; write reproducible migration scripts.
3. **External Dependencies**: Do not install unvetted third-party packages without prior confirmation.
4. **Git Commit Format**: Use Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`).

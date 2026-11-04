# ADR-0003: Multi-Tenant Data Storage and Hybrid Vector Search Architecture

| Status | Accepted |
| :--- | :--- |
| **Date** | 2026-11-04 |
| **Deciders** | Data & Backend Team |

---

## 1. Context and Problem Statement

The platform must store:
1. Multi-tenant relational data (users, organizations, contracts, audit results, audit trail).
2. Large corpus of Indonesian statutory regulations (POJK, SEOJK, UU PDP, Bank Indonesia regulations) with sub-second retrieval latency and high semantic recall.
3. Binary contract files (PDF, DOCX).
4. Ephemeral session state and regulation cache.

---

## 2. Decision

We separate storage responsibilities across specialized engines:

1. **Relational Database: PostgreSQL**
   - Stores tenant hierarchy, user identities, contract records, and granular `clause_audit_results`.
   - Enforces multi-tenancy at the data layer using foreign keys tied to `organization_id`.

2. **Vector Database: Qdrant**
   - Stores chunked Indonesian regulatory articles with dense vector embeddings and sparse lexical tokens (BM25) for **Hybrid Search**.
   - Leverages payload filtering (e.g., filter by `regulation_type: 'POJK'`, `status: 'ACTIVE'`, `year: 2022`) to eliminate irrelevant retrieval candidates before reranking.

3. **In-Memory Cache: Redis**
   - Caches parsed regulatory lookups, active SSE session channels, and rate-limiting counters.

4. **Object Storage: MinIO / AWS S3**
   - Retains original uploaded contract documents, processed page images, and exported audit PDF reports.

---

## 3. Consequences

### Positive
- Hybrid search in Qdrant ensures both exact legal keyword matches (e.g., "0.3% per hari", "CAM") and broad conceptual matches are retrieved accurately.
- Relational integrity and financial audit history remain fully ACID compliant in PostgreSQL.

### Trade-offs / Mitigations
- Multiple infrastructure services need coordination.
  - *Mitigation*: Single `docker-compose.yml` encapsulating Postgres, Qdrant, Redis, and MinIO for local development.

---
name: ai-agent-rag-standards
description: >-
  Use this skill when developing or modifying the multi-agent compliance pipeline, LangGraph state machine, RAG ingestion with PyMuPDF, Qdrant vector retrieval, or Gemini model routing.
---

# AI Agent & RAG Standards
**Engine:** Python 3.11+ / FastAPI / LangGraph  
**LLM Providers:** Google Gemini 1.5 Flash (Parsing/Math/Formatting) & Gemini 1.5 Pro (Deep Audit/Reasoning)  
**Vector Database:** Qdrant (HNSW Cosine Similarity Indexing)  
**Ingestion Engine:** PyMuPDF (fitz) + Custom Clause Chunking

---

## 1. Multi-Agent Pipeline Graph (LangGraph)

The audit workflow runs as a directed state machine:

```
[Start: Raw PDF in MinIO]
           │
           ▼
┌──────────────────────┐
│  Clause Parser Agent │  -> Segments PDF into discrete, numbered Clause Objects
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Compliance Auditor   │  <-> Queries Qdrant for POJK / UU PDP Regulatory Articles
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Risk Evaluator Agent │  -> Computes deterministic financial fines & violation severity
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Legal Drafter Agent  │  -> Generates compliant redline revisions & legal explanations
└──────────┬───────────┘
           ▼
[End: Compliance Matrix JSON & Redlines]
```

---

## 2. Model Tiering Matrix

| Agent Role | Model Selected | Rationale & Cost Strategy |
| :--- | :--- | :--- |
| **Clause Parser** | `gemini-1.5-flash` | High throughput, low latency, large context window (cheap parsing). |
| **Regulatory Auditor** | `gemini-1.5-pro` | Complex legal reasoning, cross-referencing nuances in Indonesian laws. |
| **Risk Calculator** | Python Tool + Flash | Deterministic mathematical calculation (Never rely on LLM for interest rate math). |
| **Legal Drafter** | `gemini-1.5-pro` | Professional Indonesian formal legal wording (Bahasa Hukum baku). |

---

## 3. Strict Structured Output Standard

All Agent responses must conform to Pydantic v2 schemas:

```python
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class LegalCitation(BaseModel):
    regulator: Literal["OJK", "BI", "KOMINFO"]
    regulation_name: str = Field(description="e.g. POJK No. 10/POJK.05/2022")
    article: str = Field(description="e.g. Pasal 29 ayat (2)")
    article_quote: str = Field(description="Exact snippet from Qdrant retrieved chunk")

class ComplianceMatrixItem(BaseModel):
    clause_number: str = Field(description="e.g. Pasal 5.2")
    topic: str = Field(description="e.g. Batasan Bunga Harian / Akses Data Kontak")
    original_text: str
    status: Literal["COMPLIANT", "VIOLATION", "AMBIGUOUS"]
    violated_regulation: Optional[LegalCitation] = None
    severity: Literal["HIGH", "MEDIUM", "LOW", "CLEAN"]
    penalty_estimate_idr: int = Field(default=0, description="Deterministic risk calculation")
    suggested_revision: Optional[str] = Field(description="Compliant draft replacing original clause")
    legal_rationale: str

class ComplianceAuditReport(BaseModel):
    contract_id: str
    total_clauses: int
    compliance_score: float = Field(ge=0.0, le=100.0)
    matrix: List[ComplianceMatrixItem]
```

---

## 4. Qdrant RAG Ingestion & Query Isolation

Every vector embedded into Qdrant must contain rich metadata and tenant/domain filtering:

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Query Qdrant with deterministic filters
def retrieve_relevant_regulations(client: QdrantClient, query_vector: list[float], topic: str):
    search_result = client.search(
        collection_name="indonesia_financial_regulations",
        query_vector=query_vector,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="status",
                    match=models.MatchValue(value="BERLAKU") # Only active regulations
                )
            ]
        ),
        limit=4,
        score_threshold=0.72 # Filter out low relevance hallucination risks
    )
    return search_result
```

---

## 5. Guardrails & Token Limits

1. **Max Graph Steps:** Limit LangGraph loop execution to `recursion_limit=10` to avoid infinite retry loops.
2. **Deterministic Math Fallback:** Never ask the LLM *"What is 0.4% minus 0.3% on Rp 10.000.000?"*. Extract the numeric rate from the clause via regex/LLM and calculate the penalty delta in pure Python code.
3. **Audit Trail Logging:** All prompts, completions, and token usage must be tracked in Langfuse / logging middleware.

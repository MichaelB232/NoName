# ADR-0002: Multi-Agent Orchestration with LangGraph and Two-Tier LLM Architecture

| Status | Accepted |
| :--- | :--- |
| **Date** | 2026-11-04 |
| **Deciders** | AI & Architecture Team |

---

## 1. Context and Problem Statement

Legal contract compliance auditing involves multiple distinct cognitive tasks:
1. Fast, high-volume extraction of continuous text into discrete clause structures.
2. Semantic regulatory retrieval and cross-statute compliance analysis (requiring high legal nuance and zero hallucinations).
3. Deterministic mathematical evaluation (calculating exact interest rates, late fee ceilings, and statutory fines).
4. Redrafting non-compliant clauses while retaining legal enforceability.

Relying on a single prompt or a single model either leads to high token costs and latency (if using heavy reasoning models everywhere) or hallucinations and shallow analysis (if using lightweight models everywhere).

---

## 2. Decision

### 2.1 Multi-Agent Framework: LangGraph
We adopt **LangGraph** (StateGraph) for orchestrating the multi-agent lifecycle:
- **Cyclical State Machine**: Allows agents to evaluate, verify, and conditionally transition between stages.
- **Strict Guardrails**: Hard limit of `MAX_STEPS = 5` per clause evaluation to eliminate infinite agent loops.
- **Specialized Roles**:
  - `ClauseParserAgent`: Extracts and formats clauses into structured JSON.
  - `ComplianceAuditorAgent`: Performs RAG queries against Qdrant and evaluates clauses against POJK and UU PDP.
  - `RiskPenaltyEvaluator`: Invokes deterministic Python math tools for financial overages.
  - `ClauseRedrafterAgent`: Produces Git-style diff suggestions.

### 2.2 Two-Tier Model Strategy (Google Gemini API)

| Tier | Model | Assigned Tasks | Justification |
| :--- | :--- | :--- | :--- |
| **Tier 1 (High Throughput)** | **Gemini 2.0 Flash / 1.5 Flash** | Extraction, JSON structuring, tool execution | Sub-second latency, low token cost, high JSON reliability. |
| **Tier 2 (Deep Reasoning)** | **Gemini 1.5 Pro** | Legal statutory reasoning, risk adjudication, redrafting | Large context window, superior Indonesian legal comprehension, low hallucination rate. |

---

## 3. Consequences

### Positive
- **Cost & Latency Optimization**: ~70% of tokens processed by Tier 1 models, reserving Tier 2 for high-stakes legal reasoning.
- **Zero Hallucination in Math**: Numerical checks are strictly computed via Python tools, not LLM internal generation.

### Trade-offs / Mitigations
- Managing state schemas across multiple agents adds initial development complexity.
  - *Mitigation*: Strictly defined Pydantic state models shared across LangGraph nodes.

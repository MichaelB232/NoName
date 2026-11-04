"""Audit pipeline graph skeleton (ai-agent-rag-standards skill §1).

    clause_parser → compliance_auditor → risk_evaluator → legal_drafter → END

Nodes are placeholders: each only advances `step_count` so the wiring and the
MAX_STEPS guardrail can be tested before real LLM logic is added.
"""

from collections.abc import Callable

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.core.config import get_settings
from app.graph.state import AuditState

NODE_ORDER: tuple[str, ...] = ("clause_parser", "compliance_auditor", "risk_evaluator", "legal_drafter")


class MaxStepsExceededError(RuntimeError):
    """Raised when the graph exceeds AGENT_MAX_STEPS (.agents/AGENTS.md §1.3)."""


def _guarded(name: str) -> Callable[[AuditState], dict[str, object]]:
    def node(state: AuditState) -> dict[str, object]:
        max_steps = get_settings().agent_max_steps
        next_step = state["step_count"] + 1
        if next_step > max_steps:
            raise MaxStepsExceededError(f"Exceeded MAX_STEPS={max_steps} at node '{name}'")
        # TODO(phase-3): replace with real node logic (Tier-1/Tier-2 Gemini + deterministic tools).
        return {"step_count": next_step, "status": name}

    return node


def build_audit_graph() -> CompiledStateGraph:
    graph: StateGraph = StateGraph(AuditState)
    for name in NODE_ORDER:
        graph.add_node(name, _guarded(name))

    graph.set_entry_point(NODE_ORDER[0])
    for current, following in zip(NODE_ORDER, NODE_ORDER[1:], strict=False):
        graph.add_edge(current, following)
    graph.add_edge(NODE_ORDER[-1], END)

    return graph.compile()

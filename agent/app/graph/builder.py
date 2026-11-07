from collections.abc import Callable
from typing import Any

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.core.config import get_settings
from app.graph.state import AuditState
from app.graph.nodes.clause_parser import clause_parser_node
from app.graph.nodes.compliance_auditor import compliance_auditor_node
from app.graph.nodes.risk_evaluator import risk_evaluator_node
from app.graph.nodes.legal_drafter import legal_drafter_node

# Pemetaan nama node ke fungsi aslinya
NODE_MAP: dict[str, Callable[[AuditState], dict[str, Any]]] = {
    "clause_parser": clause_parser_node,
    "compliance_auditor": compliance_auditor_node,
    "risk_evaluator": risk_evaluator_node,
    "legal_drafter": legal_drafter_node,
}

# Urutan eksekusi alur kerja audit
NODE_ORDER: tuple[str, ...] = (
    "clause_parser",
    "compliance_auditor",
    "risk_evaluator",
    "legal_drafter",
)


class MaxStepsExceededError(RuntimeError):
    """Raised when the graph exceeds AGENT_MAX_STEPS"""

def _guarded(
    name: str, node_func: Callable[[AuditState], dict[str, Any]]
) -> Callable[[AuditState], dict[str, Any]]:
    def wrapper(state: AuditState) -> dict[str, Any]:
        try:
            max_steps = get_settings().agent_max_steps
        except Exception:
            max_steps = 5

        current_steps = state.get("step_count", 0)
        if current_steps >= max_steps:
            raise MaxStepsExceededError(
                f"Exceeded MAX_STEPS={max_steps} at node '{name}'"
            )

        return node_func(state)

    return wrapper


def build_audit_graph() -> CompiledStateGraph:
    graph: StateGraph = StateGraph(AuditState)

    for name in NODE_ORDER:
        node_fn = NODE_MAP[name]
        graph.add_node(name, _guarded(name, node_fn))

    graph.set_entry_point(NODE_ORDER[0])

    for current, following in zip(NODE_ORDER, NODE_ORDER[1:], strict=False):
        graph.add_edge(current, following)

    graph.add_edge(NODE_ORDER[-1], END)

    return graph.compile()

from decimal import Decimal

import pytest

from app.graph.builder import NODE_ORDER, MaxStepsExceededError, build_audit_graph
from app.tools.interest_calculator import InterestCapInput, evaluate_interest_cap

# NOTE: the cap below is an arbitrary TEST FIXTURE, not a regulatory value.
FIXTURE_CAP = Decimal("0.30")


def test_interest_over_cap_is_flagged_with_exact_excess() -> None:
    result = evaluate_interest_cap(
        InterestCapInput(
            contract_daily_rate_percent=Decimal("0.45"),
            regulatory_cap_daily_percent=FIXTURE_CAP,
            cap_source_citation="TEST_FIXTURE",
            principal_idr=Decimal("10000000"),
            tenor_days=30,
        )
    )
    assert result.is_within_cap is False
    assert result.excess_daily_rate_percent == Decimal("0.15")
    assert result.excess_interest_idr == Decimal("450000")


def test_interest_within_cap_has_zero_excess() -> None:
    result = evaluate_interest_cap(
        InterestCapInput(
            contract_daily_rate_percent=Decimal("0.28"),
            regulatory_cap_daily_percent=FIXTURE_CAP,
            cap_source_citation="TEST_FIXTURE",
            principal_idr=Decimal("5000000"),
            tenor_days=60,
        )
    )
    assert result.is_within_cap is True
    assert result.excess_interest_idr == Decimal("0")


def test_graph_runs_all_nodes_within_max_steps() -> None:
    final = build_audit_graph().invoke(
        {
            "contract_id": "c1",
            "organization_id": "o1",
            "s3_key": "org_o1/x.pdf",
            "raw_text": "",
            "clauses": [],
            "findings": [],
            "step_count": 0,
            "status": "INIT",
        }
    )
    assert final["step_count"] == len(NODE_ORDER)
    assert final["status"] == NODE_ORDER[-1]


def test_graph_halts_when_max_steps_exceeded() -> None:
    with pytest.raises(MaxStepsExceededError):
        build_audit_graph().invoke(
            {
                "contract_id": "c1",
                "organization_id": "o1",
                "s3_key": "org_o1/x.pdf",
                "raw_text": "",
                "clauses": [],
                "findings": [],
                "step_count": 4,  # 4 + 4 nodes > MAX_STEPS=5
                "status": "INIT",
            }
        )

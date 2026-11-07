from decimal import ROUND_HALF_UP, Decimal
from pydantic import BaseModel, Field


class InterestCapInput(BaseModel):
    contract_daily_rate_percent: Decimal = Field(ge=0)
    regulatory_cap_daily_percent: Decimal = Field(ge=0)
    cap_source_citation: str = Field(
        min_length=1, description="Where the cap came from (verified)"
    )
    principal_idr: Decimal = Field(ge=0)
    tenor_days: int = Field(ge=1)


class InterestCapResult(BaseModel):
    is_within_cap: bool
    excess_daily_rate_percent: Decimal
    excess_interest_idr: Decimal
    cap_source_citation: str


def evaluate_interest_cap(data: InterestCapInput) -> InterestCapResult:
    excess_rate = max(
        Decimal(0), data.contract_daily_rate_percent - data.regulatory_cap_daily_percent
    )
    excess_idr = (
        data.principal_idr * excess_rate / Decimal(100) * data.tenor_days
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return InterestCapResult(
        is_within_cap=excess_rate == 0,
        excess_daily_rate_percent=excess_rate,
        excess_interest_idr=excess_idr,
        cap_source_citation=data.cap_source_citation,
    )

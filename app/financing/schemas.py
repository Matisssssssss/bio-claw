from __future__ import annotations

from pydantic import BaseModel


class FinancingEvent(BaseModel):
    event_type: str
    amount: float | None = None
    pricing: float | None = None
    discount_pct: float | None = None
    dilution_implication: float = 0.5
    runway_impact_quarters: float | None = None
    source_filing: str = ''
    confidence: float = 0.5


class FinancingRiskAssessment(BaseModel):
    raise_probability_6m: float
    pre_catalyst_raise_risk: float
    overhang_severity: float
    dilution_adjusted_attractiveness: float
    historical_behavior_score: float
    notes: list[str]

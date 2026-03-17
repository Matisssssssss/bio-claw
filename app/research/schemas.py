from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class CatalystType(str, Enum):
    PDUFA = 'pdufa'
    ADCOM = 'adcom'
    TOPLINE = 'topline'
    INTERIM = 'interim'
    FILING = 'filing'
    FINANCING = 'financing'
    CONFERENCE = 'conference'


class RiskBucket(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    EXTREME_BINARY = 'extreme_binary'


class CompanyOverview(BaseModel):
    ticker: str
    name: str
    market_cap: float | None = None
    enterprise_value: float | None = None
    cash_and_equivalents: float | None = None
    debt: float | None = None
    biotech_focus: str | None = None


class Catalyst(BaseModel):
    ticker: str
    type: CatalystType
    title: str
    event_date: date | None = None
    date_window_start: date | None = None
    date_window_end: date | None = None
    source: str
    confidence: float = 0.5


class TrialSignal(BaseModel):
    trial_id: str
    phase: str
    status: str
    primary_endpoint: str | None = None
    design: str | None = None
    readout_window: str | None = None


class FinancialSignal(BaseModel):
    cash: float | None = None
    quarterly_burn: float | None = None
    runway_quarters: float | None = None
    debt: float | None = None
    shelf_present: bool = False
    atm_present: bool = False
    dilution_risk_score: float = 0.5


class SentimentSignal(BaseModel):
    sentiment_score: float = 0.0
    volume_abnormality: float = 0.0
    headlines: List[str] = Field(default_factory=list)


class AgentOutput(BaseModel):
    agent_name: str
    ticker: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    payload: Dict[str, object] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    catalyst_score: float = 0
    market_score: float = 0
    financial_score: float = 0
    sentiment_score: float = 0
    insider_score: float = 0
    short_interest_score: float = 0
    science_score: float = 0
    competition_score: float = 0
    timing_score: float = 0
    risk_penalty: float = 0
    final_opportunity_score: float = 0
    confidence_score: float = 0
    data_completeness_score: float = 0
    catalyst_proximity_score: float = 0
    red_flag_count: int = 0
    explainability_trace: Dict[str, str] = Field(default_factory=dict)


class Dossier(BaseModel):
    company: CompanyOverview
    catalysts: List[Catalyst] = Field(default_factory=list)
    trials: List[TrialSignal] = Field(default_factory=list)
    financial: FinancialSignal = Field(default_factory=FinancialSignal)
    sentiment: SentimentSignal = Field(default_factory=SentimentSignal)
    bull_thesis: str = ''
    bear_thesis: str = ''
    neutral_committee_view: str = ''
    risk_bucket: RiskBucket = RiskBucket.HIGH
    score_breakdown: ScoreBreakdown = Field(default_factory=ScoreBreakdown)
    what_changed: List[str] = Field(default_factory=list)
    canonical_catalysts: List[Dict[str, object]] = Field(default_factory=list)
    clinical_assessment: List[Dict[str, object]] = Field(default_factory=list)
    financing_events: List[Dict[str, object]] = Field(default_factory=list)
    financing_risk: Dict[str, object] = Field(default_factory=dict)
    historical_analogs: List[Dict[str, object]] = Field(default_factory=list)
    archetype: Dict[str, object] = Field(default_factory=dict)
    entity_resolution: Dict[str, object] = Field(default_factory=dict)

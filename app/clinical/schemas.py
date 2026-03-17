from __future__ import annotations

from pydantic import BaseModel, Field


class TrialIntelligence(BaseModel):
    trial_id: str
    phase: str
    study_design: str | None = None
    randomized: bool | None = None
    masking: str | None = None
    comparator_arm: str | None = None
    control_type: str | None = None
    primary_endpoints: list[str] = Field(default_factory=list)
    secondary_endpoints: list[str] = Field(default_factory=list)
    enrollment_target: int | None = None
    actual_enrollment: int | None = None
    primary_completion_date: str | None = None
    full_completion_date: str | None = None
    results_posting_date: str | None = None
    sponsor: str | None = None
    collaborator: str | None = None
    status: str | None = None
    geography: str | None = None


class ClinicalAssessment(BaseModel):
    trial_id: str
    design_quality_score: float
    endpoint_quality_score: float
    interpretability_score: float
    ambiguity_risk: float
    regulatory_relevance: float
    data_maturity_score: float
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    confidence: float = 0.5
    likely_catalyst_window: str | None = None

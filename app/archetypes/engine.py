from __future__ import annotations

from pydantic import BaseModel


class ArchetypeResult(BaseModel):
    archetype: str
    risk_class: str
    holding_period_days: int
    catalyst_horizon_days: int
    sizing_hint: float
    rationale: list[str]


class ArchetypeEngine:
    def classify(self, dossier: dict) -> ArchetypeResult:
        score = dossier.get('score_breakdown', {}).get('final_opportunity_score', 0.0)
        risk = dossier.get('score_breakdown', {}).get('risk_penalty', 0.5)
        runway = dossier.get('financial', {}).get('runway_quarters') or 4
        catalyst_count = len(dossier.get('catalysts', []))

        if catalyst_count and risk > 0.6:
            return ArchetypeResult(archetype='pre-topline-binary', risk_class='high', holding_period_days=75, catalyst_horizon_days=90, sizing_hint=0.02, rationale=['Near-term binary catalyst', 'Elevated event risk'])
        if runway < 4:
            return ArchetypeResult(archetype='financing-overhang-rebound', risk_class='high', holding_period_days=45, catalyst_horizon_days=60, sizing_hint=0.015, rationale=['Tight runway', 'Potential financing reset'])
        if score > 0.55 and risk < 0.45:
            return ArchetypeResult(archetype='de-risked-post-data-continuation', risk_class='medium', holding_period_days=120, catalyst_horizon_days=150, sizing_hint=0.04, rationale=['Strong score with manageable risk'])
        return ArchetypeResult(archetype='broken-biotech-special-situation', risk_class='extreme', holding_period_days=30, catalyst_horizon_days=45, sizing_hint=0.01, rationale=['Defaulting to special-situation due to mixed evidence'])

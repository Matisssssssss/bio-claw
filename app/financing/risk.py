from __future__ import annotations

from app.financing.schemas import FinancingEvent, FinancingRiskAssessment


class FinancingRiskEngine:
    def assess(self, events: list[FinancingEvent], runway_quarters: float | None, catalyst_days: int | None = None) -> FinancingRiskAssessment:
        notes: list[str] = []
        overhang = 0.2 + sum(e.dilution_implication for e in events) / max(1, len(events)) if events else 0.2
        raise_prob = 0.2

        if runway_quarters is not None:
            if runway_quarters < 3:
                raise_prob += 0.5
                notes.append('Runway under 3 quarters implies near-term financing probability.')
            elif runway_quarters < 5:
                raise_prob += 0.3
        if any(e.event_type in {'atm', 'shelf_registration'} for e in events):
            overhang += 0.2
            raise_prob += 0.15
            notes.append('Shelf/ATM infrastructure enables opportunistic raises.')
        pre_cat = min(1.0, raise_prob + 0.15) if catalyst_days is not None and catalyst_days > 45 else min(1.0, raise_prob + 0.05)
        attractiveness = max(0.0, 1 - overhang * 0.7 - raise_prob * 0.4)

        return FinancingRiskAssessment(
            raise_probability_6m=min(1.0, raise_prob),
            pre_catalyst_raise_risk=pre_cat,
            overhang_severity=min(1.0, overhang),
            dilution_adjusted_attractiveness=attractiveness,
            historical_behavior_score=0.45 if len(events) >= 2 else 0.6,
            notes=notes,
        )

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class HistoricalSetup:
    setup_id: str
    catalyst_type: str
    market_cap_bucket: str
    phase: str
    modality: str
    short_interest: float
    runway_quarters: float
    sentiment: float
    dilution_risk: float
    outcome_return: float


class SimilarityEngine:
    def vectorize(self, setup: dict) -> list[float]:
        return [
            float(setup.get('short_interest', 0.15)),
            float(setup.get('runway_quarters', 4.0)) / 10,
            float(setup.get('sentiment', 0.0)),
            float(setup.get('dilution_risk', 0.5)),
        ]

    def _dist(self, a: list[float], b: list[float]) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

    def nearest(self, current: dict, history: list[HistoricalSetup], k: int = 3) -> list[dict]:
        cvec = self.vectorize(current)
        scored = []
        for h in history:
            hvec = self.vectorize(h.__dict__)
            d = self._dist(cvec, hvec)
            meta_bonus = 0.0
            if current.get('catalyst_type') == h.catalyst_type:
                meta_bonus -= 0.2
            if current.get('phase') == h.phase:
                meta_bonus -= 0.15
            scored.append((d + meta_bonus, h))
        top = sorted(scored, key=lambda x: x[0])[:k]
        return [
            {
                'setup_id': h.setup_id,
                'distance': round(dist, 4),
                'outcome_return': h.outcome_return,
                'catalyst_type': h.catalyst_type,
                'phase': h.phase,
            }
            for dist, h in top
        ]

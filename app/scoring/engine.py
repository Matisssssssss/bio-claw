from __future__ import annotations

from datetime import date, datetime

from app.config.settings import AppSettings
from app.research.schemas import ScoreBreakdown


class BiotechScoringEngine:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    def score(self, state: dict, strategy: str = 'pre-pdufa') -> ScoreBreakdown:
        w = self.settings.strategy_profiles[strategy]
        market = state.get('MarketDataAgent', {})
        financial = state.get('FinancialHealthAgent', {}).get('financial', {})
        news = state.get('NewsSentimentAgent', {})
        insider = state.get('InsiderAndFlowAgent', {})
        science = state.get('ScienceAndMechanismAgent', {})
        competition = state.get('CompetitiveLandscapeAgent', {})
        risk = state.get('CatalystRiskAgent', {})
        catalysts = state.get('RegulatoryCatalystAgent', {}).get('catalysts', [])

        catalyst_score = 0.7 if catalysts else 0.2
        market_score = min(1.0, max(0.0, 0.5 + market.get('price_change_30d', 0) + 0.2 * (market.get('rel_volume', 1) - 1)))
        financial_score = min(1.0, max(0.0, 0.8 - financial.get('dilution_risk_score', 0.5)))
        sentiment_score = min(1.0, max(0.0, 0.5 + news.get('sentiment_score', 0)))
        insider_score = insider.get('insider_score', 0.5)
        short_interest_score = 0.5
        science_score = science.get('science_score', 0.5)
        competition_score = 1.0 - (0.3 if competition.get('crowded') else 0.0)
        risk_penalty = risk.get('risk_score', 0.5)

        timing_score = 0.2
        if catalysts and catalysts[0].get('event_date'):
            event_date = date.fromisoformat(catalysts[0]['event_date'])
            days = (event_date - date.today()).days
            timing_score = max(0.0, min(1.0, 1 - abs(days - 45) / 90))

        final = (
            w.catalyst * catalyst_score
            + w.market * market_score
            + w.financial * financial_score
            + w.sentiment * sentiment_score
            + w.insider * insider_score
            + w.short_interest * short_interest_score
            + w.science * science_score
            + w.competition * competition_score
            + w.timing * timing_score
            - w.risk_penalty * risk_penalty
        )
        final = max(0.0, min(1.0, final))
        red_flags = len(risk.get('red_flags', []))
        completeness = sum(1 for k in ['MarketDataAgent', 'RegulatoryCatalystAgent', 'ClinicalTrialsAgent', 'FinancialHealthAgent', 'NewsSentimentAgent'] if state.get(k)) / 5

        return ScoreBreakdown(
            catalyst_score=catalyst_score,
            market_score=market_score,
            financial_score=financial_score,
            sentiment_score=sentiment_score,
            insider_score=insider_score,
            short_interest_score=short_interest_score,
            science_score=science_score,
            competition_score=competition_score,
            timing_score=timing_score,
            risk_penalty=risk_penalty,
            final_opportunity_score=final,
            confidence_score=max(0.2, completeness - red_flags * 0.1),
            data_completeness_score=completeness,
            catalyst_proximity_score=timing_score,
            red_flag_count=red_flags,
            explainability_trace={
                'formula': 'Weighted sum across domain factors minus risk penalty',
                'strategy': strategy,
                'generated_at': datetime.utcnow().isoformat(),
            },
        )

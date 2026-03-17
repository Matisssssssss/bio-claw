from __future__ import annotations

from typing import Any, Dict, Iterable

from app.agents.advanced import (
    ArchetypeAgent,
    CanonicalCatalystAgent,
    ChangeDetectionAgent,
    ClinicalAssessmentAgent,
    EntityResolutionAgent,
    FinancingRiskAgent,
    SimilarityAgent,
)
from app.agents.implementations import (
    BacktestAgent,
    CatalystRiskAgent,
    ClinicalTrialsAgent,
    CompetitiveLandscapeAgent,
    FinancialHealthAgent,
    InsiderAndFlowAgent,
    MarketDataAgent,
    MemoryAgent,
    NeutralInvestmentCommitteeAgent,
    NewsSentimentAgent,
    PortfolioConstructionAgent,
    RegulatoryCatalystAgent,
    ScienceAndMechanismAgent,
    ThesisBearAgent,
    ThesisBullAgent,
)
from app.config.settings import get_settings
from app.research.schemas import (
    Catalyst,
    CompanyOverview,
    Dossier,
    FinancialSignal,
    RiskBucket,
    SentimentSignal,
    TrialSignal,
)
from app.scoring.engine import BiotechScoringEngine


class BiotechResearchOrchestrator:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.scorer = BiotechScoringEngine(self.settings)
        self.pipeline = [
            MemoryAgent(),
            EntityResolutionAgent(),
            MarketDataAgent(),
            RegulatoryCatalystAgent(),
            CanonicalCatalystAgent(),
            ClinicalTrialsAgent(),
            ClinicalAssessmentAgent(),
            FinancialHealthAgent(),
            FinancingRiskAgent(),
            InsiderAndFlowAgent(),
            NewsSentimentAgent(),
            CompetitiveLandscapeAgent(),
            SimilarityAgent(),
            ScienceAndMechanismAgent(),
            CatalystRiskAgent(),
            ThesisBullAgent(),
            ThesisBearAgent(),
            NeutralInvestmentCommitteeAgent(),
            PortfolioConstructionAgent(),
            BacktestAgent(),
        ]

    def run_ticker(self, ticker: str, strategy: str = 'pre-pdufa') -> Dossier:
        state: Dict[str, Any] = {}
        for agent in self.pipeline:
            output = agent.run(ticker, state)
            state[output.agent_name] = output.payload
        score = self.scorer.score(state, strategy=strategy)
        state['score_breakdown'] = score.model_dump()
        state['ArchetypeAgent'] = ArchetypeAgent().run(ticker, state).payload
        state['ChangeDetectionAgent'] = ChangeDetectionAgent().run(ticker, state).payload

        company = CompanyOverview(
            ticker=ticker,
            name=f'{ticker} Biopharma',
            market_cap=state['MarketDataAgent'].get('market_cap'),
            enterprise_value=state['MarketDataAgent'].get('enterprise_value'),
            cash_and_equivalents=state['FinancialHealthAgent']['financial'].get('cash'),
            debt=state['FinancialHealthAgent']['financial'].get('debt'),
            biotech_focus='Oncology and rare disease pipeline',
        )
        catalysts = [Catalyst.model_validate(c) for c in state['RegulatoryCatalystAgent'].get('catalysts', [])]
        trials = [TrialSignal.model_validate(t) for t in state['ClinicalTrialsAgent'].get('trials', [])]
        financial = FinancialSignal.model_validate(state['FinancialHealthAgent']['financial'])
        sentiment = SentimentSignal(
            sentiment_score=state['NewsSentimentAgent']['sentiment_score'],
            volume_abnormality=state['NewsSentimentAgent']['abnormality'],
            headlines=[x['headline'] for x in state['NewsSentimentAgent']['news']],
        )

        return Dossier(
            company=company,
            catalysts=catalysts,
            trials=trials,
            financial=financial,
            sentiment=sentiment,
            bull_thesis=state['ThesisBullAgent']['bull_thesis'],
            bear_thesis=state['ThesisBearAgent']['bear_thesis'],
            neutral_committee_view=state['NeutralInvestmentCommitteeAgent']['committee_view'],
            risk_bucket=RiskBucket.EXTREME_BINARY if score.risk_penalty > 0.7 else RiskBucket.HIGH,
            score_breakdown=score,
            what_changed=[x['message'] for x in state['ChangeDetectionAgent']['changes']],
            canonical_catalysts=state['CanonicalCatalystAgent']['canonical_catalysts'],
            clinical_assessment=state['ClinicalAssessmentAgent']['clinical_assessments'],
            financing_events=state['FinancingRiskAgent']['financing_events'],
            financing_risk=state['FinancingRiskAgent']['financing_risk'],
            historical_analogs=state['SimilarityAgent']['similar_setups'],
            archetype=state['ArchetypeAgent']['archetype'],
            entity_resolution=state['EntityResolutionAgent']['resolution'],
        )

    def scan_watchlist(self, tickers: Iterable[str], strategy: str = 'pre-pdufa') -> list[Dossier]:
        return [self.run_ticker(ticker, strategy=strategy) for ticker in tickers]

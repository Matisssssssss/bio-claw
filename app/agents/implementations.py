from __future__ import annotations

from datetime import datetime
from statistics import mean
from typing import Any, Dict

from app.agents.base import ResearchAgent
from app.clients.providers import (
    MockClinicalTrialsClient,
    MockFilingClient,
    MockInsiderClient,
    MockMarketDataClient,
    MockNewsClient,
    MockRegulatoryClient,
)
from app.parsers.filings import parse_financial_health
from app.research.schemas import AgentOutput


class MarketDataAgent(ResearchAgent):
    name = 'MarketDataAgent'

    def __init__(self) -> None:
        self.client = MockMarketDataClient()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        snap = self.client.get_snapshot(ticker)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload=snap)


class RegulatoryCatalystAgent(ResearchAgent):
    name = 'RegulatoryCatalystAgent'

    def __init__(self) -> None:
        self.client = MockRegulatoryClient()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'catalysts': self.client.get_catalysts(ticker)})


class ClinicalTrialsAgent(ResearchAgent):
    name = 'ClinicalTrialsAgent'

    def __init__(self) -> None:
        self.client = MockClinicalTrialsClient()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'trials': self.client.get_trials(ticker)})


class FinancialHealthAgent(ResearchAgent):
    name = 'FinancialHealthAgent'

    def __init__(self) -> None:
        self.client = MockFilingClient()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        filings = self.client.get_filings(ticker)
        financial = parse_financial_health(filings)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'financial': financial.model_dump(), 'filings': filings})


class InsiderAndFlowAgent(ResearchAgent):
    name = 'InsiderAndFlowAgent'

    def __init__(self) -> None:
        self.client = MockInsiderClient()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        tx = self.client.get_insider_transactions(ticker)
        buys = sum(t['shares'] for t in tx if t['action'] == 'buy')
        sells = sum(t['shares'] for t in tx if t['action'] == 'sell')
        insider_score = max(0.0, min(1.0, 0.5 + (buys - sells) / 100_000))
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'transactions': tx, 'insider_score': insider_score})


class NewsSentimentAgent(ResearchAgent):
    name = 'NewsSentimentAgent'

    def __init__(self) -> None:
        self.client = MockNewsClient()

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        items = self.client.get_news(ticker)
        score = mean([x['sentiment'] for x in items]) if items else 0.0
        abnormality = abs(score) * len(items)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'news': items, 'sentiment_score': score, 'abnormality': abnormality})


class CompetitiveLandscapeAgent(ResearchAgent):
    name = 'CompetitiveLandscapeAgent'

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'peer_count': 6, 'soc_strength': 0.7, 'crowded': True})


class ScienceAndMechanismAgent(ResearchAgent):
    name = 'ScienceAndMechanismAgent'

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'moa': 'Targeted kinase inhibitor', 'validation': 'moderate', 'science_score': 0.64})


class CatalystRiskAgent(ResearchAgent):
    name = 'CatalystRiskAgent'

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        red_flags = []
        fin = state.get('FinancialHealthAgent', {}).get('financial', {})
        if fin.get('runway_quarters') is not None and fin.get('runway_quarters', 10) < 4:
            red_flags.append('Short cash runway')
        if fin.get('atm_present'):
            red_flags.append('ATM overhang risk')
        risk_score = min(1.0, 0.3 + 0.2 * len(red_flags))
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'risk_score': risk_score, 'red_flags': red_flags})


class ThesisBullAgent(ResearchAgent):
    name = 'ThesisBullAgent'

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        thesis = 'Near-term catalyst, credible MoA, and positive insider skew support upside optionality.'
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'bull_thesis': thesis})


class ThesisBearAgent(ResearchAgent):
    name = 'ThesisBearAgent'

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        thesis = 'Binary clinical risk plus financing overhang can cap upside and amplify drawdowns.'
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'bear_thesis': thesis})


class NeutralInvestmentCommitteeAgent(ResearchAgent):
    name = 'NeutralInvestmentCommitteeAgent'

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        sentiment = state.get('NewsSentimentAgent', {}).get('sentiment_score', 0)
        risk = state.get('CatalystRiskAgent', {}).get('risk_score', 0.5)
        action = 'watch' if sentiment > -0.1 and risk < 0.7 else 'speculative'
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'committee_view': f'Balanced setup; action bucket: {action}.', 'action_bucket': action})


class PortfolioConstructionAgent(ResearchAgent):
    name = 'PortfolioConstructionAgent'

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        risk = state.get('CatalystRiskAgent', {}).get('risk_score', 0.5)
        size = max(0.01, 0.06 - 0.04 * risk)
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'target_weight': round(size, 4)})


class MemoryAgent(ResearchAgent):
    name = 'MemoryAgent'

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'what_changed': ['No prior run found; baseline created.'], 'timestamp': datetime.utcnow().isoformat(), 'previous_snapshot': None})


class BacktestAgent(ResearchAgent):
    name = 'BacktestAgent'

    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        return AgentOutput(agent_name=self.name, ticker=ticker, payload={'historical_similarity_score': 0.58, 'avg_tminus30_to_tminus1': 0.12})

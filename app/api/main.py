from __future__ import annotations

from fastapi import FastAPI

from app.alerts.engine import generate_alerts
from app.archetypes.engine import ArchetypeEngine
from app.backtesting.engine import BacktestEngine
from app.catalysts.engine import CanonicalCatalystEngine
from app.portfolio.construction import build_portfolio
from app.openclaw.api import router as openclaw_router
from app.research.orchestrator import BiotechResearchOrchestrator
from app.similarity.engine import HistoricalSetup, SimilarityEngine

api = FastAPI(title='Biotech Scout API', version='0.2.0')
orch = BiotechResearchOrchestrator()


@api.get('/health')
def health() -> dict:
    return {'status': 'ok'}


@api.get('/companies/{ticker}')
def company(ticker: str) -> dict:
    d = orch.run_ticker(ticker.upper())
    return d.company.model_dump()


@api.get('/companies/{ticker}/dossier')
def company_dossier(ticker: str) -> dict:
    return orch.run_ticker(ticker.upper()).model_dump(mode='json')


@api.get('/companies/{ticker}/scores')
def company_scores(ticker: str) -> dict:
    return orch.run_ticker(ticker.upper()).score_breakdown.model_dump()


@api.get('/companies/{ticker}/changes')
def company_changes(ticker: str) -> list[str]:
    return orch.run_ticker(ticker.upper()).what_changed


@api.get('/companies/{ticker}/peers')
def peers(ticker: str) -> dict:
    d = orch.run_ticker(ticker.upper())
    return {'ticker': ticker.upper(), 'crowding': d.score_breakdown.competition_score, 'peer_summary': d.historical_analogs}


@api.get('/catalysts/upcoming')
def catalysts(days: int = 30) -> list[dict]:
    d = orch.run_ticker('XBI')
    return [c.model_dump(mode='json') for c in d.catalysts]


@api.get('/catalysts/canonical/{ticker}')
def canonical_catalysts(ticker: str) -> list[dict]:
    return orch.run_ticker(ticker.upper()).canonical_catalysts


@api.get('/financing/{ticker}')
def financing(ticker: str) -> dict:
    d = orch.run_ticker(ticker.upper())
    return {'events': d.financing_events, 'risk': d.financing_risk}


@api.get('/watchlists/{name}')
def watchlist(name: str) -> dict:
    tickers = ['NBIX', 'SRPT', 'ALNY']
    return {'name': name, 'tickers': tickers}


@api.post('/scan/universe')
def scan_universe() -> list[dict]:
    return [x.model_dump(mode='json') for x in orch.scan_watchlist(['NBIX', 'SRPT', 'ALNY'])]


@api.post('/research/{ticker}')
def run_research(ticker: str) -> dict:
    return orch.run_ticker(ticker.upper()).model_dump(mode='json')


@api.get('/event-studies/{type}')
def event_study(type: str) -> dict:
    return BacktestEngine().run_strategy_backtest(type, [0.05, -0.03, 0.1, 0.02])


@api.get('/similarity/{ticker}')
def similarity(ticker: str) -> list[dict]:
    d = orch.run_ticker(ticker.upper())
    return d.historical_analogs


@api.get('/archetypes/{ticker}')
def archetypes(ticker: str) -> dict:
    d = orch.run_ticker(ticker.upper())
    return d.archetype


@api.get('/portfolio/suggestions')
def portfolio_suggestions() -> list[dict]:
    dossiers = orch.scan_watchlist(['NBIX', 'SRPT', 'ALNY'])
    ideas = [{'ticker': d.company.ticker, 'score': d.score_breakdown.final_opportunity_score, 'archetype': d.archetype.get('archetype', ''), 'liquidity_score': 0.7} for d in dossiers]
    return build_portfolio(ideas)


@api.get('/alerts')
def alerts() -> list[str]:
    return generate_alerts(orch.run_ticker('NBIX'))


@api.get('/strategies')
def strategies() -> list[str]:
    return list(orch.settings.strategy_profiles.keys())


api.include_router(openclaw_router)

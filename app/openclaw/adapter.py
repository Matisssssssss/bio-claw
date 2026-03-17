from __future__ import annotations

from app.openclaw.registry import OpenClawToolRegistry
from app.openclaw.schemas import OpenClawToolSpec
from app.portfolio.construction import build_portfolio
from app.research.orchestrator import BiotechResearchOrchestrator


class OpenClawAdapter:
    def __init__(self) -> None:
        self.orch = BiotechResearchOrchestrator()
        self.registry = OpenClawToolRegistry()
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        self.registry.register(
            OpenClawToolSpec(
                name='biotech.research_ticker',
                description='Run full biotech research dossier for a ticker',
                input_schema={
                    'type': 'object',
                    'properties': {'ticker': {'type': 'string'}, 'strategy': {'type': 'string'}},
                    'required': ['ticker'],
                },
            ),
            self._research_ticker,
        )
        self.registry.register(
            OpenClawToolSpec(
                name='biotech.canonical_catalysts',
                description='Return canonical catalysts for a ticker',
                input_schema={
                    'type': 'object',
                    'properties': {'ticker': {'type': 'string'}},
                    'required': ['ticker'],
                },
            ),
            self._canonical_catalysts,
        )
        self.registry.register(
            OpenClawToolSpec(
                name='biotech.changes',
                description='Return what-changed summary for a ticker',
                input_schema={
                    'type': 'object',
                    'properties': {'ticker': {'type': 'string'}},
                    'required': ['ticker'],
                },
            ),
            self._changes,
        )
        self.registry.register(
            OpenClawToolSpec(
                name='biotech.similarity',
                description='Return historical analogs for a ticker setup',
                input_schema={
                    'type': 'object',
                    'properties': {'ticker': {'type': 'string'}},
                    'required': ['ticker'],
                },
            ),
            self._similarity,
        )
        self.registry.register(
            OpenClawToolSpec(
                name='biotech.portfolio_suggestions',
                description='Build portfolio suggestions from a watchlist',
                input_schema={
                    'type': 'object',
                    'properties': {'tickers': {'type': 'array', 'items': {'type': 'string'}}},
                    'required': ['tickers'],
                },
            ),
            self._portfolio,
        )

    def _research_ticker(self, args: dict) -> dict:
        ticker = str(args['ticker']).upper()
        strategy = str(args.get('strategy', 'pre-pdufa'))
        dossier = self.orch.run_ticker(ticker, strategy=strategy)
        return {'ticker': ticker, 'dossier': dossier.model_dump(mode='json')}

    def _canonical_catalysts(self, args: dict) -> dict:
        ticker = str(args['ticker']).upper()
        dossier = self.orch.run_ticker(ticker)
        return {'ticker': ticker, 'canonical_catalysts': dossier.canonical_catalysts}

    def _changes(self, args: dict) -> dict:
        ticker = str(args['ticker']).upper()
        dossier = self.orch.run_ticker(ticker)
        return {'ticker': ticker, 'changes': dossier.what_changed}

    def _similarity(self, args: dict) -> dict:
        ticker = str(args['ticker']).upper()
        dossier = self.orch.run_ticker(ticker)
        return {'ticker': ticker, 'analogs': dossier.historical_analogs}

    def _portfolio(self, args: dict) -> dict:
        tickers = [str(x).upper() for x in args['tickers']]
        dossiers = self.orch.scan_watchlist(tickers)
        ideas = [
            {
                'ticker': d.company.ticker,
                'score': d.score_breakdown.final_opportunity_score,
                'archetype': d.archetype.get('archetype', ''),
                'liquidity_score': 0.7,
            }
            for d in dossiers
        ]
        return {'portfolio': build_portfolio(ideas)}

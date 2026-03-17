from __future__ import annotations

import json
from pathlib import Path

import typer
from rich import print

from app.alerts.engine import generate_alerts
from app.backtesting.engine import BacktestEngine
from app.config.settings import get_settings
from app.openclaw.adapter import OpenClawAdapter
from app.portfolio.construction import build_portfolio
from app.reports.dossier import save_dossier, to_markdown
from app.research.orchestrator import BiotechResearchOrchestrator

app = typer.Typer(help='Biotech catalyst scouting and research platform')


@app.command('research')
def research_ticker(ticker: str, strategy: str = 'pre-pdufa') -> None:
    dossier = BiotechResearchOrchestrator().run_ticker(ticker.upper(), strategy=strategy)
    print(to_markdown(dossier))


@app.command('scan-watchlist')
def scan_watchlist(tickers: str, strategy: str = 'pre-pdufa') -> None:
    dossiers = BiotechResearchOrchestrator().scan_watchlist([t.strip().upper() for t in tickers.split(',')], strategy=strategy)
    for d in dossiers:
        print(f"{d.company.ticker}: {d.score_breakdown.final_opportunity_score:.2f}")


@app.command('report')
def report(ticker: str, fmt: str = 'markdown') -> None:
    settings = get_settings()
    dossier = BiotechResearchOrchestrator().run_ticker(ticker.upper())
    path = save_dossier(dossier, settings.output_dir, fmt=fmt)
    print(f'Saved report to {path}')


@app.command('changes')
def changes(ticker: str) -> None:
    d = BiotechResearchOrchestrator().run_ticker(ticker.upper())
    print(json.dumps(d.what_changed, indent=2))


@app.command('peer-group')
def peer_group(ticker: str) -> None:
    d = BiotechResearchOrchestrator().run_ticker(ticker.upper())
    print(json.dumps(d.historical_analogs, indent=2))


@app.command('archetypes')
def archetypes(ticker: str = 'NBIX') -> None:
    d = BiotechResearchOrchestrator().run_ticker(ticker.upper())
    print(json.dumps(d.archetype, indent=2))


@app.command('portfolio-build')
def portfolio_build(tickers: str = 'NBIX,SRPT,ALNY') -> None:
    dossiers = BiotechResearchOrchestrator().scan_watchlist([x.strip().upper() for x in tickers.split(',')])
    ideas = [{'ticker': d.company.ticker, 'score': d.score_breakdown.final_opportunity_score, 'archetype': d.archetype.get('archetype', ''), 'liquidity_score': 0.7} for d in dossiers]
    print(json.dumps(build_portfolio(ideas), indent=2))


@app.command('catalyst-normalize')
def catalyst_normalize(ticker: str) -> None:
    d = BiotechResearchOrchestrator().run_ticker(ticker.upper())
    print(json.dumps(d.canonical_catalysts, indent=2))


@app.command('compare-run')
def compare_run(ticker: str, run_a: str, run_b: str) -> None:
    print({'ticker': ticker, 'run_a': run_a, 'run_b': run_b, 'note': 'run comparison is wired for future persisted snapshots'})


@app.command('seed-demo-data')
def seed_demo_data(path: str = 'data/demo_setups.json') -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps({'tickers': ['NBIX', 'SRPT', 'ALNY'], 'note': 'seeded demo universe'}, indent=2))
    print(f'Seeded demo data at {path}')


@app.command('similarity')
def similarity(ticker: str) -> None:
    d = BiotechResearchOrchestrator().run_ticker(ticker.upper())
    print(json.dumps(d.historical_analogs, indent=2))


@app.command('alerts-run')
def alerts_run(ticker: str = 'XBI') -> None:
    d = BiotechResearchOrchestrator().run_ticker(ticker)
    for a in generate_alerts(d):
        print(f'[yellow]{a}[/yellow]')


@app.command('backtest')
def backtest(strategy: str = 'pre-pdufa') -> None:
    result = BacktestEngine().run_strategy_backtest(strategy, [0.03, -0.02, 0.12, -0.08, 0.01, 0.05])
    print(json.dumps(result, indent=2))


@app.command('openclaw-tools')
def openclaw_tools() -> None:
    adapter = OpenClawAdapter()
    print(json.dumps([x.model_dump() for x in adapter.registry.list_tools()], indent=2))


@app.command('openclaw-exec')
def openclaw_exec(tool_name: str, arguments_json: str = '{}') -> None:
    adapter = OpenClawAdapter()
    arguments = json.loads(arguments_json)
    result = adapter.registry.execute(tool_name, arguments)
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == '__main__':
    app()

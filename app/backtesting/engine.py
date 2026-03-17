from __future__ import annotations

from typing import Iterable

from app.event_studies.analytics import summarize_event_window


class BacktestEngine:
    def run_strategy_backtest(self, strategy: str, event_returns: Iterable[float]) -> dict:
        summary = summarize_event_window(event_returns)
        summary['strategy'] = strategy
        summary['sample_size'] = len(list(event_returns)) if not isinstance(event_returns, list) else len(event_returns)
        return summary

from __future__ import annotations

from typing import Protocol


class MarketDataProvider(Protocol):
    def get_snapshot(self, ticker: str) -> dict: ...


class RegulatoryProvider(Protocol):
    def get_catalysts(self, ticker: str) -> list[dict]: ...


class ClinicalTrialsProvider(Protocol):
    def get_trials(self, ticker: str) -> list[dict]: ...


class FilingProvider(Protocol):
    def get_filings(self, ticker: str) -> list[dict]: ...


class NewsProvider(Protocol):
    def get_news(self, ticker: str) -> list[dict]: ...


class InsiderProvider(Protocol):
    def get_insider_transactions(self, ticker: str) -> list[dict]: ...

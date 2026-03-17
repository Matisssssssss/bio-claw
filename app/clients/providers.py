from __future__ import annotations

from datetime import date, timedelta


class MockMarketDataClient:
    def get_snapshot(self, ticker: str) -> dict:
        return {
            'ticker': ticker,
            'market_cap': 1_500_000_000,
            'enterprise_value': 1_200_000_000,
            'avg_volume': 2_100_000,
            'rel_volume': 1.8,
            'float': 125_000_000,
            'volatility_30d': 0.62,
            'price_change_30d': -0.11,
        }


class MockRegulatoryClient:
    def get_catalysts(self, ticker: str) -> list[dict]:
        return [
            {
                'ticker': ticker,
                'type': 'pdufa',
                'title': 'PDUFA date for lead asset',
                'event_date': str(date.today() + timedelta(days=55)),
                'source': 'mock-regulatory',
                'confidence': 0.8,
            }
        ]


class MockClinicalTrialsClient:
    def get_trials(self, ticker: str) -> list[dict]:
        return [
            {
                'trial_id': f'NCT-{ticker}-001',
                'phase': 'Phase 3',
                'status': 'Active, not recruiting',
                'primary_endpoint': 'Progression-free survival',
                'design': 'Randomized, double-blind',
                'readout_window': 'Q4 2026',
            }
        ]


class MockFilingClient:
    def get_filings(self, ticker: str) -> list[dict]:
        return [
            {'form': '10-Q', 'cash': 320_000_000, 'burn': 55_000_000, 'debt': 25_000_000},
            {'form': 'S-3', 'shelf': True},
            {'form': '8-K', 'atm': True},
        ]


class MockNewsClient:
    def get_news(self, ticker: str) -> list[dict]:
        return [
            {'headline': f'{ticker} announces conference presentation', 'sentiment': 0.2},
            {'headline': f'{ticker} trial update shows manageable safety', 'sentiment': 0.4},
            {'headline': f'Analyst cautious on {ticker} valuation', 'sentiment': -0.3},
        ]


class MockInsiderClient:
    def get_insider_transactions(self, ticker: str) -> list[dict]:
        return [
            {'insider': 'CEO', 'action': 'buy', 'shares': 25_000},
            {'insider': 'CFO', 'action': 'sell', 'shares': 5_000},
        ]

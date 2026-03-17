from __future__ import annotations

from app.research.schemas import FinancialSignal


def parse_financial_health(filings: list[dict]) -> FinancialSignal:
    cash = None
    burn = None
    debt = None
    shelf = False
    atm = False

    for filing in filings:
        cash = filing.get('cash', cash)
        burn = filing.get('burn', burn)
        debt = filing.get('debt', debt)
        shelf = shelf or bool(filing.get('shelf', False))
        atm = atm or bool(filing.get('atm', False))

    runway = (cash / burn) if (cash and burn and burn > 0) else None
    dilution = 0.25
    if shelf:
        dilution += 0.3
    if atm:
        dilution += 0.3
    if runway is not None and runway < 4:
        dilution += 0.2

    return FinancialSignal(
        cash=cash,
        quarterly_burn=burn,
        runway_quarters=runway,
        debt=debt,
        shelf_present=shelf,
        atm_present=atm,
        dilution_risk_score=min(1.0, dilution),
    )

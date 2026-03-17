from app.parsers.filings import parse_financial_health


def test_runway_and_dilution_detection() -> None:
    filings = [
        {'form': '10-Q', 'cash': 200.0, 'burn': 60.0, 'debt': 10.0},
        {'form': 'S-3', 'shelf': True},
        {'form': '8-K', 'atm': True},
    ]
    fs = parse_financial_health(filings)
    assert fs.runway_quarters is not None
    assert fs.shelf_present is True
    assert fs.atm_present is True
    assert fs.dilution_risk_score > 0.7

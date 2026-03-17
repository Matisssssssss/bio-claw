from app.financing.parser import FilingFinancingParser


def test_financing_event_extraction() -> None:
    parser = FilingFinancingParser()
    events = parser.parse_text('Company filed Form S-3 shelf registration for $200 million and launched ATM.', 'S-3')
    types = {e.event_type for e in events}
    assert 'shelf_registration' in types
    assert 'atm' in types

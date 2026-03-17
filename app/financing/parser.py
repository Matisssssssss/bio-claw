from __future__ import annotations

import re

from app.financing.schemas import FinancingEvent

_AMOUNT_RE = re.compile(r'\$([0-9]+(?:\.[0-9]+)?)\s*(million|billion)', re.IGNORECASE)


class FilingFinancingParser:
    def parse_text(self, filing_text: str, source_filing: str) -> list[FinancingEvent]:
        text = filing_text.lower()
        out: list[FinancingEvent] = []
        amount = None
        m = _AMOUNT_RE.search(filing_text)
        if m:
            amount = float(m.group(1)) * (1_000_000 if m.group(2).lower() == 'million' else 1_000_000_000)

        if 'at-the-market' in text or 'atm' in text:
            out.append(FinancingEvent(event_type='atm', amount=amount, dilution_implication=0.75, source_filing=source_filing, confidence=0.8))
        if 'shelf registration' in text or 'form s-3' in text:
            out.append(FinancingEvent(event_type='shelf_registration', amount=amount, dilution_implication=0.65, source_filing=source_filing, confidence=0.85))
        if 'convertible notes' in text:
            out.append(FinancingEvent(event_type='convertible_debt', amount=amount, dilution_implication=0.6, source_filing=source_filing, confidence=0.8))
        if 'warrant' in text:
            out.append(FinancingEvent(event_type='warrants', amount=amount, dilution_implication=0.7, source_filing=source_filing, confidence=0.7))
        if 'public offering' in text or 'follow-on' in text:
            out.append(FinancingEvent(event_type='follow_on', amount=amount, dilution_implication=0.8, source_filing=source_filing, confidence=0.75))
        if 'royalty financing' in text:
            out.append(FinancingEvent(event_type='royalty_financing', amount=amount, dilution_implication=0.3, source_filing=source_filing, confidence=0.65))
        return out

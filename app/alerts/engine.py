from __future__ import annotations

from datetime import date

from app.research.schemas import Dossier


def generate_alerts(dossier: Dossier, days: int = 30) -> list[str]:
    alerts: list[str] = []
    for c in dossier.catalysts:
        if c.event_date and 0 <= (c.event_date - date.today()).days <= days:
            alerts.append(f"Catalyst approaching: {c.title} on {c.event_date}")
    if dossier.financial.dilution_risk_score > 0.7:
        alerts.append('High dilution risk detected')
    if dossier.sentiment.volume_abnormality > 1.5:
        alerts.append('News/sentiment shock detected')
    return alerts

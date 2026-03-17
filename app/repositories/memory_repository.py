from __future__ import annotations

from sqlalchemy import select

from app.storage.database import SessionLocal
from app.storage.models import ResearchDossierModel


class MemoryRepository:
    def save_snapshot(self, ticker: str, run_id: str, dossier_json: dict) -> None:
        with SessionLocal() as db:
            db.add(ResearchDossierModel(ticker=ticker, run_id=run_id, dossier_json=dossier_json))
            db.commit()

    def latest_snapshot(self, ticker: str) -> dict | None:
        with SessionLocal() as db:
            stmt = select(ResearchDossierModel).where(ResearchDossierModel.ticker == ticker).order_by(ResearchDossierModel.id.desc())
            row = db.execute(stmt).scalars().first()
            return row.dossier_json if row else None

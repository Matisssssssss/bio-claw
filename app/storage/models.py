from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = 'companies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, default='')
    ticker: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    cik: Mapped[str | None] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(255))
    biotech_focus: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AliasMap(Base):
    __tablename__ = 'alias_map'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(32), index=True)
    entity_id: Mapped[str] = mapped_column(String(64), index=True)
    alias: Mapped[str] = mapped_column(String(255), index=True)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)


class AssetModel(Base):
    __tablename__ = 'assets'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    company_id: Mapped[str] = mapped_column(String(64), index=True)
    canonical_name: Mapped[str] = mapped_column(String(255), index=True)
    modality: Mapped[str | None] = mapped_column(String(64))
    target: Mapped[str | None] = mapped_column(String(255))


class IndicationModel(Base):
    __tablename__ = 'indications'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    indication_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)


class CanonicalCatalystModel(Base):
    __tablename__ = 'canonical_catalysts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    catalyst_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    company_id: Mapped[str | None] = mapped_column(String(64), index=True)
    asset_id: Mapped[str | None] = mapped_column(String(64), index=True)
    indication_id: Mapped[str | None] = mapped_column(String(64), index=True)
    catalyst_type: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    event_date: Mapped[datetime | None] = mapped_column(DateTime)
    event_window_start: Mapped[datetime | None] = mapped_column(DateTime)
    event_window_end: Mapped[datetime | None] = mapped_column(DateTime)
    source_records_json: Mapped[dict] = mapped_column(JSON, default={})
    latest_updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class FinancingEventModel(Base):
    __tablename__ = 'financing_events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(16), index=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    amount: Mapped[float | None] = mapped_column(Float)
    dilution_implication: Mapped[float] = mapped_column(Float, default=0.5)
    source_filing: Mapped[str] = mapped_column(String(64))
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class FinancialSnapshot(Base):
    __tablename__ = 'financial_snapshots'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(16), index=True)
    cash: Mapped[float | None] = mapped_column(Float)
    burn: Mapped[float | None] = mapped_column(Float)
    runway_quarters: Mapped[float | None] = mapped_column(Float)
    shelf_present: Mapped[bool] = mapped_column(Boolean, default=False)
    atm_present: Mapped[bool] = mapped_column(Boolean, default=False)
    as_of: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ResearchDossierModel(Base):
    __tablename__ = 'research_dossiers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(16), index=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True, default='')
    dossier_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ScoreModel(Base):
    __tablename__ = 'scores'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(16), index=True)
    score_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RunHistory(Base):
    __tablename__ = 'run_history'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, default='')
    run_type: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class CatalystStatus(str, Enum):
    EXPECTED = 'expected'
    CONFIRMED = 'confirmed'
    INFERRED = 'inferred'
    HISTORICAL = 'historical'
    NEGATIVE = 'negative'


class DatePrecision(str, Enum):
    EXACT = 'exact'
    MONTH = 'month'
    QUARTER = 'quarter'
    VAGUE = 'vague'


class CatalystSourceRecord(BaseModel):
    source: str
    source_id: str
    observed_at: datetime = Field(default_factory=datetime.utcnow)
    raw_title: str


class CanonicalCatalyst(BaseModel):
    catalyst_id: str
    company_id: str | None = None
    asset_id: str | None = None
    indication_id: str | None = None
    catalyst_type: str
    source_records: list[CatalystSourceRecord] = Field(default_factory=list)
    earliest_seen_at: datetime = Field(default_factory=datetime.utcnow)
    latest_updated_at: datetime = Field(default_factory=datetime.utcnow)
    event_date: date | None = None
    event_window_start: date | None = None
    event_window_end: date | None = None
    date_precision: DatePrecision = DatePrecision.VAGUE
    confidence: float = 0.5
    status: CatalystStatus = CatalystStatus.EXPECTED
    evidence_links: list[str] = Field(default_factory=list)


class CatalystChange(BaseModel):
    catalyst_id: str
    change_type: str
    old_value: str | None = None
    new_value: str | None = None

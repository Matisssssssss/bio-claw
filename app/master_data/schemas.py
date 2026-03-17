from __future__ import annotations

from pydantic import BaseModel, Field


class AliasRecord(BaseModel):
    alias: str
    canonical: str
    entity_type: str
    confidence: float = 1.0


class CompanyMaster(BaseModel):
    company_id: str
    ticker: str
    cik: str | None = None
    name: str
    aliases: list[str] = Field(default_factory=list)


class AssetMaster(BaseModel):
    asset_id: str
    company_id: str
    canonical_name: str
    aliases: list[str] = Field(default_factory=list)
    target: str | None = None
    modality: str | None = None


class IndicationMaster(BaseModel):
    indication_id: str
    name: str
    aliases: list[str] = Field(default_factory=list)


class EntityResolutionResult(BaseModel):
    company: CompanyMaster | None = None
    asset: AssetMaster | None = None
    indication: IndicationMaster | None = None
    trial_id: str | None = None
    match_confidence: float = 0.0
    notes: list[str] = Field(default_factory=list)

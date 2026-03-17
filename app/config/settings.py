from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class StrategyWeights(BaseModel):
    catalyst: float = 0.2
    market: float = 0.1
    financial: float = 0.15
    sentiment: float = 0.1
    insider: float = 0.1
    short_interest: float = 0.05
    science: float = 0.15
    competition: float = 0.05
    timing: float = 0.1
    risk_penalty: float = 0.15


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__', extra='ignore')

    app_name: str = 'biotech-scout'
    database_url: str = 'sqlite:///./biotech_scout.db'
    default_universe: List[str] = Field(default_factory=lambda: ["XBI", "IBB"])
    cache_ttl_seconds: int = 900
    log_level: str = 'INFO'

    finnhub_api_key: str | None = None
    polygon_api_key: str | None = None
    alpha_vantage_api_key: str | None = None
    news_api_key: str | None = None

    strategy_profiles: Dict[str, StrategyWeights] = Field(
        default_factory=lambda: {
            "pre-pdufa": StrategyWeights(catalyst=0.28, timing=0.16, risk_penalty=0.18),
            "pre-topline-binary": StrategyWeights(catalyst=0.24, science=0.2, risk_penalty=0.2),
            "post-selloff-recovery": StrategyWeights(financial=0.22, sentiment=0.15, risk_penalty=0.12),
            "financing-overhang-rebound": StrategyWeights(financial=0.3, sentiment=0.12, timing=0.12),
            "momentum-into-catalyst": StrategyWeights(market=0.22, catalyst=0.22, timing=0.2),
            "deep-value-biotech-special-situation": StrategyWeights(financial=0.3, science=0.2, catalyst=0.16),
        }
    )

    output_dir: Path = Path('outputs')


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()

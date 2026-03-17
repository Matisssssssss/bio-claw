from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class OpenClawToolSpec(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any] = Field(default_factory=dict)


class OpenClawToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class OpenClawToolResult(BaseModel):
    tool_name: str
    ok: bool
    result: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class OpenClawHealth(BaseModel):
    service: str = 'biotech-scout-openclaw-adapter'
    ready: bool = True
    version: str = '0.3.0'

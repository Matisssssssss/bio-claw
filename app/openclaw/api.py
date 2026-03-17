from __future__ import annotations

from fastapi import APIRouter

from app.openclaw.adapter import OpenClawAdapter
from app.openclaw.schemas import (
    OpenClawHealth,
    OpenClawToolCall,
    OpenClawToolResult,
    OpenClawToolSpec,
)

router = APIRouter(prefix='/openclaw', tags=['openclaw'])
adapter = OpenClawAdapter()


@router.get('/health', response_model=OpenClawHealth)
def openclaw_health() -> OpenClawHealth:
    return OpenClawHealth()


@router.get('/tools', response_model=list[OpenClawToolSpec])
def list_tools() -> list[OpenClawToolSpec]:
    return adapter.registry.list_tools()


@router.post('/execute', response_model=OpenClawToolResult)
def execute_tool(call: OpenClawToolCall) -> OpenClawToolResult:
    return adapter.registry.execute(call.tool_name, call.arguments)

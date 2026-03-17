from __future__ import annotations

from typing import Any, Callable

from app.openclaw.schemas import OpenClawToolResult, OpenClawToolSpec

ToolFn = Callable[[dict[str, Any]], dict[str, Any]]


class OpenClawToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[OpenClawToolSpec, ToolFn]] = {}

    def register(self, spec: OpenClawToolSpec, fn: ToolFn) -> None:
        self._tools[spec.name] = (spec, fn)

    def list_tools(self) -> list[OpenClawToolSpec]:
        return [spec for spec, _fn in self._tools.values()]

    def execute(self, tool_name: str, arguments: dict[str, Any]) -> OpenClawToolResult:
        entry = self._tools.get(tool_name)
        if not entry:
            return OpenClawToolResult(tool_name=tool_name, ok=False, error=f'Unknown tool: {tool_name}')
        spec, fn = entry
        try:
            result = fn(arguments)
            return OpenClawToolResult(tool_name=tool_name, ok=True, result=result)
        except Exception as exc:  # noqa: BLE001
            return OpenClawToolResult(tool_name=tool_name, ok=False, error=str(exc))

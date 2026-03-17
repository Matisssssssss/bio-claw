from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class CacheEntry:
    value: Any
    created_at: float
    ttl_seconds: int


@dataclass
class InMemoryTTLCache:
    entries: dict[str, CacheEntry] = field(default_factory=dict)

    def get(self, key: str) -> Any | None:
        entry = self.entries.get(key)
        if not entry:
            return None
        if time.time() - entry.created_at > entry.ttl_seconds:
            self.entries.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        self.entries[key] = CacheEntry(value=value, created_at=time.time(), ttl_seconds=ttl_seconds)


class ProviderRunner:
    def __init__(self, retries: int = 2, backoff_seconds: float = 0.2) -> None:
        self.retries = retries
        self.backoff_seconds = backoff_seconds

    def run(self, fn: Callable[[], Any]) -> Any:
        last_err: Exception | None = None
        for i in range(self.retries + 1):
            try:
                return fn()
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                if i < self.retries:
                    time.sleep(self.backoff_seconds * (i + 1))
        raise RuntimeError(f'Provider failed after retries: {last_err}')

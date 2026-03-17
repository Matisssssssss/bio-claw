from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from app.research.schemas import AgentOutput


class ResearchAgent(ABC):
    name: str

    @abstractmethod
    def run(self, ticker: str, state: Dict[str, Any]) -> AgentOutput:
        raise NotImplementedError

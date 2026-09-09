from __future__ import annotations

from dataclasses import asdict, dataclass, field
from time import time
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class AgentDecision:
    answer: str = ""
    tool_call: ToolCall | None = None


@dataclass
class TraceEvent:
    event: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RunResult:
    answer: str
    success: bool
    latency_ms: float
    tool_calls: int
    retries: int
    estimated_cost_usd: float
    trace: list[TraceEvent]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["trace"] = [event.to_dict() for event in self.trace]
        return data


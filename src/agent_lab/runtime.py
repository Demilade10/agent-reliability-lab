from __future__ import annotations

from time import perf_counter, sleep
from typing import Protocol

from .memory import SQLiteMemory
from .models import AgentDecision, RunResult, TraceEvent
from .tools import ToolError, ToolRegistry


class Policy(Protocol):
    def decide(self, message: str, observation: object | None = None) -> AgentDecision: ...


class AgentRuntime:
    def __init__(
        self,
        policy: Policy,
        tools: ToolRegistry,
        memory: SQLiteMemory,
        max_retries: int = 2,
        retry_delay_seconds: float = 0.01,
    ) -> None:
        self.policy = policy
        self.tools = tools
        self.memory = memory
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds

    def run(self, message: str, user_id: str = "demo") -> RunResult:
        started = perf_counter()
        trace = [TraceEvent("run_started", {"user_id": user_id, "message": message})]
        decision = self.policy.decide(message)
        calls = retries = 0

        if decision.tool_call is None:
            answer = decision.answer
            success = True
        else:
            call = decision.tool_call
            calls += 1
            trace.append(TraceEvent("tool_requested", {"name": call.name}))
            observation = None
            success = False
            for attempt in range(self.max_retries + 1):
                try:
                    observation = self.tools.call(call.name, call.arguments)
                    success = True
                    trace.append(TraceEvent("tool_succeeded", {"name": call.name, "attempt": attempt + 1}))
                    break
                except ToolError as error:
                    trace.append(TraceEvent("tool_failed", {"name": call.name, "error": str(error), "attempt": attempt + 1}))
                    if attempt < self.max_retries:
                        retries += 1
                        sleep(self.retry_delay_seconds * (2**attempt))
            answer = (
                self.policy.decide(message, observation).answer
                if success
                else "I could not complete that tool call safely."
            )

        self.memory.set(user_id, "last_message", message)
        latency_ms = (perf_counter() - started) * 1000
        trace.append(TraceEvent("run_finished", {"success": success, "latency_ms": latency_ms}))
        return RunResult(answer, success, latency_ms, calls, retries, 0.0, trace)


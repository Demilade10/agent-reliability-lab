from __future__ import annotations

from .models import AgentDecision, ToolCall


class RuleBasedPolicy:
    """Deterministic policy used for offline demos and repeatable evaluations."""

    def decide(self, message: str, observation: object | None = None) -> AgentDecision:
        if observation is not None:
            return AgentDecision(answer=f"The result is {observation}.")

        lowered = message.lower().strip()
        if lowered.startswith("calculate "):
            return AgentDecision(
                tool_call=ToolCall("calculate", {"expression": message[10:].strip()})
            )
        return AgentDecision(answer="I can help with calculations. Try: calculate 12 * 4")


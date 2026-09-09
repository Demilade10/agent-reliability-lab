from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


class ToolError(RuntimeError):
    pass


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    function: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def call(self, name: str, arguments: dict[str, Any]) -> Any:
        tool = self._tools.get(name)
        if tool is None:
            raise ToolError(f"Unknown tool: {name}")
        try:
            return tool.function(**arguments)
        except (TypeError, ValueError) as error:
            raise ToolError(f"Invalid call to {name}: {error}") from error

    @property
    def names(self) -> list[str]:
        return sorted(self._tools)


def calculate(expression: str) -> float:
    """Safely evaluate basic two-number arithmetic."""
    parts = expression.strip().split()
    if len(parts) != 3 or parts[1] not in {"+", "-", "*", "/"}:
        raise ValueError("Use format: NUMBER OPERATOR NUMBER")
    left, operator, right = float(parts[0]), parts[1], float(parts[2])
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if right == 0:
        raise ValueError("Division by zero")
    return left / right

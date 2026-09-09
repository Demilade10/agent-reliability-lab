import pytest

from agent_lab.tools import ToolError, ToolRegistry, calculate


def test_calculator_rejects_code_execution():
    with pytest.raises(ValueError):
        calculate("__import__('os').system('echo unsafe')")


def test_unknown_tool_is_explicit_failure():
    with pytest.raises(ToolError, match="Unknown tool"):
        ToolRegistry().call("missing", {})


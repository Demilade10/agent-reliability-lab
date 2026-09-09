import ast
from pathlib import Path


def test_adk_entry_point_defines_root_agent_without_importing_optional_dependency():
    source = Path("src/incident_agent/agent.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assigned_names = {
        target.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    assert "root_agent" in assigned_names


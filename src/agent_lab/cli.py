from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluation import evaluate, load_cases
from .memory import SQLiteMemory
from .policy import RuleBasedPolicy
from .runtime import AgentRuntime
from .tools import Tool, ToolRegistry, calculate


def build_runtime(database: str = "agent_memory.db") -> AgentRuntime:
    tools = ToolRegistry()
    tools.register(Tool("calculate", "Perform basic arithmetic", calculate))
    return AgentRuntime(RuleBasedPolicy(), tools, SQLiteMemory(database))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run or evaluate a reliable tool-using agent")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("message")
    eval_parser = subparsers.add_parser("eval")
    eval_parser.add_argument("--cases", default="evals/cases.json")
    eval_parser.add_argument("--output", default="reports/evaluation.json")
    args = parser.parse_args()

    runtime = build_runtime()
    if args.command == "run":
        print(json.dumps(runtime.run(args.message).to_dict(), indent=2))
        return
    report = evaluate(runtime, load_cases(args.cases))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Pass rate: {report['pass_rate']:.0%} ({report['passed']}/{report['total']})")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()


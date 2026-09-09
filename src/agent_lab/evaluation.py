from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .runtime import AgentRuntime


@dataclass(frozen=True)
class EvalCase:
    name: str
    message: str
    expected_answer: str
    expected_success: bool = True


def evaluate(runtime: AgentRuntime, cases: list[EvalCase]) -> dict:
    results = []
    for case in cases:
        run = runtime.run(case.message, user_id=f"eval-{case.name}")
        passed = run.answer == case.expected_answer and run.success == case.expected_success
        results.append({"case": asdict(case), "passed": passed, "run": run.to_dict()})
    passed_count = sum(item["passed"] for item in results)
    return {
        "total": len(results),
        "passed": passed_count,
        "pass_rate": passed_count / len(results) if results else 0,
        "average_latency_ms": sum(item["run"]["latency_ms"] for item in results) / len(results) if results else 0,
        "results": results,
    }


def load_cases(path: str | Path) -> list[EvalCase]:
    return [EvalCase(**item) for item in json.loads(Path(path).read_text(encoding="utf-8"))]


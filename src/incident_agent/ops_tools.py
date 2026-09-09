from __future__ import annotations

from typing import Any

SERVICE_HEALTH: dict[str, dict[str, Any]] = {
    "payments": {
        "status": "degraded",
        "error_count": 84,
        "request_count": 1200,
        "p95_latency_ms": 1850,
        "last_deploy": "payments-api@2026.09.09.3",
    },
    "identity": {
        "status": "healthy",
        "error_count": 2,
        "request_count": 1800,
        "p95_latency_ms": 240,
        "last_deploy": "identity-api@2026.09.08.2",
    },
}

RUNBOOKS = {
    "payments": [
        "Confirm elevated errors across two consecutive five-minute windows.",
        "Compare the incident start time with the latest deployment.",
        "Roll back only after approval from the incident commander.",
        "Verify recovery using error rate and p95 latency.",
    ],
    "identity": [
        "Check authentication error rate and token-provider health.",
        "Confirm whether failures affect one region or all regions.",
        "Escalate before rotating any production credentials.",
    ],
}


def get_service_health(service: str) -> dict[str, Any]:
    """Return the latest simulated health snapshot for a named service."""
    normalized = service.lower().strip()
    if normalized not in SERVICE_HEALTH:
        return {"status": "not_found", "service": normalized}
    return {"service": normalized, **SERVICE_HEALTH[normalized]}


def get_runbook(service: str) -> dict[str, Any]:
    """Return safe diagnostic steps for a service; never performs remediation."""
    normalized = service.lower().strip()
    steps = RUNBOOKS.get(normalized)
    if steps is None:
        return {"status": "not_found", "service": normalized, "steps": []}
    return {"status": "found", "service": normalized, "steps": steps}


def calculate_error_rate(error_count: int, request_count: int) -> dict[str, Any]:
    """Calculate an error percentage from observed errors and total requests."""
    if error_count < 0 or request_count <= 0 or error_count > request_count:
        return {"status": "invalid_input", "error_rate_percent": None}
    rate = round((error_count / request_count) * 100, 2)
    return {"status": "ok", "error_rate_percent": rate}


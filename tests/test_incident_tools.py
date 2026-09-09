from incident_agent.ops_tools import calculate_error_rate, get_runbook, get_service_health


def test_degraded_service_snapshot_is_specific():
    health = get_service_health(" Payments ")
    assert health["status"] == "degraded"
    assert health["last_deploy"].startswith("payments-api@")


def test_unknown_service_fails_closed():
    assert get_service_health("orders") == {"status": "not_found", "service": "orders"}
    assert get_runbook("orders")["steps"] == []


def test_error_rate_is_calculated():
    assert calculate_error_rate(84, 1200) == {
        "status": "ok",
        "error_rate_percent": 7.0,
    }


def test_impossible_error_rate_is_rejected():
    assert calculate_error_rate(11, 10)["status"] == "invalid_input"
    assert calculate_error_rate(1, 0)["error_rate_percent"] is None


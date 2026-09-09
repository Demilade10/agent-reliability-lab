from agent_lab.cli import build_runtime


def test_successful_tool_run(tmp_path):
    result = build_runtime(str(tmp_path / "memory.db")).run("calculate 6 * 7")
    assert result.success is True
    assert result.answer == "The result is 42.0."
    assert result.tool_calls == 1
    assert any(event.event == "tool_succeeded" for event in result.trace)


def test_invalid_tool_input_retries_and_fails_safely(tmp_path):
    result = build_runtime(str(tmp_path / "memory.db")).run("calculate 5 / 0")
    assert result.success is False
    assert result.retries == 2
    assert result.answer == "I could not complete that tool call safely."


def test_memory_persists_between_instances(tmp_path):
    path = tmp_path / "memory.db"
    build_runtime(str(path)).run("hello", user_id="demy")
    runtime = build_runtime(str(path))
    assert runtime.memory.get("demy", "last_message") == "hello"


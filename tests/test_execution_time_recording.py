import json
from pathlib import Path

import pytest

from scripts.execution_time_recording import collect, rollout_diagnostic


def event(second, kind, **kw):
    return {"timestamp": f"2026-09-05T00:00:{second:02d}+00:00", "type": "response_item", "payload": {"type": kind, **kw}}


def events():
    return [dict(event(0, "ignored"), type="session_meta", payload={"id": "root"}),
            event(1, "task_started", turn_id="one"), event(2, "message", role="user"),
            event(3, "custom_tool_call", call_id="a"), event(4, "custom_tool_call", call_id="b"),
            event(6, "custom_tool_call_output", call_id="a"), event(7, "custom_tool_call_output", call_id="b"),
            event(8, "task_complete", turn_id="one")]


def test_parallel_tools_not_double_counted():
    d = rollout_diagnostic(events(), "root")
    assert d["root_tool_union_seconds"] == 4
    assert d["root_span_seconds"] == 7
    assert d["evidence_class"] == "proxy"


def test_no_tools_and_multiple_turns():
    e = events(); e = e[:3] + e[-1:]
    e += [event(10, "task_started", turn_id="two"), event(11, "message", role="user"), event(15, "task_complete", turn_id="two")]
    d = rollout_diagnostic(e, "root")
    assert d["root_span_seconds"] == 14
    assert d["turn_count"] == 2
    assert d["root_tool_union_seconds"] == 0


def test_missing_tool_output_is_not_zero():
    e = events(); del e[6]
    assert rollout_diagnostic(e, "root")["root_tool_union_seconds"] is None


@pytest.mark.parametrize("mode", ["reversed", "interrupted", "wrong_thread", "duplicate_complete"])
def test_invalid_and_incomplete(mode):
    e = events()
    if mode == "reversed": e[4]["timestamp"] = e[1]["timestamp"]
    if mode == "interrupted": e.pop()
    if mode == "duplicate_complete": e.append(e[-1])
    with pytest.raises(ValueError):
        rollout_diagnostic(e, "other" if mode == "wrong_thread" else "root")


def test_collection_preserves_kpi_and_missing_boundaries(tmp_path):
    execution = dict(run_id="run", case_id="case", iteration=1, status="excluded", elapsed_seconds=20, started_at="start", ended_at="end")
    binding = dict(prompt_set_identity={"name": "prompt"}, comparison_conditions={"agent_environment": {"codex_cli": "0.153.3"}})
    source = tmp_path / "execution.json"; source.write_text(json.dumps(execution))
    before = source.read_bytes()
    d = collect(execution, binding, tmp_path, source)
    assert d["elapsed_seconds"] == 20
    assert all(d[k] is None for k in ["startup_seconds", "work_seconds", "shutdown_seconds"])
    assert d["timeline_status"] == "unavailable"
    assert source.read_bytes() == before
    with pytest.raises(FileExistsError): collect(execution, binding, tmp_path, source)


def test_usage_does_not_prove_child_completion(tmp_path):
    log = tmp_path / "rollout.jsonl"; log.write_text("\n".join(json.dumps(x) for x in events()))
    usage = tmp_path / "all-agent-usage"; usage.mkdir()
    (usage / "usage.json").write_text(json.dumps({"root_thread_id": "root", "session_count": 2, "sessions": [{"thread_id": "root", "rollout_file": str(log)}]}))
    source = tmp_path / "execution.json"; source.write_text("{}")
    d = collect(dict(run_id="r", case_id="c", iteration=1, status="valid", elapsed_seconds=10, started_at="s", ended_at="e"), dict(prompt_set_identity={}, comparison_conditions={"agent_environment": {"codex_cli": "0.153.3"}}), tmp_path, source)
    assert d["timeline_status"] == "proxy_only"
    assert d["child_completion_status"] == "unavailable"
    assert d["work_seconds"] is None

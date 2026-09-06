"""Append-only, model-invisible time diagnostics; never replaces elapsed KPI."""
from __future__ import annotations

import hashlib
import json
import math
import uuid
from datetime import datetime
from pathlib import Path

CONTRACT = "execution-time-recording/r1"
# These versions have observed persisted event semantics, but no verified input-delivery marker.
SUPPORTED = {"0.146.0", "0.153.3"}


def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def read_events(path):
    data = path.read_bytes()
    return [json.loads(line) for line in data.splitlines() if line.strip()], hashlib.sha256(data).hexdigest()


def rollout_diagnostic(events, expected_thread):
    """UTC event spans are proxies, not synchronized monotonic work time."""
    metas = [e for e in events if e.get("type") == "session_meta"]
    if len(metas) != 1 or metas[0]["payload"].get("id") != expected_thread:
        raise ValueError("thread_identity_mismatch")
    starts, finishes, users, intervals, pending = [], [], [], [], {}
    previous = -math.inf
    for line, event in enumerate(events, 1):
        at = timestamp(event["timestamp"])
        if not math.isfinite(at) or at < previous:
            raise ValueError("invalid_timeline")
        previous = at
        p = event.get("payload", {})
        kind = p.get("type")
        if kind == "task_started":
            starts.append((at, line, p.get("turn_id")))
        elif kind == "task_complete":
            finishes.append((at, line, p.get("turn_id")))
        elif kind == "message" and p.get("role") == "user":
            users.append((at, line))
        elif kind in ("function_call", "custom_tool_call"):
            if p["call_id"] in pending:
                raise ValueError("duplicate_call")
            pending[p["call_id"]] = at
        elif kind in ("function_call_output", "custom_tool_call_output"):
            if p["call_id"] not in pending:
                raise ValueError("unmatched_tool_output")
            intervals.append((pending.pop(p["call_id"]), at))
    if not starts or not finishes or len(starts) != len(finishes):
        raise ValueError("incomplete_turns")
    turn_ids = [s[2] for s in starts]
    if None in turn_ids or len(set(turn_ids)) != len(turn_ids):
        raise ValueError("ambiguous_turn_identity")
    for index, (s, f) in enumerate(zip(starts, finishes)):
        if s[2] != f[2] or s[0] > f[0] or (index and s[0] < finishes[index - 1][0]):
            raise ValueError("invalid_timeline")
    start, finish = starts[0], finishes[-1]
    if not users or not start[0] <= users[0][0] <= finish[0]:
        raise ValueError("missing_initial_user_record")
    right, tool_time = start[0], 0.0
    for a, b in sorted(intervals):
        a, b = max(a, start[0]), min(b, finish[0])
        tool_time += max(0.0, b - max(a, right))
        right = max(right, b)
    return {
        "evidence_class": "proxy", "clock": "rollout_utc_unsynchronized",
        "root_started": {"utc_seconds": start[0], "line": start[1]},
        "last_response_completed": {"utc_seconds": finish[0], "line": finish[1]},
        "first_user_record": {"utc_seconds": users[0][0], "line": users[0][1]},
        "root_span_seconds": finish[0] - start[0],
        "root_to_first_user_seconds": users[0][0] - start[0],
        "root_tool_union_seconds": None if pending else tool_time,
        "tool_status": "missing_result" if pending else "observed",
        "turn_count": len(starts),
    }


def collect(execution, binding, extension, execution_path):
    conditions = binding["comparison_conditions"]
    version = conditions.get("agent_environment", {}).get("codex_cli")
    record = {
        "schema_version": "the-caption-prompt.execution-time-diagnostic/v1",
        "contract": CONTRACT, "record_id": uuid.uuid4().hex,
        "collector_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "run_id": execution["run_id"], "attempt_id": execution["run_id"],
        "case_id": execution["case_id"], "iteration": execution["iteration"],
        "sample_id": binding.get("sample_id"), "result_id": None,
        "prompt_set_identity": binding["prompt_set_identity"],
        "comparison_conditions": conditions,
        "execution_status": execution["status"],
        "elapsed_seconds": execution["elapsed_seconds"],
        "elapsed_evidence_class": "direct",
        "execution_source": {"path": str(execution_path), "sha256": hashlib.sha256(execution_path.read_bytes()).hexdigest()},
        "boundaries": {
            "t0": {"utc": execution["started_at"], "event": "execution_started"},
            "t1": None, "t2": None,
            "t3": {"utc": execution["ended_at"], "event": "execution_ended"},
        },
        "clock": {"elapsed": "evaluation_loop_perf_counter", "boundary_utc": "unsynchronized", "mapping_error_seconds": None},
        "startup_seconds": None, "work_seconds": None, "shutdown_seconds": None,
        "interval_evidence_class": "unavailable",
        "missing_reasons": ["initial_input_delivery_not_observable", "monotonic_clock_mapping_unavailable"],
        "sum_difference_seconds": None, "sum_tolerance_seconds": None,
        "timeline_status": "unavailable", "child_completion_status": "unavailable",
        "proxy": None, "sources": [], "errors": [],
    }
    try:
        if version not in SUPPORTED:
            raise ValueError("unsupported_runtime")
        usage_path = extension / "all-agent-usage/usage.json"
        usage = json.loads(usage_path.read_text())
        root = next(s for s in usage["sessions"] if s["thread_id"] == usage["root_thread_id"])
        rollout = Path(root["rollout_file"])
        events, digest = read_events(rollout)
        record["sources"].append({"path": str(rollout), "sha256": digest})
        record["proxy"] = rollout_diagnostic(events, usage["root_thread_id"])
        record["timeline_status"] = "proxy_only"
        # Session usage is not proof of child terminal state.
        record["session_count"] = usage.get("session_count")
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        record["missing_reasons"].append(type(exc).__name__ + ":" + str(exc)[:160])
        if isinstance(exc, ValueError) and str(exc) in {"invalid_timeline", "ambiguous_turn_identity", "thread_identity_mismatch", "duplicate_call", "unmatched_tool_output"}:
            record["timeline_status"] = "invalid_timeline"
    adapter_clock = extension / "execution-time/adapter-clock.json"
    record["adapter_clock"] = None
    if adapter_clock.exists():
        try:
            data = adapter_clock.read_bytes()
            observation = json.loads(data)
            if observation["run_id"] != execution["run_id"] or observation["cli_elapsed_seconds"] < 0:
                raise ValueError("invalid_adapter_clock")
            record["adapter_clock"] = observation
            record["sources"].append({"path": str(adapter_clock), "sha256": hashlib.sha256(data).hexdigest()})
        except (OSError, ValueError, KeyError, TypeError):
            record["missing_reasons"].append("invalid_adapter_clock")
    stderr = extension / "codex-adapter/codex-stderr.bin"
    if stderr.exists():
        data = stderr.read_bytes()
        record["sources"].append({"path": str(stderr), "sha256": hashlib.sha256(data).hexdigest()})
        for code, marker in [("model_refresh_timeout", b"failed to refresh available models: timeout waiting for child process to exit"), ("connection_reset", b"Connection reset by peer")]:
            record["errors"].append({"code": code, "count": data.count(marker), "phase": "unavailable"})
    target = extension / "execution-time/diagnostic.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return record

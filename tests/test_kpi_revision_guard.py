"""Pin KPI counting outputs to their revision labels.

Comparison identity no longer includes the harness code hash
(docs/comparison-condition-identity-redesign.md). A change that alters how tokens or
elapsed time are counted must therefore change the revision label. If a test here fails,
either restore the counting or bump the revision and add a new row; never edit an existing row.
"""

import json
import tempfile
from pathlib import Path

from scripts import claude_all_agent_evidence as claude_evidence
from scripts.execution_time_recording import CONTRACT as TIME_CONTRACT
from scripts.execution_time_recording import rollout_diagnostic

SESSION = "11111111-2222-3333-4444-555555555555"
MODEL = "claude-opus-5-5"

CLAUDE_TOKEN_OUTPUTS = {
    "claude-v1": {"all_agent_total_tokens": 132, "response_count": 2},
}
TIME_OUTPUTS = {
    "execution-time-recording/r1": {"root_span_seconds": 7, "root_tool_union_seconds": 4, "turn_count": 1},
}


def usage(input_tokens, cache_creation, cache_read, output):
    return {
        "input_tokens": input_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "output_tokens": output,
    }


def assistant(message_id, values, model=MODEL):
    return {
        "type": "assistant",
        "sessionId": SESSION,
        "requestId": "req_" + message_id,
        "message": {"id": message_id, "model": model, "content": [{"type": "text", "text": "x"}], "usage": values},
    }


def claude_token_output():
    with tempfile.TemporaryDirectory() as directory:
        transcript = Path(directory) / "projects" / "-tmp-work" / f"{SESSION}.jsonl"
        transcript.parent.mkdir(parents=True)
        rows = [
            assistant("msg_1", usage(10, 5, 100, 1)),
            assistant("msg_1", usage(10, 5, 100, 7)),
            assistant("msg_2", usage(0, 0, 0, 10)),
        ]
        transcript.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
        totals = {"inputTokens": 10, "cacheCreationInputTokens": 5, "cacheReadInputTokens": 100, "outputTokens": 17}
        stream = (
            json.dumps({"type": "system", "subtype": "init", "session_id": SESSION})
            + "\n"
            + json.dumps({"type": "result", "subtype": "success", "is_error": False, "session_id": SESSION, "modelUsage": {MODEL: totals}})
            + "\n"
        ).encode()
        report = claude_evidence.collect_usage(Path(directory), claude_evidence.parse_stream(stream))
    return {key: report[key] for key in ("all_agent_total_tokens", "response_count")}


def event(second, kind, **kw):
    return {"timestamp": f"2026-09-05T00:00:{second:02d}+00:00", "type": "response_item", "payload": {"type": kind, **kw}}


def time_output():
    events = [
        dict(event(0, "ignored"), type="session_meta", payload={"id": "root"}),
        event(1, "task_started", turn_id="one"),
        event(2, "message", role="user"),
        event(3, "custom_tool_call", call_id="a"),
        event(4, "custom_tool_call", call_id="b"),
        event(6, "custom_tool_call_output", call_id="a"),
        event(7, "custom_tool_call_output", call_id="b"),
        event(8, "task_complete", turn_id="one"),
    ]
    diagnostic = rollout_diagnostic(events, "root")
    return {key: diagnostic[key] for key in TIME_OUTPUTS[TIME_CONTRACT]}


def test_claude_token_counting_matches_its_revision():
    revision = claude_evidence.TOKEN_ACCOUNTING["revision"]
    assert revision in CLAUDE_TOKEN_OUTPUTS, f"add a pinned row for {revision}"
    assert claude_token_output() == CLAUDE_TOKEN_OUTPUTS[revision]


def test_time_recording_matches_its_contract():
    assert TIME_CONTRACT in TIME_OUTPUTS, f"add a pinned row for {TIME_CONTRACT}"
    assert time_output() == TIME_OUTPUTS[TIME_CONTRACT]

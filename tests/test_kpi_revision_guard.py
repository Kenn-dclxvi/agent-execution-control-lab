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


COST_OUTPUTS = {
    "the-caption-prompt.usage-components/v1": {
        "codex": {"uncached_input": 10_200, "cache_read": 290_800, "output": 30, "long_context_tokens": 300_020},
        "claude": {"cache_write_1h": 20, "cache_write_5m": 10, "cache_read": 100, "output": 5},
        "cost_micro_usd": 2_000 * 2 + 1_000 * 0.1 * 10 + 100,
    },
}


def cost_output():
    from scripts import usage_components as uc

    with tempfile.TemporaryDirectory() as directory:
        first = {"input_tokens": 1000, "cached_input_tokens": 800, "output_tokens": 10, "reasoning_output_tokens": 0, "total_tokens": 1010}
        second = {"input_tokens": 300_000, "cached_input_tokens": 290_000, "output_tokens": 20, "reasoning_output_tokens": 0, "total_tokens": 300_020}
        total = {key: first[key] + second[key] for key in first}
        events = [
            {"payload": {"type": "token_count", "info": {"total_token_usage": first, "last_token_usage": first}}},
            {"payload": {"type": "token_count", "info": {"total_token_usage": first, "last_token_usage": first}}},
            {"payload": {"type": "token_count", "info": {"total_token_usage": total, "last_token_usage": second}}},
        ]
        rollout = Path(directory) / "rollout.jsonl"
        rollout.write_text("".join(json.dumps(item) + "\n" for item in events), encoding="utf-8")
        codex = uc.summed_components([uc.codex_components([rollout], "m")])
    claude = uc.claude_components(
        [
            {
                "model": "m",
                "usage": {"input_tokens": 0, "cache_creation_input_tokens": 30, "cache_read_input_tokens": 100, "output_tokens": 5},
                "cache_creation_split": {"ephemeral_1h_input_tokens": 20, "ephemeral_5m_input_tokens": 10},
            }
        ]
    )["by_model"]["m"]["standard"]
    prices = {"uncached_input": 2.0, "cache_read": 0.1, "cache_write_5m": 2.5, "cache_write_1h": 4.0, "cache_write_unsplit": None, "output": 10.0}
    table = {"models": {"m": {"standard": prices}}}
    components = uc.components_document({"m": {"standard": {**uc.empty_buckets(), "uncached_input": 2_000, "cache_read": 10_000, "output": 10}}}, "test")
    return {
        "codex": {key: codex[key] for key in ("uncached_input", "cache_read", "output", "long_context_tokens")},
        "claude": {key: claude[key] for key in ("cache_write_1h", "cache_write_5m", "cache_read", "output")},
        "cost_micro_usd": round(uc.run_cost(components, table) * 1_000_000, 6),
    }


def test_cost_counting_matches_its_revision():
    from scripts.usage_components import USAGE_COMPONENTS_SCHEMA

    assert USAGE_COMPONENTS_SCHEMA in COST_OUTPUTS, f"add a pinned row for {USAGE_COMPONENTS_SCHEMA}"
    assert cost_output() == COST_OUTPUTS[USAGE_COMPONENTS_SCHEMA]

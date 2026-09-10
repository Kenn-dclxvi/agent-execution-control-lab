#!/usr/bin/env python3
"""Normalize only confirmed fields from a synthetic agentic raw trace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_SCHEMA = ROOT / "docs/general-chat-agentic-raw-normalizer-input.schema.json"
DEFAULT_OUTPUT_SCHEMA = ROOT / "docs/general-chat-agentic-binding-extractor-input.schema.json"
DEFAULT_SYNTHETIC_FIXTURE = ROOT / "docs/general-chat-agentic-raw-normalizer-synthetic-r1.json"
NORMALIZED_SCHEMA_VERSION = "general-chat-agentic-normalized-trace/v1"


class NormalizationError(Exception):
    """A synthetic input or schema could not be loaded."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise NormalizationError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise NormalizationError(f"JSON value must be an object: {path}")
    return value


def validate(value: dict[str, Any], schema: dict[str, Any]) -> None:
    jsonschema.Draft202012Validator(schema).validate(value)


def terminal_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projected = []
    for event in events:
        payload = event.get("payload")
        if not isinstance(payload, dict) or payload.get("type") != "task_complete":
            continue
        result = payload.get("last_agent_message")
        projected.append({"sender": None, "result": result if isinstance(result, str) else None})
    return projected


def final_usage(events: list[dict[str, Any]]) -> dict[str, int] | None:
    observed = None
    for event in events:
        payload = event.get("payload")
        if not isinstance(payload, dict) or payload.get("type") != "token_count":
            continue
        info = payload.get("info")
        usage = info.get("total_token_usage") if isinstance(info, dict) else None
        if isinstance(usage, dict):
            observed = {
                field: usage[field]
                for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")
            }
    return observed


def normalize_known_fields(raw: dict[str, Any]) -> dict[str, Any]:
    root_ids = [event["thread_id"] for event in raw["root_events"]]
    root_id = root_ids[0] if len(root_ids) == 1 else None
    descendants = []
    sessions = []
    for session in raw["sessions"]:
        meta = session["session_meta"]["payload"]
        events = session["events"]
        usage = final_usage(events)
        sessions.append(
            {
                "thread_id": meta["id"],
                "parent_thread_id": meta["parent_thread_id"],
                "input_tokens": usage["input_tokens"] if usage is not None else None,
                "cached_input_tokens": usage["cached_input_tokens"] if usage is not None else None,
                "output_tokens": usage["output_tokens"] if usage is not None else None,
                "total_tokens": usage["total_tokens"] if usage is not None else None,
            }
        )
        if meta["parent_thread_id"] is not None:
            descendants.append(
                {
                    "thread_id": meta["id"],
                    "parent_thread_id": meta["parent_thread_id"],
                    "task_identity": None,
                    "terminal_events": terminal_events(events),
                }
            )
    return {
        "schema_version": NORMALIZED_SCHEMA_VERSION,
        "probe_id": raw["probe_id"],
        "root": {
            "thread_started": root_ids,
            "spawn_calls": [],
            "spawn_results": [],
            "tool_calls": [],
            "tool_results": [],
            "final_responses": [],
        },
        "descendants": descendants,
        "usage": {"root_thread_id": root_id, "sessions": sessions},
        "monotonic": {
            "started_ms": raw["monotonic"]["started_ms"],
            "ended_ms": raw["monotonic"]["ended_ms"],
        },
        "projection": {"raw_transcript_required": False},
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--synthetic-fixture", type=Path, default=DEFAULT_SYNTHETIC_FIXTURE)
    value.add_argument("--input-schema", type=Path, default=DEFAULT_INPUT_SCHEMA)
    value.add_argument("--output-schema", type=Path, default=DEFAULT_OUTPUT_SCHEMA)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        synthetic = load_object(args.synthetic_fixture.resolve())
        if synthetic.get("schema_version") != "general-chat-agentic-raw-normalizer-synthetic-fixture/v1":
            raise NormalizationError("synthetic fixture schema mismatch")
        raw = synthetic.get("raw_trace")
        if not isinstance(raw, dict):
            raise NormalizationError("synthetic fixture has no raw_trace object")
        input_schema = load_object(args.input_schema.resolve())
        output_schema = load_object(args.output_schema.resolve())
        validate(raw, input_schema)
        normalized = normalize_known_fields(raw)
        validate(normalized, output_schema)
    except (NormalizationError, jsonschema.ValidationError, jsonschema.SchemaError) as error:
        print(
            json.dumps(
                {
                    "schema_version": NORMALIZED_SCHEMA_VERSION,
                    "status": "normalizer_error",
                    "error": str(error),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(normalized, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

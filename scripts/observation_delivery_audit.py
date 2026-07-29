#!/usr/bin/env python3
"""Audit whether a rollout kept nested tool results behind code mode."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "the-caption-prompt.observation-delivery-audit/v1"


class ObservationDeliveryAuditError(Exception):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def audit(rollout: Path) -> dict[str, Any]:
    outer_code_calls = 0
    outer_code_outputs = 0
    direct_calls: list[dict[str, str]] = []
    direct_outputs = 0
    model_visible_result_bytes = 0
    model_steps = 0

    try:
        lines = rollout.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise ObservationDeliveryAuditError(f"missing rollout: {rollout}") from exc
    for line_number, raw_line in enumerate(lines, start=1):
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ObservationDeliveryAuditError(
                f"invalid rollout JSON at line {line_number}"
            ) from exc
        if not isinstance(event, dict):
            continue
        if event.get("type") == "event_msg":
            payload = event.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "token_count":
                model_steps += 1
            continue
        if event.get("type") != "response_item":
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        item_type = payload.get("type")
        if item_type == "custom_tool_call" and payload.get("name") == "exec":
            outer_code_calls += 1
        elif item_type == "custom_tool_call_output":
            outer_code_outputs += 1
            model_visible_result_bytes += len(canonical_json(payload.get("output")))
        elif item_type == "function_call":
            direct_calls.append(
                {
                    "name": str(payload.get("name", "")),
                    "call_id": str(payload.get("call_id", "")),
                }
            )
        elif item_type == "function_call_output":
            direct_outputs += 1
            model_visible_result_bytes += len(canonical_json(payload.get("output")))

    mechanism_passed = (
        outer_code_calls > 0
        and outer_code_calls == outer_code_outputs
        and not direct_calls
        and direct_outputs == 0
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "rollout": str(rollout.resolve()),
        "mechanism_passed": mechanism_passed,
        "outer_code_calls": outer_code_calls,
        "outer_code_outputs": outer_code_outputs,
        "direct_calls": direct_calls,
        "direct_outputs": direct_outputs,
        "model_reentries_from_tool_results": outer_code_outputs + direct_outputs,
        "model_visible_result_bytes": model_visible_result_bytes,
        "model_steps": model_steps,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--rollout", required=True)
    value.add_argument("--output", required=True)
    return value


def main() -> int:
    args = parser().parse_args()
    result = audit(Path(args.rollout))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
    return 0 if result["mechanism_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

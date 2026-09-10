#!/usr/bin/env python3
"""Qualification runtime r4 with corrected terminal token accounting."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
import json
from pathlib import Path
from typing import Any


MODULE_PATH = Path(__file__).with_name("run_qualification_v3.py")
SPEC = importlib.util.spec_from_file_location("general_chat_qualification_r3", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load qualification runtime r3")
r3 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r3)
base = r3.base


def parse_usage(stdout: bytes) -> tuple[str, int]:
    thread_ids: list[str] = []
    usages: list[dict[str, Any]] = []
    failures: list[str] = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("type") == "thread.started":
            thread_ids.append(event.get("thread_id"))
        elif event.get("type") == "turn.completed":
            usages.append(event.get("usage") or {})
        elif event.get("type") in {"error", "turn.failed"}:
            failures.append(event.get("type"))
    if failures or len(thread_ids) != 1 or len(usages) != 1:
        raise base.QualificationError("Codex JSONL terminal identity is incomplete")
    usage = usages[0]
    total = usage.get("total_tokens")
    if not isinstance(total, int):
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        if not isinstance(input_tokens, int) or input_tokens < 0 or not isinstance(output_tokens, int) or output_tokens < 0:
            raise base.QualificationError("Codex terminal token operands are unavailable")
        total = input_tokens + output_tokens
    if total < 0:
        raise base.QualificationError("Codex terminal token total is invalid")
    return thread_ids[0], total


# r3.run_slot reads the parser through this shared base module. Bind the r4 parser
# before any slot is issued; every slot in this runtime uses the same accounting.
base.parse_usage = parse_usage


def validate_profile(profile_path: Path) -> dict[str, Any]:
    bound = base.validate_profile(profile_path)
    adapter_path = base.verify_reference(bound["profile"].get("runtime_adapter_ref") or {}, "runtime adapter")
    if adapter_path != Path(__file__).resolve():
        raise base.QualificationError("runtime adapter path mismatch")
    isolation = (bound["profile"].get("runtime_ref") or {}).get("runtime_state_isolation")
    if isolation != {
        "codex_home": "per_slot_temporary",
        "auth_transport": "host_auth_symlink_not_persisted",
        "skills_cache": "not_shared",
        "models_cache": "not_shared",
    }:
        raise base.QualificationError("runtime state isolation contract mismatch")
    accounting = (bound["profile"].get("runtime_ref") or {}).get("token_accounting") or {}
    if accounting.get("contract_id") != "codex-jsonl-single-agent-all-agent-total-r2":
        raise base.QualificationError("token accounting contract mismatch")
    return bound


def make_preflight(profile_path: Path) -> dict[str, Any]:
    validate_profile(profile_path)
    receipt = base.make_preflight(profile_path)
    receipt["receipt_id"] = "chat-control-free-core-r1-n1-preflight-r4"
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256")
    return receipt


def validate_preflight(path: Path, profile_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = base.load_object(path)
    if receipt.get("schema_version") != "general-chat-response-preflight/v1":
        raise base.QualificationError("preflight schema mismatch")
    if receipt.get("receipt_sha256") != base.content_identity(receipt, "receipt_sha256"):
        raise base.QualificationError("preflight receipt hash mismatch")
    if receipt.get("state") != "ready_not_issued" or receipt.get("issued_slot_count") != 0:
        raise base.QualificationError("preflight is not ready")
    expected = make_preflight(profile_path)
    if receipt != expected:
        raise base.QualificationError("preflight receipt is stale")
    return receipt, validate_profile(profile_path)


def execute(profile_path: Path, preflight_path: Path, dispatch_path: Path, result_path: Path) -> dict[str, Any]:
    receipt, bound = validate_preflight(preflight_path, profile_path)
    dispatch = {
        "schema_version": "general-chat-response-dispatch/v1",
        "dispatch_id": "chat-control-free-core-r1-n1-dispatch-r4",
        "preflight": {
            "path": str(preflight_path.resolve().relative_to(base.ROOT)),
            "sha256": base.sha256_file(preflight_path),
            "receipt_id": receipt["receipt_id"],
        },
        "slots": receipt["slots"],
        "issued_slot_count": len(receipt["slots"]),
        "state": "issued_once",
    }
    dispatch["dispatch_sha256"] = base.content_identity(dispatch, "dispatch_sha256")
    base.write_once(dispatch_path, dispatch)
    cases = {item["case_id"]: item for item in bound["cases"]["cases"]}
    oracles = {item["case_id"]: item for item in bound["oracle"]["cases"]}
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=24) as executor:
        futures = {
            executor.submit(r3.run_slot, bound, cases[slot["case_id"]], oracles[slot["case_id"]]): slot
            for slot in receipt["slots"]
        }
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda item: item["slot_id"])
    valid = [row for row in rows if row["status"] == "valid"]
    result = {
        "schema_version": "general-chat-response-qualification-result/v1",
        "result_id": "chat-control-free-core-r1-n1-qualification-r4",
        "target_id": "general-chat-response-control",
        "profile": receipt["profile"],
        "preflight": dispatch["preflight"],
        "dispatch": {
            "path": str(dispatch_path.resolve().relative_to(base.ROOT)),
            "sha256": base.sha256_file(dispatch_path),
            "dispatch_id": dispatch["dispatch_id"],
        },
        "cases": rows,
        "summary": {
            "authorized_slots": len(rows),
            "valid_results": len(valid),
            "unrateable_results": sum(row["status"] == "unrateable" for row in rows),
            "external_failures": sum(row["status"] == "external_failure" for row in rows),
            "score_distribution": {
                str(score): sum(row.get("quality_score") == score for row in valid) for score in (1, 2, 3, 4)
            },
            "all_kpis_complete": len(valid) == len(rows) and all(
                isinstance(row.get("all_agent_total_tokens"), int)
                and isinstance(row.get("elapsed_seconds"), (int, float)) for row in valid
            ),
            "qualification_state": "measurement_established" if len(valid) == len(rows) else "measurement_not_established",
        },
        "lifecycle": {
            "evaluation": "qualification_n1_completed",
            "candidate": "not_created",
            "adoption": "not_decided",
            "release": "not_created",
            "projection": "not_authorized",
        },
    }
    result["result_sha256"] = base.content_identity(result, "result_sha256")
    base.write_once(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight_parser = subparsers.add_parser("preflight")
    preflight_parser.add_argument("--profile", type=Path, required=True)
    preflight_parser.add_argument("--output", type=Path, required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--profile", type=Path, required=True)
    run_parser.add_argument("--preflight", type=Path, required=True)
    run_parser.add_argument("--dispatch-output", type=Path, required=True)
    run_parser.add_argument("--result-output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            receipt = make_preflight(args.profile)
            base.write_once(args.output, receipt)
            print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
        else:
            result = execute(args.profile, args.preflight, args.dispatch_output, args.result_output)
            print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
    except base.QualificationError as error:
        print(str(error), file=__import__("sys").stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

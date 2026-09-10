#!/usr/bin/env python3
"""Evaluate RequiredValueCarrier r1 on all eight fixed cases at N=5."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
from typing import Any


MODULE_PATH = Path(__file__).with_name("run_candidate_targeted_n5.py")
SPEC = importlib.util.spec_from_file_location("general_chat_candidate_targeted_n5", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load targeted Candidate runtime")
targeted = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(targeted)
base = targeted.base


def validate_profile(profile_path: Path) -> dict[str, Any]:
    profile_path = profile_path.resolve()
    profile = base.load_object(profile_path)
    normalized = copy.deepcopy(profile)
    normalized["runtime_adapter_ref"] = {
        "path": "evaluations/targets/general-chat-response-control/runtime/run_candidate_targeted_n5.py",
        "sha256": base.sha256_file(MODULE_PATH),
    }
    with tempfile.TemporaryDirectory(prefix="general-chat-core-profile-") as raw_temp:
        normalized_path = Path(raw_temp) / "profile.json"
        normalized_path.write_text(json.dumps(normalized, ensure_ascii=False), encoding="utf-8")
        bound = targeted.validate_profile(normalized_path)
    bound["profile"], bound["profile_path"] = profile, profile_path
    adapter_path = base.verify_reference(profile.get("runtime_adapter_ref") or {}, "runtime adapter")
    if adapter_path != Path(__file__).resolve():
        raise base.QualificationError("runtime adapter path mismatch")
    return bound


def make_preflight(profile_path: Path) -> dict[str, Any]:
    bound = validate_profile(profile_path)
    slots = [
        {"slot_id": f"{case['case_id']}-i{i:03d}", "case_id": case["case_id"], "case_revision": case["case_revision"], "iteration": i}
        for case in bound["cases"]["cases"] for i in range(1, 6)
    ]
    baseline_path = base.ROOT / "evaluations/targets/general-chat-response-control/results/chat-control-free-core-r1-n5-baseline-r1.json"
    targeted_path = base.ROOT / "evaluations/targets/general-chat-response-control/results/required-value-carrier-core-r1-q02-n5-r1.json"
    receipt = {
        "schema_version": "general-chat-response-preflight/v1",
        "receipt_id": "required-value-carrier-core-r1-n5-preflight-r1",
        "reference_result": {"path": str(baseline_path.relative_to(base.ROOT)), "sha256": base.sha256_file(baseline_path), "baseline_state": "measured"},
        "targeted_gate_result": {"path": str(targeted_path.relative_to(base.ROOT)), "sha256": base.sha256_file(targeted_path), "targeted_gate_passed": True},
        "target": {"path": str(base.TARGET_PATH.relative_to(base.ROOT)), "sha256": base.sha256_file(base.TARGET_PATH)},
        "registration": {"path": str(base.REGISTRATION_PATH.relative_to(base.ROOT)), "sha256": base.sha256_file(base.REGISTRATION_PATH)},
        "profile": {"path": str(bound["profile_path"].relative_to(base.ROOT)), "sha256": base.sha256_file(bound["profile_path"]), "profile_id": bound["profile"]["profile_id"]},
        "prompt_set_identity": bound["profile"]["prompt_set_identity"], "target_subject_ref": bound["profile"]["target_subject_ref"],
        "evaluation_set_ref": bound["profile"]["evaluation_set_ref"], "runtime_ref": bound["profile"]["runtime_ref"],
        "task_spec_ref": bound["profile"]["task_spec_ref"], "rating_ref": bound["profile"]["rating_ref"],
        "allowed_delta": "prompt_set_identity only", "slots": slots, "authorized_slot_count": 40,
        "issued_slot_count": 0, "state": "ready_not_issued",
    }
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256")
    return receipt


def validate_preflight(path: Path, profile_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = base.load_object(path)
    if receipt.get("receipt_sha256") != base.content_identity(receipt, "receipt_sha256") or receipt.get("state") != "ready_not_issued" or receipt.get("issued_slot_count") != 0:
        raise base.QualificationError("preflight is invalid")
    expected = make_preflight(profile_path)
    if receipt != expected: raise base.QualificationError("preflight receipt is stale")
    return receipt, validate_profile(profile_path)


def execute(profile_path: Path, preflight_path: Path, dispatch_path: Path, result_path: Path) -> dict[str, Any]:
    receipt, bound = validate_preflight(preflight_path, profile_path)
    dispatch = {"schema_version": "general-chat-response-dispatch/v1", "dispatch_id": "required-value-carrier-core-r1-n5-dispatch-r1", "preflight": {"path": str(preflight_path.resolve().relative_to(base.ROOT)), "sha256": base.sha256_file(preflight_path), "receipt_id": receipt["receipt_id"]}, "slots": receipt["slots"], "issued_slot_count": 40, "state": "issued_once"}
    dispatch["dispatch_sha256"] = base.content_identity(dispatch, "dispatch_sha256"); base.write_once(dispatch_path, dispatch)
    cases = {item["case_id"]: item for item in bound["cases"]["cases"]}; oracles = {item["case_id"]: item for item in bound["oracle"]["cases"]}
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=24) as executor:
        futures = [executor.submit(targeted.run_slot, bound, cases[slot["case_id"]], oracles[slot["case_id"]], slot["iteration"]) for slot in receipt["slots"]]
        for future in as_completed(futures): rows.append(future.result())
    rows.sort(key=lambda item: item["slot_id"]); valid = [row for row in rows if row["status"] == "valid"]
    preservation_passed = len(valid) == 40 and all(row["quality_score"] == 4 for row in valid)
    result = {"schema_version": "general-chat-response-candidate-result/v1", "result_id": "required-value-carrier-core-r1-n5-r1", "target_id": "general-chat-response-control", "profile": receipt["profile"], "reference_result": receipt["reference_result"], "targeted_gate_result": receipt["targeted_gate_result"], "preflight": dispatch["preflight"], "dispatch": {"path": str(dispatch_path.resolve().relative_to(base.ROOT)), "sha256": base.sha256_file(dispatch_path), "dispatch_id": dispatch["dispatch_id"]}, "cases": rows, "summary": {"authorized_slots": 40, "valid_results": len(valid), "unrateable_results": sum(row["status"] == "unrateable" for row in rows), "external_failures": sum(row["status"] == "external_failure" for row in rows), "score_distribution": {str(score): sum(row.get("quality_score") == score for row in valid) for score in (1,2,3,4)}, "preservation_gate_passed": preservation_passed}, "lifecycle": {"evaluation": "core_n5_completed", "candidate": "evaluation_passed" if preservation_passed else "evaluation_failed", "adoption": "not_decided", "release": "not_created", "projection": "not_authorized"}}
    result["result_sha256"] = base.content_identity(result, "result_sha256"); base.write_once(result_path, result); return result


def main() -> int:
    parser = argparse.ArgumentParser(); subs = parser.add_subparsers(dest="command", required=True)
    pre = subs.add_parser("preflight"); pre.add_argument("--profile", type=Path, required=True); pre.add_argument("--output", type=Path, required=True)
    run = subs.add_parser("run"); run.add_argument("--profile", type=Path, required=True); run.add_argument("--preflight", type=Path, required=True); run.add_argument("--dispatch-output", type=Path, required=True); run.add_argument("--result-output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            receipt = make_preflight(args.profile); base.write_once(args.output, receipt); print(json.dumps({"authorized_slot_count": 40, "state": receipt["state"]}, sort_keys=True))
        else:
            result = execute(args.profile, args.preflight, args.dispatch_output, args.result_output); print(json.dumps(result["summary"], sort_keys=True))
    except base.QualificationError as error:
        print(str(error), file=__import__("sys").stderr); return 1
    return 0


if __name__ == "__main__": raise SystemExit(main())

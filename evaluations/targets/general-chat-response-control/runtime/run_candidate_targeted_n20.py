#!/usr/bin/env python3
"""Extend the passed RequiredValueCarrier targeted evaluation from N=5 to N=20."""

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
    raise RuntimeError("cannot load targeted Candidate N=5 runtime")
n5 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(n5)
base = n5.base


def validate_profile(profile_path: Path) -> dict[str, Any]:
    profile_path = profile_path.resolve(); profile = base.load_object(profile_path); normalized = copy.deepcopy(profile)
    normalized["runtime_adapter_ref"] = {"path": "evaluations/targets/general-chat-response-control/runtime/run_candidate_targeted_n5.py", "sha256": base.sha256_file(MODULE_PATH)}
    normalized["repetition_condition"] = {"iterations": 5, "order": "case_id_ascending_then_iteration_ascending", "valid_low_quality_policy": "retain", "external_failure_policy": "record_and_stop_before_comparison"}
    with tempfile.TemporaryDirectory(prefix="general-chat-n20-profile-") as raw_temp:
        path = Path(raw_temp) / "profile.json"; path.write_text(json.dumps(normalized, ensure_ascii=False), encoding="utf-8"); bound = n5.validate_profile(path)
    bound["profile"], bound["profile_path"] = profile, profile_path
    if base.verify_reference(profile.get("runtime_adapter_ref") or {}, "runtime adapter") != Path(__file__).resolve(): raise base.QualificationError("runtime adapter path mismatch")
    if profile.get("repetition_condition") != {"iterations": 20, "order": "iteration_ascending", "valid_low_quality_policy": "retain", "external_failure_policy": "record_and_stop_before_comparison"}: raise base.QualificationError("N=20 repetition condition mismatch")
    return bound


def make_preflight(profile_path: Path) -> dict[str, Any]:
    bound = validate_profile(profile_path); case = next(item for item in bound["cases"]["cases"] if item["case_id"] == "GCR-Q02")
    slots = [{"slot_id": f"GCR-Q02-i{i:03d}", "case_id": "GCR-Q02", "case_revision": case["case_revision"], "iteration": i} for i in range(1, 21)]
    core_path = base.ROOT / "evaluations/targets/general-chat-response-control/results/required-value-carrier-core-r1-n5-r1.json"
    receipt = {"schema_version": "general-chat-response-preflight/v1", "receipt_id": "required-value-carrier-core-r1-q02-n20-preflight-r1", "prior_gate_result": {"path": str(core_path.relative_to(base.ROOT)), "sha256": base.sha256_file(core_path), "preservation_gate_passed": True}, "target": {"path": str(base.TARGET_PATH.relative_to(base.ROOT)), "sha256": base.sha256_file(base.TARGET_PATH)}, "registration": {"path": str(base.REGISTRATION_PATH.relative_to(base.ROOT)), "sha256": base.sha256_file(base.REGISTRATION_PATH)}, "profile": {"path": str(profile_path.resolve().relative_to(base.ROOT)), "sha256": base.sha256_file(profile_path), "profile_id": bound["profile"]["profile_id"]}, "prompt_set_identity": bound["profile"]["prompt_set_identity"], "target_subject_ref": bound["profile"]["target_subject_ref"], "evaluation_set_ref": bound["profile"]["evaluation_set_ref"], "runtime_ref": bound["profile"]["runtime_ref"], "task_spec_ref": bound["profile"]["task_spec_ref"], "rating_ref": bound["profile"]["rating_ref"], "allowed_delta": "repetition extension on GCR-Q02 only", "slots": slots, "authorized_slot_count": 20, "issued_slot_count": 0, "state": "ready_not_issued"}
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256"); return receipt


def validate_preflight(path: Path, profile_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = base.load_object(path)
    if receipt.get("receipt_sha256") != base.content_identity(receipt, "receipt_sha256") or receipt.get("state") != "ready_not_issued" or receipt.get("issued_slot_count") != 0: raise base.QualificationError("preflight is invalid")
    if receipt != make_preflight(profile_path): raise base.QualificationError("preflight receipt is stale")
    return receipt, validate_profile(profile_path)


def execute(profile_path: Path, preflight_path: Path, dispatch_path: Path, result_path: Path) -> dict[str, Any]:
    receipt, bound = validate_preflight(preflight_path, profile_path)
    dispatch = {"schema_version": "general-chat-response-dispatch/v1", "dispatch_id": "required-value-carrier-core-r1-q02-n20-dispatch-r1", "preflight": {"path": str(preflight_path.resolve().relative_to(base.ROOT)), "sha256": base.sha256_file(preflight_path), "receipt_id": receipt["receipt_id"]}, "slots": receipt["slots"], "issued_slot_count": 20, "state": "issued_once"}
    dispatch["dispatch_sha256"] = base.content_identity(dispatch, "dispatch_sha256"); base.write_once(dispatch_path, dispatch)
    case = next(item for item in bound["cases"]["cases"] if item["case_id"] == "GCR-Q02"); oracle = next(item for item in bound["oracle"]["cases"] if item["case_id"] == "GCR-Q02")
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(n5.run_slot, bound, case, oracle, i) for i in range(1, 21)]
        for future in as_completed(futures): rows.append(future.result())
    rows.sort(key=lambda item: item["slot_id"]); valid = [row for row in rows if row["status"] == "valid"]
    gate_passed = len(valid) == 20 and all(row["quality_score"] == 4 and not row["response"]["clarification_value_ids"] and not row["response"]["request_evidence_ids"] and not row["response"]["unresolved_topic_ids"] for row in valid)
    result = {"schema_version": "general-chat-response-candidate-result/v1", "result_id": "required-value-carrier-core-r1-q02-n20-r1", "target_id": "general-chat-response-control", "profile": receipt["profile"], "prior_gate_result": receipt["prior_gate_result"], "preflight": dispatch["preflight"], "dispatch": {"path": str(dispatch_path.resolve().relative_to(base.ROOT)), "sha256": base.sha256_file(dispatch_path), "dispatch_id": dispatch["dispatch_id"]}, "cases": rows, "summary": {"authorized_slots": 20, "valid_results": len(valid), "unrateable_results": sum(row["status"] == "unrateable" for row in rows), "external_failures": sum(row["status"] == "external_failure" for row in rows), "score_distribution": {str(score): sum(row.get("quality_score") == score for row in valid) for score in (1,2,3,4)}, "targeted_n20_gate_passed": gate_passed}, "lifecycle": {"evaluation": "targeted_n20_completed", "candidate": "evaluation_passed" if gate_passed else "evaluation_failed", "adoption": "not_decided", "release": "not_created", "projection": "not_authorized"}}
    result["result_sha256"] = base.content_identity(result, "result_sha256"); base.write_once(result_path, result); return result


def main() -> int:
    parser = argparse.ArgumentParser(); subs = parser.add_subparsers(dest="command", required=True); pre = subs.add_parser("preflight"); pre.add_argument("--profile", type=Path, required=True); pre.add_argument("--output", type=Path, required=True); run = subs.add_parser("run"); run.add_argument("--profile", type=Path, required=True); run.add_argument("--preflight", type=Path, required=True); run.add_argument("--dispatch-output", type=Path, required=True); run.add_argument("--result-output", type=Path, required=True); args = parser.parse_args()
    try:
        if args.command == "preflight": receipt = make_preflight(args.profile); base.write_once(args.output, receipt); print(json.dumps({"authorized_slot_count": 20, "state": receipt["state"]}, sort_keys=True))
        else: result = execute(args.profile, args.preflight, args.dispatch_output, args.result_output); print(json.dumps(result["summary"], sort_keys=True))
    except base.QualificationError as error: print(str(error), file=__import__("sys").stderr); return 1
    return 0


if __name__ == "__main__": raise SystemExit(main())

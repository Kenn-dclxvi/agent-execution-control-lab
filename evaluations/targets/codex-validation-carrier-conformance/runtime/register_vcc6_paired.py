#!/usr/bin/env python3
"""Register VCC6 P001/P002 paired N=5 observations and fixed KPI gates."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import statistics
from typing import Any


def _load_runner():
    path = Path(__file__).with_name("runner_vcc6_paired.py")
    spec = importlib.util.spec_from_file_location("codex_validation_carrier_vcc6_paired_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("paired runner cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = _load_runner()
RESULT_SCHEMA = "codex-validation-carrier-paired-comparison-result/v1"


def collect_new_row(slot: dict[str, Any], evidence_root: Path) -> dict[str, Any]:
    private = evidence_root / slot["slot_id"] / "private"
    required = {
        "observation": private / "execution-observation.json",
        "grade": private / "grade.json",
        "final_response": private / "final-response.json",
        "codex_events": private / "codex-events.jsonl",
        "stderr": private / "codex-stderr.bin",
        "dispatch_receipt": private / "dispatch-receipt.json",
    }
    if any(not path.is_file() for path in required.values()):
        raise runner.RuntimeGateError(f"paired evidence is incomplete: {slot['slot_id']}")
    observation = runner.adapter.load_object(required["observation"])
    grade = runner.adapter.load_object(required["grade"])
    if observation.get("slot") != slot or observation.get("status") != "valid":
        raise runner.RuntimeGateError(f"paired observation is invalid: {slot['slot_id']}")
    if grade.get("case_id") != slot["case_id"] or grade.get("quality_score") != observation.get("quality_score"):
        raise runner.RuntimeGateError(f"paired grade binding mismatch: {slot['slot_id']}")
    tokens = observation.get("all_agent_total_tokens")
    elapsed = observation.get("elapsed_seconds")
    if not isinstance(tokens, int) or isinstance(tokens, bool) or tokens < 0:
        raise runner.RuntimeGateError(f"paired tokens are unavailable: {slot['slot_id']}")
    if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0:
        raise runner.RuntimeGateError(f"paired elapsed is unavailable: {slot['slot_id']}")
    return {
        "slot": slot,
        "source": "new_dispatch",
        "status": "valid",
        "quality_score": observation["quality_score"],
        "mechanism_passed": observation["mechanism_passed"],
        "all_agent_total_tokens": tokens,
        "elapsed_seconds": elapsed,
        "evidence": {name: {"sha256": runner.base.sha256_file(path), "bytes": path.stat().st_size} for name, path in required.items()},
    }


def collect_reused_rows(plan: dict[str, Any], reuse_result: dict[str, Any]) -> list[dict[str, Any]]:
    source_by_case = {row["slot"]["case_id"]: row for row in reuse_result["cases"]}
    rows = []
    for slot in plan["reused_slots"]:
        source = source_by_case.get(slot["case_id"])
        if source is None or source.get("status") != "valid" or source.get("slot", {}).get("iteration") != 1:
            raise runner.RuntimeGateError(f"reused row is unavailable: {slot['slot_id']}")
        rows.append({
            "slot": slot,
            "source": "reused_candidate_only_n1",
            "source_result_id": reuse_result["result_id"],
            "status": "valid",
            "quality_score": source["quality_score"],
            "mechanism_passed": source["mechanism_passed"],
            "all_agent_total_tokens": source["all_agent_total_tokens"],
            "elapsed_seconds": source["elapsed_seconds"],
            "evidence": source["evidence"],
        })
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(rows) != 30 or any(row.get("status") != "valid" for row in rows):
        raise runner.RuntimeGateError("each paired arm requires 30 valid rows")
    scores = [row["quality_score"] for row in rows]
    tokens = [row["all_agent_total_tokens"] for row in rows]
    elapsed = [row["elapsed_seconds"] for row in rows]
    return {
        "valid_results": len(rows),
        "external_failures": 0,
        "quality_score_distribution": {str(score): scores.count(score) for score in sorted(set(scores))},
        "quality_score_mean": statistics.mean(scores),
        "quality_score_median": statistics.median(scores),
        "mechanism_passed": sum(row["mechanism_passed"] is True for row in rows),
        "mechanism_failed": sum(row["mechanism_passed"] is False for row in rows),
        "all_agent_total_tokens_sum": sum(tokens),
        "all_agent_total_tokens_median": statistics.median(tokens),
        "elapsed_seconds_sum": sum(elapsed),
        "elapsed_seconds_median": statistics.median(elapsed),
    }


def case_comparisons(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for case_index in range(1, 7):
        case_id = f"VCC-H0{case_index}"
        arm_rows = {arm: [row for row in rows if row["slot"]["arm"] == arm and row["slot"]["case_id"] == case_id] for arm in ("P001", "P002")}
        summaries = {arm: summarize_case(values) for arm, values in arm_rows.items()}
        output.append({
            "case_id": case_id,
            "P001": summaries["P001"],
            "P002": summaries["P002"],
            "delta_p002_minus_p001": {
                "all_agent_total_tokens_sum": summaries["P002"]["all_agent_total_tokens_sum"] - summaries["P001"]["all_agent_total_tokens_sum"],
                "elapsed_seconds_sum": summaries["P002"]["elapsed_seconds_sum"] - summaries["P001"]["elapsed_seconds_sum"],
            },
        })
    return output


def summarize_case(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(rows) != 5:
        raise runner.RuntimeGateError("each case arm requires five rows")
    scores = [row["quality_score"] for row in rows]
    return {
        "valid_results": 5,
        "quality_score_distribution": {str(score): scores.count(score) for score in sorted(set(scores))},
        "mechanism_passed": sum(row["mechanism_passed"] is True for row in rows),
        "all_agent_total_tokens_sum": sum(row["all_agent_total_tokens"] for row in rows),
        "elapsed_seconds_sum": sum(row["elapsed_seconds"] for row in rows),
    }


def build_result(*, repository_root: Path, preflight_path: Path, evidence_root: Path):
    repository_root = repository_root.resolve()
    preflight, plan = runner.validate_preflight(repository_root=repository_root, receipt_path=preflight_path)
    profile_path = runner.base.safe_repository_file(repository_root, plan["profile"], "paired profile")
    target_path = runner.base.safe_repository_file(repository_root, plan["target"], "target")
    binding = runner.validate_profile(repository_root=repository_root, profile_path=profile_path, target_path=target_path)
    new_rows = [collect_new_row(slot, evidence_root.resolve()) for slot in plan["dispatch_slots"]]
    reused_rows = collect_reused_rows(plan, binding["reuse_result"])
    rows_by_id = {row["slot"]["slot_id"]: row for row in new_rows + reused_rows}
    rows = [rows_by_id[slot["slot_id"]] for slot in plan["logical_slots"]]
    if len(rows_by_id) != 60:
        raise runner.RuntimeGateError("paired result does not contain 60 unique logical slots")
    arm_rows = {arm: [row for row in rows if row["slot"]["arm"] == arm] for arm in ("P001", "P002")}
    arm_summary = {arm: summarize(values) for arm, values in arm_rows.items()}
    p001, p002 = arm_summary["P001"], arm_summary["P002"]
    quality_gate = p002["quality_score_distribution"] == {"4": 30}
    tokens_delta = p002["all_agent_total_tokens_sum"] - p001["all_agent_total_tokens_sum"]
    elapsed_delta = p002["elapsed_seconds_sum"] - p001["elapsed_seconds_sum"]
    cost_gate = quality_gate and tokens_delta < 0 and elapsed_delta < 0
    result = {
        "schema_version": RESULT_SCHEMA,
        "result_id": "vcc6-p001-p002-n5-comparison-r1",
        "target": plan["target"],
        "profile": plan["profile"],
        "plan": preflight["plan"],
        "preflight": {
            "path": str(preflight_path.resolve().relative_to(repository_root)),
            "sha256": runner.base.sha256_file(preflight_path),
            "preflight_id": preflight["preflight_id"],
            "receipt_sha256": preflight["receipt_sha256"],
        },
        "arms": plan["arms"],
        "evaluation_set_ref": plan["evaluation_set_ref"],
        "rating_ref": plan["rating_ref"],
        "runtime_ref": plan["runtime_ref"],
        "token_accounting_ref": plan["token_accounting_ref"],
        "execution_code": preflight["execution_code"],
        "private_evidence_root": str(evidence_root.resolve()),
        "logical_slot_count": 60,
        "reused_slot_count": 6,
        "new_dispatch_slot_count": 54,
        "cases": rows,
        "arm_summary": arm_summary,
        "case_comparison": case_comparisons(rows),
        "comparison": {
            "validity_gate_passed": len(rows) == 60 and all(row["status"] == "valid" for row in rows),
            "p002_quality_gate_passed": quality_gate,
            "primary_cost_aggregate": "sum_over_30_valid_runs_per_arm",
            "delta_p002_minus_p001": {
                "all_agent_total_tokens_sum": tokens_delta,
                "elapsed_seconds_sum": elapsed_delta,
                "all_agent_total_tokens_percent": tokens_delta / p001["all_agent_total_tokens_sum"] * 100,
                "elapsed_seconds_percent": elapsed_delta / p001["elapsed_seconds_sum"] * 100,
            },
            "cost_improvement_gate_passed": cost_gate,
            "standard14_next_gate_passed": cost_gate,
        },
        "allowed_next_profile_class": "p002_standard14_n5" if cost_gate else None,
        "state": "paired_targeted_n5_gate_passed_standard14_n5_allowed" if cost_gate else "paired_targeted_n5_cost_gate_failed_stop_before_standard14",
    }
    result["result_sha256"] = runner.base.content_identity(result, "result_sha256")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_result(repository_root=args.repository_root, preflight_path=args.preflight, evidence_root=args.evidence_root)
    runner.base.write_once(args.output, runner.base.canonical_bytes(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

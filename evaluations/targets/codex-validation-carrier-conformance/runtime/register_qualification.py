#!/usr/bin/env python3
"""Register six private qualification observations as one public result receipt."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import statistics
from typing import Any


def _load_runner():
    path = Path(__file__).with_name("runner.py")
    spec = importlib.util.spec_from_file_location("codex_validation_carrier_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("qualification runner cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = _load_runner()
RESULT_SCHEMA = "codex-validation-carrier-qualification-result/v1"


def collect_row(slot: dict[str, Any], evidence_root: Path) -> dict[str, Any]:
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
        raise runner.RuntimeGateError(f"qualification evidence is incomplete: {slot['slot_id']}")
    observation = runner.adapter.load_object(required["observation"])
    grade = runner.adapter.load_object(required["grade"])
    if observation.get("slot") != slot or observation.get("status") != "valid":
        raise runner.RuntimeGateError(f"qualification observation is invalid: {slot['slot_id']}")
    if grade.get("case_id") != slot["case_id"] or grade.get("quality_score") != observation.get("quality_score"):
        raise runner.RuntimeGateError(f"qualification grade binding mismatch: {slot['slot_id']}")
    tokens = observation.get("all_agent_total_tokens")
    elapsed = observation.get("elapsed_seconds")
    if not isinstance(tokens, int) or isinstance(tokens, bool) or tokens < 0:
        raise runner.RuntimeGateError(f"qualification tokens are unavailable: {slot['slot_id']}")
    if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0:
        raise runner.RuntimeGateError(f"qualification elapsed is unavailable: {slot['slot_id']}")
    return {
        "slot": slot,
        "status": "valid",
        "quality_score": observation["quality_score"],
        "mechanism_passed": observation["mechanism_passed"],
        "all_agent_total_tokens": tokens,
        "elapsed_seconds": elapsed,
        "evidence": {name: {"sha256": runner.sha256_file(path), "bytes": path.stat().st_size} for name, path in required.items()},
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(rows) != 6 or any(row.get("status") != "valid" for row in rows):
        raise runner.RuntimeGateError("qualification requires six valid rows")
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


def build_result(*, repository_root: Path, preflight_path: Path, evidence_root: Path) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    preflight, plan = runner.validate_preflight(repository_root=repository_root, receipt_path=preflight_path)
    rows = [collect_row(slot, evidence_root.resolve()) for slot in plan["slots"]]
    result = {
        "schema_version": RESULT_SCHEMA,
        "result_id": "codex-validation-carrier-control-free-heldout-r1-n1-qualification-r1",
        "target": plan["target"],
        "profile": plan["profile"],
        "plan": preflight["plan"],
        "preflight": {
            "path": str(preflight_path.resolve().relative_to(repository_root)),
            "sha256": runner.sha256_file(preflight_path),
            "preflight_id": preflight["preflight_id"],
            "receipt_sha256": preflight["receipt_sha256"],
        },
        "prompt_set_identity": plan["prompt_set_identity"],
        "evaluation_set_ref": plan["evaluation_set_ref"],
        "rating_ref": plan["rating_ref"],
        "runtime_ref": plan["runtime_ref"],
        "token_accounting_ref": plan["token_accounting_ref"],
        "execution_code": preflight["execution_code"],
        "private_evidence_root": str(evidence_root.resolve()),
        "cases": rows,
        "summary": summarize(rows),
        "qualification": {
            "measurement_path": "passed",
            "all_cases_have_three_kpis": True,
            "control_free_quality": "retained_as_observed",
            "low_quality_rerun": False,
            "formal_comparison": "not_started",
            "candidate_creation": "not_authorized_by_this_result",
        },
        "state": "measurement_qualified_control_free_observed_not_formal_comparison",
    }
    result["result_sha256"] = runner.content_identity(result, "result_sha256")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_result(repository_root=args.repository_root, preflight_path=args.preflight, evidence_root=args.evidence_root)
    runner.write_once(args.output, runner.canonical_bytes(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

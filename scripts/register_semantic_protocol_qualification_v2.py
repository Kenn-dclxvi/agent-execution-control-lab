#!/usr/bin/env python3
"""Grade and register one complete semantic-protocol qualification run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys
from typing import Any

try:
    from .portable_semantic_conformance import grade_response
    from .run_semantic_protocol_qualification_v2 import (
        QualificationGateError,
        canonical_bytes,
        load_object,
        sha256_file,
        validate_preflight,
        write_once,
    )
except ImportError:
    from portable_semantic_conformance import grade_response
    from run_semantic_protocol_qualification_v2 import (
        QualificationGateError,
        canonical_bytes,
        load_object,
        sha256_file,
        validate_preflight,
        write_once,
    )


RESULT_SCHEMA = "portable-instruction-semantic-qualification-result/v1"
CONTROL_FREE_PROMPT_IDENTITY = "portable-semantic-a544769-control-free-r1"


def result_identity(plan: dict[str, Any]) -> str:
    plan_id = plan.get("plan_id")
    if not isinstance(plan_id, str) or plan_id.count("-dispatch-") != 1:
        raise QualificationGateError("qualification plan identity cannot bind result identity")
    return plan_id.replace("-dispatch-", "-qualification-", 1)


def quality_gate_result(plan: dict[str, Any], scores: list[int]) -> dict[str, Any]:
    prompt_identity = (plan.get("prompt_set_identity") or {}).get("name")
    if prompt_identity == CONTROL_FREE_PROMPT_IDENTITY:
        return {
            "quality_gate": "descriptive_not_an_admission_gate",
            "quality_gate_contract": "control_free_measurement_only",
            "comparison_reference": "not_applicable",
        }
    passed = len(scores) == 14 and all(score == 4 for score in scores)
    return {
        "quality_gate": "passed" if passed else "failed",
        "quality_gate_contract": "exact_all_14_score4",
        "comparison_reference": "authorized_after_quality_gate" if passed else "not_authorized",
    }


def collect_qualification(
    *,
    plan: dict[str, Any],
    output_root: Path,
    inputs: dict[str, Any],
    oracle: dict[str, Any],
    response_schema: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for slot in plan["slots"]:
        private = output_root.resolve() / slot["slot_id"] / "private"
        observation_path = private / "execution-observation.json"
        response_path = private / "final-response.json"
        if not observation_path.is_file() or not response_path.is_file():
            raise QualificationGateError(f"qualification slot is incomplete: {slot['slot_id']}")
        if (private / "execution-failure.json").exists():
            raise QualificationGateError(f"qualification slot has a failure receipt: {slot['slot_id']}")
        observation = load_object(observation_path)
        response = load_object(response_path)
        if observation.get("slot") != slot or observation.get("status") != "executor_complete_unrated":
            raise QualificationGateError(f"qualification observation is not admissible: {slot['slot_id']}")
        if response.get("case_id") != slot["case_id"]:
            raise QualificationGateError(f"qualification response case differs from slot: {slot['slot_id']}")
        usage = observation.get("token_accounting") or {}
        total_tokens = usage.get("all_agent_total_tokens")
        elapsed = observation.get("elapsed_seconds")
        if not isinstance(total_tokens, int) or total_tokens <= 0:
            raise QualificationGateError(f"qualification token total is unavailable: {slot['slot_id']}")
        if not isinstance(elapsed, (int, float)) or elapsed < 0:
            raise QualificationGateError(f"qualification elapsed value is unavailable: {slot['slot_id']}")
        rating = grade_response(inputs, oracle, response_schema, response)
        rows.append(
            {
                "slot": slot,
                "status": "valid",
                "quality_score": rating["quality_score"],
                "quality_status": rating["status"],
                "mechanism_passed": rating["mechanism_passed"],
                "mechanism_predicates": rating["mechanism_predicates"],
                "diagnostics": rating["diagnostics"],
                "all_agent_total_tokens": total_tokens,
                "elapsed_seconds": elapsed,
                "session_count": usage.get("session_count"),
                "response_sha256": sha256_file(response_path),
                "observation_sha256": sha256_file(observation_path),
            }
        )
    return rows


def build_result(
    *,
    repository_root: Path,
    plan_path: Path,
    preflight_path: Path,
    bundle_path: Path,
    output_root: Path,
    grader_path: Path,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    preflight, plan = validate_preflight(
        receipt_path=preflight_path,
        repository_root=repository_root,
        bundle_path=bundle_path,
    )
    target_path = repository_root / plan["target"]["path"]
    target_root = target_path.parent
    qualification_artifacts = plan.get("qualification_artifacts")
    if qualification_artifacts is None:
        inputs_path = target_root / "cases/heldout-r1/input-cases.json"
        oracle_path = target_root / "cases/heldout-r1/oracle.json"
        schema_path = target_root / "cases/heldout-r1/response.schema.json"
    else:
        inputs_path = repository_root / qualification_artifacts["cases"]["path"]
        oracle_path = repository_root / qualification_artifacts["oracle"]["path"]
        schema_path = repository_root / qualification_artifacts["response_schema"]["path"]
    rows = collect_qualification(
        plan=plan,
        output_root=output_root,
        inputs=load_object(inputs_path),
        oracle=load_object(oracle_path),
        response_schema=load_object(schema_path),
    )
    scores = [row["quality_score"] for row in rows]
    tokens = [row["all_agent_total_tokens"] for row in rows]
    elapsed = [row["elapsed_seconds"] for row in rows]
    result = {
        "schema_version": RESULT_SCHEMA,
        "result_id": result_identity(plan),
        "target": plan["target"],
        "profile": plan["profile"],
        "plan": {
            "path": str(plan_path.resolve().relative_to(repository_root)),
            "sha256": sha256_file(plan_path),
            "plan_id": plan["plan_id"],
        },
        "preflight": {
            "path": str(preflight_path.resolve().relative_to(repository_root)),
            "sha256": sha256_file(preflight_path),
            "preflight_id": preflight["preflight_id"],
        },
        "grader": {
            "path": str(grader_path.resolve().relative_to(repository_root)),
            "sha256": sha256_file(grader_path),
            "rating_contract": plan["rating_ref"],
        },
        "private_output_root": str(output_root.resolve()),
        "raw_artifacts_private": True,
        "summary": {
            "authorized_slots": len(plan["slots"]),
            "issued_slots": len(rows),
            "valid_results": len(rows),
            "external_failures": 0,
            "schema_valid_results": len(rows),
            "score_distribution": {str(score): scores.count(score) for score in range(1, 5)},
            "score4_results": scores.count(4),
            "mechanism_passed_results": sum(row["mechanism_passed"] for row in rows),
            "all_agent_total_tokens_median": statistics.median(tokens),
            "all_agent_total_tokens_min": min(tokens),
            "all_agent_total_tokens_max": max(tokens),
            "elapsed_seconds_median": statistics.median(elapsed),
            "elapsed_seconds_min": min(elapsed),
            "elapsed_seconds_max": max(elapsed),
        },
        "cases": rows,
        "qualification": {
            "measurement_gate": "passed",
            **quality_gate_result(plan, scores),
            "adoption": "not_decided",
            "release": "not_decided",
            "runtime_projection": "not_authorized",
        },
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--grader", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_result(
            repository_root=args.repository_root,
            plan_path=args.plan,
            preflight_path=args.preflight,
            bundle_path=args.bundle,
            output_root=args.output_root,
            grader_path=args.grader,
        )
        write_once(args.output.resolve(), canonical_bytes(result))
    except (OSError, QualificationGateError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

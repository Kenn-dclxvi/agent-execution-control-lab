#!/usr/bin/env python3
"""Register N=20 from reused N=5 rows and newly issued i006-i020 rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys
from typing import Any

try:
    from . import register_semantic_protocol_qualification_v2 as base
    from .run_semantic_protocol_qualification_v4 import (
        QualificationGateError, canonical_bytes, load_object, sha256_file,
        validate_preflight, write_once,
    )
except ImportError:
    import register_semantic_protocol_qualification_v2 as base
    from run_semantic_protocol_qualification_v4 import (
        QualificationGateError, canonical_bytes, load_object, sha256_file,
        validate_preflight, write_once,
    )


def quality_gate_result(scores: list[int]) -> dict[str, Any]:
    passed = len(scores) == 280 and all(score == 4 for score in scores)
    return {
        "quality_gate": "passed" if passed else "failed",
        "quality_gate_contract": "exact_all_280_score4",
        "comparison_reference": "authorized_after_quality_gate" if passed else "not_authorized",
    }


def build_result(
    *, repository_root: Path, plan_path: Path, preflight_path: Path,
    bundle_path: Path, output_root: Path, retry_output_root: Path | None,
    grader_path: Path,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    preflight, plan = validate_preflight(
        receipt_path=preflight_path, repository_root=repository_root,
        bundle_path=bundle_path,
    )
    if plan_path.resolve() != (repository_root / preflight["plan"]["path"]).resolve():
        raise QualificationGateError("registrar plan differs from preflight plan")
    qualification_artifacts = plan["qualification_artifacts"]
    primary_slots: list[dict[str, Any]] = []
    retry_slots: list[dict[str, Any]] = []
    excluded_attempts: list[dict[str, Any]] = []
    for slot in plan["slots"]:
        primary_private = output_root.resolve() / slot["slot_id"] / "private"
        retry_private = (
            retry_output_root.resolve() / slot["slot_id"] / "private"
            if retry_output_root is not None else None
        )
        if (primary_private / "execution-observation.json").is_file():
            if retry_private is not None and retry_private.exists():
                raise QualificationGateError(f"valid slot was retried: {slot['slot_id']}")
            primary_slots.append(slot)
            continue
        failure_path = primary_private / "execution-failure.json"
        if (
            not failure_path.is_file() or retry_private is None
            or not (retry_private / "execution-observation.json").is_file()
        ):
            raise QualificationGateError(f"slot lacks valid primary or external retry: {slot['slot_id']}")
        if (retry_private / "execution-failure.json").exists():
            raise QualificationGateError(f"external retry failed: {slot['slot_id']}")
        failure = load_object(failure_path)
        if failure.get("status") != "excluded_external_failure" or failure.get("slot") != slot:
            raise QualificationGateError(f"excluded attempt binding mismatch: {slot['slot_id']}")
        retry_slots.append(slot)
        excluded_attempts.append({
            "slot": slot,
            "status": "excluded_external_failure",
            "reason": failure.get("reason"),
            "private_output_root": str(output_root.resolve()),
            "failure_receipt_sha256": sha256_file(failure_path),
            "events_sha256": sha256_file(primary_private / "codex-events.jsonl"),
            "replacement_private_output_root": str(retry_output_root.resolve()),
        })
    inputs = load_object(repository_root / qualification_artifacts["cases"]["path"])
    oracle = load_object(repository_root / qualification_artifacts["oracle"]["path"])
    response_schema = load_object(repository_root / qualification_artifacts["response_schema"]["path"])
    retry_rows = (
        base.collect_qualification(
            plan={**plan, "slots": retry_slots}, output_root=retry_output_root,
            inputs=inputs, oracle=oracle, response_schema=response_schema,
        )
        if retry_slots and retry_output_root is not None
        else []
    )
    new_rows = [
        *base.collect_qualification(
            plan={**plan, "slots": primary_slots}, output_root=output_root,
            inputs=inputs, oracle=oracle, response_schema=response_schema,
        ),
        *retry_rows,
    ]
    reference = preflight["existing_iteration_result"]
    reused_rows = load_object(repository_root / reference["path"])["cases"]
    rows = sorted(
        [*reused_rows, *new_rows],
        key=lambda row: (row["slot"]["case_id"], row["slot"]["iteration"]),
    )
    case_ids = sorted({row["slot"]["case_id"] for row in rows})
    expected = [(case_id, iteration) for case_id in case_ids for iteration in range(1, 21)]
    observed = [(row["slot"]["case_id"], row["slot"]["iteration"]) for row in rows]
    if observed != expected or len({row["slot"]["slot_id"] for row in rows}) != 280:
        raise QualificationGateError("aggregate result does not contain exact N=20 coverage")
    scores = [row["quality_score"] for row in rows]
    tokens = [row["all_agent_total_tokens"] for row in rows]
    elapsed = [row["elapsed_seconds"] for row in rows]
    result = {
        "schema_version": base.RESULT_SCHEMA,
        "result_id": base.result_identity(plan),
        "target": plan["target"],
        "profile": plan["profile"],
        "plan": {"path": str(plan_path.resolve().relative_to(repository_root)), "sha256": sha256_file(plan_path), "plan_id": plan["plan_id"]},
        "preflight": {"path": str(preflight_path.resolve().relative_to(repository_root)), "sha256": sha256_file(preflight_path), "preflight_id": preflight["preflight_id"]},
        "existing_iteration_result": reference,
        "grader": {"path": str(grader_path.resolve().relative_to(repository_root)), "sha256": sha256_file(grader_path), "rating_contract": plan["rating_ref"]},
        "private_output_root": str(output_root.resolve()),
        "retry_private_output_root": str(retry_output_root.resolve()) if retry_output_root is not None else None,
        "raw_artifacts_private": True,
        "excluded_attempts": excluded_attempts,
        "summary": {
            "authorized_slots": 280, "reused_slots": 70,
            "newly_authorized_slots": len(plan["slots"]), "issued_slots": len(new_rows),
            "excluded_attempts": len(excluded_attempts), "valid_results": len(rows),
            "external_failures": 0, "schema_valid_results": len(rows),
            "score_distribution": {str(score): scores.count(score) for score in range(1, 5)},
            "score4_results": scores.count(4),
            "mechanism_passed_results": sum(row["mechanism_passed"] for row in rows),
            "all_agent_total_tokens_median": statistics.median(tokens),
            "all_agent_total_tokens_min": min(tokens), "all_agent_total_tokens_max": max(tokens),
            "elapsed_seconds_median": statistics.median(elapsed),
            "elapsed_seconds_min": min(elapsed), "elapsed_seconds_max": max(elapsed),
        },
        "cases": rows,
        "qualification": {
            "measurement_gate": "passed", **quality_gate_result(scores),
            "adoption": "not_decided", "release": "not_decided",
            "runtime_projection": "not_authorized",
        },
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repository-root", "plan", "preflight", "bundle", "output-root", "grader", "output"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--retry-output-root", type=Path)
    args = parser.parse_args()
    try:
        result = build_result(
            repository_root=args.repository_root, plan_path=args.plan,
            preflight_path=args.preflight, bundle_path=args.bundle,
            output_root=args.output_root, retry_output_root=args.retry_output_root,
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

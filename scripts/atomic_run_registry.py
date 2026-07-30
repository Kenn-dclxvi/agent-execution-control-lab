#!/usr/bin/env python3
"""Append-only atomic run registry and count-free derived analysis."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import uuid
from pathlib import Path
from typing import Any

if __package__:
    from .evaluation_loop import (
        EXECUTION_SCHEMA_V3,
        TOKEN_ACCOUNTING,
        EvaluationError,
        frozen_set,
        identity_sha256,
        load_json,
        load_reference_result,
        require_non_empty_string,
        require_positive,
        token_accounting_for_result,
        utc_now,
        write_json_once,
    )
else:
    from evaluation_loop import (
        EXECUTION_SCHEMA_V3,
        TOKEN_ACCOUNTING,
        EvaluationError,
        frozen_set,
        identity_sha256,
        load_json,
        load_reference_result,
        require_non_empty_string,
        require_positive,
        token_accounting_for_result,
        utc_now,
        write_json_once,
    )


ATOMIC_RUN_SCHEMA = "the-caption-prompt.atomic-run/v1"
RUN_POOL_SCHEMA = "the-caption-prompt.run-pool/v1"
DISPATCH_PLAN_SCHEMA = "the-caption-prompt.atomic-dispatch-plan/v1"
SELECTION_SCHEMA = "the-caption-prompt.atomic-run-selection/v1"
ANALYSIS_SCHEMA = "the-caption-prompt.atomic-run-analysis/v1"
COMPARISON_SCHEMA = "the-caption-prompt.atomic-run-comparison/v1"


def split_conditions(compatibility: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Move count and scheduler declarations out of effective run compatibility."""
    effective = json.loads(json.dumps(compatibility))
    coverage = effective.pop("coverage", None)
    repetition = effective.pop("repetition_condition", None)
    executor = effective.get("executor_parameters")
    max_workers = None
    if isinstance(executor, dict):
        max_workers = executor.pop("max_workers", None)
    provenance = {
        "coverage": coverage,
        "repetition_condition": repetition,
        "max_workers": max_workers,
    }
    return effective, provenance


def atomic_id(run_id: str, accounting: dict[str, str]) -> str:
    return identity_sha256({"run_id": run_id, "token_accounting": accounting})


def write_or_verify(path: Path, value: dict[str, Any], volatile: set[str]) -> None:
    if not path.exists():
        write_json_once(path, value)
        return
    existing = load_json(path)
    left = {key: item for key, item in existing.items() if key not in volatile}
    right = {key: item for key, item in value.items() if key not in volatile}
    if left != right:
        raise EvaluationError(f"existing append-only artifact conflicts: {path}")


def build_record(
    *,
    run_id: str,
    prompt_identity: dict[str, Any],
    case_id: str,
    fixture: Any,
    effective_common: dict[str, Any],
    provenance: dict[str, Any],
    sample_id: str,
    accounting: dict[str, str],
    quality_score: int,
    total_tokens: int,
    elapsed_seconds: float,
    source: dict[str, Any],
) -> dict[str, Any]:
    effective = {
        **effective_common,
        "case_id": case_id,
        "fixture": fixture,
    }
    comparison_block_key = identity_sha256(effective)
    run_condition_key = identity_sha256(
        {"prompt_set_identity": prompt_identity, "effective_conditions": effective}
    )
    stratum = {"max_workers": provenance.get("max_workers")}
    record = {
        "schema_version": ATOMIC_RUN_SCHEMA,
        "atomic_run_id": atomic_id(run_id, accounting),
        "run_id": run_id,
        "sample_id": sample_id,
        "prompt_set_identity": prompt_identity,
        "prompt_set_identity_sha256": identity_sha256(prompt_identity),
        "case_id": case_id,
        "effective_conditions": effective,
        "comparison_block_key": comparison_block_key,
        "run_condition_key": run_condition_key,
        "execution_provenance": provenance,
        "execution_stratum": stratum,
        "execution_stratum_key": identity_sha256(stratum),
        "token_accounting": accounting,
        "quality_score": quality_score,
        "total_tokens": total_tokens,
        "elapsed_seconds": elapsed_seconds,
        "source": source,
        "registered_at": utc_now(),
    }
    record["record_content_sha256"] = identity_sha256(record)
    return record


def load_atomic_run(registry: Path, record_id: str) -> dict[str, Any]:
    record = load_json(registry / "runs" / f"{record_id}.json")
    if record.get("schema_version") != ATOMIC_RUN_SCHEMA:
        raise EvaluationError("atomic run has an unsupported schema_version")
    if record.get("atomic_run_id") != record_id:
        raise EvaluationError("atomic run identity does not match its path")
    content = dict(record)
    stored = content.pop("record_content_sha256", None)
    if stored != identity_sha256(content):
        raise EvaluationError("atomic run content SHA-256 does not match")
    return record


def registry_runs(registry: Path) -> list[dict[str, Any]]:
    return [load_atomic_run(registry, path.stem) for path in sorted((registry / "runs").glob("*.json"))]


def pool_document(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        raise EvaluationError("cannot build a run pool without records")
    prompt_identity = records[0]["prompt_set_identity"]
    if any(record["prompt_set_identity"] != prompt_identity for record in records):
        raise EvaluationError("one run pool may contain only one prompt identity")
    case_ids = sorted({record["case_id"] for record in records})
    blocks: dict[str, str] = {}
    comparison_conditions: dict[str, Any] = {}
    for case_id in case_ids:
        selected = [record for record in records if record["case_id"] == case_id]
        keys = {record["comparison_block_key"] for record in selected}
        if len(keys) != 1:
            raise EvaluationError(f"effective conditions differ within case: {case_id}")
        blocks[case_id] = next(iter(keys))
        comparison_conditions[case_id] = selected[0]["effective_conditions"]
    comparison_key = identity_sha256(comparison_conditions)
    pool_key = identity_sha256(
        {
            "prompt_set_identity": prompt_identity,
            "comparison_block_keys": blocks,
        }
    )
    document = {
        "schema_version": RUN_POOL_SCHEMA,
        "pool_key": pool_key,
        "prompt_set_identity": prompt_identity,
        "prompt_set_identity_sha256": identity_sha256(prompt_identity),
        "case_ids": case_ids,
        "comparison_block_keys": blocks,
        "comparison_key": comparison_key,
        "effective_conditions_by_case": comparison_conditions,
        "created_at": utc_now(),
    }
    document["pool_content_sha256"] = identity_sha256(document)
    return document


def store_records_and_pool(registry: Path, records: list[dict[str, Any]]) -> dict[str, Any]:
    for record in records:
        write_or_verify(
            registry / "runs" / f"{record['atomic_run_id']}.json",
            record,
            {"registered_at", "record_content_sha256"},
        )
    pool = pool_document(records)
    pool_path = registry / "pools" / f"{pool['pool_key']}.json"
    write_or_verify(pool_path, pool, {"created_at", "pool_content_sha256"})
    return pool


def import_result(args: argparse.Namespace) -> dict[str, Any]:
    registry = Path(args.registry).resolve()
    result = load_reference_result(registry, args.result_id)
    compatibility = result["compatibility"]
    effective, provenance = split_conditions(compatibility)
    fixtures = effective.pop("fixtures", None)
    if not isinstance(fixtures, dict):
        raise EvaluationError("source result has no fixture identities")
    accounting = token_accounting_for_result(result)
    records: list[dict[str, Any]] = []
    for row in result.get("case_results", []):
        case_id = require_non_empty_string(row.get("case_id"), "case result case_id")
        iteration = require_positive(row.get("iteration"), "case result iteration")
        run_id = require_non_empty_string(row.get("run_id"), "case result run_id")
        sample_id = f"legacy:{result['compatibility_key']}:{iteration}"
        records.append(
            build_record(
                run_id=run_id,
                prompt_identity=result["prompt_set_identity"],
                case_id=case_id,
                fixture=fixtures[case_id],
                effective_common=effective,
                provenance=provenance,
                sample_id=sample_id,
                accounting=accounting,
                quality_score=row["quality_score"],
                total_tokens=row["total_tokens"],
                elapsed_seconds=row["elapsed_seconds"],
                source={
                    "kind": "prompt_set_result",
                    "result_id": result["result_id"],
                    "result_content_sha256": result["result_content_sha256"],
                },
            )
        )
    pool = store_records_and_pool(registry, records)
    return {
        "layer": 4,
        "result_id": result["result_id"],
        "pool_key": pool["pool_key"],
        "comparison_key": pool["comparison_key"],
        "registered_run_count": len(records),
    }


def register_cycle_run(args: argparse.Namespace) -> dict[str, Any]:
    registry = Path(args.registry).resolve()
    cycle = Path(args.cycle).resolve()
    run_id = require_non_empty_string(args.run_id, "run id")
    binding = load_json(cycle / "layer2" / "bindings" / f"{run_id}.json")
    execution = load_json(cycle / "layer2" / "evidence" / run_id / "execution.json")
    rating = load_json(cycle / "layer3" / "ratings" / f"{run_id}.json")
    if binding.get("status") != "valid" or execution.get("status") != "valid":
        raise EvaluationError("only valid runs can enter the atomic registry")
    if execution.get("schema_version") != EXECUTION_SCHEMA_V3:
        raise EvaluationError("atomic registration requires execution schema v3")
    if execution.get("token_accounting") != TOKEN_ACCOUNTING:
        raise EvaluationError("atomic registration requires all-agent token accounting v1")
    manifest = frozen_set(cycle)
    case_id = binding["case_id"]
    case = next((item for item in manifest["cases"] if item["id"] == case_id), None)
    if case is None:
        raise EvaluationError(f"frozen set has no case: {case_id}")
    conditions = binding["comparison_conditions"]
    compatibility = {
        "evaluation_set": {
            "set_id": manifest["set_id"],
            "revision": manifest["revision"],
            "identity_sha256": manifest["identity_sha256"],
        },
        "fixtures": {case_id: case["fixture_identity"]},
        **conditions,
        "coverage": {"case_ids": [case_id], "iterations": [binding["iteration"]]},
    }
    effective, provenance = split_conditions(compatibility)
    fixtures = effective.pop("fixtures")
    sample_id = binding.get("sample_id") or f"run:{run_id}"
    record = build_record(
        run_id=run_id,
        prompt_identity=binding["prompt_set_identity"],
        case_id=case_id,
        fixture=fixtures[case_id],
        effective_common=effective,
        provenance=provenance,
        sample_id=sample_id,
        accounting=TOKEN_ACCOUNTING,
        quality_score=rating["score"],
        total_tokens=execution["total_tokens"],
        elapsed_seconds=execution["elapsed_seconds"],
        source={
            "kind": "cycle_run",
            "cycle_layer1_identity_sha256": manifest["identity_sha256"],
        },
    )
    if args.pool_key:
        pool = load_pool(registry, args.pool_key)
        if (
            pool["prompt_set_identity_sha256"] != record["prompt_set_identity_sha256"]
            or pool["comparison_block_keys"].get(case_id) != record["comparison_block_key"]
        ):
            raise EvaluationError("registered run does not belong to the requested pool")
        write_or_verify(
            registry / "runs" / f"{record['atomic_run_id']}.json",
            record,
            {"registered_at", "record_content_sha256"},
        )
    else:
        matches = []
        for path in sorted((registry / "pools").glob("*.json")):
            candidate = load_pool(registry, path.stem)
            if (
                candidate["prompt_set_identity_sha256"] == record["prompt_set_identity_sha256"]
                and candidate["comparison_block_keys"].get(case_id)
                == record["comparison_block_key"]
            ):
                matches.append(candidate)
        if len(matches) > 1:
            raise EvaluationError("run matches multiple pools; specify --pool-key")
        if matches:
            pool = matches[0]
            write_or_verify(
                registry / "runs" / f"{record['atomic_run_id']}.json",
                record,
                {"registered_at", "record_content_sha256"},
            )
        else:
            pool = store_records_and_pool(registry, [record])
    return {
        "layer": 4,
        "atomic_run_id": record["atomic_run_id"],
        "pool_key": pool["pool_key"],
        "comparison_key": pool["comparison_key"],
    }


def load_pool(registry: Path, pool_key: str) -> dict[str, Any]:
    pool = load_json(registry / "pools" / f"{pool_key}.json")
    if pool.get("schema_version") != RUN_POOL_SCHEMA or pool.get("pool_key") != pool_key:
        raise EvaluationError("run pool identity is invalid")
    content = dict(pool)
    stored = content.pop("pool_content_sha256", None)
    if stored != identity_sha256(content):
        raise EvaluationError("run pool content SHA-256 does not match")
    return pool


def runs_for_pool(registry: Path, pool: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        record
        for record in registry_runs(registry)
        if record["prompt_set_identity_sha256"] == pool["prompt_set_identity_sha256"]
        and record["case_id"] in pool["comparison_block_keys"]
        and record["comparison_block_key"] == pool["comparison_block_keys"][record["case_id"]]
    ]


def complete_samples(records: list[dict[str, Any]], case_ids: list[str]) -> dict[str, dict[str, dict[str, Any]]]:
    grouped: dict[str, dict[str, dict[str, Any]]] = {}
    for record in records:
        sample = grouped.setdefault(record["sample_id"], {})
        if record["case_id"] in sample:
            raise EvaluationError(
                f"duplicate case in atomic sample: {record['sample_id']} / {record['case_id']}"
            )
        sample[record["case_id"]] = record
    return {
        sample_id: rows
        for sample_id, rows in grouped.items()
        if sorted(rows) == case_ids
    }


def plan_missing(args: argparse.Namespace) -> dict[str, Any]:
    registry = Path(args.registry).resolve()
    pool = load_pool(registry, args.pool_key)
    desired = require_positive(args.desired_count, "desired count")
    complete = complete_samples(runs_for_pool(registry, pool), pool["case_ids"])
    existing = len(complete)
    missing_count = max(0, desired - existing)
    plan_id = uuid.uuid4().hex
    missing_slots = []
    for dispatch_iteration in range(1, missing_count + 1):
        sample_id = f"planned:{plan_id}:{uuid.uuid4().hex}"
        for case_id in pool["case_ids"]:
            missing_slots.append(
                {
                    "sample_id": sample_id,
                    "case_id": case_id,
                    "dispatch_iteration": dispatch_iteration,
                    "comparison_block_key": pool["comparison_block_keys"][case_id],
                }
            )
    plan = {
        "schema_version": DISPATCH_PLAN_SCHEMA,
        "plan_id": plan_id,
        "pool_key": pool["pool_key"],
        "pool_content_sha256": pool["pool_content_sha256"],
        "desired_count": desired,
        "existing_complete_sample_count": existing,
        "missing_sample_count": missing_count,
        "missing_slots": missing_slots,
        "created_at": utc_now(),
    }
    plan["plan_content_sha256"] = identity_sha256(plan)
    output = Path(args.output).resolve()
    write_json_once(output, plan)
    return {
        "layer": 1,
        "artifact": str(output),
        "pool_key": pool["pool_key"],
        "existing_complete_sample_count": existing,
        "desired_count": desired,
        "missing_sample_count": missing_count,
        "missing_slot_count": len(missing_slots),
    }


def select_runs(args: argparse.Namespace) -> dict[str, Any]:
    registry = Path(args.registry).resolve()
    pool = load_pool(registry, args.pool_key)
    count = require_positive(args.count, "selection count")
    complete = complete_samples(runs_for_pool(registry, pool), pool["case_ids"])
    ordered = sorted(
        complete.items(),
        key=lambda item: (
            max(row["registered_at"] for row in item[1].values()),
            item[0],
        ),
    )
    if len(ordered) < count:
        raise EvaluationError(
            f"run pool has only {len(ordered)} complete samples; requested {count}"
        )
    chosen = ordered[:count]
    selection_id = uuid.uuid4().hex
    selection = {
        "schema_version": SELECTION_SCHEMA,
        "selection_id": selection_id,
        "pool_key": pool["pool_key"],
        "pool_content_sha256": pool["pool_content_sha256"],
        "comparison_key": pool["comparison_key"],
        "sample_ids": [sample_id for sample_id, _ in chosen],
        "atomic_run_ids": [
            rows[case_id]["atomic_run_id"]
            for sample_id, rows in chosen
            for case_id in pool["case_ids"]
        ],
        "case_ids": pool["case_ids"],
        "created_at": utc_now(),
    }
    selection["selection_content_sha256"] = identity_sha256(selection)
    output = Path(args.output).resolve()
    write_json_once(output, selection)
    return {
        "layer": 4,
        "artifact": str(output),
        "selection_id": selection_id,
        "sample_count": len(chosen),
        "run_count": len(selection["atomic_run_ids"]),
    }


def load_selection(path: Path) -> dict[str, Any]:
    selection = load_json(path)
    if selection.get("schema_version") != SELECTION_SCHEMA:
        raise EvaluationError("run selection has an unsupported schema_version")
    content = dict(selection)
    stored = content.pop("selection_content_sha256", None)
    if stored != identity_sha256(content):
        raise EvaluationError("run selection content SHA-256 does not match")
    return selection


def aggregate_selection(args: argparse.Namespace) -> dict[str, Any]:
    registry = Path(args.registry).resolve()
    selection_path = Path(args.selection).resolve()
    selection = load_selection(selection_path)
    pool = load_pool(registry, selection["pool_key"])
    records = {
        record_id: load_atomic_run(registry, record_id)
        for record_id in selection["atomic_run_ids"]
    }
    per_sample = []
    strata: dict[str, list[dict[str, Any]]] = {}
    for sample_id in selection["sample_ids"]:
        selected = [record for record in records.values() if record["sample_id"] == sample_id]
        if sorted(record["case_id"] for record in selected) != pool["case_ids"]:
            raise EvaluationError(f"selection sample is incomplete: {sample_id}")
        row = {
            "sample_id": sample_id,
            "quality_score": sum(record["quality_score"] for record in selected)
            / (4 * len(selected))
            * 100,
            "total_tokens": sum(record["total_tokens"] for record in selected),
            "elapsed_seconds": sum(record["elapsed_seconds"] for record in selected),
        }
        per_sample.append(row)
        stratum_keys = {record["execution_stratum_key"] for record in selected}
        if len(stratum_keys) == 1:
            strata.setdefault(next(iter(stratum_keys)), []).append(row)
    median = {
        key: statistics.median(row[key] for row in per_sample)
        for key in ("quality_score", "total_tokens", "elapsed_seconds")
    }
    analysis_id = uuid.uuid4().hex
    analysis = {
        "schema_version": ANALYSIS_SCHEMA,
        "analysis_id": analysis_id,
        "selection": {
            "path": str(selection_path),
            "selection_id": selection["selection_id"],
            "content_sha256": selection["selection_content_sha256"],
        },
        "pool_key": pool["pool_key"],
        "comparison_key": pool["comparison_key"],
        "prompt_set_identity": pool["prompt_set_identity"],
        "case_ids": pool["case_ids"],
        "sample_count": len(per_sample),
        "run_count": len(records),
        "samples": per_sample,
        "median": median,
        "strata": [
            {
                "execution_stratum_key": key,
                "sample_count": len(rows),
                "median": {
                    metric: statistics.median(row[metric] for row in rows)
                    for metric in ("quality_score", "total_tokens", "elapsed_seconds")
                },
            }
            for key, rows in sorted(strata.items())
        ],
        "created_at": utc_now(),
    }
    analysis["analysis_content_sha256"] = identity_sha256(analysis)
    output = Path(args.output).resolve()
    write_json_once(output, analysis)
    return {
        "layer": 4,
        "artifact": str(output),
        "analysis_id": analysis_id,
        "sample_count": len(per_sample),
        "run_count": len(records),
        "stratum_count": len(strata),
    }


def load_analysis(path: Path) -> dict[str, Any]:
    analysis = load_json(path)
    if analysis.get("schema_version") != ANALYSIS_SCHEMA:
        raise EvaluationError("atomic analysis has an unsupported schema_version")
    content = dict(analysis)
    stored = content.pop("analysis_content_sha256", None)
    if stored != identity_sha256(content):
        raise EvaluationError("atomic analysis content SHA-256 does not match")
    return analysis


def compare_analyses(args: argparse.Namespace) -> dict[str, Any]:
    reference_path = Path(args.reference).resolve()
    candidate_path = Path(args.candidate).resolve()
    reference = load_analysis(reference_path)
    candidate = load_analysis(candidate_path)
    if candidate["comparison_key"] != reference["comparison_key"]:
        raise EvaluationError("atomic analyses have different effective comparison conditions")
    if candidate["case_ids"] != reference["case_ids"]:
        raise EvaluationError("atomic analyses have different case coverage")
    if candidate["sample_count"] != reference["sample_count"]:
        raise EvaluationError("atomic analyses have different selected sample counts")
    differences = {
        key: candidate["median"][key] - reference["median"][key]
        for key in ("quality_score", "total_tokens", "elapsed_seconds")
    }
    ref_strata = {item["execution_stratum_key"]: item for item in reference["strata"]}
    cand_strata = {item["execution_stratum_key"]: item for item in candidate["strata"]}
    matched_strata = []
    for key in sorted(set(ref_strata).intersection(cand_strata)):
        left = ref_strata[key]
        right = cand_strata[key]
        matched_strata.append(
            {
                "execution_stratum_key": key,
                "reference_sample_count": left["sample_count"],
                "candidate_sample_count": right["sample_count"],
                "differences": {
                    metric: right["median"][metric] - left["median"][metric]
                    for metric in ("quality_score", "total_tokens", "elapsed_seconds")
                },
            }
        )
    comparison = {
        "schema_version": COMPARISON_SCHEMA,
        "reference": {
            "path": str(reference_path),
            "analysis_id": reference["analysis_id"],
            "prompt_set_identity": reference["prompt_set_identity"],
        },
        "candidate": {
            "path": str(candidate_path),
            "analysis_id": candidate["analysis_id"],
            "prompt_set_identity": candidate["prompt_set_identity"],
        },
        "comparison_key": reference["comparison_key"],
        "sample_count": reference["sample_count"],
        "differences": differences,
        "matched_strata": matched_strata,
        "strata_balance": (
            "matched"
            if {key: item["sample_count"] for key, item in ref_strata.items()}
            == {key: item["sample_count"] for key, item in cand_strata.items()}
            else "different"
        ),
        "generated_at": utc_now(),
    }
    output = Path(args.output).resolve()
    write_json_once(output, comparison)
    return {
        "layer": 4,
        "artifact": str(output),
        "sample_count": reference["sample_count"],
        "matched_stratum_count": len(matched_strata),
        "strata_balance": comparison["strata_balance"],
    }


def query_runs(args: argparse.Namespace) -> dict[str, Any]:
    registry = Path(args.registry).resolve()
    selected = registry_runs(registry)
    if args.pool_key:
        pool = load_pool(registry, args.pool_key)
        selected = runs_for_pool(registry, pool)
    if args.case_id:
        selected = [record for record in selected if record["case_id"] == args.case_id]
    return {
        "schema_version": "the-caption-prompt.atomic-run-query/v1",
        "count": len(selected),
        "runs": [
            {
                "atomic_run_id": record["atomic_run_id"],
                "sample_id": record["sample_id"],
                "case_id": record["case_id"],
                "pool_prompt_identity_sha256": record["prompt_set_identity_sha256"],
                "comparison_block_key": record["comparison_block_key"],
            }
            for record in selected
        ],
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="subcommand", required=True)

    imported = commands.add_parser("import-result")
    imported.add_argument("--registry", required=True)
    imported.add_argument("--result-id", required=True)
    imported.set_defaults(handler=import_result)

    registered = commands.add_parser("register-run")
    registered.add_argument("--registry", required=True)
    registered.add_argument("--cycle", required=True)
    registered.add_argument("--run-id", required=True)
    registered.add_argument("--pool-key")
    registered.set_defaults(handler=register_cycle_run)

    query = commands.add_parser("query-runs")
    query.add_argument("--registry", required=True)
    query.add_argument("--pool-key")
    query.add_argument("--case-id")
    query.set_defaults(handler=query_runs)

    missing = commands.add_parser("plan-missing")
    missing.add_argument("--registry", required=True)
    missing.add_argument("--pool-key", required=True)
    missing.add_argument("--desired-count", type=int, required=True)
    missing.add_argument("--output", required=True)
    missing.set_defaults(handler=plan_missing)

    select = commands.add_parser("select-runs")
    select.add_argument("--registry", required=True)
    select.add_argument("--pool-key", required=True)
    select.add_argument("--count", type=int, required=True)
    select.add_argument("--output", required=True)
    select.set_defaults(handler=select_runs)

    aggregate = commands.add_parser("aggregate-selection")
    aggregate.add_argument("--registry", required=True)
    aggregate.add_argument("--selection", required=True)
    aggregate.add_argument("--output", required=True)
    aggregate.set_defaults(handler=aggregate_selection)

    compare = commands.add_parser("compare-analyses")
    compare.add_argument("--reference", required=True)
    compare.add_argument("--candidate", required=True)
    compare.add_argument("--output", required=True)
    compare.set_defaults(handler=compare_analyses)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        result = args.handler(args)
    except (EvaluationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

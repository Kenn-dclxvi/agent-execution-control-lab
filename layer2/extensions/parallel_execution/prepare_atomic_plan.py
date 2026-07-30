#!/usr/bin/env python3
"""Materialize only missing atomic runs into one resource-class global queue plan."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

try:
    from .parallel_runner import ParallelRunError, write_json_once
    from .prepare_global_plan import DEFAULT_MAX_WORKERS, load_duration_hints
    from .prepare_plan import collect_templates
except ImportError:
    from parallel_runner import ParallelRunError, write_json_once
    from prepare_global_plan import DEFAULT_MAX_WORKERS, load_duration_hints
    from prepare_plan import collect_templates

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.atomic_run_registry import (  # noqa: E402
    DISPATCH_PLAN_SCHEMA,
    EvaluationError,
    identity_sha256,
    load_json,
    load_pool,
    split_conditions,
)


def prepare_atomic_plan(
    *,
    templates: list[Path],
    dispatch_plan_path: Path,
    registry: Path,
    cycle: Path,
    evaluator: Path,
    duration_hints_path: Path,
    resource_class: dict[str, Any],
    output: Path,
    max_workers: int = DEFAULT_MAX_WORKERS,
    max_attempts: int = 3,
    monitor_interval_seconds: int = 15,
) -> dict[str, Any]:
    dispatch = load_json(dispatch_plan_path.resolve())
    if dispatch.get("schema_version") != DISPATCH_PLAN_SCHEMA:
        raise ParallelRunError("dispatch plan has an unsupported schema_version")
    content = dict(dispatch)
    stored_hash = content.pop("plan_content_sha256", None)
    if stored_hash != identity_sha256(content):
        raise ParallelRunError("dispatch plan content SHA-256 does not match")
    pool = load_pool(registry.resolve(), dispatch["pool_key"])
    if dispatch.get("pool_content_sha256") != pool["pool_content_sha256"]:
        raise ParallelRunError("run pool changed after the dispatch plan was created")
    missing_slots = dispatch.get("missing_slots")
    if not isinstance(missing_slots, list) or not missing_slots:
        raise ParallelRunError("dispatch plan has no missing slots")
    if not isinstance(resource_class, dict) or not resource_class:
        raise ParallelRunError("resource_class must be a non-empty object")
    cycle = cycle.resolve()
    evaluator = evaluator.resolve()
    output = output.resolve()
    if not (cycle / "layer1" / "set.json").is_file():
        raise ParallelRunError(f"cycle is not frozen: {cycle}")
    if not evaluator.is_file():
        raise ParallelRunError(f"evaluation loop does not exist: {evaluator}")
    if output.exists():
        raise ParallelRunError(f"refusing to overwrite output: {output}")
    hints = load_duration_hints(duration_hints_path.resolve())
    template_map = dict(collect_templates(templates))
    if sorted(template_map) != pool["case_ids"]:
        raise ParallelRunError("capsule templates do not match the run pool cases")
    missing_sample_count = dispatch["missing_sample_count"]
    manifest = load_json(cycle / "layer1" / "set.json")
    manifest_cases = {case["id"]: case for case in manifest.get("cases", [])}
    for case_id, template in template_map.items():
        conditions = template.get("comparison_conditions")
        if not isinstance(conditions, dict):
            raise ParallelRunError(f"template comparison conditions are invalid: {case_id}")
        executor = conditions.get("executor_parameters")
        if not isinstance(executor, dict) or executor.get("max_workers") != max_workers:
            raise ParallelRunError(f"template max_workers does not match the queue: {case_id}")
        if case_id not in hints:
            raise ParallelRunError(f"duration hint missing for case: {case_id}")
        binding = template.get("binding")
        if not isinstance(binding, dict) or binding.get("prompt_set_identity") != pool["prompt_set_identity"]:
            raise ParallelRunError(f"template prompt identity does not match the pool: {case_id}")
        case = manifest_cases.get(case_id)
        if not isinstance(case, dict) or "fixture_identity" not in case:
            raise ParallelRunError(f"frozen set has no fixture identity for case: {case_id}")
        compatibility = {
            "evaluation_set": {
                "set_id": manifest["set_id"],
                "revision": manifest["revision"],
                "identity_sha256": manifest["identity_sha256"],
            },
            "fixtures": {case_id: case["fixture_identity"]},
            **conditions,
            "coverage": {"case_ids": [case_id], "iterations": [1]},
        }
        effective, _ = split_conditions(compatibility)
        fixtures = effective.pop("fixtures")
        run_effective = {**effective, "case_id": case_id, "fixture": fixtures[case_id]}
        if identity_sha256(run_effective) != pool["comparison_block_keys"][case_id]:
            raise ParallelRunError(f"template effective conditions do not match the pool: {case_id}")

    output.mkdir(parents=True)
    capsule_dir = output / "capsules"
    capsule_dir.mkdir()
    jobs = []
    ordered_slots = sorted(
        missing_slots,
        key=lambda slot: (
            -hints[slot["case_id"]],
            slot["dispatch_iteration"],
            slot["case_id"],
        ),
    )
    for sequence, slot in enumerate(ordered_slots, start=1):
        case_id = slot["case_id"]
        capsule = copy.deepcopy(template_map[case_id])
        capsule["schema_version"] = "the-caption-prompt.execution-capsule/v3"
        capsule["comparison_conditions"].pop("repetition_condition", None)
        binding = capsule.get("binding")
        if not isinstance(binding, dict):
            raise ParallelRunError(f"capsule template has no binding: {case_id}")
        binding["iteration"] = slot["dispatch_iteration"]
        binding["sample_id"] = slot["sample_id"]
        filename = f"{case_id}-i{slot['dispatch_iteration']}.json"
        destination = capsule_dir / filename
        write_json_once(destination, capsule)
        jobs.append(
            {
                "sequence": sequence,
                "estimated_seconds": hints[case_id],
                "capsule": str(destination),
            }
        )
    plan = {
        "schema_version": "the-caption-prompt.parallel-execution-plan/v3",
        "schedule_policy": "global_queue",
        "ordering": "pair-block-longest-first",
        "resource_class": resource_class,
        "dispatch_plan": str(dispatch_plan_path.resolve()),
        "dispatch_plan_sha256": stored_hash,
        "pool_key": pool["pool_key"],
        "cycle": str(cycle),
        "evaluation_loop": str(evaluator),
        "max_workers": max_workers,
        "max_attempts": max_attempts,
        "monitor_interval_seconds": monitor_interval_seconds,
        "jobs": jobs,
    }
    plan_path = output / "global-plan.json"
    write_json_once(plan_path, plan)
    return {
        "plan": str(plan_path),
        "pool_key": pool["pool_key"],
        "missing_sample_count": missing_sample_count,
        "slot_count": len(jobs),
        "max_workers": max_workers,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--template", action="append", required=True)
    result.add_argument("--dispatch-plan", required=True)
    result.add_argument("--registry", required=True)
    result.add_argument("--cycle", required=True)
    result.add_argument("--evaluation-loop", required=True)
    result.add_argument("--duration-hints", required=True)
    result.add_argument("--resource-class", required=True)
    result.add_argument("--output", required=True)
    result.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS)
    result.add_argument("--max-attempts", type=int, default=3)
    result.add_argument("--monitor-interval-seconds", type=int, default=15)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        resource_class = json.loads(Path(args.resource_class).read_text(encoding="utf-8"))
        result = prepare_atomic_plan(
            templates=[Path(path) for path in args.template],
            dispatch_plan_path=Path(args.dispatch_plan),
            registry=Path(args.registry),
            cycle=Path(args.cycle),
            evaluator=Path(args.evaluation_loop),
            duration_hints_path=Path(args.duration_hints),
            resource_class=resource_class,
            output=Path(args.output),
            max_workers=args.max_workers,
            max_attempts=args.max_attempts,
            monitor_interval_seconds=args.monitor_interval_seconds,
        )
    except (ParallelRunError, EvaluationError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

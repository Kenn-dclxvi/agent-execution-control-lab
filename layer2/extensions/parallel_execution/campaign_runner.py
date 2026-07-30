#!/usr/bin/env python3
"""Run separate prompt-set plans in one longest-first queue capped at M=24."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import shutil
import sys
import threading
import time
from pathlib import Path
from typing import Any

try:
    from .parallel_runner import (
        OsMonitor,
        ParallelRunError,
        execute_job,
        load_object,
        require_positive_integer,
        run_plan,
        utc_now,
        validate_plan,
        write_json_once,
    )
    from .prepare_global_plan import DEFAULT_MAX_WORKERS
except ImportError:  # Direct script execution.
    from parallel_runner import (
        OsMonitor,
        ParallelRunError,
        execute_job,
        load_object,
        require_positive_integer,
        utc_now,
        validate_plan,
        write_json_once,
    )
    from prepare_global_plan import DEFAULT_MAX_WORKERS


def conditions_for_plan(plan: dict[str, Any]) -> dict[str, Any]:
    capsule = load_object(plan["jobs"][0]["capsule"])
    conditions = capsule.get("comparison_conditions")
    if not isinstance(conditions, dict):
        raise ParallelRunError("capsule comparison_conditions must be an object")
    return conditions


def canonical_sha256(value: object) -> str:
    document = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(document).hexdigest()


def prepare_campaign(
    plan_paths: list[Path],
    runner_outputs: list[Path],
    campaign_output: Path,
    max_workers: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if len(plan_paths) < 2:
        raise ParallelRunError("campaign requires at least two prompt-set plans")
    if len(plan_paths) != len(runner_outputs):
        raise ParallelRunError("plan and runner output counts must match")
    max_workers = require_positive_integer(max_workers, "max_workers")
    if max_workers > DEFAULT_MAX_WORKERS:
        raise ParallelRunError(f"max_workers exceeds qualified limit: {DEFAULT_MAX_WORKERS}")
    resolved_outputs = [path.resolve() for path in runner_outputs]
    if len(set(resolved_outputs)) != len(resolved_outputs):
        raise ParallelRunError("runner outputs must be unique")
    campaign_output = campaign_output.resolve()
    if campaign_output in resolved_outputs:
        raise ParallelRunError("campaign output must differ from runner outputs")
    if campaign_output.exists():
        raise ParallelRunError(f"refusing to overwrite output: {campaign_output}")
    for output in resolved_outputs:
        if output.exists():
            raise ParallelRunError(f"refusing to overwrite output: {output}")

    plans: list[dict[str, Any]] = []
    compatibility_mode: str | None = None
    conditions_sha256: str | None = None
    resource_class_sha256: str | None = None
    for index, plan_path in enumerate(plan_paths):
        plan = validate_plan(plan_path.resolve())
        if plan["schedule_policy"] != "global_queue":
            raise ParallelRunError("campaign accepts global_queue plans only")
        if plan["max_workers"] != max_workers:
            raise ParallelRunError("every plan max_workers must equal campaign max_workers")
        conditions = conditions_for_plan(plan)
        executor = conditions.get("executor_parameters")
        if not isinstance(executor, dict) or executor.get("max_workers") != max_workers:
            raise ParallelRunError(
                "comparison_conditions.executor_parameters.max_workers must equal campaign max_workers"
            )
        current_sha256 = canonical_sha256(conditions)
        resource_class = plan.get("resource_class")
        current_mode = "resource_class" if resource_class is not None else "legacy_conditions"
        if compatibility_mode is None:
            compatibility_mode = current_mode
        elif compatibility_mode != current_mode:
            raise ParallelRunError(
                "campaign cannot mix resource-class plans with legacy condition-bound plans"
            )
        if current_mode == "legacy_conditions":
            if conditions_sha256 is None:
                conditions_sha256 = current_sha256
            elif current_sha256 != conditions_sha256:
                raise ParallelRunError("campaign plans must have identical comparison conditions")
        else:
            current_resource_sha256 = canonical_sha256(resource_class)
            if resource_class_sha256 is None:
                resource_class_sha256 = current_resource_sha256
            elif current_resource_sha256 != resource_class_sha256:
                raise ParallelRunError("campaign plans must have identical resource_class values")
        plans.append(
            {
                **plan,
                "plan_path": plan_path.resolve(),
                "runner_output": resolved_outputs[index],
                "plan_index": index,
            }
        )

    pending: list[dict[str, Any]] = []
    for plan in plans:
        for job in plan["jobs"]:
            pending.append(
                {
                    "plan": plan,
                    "job": dict(job),
                    "plan_sequence": job["sequence"],
                }
            )
    groups: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for item in pending:
        binding = item["job"]["binding"]
        groups.setdefault((binding["case_id"], binding["iteration"]), []).append(item)
    ordered_groups = sorted(
        groups.items(),
        key=lambda pair: (
            -max(item["job"]["estimated_seconds"] for item in pair[1]),
            pair[0][0],
            pair[0][1],
        ),
    )
    pending = [
        item
        for _, group in ordered_groups
        for item in sorted(group, key=lambda value: value["plan"]["plan_index"])
    ]
    for sequence, item in enumerate(pending, start=1):
        item["job"]["sequence"] = sequence
    return plans, pending


def run_campaign(
    plan_paths: list[Path],
    runner_outputs: list[Path],
    campaign_output: Path,
    max_workers: int = DEFAULT_MAX_WORKERS,
) -> dict[str, Any]:
    plans, pending = prepare_campaign(
        plan_paths, runner_outputs, campaign_output, max_workers
    )
    campaign_output = campaign_output.resolve()
    campaign_output.mkdir(parents=True)
    group_document = {
        "schema_version": "the-caption-prompt.parallel-campaign-plan/v1",
        "schedule_policy": "global_queue",
        "ordering": "pair-block-longest-first",
        "max_workers": max_workers,
        "compatibility_mode": (
            "resource_class" if plans[0].get("resource_class") is not None else "legacy_conditions"
        ),
        "plans": [
            {
                "plan": str(plan["plan_path"]),
                "plan_sha256": hashlib.sha256(plan["plan_path"].read_bytes()).hexdigest(),
                "runner_output": str(plan["runner_output"]),
                "requested_slots": len(plan["jobs"]),
            }
            for plan in plans
        ],
    }
    if plans[0].get("resource_class") is not None:
        group_document["resource_class"] = plans[0]["resource_class"]
    write_json_once(campaign_output / "plan-group.json", group_document)
    monitor_path = campaign_output / "os-samples.jsonl"
    monitor_path.touch(exist_ok=False)

    for plan in plans:
        output = plan["runner_output"]
        output.mkdir(parents=True)
        write_json_once(output / "plan.json", load_object(plan["plan_path"]))
        (output / "attempts.jsonl").touch(exist_ok=False)
        plan["log_lock"] = threading.Lock()
        plan["results"] = []
        plan["errors"] = []

    monitor = OsMonitor(
        monitor_path,
        plans[0]["cycle"],
        min(plan["monitor_interval_seconds"] for plan in plans),
    )
    started_at = utc_now()
    started = time.perf_counter()
    monitor.start()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            future_items = {}
            for item in pending:
                plan = item["plan"]
                future = pool.submit(
                    execute_job,
                    item["job"],
                    plan["cycle"],
                    plan["evaluation_loop"],
                    plan["max_attempts"],
                    plan["runner_output"] / "attempts.jsonl",
                    plan["log_lock"],
                )
                future_items[future] = plan
            for future in concurrent.futures.as_completed(future_items):
                plan = future_items[future]
                try:
                    plan["results"].append(future.result())
                except ParallelRunError as exc:
                    plan["errors"].append(str(exc))
    finally:
        monitor.stop()
    elapsed = time.perf_counter() - started

    plan_summaries = []
    for plan in plans:
        output = plan["runner_output"]
        shutil.copyfile(monitor_path, output / "os-samples.jsonl")
        attempts = [
            json.loads(line)
            for line in (output / "attempts.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        excluded = [
            item for item in attempts if item.get("result", {}).get("status") == "excluded"
        ]
        complete = not plan["errors"] and len(plan["results"]) == len(plan["jobs"])
        summary = {
            "schema_version": "the-caption-prompt.parallel-execution-summary/v1",
            "started_at": started_at,
            "ended_at": utc_now(),
            "elapsed_seconds": elapsed,
            "max_workers": max_workers,
            "schedule_policy": "global_queue",
            "requested_slots": len(plan["jobs"]),
            "valid_slots": len(plan["results"]),
            "attempt_count": len(attempts),
            "excluded_attempt_count": len(excluded),
            "status": "complete" if complete else "failed",
            "errors": plan["errors"],
            "campaign_output": str(campaign_output),
        }
        write_json_once(output / "summary.json", summary)
        plan_summaries.append(summary)

    errors = [error for plan in plans for error in plan["errors"]]
    summary = {
        "schema_version": "the-caption-prompt.parallel-campaign-summary/v1",
        "started_at": started_at,
        "ended_at": utc_now(),
        "elapsed_seconds": elapsed,
        "max_workers": max_workers,
        "schedule_policy": "global_queue",
        "requested_slots": len(pending),
        "valid_slots": sum(len(plan["results"]) for plan in plans),
        "plan_count": len(plans),
        "status": "complete" if not errors else "failed",
        "errors": errors,
        "plan_summaries": plan_summaries,
    }
    write_json_once(campaign_output / "summary.json", summary)
    if summary["status"] != "complete":
        raise ParallelRunError("parallel campaign did not complete every requested slot")
    return summary


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--plan", action="append", required=True)
    result.add_argument("--runner-output", action="append", required=True)
    result.add_argument("--campaign-output", required=True)
    result.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        summary = run_campaign(
            [Path(path) for path in args.plan],
            [Path(path) for path in args.runner_output],
            Path(args.campaign_output),
            args.max_workers,
        )
    except (ParallelRunError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

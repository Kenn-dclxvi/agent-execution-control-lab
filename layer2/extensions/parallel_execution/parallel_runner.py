#!/usr/bin/env python3
"""Run independent Layer 2 capsules with bounded outer parallelism."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


class ParallelRunError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ParallelRunError(f"invalid JSON object: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ParallelRunError(f"JSON root must be an object: {path}")
    return value


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ParallelRunError(f"{name} must be a non-empty string")
    return value


def require_positive_integer(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ParallelRunError(f"{name} must be a positive integer")
    return value


def require_positive_number(value: Any, name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
        raise ParallelRunError(f"{name} must be a positive number")
    return float(value)


def write_json_once(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ParallelRunError(f"refusing to overwrite: {path}") from exc


def append_jsonl(path: Path, value: dict[str, Any], lock: threading.Lock) -> None:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    with lock:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized + "\n")
            handle.flush()
            os.fsync(handle.fileno())


def command_text(command: list[str]) -> str:
    completed = subprocess.run(command, capture_output=True, check=False, text=True)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"exit {completed.returncode}"
        raise OSError(detail)
    return completed.stdout


def os_sample(disk_path: Path) -> dict[str, Any]:
    sample: dict[str, Any] = {"sampled_at": utc_now()}
    errors: list[str] = []
    try:
        load1, load5, load15 = os.getloadavg()
        sample["load_average"] = {"one": load1, "five": load5, "fifteen": load15}
    except OSError as exc:
        errors.append(f"load_average: {exc}")
    try:
        usage = shutil.disk_usage(disk_path)
        sample["disk"] = {
            "path": str(disk_path),
            "free_bytes": usage.free,
            "total_bytes": usage.total,
            "used_bytes": usage.used,
        }
    except OSError as exc:
        errors.append(f"disk: {exc}")
    try:
        pressure = command_text(["memory_pressure", "-Q"])
        match = re.search(r"System-wide memory free percentage:\s*(\d+)%", pressure)
        if match is None:
            raise OSError("free percentage was not reported")
        sample["memory_free_percent"] = int(match.group(1))
    except OSError as exc:
        errors.append(f"memory_pressure: {exc}")
    try:
        swap = command_text(["sysctl", "-n", "vm.swapusage"])
        match = re.search(r"used\s*=\s*([0-9.]+)([KMG])", swap)
        if match is None:
            raise OSError("swap usage was not reported")
        scale = {"K": 1 / 1024, "M": 1, "G": 1024}[match.group(2)]
        sample["swap_used_mib"] = float(match.group(1)) * scale
    except OSError as exc:
        errors.append(f"swap: {exc}")
    try:
        commands = command_text(["ps", "-axo", "command="]).splitlines()
        sample["processes"] = {
            "codex": sum(1 for command in commands if re.search(r"(^|/)codex(?:\s|$)", command)),
            "evaluation_loop": sum(1 for command in commands if "evaluation_loop.py run" in command),
        }
    except OSError as exc:
        errors.append(f"processes: {exc}")
    if errors:
        sample["sample_errors"] = errors
    return sample


class OsMonitor:
    def __init__(
        self,
        path: Path,
        disk_path: Path,
        interval_seconds: float,
        sampler: Callable[[Path], dict[str, Any]] = os_sample,
    ) -> None:
        self.path = path
        self.disk_path = disk_path
        self.interval_seconds = interval_seconds
        self.sampler = sampler
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._run, name="evaluation-os-monitor", daemon=True)

    def _record(self) -> None:
        try:
            sample = self.sampler(self.disk_path)
        except Exception as exc:  # Monitor failure must not alter execution output.
            sample = {"sampled_at": utc_now(), "sample_errors": [f"sampler: {exc}"]}
        append_jsonl(self.path, sample, self.lock)

    def _run(self) -> None:
        self._record()
        while not self.stop_event.wait(self.interval_seconds):
            self._record()

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        self.thread.join()
        self._record()


def binding_from_capsule(path: Path) -> dict[str, Any]:
    capsule = load_object(path)
    if capsule.get("schema_version") not in {
        "the-caption-prompt.execution-capsule/v2",
        "the-caption-prompt.execution-capsule/v3",
    }:
        raise ParallelRunError(f"unsupported capsule schema_version: {path}")
    binding = capsule.get("binding")
    if not isinstance(binding, dict):
        raise ParallelRunError(f"capsule binding must be an object: {path}")
    case_id = require_string(binding.get("case_id"), f"{path}.binding.case_id")
    iteration = require_positive_integer(binding.get("iteration"), f"{path}.binding.iteration")
    prompt_set_identity = binding.get("prompt_set_identity")
    if not isinstance(prompt_set_identity, dict):
        raise ParallelRunError(f"capsule prompt_set_identity must be an object: {path}")
    require_string(prompt_set_identity.get("name"), f"{path}.binding.prompt_set_identity.name")
    if not any(prompt_set_identity.get(key) for key in ("revision", "bundle_sha256")):
        raise ParallelRunError(f"capsule prompt_set_identity needs revision or bundle_sha256: {path}")
    comparison_conditions = capsule.get("comparison_conditions")
    if not isinstance(comparison_conditions, dict):
        raise ParallelRunError(f"capsule comparison_conditions must be an object: {path}")
    identity_document = json.dumps(
        prompt_set_identity, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    conditions_document = json.dumps(
        comparison_conditions, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return {
        "case_id": case_id,
        "iteration": iteration,
        "prompt_set_identity": prompt_set_identity,
        "prompt_set_identity_sha256": hashlib.sha256(identity_document).hexdigest(),
        "comparison_conditions_sha256": hashlib.sha256(conditions_document).hexdigest(),
    }


def validate_plan(path: Path) -> dict[str, Any]:
    plan = load_object(path)
    schema_version = plan.get("schema_version")
    if schema_version != "the-caption-prompt.parallel-execution-plan/v3":
        raise ParallelRunError("unsupported plan schema_version")
    schedule_policy = plan.get("schedule_policy", "wave_barrier")
    if schedule_policy not in {"wave_barrier", "global_queue"}:
        raise ParallelRunError("unsupported schedule_policy")
    cycle = Path(require_string(plan.get("cycle"), "cycle")).resolve()
    evaluator = Path(require_string(plan.get("evaluation_loop"), "evaluation_loop")).resolve()
    if not (cycle / "layer1" / "set.json").is_file():
        raise ParallelRunError(f"cycle is not frozen: {cycle}")
    if not evaluator.is_file():
        raise ParallelRunError(f"evaluation loop does not exist: {evaluator}")
    max_workers = require_positive_integer(plan.get("max_workers"), "max_workers")
    max_attempts = require_positive_integer(plan.get("max_attempts", 3), "max_attempts")
    monitor_interval = require_positive_number(
        plan.get("monitor_interval_seconds", 15), "monitor_interval_seconds"
    )
    resource_class = plan.get("resource_class")
    if resource_class is not None and (
        not isinstance(resource_class, dict) or not resource_class
    ):
        raise ParallelRunError("resource_class must be a non-empty object")
    raw_jobs = plan.get("jobs")
    if not isinstance(raw_jobs, list) or not raw_jobs:
        raise ParallelRunError("jobs must be a non-empty array")
    jobs: list[dict[str, Any]] = []
    keys: set[tuple[str, int]] = set()
    cycle_signature: tuple[str, str] | None = None
    wave_counts: dict[int, int] = {}
    sequences: list[int] = []
    for index, raw_job in enumerate(raw_jobs):
        if not isinstance(raw_job, dict):
            raise ParallelRunError(f"jobs[{index}] must be an object")
        capsule = Path(require_string(raw_job.get("capsule"), f"jobs[{index}].capsule")).resolve()
        if not capsule.is_file():
            raise ParallelRunError(f"capsule does not exist: {capsule}")
        binding = binding_from_capsule(capsule)
        signature = (
            binding["prompt_set_identity_sha256"],
            binding["comparison_conditions_sha256"],
        )
        if cycle_signature is None:
            cycle_signature = signature
        elif signature != cycle_signature:
            raise ParallelRunError("all jobs must use one prompt identity and comparison conditions")
        key = (binding["case_id"], binding["iteration"])
        if key in keys:
            raise ParallelRunError(f"duplicate execution slot: {key}")
        keys.add(key)
        job = {"capsule": capsule, "binding": binding, "index": index}
        if schedule_policy == "wave_barrier":
            wave = require_positive_integer(raw_job.get("wave"), f"jobs[{index}].wave")
            wave_counts[wave] = wave_counts.get(wave, 0) + 1
            job["wave"] = wave
        else:
            sequence = require_positive_integer(
                raw_job.get("sequence"), f"jobs[{index}].sequence"
            )
            estimated_seconds = require_positive_number(
                raw_job.get("estimated_seconds"), f"jobs[{index}].estimated_seconds"
            )
            sequences.append(sequence)
            job["sequence"] = sequence
            job["estimated_seconds"] = estimated_seconds
        jobs.append(job)
    if schedule_policy == "wave_barrier":
        waves = sorted(wave_counts)
        if waves != list(range(1, max(waves) + 1)):
            raise ParallelRunError("job waves must be contiguous and start at 1")
        oversized = [wave for wave, count in wave_counts.items() if count > max_workers]
        if oversized:
            raise ParallelRunError(f"job wave exceeds max_workers: {oversized[0]}")
    else:
        if sequences != list(range(1, len(jobs) + 1)):
            raise ParallelRunError("global job sequences must be ordered, contiguous, and start at 1")
        waves = []
    return {
        "cycle": cycle,
        "evaluation_loop": evaluator,
        "max_workers": max_workers,
        "max_attempts": max_attempts,
        "monitor_interval_seconds": monitor_interval,
        "schedule_policy": schedule_policy,
        "resource_class": resource_class,
        "jobs": jobs,
        "waves": waves,
    }


def parse_result(stdout: str) -> dict[str, Any]:
    lines = [line for line in stdout.splitlines() if line.strip()]
    if not lines:
        raise ParallelRunError("evaluation loop produced no result")
    try:
        result = json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise ParallelRunError(f"evaluation loop result is not JSON: {lines[-1]}") from exc
    if not isinstance(result, dict) or result.get("status") not in {"valid", "excluded"}:
        raise ParallelRunError("evaluation loop result has no valid status")
    return result


def execute_job(
    job: dict[str, Any],
    cycle: Path,
    evaluator: Path,
    max_attempts: int,
    attempt_path: Path,
    log_lock: threading.Lock,
) -> dict[str, Any]:
    binding = job["binding"]
    capsule = job["capsule"]
    for attempt in range(1, max_attempts + 1):
        started_at = utc_now()
        started = time.perf_counter()
        completed = subprocess.run(
            [
                sys.executable,
                str(evaluator),
                "run",
                "--cycle",
                str(cycle),
                "--capsule",
                str(capsule),
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        elapsed = time.perf_counter() - started
        record: dict[str, Any] = {
            **binding,
            "attempt": attempt,
            "capsule": str(capsule),
            "started_at": started_at,
            "ended_at": utc_now(),
            "runner_elapsed_seconds": elapsed,
            "controller_exit_code": completed.returncode,
        }
        if "sequence" in job:
            record["dispatch_sequence"] = job["sequence"]
            record["estimated_seconds"] = job["estimated_seconds"]
        if completed.returncode != 0:
            record["controller_stderr"] = completed.stderr
            append_jsonl(attempt_path, record, log_lock)
            raise ParallelRunError(
                f"Layer 2 controller failed for {binding['case_id']} "
                f"iteration {binding['iteration']}: {completed.stderr.strip()}"
            )
        result = parse_result(completed.stdout)
        record["result"] = result
        append_jsonl(attempt_path, record, log_lock)
        if result["status"] == "valid":
            return record
    raise ParallelRunError(
        f"external failure retry limit reached for {binding['case_id']} "
        f"iteration {binding['iteration']}"
    )


def run_plan(plan_path: Path, output: Path) -> dict[str, Any]:
    plan = validate_plan(plan_path.resolve())
    output = output.resolve()
    if output.exists():
        raise ParallelRunError(f"refusing to overwrite output: {output}")
    output.mkdir(parents=True)
    plan_copy = load_object(plan_path.resolve())
    write_json_once(output / "plan.json", plan_copy)
    attempt_path = output / "attempts.jsonl"
    attempt_path.touch(exist_ok=False)
    monitor_path = output / "os-samples.jsonl"
    monitor_path.touch(exist_ok=False)
    log_lock = threading.Lock()
    monitor = OsMonitor(
        monitor_path,
        plan["cycle"],
        plan["monitor_interval_seconds"],
    )
    started_at = utc_now()
    started = time.perf_counter()
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    monitor.start()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=plan["max_workers"]) as pool:
            if plan["schedule_policy"] == "global_queue":
                job_groups = [plan["jobs"]]
            else:
                job_groups = [
                    [job for job in plan["jobs"] if job["wave"] == wave]
                    for wave in plan["waves"]
                ]
            for jobs in job_groups:
                futures = [
                    pool.submit(
                        execute_job,
                        job,
                        plan["cycle"],
                        plan["evaluation_loop"],
                        plan["max_attempts"],
                        attempt_path,
                        log_lock,
                    )
                    for job in jobs
                ]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        results.append(future.result())
                    except ParallelRunError as exc:
                        errors.append(str(exc))
                if errors:
                    break
    finally:
        monitor.stop()
    elapsed = time.perf_counter() - started
    attempts = [
        json.loads(line)
        for line in attempt_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    excluded = [item for item in attempts if item.get("result", {}).get("status") == "excluded"]
    summary = {
        "schema_version": "the-caption-prompt.parallel-execution-summary/v1",
        "started_at": started_at,
        "ended_at": utc_now(),
        "elapsed_seconds": elapsed,
        "max_workers": plan["max_workers"],
        "schedule_policy": plan["schedule_policy"],
        "requested_slots": len(plan["jobs"]),
        "valid_slots": len(results),
        "attempt_count": len(attempts),
        "excluded_attempt_count": len(excluded),
        "status": "complete" if not errors and len(results) == len(plan["jobs"]) else "failed",
        "errors": errors,
    }
    write_json_once(output / "summary.json", summary)
    if summary["status"] != "complete":
        raise ParallelRunError("parallel execution did not complete every requested slot")
    return summary


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--plan", required=True)
    result.add_argument("--output", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        summary = run_plan(Path(args.plan), Path(args.output))
    except (ParallelRunError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

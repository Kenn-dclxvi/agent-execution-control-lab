#!/usr/bin/env python3
"""Recover the Candidate170 diagnostic packet without changing its prompt."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

import pr_review_measurement_c02_evidence_diagnostic as base


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-measurement-c02-evidence-diagnostic-n1-r3"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-measure-c02-evidence-diagnostic-r3.yml"
WORKFLOW_REVISION = "pr-review-measure-c02-evidence-diagnostic-r3"
COMPARISON_REVISION = "pr-review-measurement-c02-evidence-diagnostic-r3"
SCHEMA_VERSION = 21


def _patch_base() -> dict:
    original = {
        "PROFILE_ID": base.PROFILE_ID,
        "PROFILE_PATH": base.PROFILE_PATH,
        "PREFLIGHT_PATH": base.PREFLIGHT_PATH,
        "WORKFLOW_PATH": base.WORKFLOW_PATH,
        "WORKFLOW_REVISION": base.WORKFLOW_REVISION,
        "COMPARISON_REVISION": base.COMPARISON_REVISION,
        "file": base.__file__,
    }
    base.PROFILE_ID = PROFILE_ID
    base.PROFILE_PATH = PROFILE_PATH
    base.PREFLIGHT_PATH = PREFLIGHT_PATH
    base.WORKFLOW_PATH = WORKFLOW_PATH
    base.WORKFLOW_REVISION = WORKFLOW_REVISION
    base.COMPARISON_REVISION = COMPARISON_REVISION
    base.__file__ = __file__
    return original


def _restore_base(original: dict) -> None:
    for key in (
        "PROFILE_ID",
        "PROFILE_PATH",
        "PREFLIGHT_PATH",
        "WORKFLOW_PATH",
        "WORKFLOW_REVISION",
        "COMPARISON_REVISION",
    ):
        setattr(base, key, original[key])
    base.__file__ = original["file"]


def _call(function, *args):
    original = _patch_base()
    try:
        return function(*args)
    finally:
        _restore_base(original)


def validate_preflight(case_id: str) -> tuple[dict, dict]:
    return _call(base.validate_preflight, case_id)


def prepare_input(case_id: str, output_dir: Path) -> dict:
    metadata = _call(base.prepare_input, case_id, output_dir)
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_measurement_c02_evidence_scope.py",
        output_dir / "pr_review_measurement_c02_evidence_scope.py",
    )
    shutil.copyfile(__file__, output_dir / Path(__file__).name)
    metadata.update(
        profile_id=PROFILE_ID,
        diagnostic_revision="content-free-evidence-and-token-r3-environment-recovery",
    )
    (output_dir / "prepare-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def collect_review(*args) -> dict:
    return _call(base.collect_review, *args)


def grade_run(*args) -> dict:
    output = args[-2]
    with tempfile.TemporaryDirectory() as directory:
        intermediate = Path(directory) / "run-result.json"
        forwarded = (*args[:-2], intermediate, args[-1])
        run = _call(base.grade_run, *forwarded)
    run.update(
        schema_version=SCHEMA_VERSION,
        comparison_revision=COMPARISON_REVISION,
        profile_id=PROFILE_ID,
        workflow_revision=WORKFLOW_REVISION,
    )
    base.base.held_out.free.core.legacy._write_json_once(output, run)
    return run


def record_terminal(*args) -> dict:
    output = args[-2]
    with tempfile.TemporaryDirectory() as directory:
        intermediate = Path(directory) / "run-result.json"
        forwarded = (*args[:-2], intermediate, args[-1])
        run = _call(base.record_terminal, *forwarded)
    run.update(
        schema_version=SCHEMA_VERSION,
        comparison_revision=COMPARISON_REVISION,
        profile_id=PROFILE_ID,
        workflow_revision=WORKFLOW_REVISION,
    )
    base.base.held_out.free.core.legacy._write_json_once(output, run)
    return run


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-preflight", "prepare"):
        item = sub.add_parser(name)
        item.add_argument("--case-id", required=True, choices=base.base.CASES)
        if name == "prepare":
            item.add_argument("--output-dir", required=True, type=Path)
    collect = sub.add_parser("collect")
    for name in ("raw-output", "execution-file", "hook-file", "review-input", "output-dir"):
        collect.add_argument(
            f"--{name}", type=Path, required=name not in {"execution-file", "hook-file"}
        )
    for name in ("action-conclusion", "model-requested"):
        collect.add_argument(f"--{name}", required=True)
    for name in ("started-ms", "finished-ms"):
        collect.add_argument(f"--{name}", required=True, type=int)
    for command in ("grade", "record-terminal"):
        item = sub.add_parser(command)
        item.add_argument("--case-id", required=True, choices=base.base.CASES)
        item.add_argument("--attempt", required=True, type=int)
        item.add_argument("--model-requested", required=True)
        item.add_argument("--github-run-id", required=True)
        item.add_argument("--output", required=True, type=Path)
        if command == "grade":
            for name in ("review-output", "review-metadata", "prepare-metadata"):
                item.add_argument(f"--{name}", required=True, type=Path)
        else:
            item.add_argument("--status", required=True)
    args = parser.parse_args()
    if args.command == "validate-preflight":
        validate_preflight(args.case_id)
        print("Candidate170 diagnostic environment recovery preflight is valid")
    elif args.command == "prepare":
        print(json.dumps(prepare_input(args.case_id, args.output_dir), ensure_ascii=False))
    elif args.command == "collect":
        print(json.dumps(collect_review(
            args.raw_output, args.action_conclusion, args.execution_file, args.hook_file,
            args.started_ms, args.finished_ms, args.model_requested, args.review_input,
            args.output_dir,
        ), ensure_ascii=False))
    elif args.command == "grade":
        print(json.dumps(grade_run(
            args.case_id, args.attempt, args.model_requested, args.review_output,
            args.review_metadata, args.prepare_metadata, args.output, args.github_run_id,
        ), ensure_ascii=False))
    else:
        print(json.dumps(record_terminal(
            args.case_id, args.attempt, args.model_requested, args.status,
            args.output, args.github_run_id,
        ), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

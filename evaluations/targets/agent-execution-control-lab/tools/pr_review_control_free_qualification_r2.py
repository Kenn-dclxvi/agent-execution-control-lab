#!/usr/bin/env python3
"""Environment recovery for the four-case control-free qualification."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pr_review_control_free_qualification as base


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-control-free-four-qualification-n1-r2"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-qualify-control-free-four-r2.yml"
WORKFLOW_REVISION = "pr-review-qualify-control-free-four-r2"

base.PROFILE_ID = PROFILE_ID
base.PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
base.PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
base.WORKFLOW_PATH = WORKFLOW_PATH
base.WORKFLOW_REVISION = WORKFLOW_REVISION

_prepare_input = base.prepare_input
_grade_run = base.grade_run
_record_terminal = base.record_terminal


def prepare_input(case_id: str, output_dir: Path) -> dict:
    metadata = _prepare_input(case_id, output_dir)
    dependencies = (
        "pr_review_measurement.py",
        "pr_review_qualification.py",
        "pr_review_code_review_qualification.py",
        "pr_review_workflow_free_calibration.py",
        "pr_review_control_free_qualification.py",
    )
    for filename in dependencies:
        shutil.copyfile(INSTANCE_ROOT / "tools" / filename, output_dir / filename)
    shutil.copyfile(Path(__file__), output_dir / Path(__file__).name)
    return metadata


def _upgrade(run: dict, output: Path) -> dict:
    run["schema_version"] = 14
    base.measurement._write_json_once(output, run)
    return run


def grade_run(
    case_id: str,
    attempt: int,
    model_requested: str,
    review_output: Path,
    review_metadata: Path,
    prepare_metadata: Path,
    output: Path,
    github_run_id: str,
) -> dict:
    with tempfile.TemporaryDirectory() as directory:
        run = _grade_run(
            case_id,
            attempt,
            model_requested,
            review_output,
            review_metadata,
            prepare_metadata,
            Path(directory) / "run-result.json",
            github_run_id,
        )
    return _upgrade(run, output)


def record_terminal(
    case_id: str,
    attempt: int,
    model_requested: str,
    status: str,
    output: Path,
    github_run_id: str,
) -> dict:
    with tempfile.TemporaryDirectory() as directory:
        run = _record_terminal(
            case_id,
            attempt,
            model_requested,
            status,
            Path(directory) / "run-result.json",
            github_run_id,
        )
    return _upgrade(run, output)


base.prepare_input = prepare_input
base.grade_run = grade_run
base.record_terminal = record_terminal


if __name__ == "__main__":
    raise SystemExit(base.main())

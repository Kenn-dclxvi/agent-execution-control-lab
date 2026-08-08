#!/usr/bin/env python3
"""Three-case qualification with nested fixture-tool call measurement."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import pr_review_control_free_qualification_r2 as recovery


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-control-free-three-qualification-n1-r3"
WORKFLOW_REVISION = "pr-review-qualify-control-free-three-r3"
COMPARISON_REVISION = "pr-review-control-free-three-qualification-r2"
RATING_ID = "pr-review-finding-quality-v7"
CASES = ("PRR-C02", "PRR-C03", "PRR-C06")

recovery.base.PROFILE_ID = PROFILE_ID
recovery.base.PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
recovery.base.PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
recovery.base.WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-qualify-control-free-three-r3.yml"
recovery.base.WORKFLOW_REVISION = WORKFLOW_REVISION
recovery.base.COMPARISON_REVISION = COMPARISON_REVISION
recovery.base.RATING_ID = RATING_ID
recovery.base.CASES = CASES

_prepare_input = recovery.prepare_input
_grade_run = recovery.grade_run
_record_terminal = recovery.record_terminal


def prepare_input(case_id: str, output_dir: Path) -> dict:
    metadata = _prepare_input(case_id, output_dir)
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_subagent_hook_r2.py",
        output_dir / "pr_review_subagent_hook_r2.py",
    )
    settings_path = output_dir / "claude-project-settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    for event_hooks in settings["hooks"].values():
        for matcher in event_hooks:
            for hook in matcher["hooks"]:
                args = hook.get("args", [])
                hook["args"] = [
                    value.replace("pr_review_subagent_hook.py", "pr_review_subagent_hook_r2.py")
                    if isinstance(value, str)
                    else value
                    for value in args
                ]
    settings_path.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    shutil.copyfile(Path(__file__), output_dir / Path(__file__).name)
    return metadata


def _upgrade(run: dict, output: Path) -> dict:
    run["schema_version"] = 15
    recovery.base.measurement._write_json_once(output, run)
    return run


def grade_run(*args) -> dict:
    output = args[6]
    with tempfile.TemporaryDirectory() as directory:
        temporary_args = (*args[:6], Path(directory) / "run-result.json", *args[7:])
        run = _grade_run(*temporary_args)
    return _upgrade(run, output)


def record_terminal(*args) -> dict:
    output = args[4]
    with tempfile.TemporaryDirectory() as directory:
        temporary_args = (*args[:4], Path(directory) / "run-result.json", *args[5:])
        run = _record_terminal(*temporary_args)
    return _upgrade(run, output)


recovery.base.prepare_input = prepare_input
recovery.base.grade_run = grade_run
recovery.base.record_terminal = record_terminal


if __name__ == "__main__":
    raise SystemExit(recovery.base.main())

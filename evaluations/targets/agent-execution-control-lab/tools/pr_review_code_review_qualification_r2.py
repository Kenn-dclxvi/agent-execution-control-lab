#!/usr/bin/env python3
"""Environment recovery for Claude Code Core PRR-C01/r4 repetition 1."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pr_review_code_review_qualification as base


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
PROFILE_ID = "pr-review-claude-code-core-c01-r4-qualification-n2-r2"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
WORKFLOW_REVISION = "pr-review-qualify-claude-code-core-r2"


def _bind_revision() -> None:
    base.PROFILE_ID = PROFILE_ID
    base.PROFILE_PATH = PROFILE_PATH
    base.PREFLIGHT_PATH = PREFLIGHT_PATH
    base.WORKFLOW_REVISION = WORKFLOW_REVISION
    base.WORKFLOW_PATH = (
        base.REPOSITORY_ROOT
        / ".github/workflows/pr-review-qualify-claude-code-core-r2.yml"
    )


def validate_preflight(repetition: int, prior_admission: Path | None = None):
    _bind_revision()
    return base.validate_preflight(repetition, prior_admission)


def prepare_input(repetition: int, output_dir: Path) -> dict:
    _bind_revision()
    metadata = base.prepare_input(repetition, output_dir)
    shutil.copyfile(Path(__file__), output_dir / Path(__file__).name)
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_qualification.py",
        output_dir / "pr_review_qualification.py",
    )
    return metadata


def collect_review(*args, **kwargs):
    _bind_revision()
    return base.collect_review(*args, **kwargs)


def _upgrade_result(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    value["schema_version"] = 8
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return value


def grade_run(*args, **kwargs):
    _bind_revision()
    output = args[6] if len(args) > 6 else kwargs["output"]
    base.grade_run(*args, **kwargs)
    return _upgrade_result(output)


def record_terminal(*args, **kwargs):
    _bind_revision()
    output = args[4] if len(args) > 4 else kwargs["output"]
    base.record_terminal(*args, **kwargs)
    return _upgrade_result(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-preflight", "prepare"):
        item = sub.add_parser(name)
        item.add_argument("--repetition", required=True, type=int)
        if name == "prepare":
            item.add_argument("--output-dir", required=True, type=Path)
    collect = sub.add_parser("collect")
    for name in ("raw-output", "execution-file", "review-input", "output-dir"):
        collect.add_argument(f"--{name}", type=Path, required=name != "execution-file")
    for name in ("action-conclusion", "model-requested"):
        collect.add_argument(f"--{name}", required=True)
    for name in ("started-ms", "finished-ms"):
        collect.add_argument(f"--{name}", required=True, type=int)
    for command in ("grade", "record-terminal"):
        item = sub.add_parser(command)
        for name in ("repetition", "attempt"):
            item.add_argument(f"--{name}", required=True, type=int)
        for name in ("model-requested", "github-run-id"):
            item.add_argument(f"--{name}", required=True)
        item.add_argument("--output", required=True, type=Path)
        if command == "grade":
            for name in ("review-output", "review-metadata", "prepare-metadata"):
                item.add_argument(f"--{name}", required=True, type=Path)
        else:
            item.add_argument("--status", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate-preflight":
            validate_preflight(args.repetition)
            print("qualification preflight is valid")
        elif args.command == "prepare":
            print(json.dumps(prepare_input(args.repetition, args.output_dir), ensure_ascii=False))
        elif args.command == "collect":
            print(json.dumps(collect_review(args.raw_output, args.action_conclusion, args.execution_file, args.started_ms, args.finished_ms, args.model_requested, args.review_input, args.output_dir), ensure_ascii=False))
        elif args.command == "grade":
            print(json.dumps(grade_run(args.repetition, args.attempt, args.model_requested, args.review_output, args.review_metadata, args.prepare_metadata, args.output, args.github_run_id), ensure_ascii=False))
        else:
            print(json.dumps(record_terminal(args.repetition, args.attempt, args.model_requested, args.status, args.output, args.github_run_id), ensure_ascii=False))
    except (base.QualificationError, base.legacy.QualificationError, base.measurement.ValidationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

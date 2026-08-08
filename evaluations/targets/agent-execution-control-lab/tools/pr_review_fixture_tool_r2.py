#!/usr/bin/env python3
"""Read-only fixture accessor with raw repository authority packet support."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath


def _load_json(environment_key: str, default: str) -> dict:
    path = Path(os.environ.get(environment_key, default))
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _safe_path(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise SystemExit("path must be repository-relative")
    return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("metadata", "changed-paths", "diff", "rules", "files", "file", "contract"),
    )
    parser.add_argument("path", nargs="?")
    args = parser.parse_args()

    if args.command == "contract":
        print(Path("review-contract.md").read_text(encoding="utf-8"), end="")
        return 0
    if args.command == "rules":
        authority = _load_json("PR_REVIEW_AUTHORITY", "authority-input.json")
        print(json.dumps(authority, ensure_ascii=False, indent=2))
        return 0

    data = _load_json("PR_REVIEW_INPUT", "review-input.json")
    if args.command == "metadata":
        print(json.dumps(data["pr"], ensure_ascii=False, indent=2))
    elif args.command == "changed-paths":
        print(json.dumps(data["changed_paths"], ensure_ascii=False, indent=2))
    elif args.command == "diff":
        for change in data["changes"]:
            print(f"diff --git a/{change['path']} b/{change['path']}")
            print(change["patch"])
    elif args.command == "files":
        print(
            json.dumps(
                {change["path"]: change["content_after"] for change in data["changes"]},
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.command == "file":
        if not args.path:
            raise SystemExit("file requires a path")
        requested = _safe_path(args.path)
        for change in data["changes"]:
            if change["path"] == requested:
                print(change["content_after"], end="")
                return 0
        raise SystemExit(f"changed file is not available: {requested}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Read-only fixture accessor for the Claude code-review workflow."""

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
    if not value or path.is_absolute() or ".." in path.parts or path.parts[0] == ".git":
        raise SystemExit("path must be repository-relative and outside .git")
    return path.as_posix()


def _snapshot_root() -> Path:
    return Path(os.environ.get("PR_REVIEW_REPOSITORY", "repository")).resolve()


def _snapshot_path(value: str) -> Path:
    root = _snapshot_root()
    requested = root.joinpath(*PurePosixPath(_safe_path(value)).parts)
    resolved = requested.resolve()
    if root != resolved and root not in resolved.parents:
        raise SystemExit("resolved path leaves repository snapshot")
    return resolved


def _list_snapshot_files() -> list[str]:
    root = _snapshot_root()
    result = []
    for directory, directories, files in os.walk(root, followlinks=False):
        current = Path(directory)
        symlink_directories = []
        for name in directories:
            path = current / name
            if path.is_symlink():
                symlink_directories.append(name)
                result.append(path.relative_to(root).as_posix())
        directories[:] = [name for name in directories if name not in symlink_directories]
        result.extend((current / name).relative_to(root).as_posix() for name in files)
    return sorted(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=(
            "workflow", "eligibility", "metadata", "changed-paths", "diff", "rules",
            "files", "file", "list-files", "contract",
        ),
    )
    parser.add_argument("path", nargs="?")
    args = parser.parse_args()

    if args.command == "workflow":
        print(Path("core-prompt.md").read_text(encoding="utf-8"), end="")
        return 0
    if args.command == "contract":
        print(Path("review-contract.md").read_text(encoding="utf-8"), end="")
        return 0
    if args.command == "eligibility":
        print(
            json.dumps(
                _load_json("PR_REVIEW_ELIGIBILITY", "review-eligibility.json"),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    data = _load_json("PR_REVIEW_INPUT", "review-input.json")
    if args.command == "rules":
        print(
            json.dumps(
                {
                    "rule_catalog": data["rules"],
                    "repository_authority": _load_json(
                        "PR_REVIEW_AUTHORITY", "authority-input.json"
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if args.command == "list-files":
        print(json.dumps(_list_snapshot_files(), ensure_ascii=False, indent=2))
        return 0
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
        path = _snapshot_path(args.path)
        if not path.is_file():
            raise SystemExit(f"snapshot file is not available: {args.path}")
        try:
            print(path.read_text(encoding="utf-8"), end="")
        except UnicodeDecodeError as exc:
            raise SystemExit(f"snapshot file is not UTF-8 text: {args.path}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

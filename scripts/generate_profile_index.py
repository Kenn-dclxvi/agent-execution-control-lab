#!/usr/bin/env python3
"""Generate the legacy-root profile index shards and their README links."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROFILES_DIR = REPO_ROOT / "evaluations" / "profiles"
SHARD_SIZE = 60
SHARD_NAME_RE = re.compile(r"^profiles-\d{3}-\d{3}\.md$")
README_LINK_RE = re.compile(r"^- \[`\d+–\d+`\]\(index/profiles-\d+-\d+\.md\)$", re.MULTILINE)
SHARD_NOTE = (
    "このファイルは`evaluations/profiles/README.md`から辿る機械的なprofile索引である。"
    "profileの用途・結果・状態の正本ではない。"
)


class ProfileIndexError(Exception):
    """Raised when the profile index cannot be planned, verified, or written."""


def profile_names(profiles_dir: Path) -> list[str]:
    names = sorted(path.name for path in profiles_dir.glob("*.json") if path.is_file())
    if not names:
        raise ProfileIndexError(f"no profile JSON found under {profiles_dir}")
    return names


def shard_plan(names: list[str]) -> list[tuple[str, int, int, list[str]]]:
    plan = []
    for start in range(0, len(names), SHARD_SIZE):
        block = names[start : start + SHARD_SIZE]
        low, high = start + 1, start + len(block)
        plan.append((f"profiles-{low:03d}-{high:03d}.md", low, high, block))
    return plan


def shard_body(low: int, high: int, block: list[str]) -> str:
    lines = [f"# Profile index {low:03d}-{high:03d}", "", SHARD_NOTE, ""]
    lines += [f"- [`{name}`](../{name})" for name in block]
    return "\n".join(lines) + "\n"


def readme_body(readme: str, plan: list[tuple[str, int, int, list[str]]]) -> str:
    matches = list(README_LINK_RE.finditer(readme))
    if not matches:
        raise ProfileIndexError("no index shard link block found in README.md")
    links = "\n".join(
        f"- [`{low:03d}–{high:03d}`](index/{name})" for name, low, high, _ in plan
    )
    return readme[: matches[0].start()] + links + readme[matches[-1].end() :]


class ProfileIndex:
    """Planned index state for one profiles directory."""

    def __init__(self, profiles_dir: Path) -> None:
        self.profiles_dir = profiles_dir
        self.index_dir = profiles_dir / "index"
        self.readme = profiles_dir / "README.md"
        if not self.readme.is_file():
            raise ProfileIndexError(f"missing README: {self.readme}")
        self.names = profile_names(profiles_dir)
        self.plan = shard_plan(self.names)
        self.expected_shards = {
            name: shard_body(low, high, block) for name, low, high, block in self.plan
        }
        self.current_readme = self.readme.read_text(encoding="utf-8")
        self.expected_readme = readme_body(self.current_readme, self.plan)

    def current_shards(self) -> dict[str, str]:
        if not self.index_dir.is_dir():
            return {}
        return {
            path.name: path.read_text(encoding="utf-8")
            for path in sorted(self.index_dir.glob("*.md"))
            if SHARD_NAME_RE.match(path.name)
        }

    def report(self) -> dict[str, object]:
        current = self.current_shards()
        result: dict[str, object] = {
            "profile_count": len(self.names),
            "shard_count": len(self.expected_shards),
            "missing_shards": sorted(set(self.expected_shards) - set(current)),
            "stale_shards": sorted(set(current) - set(self.expected_shards)),
            "outdated_shards": sorted(
                name
                for name, body in self.expected_shards.items()
                if name in current and current[name] != body
            ),
            "readme_outdated": self.expected_readme != self.current_readme,
        }
        result["current"] = not (
            result["missing_shards"]
            or result["stale_shards"]
            or result["outdated_shards"]
            or result["readme_outdated"]
        )
        return result

    def write(self) -> list[str]:
        current = self.current_shards()
        changed = []
        self.index_dir.mkdir(parents=True, exist_ok=True)
        for name, body in self.expected_shards.items():
            if current.get(name) != body:
                (self.index_dir / name).write_text(body, encoding="utf-8", newline="\n")
                changed.append(name)
        for name in sorted(set(current) - set(self.expected_shards)):
            (self.index_dir / name).unlink()
            changed.append(f"removed:{name}")
        if self.expected_readme != self.current_readme:
            self.readme.write_text(self.expected_readme, encoding="utf-8", newline="\n")
            self.current_readme = self.expected_readme
            changed.append("README.md")
        return changed


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--profiles-dir",
        default=str(DEFAULT_PROFILES_DIR),
        help="Profiles directory holding the profile JSON files and index/",
    )
    result.add_argument(
        "--write",
        action="store_true",
        help="Regenerate shards and README links. Without it, only report the diff",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        index = ProfileIndex(Path(args.profiles_dir))
        report = index.report()
        if args.write:
            report["written"] = index.write()
            report["current"] = True
    except (ProfileIndexError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["current"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

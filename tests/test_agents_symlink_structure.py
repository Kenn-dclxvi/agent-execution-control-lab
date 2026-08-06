from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# path-scoped agent instructions: root と領域ディレクトリ
SCOPES = [
    "",
    "docs",
    "prompts",
    "evaluations",
    "evaluations/targets",
    "evaluations/targets/click",
    "scripts",
    "tests",
    "layer2",
]


def _scoped(name: str, scope: str) -> str:
    return f"{scope}/{name}" if scope else name


def _index_entries(paths: list[str]) -> dict[str, tuple[str, str]]:
    """git index 上の (mode, blob) を path 別に返す。

    checkout 環境の表示ではなく Git object 上の tree mode を確認する
    （tests/AGENTS.md の要求）。
    """
    out = subprocess.run(
        ["git", "ls-files", "-s", "--", *paths],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    entries: dict[str, tuple[str, str]] = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        mode, blob, _stage = meta.split()
        entries[path] = (mode, blob)
    return entries


class AgentsSymlinkStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        agents = [_scoped("AGENTS.md", s) for s in SCOPES]
        claude = [_scoped("CLAUDE.md", s) for s in SCOPES]
        self.entries = _index_entries(agents + claude)

    def test_agents_are_regular_files(self) -> None:
        for scope in SCOPES:
            path = _scoped("AGENTS.md", scope)
            self.assertIn(path, self.entries, f"missing tracked file: {path}")
            mode, _ = self.entries[path]
            self.assertEqual(
                mode, "100644", f"{path} must be a regular file (mode 100644)"
            )

    def test_claude_are_relative_symlinks_to_agents(self) -> None:
        blobs = set()
        for scope in SCOPES:
            path = _scoped("CLAUDE.md", scope)
            self.assertIn(path, self.entries, f"missing tracked file: {path}")
            mode, blob = self.entries[path]
            self.assertEqual(
                mode, "120000", f"{path} must be a symlink (mode 120000)"
            )
            target = subprocess.run(
                ["git", "cat-file", "-p", blob],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            self.assertEqual(
                target,
                "AGENTS.md",
                f"{path} link target must be exactly 'AGENTS.md', got {target!r}",
            )
            blobs.add(blob)
        # 全 CLAUDE.md は同一の相対 target を指すため blob は 1 種類に収束する。
        self.assertEqual(
            len(blobs), 1, "all CLAUDE.md symlinks must share one relative target blob"
        )


if __name__ == "__main__":
    unittest.main()

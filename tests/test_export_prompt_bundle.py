from __future__ import annotations

import hashlib
import platform
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import (
    bundle_sha256,
    duplicate_candidate,
    export_baseline,
    verify_bundle,
)
from scripts.run_codex_evaluation import parse_usage, prepare_runtime_links, render_task


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


class ExportPromptBundleTest(unittest.TestCase):
    def test_exports_and_verifies_empty_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            git(source, "init", "-q")
            git(source, "config", "user.name", "Bundle Test")
            git(source, "config", "user.email", "bundle@example.invalid")
            (source / "tracked.txt").write_text("fixture\n", encoding="utf-8")
            git(source, "add", "tracked.txt")
            git(source, "commit", "-qm", "source")
            commit = git(source, "rev-parse", "HEAD")

            bundle_path = root / "empty-baseline"
            manifest = export_baseline(
                source,
                commit,
                "https://example.invalid/source.git",
                bundle_path,
                "no-prompt-files-r1",
                [],
            )

            self.assertEqual(manifest["files"], [])
            self.assertEqual(manifest["bundle_sha256"], bundle_sha256([]))
            self.assertEqual(list((bundle_path / "files").iterdir()), [])
            self.assertEqual(verify_bundle(bundle_path)["prompt_identity"], "no-prompt-files-r1")

    def test_exports_baseline_and_bit_identical_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            git(source, "init", "-q")
            git(source, "config", "user.name", "Bundle Test")
            git(source, "config", "user.email", "bundle@example.invalid")
            (source / "docs").mkdir()
            (source / "AGENTS.md").write_text("root instructions\n", encoding="utf-8")
            (source / "docs" / "AGENTS.md").write_text("docs instructions\n", encoding="utf-8")
            (source / "CLAUDE.md").symlink_to("AGENTS.md")
            git(source, "add", "AGENTS.md", "CLAUDE.md", "docs/AGENTS.md")
            git(source, "commit", "-qm", "prompt source")
            commit = git(source, "rev-parse", "HEAD")

            baseline_path = root / "baseline"
            candidate_path = root / "candidate"
            baseline = export_baseline(
                source,
                commit,
                "https://example.invalid/source.git",
                baseline_path,
                "baseline-r1",
                ["docs/AGENTS.md", "CLAUDE.md", "AGENTS.md"],
            )
            candidate = duplicate_candidate(baseline_path, candidate_path, "candidate-r1")

            self.assertEqual(baseline["artifact"]["artifact_role"], "baseline")
            self.assertEqual(candidate["artifact"]["artifact_role"], "candidate")
            self.assertEqual(candidate["artifact"]["baseline_identity"], "baseline-r1")
            self.assertEqual(candidate["content_relation"]["kind"], "bit_identical_copy")
            self.assertEqual(candidate["bundle_sha256"], baseline["bundle_sha256"])
            self.assertEqual(candidate["files"], baseline["files"])
            # 命令ファイルは自動読込対象名を避けて suffix 付きで格納され、実体名は
            # target として manifest 側にのみ残る（bundle_sha256 は不変）。
            self.assertEqual(baseline["storage_format"], "instruction-suffixed/v1")
            self.assertEqual((candidate_path / "files" / "AGENTS.md.txt").read_bytes(), b"root instructions\n")
            self.assertFalse((candidate_path / "files" / "AGENTS.md").exists())
            self.assertTrue((candidate_path / "files" / "CLAUDE.md.txt").is_symlink())
            self.assertEqual((candidate_path / "files" / "CLAUDE.md.txt").readlink(), Path("AGENTS.md.txt"))
            self.assertFalse((candidate_path / "files" / "CLAUDE.md").exists())
            self.assertEqual(
                sorted(entry["target"] for entry in candidate["files"]),
                ["AGENTS.md", "CLAUDE.md", "docs/AGENTS.md"],
            )
            self.assertEqual(verify_bundle(candidate_path)["prompt_identity"], "candidate-r1")

    def test_renders_case_task_and_parses_codex_usage(self) -> None:
        task = render_task({"payload": {"trial_prompt_input": {"goal": "restore behavior"}}})
        total, usage = parse_usage(
            b'{"type":"turn.completed","usage":{"input_tokens":120,"output_tokens":30}}\n'
        )

        self.assertIn('"goal": "restore behavior"', task)
        self.assertEqual(total, 150)
        self.assertEqual(usage["input_tokens"], 120)

    def test_prepares_identity_checked_ignored_runtime_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            runtime = root / "runtime"
            workspace.mkdir()
            runtime.mkdir()
            git(workspace, "init", "-q")
            git(workspace, "config", "user.name", "Runtime Test")
            git(workspace, "config", "user.email", "runtime@example.invalid")
            (workspace / ".gitignore").write_text(".venv/\n", encoding="utf-8")
            git(workspace, "add", ".gitignore")
            git(workspace, "commit", "-qm", "workspace")
            identity = runtime / "pyvenv.cfg"
            identity.write_text("runtime identity\n", encoding="utf-8")
            expected = hashlib.sha256(identity.read_bytes()).hexdigest()
            result = prepare_runtime_links(
                workspace,
                [
                    {
                        "target": ".venv",
                        "source": str(runtime),
                        "identity_file": "pyvenv.cfg",
                        "identity_sha256": expected,
                    }
                ],
            )

            self.assertTrue((workspace / ".venv").is_symlink())
            self.assertEqual(result[0]["identity_sha256"], expected)
            self.assertEqual(git(workspace, "status", "--short"), "")

    def test_can_copy_runtime_inside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            runtime = root / "runtime"
            workspace.mkdir()
            runtime.mkdir()
            git(workspace, "init", "-q")
            git(workspace, "config", "user.name", "Runtime Test")
            git(workspace, "config", "user.email", "runtime@example.invalid")
            (workspace / ".gitignore").write_text(".venv/\n", encoding="utf-8")
            git(workspace, "add", ".gitignore")
            git(workspace, "commit", "-qm", "workspace")
            identity = runtime / "pyvenv.cfg"
            identity.write_text("runtime identity\n", encoding="utf-8")
            expected = hashlib.sha256(identity.read_bytes()).hexdigest()

            result = prepare_runtime_links(
                workspace,
                [
                    {
                        "target": ".venv",
                        "source": str(runtime),
                        "identity_file": "pyvenv.cfg",
                        "identity_sha256": expected,
                        "materialization": "copy",
                    }
                ],
            )

            self.assertFalse((workspace / ".venv").is_symlink())
            self.assertEqual((workspace / ".venv" / "pyvenv.cfg").read_bytes(), identity.read_bytes())
            self.assertEqual(result[0]["materialization"], "copy")
            self.assertEqual(git(workspace, "status", "--short"), "")

    def test_can_materialize_shared_venv_with_local_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            git(workspace, "init", "-q")
            git(workspace, "config", "user.name", "Runtime Test")
            git(workspace, "config", "user.email", "runtime@example.invalid")
            (workspace / ".gitignore").write_text(".venv/\n", encoding="utf-8")
            git(workspace, "add", ".gitignore")
            git(workspace, "commit", "-qm", "workspace")

            runtime = root / "runtime"
            subprocess.run(
                [sys.executable, "-m", "venv", runtime],
                check=True,
                capture_output=True,
            )
            purelib = subprocess.run(
                [
                    runtime / "bin" / "python",
                    "-c",
                    "import sysconfig; print(sysconfig.get_path('purelib'))",
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            Path(purelib, "pytest.py").write_text("VALUE = 'shared-pytest'\n", encoding="utf-8")
            identity = runtime / "requirements.freeze.txt"
            frozen = subprocess.run(
                [runtime / "bin" / "python", "-m", "pip", "freeze", "--all"],
                check=True,
                capture_output=True,
            ).stdout
            identity.write_bytes(frozen)

            result = prepare_runtime_links(
                workspace,
                [
                    {
                        "target": ".venv",
                        "source": str(runtime),
                        "identity_file": "requirements.freeze.txt",
                        "identity_sha256": hashlib.sha256(identity.read_bytes()).hexdigest(),
                        "materialization": "venv_shim",
                        "python_version": platform.python_version(),
                    }
                ],
            )

            local_runtime = (workspace / ".venv").resolve()
            local_python = local_runtime / "bin" / "python"
            probe = subprocess.run(
                [
                    local_python,
                    "-c",
                    (
                        "import pip, pytest, sys; "
                        "print(pip.__version__); print(pytest.VALUE); "
                        "print(sys.prefix); print(sys.executable)"
                    ),
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
            activated = subprocess.run(
                ["/bin/sh", "-c", '. .venv/bin/activate && printf "%s" "$VIRTUAL_ENV"'],
                cwd=workspace,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            byte_size = sum(
                path.stat().st_size
                for path in (workspace / ".venv").rglob("*")
                if path.is_file()
            )

            self.assertTrue(probe[0])
            self.assertEqual(probe[1], "shared-pytest")
            self.assertEqual(probe[2:], [str(local_runtime), str(local_python)])
            self.assertEqual(activated, str(local_runtime))
            self.assertEqual(result[0]["materialization"], "venv_shim")
            self.assertEqual(result[0]["python_version"], platform.python_version())
            self.assertFalse((workspace / ".venv").is_symlink())
            self.assertLess(byte_size, 1_000_000)


if __name__ == "__main__":
    unittest.main()

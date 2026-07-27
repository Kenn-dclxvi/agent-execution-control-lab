from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import export_baseline
from scripts.prepare_desktop_evaluation_slot import DesktopSlotError, prepare_desktop_slot


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        check=True,
        text=True,
    )
    return completed.stdout.strip()


class PrepareDesktopEvaluationSlotTest(unittest.TestCase):
    def source_repo(self, root: Path) -> tuple[Path, str, str]:
        source = root / "source"
        source.mkdir()
        git(source, "init", "-q")
        git(source, "config", "user.name", "Desktop Slot Test")
        git(source, "config", "user.email", "slot@example.invalid")
        (source / ".gitignore").write_text(".venv/\n", encoding="utf-8")
        (source / "AGENTS.md").write_text("candidate 43\n", encoding="utf-8")
        git(source, "add", ".gitignore", "AGENTS.md")
        git(source, "commit", "-qm", "target")
        return source, git(source, "rev-parse", "HEAD"), git(source, "rev-parse", "HEAD^{tree}")

    def bundle(self, source: Path, ref: str, output: Path, identity: str) -> tuple[Path, str]:
        manifest = export_baseline(
            source,
            ref,
            "https://example.invalid/THE-CAPTION.git",
            output,
            identity,
            ["AGENTS.md"],
        )
        return output, manifest["bundle_sha256"]

    def runtime_link(self, root: Path) -> tuple[Path, str]:
        runtime = root / "runtime"
        runtime.mkdir()
        identity = runtime / "identity.txt"
        identity.write_text("runtime r1\n", encoding="utf-8")
        return runtime, hashlib.sha256(identity.read_bytes()).hexdigest()

    def test_reuses_one_managed_workspace_for_different_prompt_bundles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target_commit, target_tree = self.source_repo(root)
            bundle43, hash43 = self.bundle(source, target_commit, root / "c43", "c43-r1")
            (source / "AGENTS.md").write_text("candidate 45\n", encoding="utf-8")
            git(source, "commit", "-qam", "candidate 45 source")
            bundle45, hash45 = self.bundle(
                source, git(source, "rev-parse", "HEAD"), root / "c45", "c45-r1"
            )
            runtime, runtime_hash = self.runtime_link(root)
            workspace = root / "desktop-slot-01"
            runtime_links = [
                {
                    "source": str(runtime),
                    "target": ".venv",
                    "identity_file": "identity.txt",
                    "identity_sha256": runtime_hash,
                    "materialization": "symlink",
                }
            ]

            first = prepare_desktop_slot(
                source_repo=source,
                workspace=workspace,
                target_commit=target_commit,
                target_tree=target_tree,
                prompt_bundle=bundle43,
                bundle_sha256=hash43,
                runtime_links=runtime_links,
            )
            first_git_dir = git(workspace, "rev-parse", "--git-dir")

            second = prepare_desktop_slot(
                source_repo=source,
                workspace=workspace,
                target_commit=target_commit,
                target_tree=target_tree,
                prompt_bundle=bundle45,
                bundle_sha256=hash45,
                runtime_links=runtime_links,
            )

            self.assertEqual(first["workspace"], second["workspace"])
            self.assertEqual(first_git_dir, git(workspace, "rev-parse", "--git-dir"))
            self.assertNotEqual(first["prompt_overlay_commit"], second["prompt_overlay_commit"])
            self.assertEqual((workspace / "AGENTS.md").read_text(encoding="utf-8"), "candidate 45\n")
            self.assertEqual(git(workspace, "rev-parse", "HEAD^"), target_commit)
            self.assertEqual(git(workspace, "status", "--short"), "")
            self.assertTrue((workspace / ".venv").is_symlink())
            self.assertEqual(second["prompt_set_identity"]["name"], "c45-r1")
            self.assertEqual(
                second["model_context_gate"],
                {
                    "required_user_config": {"features.memories": False},
                    "required_memory_instructions": "absent",
                },
            )
            self.assertEqual(
                second["codex_app_command"],
                ["codex", "app", str(workspace.resolve())],
            )

    def test_prepares_empty_bundle_as_an_empty_overlay_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _, _ = self.source_repo(root)
            (source / "AGENTS.md").unlink()
            git(source, "add", "AGENTS.md")
            git(source, "commit", "-qm", "remove repository instructions")
            target_commit = git(source, "rev-parse", "HEAD")
            target_tree = git(source, "rev-parse", "HEAD^{tree}")
            bundle_path = root / "empty-bundle"
            manifest = export_baseline(
                source,
                target_commit,
                "https://example.invalid/click.git",
                bundle_path,
                "no-agents-r1",
                [],
            )

            receipt = prepare_desktop_slot(
                source_repo=source,
                workspace=root / "desktop-slot-01",
                target_commit=target_commit,
                target_tree=target_tree,
                prompt_bundle=bundle_path,
                bundle_sha256=manifest["bundle_sha256"],
            )
            workspace = Path(receipt["workspace"])

            self.assertFalse((workspace / "AGENTS.md").exists())
            self.assertEqual(git(workspace, "rev-parse", "HEAD^"), target_commit)
            self.assertEqual(git(workspace, "rev-parse", "HEAD^{tree}"), target_tree)
            self.assertEqual(git(workspace, "status", "--short"), "")

    def test_refuses_to_reuse_a_dirty_managed_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target_commit, target_tree = self.source_repo(root)
            bundle, bundle_hash = self.bundle(source, target_commit, root / "bundle", "c43-r1")
            workspace = root / "desktop-slot-01"
            prepare_desktop_slot(
                source_repo=source,
                workspace=workspace,
                target_commit=target_commit,
                target_tree=target_tree,
                prompt_bundle=bundle,
                bundle_sha256=bundle_hash,
            )
            (workspace / "AGENTS.md").write_text("user work\n", encoding="utf-8")

            with self.assertRaisesRegex(DesktopSlotError, "dirty Desktop slot"):
                prepare_desktop_slot(
                    source_repo=source,
                    workspace=workspace,
                    target_commit=target_commit,
                    target_tree=target_tree,
                    prompt_bundle=bundle,
                    bundle_sha256=bundle_hash,
                )

            self.assertEqual((workspace / "AGENTS.md").read_text(encoding="utf-8"), "user work\n")

    def test_refuses_to_adopt_an_unmanaged_existing_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target_commit, target_tree = self.source_repo(root)
            bundle, bundle_hash = self.bundle(source, target_commit, root / "bundle", "c43-r1")
            unmanaged = root / "unmanaged"
            git(root, "clone", "-q", str(source), str(unmanaged))

            with self.assertRaisesRegex(DesktopSlotError, "unmanaged workspace"):
                prepare_desktop_slot(
                    source_repo=source,
                    workspace=unmanaged,
                    target_commit=target_commit,
                    target_tree=target_tree,
                    prompt_bundle=bundle,
                    bundle_sha256=bundle_hash,
                )


if __name__ == "__main__":
    unittest.main()

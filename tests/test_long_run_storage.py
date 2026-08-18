from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from layer2.extensions.long_run_storage.long_run_storage import (
    GIB,
    LongRunStorageError,
    compact_batch,
    create_rating_view,
    evaluate_capacity,
    materialize_layer1,
    seal_batch,
)


class LongRunStorageTest(unittest.TestCase):
    def git(self, workspace: Path, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=workspace,
            capture_output=True,
            check=True,
            text=True,
        )
        return completed.stdout.strip()

    def extract_archive(self, archive: Path, destination: Path) -> None:
        destination.mkdir(parents=True, exist_ok=True)
        zstd = subprocess.Popen(
            ["zstd", "-q", "-dc", str(archive)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertIsNotNone(zstd.stdout)
        self.assertIsNotNone(zstd.stderr)
        assert zstd.stdout is not None
        assert zstd.stderr is not None
        with tarfile.open(fileobj=zstd.stdout, mode="r|") as handle:
            handle.extractall(destination, filter="data")
        zstd.stdout.close()
        stderr = zstd.stderr.read().decode("utf-8", errors="replace")
        zstd.stderr.close()
        self.assertEqual(zstd.wait(), 0, stderr)

    def make_batch(self, root: Path, with_usage: bool = True) -> tuple[Path, str]:
        batch = root / "batch-001"
        cycle = batch / "cycle"
        run_id = "a" * 32
        evidence = cycle / "layer2" / "evidence" / run_id
        workspace = evidence / "workspace"
        extension = cycle / "layer2" / "extensions" / run_id
        adapter = extension / "codex-adapter"
        fixture = cycle / "layer1" / "fixtures" / "CASE-1"
        fixture.mkdir(parents=True)
        (fixture / "large-fixture.txt").write_text("fixture\n", encoding="utf-8")
        (fixture / "empty-directory").mkdir()
        (cycle / "layer1" / "set.json").write_text("{}\n", encoding="utf-8")
        workspace.mkdir(parents=True)
        self.git(workspace, "init", "-q")
        self.git(workspace, "config", "user.email", "test@example.invalid")
        self.git(workspace, "config", "user.name", "Test")
        (workspace / "src.py").write_text("before = True\n", encoding="utf-8")
        self.git(workspace, "add", "src.py")
        self.git(workspace, "commit", "-qm", "fixture")
        (workspace / "AGENTS.md").write_text("prompt\n", encoding="utf-8")
        self.git(workspace, "add", "AGENTS.md")
        self.git(workspace, "commit", "-qm", "prompt overlay")
        overlay_commit = self.git(workspace, "rev-parse", "HEAD")
        (workspace / "src.py").write_text("after = True\n", encoding="utf-8")
        (workspace / "new.txt").write_text("new result\n", encoding="utf-8")
        (workspace / "AGENTS.md").write_text("prompt edited by agent\n", encoding="utf-8")

        bundle = root / "bundle"
        bundle.mkdir()
        (bundle / "manifest.json").write_text(
            json.dumps({"files": [{"target": "AGENTS.md"}]}), encoding="utf-8"
        )
        capsule = {
            "parameters": {"prompt_bundle": str(bundle)},
            "binding": {"case_id": "CASE-1", "iteration": 1},
        }
        capsules = cycle / "layer2" / "capsules"
        capsules.mkdir(parents=True)
        (capsules / f"{run_id}.json").write_text(json.dumps(capsule), encoding="utf-8")
        evidence.mkdir(parents=True, exist_ok=True)
        (evidence / "case.json").write_text('{"id":"CASE-1"}\n', encoding="utf-8")
        (evidence / "usage.json").write_text('{"total_tokens":123}\n', encoding="utf-8")
        (evidence / "stdout.bin").write_bytes(b"raw output")
        (evidence / "execution.json").write_text(
            json.dumps({"status": "valid", "run_id": run_id}), encoding="utf-8"
        )
        adapter.mkdir(parents=True)
        (adapter / "final-response.txt").write_text("tests passed\n", encoding="utf-8")
        (adapter / "codex-events.jsonl").write_text("{}\n", encoding="utf-8")
        (adapter / "execution.json").write_text(
            json.dumps(
                {
                    "prompt_overlay_commit": overlay_commit,
                    "codex_exit_code": 0,
                    "final_changed_paths": ["AGENTS.md", "new.txt", "src.py"],
                    "unexpected_changed_paths": [],
                }
            ),
            encoding="utf-8",
        )
        if with_usage:
            usage = extension / "all-agent-usage"
            usage.mkdir()
            (usage / "usage.json").write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.all-agent-usage/v1",
                        "all_agent_total_tokens": 123,
                        "sessions": [{"thread_id": "root", "usage": {"total_tokens": 123}}],
                    }
                ),
                encoding="utf-8",
            )
        (batch / "summary.json").write_text('{"status":"complete"}\n', encoding="utf-8")
        (batch / "plan.json").write_text("{}\n", encoding="utf-8")
        runner = batch / "runner-evidence"
        runner.mkdir()
        (runner / "attempts.jsonl").write_text("{}\n", encoding="utf-8")
        return batch, run_id

    def test_capacity_guard_accounts_for_next_batch(self) -> None:
        allowed = evaluate_capacity(30 * GIB, 25 * GIB, 20 * GIB, 4 * GIB)
        stopped = evaluate_capacity(28 * GIB, 25 * GIB, 20 * GIB, 4 * GIB)
        breached = evaluate_capacity(19 * GIB, 25 * GIB, 20 * GIB)
        self.assertTrue(allowed["dispatch_allowed"])
        self.assertEqual(stopped["status"], "dispatch_stopped")
        self.assertEqual(breached["status"], "hard_floor_breached")

    def test_layer1_clone_is_fail_closed_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            destination = root / "destination"

            def fake_copy(_source: Path, target: Path) -> str:
                target.mkdir()
                return "copy"

            with mock.patch(
                "layer2.extensions.long_run_storage.long_run_storage.materialize_tree",
                side_effect=fake_copy,
            ):
                with self.assertRaisesRegex(LongRunStorageError, "did not use clonefile"):
                    materialize_layer1(source, destination, root / "receipt.json")
            self.assertFalse(destination.exists())

    @unittest.skipUnless(shutil.which("zstd"), "zstd is required")
    def test_seal_losslessly_archives_fixture_and_workspace_before_prune(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            batch, run_id = self.make_batch(Path(temporary))
            receipt = seal_batch(batch)
            rating = batch / "cycle" / "layer2" / "evidence" / run_id / "rating-view"
            diff = (rating / "result.diff").read_text(encoding="utf-8")
            self.assertIn("src.py", diff)
            self.assertIn("new.txt", diff)
            self.assertNotIn("AGENTS.md", diff)
            self.assertFalse((rating.parent / "workspace").exists())
            self.assertTrue((batch / "cycle" / "layer1" / "fixtures").is_dir())
            archive = batch / "compact" / "execution-evidence.tar.zst"
            self.assertTrue(archive.is_file())
            restored = Path(temporary) / "restored-execution"
            self.extract_archive(archive, restored)
            restored_fixture = (
                restored / "cycle" / "layer1" / "fixtures" / "CASE-1"
            )
            restored_workspace = (
                restored / "cycle" / "layer2" / "evidence" / run_id / "workspace"
            )
            self.assertEqual(
                (restored_fixture / "large-fixture.txt").read_text(encoding="utf-8"),
                "fixture\n",
            )
            self.assertTrue((restored_fixture / "empty-directory").is_dir())
            self.assertEqual(
                (restored_workspace / "src.py").read_text(encoding="utf-8"),
                "after = True\n",
            )
            self.assertEqual(
                (restored_workspace / "new.txt").read_text(encoding="utf-8"),
                "new result\n",
            )
            manifest = json.loads(
                (batch / "compact" / "execution-seal.json").read_text(encoding="utf-8")
            )
            archived_paths = {entry["path"] for entry in manifest["entries"]}
            self.assertIn(
                "cycle/layer1/fixtures/CASE-1/large-fixture.txt", archived_paths
            )
            self.assertIn(
                f"cycle/layer2/evidence/{run_id}/workspace/src.py", archived_paths
            )
            self.assertGreater(receipt["allocated_bytes_reclaimed"], 0)

    @unittest.skipUnless(shutil.which("zstd"), "zstd is required")
    def test_seal_cli_prunes_matching_codex_project_config(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            batch, run_id = self.make_batch(root)
            workspace = (
                batch.resolve()
                / "cycle"
                / "layer2"
                / "evidence"
                / run_id
                / "workspace"
            )
            config = root / "config.toml"
            config.write_text(
                f'[projects."{workspace}"]\ntrust_level = "trusted"\n',
                encoding="utf-8",
            )
            script = (
                Path(__file__).parents[1]
                / "layer2/extensions/long_run_storage/long_run_storage.py"
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "seal-batch",
                    "--batch",
                    str(batch),
                    "--codex-config",
                    str(config),
                ],
                capture_output=True,
                check=True,
                text=True,
            )

            output = json.loads(completed.stdout)
            cleanup = output["codex_project_config_cleanup"]
            self.assertEqual(cleanup["status"], "updated")
            self.assertEqual(cleanup["removed_paths"], [str(workspace)])
            self.assertNotIn(str(workspace), config.read_text(encoding="utf-8"))
            self.assertTrue(
                (batch / "compact/codex-project-config-prune-receipt.json").is_file()
            )

    @unittest.skipUnless(shutil.which("zstd"), "zstd is required")
    def test_seal_rejects_valid_run_without_all_agent_usage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            batch, _ = self.make_batch(Path(temporary), with_usage=False)
            with self.assertRaisesRegex(LongRunStorageError, "all-agent usage"):
                seal_batch(batch)
            self.assertFalse((batch / "compact").exists())

    @unittest.skipUnless(shutil.which("zstd"), "zstd is required")
    def test_seal_reuses_only_matching_existing_rating_view(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            batch, run_id = self.make_batch(Path(temporary))
            create_rating_view(batch / "cycle", run_id)
            layer3 = batch / "cycle/layer3/ratings"
            layer3.mkdir(parents=True)
            (layer3 / f"{run_id}.json").write_text(
                json.dumps({"run_id": run_id}), encoding="utf-8"
            )
            receipt = seal_batch(batch, reuse_existing_rating_views=True)
            self.assertIn(
                f"cycle/layer2/evidence/{run_id}/workspace",
                receipt["pruned_paths"],
            )

        with tempfile.TemporaryDirectory() as temporary:
            batch, run_id = self.make_batch(Path(temporary))
            create_rating_view(batch / "cycle", run_id)
            layer3 = batch / "cycle/layer3/ratings"
            layer3.mkdir(parents=True)
            (layer3 / f"{run_id}.json").write_text(
                json.dumps({"run_id": run_id}), encoding="utf-8"
            )
            validation = (
                batch / "cycle/layer2/evidence" / run_id / "rating-view/validation.json"
            )
            validation.write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(LongRunStorageError, "validation mismatch"):
                seal_batch(batch, reuse_existing_rating_views=True)
            self.assertFalse((batch / "compact").exists())

    @unittest.skipUnless(shutil.which("zstd"), "zstd is required")
    def test_alternate_real_cycle_path_seals_and_compacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            batch, run_id = self.make_batch(Path(temporary))
            alternate = batch / "cycle-r3"
            (batch / "cycle").rename(alternate)
            create_rating_view(alternate, run_id)
            ratings = alternate / "layer3/ratings"
            ratings.mkdir(parents=True)
            (ratings / f"{run_id}.json").write_text(
                json.dumps({"run_id": run_id}), encoding="utf-8"
            )
            layer4 = alternate / "layer4"
            layer4.mkdir()
            registration = layer4 / "result-registration.json"
            registration.write_text('{"status":"registered"}\n', encoding="utf-8")
            seal_batch(
                batch,
                cycle_path=Path("cycle-r3"),
                reuse_existing_rating_views=True,
            )
            receipt = compact_batch(batch, cycle_path=Path("cycle-r3"))
            self.assertFalse((alternate / "layer2").exists())
            self.assertIn("cycle-r3/layer2", receipt["pruned_paths"])
            self.assertTrue(registration.is_file())

    def test_cycle_path_rejects_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            batch, _ = self.make_batch(Path(temporary))
            (batch / "cycle-real").mkdir()
            shutil.rmtree(batch / "cycle")
            (batch / "cycle").symlink_to("cycle-real")
            with self.assertRaisesRegex(LongRunStorageError, "real directory"):
                seal_batch(batch)

    @unittest.skipUnless(shutil.which("zstd"), "zstd is required")
    def test_final_compact_requires_registration_and_keeps_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            batch, run_id = self.make_batch(Path(temporary))
            seal_batch(batch)
            with self.assertRaisesRegex(LongRunStorageError, "result-registration"):
                compact_batch(batch)
            layer3 = batch / "cycle" / "layer3" / "ratings"
            layer3.mkdir(parents=True)
            (layer3 / "rating.json").write_text('{"quality_score":4}\n', encoding="utf-8")
            layer4 = batch / "cycle" / "layer4"
            layer4.mkdir()
            registration = layer4 / "result-registration.json"
            registration.write_text('{"status":"registered"}\n', encoding="utf-8")
            receipt = compact_batch(batch)
            self.assertTrue((batch / "compact" / "final-evidence.tar.zst").is_file())
            self.assertTrue(registration.is_file())
            self.assertTrue((batch / "cycle" / "layer1" / "fixtures").is_dir())
            self.assertFalse((batch / "cycle" / "layer2").exists())
            self.assertIn("cycle/layer2", receipt["pruned_paths"])
            restored = Path(temporary) / "restored-final"
            self.extract_archive(
                batch / "compact" / "execution-evidence.tar.zst", restored
            )
            self.extract_archive(batch / "compact" / "final-evidence.tar.zst", restored)
            self.assertEqual(
                (
                    restored
                    / "cycle"
                    / "layer1"
                    / "fixtures"
                    / "CASE-1"
                    / "large-fixture.txt"
                ).read_text(encoding="utf-8"),
                "fixture\n",
            )
            self.assertTrue(
                (
                    restored
                    / "cycle"
                    / "layer2"
                    / "evidence"
                    / run_id
                    / "workspace"
                    / ".git"
                ).is_dir()
            )
            self.assertTrue(
                (restored / "cycle" / "layer3" / "ratings" / "rating.json").is_file()
            )
            self.assertTrue(
                restored.joinpath("cycle/layer4/result-registration.json").is_file()
            )


if __name__ == "__main__":
    unittest.main()

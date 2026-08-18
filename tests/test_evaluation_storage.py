from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "evaluation_storage.py"


class EvaluationStorageTest(unittest.TestCase):
    def cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            check=check,
            capture_output=True,
            text=True,
        )

    def make_run(self, storage: Path, name: str) -> Path:
        run = storage / "runs" / name
        run.mkdir(parents=True)
        (run / "evidence.txt").write_text(f"{name}\n", encoding="utf-8")
        old = time.time() - 5 * 86400
        os.utime(run / "evidence.txt", (old, old))
        os.utime(run, (old, old))
        return run

    def setup_storage(self, root: Path) -> tuple[Path, Path, Path]:
        storage = root / "storage"
        repository = root / "repository"
        repository.mkdir()
        scratch = self.make_run(storage, "scratch")
        (scratch / "recent-directory-metadata").mkdir()
        old = time.time() - 5 * 86400
        os.utime(scratch, (old, old))
        referenced = self.make_run(storage, "referenced")
        registered = self.make_run(storage, "registered")
        registration = registered / "cycle" / "layer4" / "result-registration.json"
        registration.parent.mkdir(parents=True)
        registration.write_text("{}\n", encoding="utf-8")
        os.utime(registration, (old, old))
        os.utime(registration.parent, (old, old))
        os.utime(registration.parent.parent, (old, old))
        os.utime(registered, (old, old))
        (repository / "result.md").write_text(
            f"raw evidence: `{referenced.resolve()}`\n", encoding="utf-8"
        )
        return storage, repository, scratch

    def test_audit_and_manifest_guarded_gc(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            storage, repository, scratch = self.setup_storage(Path(tmp))
            audit = self.cli(
                "audit",
                "--root",
                str(storage),
                "--repository",
                str(repository),
                "--scratch-days",
                "3",
            )
            report = json.loads(audit.stdout)
            self.assertEqual(report["gc_candidates"], ["runs/scratch"])
            protected = {item["path"]: item["protected_by"] for item in report["runs"]}
            self.assertIn("repository_reference", protected["runs/referenced"])
            self.assertIn("result_registration", protected["runs/registered"])

            manifest = Path(tmp) / "gc-manifest.json"
            receipt = Path(tmp) / "gc-receipt.json"
            planned = self.cli(
                "gc",
                "--root",
                str(storage),
                "--repository",
                str(repository),
                "--scratch-days",
                "3",
                "--manifest",
                str(manifest),
            )
            self.assertEqual(json.loads(planned.stdout)["entry_count"], 1)
            applied = self.cli(
                "gc",
                "--root",
                str(storage),
                "--repository",
                str(repository),
                "--manifest",
                str(manifest),
                "--apply",
                "--receipt",
                str(receipt),
            )
            self.assertEqual(json.loads(applied.stdout)["deleted_count"], 1)
            self.assertFalse(scratch.exists())
            self.assertTrue((storage / "runs" / "referenced").exists())
            self.assertTrue((storage / "runs" / "registered").exists())
            self.assertTrue(receipt.exists())

    def test_apply_refuses_content_changed_after_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            storage, repository, scratch = self.setup_storage(Path(tmp))
            manifest = Path(tmp) / "gc-manifest.json"
            receipt = Path(tmp) / "gc-receipt.json"
            self.cli(
                "gc",
                "--root",
                str(storage),
                "--repository",
                str(repository),
                "--scratch-days",
                "3",
                "--manifest",
                str(manifest),
            )
            (scratch / "evidence.txt").write_text("changed\n", encoding="utf-8")
            completed = self.cli(
                "gc",
                "--root",
                str(storage),
                "--repository",
                str(repository),
                "--manifest",
                str(manifest),
                "--apply",
                "--receipt",
                str(receipt),
                check=False,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertTrue(scratch.exists())
            self.assertFalse(receipt.exists())

    @unittest.skipUnless(sys.platform == "darwin", "clonefile is a macOS facility")
    def test_identical_git_packs_are_rematerialized_and_remain_independent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "storage"
            packs = [
                root / "runs" / name / "fixture" / ".git" / "objects" / "pack"
                for name in ("one", "two")
            ]
            for pack_dir in packs:
                pack_dir.mkdir(parents=True)
                (pack_dir / "pack-abc.pack").write_bytes(b"same pack bytes\n" * 1024)
            manifest = Path(tmp) / "pack-manifest.json"
            receipt = Path(tmp) / "pack-receipt.json"
            planned = self.cli(
                "deduplicate-packs",
                "--root",
                str(root),
                "--manifest",
                str(manifest),
            )
            self.assertEqual(json.loads(planned.stdout)["entry_count"], 1)
            applied = self.cli(
                "deduplicate-packs",
                "--root",
                str(root),
                "--manifest",
                str(manifest),
                "--apply",
                "--receipt",
                str(receipt),
            )
            self.assertEqual(json.loads(applied.stdout)["rematerialized_count"], 1)
            source = packs[0] / "pack-abc.pack"
            target = packs[1] / "pack-abc.pack"
            self.assertEqual(source.read_bytes(), target.read_bytes())
            target.write_bytes(b"independent\n" + target.read_bytes())
            self.assertNotEqual(source.read_bytes(), target.read_bytes())

    @unittest.skipUnless(sys.platform == "darwin", "clonefile is a macOS facility")
    def test_stable_regular_files_are_rematerialized_and_archives_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "storage"
            files = [root / "runs" / name / "fixture.bin" for name in ("one", "two")]
            old = time.time() - 2 * 86400
            for path in files:
                path.parent.mkdir(parents=True)
                path.write_bytes(b"same regular bytes\n" * 4096)
                os.utime(path, (old, old))
                archive = path.with_name("evidence.tar.zst")
                archive.write_bytes(b"same archive bytes\n" * 4096)
                os.utime(archive, (old, old))
            manifest = Path(tmp) / "file-manifest.json"
            receipt = Path(tmp) / "file-receipt.json"
            planned = self.cli(
                "deduplicate-files",
                "--root",
                str(root),
                "--manifest",
                str(manifest),
                "--minimum-size-bytes",
                "1",
                "--minimum-age-hours",
                "24",
            )
            plan = json.loads(planned.stdout)
            self.assertEqual(plan["entry_count"], 1)
            self.assertNotIn("tar.zst", manifest.read_text(encoding="utf-8"))
            applied = self.cli(
                "deduplicate-files",
                "--root",
                str(root),
                "--manifest",
                str(manifest),
                "--apply",
                "--receipt",
                str(receipt),
            )
            self.assertEqual(json.loads(applied.stdout)["rematerialized_count"], 1)
            self.assertEqual(files[0].read_bytes(), files[1].read_bytes())
            files[1].write_bytes(b"independent\n" + files[1].read_bytes())
            self.assertNotEqual(files[0].read_bytes(), files[1].read_bytes())

    def test_file_dedup_refuses_content_changed_after_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "storage"
            files = [root / "runs" / name / "fixture.bin" for name in ("one", "two")]
            old = time.time() - 2 * 86400
            for path in files:
                path.parent.mkdir(parents=True)
                path.write_bytes(b"same regular bytes\n" * 4096)
                os.utime(path, (old, old))
            manifest = Path(tmp) / "file-manifest.json"
            receipt = Path(tmp) / "file-receipt.json"
            self.cli(
                "deduplicate-files",
                "--root",
                str(root),
                "--manifest",
                str(manifest),
                "--minimum-size-bytes",
                "1",
                "--minimum-age-hours",
                "24",
            )
            files[1].write_bytes(b"changed\n")
            completed = self.cli(
                "deduplicate-files",
                "--root",
                str(root),
                "--manifest",
                str(manifest),
                "--apply",
                "--receipt",
                str(receipt),
                check=False,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertFalse(receipt.exists())


if __name__ == "__main__":
    unittest.main()

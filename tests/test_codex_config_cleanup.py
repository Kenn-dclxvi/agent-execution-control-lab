from __future__ import annotations

import json
import stat
import tempfile
import tomllib
import unittest
from pathlib import Path

from layer2.extensions.long_run_storage.codex_config_cleanup import (
    CodexConfigCleanupError,
    maintain_codex_config_for_batch,
    prune_codex_project_config,
)


class CodexConfigCleanupTest(unittest.TestCase):
    def make_receipt(self, root: Path, paths: list[str] | None = None) -> tuple[Path, Path]:
        batch = root / "batch-001"
        compact = batch / "compact"
        compact.mkdir(parents=True)
        receipt = compact / "execution-prune-receipt.json"
        receipt.write_text(
            json.dumps(
                {
                    "schema_version": "the-caption-prompt.execution-prune-receipt/v1",
                    "batch": str(batch),
                    "pruned_paths": paths
                    or ["cycle/layer2/evidence/run-01/workspace"],
                }
            ),
            encoding="utf-8",
        )
        return batch, receipt

    def test_removes_only_exact_receipt_project_and_preserves_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            batch, receipt = self.make_receipt(root)
            target = batch / "cycle/layer2/evidence/run-01/workspace"
            unrelated = root / "other-missing-workspace"
            config = root / "config.toml"
            config.write_text(
                "# keep this comment\n"
                "model = \"gpt-5\"\n\n"
                f'[projects."{target}"]\ntrust_level = "trusted"\n\n'
                f'[projects."{unrelated}"]\ntrust_level = "trusted"\n',
                encoding="utf-8",
            )
            config.chmod(0o600)

            result = prune_codex_project_config(receipt, config)

            parsed = tomllib.loads(config.read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "updated")
            self.assertEqual(result["removed_paths"], [str(target)])
            self.assertNotIn(str(target), parsed["projects"])
            self.assertIn(str(unrelated), parsed["projects"])
            self.assertIn("# keep this comment", config.read_text(encoding="utf-8"))
            self.assertEqual(stat.S_IMODE(config.stat().st_mode), 0o600)

    def test_unchanged_when_target_is_not_registered(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, receipt = self.make_receipt(root)
            config = root / "config.toml"
            original = 'model = "gpt-5"\n'
            config.write_text(original, encoding="utf-8")

            result = prune_codex_project_config(receipt, config)

            self.assertEqual(result["status"], "unchanged")
            self.assertEqual(config.read_text(encoding="utf-8"), original)

    def test_rejects_pruned_path_outside_workspace_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, receipt = self.make_receipt(root, ["../../.codex"])
            config = root / "config.toml"
            config.write_text('model = "gpt-5"\n', encoding="utf-8")

            with self.assertRaisesRegex(CodexConfigCleanupError, "unexpected pruned"):
                prune_codex_project_config(receipt, config)

    def test_rejects_receipt_bound_to_another_batch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, receipt = self.make_receipt(root)
            document = json.loads(receipt.read_text(encoding="utf-8"))
            document["batch"] = str(root / "another-batch")
            receipt.write_text(json.dumps(document), encoding="utf-8")
            config = root / "config.toml"
            config.write_text('model = "gpt-5"\n', encoding="utf-8")

            with self.assertRaisesRegex(CodexConfigCleanupError, "does not match"):
                prune_codex_project_config(receipt, config)

    def test_maintenance_receipt_is_write_once_and_reusable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            batch, _ = self.make_receipt(root)
            config = root / "config.toml"
            config.write_text('model = "gpt-5"\n', encoding="utf-8")

            first = maintain_codex_config_for_batch(batch, config)
            config.write_text('model = "gpt-5.1"\n', encoding="utf-8")
            second = maintain_codex_config_for_batch(batch, config)

            self.assertEqual(second, first)
            maintenance = batch / "compact/codex-project-config-prune-receipt.json"
            self.assertTrue(maintenance.is_file())
            self.assertEqual(json.loads(maintenance.read_text(encoding="utf-8")), first)


if __name__ == "__main__":
    unittest.main()

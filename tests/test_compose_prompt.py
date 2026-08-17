from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.compose_prompt import (
    CompositionError,
    compose,
    composition_sha256,
    verify_bundle_binding,
)
from scripts.evaluation_loop import EvaluationError, validate_prompt_set_identity
from scripts.export_prompt_bundle import BundleError, verify_bundle


ROOT = Path(__file__).resolve().parents[1]
COMPOSITION = ROOT / "prompts/compositions/the-caption-c147-full-agent-r1/composition.json"
C147 = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/files/AGENTS.md.txt"
C147_BUNDLE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"


class ComposePromptTest(unittest.TestCase):
    def test_c147_full_agent_composition_is_byte_identical(self) -> None:
        output, receipt = compose(COMPOSITION)

        self.assertEqual(output, C147.read_bytes())
        self.assertEqual(receipt["output_target"], "AGENTS.md")
        self.assertFalse(receipt["evaluation_eligible"])
        self.assertFalse(receipt["model_visible"])
        self.assertEqual(
            receipt["composition_sha256"],
            "3ca6d870d4069efb3a37e5f39e67681d9d320166be1749fd09c2fb55ad5e1bc7",
        )
        self.assertEqual(receipt["bytes"], 10772)
        self.assertEqual(
            receipt["output_sha256"],
            "46ed3811aa798fec6356cf53feb7403ff15bf75c71a9c76af6d6893b05fb8fc7",
        )
        self.assertEqual(
            receipt["functional_blocks"],
            ["core", "delegation", "validation", "execution"],
        )

    def test_cli_renders_one_self_contained_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/compose_prompt.py"),
                    "render",
                    "--manifest",
                    str(COMPOSITION),
                    "--output",
                    str(target),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            receipt = json.loads(completed.stdout)
            self.assertEqual(target.read_bytes(), C147.read_bytes())
            self.assertEqual(receipt["operation"], "render")
            self.assertFalse((target.parent / "components").exists())

    def test_composition_binds_to_verified_full_bundle_only(self) -> None:
        receipt = verify_bundle_binding(COMPOSITION, C147_BUNDLE)

        self.assertEqual(receipt["binding_status"], "verified")
        self.assertEqual(
            receipt["bundle_prompt_identity"],
            "the-caption-3ce91a4-result-effect-scope-r1",
        )
        self.assertEqual(
            receipt["output_sha256"],
            "46ed3811aa798fec6356cf53feb7403ff15bf75c71a9c76af6d6893b05fb8fc7",
        )

    def test_composition_is_neither_bundle_nor_prompt_set_identity(self) -> None:
        with self.assertRaisesRegex(BundleError, "invalid bundle manifest"):
            verify_bundle(COMPOSITION.parent)
        with self.assertRaisesRegex(EvaluationError, "unsupported key: artifact"):
            validate_prompt_set_identity(json.loads(COMPOSITION.read_text(encoding="utf-8")))
        with self.assertRaisesRegex(EvaluationError, "unsupported key: composition_sha256"):
            validate_prompt_set_identity(
                {
                    "name": "prompt-r1",
                    "bundle_sha256": "0" * 64,
                    "composition_sha256": "1" * 64,
                }
            )

    def test_rejects_component_content_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "composition"
            shutil.copytree(COMPOSITION.parent, copied)
            component = copied / "components/00-header.md"
            component.write_text("changed\n", encoding="utf-8")

            with self.assertRaisesRegex(CompositionError, "component SHA-256 mismatch"):
                compose(copied / "composition.json")

    def test_rejects_bundle_prompt_identity_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "composition"
            shutil.copytree(COMPOSITION.parent, copied)
            path = copied / "composition.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["output_prompt_identity"] = "different-prompt-r1"
            manifest["composition_sha256"] = composition_sha256(manifest)
            path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(CompositionError, "bundle prompt identity mismatch"):
                verify_bundle_binding(path, C147_BUNDLE)

    def test_rejects_component_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / "outside-component.txt"
            manifest = {
                "schema_version": "agent-execution-control.prompt-composition/v1",
                "artifact": {
                    "artifact_role": "composition_source",
                    "evaluation_eligible": False,
                    "model_visible": False,
                },
                "composition_identity": "invalid-r1",
                "source_prompt_identity": "source-r1",
                "output_prompt_identity": "output-r1",
                "output_target": "AGENTS.md",
                "expected_output_sha256": hashlib.sha256(b"x").hexdigest(),
                "functional_blocks": ["core"],
                "components": [
                    {
                        "id": "escape",
                        "functional_block": "core",
                        "path": "../outside-component.txt",
                        "sha256": hashlib.sha256(b"x").hexdigest(),
                    }
                ],
            }
            manifest["composition_sha256"] = composition_sha256(manifest)
            (root / "composition.json").write_text(json.dumps(manifest), encoding="utf-8")
            outside.write_bytes(b"x")
            self.addCleanup(outside.unlink, missing_ok=True)

            with self.assertRaisesRegex(CompositionError, "unsafe component path"):
                compose(root / "composition.json")

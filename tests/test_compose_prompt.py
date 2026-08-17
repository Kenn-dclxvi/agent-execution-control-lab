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
DRAFT_ROOT = ROOT / "prompts/compositions/c147-portable-kernel-draft-r1"
DRAFT_ROOT_ONLY = DRAFT_ROOT / "root-only.composition.json"
DRAFT_FULL_AGENT = DRAFT_ROOT / "full-agent.composition.json"
DRAFT_COVERAGE = DRAFT_ROOT / "primitive-coverage.json"
DRAFT_COST_LEDGER = DRAFT_ROOT / "functional-block-cost-ledger.json"
C147 = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/files/AGENTS.md.txt"
C147_BUNDLE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"


class ComposePromptTest(unittest.TestCase):
    def test_full_agent_cost_ledger_partitions_all_bytes_and_primitives(self) -> None:
        manifest = json.loads((DRAFT_ROOT / "full-agent.candidate.composition.json").read_text())
        coverage = json.loads(DRAFT_COVERAGE.read_text())
        ledger = json.loads(DRAFT_COST_LEDGER.read_text())
        components = {item["id"]: item for item in manifest["components"]}
        statement_counts: dict[str, int] = {}
        entries = coverage["common"] + coverage["variants"]["full-agent"]
        for entry in entries:
            component_id = entry["statement"].split(":", 1)[0]
            statement_counts[component_id] = statement_counts.get(component_id, 0) + 1

        listed_components = [
            component_id for block in ledger["blocks"] for component_id in block["components"]
        ]
        assert sorted(listed_components) == sorted(components)
        assert len(listed_components) == len(set(listed_components))
        assert sum(block["bytes"] for block in ledger["blocks"]) == 10781
        assert sum(block["primitive_count"] for block in ledger["blocks"]) == 81
        assert all(block["removable"] is False for block in ledger["blocks"])
        for block in ledger["blocks"]:
            assert block["bytes"] == sum(
                (DRAFT_ROOT / components[item]["path"]).stat().st_size for item in block["components"]
            )
            assert block["primitive_count"] == sum(
                statement_counts.get(item, 0) for item in block["components"]
            )

    def test_c147_full_agent_composition_is_byte_identical(self) -> None:
        output, receipt = compose(COMPOSITION)

        self.assertEqual(output, C147.read_bytes())
        self.assertEqual(receipt["output_target"], "AGENTS.md")
        self.assertFalse(receipt["evaluation_eligible"])
        self.assertFalse(receipt["model_visible"])
        self.assertEqual(
            receipt["composition_sha256"],
            "b4fa993ca3895c24318b626636c36da89e39201ceb0cb01d3898930a377a4c5b",
        )
        self.assertEqual(receipt["dependency_closure"], "verified")
        self.assertEqual(
            receipt["schema_version"],
            "agent-execution-control.prompt-composition-receipt/v2",
        )
        self.assertIn("actor.worker_admission", receipt["provided_capabilities"])
        self.assertIn("validation.execution", receipt["provided_capabilities"])
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

    def test_v1_composition_remains_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "composition"
            shutil.copytree(COMPOSITION.parent, copied)
            path = copied / "composition.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["schema_version"] = "agent-execution-control.prompt-composition/v1"
            for component in manifest["components"]:
                component.pop("provides")
                component.pop("requires")
            manifest["composition_sha256"] = composition_sha256(manifest)
            path.write_text(json.dumps(manifest), encoding="utf-8")

            output, receipt = compose(path)

            self.assertEqual(output, C147.read_bytes())
            self.assertNotIn("dependency_closure", receipt)
            self.assertEqual(
                receipt["schema_version"],
                "agent-execution-control.prompt-composition-receipt/v1",
            )

    def test_rejects_unresolved_component_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "composition"
            shutil.copytree(COMPOSITION.parent, copied)
            path = copied / "composition.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["components"][0]["requires"] = ["missing.capability"]
            manifest["composition_sha256"] = composition_sha256(manifest)
            path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(CompositionError, "unresolved component capabilities"):
                compose(path)

    def test_rejects_ambiguous_component_provider(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "composition"
            shutil.copytree(COMPOSITION.parent, copied)
            path = copied / "composition.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["components"][1]["provides"].append("document.header")
            manifest["composition_sha256"] = composition_sha256(manifest)
            path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(CompositionError, "is provided by both"):
                compose(path)

    def test_portable_draft_variants_render_one_file_without_prompt_identity(self) -> None:
        root_output, root_receipt = compose(DRAFT_ROOT_ONLY)
        full_output, full_receipt = compose(DRAFT_FULL_AGENT)

        self.assertEqual(len(root_output), 10418)
        self.assertEqual(len(full_output), 10781)
        self.assertEqual(
            root_receipt["output_sha256"],
            "0e625b4c527e8b520c676cee15424ba222576ebc0e29d6f37eeea1ec08166a36",
        )
        self.assertEqual(
            full_receipt["output_sha256"],
            "3d3733a4ec0bb531a5be8eb53922e92fafe37b479b6190d24a8176ae452805e3",
        )
        for receipt in (root_receipt, full_receipt):
            self.assertEqual(receipt["lifecycle_state"], "draft")
            self.assertFalse(receipt["bundle_binding_eligible"])
            self.assertIsNone(receipt["output_prompt_identity"])
            self.assertEqual(receipt["dependency_closure"], "verified")
            self.assertEqual(
                receipt["schema_version"],
                "agent-execution-control.prompt-composition-receipt/v3",
            )
        self.assertIn(b"SINGLE_ACTOR", root_output)
        self.assertNotIn(b"MULTI_ACTOR", root_output)
        self.assertIn(b"MULTI_ACTOR", full_output)
        self.assertNotIn(b"SINGLE_ACTOR", full_output)
        for output in (root_output, full_output):
            text = output.decode("utf-8")
            self.assertIn("資格成立時はその一件を開始する", text)
            self.assertIn("固定inputおよびresult kindへ対応できる場合だけadmitする", text)
            self.assertIn("そのfrontierを`unavailable`にする", text)
            self.assertIn("いずれかがなければ別methodまたは推測で補完せず`unavailable`にする", text)

    def test_portable_draft_cannot_bind_to_bundle(self) -> None:
        with self.assertRaisesRegex(CompositionError, "not eligible for bundle binding"):
            verify_bundle_binding(DRAFT_ROOT_ONLY, C147_BUNDLE)

    def test_portable_draft_coverage_maps_all_81_primitives_per_variant(self) -> None:
        ledger = json.loads(DRAFT_COVERAGE.read_text(encoding="utf-8"))
        expected = {
            *(f"S{i}" for i in range(1, 9)),
            *(f"P{i}" for i in range(1, 6)),
            *(f"T{i}" for i in range(1, 4)),
            *(f"C{i}" for i in range(1, 5)),
            *(f"E{i}" for i in range(1, 16)),
            *(f"O{i}" for i in range(1, 8)),
            *(f"R{i}" for i in range(1, 3)),
            *(f"I{i}" for i in range(1, 3)),
            *(f"D{i}" for i in range(1, 12)),
            *(f"VC{i}" for i in range(1, 10)),
            *(f"VP{i}" for i in range(1, 7)),
            *(f"M{i}" for i in range(1, 7)),
            *(f"RC{i}" for i in range(1, 4)),
        }
        common = ledger["common"]
        self.assertEqual(ledger["required_primitive_count"], 81)

        for variant, manifest_path in {
            "root-only": DRAFT_ROOT_ONLY,
            "full-agent": DRAFT_FULL_AGENT,
        }.items():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            component_paths = {
                entry["id"]: DRAFT_ROOT / entry["path"] for entry in manifest["components"]
            }
            entries = [*common, *ledger["variants"][variant]]
            ids = [entry["id"] for entry in entries]
            self.assertEqual(len(ids), 81)
            self.assertEqual(set(ids), expected)
            self.assertEqual(len(ids), len(set(ids)))
            for entry in entries:
                component_id, raw_ordinal = entry["statement"].split(":", 1)
                self.assertIn(component_id, component_paths)
                statements = [
                    line
                    for line in component_paths[component_id].read_text(encoding="utf-8").splitlines()
                    if line.startswith("- ") or line.startswith("  ")
                ]
                ordinal = int(raw_ordinal)
                self.assertGreaterEqual(ordinal, 1)
                self.assertLessEqual(ordinal, len(statements))

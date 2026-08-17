from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.evaluation_loop import SUPPORTED_QUALITY_RATINGS


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "evaluations/targets"
REGISTRY_README = TARGETS / "README.md"
SCHEMA_VERSION_V1 = "the-caption-prompt.evaluation-target/v1"
SCHEMA_VERSION_V2 = "the-caption-prompt.evaluation-target/v2"
SCHEMA_VERSIONS = {SCHEMA_VERSION_V1, SCHEMA_VERSION_V2}
LAYOUTS = ("legacy_root", "namespaced")
LEGACY_ROOT_TARGET_ID = "the-caption"


def descriptors() -> list[tuple[str, dict]]:
    result = []
    for path in sorted(TARGETS.glob("*/target.json")):
        result.append((path.parent.name, json.loads(path.read_text(encoding="utf-8"))))
    return result


class EvaluationTargetRegistryTest(unittest.TestCase):
    def test_registry_has_at_least_one_descriptor(self) -> None:
        self.assertTrue(descriptors())

    def test_descriptor_identity_and_layout(self) -> None:
        for directory, descriptor in descriptors():
            with self.subTest(target=directory):
                self.assertIn(descriptor["schema_version"], SCHEMA_VERSIONS)
                self.assertEqual(descriptor["target_id"], directory)
                self.assertIn(descriptor["layout"], LAYOUTS)
                self.assertIn(descriptor["visibility"], ("private", "public"))
                self.assertIsInstance(descriptor["third_party_reproducible"], bool)

    def test_legacy_root_layout_is_reserved_for_the_caption(self) -> None:
        for directory, descriptor in descriptors():
            if descriptor["layout"] == "legacy_root":
                self.assertEqual(directory, LEGACY_ROOT_TARGET_ID)

    def test_artifact_roots_exist(self) -> None:
        for directory, descriptor in descriptors():
            for name, relative in descriptor["artifact_roots"].items():
                with self.subTest(target=directory, root=name):
                    self.assertTrue((ROOT / relative).is_dir(), relative)

    def test_namespaced_artifact_roots_are_self_contained(self) -> None:
        for directory, descriptor in descriptors():
            if descriptor["layout"] != "namespaced":
                continue
            prefix = f"evaluations/targets/{directory}/"
            for name, relative in descriptor["artifact_roots"].items():
                with self.subTest(target=directory, root=name):
                    self.assertTrue(relative.startswith(prefix), relative)

    def test_registered_in_readme(self) -> None:
        text = REGISTRY_README.read_text(encoding="utf-8")
        for directory, _ in descriptors():
            with self.subTest(target=directory):
                self.assertIn(f"`{directory}`", text)

    def test_target_specific_modules_exist(self) -> None:
        for directory, descriptor in descriptors():
            for relative in descriptor.get("target_specific_modules", []):
                with self.subTest(target=directory, module=relative):
                    self.assertTrue((ROOT / relative).is_file(), relative)

    def test_current_rating_contract_is_registered(self) -> None:
        supported = {entry["contract_id"] for entry in SUPPORTED_QUALITY_RATINGS}
        for directory, descriptor in descriptors():
            contract = descriptor["current_rating_contract"]
            with self.subTest(target=directory):
                self.assertIn("current_rating_contract", descriptor)
                if contract is None:
                    continue
                roots = descriptor["artifact_roots"]["rating_contracts"]
                contract_path = ROOT / roots / f"{contract}.json"
                self.assertTrue(contract_path.is_file())
                if descriptor["schema_version"] == SCHEMA_VERSION_V1:
                    self.assertIn(contract, supported)
                else:
                    target_contract = json.loads(contract_path.read_text(encoding="utf-8"))
                    self.assertEqual(target_contract["contract_id"], contract)
                    self.assertEqual(
                        target_contract["schema_version"],
                        "portable-instruction-semantic-rating/v1",
                    )
                    self.assertIn(
                        "scripts/portable_semantic_conformance.py",
                        descriptor["target_specific_modules"],
                    )

    def test_null_rating_contract_has_no_registered_results(self) -> None:
        for directory, descriptor in descriptors():
            if descriptor["current_rating_contract"] is not None:
                continue
            results = ROOT / descriptor["artifact_roots"]["published_results"]
            registered = [p for p in results.glob("*.md") if p.name != "README.md"]
            with self.subTest(target=directory):
                self.assertEqual(registered, [], "rating contract未確定のinstanceにresultがある")

    def test_the_caption_refs_match_profiles(self) -> None:
        descriptor = json.loads((TARGETS / LEGACY_ROOT_TARGET_ID / "target.json").read_text(encoding="utf-8"))
        repository = descriptor["target_repository"]
        expected = {
            (repository["repository"], repository["primary_ref"]["commit"], repository["primary_ref"]["tree"])
        }
        observed = set()
        for path in sorted((ROOT / descriptor["artifact_roots"]["profiles"]).glob("*.json")):
            profile = json.loads(path.read_text(encoding="utf-8"))
            ref = profile.get("comparison_conditions", {}).get("target_repository_ref")
            if ref:
                observed.add((ref["repository"], ref["commit"], ref["tree"]))
        self.assertEqual(observed, expected)

    def test_the_caption_case_commits_are_declared(self) -> None:
        descriptor = json.loads((TARGETS / LEGACY_ROOT_TARGET_ID / "target.json").read_text(encoding="utf-8"))
        repository = descriptor["target_repository"]
        declared = {repository["primary_ref"]["commit"]}
        declared.update(entry["commit"] for entry in repository["additional_refs"])
        cases_root = ROOT / descriptor["artifact_roots"]["cases"]
        observed = set()
        for path in sorted(cases_root.rglob("private/case-data.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            identity = data.get("fixture", {}).get("target_identity")
            if identity:
                observed.add(identity["commit"])
        self.assertTrue(observed)
        self.assertTrue(observed <= declared, observed - declared)

    def test_additional_refs_declare_their_users(self) -> None:
        descriptor = json.loads((TARGETS / LEGACY_ROOT_TARGET_ID / "target.json").read_text(encoding="utf-8"))
        cases_root = ROOT / descriptor["artifact_roots"]["cases"]
        for entry in descriptor["target_repository"]["additional_refs"]:
            for used_by in entry["used_by"]:
                with self.subTest(ref=entry["commit"], case=used_by):
                    data = json.loads(
                        (cases_root / used_by / "private/case-data.json").read_text(encoding="utf-8")
                    )
                    self.assertEqual(data["fixture"]["target_identity"]["commit"], entry["commit"])


if __name__ == "__main__":
    unittest.main()

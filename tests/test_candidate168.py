import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C167 = ROOT / "prompts/candidates/the-caption-3ce91a4-prechange-repair-contract-admission-r1"
C168 = ROOT / "prompts/candidates/the-caption-3ce91a4-repair-evidence-burden-r1"
P167 = ROOT / "evaluations/profiles/candidate167-prechange-repair-contract-admission-r1-medium-m24-n5-cli0146.json"
P168 = ROOT / "evaluations/profiles/candidate168-repair-evidence-burden-r1-medium-m24-n5-cli0146.json"


class Candidate168Test(unittest.TestCase):
    def test_bundle_is_direct_child_with_only_root_agents_changed(self) -> None:
        source = verify_bundle(C167)
        candidate = verify_bundle(C168)

        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": source["prompt_identity"],
        })
        self.assertNotEqual(candidate["bundle_sha256"], source["bundle_sha256"])

        source_entries = {entry["target"]: entry for entry in source["files"]}
        candidate_entries = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual(source_entries.keys(), candidate_entries.keys())
        changed = [
            target
            for target in source_entries
            if source_entries[target] != candidate_entries[target]
        ]
        self.assertEqual(changed, ["AGENTS.md"])

    def test_repair_ready_requires_proven_violation_and_postconditions(self) -> None:
        prompt = (C168 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        required = [
            "repair_violation_proven",
            "repair_postconditions_proven",
            "具体的矛盾または必須効果の欠落",
            "repair criterionを越える改善を含まない",
            "意味的に同等な表現を認め",
            "安全そうな表現、以前の表現、一般的best practiceまたは構成可能なpostconditionで不足を補完しない",
            "`ready`は`repair_violation_proven=true ∧ repair_postconditions_proven=true`の場合だけ",
        ]
        for value in required:
            self.assertIn(value, prompt)

        forbidden_case_specific = [
            "TC-RC",
            "SAFE RATIO",
            "T4",
            "T6",
            "implementation-delegation-test-results",
            "positive-contract-output-test-results",
        ]
        for value in forbidden_case_specific:
            self.assertNotIn(value, prompt)

    def test_targeted_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(P167.read_text(encoding="utf-8"))
        candidate = json.loads(P168.read_text(encoding="utf-8"))
        manifest = verify_bundle(C168)

        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])

        source_without_identity = copy.deepcopy(source)
        candidate_without_identity = copy.deepcopy(candidate)
        source_without_identity.pop("profile_id")
        candidate_without_identity.pop("profile_id")
        source_without_identity.pop("prompt_set_identity")
        candidate_without_identity.pop("prompt_set_identity")
        self.assertEqual(candidate_without_identity, source_without_identity)


if __name__ == "__main__":
    unittest.main()

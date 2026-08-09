import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C168 = ROOT / "prompts/candidates/the-caption-3ce91a4-repair-evidence-burden-r1"
C169 = ROOT / "prompts/candidates/the-caption-3ce91a4-repair-decision-evidence-closure-r1"
P168 = ROOT / "evaluations/profiles/candidate168-repair-evidence-burden-r1-medium-m24-n5-cli0146.json"
P169 = ROOT / "evaluations/profiles/candidate169-repair-decision-evidence-closure-r1-medium-m24-n5-cli0146.json"


class Candidate169Test(unittest.TestCase):
    def test_bundle_is_direct_child_with_only_root_agents_changed(self) -> None:
        source = verify_bundle(C168)
        candidate = verify_bundle(C169)

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

    def test_repair_decision_binds_one_proposition_and_aligned_evidence(self) -> None:
        prompt = (C169 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        required = [
            "repair_decision_proposition",
            "repair_decision_proposition_ready",
            "TaskSpecのrequired outcome / repair criterion / stop condition / preservation constraint",
            "非同値な別命題を選ぶとterminal dispositionまたは許されるactionが変わる余地がない",
            "evidence_role := normative_authority | current_artifact | event_observation | provenance",
            "proposition_evidence_admissible",
            "current artifactは自身が記述する事実の真偽を",
            "必要な`event_observation`がmissingまたはforbiddenなら",
            "TaskSpecのrequired outcomeが許可された証拠に合わせた公開表現または主張強度の調整を明示する場合だけ",
            "役割を越えた推論",
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
        source = json.loads(P168.read_text(encoding="utf-8"))
        candidate = json.loads(P169.read_text(encoding="utf-8"))
        manifest = verify_bundle(C169)

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

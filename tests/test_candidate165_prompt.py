from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C164 = ROOT / "prompts/candidates/the-caption-3ce91a4-autonomous-review-admission-r1"
C165 = ROOT / "prompts/candidates/the-caption-3ce91a4-review-result-admission-r1"
CASES = ROOT / "evaluations/cases"
PROFILE = ROOT / "evaluations/profiles/candidate165-review-result-admission-r1-medium-m24-n5-cli0146.json"
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate165-review-result-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
C147_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate147-result-effect-scope-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


def controls(path: Path) -> dict[str, str]:
    return {
        line[2:].split(":", 1)[0]: line
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ":" in line
    }


class Candidate165PromptTest(unittest.TestCase):
    def test_direct_child_changes_only_root_agents(self) -> None:
        source = verify_bundle(C164)
        candidate = verify_bundle(C165)
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": source["prompt_identity"],
        })
        before = {x["target"]: x for x in source["files"]}
        after = {x["target"]: x for x in candidate["files"]}
        self.assertEqual([k for k in before if before[k] != after[k]], ["AGENTS.md"])

    def test_result_admission_is_the_only_control_change(self) -> None:
        before = controls(C164 / "files/AGENTS.md.txt")
        after = controls(C165 / "files/AGENTS.md.txt")
        self.assertNotIn("RESULT_ADMISSION", before)
        for label, line in before.items():
            self.assertEqual(after[label], line)
        rule = after["RESULT_ADMISSION"]
        for text in (
            "criterion_result_admissible :=",
            "current TaskSpec",
            "同じoperation",
            "context_only",
            "terminal / stop condition / recoveryへbindしない",
            "TaskSpecが明示bindしたauthoritative result",
        ):
            self.assertIn(text, rule)

    def test_result_admission_cases_and_profile_are_fixed(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        expected = {
            "TC-HR03-T6-SUMMARY-BIASED",
            "TC-RA02-UNBOUND-OPTIMISTIC-DEFECT",
            "TC-RA03-TASKSPEC-AUTHORITATIVE-STOP",
            "TC-RA04-MISMATCHED-REVIEW-RECEIPT",
        }
        self.assertEqual({x["id"] for x in profile["cases"]}, expected)
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "dc434293678fbc1623f395ff21f5c146d41361b08148584db1b999c62215b452")
        for case_id in expected - {"TC-HR03-T6-SUMMARY-BIASED"}:
            revision = CASES / case_id / "result-admission-r1"
            private = json.loads((revision / "private/case-data.json").read_text(encoding="utf-8"))
            self.assertEqual(private["visibility"], "model_invisible")
            self.assertEqual(
                private["seed"]["artifact"]["raw_sha256"],
                hashlib.sha256((revision / "private/seed.patch").read_bytes()).hexdigest(),
            )

    def test_standard14_profile_changes_only_profile_and_prompt_identity(self) -> None:
        reference = json.loads(C147_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(STANDARD14_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["profile_id"], "candidate165-review-result-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1")
        self.assertEqual(candidate["prompt_set_identity"], {
            "name": "the-caption-3ce91a4-review-result-admission-r1",
            "revision": "r1",
            "bundle_sha256": "dc434293678fbc1623f395ff21f5c146d41361b08148584db1b999c62215b452",
        })
        for key in reference.keys() - {"profile_id", "prompt_set_identity"}:
            self.assertEqual(candidate[key], reference[key], key)


if __name__ == "__main__":
    unittest.main()

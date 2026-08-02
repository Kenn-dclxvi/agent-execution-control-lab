from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C145 = ROOT / "prompts/candidates/the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1"
C147 = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
PROFILE = ROOT / "evaluations/profiles/candidate147-result-effect-scope-v14-reasoning-medium-f01-f02-f03-global-m24-n5-cli0146-r1.json"
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate147-result-effect-scope-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
F06_EXTENSION_PROFILES = {
    n: ROOT / f"evaluations/profiles/candidate147-result-effect-scope-v14-reasoning-medium-f06-global-m24-n{n}-cli0146-r1.json"
    for n in (5, 29, 53, 77, 100)
}
STANDARD14_EXTENSION_PROFILES = {
    n: ROOT / f"evaluations/profiles/candidate147-result-effect-scope-v14-reasoning-medium-standard14-global-m24-n{n}-cli0146-r1.json"
    for n in (29, 53, 77, 100)
}


class Candidate147Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C145)
        candidate = verify_bundle(C147)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_text = (C145 / "files/AGENTS.md.txt").read_text()
        candidate_text = (C147 / "files/AGENTS.md.txt").read_text()
        for term in (
            "required_predicate_state := satisfied | unsatisfied | unobserved",
            "evidence_consumer_ready :=",
            "implementation_bound :=",
            "validation_predicate_ready :=",
        ):
            self.assertIn(term, source_text)
            self.assertIn(term, candidate_text)
        for term in (
            "result_effect_scope :=",
            "decision_boundary(next_operation) :=",
            "resultの停止効果をtask全体または後続全invocationへ伝播させない",
            "TaskSpecで既に許可・固定されたreadを開始identityと同一model stepから発行",
            "共同resultを受領するまでartifact変更とrequired commandだけを発行しない",
        ):
            self.assertIn(term, candidate_text)
            self.assertNotIn(term, source_text)
        for term in (
            "consumer_closure_ready",
            "prechange_evidence_wave_ready",
            "single_change_target_ready",
            "continuation_scope_complete",
            "effect_prechange_state",
            "joint_owner_domain",
            "F01",
            "F02",
            "F03",
        ):
            self.assertNotIn(term, candidate_text)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            [
                "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
                "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND",
                "TC-F03-ATOMIC-CONTEXT-CLEANUP",
            ],
        )
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(profile["prompt_set_identity"]["name"], candidate["prompt_identity"])
        standard14 = json.loads(STANDARD14_PROFILE.read_text())
        self.assertEqual(standard14["iterations"], 5)
        self.assertEqual(standard14["execution"]["max_workers"], 24)
        self.assertEqual(len(standard14["cases"]), 14)
        self.assertEqual(standard14["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(standard14["prompt_set_identity"]["name"], candidate["prompt_identity"])
        for iterations, path in F06_EXTENSION_PROFILES.items():
            extension = json.loads(path.read_text())
            self.assertEqual(extension["iterations"], iterations)
            self.assertEqual(extension["comparison_conditions"]["repetition_condition"]["iterations"], iterations)
            self.assertEqual(extension["execution"]["max_workers"], 24)
            self.assertEqual(
                extension["cases"],
                [{"id": "TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT", "revision": "r2"}],
            )
            self.assertEqual(extension["prompt_set_identity"], standard14["prompt_set_identity"])
            self.assertEqual(
                extension["comparison_conditions"] | {"repetition_condition": {}},
                standard14["comparison_conditions"] | {"repetition_condition": {}},
            )
        for iterations, path in STANDARD14_EXTENSION_PROFILES.items():
            extension = json.loads(path.read_text())
            self.assertEqual(extension["iterations"], iterations)
            self.assertEqual(extension["comparison_conditions"]["repetition_condition"]["iterations"], iterations)
            self.assertEqual(extension["execution"]["max_workers"], 24)
            self.assertEqual(extension["cases"], standard14["cases"])
            self.assertEqual(extension["prompt_set_identity"], standard14["prompt_set_identity"])
            self.assertEqual(
                extension["comparison_conditions"] | {"repetition_condition": {}},
                standard14["comparison_conditions"] | {"repetition_condition": {}},
            )


if __name__ == "__main__":
    unittest.main()

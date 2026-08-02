from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C145 = ROOT / "prompts/candidates/the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1"
C146 = ROOT / "prompts/candidates/the-caption-3ce91a4-consumer-closure-evidence-operation-r1"
PROFILE = ROOT / "evaluations/profiles/candidate146-consumer-closure-evidence-operation-v14-reasoning-medium-f01-f02-f03-global-m24-n5-cli0146-r1.json"


class Candidate146Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C145)
        candidate = verify_bundle(C146)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_text = (C145 / "files/AGENTS.md.txt").read_text()
        candidate_text = (C146 / "files/AGENTS.md.txt").read_text()
        for term in (
            "required_predicate_state := satisfied | unsatisfied | unobserved",
            "evidence_consumer_ready :=",
            "implementation_bound :=",
            "validation_predicate_ready :=",
        ):
            self.assertIn(term, source_text)
            self.assertIn(term, candidate_text)
        for term in (
            "consumer_closure_ready :=",
            "全観測を一つのrepository evidence operationから発行",
            "共同resultを全件受領後に一度だけpredicate stateを更新",
            "開始観測と停止後に禁止される観測を同じclosureへ入れない",
        ):
            self.assertIn(term, candidate_text)
            self.assertNotIn(term, source_text)
        for term in (
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


if __name__ == "__main__":
    unittest.main()

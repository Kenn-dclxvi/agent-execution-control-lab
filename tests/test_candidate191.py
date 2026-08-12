from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-current-prior-review-result-admission-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-explicit-review-operation-applicability-r1"


class Candidate191Test(unittest.TestCase):
    def test_review_operation_requires_explicit_operation_binding(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)

        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(
            candidate["content_relation"]["source_prompt_identity"],
            parent["prompt_identity"],
        )
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(
            candidate["bundle_sha256"],
            "6ff3f31585185ca2f08fd63eb19e4d75156425aecc1e1a6da63753768b24a163",
        )

        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        labels = [
            line.split(":", 1)[0][2:]
            for line in text.splitlines()
            if line.startswith("- ")
        ]
        self.assertEqual(len(labels), 19)
        self.assertEqual(labels, [
            "OPERATION_SPEC", "PRODUCER_BINDING", "PRODUCER_RESULT",
            "OWNER_ROLE", "OPERATION_TERMINAL", "WORKER_CONTEXT", "EVIDENCE_ADMISSION",
            "REVIEW_REQUIREMENT", "REVIEW_EXECUTION_PERMISSION", "REVIEW_PACKET",
            "OBSERVATION_RESULT", "REVIEW_JUDGEMENT", "REVIEW_RESULT_ADMISSION",
            "RESULT_EFFECT", "CHANGE_ADMISSION", "VALIDATION_CLOSURE",
            "VALIDATION_PLAN", "METHOD", "RECOVERY",
        ])

        for required in (
            "explicit_review_operation_fixed :=",
            "reviewを現在subjectへ必要な独立operationとして直接名指し",
            "review_control_applicable := explicit_review_operation_fixed",
            "criterion owner、non_machine_risk、静的確認、独立確認",
            "task identity、worker、producerまたはspawnを成立させない",
            "review operation、packet、producer、spawn、review resultまたはreview admissionを作らず",
            "current_review_result_admissible :=",
            "prior_review_result_admissible :=",
        ):
            self.assertIn(required, text)

        for historical_identity in (
            "C147", "Candidate147", "Candidate176", "Candidate190",
            "Standard14", "TC-F02",
        ):
            self.assertNotIn(historical_identity, text)


if __name__ == "__main__":
    unittest.main()

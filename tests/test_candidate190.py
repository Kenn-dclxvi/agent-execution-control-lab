from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
DIAGNOSTIC_PREDECESSOR = ROOT / "prompts/candidates/the-caption-3ce91a4-self-contained-review-control-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-current-prior-review-result-admission-r1"


class Candidate190Test(unittest.TestCase):
    def test_current_and_prior_review_result_admission_are_separate(self) -> None:
        parent = verify_bundle(PARENT)
        predecessor = verify_bundle(DIAGNOSTIC_PREDECESSOR)
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
            "63d8a79139e2b1e89268455cf997ccf7bd078b37d1bf44e51e0079aa05bfc30c",
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
        self.assertEqual(
            labels,
            [
                "OPERATION_SPEC",
                "PRODUCER_BINDING",
                "PRODUCER_RESULT",
                "OPERATION_TERMINAL",
                "WORKER_CONTEXT",
                "EVIDENCE_ADMISSION",
                "REVIEW_REQUIREMENT",
                "REVIEW_EXECUTION_PERMISSION",
                "REVIEW_PACKET",
                "OBSERVATION_RESULT",
                "REVIEW_JUDGEMENT",
                "REVIEW_RESULT_ADMISSION",
                "RESULT_EFFECT",
                "CHANGE_ADMISSION",
                "VALIDATION_CLOSURE",
                "VALIDATION_PLAN",
                "METHOD",
                "RECOVERY",
            ],
        )

        for required in (
            "current_review_result_admissible :=",
            "review_execution_permission=allowed",
            "prior_review_result_admissible :=",
            "result_use_permission=allowed",
            "result_still_valid=true",
            "current review resultへ別の`result_use_permission`を追加要求せず",
            "保存resultへ新規`review_execution_permission`を要求しない",
            "保存済みprior resultの場合だけresult use permission",
        ):
            self.assertIn(required, text)

        self.assertNotIn(
            "review_result_admissible := operation identityがcurrent reviewまたはTaskSpec許可prior identityと一致",
            text,
        )
        self.assertEqual(text.count("current_review_result_admissible :="), 1)
        self.assertEqual(text.count("prior_review_result_admissible :="), 1)

        for historical_identity in (
            "C147",
            "Candidate147",
            "Candidate176",
            "Candidate189",
            "ADR07",
        ):
            self.assertNotIn(historical_identity, text)

        self.assertEqual(
            predecessor["bundle_sha256"],
            "76153f5b91019aca7a20a449831510cc4528f6477ea17815f9525ef3bfb90cb6",
        )


if __name__ == "__main__":
    unittest.main()

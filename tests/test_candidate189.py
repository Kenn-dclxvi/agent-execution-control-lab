from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
FAILED_PREDECESSOR = ROOT / "prompts/candidates/the-caption-3ce91a4-review-control-responsibility-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-self-contained-review-control-r1"


class Candidate189Test(unittest.TestCase):
    def test_self_contained_review_control_matches_responsibility_design(self) -> None:
        parent = verify_bundle(PARENT)
        failed = verify_bundle(FAILED_PREDECESSOR)
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
            "76153f5b91019aca7a20a449831510cc4528f6477ea17815f9525ef3bfb90cb6",
        )

        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

        text_path = CANDIDATE / "files/AGENTS.md.txt"
        text = text_path.read_text(encoding="utf-8")
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
            "required result kind / result consumer",
            "同一predicateを他producerへ順次・並行に割り当てない",
            "producer terminal後もfalseなら`unavailable`",
            "全worker packetへ",
            "scoped diffまたはresult / required evidence / allowed read / forbidden input",
            "review packetにもこの共通contractを適用",
            "repository evidenceは全lifecycleでdefault deny",
            "implementation_bound :=",
            "review_control_applicable :=",
            "review_requirement := not_applicable",
            "新規実行permissionは保存result利用permissionを兼ねず",
            "observation_integration_allowed :=",
            "counterexample_certificate_ready :=",
            "no_counterexample_certificate_ready :=",
            "review_unavailable_ready :=",
            "review_result_admissible :=",
            "driftが変更とrequired commandだけを禁止するなら",
            "terminal reviewを再開せず",
            "これは`implementation_bound`、明示permission、change predicate、保持constraintおよびvalidation gateを置換せず",
            "review judgement、review result生成、失効result再利用またはterminal review再開を含めない",
        ):
            self.assertIn(required, text)

        for historical_identity in (
            "C147",
            "Candidate147",
            "Candidate176",
            "Candidate177",
            "Candidate188",
            "ADR01",
            "ADR09",
        ):
            self.assertNotIn(historical_identity, text)

        self.assertLess(len(text_path.read_bytes()), len((FAILED_PREDECESSOR / "files/AGENTS.md.txt").read_bytes()))
        self.assertEqual(
            failed["bundle_sha256"],
            "f77250b6b1a26c447627ae6aec965dbd70668947a955449c0955d208e912c253",
        )


if __name__ == "__main__":
    unittest.main()

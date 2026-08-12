from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-explicit-review-operation-applicability-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-consumer-bound-coissuance-r1"


class Candidate192Test(unittest.TestCase):
    def test_dispatch_requires_consumer_and_closes_coissuance(self) -> None:
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
            "1d5770dec7f508c2c6999ed8bff934779efb94f82fb17358da0a63e2098d0f81",
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
        self.assertEqual(len(labels), 20)
        self.assertEqual(labels[7], "DISPATCH_ADMISSION")
        self.assertEqual(labels.count("OWNER_ROLE"), 1)
        self.assertEqual(labels.count("RESULT_EFFECT"), 1)

        for required in (
            "invocation_consumer_ready(i) :=",
            "そのresultを消費するbind済みnonterminal operationがなければ発行せず",
            "開始状態の明示自体、drift可能性、一般的安全確認または許可済みreadの存在をconsumerにしない",
            "dispatch_dependency(i,j) :=",
            "coissuance_ready(S) :=",
            "一model stepで全件発行",
            "operation identity、lifecycle、predicate、consumerまたはresult格納先の分離だけでは",
            "別tool callのまま同一model stepから発行",
            "発行可否と共同発行は`DISPATCH_ADMISSION`だけが所有",
        ):
            self.assertIn(required, text)

        self.assertIn("explicit_review_operation_fixed :=", text)
        self.assertIn("current_review_result_admissible :=", text)
        self.assertIn("prior_review_result_admissible :=", text)

        for historical_identity in (
            "C147", "Candidate147", "Candidate176", "Candidate191",
            "Standard14", "A01",
        ):
            self.assertNotIn(historical_identity, text)


if __name__ == "__main__":
    unittest.main()

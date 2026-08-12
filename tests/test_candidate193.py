from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-explicit-review-operation-applicability-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-frontier-bound-dispatch-transition-r1"


class Candidate193Test(unittest.TestCase):
    def test_frontier_is_bound_to_current_response_and_result_collection(self) -> None:
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
            "a392acd88a127cd297e9d714cf19a4f35c5de8b08aaa21513b6a936e380c9bb8",
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
        self.assertEqual(labels[7], "DISPATCH_TRANSITION")
        self.assertEqual(labels.count("OWNER_ROLE"), 1)
        self.assertEqual(labels.count("RESULT_EFFECT"), 1)

        for required in (
            "dispatch_candidate(i) :=",
            "開始identity・開始状態の明示、drift可能性、安全確認、許可済みreadまたは報告上の有用性だけではconsumerを作らない",
            "dispatch_predecessor(i,j) :=",
            "dispatch_frontier :=",
            "現在responseのtool-call identity集合をfrontier全件と一対一一致",
            "frontierが空なら現在responseからtoolを発行しない",
            "各invocationを個別result contractを持つ別tool callとして全件発行",
            "一部だけを発行してmodelへ戻らず",
            "全invocationのterminal result受領と元identity・consumerへのbindingまでmodel判断を再開しない",
            "cell ID付きnonterminal resultでは同じcell IDへのwait以外を先に発行せず",
            "発行可否、frontier、同一response発行およびresult収集closureは`DISPATCH_TRANSITION`だけが所有",
        ):
            self.assertIn(required, text)

        for retained in (
            "explicit_review_operation_fixed :=",
            "current_review_result_admissible :=",
            "prior_review_result_admissible :=",
            "criterion owner、non_machine_risk",
        ):
            self.assertIn(retained, text)

        for rejected in (
            "coissuance_ready(S) :=",
            "発行可否と共同発行は`DISPATCH_ADMISSION`だけが所有",
        ):
            self.assertNotIn(rejected, text)

        for historical_identity in (
            "C147", "Candidate147", "Candidate191", "Candidate192",
            "Standard14", "A01",
        ):
            self.assertNotIn(historical_identity, text)


if __name__ == "__main__":
    unittest.main()

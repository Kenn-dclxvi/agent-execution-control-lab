from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-control-responsibility-r1"


class Candidate188Test(unittest.TestCase):
    def test_direct_child_reconstructs_review_control_responsibilities(self) -> None:
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
            "f77250b6b1a26c447627ae6aec965dbd70668947a955449c0955d208e912c253",
        )
        self.assertEqual(
            candidate["provenance"]["design_inputs"][:4],
            [
                "docs/review-control-reconstruction-responsibility-design.md",
                "docs/review-control-reconstruction-direction-review.md",
                "docs/review-control-reconstruction-causal-analysis.md",
                "docs/review-control-reconstruction-milestone-plan.md",
            ],
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
                "REVIEW_REQUIREMENT",
                "REVIEW_EXECUTION_PERMISSION",
                "PACKET_FORMATION",
                "OBSERVATION_RESULT",
                "REVIEW_JUDGEMENT",
                "RESULT_ADMISSION",
                "RESULT_EFFECT",
                "CHANGE_TERMINAL",
                "VALIDATION_CLOSURE",
                "VALIDATION_PLAN",
                "METHOD",
                "RECOVERY",
            ],
        )

        for required in (
            "review_control_applicable(subject)",
            "review_requirement := not_applicable if review_control_applicable=false",
            "finite_direct_match(subject)",
            "review_execution_permission := allowed | denied",
            "result_use_permission=allowed",
            "invocation result contract identity",
            "atomのproducerはbind済みreview producer",
            "tool invocationは観測源であってproducerではない",
            "observation_integration_allowed",
            "counterexample_certificate_ready",
            "no_counterexample_certificate_ready",
            "review_unavailable_ready",
            "result_admissible",
            "result_dependency_set",
            "review_execution_permission`は保存result dependencyへ入れない",
            "terminal reviewをdependency変更後に再開せず",
            "subject_change_allowed",
            "subject_change_denied",
        ):
            self.assertIn(required, text)

        for removed_label in (
            "SPEC",
            "PRODUCER",
            "TERMINAL",
            "CONTEXT",
            "EVIDENCE_GATE",
            "OWNER_ROLE",
            "ROOT",
            "INDEPENDENCE",
            "DECISION_BOUNDARY",
        ):
            self.assertNotIn(f"- {removed_label}:", text)


if __name__ == "__main__":
    unittest.main()

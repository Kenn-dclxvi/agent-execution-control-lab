from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs/post-candidate197-c147-minimal-operation-selection-design.md"
DIRECTION_REVIEW = ROOT / "docs/post-candidate197-c147-minimal-operation-selection-direction-review.md"


class PostCandidate197DesignTest(unittest.TestCase):
    def test_design_uses_c147_direct_base_and_no_turn_limit(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        for required in (
            "design_fixed / c147_direct_base",
            "Candidate197の三条項を親または修正元にしない",
            "ターン数、wave数または固定step数を制御へ入れない",
            "current_minimal_set_not_global_shortest",
            "conditional_operation_classes",
            "candidate_not_created",
        ):
            self.assertIn(required, text)

    def test_operation_and_review_selection_are_directly_bound(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        for required in (
            "candidate_operation :=",
            "operation_needed :=",
            "包含関係上の最小集合",
            "required review scope identityが一件以上ある",
            "new_review_needed :=",
            "required_review_scope_identities=[]",
            "reviewerを一件だけ選ぶ",
            "known_cases_23_classified",
            "unclassified_0",
        ):
            self.assertIn(required, text)

        for rejected in (
            "OPERATION_TICKET",
            "PREDECESSOR_EDGE",
            "observation ledger",
            "materialized predispatch adjudication",
            "dispatch frontier",
        ):
            self.assertNotIn(rejected, text)

    def test_direction_review_allows_only_the_fixed_candidate_shape(self) -> None:
        text = DIRECTION_REVIEW.read_text(encoding="utf-8")
        for required in (
            "direction_review_passed",
            "reviewed_states_18",
            "blocking_counterexamples_0",
            "Candidate147",
            "SPEC",
            "DECISION_BOUNDARY",
            "追加labelはreview候補形成の一件だけ",
            "candidate_implementation_allowed",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()

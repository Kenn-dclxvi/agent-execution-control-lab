from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs/post-candidate198-c147-structured-prechange-review-design.md"
DIRECTION_REVIEW = ROOT / "docs/post-candidate198-c147-structured-prechange-review-direction-review.md"
DOCS_INDEX = ROOT / "docs/README.md"


class PostCandidate198StructuredPrechangeDesignTest(unittest.TestCase):
    def test_design_uses_c147_and_separates_start_from_review(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        for required in (
            "design_fixed / c147_direct_base / chronological_boundary_structure",
            "START_BOUNDARY",
            "PRECHANGE_REVIEW",
            "prechange_transition :=",
            "responsibility_separation != dispatch_dependency",
            "review_after_implementation_bound_before_change",
            "current_result_only",
            "ADR9_then_Standard14_only",
            "candidate_not_created",
        ):
            self.assertIn(required, text)

    def test_design_preserves_execution_and_limits_prompt_changes(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        for required in (
            "C147の`DECISION_BOUNDARY`を通常operationの発行順序の正本として逐語維持",
            "`EVIDENCE_GATE`末尾にある`implementation_bound`からartifact変更への無条件遷移",
            "required resultが`HEAD / HEAD^ / HEAD^^`の三値",
            "APPLICABILITY / EXECUTION_PERMISSION / OPERATION_READY / PACKET / OBSERVATION / JUDGEMENT / RESULT_ADMISSION / CHANGE_EFFECT",
            "Candidate198の`selected_operations`、包含最小集合、候補の再選択および`REVIEW_SELECTION`は継承しない",
            "保存済みreview resultの再利用",
        ):
            self.assertIn(required, text)

    def test_direction_review_records_revisions_and_implementation_boundary(self) -> None:
        text = DIRECTION_REVIEW.read_text(encoding="utf-8")
        for required in (
            "direction_review_passed_after_revision",
            "initial_blocking_counterexamples_3",
            "unresolved_blocking_counterexamples_0",
            "reviewed_states_20",
            "candidate_implementation_allowed",
            "C147の12条項逐語保持",
            "`START_BOUNDARY`と`PRECHANGE_REVIEW`の二件",
            "profile_not_created",
            "evaluation_not_started",
        ):
            self.assertIn(required, text)

    def test_docs_index_links_both_frontier_documents(self) -> None:
        text = DOCS_INDEX.read_text(encoding="utf-8")
        self.assertIn(DESIGN.name, text)
        self.assertIn(DIRECTION_REVIEW.name, text)


if __name__ == "__main__":
    unittest.main()

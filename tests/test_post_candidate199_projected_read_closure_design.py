from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs/post-candidate199-c147-projected-review-read-closure-design.md"
DIRECTION_REVIEW = ROOT / "docs/post-candidate199-c147-projected-review-read-closure-direction-review.md"
DOCS_INDEX = ROOT / "docs/README.md"


class PostCandidate199ProjectedReadClosureDesignTest(unittest.TestCase):
    def test_design_uses_c147_and_closes_projected_sources(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        for required in (
            "design_fixed / c147_direct_base",
            "packet_projection_ready",
            "projected_source_closed",
            "reviewer_observation_read_set",
            "reviewer_read_admissible",
            "rootが起動前に先読みしない",
            "一invocationでclosed sourceまたは許可外targetを混ぜない",
            "ADR9_then_Standard14_only",
            "candidate_not_created",
        ):
            self.assertIn(required, text)

    def test_direction_review_resolves_both_blocking_counterexamples(self) -> None:
        text = DIRECTION_REVIEW.read_text(encoding="utf-8")
        for required in (
            "direction_review_passed_after_revision",
            "initial_blocking_counterexamples_2",
            "unresolved_blocking_counterexamples_0",
            "reviewed_states_18",
            "rootによるreviewer observation先読み",
            "一commandへのclosed source混入",
            "candidate_implementation_allowed",
        ):
            self.assertIn(required, text)

    def test_docs_index_links_both_documents(self) -> None:
        text = DOCS_INDEX.read_text(encoding="utf-8")
        self.assertIn(DESIGN.name, text)
        self.assertIn(DIRECTION_REVIEW.name, text)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-mutation-review-effect-boundary-r1"


class Candidate183Test(unittest.TestCase):
    def test_direct_child_adds_only_mutation_review_boundary(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])

        parent_text = (PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        additions = {
            line
            for line in candidate_text.splitlines(keepends=True)
            if line.startswith("- MUTATION_REVIEW_BOUNDARY:")
            or line.startswith("- MUTATION_REVIEW_RESULT:")
        }
        self.assertEqual(len(additions), 2)
        self.assertEqual("".join(line for line in candidate_text.splitlines(keepends=True) if line not in additions), parent_text)

        for required in (
            "fixed_effect_correspondence(m) :=",
            "review_result_effect_scope :=",
            "counterexample_found | no_counterexample_found | unavailable",
            "combination_not_admitted",
            "mutation_review_admitted(m) :=",
            "mutation_emission_ready(invocation) :=",
            "missing / unreadable / non-success / unobserved",
            "METHOD` / `RECOVERY",
        ):
            self.assertIn(required, candidate_text)


if __name__ == "__main__":
    unittest.main()

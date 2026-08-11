from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-admission-totality-r1"


class Candidate185Test(unittest.TestCase):
    def test_direct_child_adds_only_review_admission_totality(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])

        parent_text = (PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        labels = (
            "REVIEW_ADMISSION",
            "FIXED_EFFECT_CORRESPONDENCE",
            "REVIEW_PACKET",
            "JUDGEMENT_RESULT",
            "COEMISSION_JUDGEMENT",
            "JUDGEMENT_EFFECT",
        )
        additions = {
            line
            for line in candidate_text.splitlines(keepends=True)
            if any(line.startswith(f"- {label}:") for label in labels)
        }
        self.assertEqual(len(additions), 6)
        self.assertEqual(
            "".join(line for line in candidate_text.splitlines(keepends=True) if line not in additions),
            parent_text,
        )

        for required in (
            "一変更predicateを意味分解せず一つの`judgement_subject`",
            "target数またはrelationの存在は式を変えず",
            "fixed_effect_correspondence_state := matched | unmatched | unbound",
            "review_requirement := not_required if state=matched else required",
            "design_relies_on_boundary",
            "review_input_state := value(identity,value) | missing(identity) | unreadable(identity) | terminal_failure(identity,result)",
            "`missing / unreadable / terminal failure`はpacketを未完成にせず",
            "manifestのexpected readable stateとsuccess condition",
            "counterexample_found | no_counterexample_found | unavailable",
            "counterexample_support",
            "no_counterexample_dependency",
            "unavailable_dependency",
            "coemission_set",
            "joint_effect_independent",
            "judgement_result_effect_scope :=",
            "judgement_basis_identity",
            "judgement_result_valid :=",
            "評価case、fixture、oracle、rating、過去finding、旧Candidate、期待terminal、修正案および会話履歴",
        ):
            self.assertIn(required, candidate_text)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-judgement-result-effect-boundary-r1"


class Candidate184Test(unittest.TestCase):
    def test_direct_child_adds_only_judgement_result_effect_boundary(self) -> None:
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
            if line.startswith("- JUDGEMENT_RESULT_EFFECT:")
            or line.startswith("- COEMISSION_ADMISSION:")
            or line.startswith("- REVIEW_EFFECT_SCOPE:")
            or line.startswith("- COMBINATION_JUDGEMENT:")
            or line.startswith("- JUDGEMENT_DEPENDENCY:")
            or line.startswith("- REVIEW_INPUT_BOUNDARY:")
        }
        self.assertEqual(len(additions), 6)
        self.assertEqual(
            "".join(line for line in candidate_text.splitlines(keepends=True) if line not in additions),
            parent_text,
        )

        for required in (
            "authority_fixed_effect=true",
            "counterexample_found | no_counterexample_found | unavailable",
            "counterexample_support",
            "no_counterexample_dependency",
            "unavailable_dependency",
            "coemission_set",
            "joint_effect_independent",
            "joint_admission_ready(i) :=",
            "judgement_basis_identity",
            "judgement_result_valid(r) :=",
            "同じcoemission identityだけ",
            "judgement_result_effect_scope :=",
            "review permission denial",
            "combination_no_counterexample_found | combination_counterexample_found | combination_unavailable",
            "coemission_identity := payload identity",
            "別の選択規則、fallback、正規化または固定範囲外",
            "combination review producerもimplementation choiceを生成したproducerと異なる",
            "class保持result",
            "停止したsubjectまたはcoemission identity",
            "TaskSpecまたは適用中authorityが直接固定済み",
            "評価case、fixture、oracle、rating、過去finding、旧Candidate、期待terminal、修正案および会話履歴",
        ):
            self.assertIn(required, candidate_text)


if __name__ == "__main__":
    unittest.main()

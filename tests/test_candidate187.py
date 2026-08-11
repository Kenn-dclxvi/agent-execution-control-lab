from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-admission-proof-obligation-r1"


class Candidate187Test(unittest.TestCase):
    def test_direct_child_adds_only_review_admission_proof(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)

        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(
            candidate["content_relation"]["source_prompt_identity"],
            parent["prompt_identity"],
        )
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(candidate["bundle_sha256"], "189a7a11615511a3341646e24ecbffb61bb278fc6652c2db492648515d797fbd")
        self.assertEqual(
            candidate["provenance"]["design_inputs"][:3],
            [
                "docs/review-admission-proof-obligation-design.md",
                "evaluations/results/candidate173-review-terminal-proof-obligation-problem-qualification-r1_2026-08-12.md",
                "evaluations/results/candidate173-review-terminal-proof-obligation-problem-qualification-r1-audit.json",
            ],
        )

        parent_text = (PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        additions = {
            line
            for line in candidate_text.splitlines(keepends=True)
            if line.startswith("- REVIEW_ADMISSION_PROOF:")
        }
        self.assertEqual(len(additions), 1)
        self.assertEqual(
            "".join(
                line
                for line in candidate_text.splitlines(keepends=True)
                if line not in additions
            ),
            parent_text,
        )

        clause = next(iter(additions))
        for required in (
            "review_admission_state := not_required | required | denied",
            "全target effect / end state / 保持relation",
            "一般設計判断なしに直接固定する場合だけ`not_required`",
            "`closure_complete` / witness不在 / 形成可能なreview disposition",
            "既存`OWNER_ROLE`に従う独立producer",
            "`delegated_result_ready=true`",
            "artifact変更 / required command / completion判定を発行しない",
            "review operation / packet / producer / invocationを作らず",
            "先行resultまたはroot代行を採用せず",
            "別operation、read-only operationまたはtask全体へ伝播させない",
        ):
            self.assertIn(required, clause)

        for excluded_label in (
            "REVIEW_DECISION_RECORD",
            "REVIEW_ADMISSION_INPUT",
            "REVIEW_INPUT_CLASSIFICATION",
            "REVIEW_PACKET",
            "JUDGEMENT_RESULT",
        ):
            self.assertNotIn(f"- {excluded_label}:", candidate_text)


if __name__ == "__main__":
    unittest.main()

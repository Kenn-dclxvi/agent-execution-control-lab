from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / (
    "prompts/candidates/"
    "the-caption-3ce91a4-natural-language-validation-carrier-closure-r1"
)
CANDIDATE = ROOT / (
    "prompts/candidates/"
    "the-caption-3ce91a4-natural-language-predicate-bound-validation-result-r1"
)


class Candidate270Test(unittest.TestCase):
    def test_candidate269_is_direct_parent_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(
            candidate["content_relation"]["source_prompt_identity"],
            base["prompt_identity"],
        )
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "481a035966f1cc6ad8faba7fd05b07baf357d29e0a75dccc563963878547c439",
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in base["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_only_validation_result_binding_is_replaced(self) -> None:
        base = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        base_before, base_closure = base.split("### VALIDATION_CLOSURE\n", 1)
        base_closure, base_after = base_closure.split("### VALIDATION_PLAN\n", 1)
        candidate_before, candidate_closure = candidate.split("### VALIDATION_CLOSURE\n", 1)
        candidate_closure, candidate_after = candidate_closure.split(
            "### VALIDATION_PLAN\n", 1
        )
        self.assertEqual(candidate_before, base_before)
        self.assertEqual(candidate_after, base_after)
        self.assertNotEqual(candidate_closure, base_closure)
        self.assertIn("発行済みの全result", base_closure)
        self.assertNotIn("発行済みの全result", candidate_closure)
        self.assertIn("対応づけ済みの確定result", candidate_closure)
        self.assertIn("対応する検証と合格条件へ明確に対応づけ", candidate_closure)

    def test_natural_language_and_non_goals_are_preserved(self) -> None:
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        closure = candidate.split("### VALIDATION_CLOSURE\n", 1)[1].split(
            "### VALIDATION_PLAN\n", 1
        )[0]
        self.assertIn("一回の外側実行へ束ねる", closure)
        self.assertIn("個別検証の途中resultはAIへ返さず", closure)
        self.assertIn("各検証を一つのshell commandへ結合してはいけない", closure)
        for forbidden in (
            "Candidate147",
            "max_output_tokens",
            "stdout",
            "stderr",
            ":=",
            "∧",
        ):
            self.assertNotIn(forbidden, closure)


if __name__ == "__main__":
    unittest.main()

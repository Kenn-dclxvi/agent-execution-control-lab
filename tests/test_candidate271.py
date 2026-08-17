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
    "the-caption-3ce91a4-natural-language-validation-ticket-terminal-return-r1"
)


class Candidate271Test(unittest.TestCase):
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
            "368d6e420b08ab1675834a15b828558c7ad4842e7c1d9155a870c1defc72ee89",
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in base["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_only_validation_closure_is_replaced(self) -> None:
        base = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        base_before, base_closure = base.split("### VALIDATION_CLOSURE\n", 1)
        base_closure, base_after = base_closure.split("### VALIDATION_PLAN\n", 1)
        candidate_before, candidate_closure = candidate.split(
            "### VALIDATION_CLOSURE\n", 1
        )
        candidate_closure, candidate_after = candidate_closure.split(
            "### VALIDATION_PLAN\n", 1
        )
        self.assertEqual(candidate_before, base_before)
        self.assertEqual(candidate_after, base_after)
        self.assertNotEqual(candidate_closure, base_closure)

    def test_pre_execution_binding_and_ticket_terminal_return_are_present(self) -> None:
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        closure = candidate.split("### VALIDATION_CLOSURE\n", 1)[1].split(
            "### VALIDATION_PLAN\n", 1
        )[0]
        for required in (
            "開始前に、各検証をその合格条件と実行identityへ対応づけ",
            "実行票に未実行または未完了の検証が残る間は",
            "個別検証のresultをAIへ返す外側invocationを発行してはならない",
            "実行票全体が完了する場合だけ",
            "発行済みであることだけを理由に完了resultへ昇格させない",
            "各検証を一つのshell commandへ結合してはいけない",
        ):
            self.assertIn(required, closure)
        for rejected in (
            "発行済みの全result",
            "対応する検証と合格条件へ明確に対応づけ",
            "Candidate147",
            "max_output_tokens",
            ":=",
            "∧",
        ):
            self.assertNotIn(rejected, closure)


if __name__ == "__main__":
    unittest.main()

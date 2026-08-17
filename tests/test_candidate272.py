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
    "the-caption-3ce91a4-natural-language-issued-result-permission-removal-r1"
)


class Candidate272Test(unittest.TestCase):
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
            "6830ca4b0a48ffa96b6145bcf6f5ac48980cb3b1816878f682a25da2dc79e5f1",
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in base["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_only_issued_result_permission_is_removed(self) -> None:
        base = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        old = (
            "個別検証の途中resultはAIへ返さず、発行済みの全resultをwrapperが終了した時に"
            "一度だけ返す。"
        )
        new = (
            "個別検証の途中resultはAIへ返さず、wrapperが終了した時に一度だけ結果を返す。"
        )
        self.assertEqual(base.count(old), 1)
        self.assertNotIn(new, base)
        self.assertEqual(candidate, base.replace(old, new))

    def test_wrapper_route_is_preserved_without_new_classification(self) -> None:
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        closure = candidate.split("### VALIDATION_CLOSURE\n", 1)[1].split(
            "### VALIDATION_PLAN\n", 1
        )[0]
        for required in (
            "一つの実行票を完了させる一回の外側実行へ束ねる",
            "個別検証の途中resultはAIへ返さず",
            "wrapperが終了した時に一度だけ結果を返す",
            "各検証を一つのshell commandへ結合してはいけない",
        ):
            self.assertIn(required, closure)
        for rejected in (
            "発行済みの全result",
            "対応する検証と合格条件へ明確に対応づけ",
            "実行票全体が完了する場合だけ",
            "完了resultへ昇格",
            "max_output_tokens",
            "Candidate147",
            ":=",
            "∧",
        ):
            self.assertNotIn(rejected, closure)


if __name__ == "__main__":
    unittest.main()

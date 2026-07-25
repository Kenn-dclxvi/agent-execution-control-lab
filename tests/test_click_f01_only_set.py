from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SET = ROOT / "evaluations/targets/click/sets/click-f01-only-r1/README.md"
SET_INDEX = ROOT / "evaluations/targets/click/sets/README.md"
CASES_ROOT = ROOT / "evaluations/targets/click/cases"
CASE_LINK_PATTERN = re.compile(r"\.\./\.\./cases/([A-Z0-9-]+)/(r\d+)/README\.md")


class ClickF01OnlySetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SET.read_text(encoding="utf-8")

    def test_declared_cases_exist_as_revisions(self) -> None:
        declared = set(CASE_LINK_PATTERN.findall(self.text))
        self.assertEqual(declared, {("CLICK-F01-ANSI-SEQUENCE-STRIP", "r1")})
        for case_id, revision in declared:
            with self.subTest(case=case_id, revision=revision):
                case_root = CASES_ROOT / case_id / revision
                self.assertTrue((case_root / "trial-prompt-input.json").is_file())
                self.assertTrue((case_root / "private/case-data.json").is_file())

    def test_set_identity_is_declared(self) -> None:
        self.assertIn("`click-f01-only-r1`", self.text)
        self.assertIn("revision: `r1`", self.text)

    def test_set_is_not_presented_as_the_standard_set(self) -> None:
        self.assertIn("標準setではない", self.text)
        self.assertIn("全体試験完了として扱わない", self.text)

    def test_prompt_set_matches_registered_baseline(self) -> None:
        bundle = json.loads(
            (
                ROOT
                / "evaluations/targets/click/prompts/baselines/click-00e592c-control-free-r1/manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.assertIn(bundle["prompt_identity"], self.text)

    def test_target_commit_matches_registered_pin(self) -> None:
        descriptor = json.loads(
            (ROOT / "evaluations/targets/click/target.json").read_text(encoding="utf-8")
        )
        self.assertIn(descriptor["target_repository"]["primary_ref"]["commit"], self.text)

    def test_m_is_fixed_at_24(self) -> None:
        self.assertIn("`M`は指定がない限り24へ固定する", self.text)

    def test_indexed_in_sets_readme(self) -> None:
        self.assertIn("click-f01-only-r1", SET_INDEX.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

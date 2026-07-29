from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "evaluations/results/candidate81-validation-wrapper-precedence-v13-medium-standard14-continuous-n5-b20_2026-07-29.md"
INDEX = ROOT / "evaluations/results/README.md"


class Candidate81B20ResultTest(unittest.TestCase):
    def test_result_preserves_completion_route_and_compatibility_boundaries(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        for fact in (
            "20 / 20 batch、1,400 / 1,400件",
            "`4 / 1 = 1,399 / 1`",
            "全件がroot-onlyかつsession count 1",
            "`+44,151,677`、`+22.91%`",
            "`-197.698秒`、`-3.77%`",
            "evaluation-set identityは一致しない",
            "mode差によりfixture digest、evaluation-set identity、compatibility keyが変わった",
            "standard14_b20_evaluated / descriptive_comparison_only",
        ):
            self.assertIn(fact, result)
        self.assertIn("Candidate82の`standard14_b20_evaluated / stopped`履歴は変更しない", result)
        self.assertIn("このB20から新しい採用、release、runtime projection、本体反映判断は行わない", result)
        self.assertIn("既存のCandidate81 releaseは別stateで`approved / projected`", result)

    def test_result_is_indexed_without_claiming_compatible_winner(self) -> None:
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn(RESULT.name, index)
        self.assertIn("compatibility keyは一致しない", index)
        self.assertIn("互換comparison、winner、採用判断へ使わない", index)


if __name__ == "__main__":
    unittest.main()

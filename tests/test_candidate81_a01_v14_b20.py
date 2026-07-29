from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / (
    "evaluations/profiles/"
    "candidate81-validation-wrapper-precedence-v14-reasoning-medium-a01-"
    "global-m24-n5-r1.json"
)
RESULT = ROOT / (
    "evaluations/results/"
    "candidate81-validation-wrapper-precedence-v14-medium-a01-continuous-"
    "n5-b20_2026-07-29.md"
)


class Candidate81A01V14B20Test(unittest.TestCase):
    def test_profile_freezes_only_a01_under_rating_v14(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["cases"],
            [{"id": "TC-A01-LATENT-MODE-POLICY", "revision": "r2"}],
        )
        self.assertEqual(
            profile["evaluation_set"],
            {"set_id": "the-caption-a01-terminal-state-r1", "revision": "r1"},
        )
        self.assertEqual(
            profile["comparison_conditions"]["task_spec"]["evaluation_set_id"],
            "the-caption-a01-terminal-state-r1",
        )
        rating = profile["comparison_conditions"]["quality_rating"]
        self.assertEqual(
            rating["contract_id"],
            "outcome-terminal-state-evidence-owner-diagnostic-v14",
        )
        self.assertEqual(
            rating["terminal_state_evidence_schema_version"],
            "the-caption-prompt.terminal-state-evidence/v1",
        )
        self.assertEqual(
            profile["prompt_set_identity"]["name"],
            "the-caption-3ce91a4-validation-wrapper-precedence-r1",
        )

    def test_result_records_complete_append_only_b20(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        for marker in (
            "20 / 20 batch、100 / 100件をvalidかつrateable",
            "公式scoreは100 / 100件が`4`",
            "`outcome_state=awaiting_required_value`",
            "root-only `100 / 100`、child session `0`、child token `0`",
            "excluded attempt / 再試行: `0 / 0`",
            "a01_v14_b20_evaluated / diagnostic_only",
            "v13 B20の再採点または互換比較として扱わない",
            "score `4 / 1 = 99 / 1`",
            "`a01_clarification_disposition_missing`",
            "v13本文分類の偽陰性",
            "2323b82e52e24b8bba06266224a74e0b",
            "883c2f4406e845cb89819136b18cfac6",
        ):
            self.assertIn(marker, result)

    def test_indexes_preserve_scope_boundary(self) -> None:
        for relative in (
            "evaluations/profiles/README.md",
            "evaluations/results/README.md",
            "docs/research-backlog.md",
            "docs/candidate-history.md",
        ):
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn(
                    "candidate81-validation-wrapper-precedence-v14-medium-a01-continuous-n5-b20_2026-07-29.md",
                    text,
                )


if __name__ == "__main__":
    unittest.main()

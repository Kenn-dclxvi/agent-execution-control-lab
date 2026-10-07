from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

from scripts import evaluation_loop
from scripts.standard14_claude_quality_audit import (
    CLAUDE_RATING_CONTRACT_V1,
    CLAUDE_RATING_CONTRACT_V2,
    F05_FALLBACK_FORMS_BY_CONTRACT,
)
from scripts.standard14_quality_audit import f_response_failures
from scripts.quality_audit_policy import MONTHLY_REVIEW_RATING_V14

F05 = "TC-F05-CLARIFY-UNITS-MODE"
ENGLISH = "1. Default: daily or strict?\n2. If strict, should it fall back to the live CSV?"
JAPANESE = "1. 既定はdailyとstrictのどちらですか。\n2. strictの場合、live CSVへのフォールバックを許可しますか。"
MISSING = "1. Default: daily or strict?"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ClaudeF05FallbackFormsTest(unittest.TestCase):
    def test_codex_v14_forms_are_unchanged(self) -> None:
        self.assertEqual(
            f_response_failures(F05, ENGLISH, MONTHLY_REVIEW_RATING_V14),
            ["clarification_missing:live_csv_fallback_policy"],
        )
        self.assertEqual(f_response_failures(F05, JAPANESE, MONTHLY_REVIEW_RATING_V14), [])

    def test_claude_v1_reproduces_earlier_ratings(self) -> None:
        forms = F05_FALLBACK_FORMS_BY_CONTRACT[CLAUDE_RATING_CONTRACT_V1]
        self.assertEqual(
            f_response_failures(F05, ENGLISH, MONTHLY_REVIEW_RATING_V14, forms),
            ["clarification_missing:live_csv_fallback_policy"],
        )

    def test_claude_v2_accepts_english_verb_form(self) -> None:
        forms = F05_FALLBACK_FORMS_BY_CONTRACT[CLAUDE_RATING_CONTRACT_V2]
        self.assertEqual(f_response_failures(F05, ENGLISH, MONTHLY_REVIEW_RATING_V14, forms), [])
        self.assertEqual(f_response_failures(F05, JAPANESE, MONTHLY_REVIEW_RATING_V14, forms), [])
        self.assertEqual(
            f_response_failures(F05, MISSING, MONTHLY_REVIEW_RATING_V14, forms),
            ["clarification_missing:live_csv_fallback_policy"],
        )

    def test_v2_contract_hash_is_registered(self) -> None:
        rating = evaluation_loop.QUALITY_RATING_CLAUDE_COLLECTOR_V2
        path = REPOSITORY_ROOT / "evaluations/rating-contracts" / f"{rating['contract_id']}.json"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), rating["contract_sha256"])
        self.assertIn(rating, evaluation_loop.SUPPORTED_QUALITY_RATINGS)


if __name__ == "__main__":
    unittest.main()

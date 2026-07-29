from __future__ import annotations

import inspect
import unittest

from scripts.quality_audit_policy import (
    MONTHLY_REVIEW_RATING_V10,
    MONTHLY_REVIEW_RATING_V13,
    MONTHLY_REVIEW_RATING_V14,
)
from scripts.targeted_review_quality_audit import (
    response_failures,
    response_rating,
)


MISMATCH_RESPONSE = """
review_findings:
- severity: major
  location: src/app/entrypoints/monthly_main.py:24
  evidence: format_test=args.forceに誤接続され、args.format_testが渡らない。
  impact: --format-testで通常処理へ進み、--forceでformat testへ進む。
finding_count: 1
zero_drift: true
"""


class TargetedReviewQualityAuditTest(unittest.TestCase):
    def test_rating_contract_is_keyword_only_and_has_no_default(self) -> None:
        parameter = inspect.signature(response_failures).parameters[
            "rating_contract_id"
        ]
        self.assertEqual(parameter.kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertIs(parameter.default, inspect.Parameter.empty)

    def test_v13_and_v14_keep_numeric_location_diagnostic_only(self) -> None:
        for contract_id in (MONTHLY_REVIEW_RATING_V13, MONTHLY_REVIEW_RATING_V14):
            with self.subTest(contract_id=contract_id):
                failures = response_failures(
                    MISMATCH_RESPONSE,
                    rating_contract_id=contract_id,
                )
                self.assertEqual(failures, [])
                score, _ = response_rating(
                    failures,
                    rating_contract_id=contract_id,
                )
                self.assertEqual(score, 4)

    def test_v10_history_still_requires_exact_numeric_location(self) -> None:
        failures = response_failures(
            MISMATCH_RESPONSE,
            rating_contract_id=MONTHLY_REVIEW_RATING_V10,
        )
        self.assertEqual(
            failures,
            ["review_location_mismatch:monthly_main.py:25"],
        )
        score, _ = response_rating(
            failures,
            rating_contract_id=MONTHLY_REVIEW_RATING_V10,
        )
        self.assertEqual(score, 3)


if __name__ == "__main__":
    unittest.main()

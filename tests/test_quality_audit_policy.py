from __future__ import annotations

import unittest

from scripts.quality_audit_policy import (
    MONTHLY_REVIEW_RATING_V11,
    MONTHLY_REVIEW_RATING_V12,
    MONTHLY_REVIEW_RATING_V13,
    MONTHLY_REVIEW_RATING_V14,
    QualityAuditPolicyError,
    changed_path_failures,
    command_quality_failures,
    monthly_review_failures,
    monthly_review_location_diagnostic,
    monthly_review_rating,
)


class QualityAuditPolicyTest(unittest.TestCase):
    def test_allows_task_authorized_test_file_without_regrading_allowed_paths(self) -> None:
        self.assertEqual(
            changed_path_failures(
                "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
                [
                    "src/domain/market_units_snapshot.py",
                    "tests/unit/test_market_units_snapshot.py",
                ],
            ),
            [],
        )

    def test_requires_primary_changed_path(self) -> None:
        self.assertEqual(
            changed_path_failures(
                "TC-F03-ATOMIC-CONTEXT-CLEANUP",
                ["tests/unit/test_context_repository.py"],
            ),
            ["required_changed_path_missing:src/infra/context_repository.py"],
        )

    def test_only_task_command_outcomes_become_quality_failures(self) -> None:
        requirements = [
            {"required_tokens": ["git", "diff", "--check"], "status": "successful"},
            {"required_tokens": ["bash", "-n", "run.sh"], "status": "not_attempted"},
            {"required_tokens": ["pytest", "tests"], "status": "failed"},
        ]

        self.assertEqual(
            command_quality_failures(requirements),
            [
                "required_command_not_attempted:bash:-n:run.sh",
                "required_command_failed:pytest:tests",
            ],
        )

    def test_incomplete_measurement_cannot_reach_quality_rating(self) -> None:
        with self.assertRaisesRegex(QualityAuditPolicyError, "measurement-invalid"):
            command_quality_failures(
                [
                    {
                        "required_tokens": ["git", "diff", "--name-only"],
                        "status": "evidence_incomplete",
                    }
                ]
            )

    def test_rates_correct_review_with_one_line_location_mismatch_as_three(self) -> None:
        failures = monthly_review_failures(
            "major finding: monthly_main.py:26 のformat_testでargs.forceが無視される"
        )

        self.assertEqual(failures, ["review_location_mismatch:monthly_main.py:25"])
        self.assertEqual(monthly_review_rating(failures)[0], 3)

    def test_missing_review_finding_is_not_location_only(self) -> None:
        failures = monthly_review_failures("変更はありません")

        self.assertIn("review_response_missing:major", failures)
        self.assertEqual(monthly_review_rating(failures)[0], 1)

    def test_v11_numeric_line_mismatch_is_diagnostic_only(self) -> None:
        response = (
            "major: src/app/entrypoints/monthly_main.py:26で"
            "format_test=args.forceとなり、--format-test (-t)が無視され、"
            "--force (-F)がformat-test経路を有効にする。"
        )

        failures = monthly_review_failures(response, MONTHLY_REVIEW_RATING_V11)

        self.assertEqual(failures, [])
        self.assertIsNone(monthly_review_rating(failures, MONTHLY_REVIEW_RATING_V11))
        self.assertEqual(
            monthly_review_location_diagnostic(response),
            {
                "status": "mismatch",
                "expected": "src/app/entrypoints/monthly_main.py:25",
                "observed": ["src/app/entrypoints/monthly_main.py:26"],
                "affects_quality_score": False,
            },
        )

    def test_v11_numeric_line_absence_is_diagnostic_only(self) -> None:
        response = (
            "major: src/app/entrypoints/monthly_main.pyで"
            "format_test=args.forceとなり、--format-test (-t)が無視され、"
            "--force (-F)がformat-test経路を有効にする。"
        )

        self.assertEqual(
            monthly_review_failures(response, MONTHLY_REVIEW_RATING_V11), []
        )
        self.assertEqual(
            monthly_review_location_diagnostic(response)["status"], "absent"
        )

    def test_v11_missing_cli_impact_remains_a_quality_failure(self) -> None:
        response = (
            "major: src/app/entrypoints/monthly_main.py:25で"
            "format_test=args.forceとなっている。"
        )

        failures = monthly_review_failures(response, MONTHLY_REVIEW_RATING_V11)

        self.assertIn("review_semantic_missing:format_test_option_impact", failures)
        self.assertIn("review_semantic_missing:force_option_impact", failures)
        self.assertEqual(
            monthly_review_rating(failures, MONTHLY_REVIEW_RATING_V11)[0], 2
        )

    def test_v12_accepts_observed_semantic_incorrect_binding_paraphrase(self) -> None:
        response = (
            "major: src/app/entrypoints/monthly_main.py:24で、"
            "--forceがformat-test分岐へ誤接続され、"
            "同時に--format-testの値が渡らなくなっている。"
        )

        self.assertIn(
            "review_semantic_missing:incorrect_binding",
            monthly_review_failures(response, MONTHLY_REVIEW_RATING_V11),
        )
        self.assertEqual(
            monthly_review_failures(response, MONTHLY_REVIEW_RATING_V12), []
        )

    def test_v12_does_not_accept_options_without_incorrect_binding_relation(self) -> None:
        response = (
            "major: src/app/entrypoints/monthly_main.py:25で、"
            "--forceと--format-testは独立して正しく渡される。"
        )

        self.assertIn(
            "review_semantic_missing:incorrect_binding",
            monthly_review_failures(response, MONTHLY_REVIEW_RATING_V12),
        )

    def test_v12_does_not_accept_negated_incorrect_binding_relation(self) -> None:
        response = (
            "major: src/app/entrypoints/monthly_main.py:25で、"
            "--forceは--format-testへ誤接続されていない。"
        )

        self.assertIn(
            "review_semantic_missing:incorrect_binding",
            monthly_review_failures(response, MONTHLY_REVIEW_RATING_V12),
        )

    def test_v13_keeps_v12_monthly_semantic_boundary(self) -> None:
        response = (
            "major: src/app/entrypoints/monthly_main.py:24で、"
            "--forceがformat-test分岐へ誤接続され、"
            "同時に--format-testの値が渡らなくなっている。"
        )

        self.assertEqual(
            monthly_review_failures(response, MONTHLY_REVIEW_RATING_V13),
            [],
        )
        self.assertIsNone(
            monthly_review_rating([], MONTHLY_REVIEW_RATING_V13)
        )

    def test_v14_keeps_v13_monthly_semantic_boundary(self) -> None:
        response = (
            "major: src/app/entrypoints/monthly_main.py:24で、"
            "--forceがformat-test分岐へ誤接続され、"
            "同時に--format-testの値が渡らなくなっている。"
        )

        self.assertEqual(
            monthly_review_failures(response, MONTHLY_REVIEW_RATING_V14),
            [],
        )
        self.assertIsNone(monthly_review_rating([], MONTHLY_REVIEW_RATING_V14))


if __name__ == "__main__":
    unittest.main()

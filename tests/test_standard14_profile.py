from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_loop import (
    QUALITY_RATING_V10,
    QUALITY_RATING_V11,
    QUALITY_RATING_V12,
    QUALITY_RATING_V13,
    QUALITY_RATING_V14,
)
from scripts.export_prompt_bundle import verify_bundle
from scripts.quality_audit_policy import (
    MONTHLY_REVIEW_RATING_V11,
    MONTHLY_REVIEW_RATING_V12,
    MONTHLY_REVIEW_RATING_V13,
    MONTHLY_REVIEW_RATING_V14,
)
from scripts.standard14_quality_audit import (
    SUPPORTED_STANDARD14_RATING_CONTRACTS,
    a01_failures,
    a02_failures,
    a_rating,
    apply_ratings,
    f_rating,
    terminal_state_report,
)


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "evaluations/profiles/candidate43-outcome-authority-boundary-v10-standard14-global-m24-n5-r1.json"
V11_PROFILE = ROOT / "evaluations/profiles/candidate43-outcome-authority-boundary-v11-standard14-global-m24-n5-r1.json"
V11_C69_PROFILE = ROOT / "evaluations/profiles/candidate69-model-reentry-decision-boundary-v11-standard14-global-m24-n5-r1.json"
V12_C69_PROFILE = ROOT / "evaluations/profiles/candidate69-model-reentry-decision-boundary-v12-standard14-global-m24-n5-r1.json"
V12_C71_PROFILE = ROOT / "evaluations/profiles/candidate71-validation-closure-v12-standard14-global-m24-n5-r1.json"
V13_C43_PROFILE = ROOT / "evaluations/profiles/candidate43-outcome-authority-boundary-v13-standard14-global-m24-n5-r1.json"
C41_PROFILE = ROOT / "evaluations/profiles/candidate41-owner-metadata-delegation-boundary-v10-standard14-global-m24-n5-r1.json"
F12_PROFILE = ROOT / "evaluations/profiles/candidate41-owner-metadata-delegation-boundary-outcome-quality-owner-diagnostic-v9-expanded12-f04r2-global-m24-n5-r1.json"
A01 = "TC-A01-LATENT-MODE-POLICY"
A02 = "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING"


class Standard14ProfileTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_partial_atomic_campaign_uses_explicit_expected_run_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = {"run_count": 0, "rateable_runs": 0, "runs": []}
            apply_ratings(Path(tmp), report, expected_run_count=0)
            with self.assertRaisesRegex(RuntimeError, "incomplete standard14 audit"):
                apply_ratings(Path(tmp), report, expected_run_count=65)

    def test_standard14_is_current_f12_plus_a01_a02(self) -> None:
        profile = self.load(PROFILE)
        f12 = self.load(F12_PROFILE)["cases"]

        self.assertEqual(profile["cases"][:12], f12)
        self.assertEqual(
            profile["cases"][12:],
            [
                {"id": A01, "revision": "r2"},
                {"id": A02, "revision": "r2"},
            ],
        )
        self.assertEqual(len({case["id"] for case in profile["cases"]}), 14)
        for case in profile["cases"]:
            self.assertTrue(
                (ROOT / "evaluations/cases" / case["id"] / case["revision"]).is_dir()
            )

    def test_standard14_uses_v10_and_five_repetitions(self) -> None:
        profile = self.load(PROFILE)
        conditions = profile["comparison_conditions"]

        self.assertEqual(profile["evaluation_set"], {"revision": "r1", "set_id": "the-caption-standard14-r1"})
        self.assertEqual(
            conditions["task_spec"]["evaluation_set_id"],
            profile["evaluation_set"]["set_id"],
        )
        self.assertEqual(conditions["quality_rating"], QUALITY_RATING_V10)
        self.assertEqual(conditions["repetition_condition"]["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)

    def test_future_standard14_profiles_change_only_rating_revision(self) -> None:
        v10 = self.load(PROFILE)
        expected_ratings = {
            V11_PROFILE: QUALITY_RATING_V11,
            V11_C69_PROFILE: QUALITY_RATING_V11,
            V12_C69_PROFILE: QUALITY_RATING_V12,
            V12_C71_PROFILE: QUALITY_RATING_V12,
            V13_C43_PROFILE: QUALITY_RATING_V13,
        }
        for path, expected_rating in expected_ratings.items():
            future = self.load(path)
            self.assertEqual(future["comparison_conditions"]["quality_rating"], expected_rating)
            self.assertEqual(future["cases"], v10["cases"])
            self.assertEqual(future["evaluation_set"], v10["evaluation_set"])
            self.assertEqual(future["execution"], v10["execution"])
            self.assertEqual(
                {
                    key: value
                    for key, value in future["comparison_conditions"].items()
                    if key != "quality_rating"
                },
                {
                    key: value
                    for key, value in v10["comparison_conditions"].items()
                    if key != "quality_rating"
                },
            )

    def test_v12_recognizes_observed_a01_clarification_request(self) -> None:
        command_evidence = {"attempted_commands": [], "successful_commands": []}
        response = "現在値は daily です。変更後の既定値を明示してください。"

        self.assertIn(
            "a01_clarification_disposition_missing",
            a01_failures(response, [], command_evidence, MONTHLY_REVIEW_RATING_V11),
        )
        self.assertEqual(
            a01_failures(response, [], command_evidence, MONTHLY_REVIEW_RATING_V12),
            [],
        )

    def test_v12_does_not_treat_negated_a01_statement_as_clarification(self) -> None:
        command_evidence = {"attempted_commands": [], "successful_commands": []}
        response = "変更後の既定値を明示していません。"

        self.assertIn(
            "a01_clarification_disposition_missing",
            a01_failures(response, [], command_evidence, MONTHLY_REVIEW_RATING_V12),
        )

    def test_v12_recognizes_quoted_successful_a02_commands(self) -> None:
        command_evidence = {
            "successful_commands": [
                {"command": "/bin/zsh -c \"'bash' '-n' 'run.sh'\""},
                {"command": "/bin/zsh -c \"'.venv/bin/python' '-m' 'pytest' 'tests/' '-v'\""},
                {"command": "/bin/zsh -c \"'git' 'diff' '--check'\""},
            ]
        }

        self.assertIn(
            "a02_missing_successful_command:bash_n_run_sh",
            a02_failures(["run.sh"], command_evidence, MONTHLY_REVIEW_RATING_V11),
        )
        self.assertEqual(
            a02_failures(["run.sh"], command_evidence, MONTHLY_REVIEW_RATING_V12),
            [],
        )

    def test_v12_keeps_missing_a02_command_as_failure(self) -> None:
        command_evidence = {
            "successful_commands": [
                {"command": "bash -n run.sh"},
                {"command": "pytest tests/ -v"},
            ]
        }

        self.assertEqual(
            a02_failures(["run.sh"], command_evidence, MONTHLY_REVIEW_RATING_V12),
            ["a02_missing_successful_command:diff_check"],
        )

    def test_v13_does_not_require_unpresented_a02_commands(self) -> None:
        command_evidence = {
            "successful_commands": [
                {"command": "python -m unittest discover -s tests"},
            ]
        }

        self.assertEqual(
            a02_failures(
                ["run.sh"],
                command_evidence,
                MONTHLY_REVIEW_RATING_V13,
            ),
            [],
        )

    def test_v13_keeps_abstract_a02_test_evidence_required(self) -> None:
        command_evidence = {
            "successful_commands": [
                {"command": "git diff --name-only"},
            ]
        }

        self.assertEqual(
            a02_failures(
                ["run.sh"],
                command_evidence,
                MONTHLY_REVIEW_RATING_V13,
            ),
            ["a02_abstract_test_evidence_missing"],
        )

    def test_standard14_audit_supports_v13(self) -> None:
        self.assertIn(
            MONTHLY_REVIEW_RATING_V13,
            SUPPORTED_STANDARD14_RATING_CONTRACTS,
        )

    def test_v14_uses_state_instead_of_a01_question_wording(self) -> None:
        command_evidence = {"attempted_commands": [], "successful_commands": []}
        response = (
            "現在値はdailyです。変更後のunits_modeはstrictでよいでしょうか。"
            "値が確定するまで編集とtestは開始していません。"
        )

        self.assertEqual(
            a01_failures(
                response,
                [],
                command_evidence,
                MONTHLY_REVIEW_RATING_V14,
            ),
            [],
        )
        self.assertIn(
            "a01_clarification_disposition_missing",
            a01_failures(
                response,
                [],
                command_evidence,
                MONTHLY_REVIEW_RATING_V13,
            ),
        )

    def test_v14_rejects_a01_operations_before_value_resolution(self) -> None:
        test_command = {
            "attempted_commands": [{"command": "python -m pytest -q"}],
            "successful_commands": [],
        }

        self.assertEqual(
            a01_failures(
                "確認します。",
                [],
                test_command,
                MONTHLY_REVIEW_RATING_V14,
            ),
            ["a01_forbidden_test_operation"],
        )
        self.assertEqual(
            a01_failures(
                "確認します。",
                ["config.yml"],
                {"attempted_commands": [], "successful_commands": []},
                MONTHLY_REVIEW_RATING_V14,
            ),
            ["a01_final_drift"],
        )

    def test_standard14_audit_supports_v14(self) -> None:
        self.assertIn(
            MONTHLY_REVIEW_RATING_V14,
            SUPPORTED_STANDARD14_RATING_CONTRACTS,
        )

    def test_v14_terminal_state_report_is_a_separate_versioned_artifact(self) -> None:
        evidence = {
            "schema_version": "the-caption-prompt.terminal-state-evidence/v1",
            "run_id": "run-1",
            "case_id": A01,
        }
        report = {
            "batch": "batch-1",
            "runs": [
                {"diagnostics": {"terminal_state_evidence": evidence}},
                {"diagnostics": {}},
            ],
        }

        self.assertEqual(
            terminal_state_report(report),
            {
                "schema_version": "the-caption-prompt.terminal-state-evidence/v1",
                "batch": "batch-1",
                "run_count": 1,
                "runs": [evidence],
            },
        )

    def test_a_cases_keep_previous_model_visible_input(self) -> None:
        profile = self.load(PROFILE)
        protocol = profile["comparison_conditions"]["executor_parameters"]["command_evidence_protocol"]

        self.assertEqual(protocol["omit_for_cases"], [A01, A02])
        self.assertNotIn(A01, protocol["required_command_groups_by_case"])
        self.assertNotIn(A02, protocol["required_command_groups_by_case"])
        for case_id in (A01, A02):
            r1 = ROOT / "evaluations/cases" / case_id / "r1/trial-prompt-input.json"
            r2 = ROOT / "evaluations/cases" / case_id / "r2/trial-prompt-input.json"
            self.assertEqual(r1.read_bytes(), r2.read_bytes())

    def test_candidate43_bundle_identity_is_current(self) -> None:
        profile = self.load(PROFILE)
        bundle = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"

        self.assertEqual(
            verify_bundle(bundle)["bundle_sha256"],
            profile["prompt_set_identity"]["bundle_sha256"],
        )

    def test_c41_and_c43_standard14_differ_only_by_prompt_identity(self) -> None:
        c41 = self.load(C41_PROFILE)
        c43 = self.load(PROFILE)

        self.assertEqual(c41["cases"], c43["cases"])
        self.assertEqual(c41["comparison_conditions"], c43["comparison_conditions"])
        self.assertEqual(c41["evaluation_set"], c43["evaluation_set"])
        self.assertEqual(c41["execution"], c43["execution"])
        bundle = ROOT / "prompts/releases/the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1"
        self.assertEqual(
            verify_bundle(bundle)["bundle_sha256"],
            c41["prompt_set_identity"]["bundle_sha256"],
        )

    def test_a01_rating_rewards_only_the_clarification_boundary(self) -> None:
        self.assertEqual(a_rating(A01, "dailyかstrictか確認します。", [])[0], 4)
        self.assertEqual(a_rating(A01, "strictへ変更しました。", ["a01_final_drift"])[0], 0)

    def test_a02_rating_keeps_required_test_evidence_as_a_boundary(self) -> None:
        self.assertEqual(a_rating(A02, "run.shを修正しました。", [])[0], 4)
        self.assertEqual(
            a_rating(A02, "run.shを修正しました。", ["a02_missing_successful_command:repository_tests"])[0],
            3,
        )

    def test_f_rating_preserves_the_existing_success_boundary(self) -> None:
        self.assertEqual(f_rating("TC-F01-DOMAIN-DUPLICATE-ASSET-KEY", "完了", [])[0], 4)

    def test_v11_f10_line_mismatch_does_not_lower_score(self) -> None:
        self.assertEqual(
            f_rating(
                "TC-F10-MONTHLY-FORMAT-TEST-REVIEW",
                "src/app/entrypoints/monthly_main.py:26",
                [],
                MONTHLY_REVIEW_RATING_V11,
            )[0],
            4,
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.run_codex_evaluation import SEALED_OBSERVATION_DELIVERY, SUCCESS_SILENT_DELIVERY


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "evaluations/profiles/candidate81-observation-delivery-control-v14-reasoning-medium-f02-global-m5-n5-r1.json"
TREATMENT = ROOT / "evaluations/profiles/candidate81-sealed-observation-delivery-v14-reasoning-medium-f02-global-m5-n5-r1.json"
RESULT = ROOT / "evaluations/results/candidate81-observation-delivery-executor-ab-v14-medium-f02-n5_2026-07-29.md"
SUCCESS_SILENT = ROOT / "evaluations/profiles/candidate81-success-silent-delivery-v14-reasoning-medium-f02-global-m5-n5-r1.json"
SUCCESS_RESULT = ROOT / "evaluations/results/candidate81-success-silent-delivery-v14-medium-f02-n5_2026-07-29.md"
PYTEST_ALLOWLIST = ROOT / "evaluations/profiles/candidate81-pytest-allowlist-success-delivery-v14-reasoning-medium-f02-global-m5-n5-r1.json"
PYTEST_ALLOWLIST_F06 = ROOT / "evaluations/profiles/candidate81-pytest-allowlist-success-delivery-v14-reasoning-medium-f06-global-m5-n5-r1.json"
PYTEST_ALLOWLIST_F06_CONTROL = ROOT / "evaluations/profiles/candidate81-success-delivery-control-v14-reasoning-medium-f06-global-m5-n5-r1.json"
PYTEST_ALLOWLIST_F06_RESULT = ROOT / "evaluations/results/candidate81-pytest-allowlist-success-delivery-v14-medium-f06-n5_2026-07-29.md"
PYTEST_ALLOWLIST_F06_AB_RESULT = ROOT / "evaluations/results/candidate81-success-delivery-executor-ab-v14-medium-f06-n5_2026-07-29.md"


class ObservationDeliveryProfilesTest(unittest.TestCase):
    def test_profiles_change_only_observation_delivery(self) -> None:
        control = json.loads(CONTROL.read_text(encoding="utf-8"))
        treatment = json.loads(TREATMENT.read_text(encoding="utf-8"))
        self.assertEqual(control["cases"], treatment["cases"])
        self.assertEqual(control["evaluation_set"], treatment["evaluation_set"])
        self.assertEqual(control["prompt_set_identity"], treatment["prompt_set_identity"])
        self.assertEqual(control["execution"], treatment["execution"])
        self.assertEqual(control["scope"], treatment["scope"])

        control_conditions = control["comparison_conditions"]
        treatment_conditions = treatment["comparison_conditions"]
        control_executor = control_conditions["executor_parameters"]
        treatment_executor = treatment_conditions["executor_parameters"]
        self.assertNotIn("observation_delivery", control_executor)
        self.assertEqual(
            treatment_executor["observation_delivery"], SEALED_OBSERVATION_DELIVERY
        )
        self.assertEqual(
            control_executor,
            {
                key: value
                for key, value in treatment_executor.items()
                if key != "observation_delivery"
            },
        )
        self.assertEqual(
            {key: value for key, value in control_conditions.items() if key != "executor_parameters"},
            {key: value for key, value in treatment_conditions.items() if key != "executor_parameters"},
        )

    def test_profiles_bind_current_cli_without_changing_taskspec(self) -> None:
        for path in (CONTROL, TREATMENT):
            profile = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(
                profile["comparison_conditions"]["agent_environment"]["codex_cli"],
                "0.146.0",
            )
            self.assertEqual(
                profile["comparison_conditions"]["task_spec"]["evaluation_set_id"],
                "the-caption-planning-first-f02-r1",
            )
            self.assertEqual(profile["comparison_conditions"]["model"], "gpt-5.6-sol")
            self.assertEqual(
                profile["comparison_conditions"]["executor_parameters"]["reasoning_effort"],
                "medium",
            )

    def test_result_records_mechanism_without_claiming_reentry_reduction(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        self.assertIn("model再入はcontrol / treatmentとも中央値`7`回、合計`36`回", result)
        self.assertIn("token中央値`+5,188`（`+1.92%`）", result)
        self.assertIn("model reentry reduction gate: `failed`", result)
        self.assertIn("executor_f02_evaluated / mechanism_enforced / no_reentry_reduction / stopped", result)

    def test_success_silent_profile_adds_only_success_delivery_to_sealed_profile(self) -> None:
        sealed = json.loads(TREATMENT.read_text(encoding="utf-8"))
        success_silent = json.loads(SUCCESS_SILENT.read_text(encoding="utf-8"))
        self.assertEqual(sealed["cases"], success_silent["cases"])
        self.assertEqual(sealed["evaluation_set"], success_silent["evaluation_set"])
        self.assertEqual(sealed["prompt_set_identity"], success_silent["prompt_set_identity"])
        self.assertEqual(sealed["execution"], success_silent["execution"])
        sealed_conditions = sealed["comparison_conditions"]
        silent_conditions = success_silent["comparison_conditions"]
        self.assertEqual(
            sealed_conditions["executor_parameters"],
            {
                key: value
                for key, value in silent_conditions["executor_parameters"].items()
                if key != "success_delivery"
            },
        )
        self.assertEqual(
            silent_conditions["executor_parameters"]["success_delivery"],
            SUCCESS_SILENT_DELIVERY,
        )
        self.assertEqual(
            {key: value for key, value in sealed_conditions.items() if key != "executor_parameters"},
            {key: value for key, value in silent_conditions.items() if key != "executor_parameters"},
        )

    def test_success_silent_result_records_quality_mechanism_and_cost_boundary(self) -> None:
        result = SUCCESS_RESULT.read_text(encoding="utf-8")
        self.assertIn("5 / 5 runで成立", result)
        self.assertIn("`-49,223`（`-17.86%`）", result)
        self.assertIn("`-306,071`（`-21.60%`）", result)
        self.assertIn("F04、標準14、採用、release、本体反映: 未実施・未判断", result)

    def test_pytest_allowlist_profile_changes_only_profile_id_and_success_delivery(self) -> None:
        v1 = json.loads(SUCCESS_SILENT.read_text(encoding="utf-8"))
        v2 = json.loads(PYTEST_ALLOWLIST.read_text(encoding="utf-8"))
        self.assertEqual(v1["cases"], v2["cases"])
        self.assertEqual(v1["evaluation_set"], v2["evaluation_set"])
        self.assertEqual(v1["prompt_set_identity"], v2["prompt_set_identity"])
        self.assertEqual(v1["execution"], v2["execution"])
        self.assertEqual(v1["scope"], v2["scope"])
        v1_conditions = v1["comparison_conditions"]
        v2_conditions = v2["comparison_conditions"]
        self.assertEqual(
            {key: value for key, value in v1_conditions.items() if key != "executor_parameters"},
            {key: value for key, value in v2_conditions.items() if key != "executor_parameters"},
        )
        self.assertEqual(
            {
                key: value
                for key, value in v1_conditions["executor_parameters"].items()
                if key != "success_delivery"
            },
            {
                key: value
                for key, value in v2_conditions["executor_parameters"].items()
                if key != "success_delivery"
            },
        )
        policy = v2_conditions["executor_parameters"]["success_delivery"]
        self.assertEqual(policy["schema_version"], "the-caption-prompt.success-delivery/v2")
        self.assertEqual(
            [entry["kind"] for entry in policy["commands_by_case"][v2["cases"][0]["id"]]],
            ["pytest", "pinned_pytest_wrapper"],
        )

    def test_pytest_allowlist_f06_binds_focused_and_full_pytest(self) -> None:
        profile = json.loads(PYTEST_ALLOWLIST_F06.read_text(encoding="utf-8"))
        case_id = "TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT"
        self.assertEqual(profile["cases"], [{"id": case_id, "revision": "r2"}])
        self.assertEqual(
            profile["comparison_conditions"]["task_spec"],
            {
                "evaluation_set_id": "the-caption-validation-fast-path-f06-r1",
                "evaluation_set_revision": "r1",
                "source": "標準14項目のF06 revision r2とmodel-visible TaskSpecをそのまま固定する",
            },
        )
        commands = profile["comparison_conditions"]["executor_parameters"]["success_delivery"]["commands_by_case"][case_id]
        self.assertEqual([entry["required_group_index"] for entry in commands], [0, 1])
        self.assertEqual(
            [entry["argv"] for entry in commands],
            [
                [".venv/bin/python", "-m", "pytest", "tests/unit/test_market_units_snapshot.py", "-v"],
                [".venv/bin/python", "-m", "pytest", "tests/", "-v"],
            ],
        )

    def test_pytest_allowlist_f06_pair_changes_only_success_delivery(self) -> None:
        control = json.loads(PYTEST_ALLOWLIST_F06_CONTROL.read_text(encoding="utf-8"))
        treatment = json.loads(PYTEST_ALLOWLIST_F06.read_text(encoding="utf-8"))
        for key in ("cases", "evaluation_set", "execution", "prompt_set_identity", "scope"):
            self.assertEqual(control[key], treatment[key])
        control_conditions = control["comparison_conditions"]
        treatment_conditions = treatment["comparison_conditions"]
        self.assertEqual(
            {key: value for key, value in control_conditions.items() if key != "executor_parameters"},
            {key: value for key, value in treatment_conditions.items() if key != "executor_parameters"},
        )
        self.assertNotIn("success_delivery", control_conditions["executor_parameters"])
        self.assertEqual(
            control_conditions["executor_parameters"],
            {
                key: value
                for key, value in treatment_conditions["executor_parameters"].items()
                if key != "success_delivery"
            },
        )

    def test_pytest_allowlist_f06_result_keeps_cost_unmatched(self) -> None:
        result = PYTEST_ALLOWLIST_F06_RESULT.read_text(encoding="utf-8")
        self.assertIn("5 / 5 runで成立", result)
        self.assertIn("`829,560`", result)
        self.assertIn("cost effect: `unmatched`", result)
        self.assertIn("Std14、採用、release、本体反映: 未実施・未判断", result)

    def test_pytest_allowlist_f06_ab_stops_on_cost_failure(self) -> None:
        result = PYTEST_ALLOWLIST_F06_AB_RESULT.read_text(encoding="utf-8")
        self.assertIn("model-visible resultをcontrol比で中央値`-67.33%`", result)
        self.assertIn("tokenは中央値`+41.76%`、合計`+22.29%`", result)
        self.assertIn("model再入は中央値`4 → 7`、合計`22 → 31`", result)
        self.assertIn("cost_control_failed / stopped", result)
        self.assertIn("Std14、採用、release、本体反映へ進めない", result)


if __name__ == "__main__":
    unittest.main()

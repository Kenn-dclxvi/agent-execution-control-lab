from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.evaluation_loop import (
    QUALITY_RATING_CLICK_V1,
    QUALITY_RATING_CLICK_V10,
    SUPPORTED_QUALITY_RATINGS,
)


ROOT = Path(__file__).resolve().parents[1]
PROFILE = (
    ROOT
    / "evaluations/targets/click/profiles/click-control-free-f01-only-global-m24-n1-r1.json"
)
PROFILE_R2 = (
    ROOT
    / "evaluations/targets/click/profiles/click-control-free-f01-only-global-m24-n1-r2.json"
)
PROFILE_N5 = (
    ROOT
    / "evaluations/targets/click/profiles/click-control-free-f01-only-global-m24-n5-r1.json"
)
PROFILE_INDEX = ROOT / "evaluations/targets/click/profiles/README.md"
DESCRIPTOR = ROOT / "evaluations/targets/click/target.json"
BUNDLE = (
    ROOT
    / "evaluations/targets/click/prompts/baselines/click-00e592c-control-free-r1/manifest.json"
)
CASE_DATA = (
    ROOT
    / "evaluations/targets/click/cases/CLICK-F01-ANSI-SEQUENCE-STRIP/r1/private/case-data.json"
)


class ClickF01ProfileTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.conditions = self.profile["comparison_conditions"]

    def test_schema_and_identity(self) -> None:
        self.assertEqual(self.profile["schema_version"], "the-caption-prompt.evaluation-profile/v3")
        self.assertEqual(
            self.profile["profile_id"], "click-control-free-f01-only-global-m24-n1-r1"
        )
        self.assertEqual(self.profile["profile_id"], PROFILE.stem)

    def test_phase1_a_shape_is_case1_n1_m24(self) -> None:
        self.assertEqual(len(self.profile["cases"]), 1)
        self.assertEqual(self.conditions["repetition_condition"]["iterations"], 1)
        self.assertEqual(self.conditions["executor_parameters"]["max_workers"], 24)
        self.assertEqual(self.profile["execution"]["max_workers"], 24)

    def test_case_matches_existing_revision(self) -> None:
        entry = self.profile["cases"][0]
        case_root = (
            ROOT / "evaluations/targets/click/cases" / entry["id"] / entry["revision"]
        )
        self.assertTrue((case_root / "trial-prompt-input.json").is_file())
        data = json.loads(CASE_DATA.read_text(encoding="utf-8"))
        self.assertEqual(entry["id"], data["case_id"])
        self.assertEqual(entry["revision"], data["case_revision"])

    def test_prompt_set_matches_bundle(self) -> None:
        bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
        identity = self.profile["prompt_set_identity"]
        self.assertEqual(identity["name"], bundle["prompt_identity"])
        self.assertEqual(identity["bundle_sha256"], bundle["bundle_sha256"])

    def test_target_ref_matches_registered_pin(self) -> None:
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        primary = descriptor["target_repository"]["primary_ref"]
        ref = self.conditions["target_repository_ref"]
        self.assertEqual(ref["commit"], primary["commit"])
        self.assertEqual(ref["tree"], primary["tree"])
        self.assertEqual(ref["repository"], descriptor["target_repository"]["repository"])

    def test_quality_rating_matches_registered_contract(self) -> None:
        rating = self.conditions["quality_rating"]
        self.assertIn(rating, SUPPORTED_QUALITY_RATINGS)
        self.assertEqual(rating, QUALITY_RATING_CLICK_V1)
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        self.assertEqual(
            descriptor["current_rating_contract"], QUALITY_RATING_CLICK_V10["contract_id"]
        )

    def test_evaluation_set_matches_defined_set(self) -> None:
        evaluation_set = self.profile["evaluation_set"]
        self.assertEqual(evaluation_set["set_id"], "click-f01-only-r1")
        set_readme = (
            ROOT / "evaluations/targets/click/sets" / evaluation_set["set_id"] / "README.md"
        )
        self.assertTrue(set_readme.is_file())
        task_spec = self.conditions["task_spec"]
        self.assertEqual(task_spec["evaluation_set_id"], evaluation_set["set_id"])
        self.assertEqual(task_spec["evaluation_set_revision"], evaluation_set["revision"])

    def test_runtime_identity_is_recorded_in_case_receipt(self) -> None:
        data = json.loads(CASE_DATA.read_text(encoding="utf-8"))
        self.assertEqual(
            self.conditions["agent_environment"]["runtime_identity_sha256"],
            data["qualification"]["receipt"]["runtime_identity_sha256"],
        )

    def test_gate_commands_declare_pythonpath(self) -> None:
        data = json.loads(CASE_DATA.read_text(encoding="utf-8"))
        for command in data["grader"]["commands"]:
            self.assertTrue(command.startswith("PYTHONPATH=src "), command)
        trial = json.loads(
            (
                ROOT
                / "evaluations/targets/click/cases/CLICK-F01-ANSI-SEQUENCE-STRIP/r1/trial-prompt-input.json"
            ).read_text(encoding="utf-8")
        )
        self.assertIn("PYTHONPATH=src", trial["validation_conditions_and_non_machine_risk"])

    def test_scope_is_undecided(self) -> None:
        self.assertEqual(
            self.profile["scope"],
            {
                "adoption": "not_decided",
                "release": "not_decided",
                "runtime_projection": "not_authorized",
            },
        )

    def test_indexed_with_runtime_identity(self) -> None:
        index = PROFILE_INDEX.read_text(encoding="utf-8")
        self.assertIn(self.profile["profile_id"], index)
        self.assertIn(
            self.conditions["agent_environment"]["runtime_identity_sha256"], index
        )

    def test_r2_adds_required_measurement_contract_without_changing_p1a_scope(self) -> None:
        r1 = json.loads(PROFILE.read_text(encoding="utf-8"))
        r2 = json.loads(PROFILE_R2.read_text(encoding="utf-8"))
        self.assertEqual(r2["profile_id"], PROFILE_R2.stem)
        r1_parameters = r1["comparison_conditions"]["executor_parameters"]
        r2_parameters = r2["comparison_conditions"]["executor_parameters"]
        protocol = r2_parameters.pop("command_evidence_protocol")
        token_accounting = r2_parameters.pop("token_accounting")
        self.assertEqual(r1_parameters, r2_parameters)
        r1["comparison_conditions"]["executor_parameters"] = r1_parameters
        r2["comparison_conditions"]["executor_parameters"] = r2_parameters
        r1.pop("profile_id")
        r2.pop("profile_id")
        self.assertEqual(r1, r2)
        self.assertEqual(
            token_accounting,
            {
                "revision": "v1",
                "scope": "all_agents",
                "source": "codex_rollout_final_usage_by_workspace",
            },
        )
        self.assertEqual(
            protocol["schema_version"],
            "the-caption-prompt.command-evidence-protocol/v1",
        )
        self.assertEqual(
            protocol["required_command_groups_by_case"]["CLICK-F01-ANSI-SEQUENCE-STRIP"],
            [
                [
                    "PYTHONPATH=src .venv/bin/python -m pytest "
                    "tests/test_compat.py tests/test_utils/test_style.py -q"
                ],
                ["PYTHONPATH=src .venv/bin/python -m pytest -q"],
            ],
        )
        self.assertIn(PROFILE_R2.stem, PROFILE_INDEX.read_text(encoding="utf-8"))

    def test_n5_changes_only_profile_identity_and_repetition_count(self) -> None:
        n1 = json.loads(PROFILE_R2.read_text(encoding="utf-8"))
        n5 = json.loads(PROFILE_N5.read_text(encoding="utf-8"))
        self.assertEqual(n5["profile_id"], PROFILE_N5.stem)
        self.assertEqual(
            n1["comparison_conditions"]["repetition_condition"]["iterations"], 1
        )
        self.assertEqual(
            n5["comparison_conditions"]["repetition_condition"]["iterations"], 5
        )
        n1.pop("profile_id")
        n5.pop("profile_id")
        n1["comparison_conditions"]["repetition_condition"]["iterations"] = 5
        self.assertEqual(n1, n5)
        self.assertIn(PROFILE_N5.stem, PROFILE_INDEX.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

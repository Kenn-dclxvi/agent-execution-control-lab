from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "evaluations/targets/click/cases/CLICK-F01-ANSI-SEQUENCE-STRIP/r1"
TRIAL_INPUT = CASE / "trial-prompt-input.json"
SEED_PATCH = CASE / "private/seed.patch"
CASE_DATA = CASE / "private/case-data.json"

TRIAL_INPUT_FIELDS = (
    "target_repository_ref_and_start_identity",
    "task_kind_goal_and_done_condition",
    "target_artifacts_allowed_paths_and_forbidden_changes",
    "validation_conditions_and_non_machine_risk",
    "read_edit_test_commit_push_merge_authorization",
    "constraints_and_required_recovery",
)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ClickF01CaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(CASE_DATA.read_text(encoding="utf-8"))

    def test_case_identity(self) -> None:
        self.assertEqual(self.data["case_id"], "CLICK-F01-ANSI-SEQUENCE-STRIP")
        self.assertEqual(self.data["case_revision"], "r1")
        self.assertEqual(self.data["visibility"], "model_invisible")

    def test_trial_input_has_the_six_fields(self) -> None:
        trial = json.loads(TRIAL_INPUT.read_text(encoding="utf-8"))
        self.assertEqual(tuple(trial.keys()), TRIAL_INPUT_FIELDS)

    def test_recorded_hashes_match_artifacts(self) -> None:
        receipt = self.data["qualification"]["receipt"]
        self.assertEqual(receipt["seed_patch_raw_sha256"], sha256_of(SEED_PATCH))
        self.assertEqual(receipt["trial_prompt_input_raw_sha256"], sha256_of(TRIAL_INPUT))
        self.assertEqual(self.data["seed"]["artifact"]["raw_sha256"], sha256_of(SEED_PATCH))

    def test_target_identity_matches_registered_pin(self) -> None:
        descriptor = json.loads(
            (ROOT / "evaluations/targets/click/target.json").read_text(encoding="utf-8")
        )
        primary = descriptor["target_repository"]["primary_ref"]
        identity = self.data["fixture"]["target_identity"]
        application = self.data["seed"]["application_contract"]
        self.assertEqual(identity["commit"], primary["commit"])
        self.assertEqual(identity["tree"], primary["tree"])
        self.assertEqual(application["target_commit"], primary["commit"])
        self.assertEqual(application["target_tree"], primary["tree"])

    def test_seed_patch_is_a_bare_diff(self) -> None:
        text = SEED_PATCH.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("diff --git "))
        for leaked in ("commit ", "Author:", "Strip all ANSI sequences"):
            self.assertNotIn(leaked, text, "seed patchへcommit headerが混入している")

    def test_seed_touches_only_the_allowed_path(self) -> None:
        paths = {
            entry["path"] for entry in self.data["seed"]["application_contract"]["preimage_files"]
        }
        self.assertEqual(paths, {"src/click/_compat.py"})
        post = {entry["path"] for entry in self.data["seed"]["expected_post_seed_files"]}
        self.assertEqual(post, {"src/click/_compat.py"})

    def test_fixture_identity_is_recorded(self) -> None:
        commit = self.data["seed"]["fixture_materialization"]["commit"]
        receipt = self.data["qualification"]["receipt"]
        self.assertIsNotNone(commit["expected_commit"])
        self.assertIsNotNone(commit["expected_tree"])
        self.assertEqual(commit["expected_commit"], receipt["fixture_head_commit"])
        self.assertEqual(commit["expected_tree"], receipt["fixture_head_tree"])

    def test_model_visible_input_does_not_leak_oracle(self) -> None:
        trial = TRIAL_INPUT.read_text(encoding="utf-8")
        for leaked in (
            "71f2baf",
            "_ansi_re",
            "30 failed",
            "1939 passed",
            self.data["seed"]["artifact"]["raw_sha256"],
            self.data["seed"]["expected_post_seed_files"][0]["git_blob_sha1"],
        ):
            self.assertNotIn(leaked, trial, f"model-visible入力へoracleが漏れている: {leaked}")

    def test_gate_commands_declare_repository_root_cwd(self) -> None:
        trial = json.loads(TRIAL_INPUT.read_text(encoding="utf-8"))
        self.assertIn("repository root", trial["validation_conditions_and_non_machine_risk"])
        self.assertIn("cwd_contract", self.data["grader"])

    def test_qualification_is_not_evaluated(self) -> None:
        self.assertEqual(
            self.data["qualification"]["status"], "fixture_qualified_prompt_not_evaluated"
        )


if __name__ == "__main__":
    unittest.main()

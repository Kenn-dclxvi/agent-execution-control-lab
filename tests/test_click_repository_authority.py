from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
CLICK = ROOT / "evaluations/targets/click"
CASE = CLICK / "cases/CLICK-F10-COMMAND-API-INVENTORY/r2"
NO_AGENTS = CLICK / "prompts/baselines/click-00e592c-no-agents-r1"
AUTHORITY = CLICK / "prompts/candidates/click-00e592c-repository-authority-r1"
C81 = CLICK / "prompts/candidates/click-00e592c-validation-wrapper-precedence-r1"
C81_AUTHORITY = CLICK / "prompts/candidates/click-00e592c-c81-repository-authority-r1"
NO_AGENTS_PROFILE = (
    CLICK
    / "profiles/click-no-agents-reasoning-medium-f10-authority-global-m24-n5-r1.json"
)
AUTHORITY_PROFILE = (
    CLICK
    / "profiles/click-repository-authority-reasoning-medium-f10-authority-global-m24-n5-r1.json"
)
NO_AGENTS_STANDARD14_R2_PROFILE = (
    CLICK
    / "profiles/click-no-agents-reasoning-medium-standard14-r2-global-m24-n5-r1.json"
)
AUTHORITY_STANDARD14_R2_PROFILE = (
    CLICK
    / "profiles/click-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1.json"
)
C81_STANDARD14_R2_PROFILE = (
    CLICK / "profiles/click-c81-reasoning-medium-standard14-r2-global-m24-n5-r1.json"
)
C81_AUTHORITY_STANDARD14_R2_PROFILE = (
    CLICK
    / "profiles/click-c81-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1.json"
)
DESIGN = ROOT / "docs/click-repository-authority-availability-design.md"
RESULT = (
    CLICK
    / "results/click-no-agents-repository-authority-reasoning-medium-f10-authority-n5_2026-07-27.md"
)
STANDARD14_R2_RESULT = (
    CLICK
    / "results/click-no-agents-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md"
)
C81_STANDARD14_R2_RESULT = (
    CLICK
    / "results/click-c81-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md"
)


class ClickRepositoryAuthorityTest(unittest.TestCase):
    def test_case_receipt_binds_the_model_visible_prompt(self) -> None:
        prompt = CASE / "trial-prompt-input.json"
        private = json.loads((CASE / "private/case-data.json").read_text(encoding="utf-8"))
        self.assertEqual(
            hashlib.sha256(prompt.read_bytes()).hexdigest(),
            private["qualification"]["receipt"]["trial_prompt_input_raw_sha256"],
        )
        visible = prompt.read_text(encoding="utf-8")
        self.assertIn("src/AGENTS.md", visible)
        self.assertIn("authority_unavailable", visible)
        self.assertIn("sourceだけから正解を推測せず", visible)

    def test_private_contract_preserves_f10_identity_and_authority_boundary(self) -> None:
        private = json.loads((CASE / "private/case-data.json").read_text(encoding="utf-8"))
        self.assertEqual(private["case_id"], "CLICK-F10-COMMAND-API-INVENTORY")
        self.assertEqual(private["case_revision"], "r2")
        self.assertEqual(private["fixture"]["authority_selectors"], ["AGENTS.md", "src/AGENTS.md"])
        self.assertEqual(
            [item["path"] for item in private["fixture"]["source_files"]],
            ["src/click/core.py", "src/click/decorators.py", "src/click/__init__.py"],
        )
        self.assertIn("does not satisfy C1 or C2", private["grader"]["success_rule"])

    def test_authority_bundle_is_scoped_and_verifiable(self) -> None:
        manifest = verify_bundle(AUTHORITY)
        self.assertEqual(manifest["artifact"]["baseline_identity"], "click-00e592c-no-agents-r1")
        self.assertEqual(
            [item["target"] for item in manifest["files"]],
            ["docs/AGENTS.md", "src/AGENTS.md", "tests/AGENTS.md"],
        )
        self.assertNotIn("AGENTS.md", [item["target"] for item in manifest["files"]])
        src = (AUTHORITY / "files/src/AGENTS.md.txt").read_text(encoding="utf-8")
        for expected in (
            "Command construction API authority",
            "`click.command`",
            "`click.group`",
            "`CommandCollection`",
            "`src/click/__init__.py`",
        ):
            self.assertIn(expected, src)

    def test_profiles_differ_only_by_prompt_identity(self) -> None:
        no_agents = json.loads(NO_AGENTS_PROFILE.read_text(encoding="utf-8"))
        authority = json.loads(AUTHORITY_PROFILE.read_text(encoding="utf-8"))
        for profile, bundle in ((no_agents, NO_AGENTS), (authority, AUTHORITY)):
            manifest = verify_bundle(bundle)
            self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])
            self.assertEqual(profile["prompt_set_identity"]["name"], manifest["prompt_identity"])
            self.assertEqual(profile["cases"], [{"id": "CLICK-F10-COMMAND-API-INVENTORY", "revision": "r2"}])
            self.assertEqual(profile["evaluation_set"]["set_id"], "click-f10-authority-availability-r1")
            self.assertEqual(profile["comparison_conditions"]["executor_parameters"]["reasoning_effort"], "medium")
            self.assertEqual(profile["comparison_conditions"]["repetition_condition"]["iterations"], 5)
            self.assertEqual(profile["execution"]["max_workers"], 24)
        comparable_no_agents = copy.deepcopy(no_agents)
        comparable_authority = copy.deepcopy(authority)
        for profile in (comparable_no_agents, comparable_authority):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(comparable_no_agents, comparable_authority)

    def test_design_audits_all_standard_cases_and_keeps_targeted_scope(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for case in ("F01", "F02", "F03", "F04", "F05", "F05-OS", "F06", "F07", "F07-P", "F08", "F10 r1", "F10-R", "A01", "A02"):
            self.assertIn(f"| {case} |", design)
        self.assertIn("既存`click-standard14-r1`は14判断点の回帰・互換比較として変更しない", design)
        self.assertIn("targeted 1 caseの差をStd14全体", design)

    def test_result_records_compatible_completed_authority_split(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        self.assertIn("b9b7277c39a146d7852752a05bf48270", result)
        self.assertIn("699004d386c64c438bb490ab17992d2f", result)
        self.assertIn("`1 = 5`", result)
        self.assertIn("`4 = 5`", result)
        self.assertIn("`authority_unavailable = 5`", result)
        self.assertIn("`authority_available_inventory = 5`", result)
        self.assertIn("`229d9d93047da4d1691825e8f0b03bf33224305791e616f54c47f87638fb0f46`", result)
        self.assertIn("token中央値 | 64,147 | 216,055 | +151,908 | +236.81%", result)
        self.assertIn("作業量とdone condition", result)

    def test_standard14_r2_profiles_replace_only_f10_revision_and_prompt(self) -> None:
        no_agents = json.loads(NO_AGENTS_STANDARD14_R2_PROFILE.read_text(encoding="utf-8"))
        authority = json.loads(AUTHORITY_STANDARD14_R2_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(no_agents["evaluation_set"], {"set_id": "click-standard14-r2", "revision": "r2"})
        self.assertEqual(len(no_agents["cases"]), 14)
        self.assertEqual(
            next(case for case in no_agents["cases"] if case["id"] == "CLICK-F10-COMMAND-API-INVENTORY")["revision"],
            "r2",
        )
        comparable_no_agents = copy.deepcopy(no_agents)
        comparable_authority = copy.deepcopy(authority)
        for profile in (comparable_no_agents, comparable_authority):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(comparable_no_agents, comparable_authority)
        for profile, bundle in ((no_agents, NO_AGENTS), (authority, AUTHORITY)):
            manifest = verify_bundle(bundle)
            self.assertEqual(profile["prompt_set_identity"]["name"], manifest["prompt_identity"])
            self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])
            self.assertEqual(profile["comparison_conditions"]["executor_parameters"]["reasoning_effort"], "medium")
            self.assertEqual(profile["execution"]["max_workers"], 24)

    def test_standard14_r2_result_records_full_compatible_campaign(self) -> None:
        result = STANDARD14_R2_RESULT.read_text(encoding="utf-8")
        for expected in (
            "7e2761fd9fbd45f38d0264d82a2b78de",
            "bfa5fdf4d1f8405282f87efc289b114f",
            "`1 = 5`, `4 = 65`",
            "`4 = 70`",
            "全140件がvalid・rateable",
            "quality中央値 | 94.643 | 100.000 | +5.357 | +5.66%",
            "all-agent token中央値 | 2,580,528 | 2,724,250 | +143,722 | +5.57%",
            "elapsed中央値 | 1,096.187秒 | 1,139.580秒 | +43.393秒 | +3.96%",
            "互換性を達成した",
        ):
            self.assertIn(expected, result)

    def test_c81_authority_bundle_preserves_both_donors(self) -> None:
        c81 = verify_bundle(C81)
        authority = verify_bundle(AUTHORITY)
        combined = verify_bundle(C81_AUTHORITY)
        self.assertEqual(
            [item["target"] for item in combined["files"]],
            ["AGENTS.md", "docs/AGENTS.md", "src/AGENTS.md", "tests/AGENTS.md"],
        )
        by_target = {item["target"]: item for item in combined["files"]}
        self.assertEqual(by_target["AGENTS.md"], c81["files"][0])
        for item in authority["files"]:
            self.assertEqual(by_target[item["target"]], item)

    def test_c81_standard14_r2_profiles_differ_only_by_prompt_identity(self) -> None:
        c81 = json.loads(C81_STANDARD14_R2_PROFILE.read_text(encoding="utf-8"))
        combined = json.loads(C81_AUTHORITY_STANDARD14_R2_PROFILE.read_text(encoding="utf-8"))
        comparable_c81 = copy.deepcopy(c81)
        comparable_combined = copy.deepcopy(combined)
        for profile in (comparable_c81, comparable_combined):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
            self.assertEqual(profile["evaluation_set"], {"set_id": "click-standard14-r2", "revision": "r2"})
            self.assertEqual(profile["comparison_conditions"]["executor_parameters"]["reasoning_effort"], "medium")
            self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(comparable_c81, comparable_combined)

    def test_c81_standard14_r2_result_records_full_compatible_campaign(self) -> None:
        result = C81_STANDARD14_R2_RESULT.read_text(encoding="utf-8")
        for expected in (
            "2d895cf954db4e5a8f35f08dce6f3362",
            "2c716bf594fb4983b9dd1dd15f67fc12",
            "`1 = 5`, `4 = 65`",
            "`4 = 70`",
            "all-agent token中央値 | 1,874,755 | 2,040,912 | +166,157 | +8.86%",
            "elapsed中央値 | 909.390秒 | 1,014.403秒 | +105.013秒 | +11.55%",
            "-705,773（-27.35%）",
            "-683,338（-25.08%）",
            "C81とsub authorityは共存でき",
        ):
            self.assertIn(expected, result)


if __name__ == "__main__":
    unittest.main()

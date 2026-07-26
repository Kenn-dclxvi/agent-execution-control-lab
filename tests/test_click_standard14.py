from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from scripts.evaluation_loop import QUALITY_RATING_CLICK_V10, SUPPORTED_QUALITY_RATINGS


ROOT = Path(__file__).resolve().parents[1]
CLICK = ROOT / "evaluations/targets/click"
PROFILE = CLICK / "profiles/click-control-free-standard14-global-m24-n5-r1.json"
SET = CLICK / "sets/click-standard14-r1/README.md"
RESULT = CLICK / "results/click-control-free-standard14-n5_2026-07-26.md"


class ClickStandard14Test(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.conditions = self.profile["comparison_conditions"]

    def test_profile_fixes_standard14_shape(self) -> None:
        self.assertEqual(self.profile["profile_id"], PROFILE.stem)
        self.assertEqual(len(self.profile["cases"]), 14)
        self.assertEqual(self.conditions["repetition_condition"]["iterations"], 5)
        self.assertEqual(self.conditions["executor_parameters"]["max_workers"], 24)
        self.assertEqual(self.profile["evaluation_set"], {"set_id": "click-standard14-r1", "revision": "r1"})

    def test_profile_uses_final_case_revisions(self) -> None:
        revisions = {item["id"]: item["revision"] for item in self.profile["cases"]}
        self.assertEqual(revisions["CLICK-F07-CANONICAL-TOX-RUNNER"], "r2")
        self.assertEqual(revisions["CLICK-F07-P-DEPENDENCY-LOCK-PAIR"], "r3")
        self.assertTrue(all(revision == "r1" for case_id, revision in revisions.items() if case_id not in {
            "CLICK-F07-CANONICAL-TOX-RUNNER", "CLICK-F07-P-DEPENDENCY-LOCK-PAIR"
        }))

    def test_all_case_artifacts_exist_and_trial_hashes_match(self) -> None:
        for case in self.profile["cases"]:
            directory = CLICK / "cases" / case["id"] / case["revision"]
            data_path = directory / "private/case-data.json"
            trial_path = directory / "trial-prompt-input.json"
            self.assertTrue((directory / "README.md").is_file())
            self.assertTrue(data_path.is_file())
            self.assertTrue(trial_path.is_file())
            data = json.loads(data_path.read_text(encoding="utf-8"))
            self.assertEqual(data["case_id"], case["id"])
            self.assertEqual(data["case_revision"], case["revision"])
            self.assertEqual(
                hashlib.sha256(trial_path.read_bytes()).hexdigest(),
                data["qualification"]["receipt"]["trial_prompt_input_raw_sha256"],
            )

    def test_rating_runtime_and_bundle_are_fixed(self) -> None:
        self.assertEqual(self.conditions["quality_rating"], QUALITY_RATING_CLICK_V10)
        self.assertIn(QUALITY_RATING_CLICK_V10, SUPPORTED_QUALITY_RATINGS)
        self.assertEqual(
            self.conditions["agent_environment"]["runtime_identity_sha256"],
            "0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952",
        )
        self.assertEqual(self.profile["prompt_set_identity"]["name"], "click-00e592c-control-free-r1")

    def test_required_command_map_covers_all_cases(self) -> None:
        groups = self.conditions["executor_parameters"]["command_evidence_protocol"]["required_command_groups_by_case"]
        self.assertEqual(set(groups), {item["id"] for item in self.profile["cases"]})
        self.assertIn("UV_CACHE_DIR=.uv-cache", groups["CLICK-F07-P-DEPENDENCY-LOCK-PAIR"][0][0])

    def test_set_and_result_record_completed_baseline(self) -> None:
        set_text = SET.read_text(encoding="utf-8")
        result_text = RESULT.read_text(encoding="utf-8")
        self.assertIn("70 / 70", set_text)
        self.assertIn("70 / 70", result_text)
        self.assertIn("2,860,702", result_text)
        self.assertIn("Bundle Bとの比較", result_text)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "evaluations/profiles"
PROFILE_STEMS = (
    "baseline-current-r2",
    "control-free-repository",
    "candidate5-completion-persistence",
    "candidate35-root-control-only",
    "candidate43-outcome-authority-boundary",
)
CANDIDATE71_MEDIUM = (
    PROFILES
    / "candidate71-validation-closure-v13-reasoning-medium-standard14-global-m24-n5-r1.json"
)


class MediumReasoningProfilesTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_profiles_change_only_reasoning_and_profile_identity(self) -> None:
        for stem in PROFILE_STEMS:
            high_path = PROFILES / f"{stem}-v13-standard14-global-m24-n5-r1.json"
            medium_path = (
                PROFILES
                / f"{stem}-v13-reasoning-medium-standard14-global-m24-n5-r1.json"
            )
            high = self.load(high_path)
            medium = self.load(medium_path)
            expected = copy.deepcopy(high)
            expected["comparison_conditions"]["executor_parameters"][
                "reasoning_effort"
            ] = "medium"
            expected["profile_id"] = medium_path.stem
            self.assertEqual(medium, expected)

    def test_medium_profiles_share_candidate71_comparison_conditions(self) -> None:
        expected = self.load(CANDIDATE71_MEDIUM)["comparison_conditions"]

        for stem in PROFILE_STEMS:
            path = (
                PROFILES
                / f"{stem}-v13-reasoning-medium-standard14-global-m24-n5-r1.json"
            )
            self.assertEqual(self.load(path)["comparison_conditions"], expected)


if __name__ == "__main__":
    unittest.main()

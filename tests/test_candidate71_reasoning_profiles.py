from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "evaluations/profiles"
HIGH = PROFILES / "candidate71-validation-closure-v13-standard14-global-m24-n5-r1.json"
LOW = PROFILES / "candidate71-validation-closure-v13-reasoning-low-standard14-global-m24-n5-r1.json"
MEDIUM = PROFILES / "candidate71-validation-closure-v13-reasoning-medium-standard14-global-m24-n5-r1.json"
XHIGH = PROFILES / "candidate71-validation-closure-v13-reasoning-xhigh-standard14-global-m24-n5-r1.json"
MAX = PROFILES / "candidate71-validation-closure-v13-reasoning-max-standard14-global-m24-n5-r1.json"
ULTRA = PROFILES / "candidate71-validation-closure-v13-reasoning-ultra-standard14-global-m24-n5-r1.json"


class Candidate71ReasoningProfilesTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_profiles_change_only_reasoning_and_profile_identity(self) -> None:
        high = self.load(HIGH)

        for path, effort in (
            (LOW, "low"),
            (MEDIUM, "medium"),
            (XHIGH, "xhigh"),
            (MAX, "max"),
            (ULTRA, "ultra"),
        ):
            profile = self.load(path)
            self.assertEqual(
                profile["comparison_conditions"]["executor_parameters"]["reasoning_effort"],
                effort,
            )
            expected = copy.deepcopy(high)
            expected["comparison_conditions"]["executor_parameters"]["reasoning_effort"] = effort
            expected["profile_id"] = path.stem
            self.assertEqual(profile, expected)

    def test_profiles_bind_the_current_candidate71_bundle(self) -> None:
        bundle = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
        identity = verify_bundle(bundle)["bundle_sha256"]

        for path in (LOW, MEDIUM, XHIGH, MAX, ULTRA):
            self.assertEqual(
                self.load(path)["prompt_set_identity"]["bundle_sha256"],
                identity,
            )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from scripts.evaluation_loop import QUALITY_RATING_CLICK_V2, SUPPORTED_QUALITY_RATINGS


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "evaluations/targets/click/profiles/click-control-free-f02-only-global-m24-n3-r1.json"
CONTRACT = ROOT / "evaluations/targets/click/rating-contracts/click-outcome-abstract-condition-preserving-v2.json"


class ClickF02ProfileTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.conditions = self.profile["comparison_conditions"]

    def test_shape_and_identity(self) -> None:
        self.assertEqual(self.profile["profile_id"], PROFILE.stem)
        self.assertEqual(self.profile["cases"], [{"id": "CLICK-F02-STREAM-DEPRECATION-CONTRACT", "revision": "r1"}])
        self.assertEqual(self.conditions["repetition_condition"]["iterations"], 3)
        self.assertEqual(self.profile["execution"]["max_workers"], 24)

    def test_set_and_bundle_are_fixed(self) -> None:
        self.assertEqual(self.profile["evaluation_set"]["set_id"], "click-f02-only-r1")
        self.assertEqual(self.profile["prompt_set_identity"]["name"], "click-00e592c-control-free-r1")

    def test_rating_v2_is_registered_and_hash_bound(self) -> None:
        rating = self.conditions["quality_rating"]
        self.assertEqual(rating, QUALITY_RATING_CLICK_V2)
        self.assertIn(rating, SUPPORTED_QUALITY_RATINGS)
        self.assertEqual(rating["contract_sha256"], hashlib.sha256(CONTRACT.read_bytes()).hexdigest())

    def test_required_commands_match_case(self) -> None:
        groups = self.conditions["executor_parameters"]["command_evidence_protocol"]["required_command_groups_by_case"]
        self.assertEqual(list(groups), ["CLICK-F02-STREAM-DEPRECATION-CONTRACT"])
        self.assertIn("tests/test_deprecations.py tests/test_testing.py", groups["CLICK-F02-STREAM-DEPRECATION-CONTRACT"][0][0])


if __name__ == "__main__":
    unittest.main()

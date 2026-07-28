from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evaluations" / "cases"
PROFILES = ROOT / "evaluations" / "profiles"

MATRIX = {
    "DAILY": {
        "current": "daily",
        "order": ["strict", "live", "daily"],
        "target": "strict",
    },
    "STRICT": {
        "current": "strict",
        "order": ["daily", "strict", "live"],
        "target": "live",
    },
    "LIVE": {
        "current": "live",
        "order": ["live", "daily", "strict"],
        "target": "daily",
    },
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class A01ThreeChoiceVariationTest(unittest.TestCase):
    def test_r1_history_and_r2_correction_are_separate(self) -> None:
        for slug in MATRIX:
            for disposition in ("AMBIGUOUS", "AUTHORITY"):
                case = CASES / f"TC-A01-THREE-CHOICE-{slug}-{disposition}"
                self.assertTrue((case / "r1" / "private" / "case-data.json").is_file())
                self.assertTrue((case / "r2" / "private" / "case-data.json").is_file())

    def test_r2_rotates_current_value_order_and_authority_target(self) -> None:
        for slug, expected in MATRIX.items():
            for disposition in ("AMBIGUOUS", "AUTHORITY"):
                case_id = f"TC-A01-THREE-CHOICE-{slug}-{disposition}"
                revision = CASES / case_id / "r2"
                trial = load_json(revision / "trial-prompt-input.json")
                private = load_json(revision / "private" / "case-data.json")
                patch = (revision / "private" / "seed.patch").read_text(encoding="utf-8")

                self.assertEqual(private["case_id"], case_id)
                self.assertEqual(private["case_revision"], "r2")
                self.assertEqual(
                    private["qualification"]["status"],
                    "fixture_qualified_prompt_not_evaluated",
                )
                order = "、".join(f"`{value}`" for value in expected["order"])
                self.assertIn(order, trial["task_kind_goal_and_done_condition"])
                self.assertIn(
                    f'units_mode: str = "{expected["current"]}"',
                    patch,
                )
                self.assertIn(
                    f'= "{expected["current"]}",',
                    patch,
                )

                if disposition == "AUTHORITY":
                    self.assertIn("src/domain/AGENTS.md", patch)
                    self.assertIn(
                        f"既定`units_mode`は`{expected['target']}`",
                        patch,
                    )
                else:
                    self.assertNotIn("src/domain/AGENTS.md", patch)

    def test_profiles_fix_c81_medium_n5_and_case_revision(self) -> None:
        expected_ids = {
            f"TC-A01-THREE-CHOICE-{slug}-{disposition}"
            for slug in MATRIX
            for disposition in ("AMBIGUOUS", "AUTHORITY")
        }
        for revision in ("r1", "r2"):
            path = PROFILES / (
                "candidate81-validation-wrapper-precedence-v13-reasoning-medium-"
                f"a01-three-choice-variation{'-r2' if revision == 'r2' else ''}-"
                "global-m24-n5-r1.json"
            )
            profile = load_json(path)
            self.assertEqual({case["id"] for case in profile["cases"]}, expected_ids)
            self.assertEqual({case["revision"] for case in profile["cases"]}, {revision})
            self.assertEqual(profile["evaluation_set"]["revision"], revision)
            self.assertEqual(
                profile["comparison_conditions"]["executor_parameters"]["reasoning_effort"],
                "medium",
            )
            self.assertEqual(
                profile["comparison_conditions"]["repetition_condition"]["iterations"],
                5,
            )
            self.assertEqual(profile["execution"]["max_workers"], 24)
            self.assertEqual(
                profile["prompt_set_identity"]["bundle_sha256"],
                "919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220",
            )


if __name__ == "__main__":
    unittest.main()

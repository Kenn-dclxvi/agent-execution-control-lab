from __future__ import annotations

import json
import unittest
from dataclasses import asdict
from pathlib import Path

from scripts.review_terminal_direction_probe import DirectionFacts, adjudicate


ROOT = Path(__file__).resolve().parents[1]
SET = ROOT / "evaluations/sets/review-terminal-proof-obligation-direction-r1"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ReviewTerminalDirectionProbeTest(unittest.TestCase):
    def test_all_six_fixed_conditions_match_private_oracle(self) -> None:
        cases = load_json(SET / "cases.json")
        oracle = load_json(SET / "private/oracle.json")

        self.assertEqual(cases["set_identity"], oracle["set_identity"])
        self.assertEqual(
            [case["condition_id"] for case in cases["cases"]],
            ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"],
        )
        for case in cases["cases"]:
            actual = asdict(adjudicate(DirectionFacts(**case["facts"])))
            self.assertEqual(actual, oracle["expected"][case["condition_id"]])

    def test_q1_and_q2_separate_unrelated_from_applicability_missing(self) -> None:
        cases = {case["condition_id"]: case["facts"] for case in load_json(SET / "cases.json")["cases"]}
        q1 = cases["Q1"]
        q2 = cases["Q2"]

        shared = {
            "finite_direct_match",
            "review_permission",
            "witness_observed",
            "direct_conflict",
            "design_effect_requires_general_change",
            "closure_complete",
            "untrusted_prior_result",
        }
        self.assertTrue(all(q1[key] == q2[key] for key in shared))
        self.assertTrue(q1["witness_applicability_complete"])
        self.assertFalse(q2["witness_applicability_complete"])
        self.assertEqual(adjudicate(DirectionFacts(**q1)).review_disposition, "counterexample_found")
        self.assertEqual(adjudicate(DirectionFacts(**q2)).review_disposition, "unavailable")

    def test_q3_and_q4_differ_only_on_closure(self) -> None:
        cases = {case["condition_id"]: case["facts"] for case in load_json(SET / "cases.json")["cases"]}
        q3 = cases["Q3"]
        q4 = cases["Q4"]

        differences = {key for key in q3 if q3[key] != q4[key]}
        self.assertEqual(differences, {"closure_complete"})
        self.assertEqual(adjudicate(DirectionFacts(**q3)).review_disposition, "unavailable")
        self.assertEqual(adjudicate(DirectionFacts(**q4)).review_disposition, "no_counterexample_found")

    def test_unrelated_missing_and_untrusted_prior_result_do_not_override_route(self) -> None:
        q1 = next(case["facts"] for case in load_json(SET / "cases.json")["cases"] if case["condition_id"] == "Q1")
        q6 = next(case["facts"] for case in load_json(SET / "cases.json")["cases"] if case["condition_id"] == "Q6")

        self.assertTrue(q1["unrelated_missing"])
        self.assertEqual(adjudicate(DirectionFacts(**q1)).terminal, "blocked")
        self.assertTrue(q6["untrusted_prior_result"])
        decision = adjudicate(DirectionFacts(**q6))
        self.assertFalse(decision.review_started)
        self.assertEqual(decision.terminal, "unavailable")


if __name__ == "__main__":
    unittest.main()

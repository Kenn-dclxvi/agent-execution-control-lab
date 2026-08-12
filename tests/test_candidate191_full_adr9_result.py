from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "evaluations/profiles/candidate191-explicit-review-operation-applicability-adr9-r2-medium-m24-n5-cli0146.json"
RESULT = ROOT / "evaluations/results/e599690689294c658b52a6a9e301697f.json"
QUALITY = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-mechanism-audit-r1.json"
RESULT_DOC = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5_2026-08-12.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Candidate191FullAdr9ResultTest(unittest.TestCase):
    def test_profile_is_full_adr9_n5_with_fixed_execution_conditions(self) -> None:
        profile = load(PROFILE)
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            [f"TC-ADR0{index}" for index in range(1, 10)],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"],
            "6ff3f31585185ca2f08fd63eb19e4d75156425aecc1e1a6da63753768b24a163",
        )

    def test_registered_result_is_all_nine_cases_score_four(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["result_id"], "e599690689294c658b52a6a9e301697f")
        self.assertEqual(
            result["result_content_sha256"],
            "2f969876645f5e2f3bfc37acaafab85b68a004dba474e21ec6b1055359d8edac",
        )
        self.assertEqual(result["compatibility"]["coverage"]["iterations"], list(range(1, 6)))
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual({row["quality_score"] for row in result["case_results"]}, {4})
        self.assertEqual(
            Counter(row["case_id"] for row in result["case_results"]),
            {f"TC-ADR0{index}": 5 for index in range(1, 10)},
        )
        self.assertEqual(result["excluded_attempts"], [])

    def test_quality_and_mechanism_gates_pass(self) -> None:
        quality = load(QUALITY)
        mechanism = load(MECHANISM)
        self.assertEqual(quality["status"], "quality_passed")
        self.assertEqual(quality["valid_run_count"], 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 45})
        self.assertEqual(quality["reused_run_count"], 30)
        self.assertEqual(quality["new_run_count"], 15)
        self.assertEqual(mechanism["status"], "mechanism_passed")
        self.assertEqual(mechanism["run_count"], 45)
        self.assertEqual(mechanism["case_count"], 9)
        self.assertEqual(mechanism["review_required_run_count"], 30)
        self.assertEqual(mechanism["review_not_applicable_run_count"], 15)
        self.assertEqual(mechanism["producer_path_match_count"], 45)
        self.assertEqual(mechanism["dependency_match_count"], 45)
        self.assertEqual(mechanism["terminal_match_count"], 45)
        self.assertEqual(mechanism["artifact_boundary_match_count"], 45)
        self.assertEqual(mechanism["required_command_match_count"], 10)
        self.assertEqual(mechanism["command_protocol_violation_count"], 0)
        self.assertEqual(mechanism["genuine_missing_machine_bound_exit_code_count"], 0)
        self.assertTrue(mechanism["mechanism_gate_passed"])

    def test_reader_indexes_and_current_plan_point_to_full_result(self) -> None:
        docs = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        results = (ROOT / "evaluations/results/README.md").read_text(encoding="utf-8")
        candidates = (ROOT / "prompts/candidates/README.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/review-control-reconstruction-milestone-plan.md").read_text(encoding="utf-8")
        profiles = (ROOT / "evaluations/profiles/README.md").read_text(encoding="utf-8")
        profile_shards = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "evaluations/profiles/index").glob("*.md")
        )
        self.assertIn(RESULT_DOC.name, docs)
        self.assertIn(RESULT_DOC.name, results)
        self.assertIn(RESULT_DOC.name, candidates)
        self.assertIn("candidate191_full_M5_passed", plan)
        self.assertIn("candidate191_M7_quality_passed_mechanism_failed_reassessed", plan)
        self.assertIn(PROFILE.name, profiles + profile_shards)


if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
PROFILE = TARGET_ROOT / "profiles/vcc6-p001-p002-codex-cli0146-sol-medium-n5-r1.json"
PLAN = TARGET_ROOT / "plans/vcc6-p001-p002-n5-dispatch-r1.json"
PREFLIGHT = TARGET_ROOT / "plans/vcc6-p001-p002-n5-preflight-r1.json"


def load_runner():
    path = TARGET_ROOT / "runtime/runner_vcc6_paired.py"
    spec = importlib.util.spec_from_file_location("codex_validation_carrier_vcc6_paired_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CodexValidationCarrierVCC6PairedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = load_runner()

    def test_profile_binds_two_prompt_arms_and_compatible_reuse(self) -> None:
        binding = self.runner.validate_profile(
            repository_root=ROOT,
            profile_path=PROFILE,
            target_path=TARGET_ROOT / "target.json",
        )
        self.assertEqual(set(binding["bundles"]), {"P001", "P002"})
        self.assertEqual(binding["profile"]["evaluation_set_ref"]["short_name"], "VCC6")
        self.assertEqual(binding["reuse_result"]["summary"]["valid_results"], 6)
        self.assertEqual(binding["reuse_result"]["summary"]["mechanism_passed"], 6)

    def test_plan_contains_60_logical_and_only_54_fresh_slots(self) -> None:
        plan = self.runner.validate_plan(repository_root=ROOT, plan_path=PLAN)
        self.assertEqual(plan["logical_slot_count"], 60)
        self.assertEqual(plan["reused_slot_count"], 6)
        self.assertEqual(plan["authorized_dispatch_slot_count"], 54)
        self.assertEqual(plan["issued_slot_count"], 0)
        self.assertEqual({slot["arm"] for slot in plan["reused_slots"]}, {"P002"})
        self.assertEqual({slot["iteration"] for slot in plan["reused_slots"]}, {1})
        self.assertEqual(sum(slot["arm"] == "P001" for slot in plan["dispatch_slots"]), 30)
        self.assertEqual(sum(slot["arm"] == "P002" for slot in plan["dispatch_slots"]), 24)

    def test_preflight_proves_prompt_only_difference_before_dispatch(self) -> None:
        receipt, plan = self.runner.validate_preflight(
            repository_root=ROOT,
            receipt_path=PREFLIGHT,
            observed_version="codex-cli 0.146.0",
        )
        self.assertTrue(receipt["prompt_difference_only"])
        self.assertTrue(receipt["dispatch_allowed"])
        self.assertEqual(receipt["authorized_dispatch_slots"], plan["dispatch_slots"])
        self.assertEqual(receipt["issued_slot_count"], 0)

    def test_registered_result_records_quality_and_failed_dual_cost_gate(self) -> None:
        path = TARGET_ROOT / "results/vcc6-p001-p002-n5-comparison-r1.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["logical_slot_count"], 60)
        self.assertEqual(result["arm_summary"]["P002"]["quality_score_distribution"], {"4": 30})
        self.assertLess(result["comparison"]["delta_p002_minus_p001"]["all_agent_total_tokens_sum"], 0)
        self.assertGreater(result["comparison"]["delta_p002_minus_p001"]["elapsed_seconds_sum"], 0)
        self.assertFalse(result["comparison"]["cost_improvement_gate_passed"])
        self.assertFalse(result["comparison"]["standard14_next_gate_passed"])
        self.assertIsNone(result["allowed_next_profile_class"])
        self.assertEqual(result["result_sha256"], self.runner.base.content_identity(result, "result_sha256"))

    def test_vcc6_policy_reuses_fixed_benchmark_with_prompt_as_only_variable(self) -> None:
        policy = json.loads(
            (TARGET_ROOT / "registrations/vcc6-fixed-benchmark-policy-r1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(policy["benchmark"]["short_name"], "VCC6")
        self.assertEqual(policy["policy"]["experimental_variable"], "prompt_identity_only")
        self.assertTrue(policy["policy"]["reuse_across_candidates"])
        self.assertTrue(policy["policy"]["result_guided_prompt_design_allowed"])
        self.assertFalse(policy["policy"]["candidate_specific_benchmark_replacement"])
        self.assertFalse(policy["policy"]["blind_claim_after_result_guided_design"])
        self.assertEqual(
            policy["historical_field_interpretation"][
                "source_freeze.prompt_boundary.prompt_change_invalidates_candidate_selection_use"
            ],
            "invalidates_blind_candidate_selection_claim_only_not_fixed_benchmark_comparison",
        )
        self.assertIn("case", policy["policy"]["fixed_conditions"])
        self.assertIn("agent_runtime_cli", policy["policy"]["fixed_conditions"])


if __name__ == "__main__":
    unittest.main()

import json
from pathlib import Path
import unittest

from scripts.compose_prompt import compose, verify_bundle_binding
from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
BUNDLE = TARGET_ROOT / "prompts/candidates/p005-portable-full-agent-codex-validation-terminal-projection-r1"
COMPOSITION_ROOT = ROOT / "prompts/compositions/c147-portable-kernel-draft-r1"
DRAFT = COMPOSITION_ROOT / "full-agent-codex-validation-terminal-projection-draft-r5.composition.json"
COMPOSITION = COMPOSITION_ROOT / "full-agent-codex-validation-terminal-projection-candidate-r1.composition.json"
REGISTRATION = TARGET_ROOT / "registrations/p005-composition-binding-r1.json"


class CodexValidationCarrierP005Test(unittest.TestCase):
    def test_candidate_bundle_is_bound_to_candidate_composition(self) -> None:
        bundle = verify_bundle(BUNDLE)
        receipt = verify_bundle_binding(COMPOSITION, BUNDLE)
        self.assertEqual(bundle["prompt_identity"], "p005-portable-full-agent-codex-validation-terminal-projection-r1")
        self.assertEqual(receipt["binding_status"], "verified")
        self.assertEqual(receipt["output_bytes_verified"], 12830)

    def test_candidate_and_management_draft_render_identical_bytes(self) -> None:
        draft_bytes, draft_receipt = compose(DRAFT)
        candidate_bytes, candidate_receipt = compose(COMPOSITION)
        self.assertEqual(candidate_bytes, draft_bytes)
        self.assertEqual(candidate_receipt["dependency_closure"], "verified")
        self.assertEqual(draft_receipt["output_sha256"], "2cb70ccd11fcfe605accf9b212050ed08b6db0eb0a522d502d35c33d58301681")

    def test_p001_is_parent_and_p002_through_p004_are_counterexamples(self) -> None:
        registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
        self.assertEqual(registration["direct_parent"]["prompt_identity"], "portable-semantic-c147-portable-full-agent-r1")
        self.assertEqual(
            [entry["prompt_identity"] for entry in registration["counterexamples"]],
            [
                "p002-portable-full-agent-codex-validation-carrier-r1",
                "p003-portable-full-agent-codex-validation-plan-identity-carrier-r1",
                "p004-portable-full-agent-codex-validation-prebound-carrier-r1",
            ],
        )
        self.assertTrue(all("直接親ではない" in entry["role"] for entry in registration["counterexamples"]))
        self.assertFalse(registration["preserved_boundary"]["case_oracle_rating_runtime_changed"])
        self.assertEqual(registration["state"], "candidate_bundle_bound_not_evaluated")

    def test_only_validation_plan_and_codex_carrier_change_from_p004(self) -> None:
        p004 = json.loads((COMPOSITION_ROOT / "full-agent-codex-validation-prebound-carrier-candidate-r1.composition.json").read_text(encoding="utf-8"))
        p005 = json.loads(COMPOSITION.read_text(encoding="utf-8"))
        changed = [(before["id"], after["id"]) for before, after in zip(p004["components"], p005["components"], strict=True) if before["sha256"] != after["sha256"] or before["id"] != after["id"]]
        self.assertEqual(
            changed,
            [
                ("validation-plan-projection-r4", "validation-terminal-projection-plan-r5"),
                ("validation-prebound-carrier-codex-r4", "validation-terminal-projection-codex-r5"),
            ],
        )

    def test_terminal_projection_is_the_only_outer_result_producer(self) -> None:
        prompt = (BUNDLE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertIn("carrier-localな`nested_result`", prompt)
        self.assertIn("outer output、text、commentary、notification、mediaまたはyieldのproducerにしない", prompt)
        self.assertIn("そのobjectだけをouterへ一度投影する", prompt)
        self.assertIn("`terminal_projection_ready=false`", prompt)

    def test_candidate_only_n1_gate_passed(self) -> None:
        result = json.loads((TARGET_ROOT / "results/vcc6-p005-shared-runner-n1-candidate-gate-r1.json").read_text(encoding="utf-8"))
        self.assertEqual(result["summary"]["valid_results"], 6)
        self.assertEqual(result["summary"]["quality_score_distribution"], {"4": 6})
        self.assertEqual(result["summary"]["mechanism_passed"], 6)
        self.assertTrue(result["candidate_gate"]["passed"])
        self.assertEqual(result["allowed_next_profile_class"], "vcc6_prompt_only_shared_runner_n5")
        h06 = next(row for row in result["cases"] if row["slot"]["case_id"] == "VCC-H06")
        self.assertEqual(h06["quality_score"], 4)
        self.assertTrue(h06["mechanism_passed"])

    def test_fresh_three_arm_n5_stops_before_standard14(self) -> None:
        result = json.loads((TARGET_ROOT / "results/vcc6-p001-p003-p005-shared-runner-n5-comparison-r1.json").read_text(encoding="utf-8"))
        self.assertEqual(result["logical_slot_count"], 90)
        self.assertEqual(result["new_dispatch_slot_count"], 90)
        self.assertEqual(result["reused_slot_count"], 0)
        self.assertEqual(result["arms"]["P005"]["summary"]["quality_score_distribution"], {"4": 30})
        self.assertEqual(result["arms"]["P005"]["summary"]["mechanism_passed"], 30)
        self.assertTrue(result["comparison"]["p005_cost_improvement_vs_p003_passed"])
        self.assertFalse(result["comparison"]["p005_cost_improvement_vs_direct_parent_p001_passed"])
        self.assertFalse(result["comparison"]["standard14_next_gate_passed"])
        self.assertIsNone(result["allowed_next_profile_class"])


if __name__ == "__main__":
    unittest.main()

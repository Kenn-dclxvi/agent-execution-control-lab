import importlib.util
import json
from pathlib import Path
import unittest

from scripts.compose_prompt import verify_bundle_binding
from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
PROFILE = TARGET_ROOT / "profiles/codex-validation-carrier-p002-heldout-r1-codex-cli0146-sol-medium-n1-r1.json"
PLAN = TARGET_ROOT / "plans/codex-validation-carrier-p002-heldout-r1-n1-dispatch-r1.json"
PREFLIGHT = TARGET_ROOT / "plans/codex-validation-carrier-p002-heldout-r1-n1-preflight-r1.json"
BUNDLE = TARGET_ROOT / "prompts/candidates/p002-portable-full-agent-codex-validation-carrier-r1"
COMPOSITION = ROOT / "prompts/compositions/c147-portable-kernel-draft-r1/full-agent-codex-validation-carrier-candidate-r1.composition.json"


def load_runner():
    path = TARGET_ROOT / "runtime/runner_p002.py"
    spec = importlib.util.spec_from_file_location("codex_validation_carrier_p002_runner_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CodexValidationCarrierP002Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = load_runner()

    def test_candidate_bundle_is_bound_to_candidate_composition(self) -> None:
        bundle = verify_bundle(BUNDLE)
        receipt = verify_bundle_binding(COMPOSITION, BUNDLE)
        self.assertEqual(bundle["prompt_identity"], "p002-portable-full-agent-codex-validation-carrier-r1")
        self.assertEqual(receipt["binding_status"], "verified")
        self.assertEqual(receipt["output_bytes_verified"], 12922)

    def test_candidate_profile_is_the_only_authorized_class(self) -> None:
        binding = self.runner.validate_profile(
            repository_root=ROOT,
            profile_path=PROFILE,
            target_path=TARGET_ROOT / "target.json",
        )
        self.assertEqual(binding["profile"]["scope"]["profile_class"], "candidate_only_p002_gate")
        registration = json.loads(binding["runtime_registration_path"].read_text(encoding="utf-8"))
        self.assertEqual(registration["allowed_next_profile_class"], "candidate_only_p002_gate")

    def test_stored_plan_and_preflight_are_fresh_and_unissued(self) -> None:
        receipt, plan = self.runner.validate_preflight(
            repository_root=ROOT,
            receipt_path=PREFLIGHT,
            observed_version="codex-cli 0.146.0",
        )
        self.assertEqual(plan["plan_id"], "codex-validation-carrier-p002-heldout-r1-n1-dispatch-r1")
        self.assertEqual(plan["authorized_slot_count"], 6)
        self.assertEqual(plan["issued_slot_count"], 0)
        self.assertTrue(receipt["dispatch_allowed"])
        self.assertEqual(receipt["profile_class"], "candidate_only_p002_gate")

    def test_control_free_runner_remains_bound_to_qualification_registration(self) -> None:
        registration = json.loads((TARGET_ROOT / "registrations/heldout-r1-runtime-registration-r1.json").read_text(encoding="utf-8"))
        self.assertEqual(
            registration["runtime_implementation"]["runner"]["sha256"],
            "81b1bc723b4cb23ca775fa49a5f97a075dc0610cbb9ac8f68e7b741ae7b03224",
        )

    def test_candidate_gate_result_passes_without_claiming_efficiency(self) -> None:
        result = json.loads((TARGET_ROOT / "results/codex-validation-carrier-p002-heldout-r1-n1-candidate-gate-r1.json").read_text(encoding="utf-8"))
        self.assertEqual(result["summary"]["quality_score_distribution"], {"4": 6})
        self.assertEqual(result["summary"]["mechanism_passed"], 6)
        self.assertTrue(result["candidate_gate"]["passed"])
        self.assertEqual(result["candidate_gate"]["efficiency_claim"], "not_available_without_p001_paired_result")
        self.assertEqual(result["allowed_next_profile_class"], "p001_p002_paired_targeted_n5")


if __name__ == "__main__":
    unittest.main()

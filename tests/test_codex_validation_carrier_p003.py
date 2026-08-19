import json
from pathlib import Path
import unittest

from scripts.compose_prompt import compose, verify_bundle_binding
from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
BUNDLE = TARGET_ROOT / "prompts/candidates/p003-portable-full-agent-codex-validation-plan-identity-carrier-r1"
COMPOSITION_ROOT = ROOT / "prompts/compositions/c147-portable-kernel-draft-r1"
DRAFT = COMPOSITION_ROOT / "full-agent-codex-validation-plan-identity-carrier-draft-r3.composition.json"
COMPOSITION = COMPOSITION_ROOT / "full-agent-codex-validation-plan-identity-carrier-candidate-r1.composition.json"
REGISTRATION = TARGET_ROOT / "registrations/p003-composition-binding-r1.json"


class CodexValidationCarrierP003Test(unittest.TestCase):
    def test_candidate_bundle_is_bound_to_candidate_composition(self) -> None:
        bundle = verify_bundle(BUNDLE)
        receipt = verify_bundle_binding(COMPOSITION, BUNDLE)
        self.assertEqual(bundle["prompt_identity"], "p003-portable-full-agent-codex-validation-plan-identity-carrier-r1")
        self.assertEqual(receipt["binding_status"], "verified")
        self.assertEqual(receipt["output_bytes_verified"], 12864)

    def test_candidate_and_management_draft_render_identical_bytes(self) -> None:
        draft_bytes, _ = compose(DRAFT)
        candidate_bytes, _ = compose(COMPOSITION)
        self.assertEqual(candidate_bytes, draft_bytes)

    def test_binding_keeps_p001_as_parent_and_p002_as_counterexample(self) -> None:
        registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
        self.assertEqual(registration["direct_parent"]["prompt_identity"], "portable-semantic-c147-portable-full-agent-r1")
        self.assertEqual(registration["failed_counterexample"]["prompt_identity"], "p002-portable-full-agent-codex-validation-carrier-r1")
        self.assertIn("直接親ではない", registration["failed_counterexample"]["role"])
        self.assertFalse(registration["preserved_boundary"]["case_oracle_rating_runtime_changed"])
        self.assertEqual(registration["state"], "candidate_bundle_bound_not_evaluated")

    def test_only_codex_carrier_component_changes_from_p002_composition(self) -> None:
        p002 = json.loads((COMPOSITION_ROOT / "full-agent-codex-validation-carrier-candidate-r1.composition.json").read_text(encoding="utf-8"))
        p003 = json.loads(COMPOSITION.read_text(encoding="utf-8"))
        p002_paths = [component["path"] for component in p002["components"]]
        p003_paths = [component["path"] for component in p003["components"]]
        self.assertEqual(p002_paths[:-2], p003_paths[:-2])
        self.assertNotEqual(p002_paths[-2], p003_paths[-2])
        self.assertEqual(p002_paths[-1], p003_paths[-1])

    def test_p003_shared_runner_preflight_is_unissued_and_no_result_exists(self) -> None:
        profile = json.loads((TARGET_ROOT / "profiles/vcc6-p003-shared-runner-sol-medium-n1-r2.json").read_text(encoding="utf-8"))
        plan = json.loads((TARGET_ROOT / "plans/vcc6-p003-shared-runner-n1-dispatch-r2.json").read_text(encoding="utf-8"))
        preflight = json.loads((TARGET_ROOT / "plans/vcc6-p003-shared-runner-n1-preflight-r2.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["scope"]["profile_class"], "vcc6_prompt_only_shared_runner_n1")
        self.assertEqual(plan["issued_slot_count"], 0)
        self.assertEqual(preflight["issued_slot_count"], 0)
        result = json.loads((TARGET_ROOT / "results/vcc6-p001-p002-p003-shared-runner-n1-result-r1.json").read_text(encoding="utf-8"))
        self.assertEqual(result["arms"]["P003"]["summary"]["valid_results"], 6)
        self.assertEqual(result["arms"]["P003"]["summary"]["quality_score_distribution"], {"4": 6})
        self.assertEqual(result["arms"]["P003"]["summary"]["mechanism_passed"], 6)
        self.assertFalse(result["comparison_scope"]["n1_stability_claim"])


if __name__ == "__main__":
    unittest.main()

import json
from pathlib import Path
import unittest

from scripts.compose_prompt import compose, verify_bundle_binding
from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
BUNDLE = TARGET_ROOT / "prompts/candidates/p004-portable-full-agent-codex-validation-prebound-carrier-r1"
COMPOSITION_ROOT = ROOT / "prompts/compositions/c147-portable-kernel-draft-r1"
DRAFT = COMPOSITION_ROOT / "full-agent-codex-validation-prebound-carrier-draft-r4.composition.json"
COMPOSITION = COMPOSITION_ROOT / "full-agent-codex-validation-prebound-carrier-candidate-r1.composition.json"
REGISTRATION = TARGET_ROOT / "registrations/p004-composition-binding-r1.json"


class CodexValidationCarrierP004Test(unittest.TestCase):
    def test_candidate_bundle_is_bound_to_candidate_composition(self) -> None:
        bundle = verify_bundle(BUNDLE)
        receipt = verify_bundle_binding(COMPOSITION, BUNDLE)
        self.assertEqual(bundle["prompt_identity"], "p004-portable-full-agent-codex-validation-prebound-carrier-r1")
        self.assertEqual(receipt["binding_status"], "verified")
        self.assertEqual(receipt["output_bytes_verified"], 12781)

    def test_candidate_and_management_draft_render_identical_bytes(self) -> None:
        draft_bytes, draft_receipt = compose(DRAFT)
        candidate_bytes, candidate_receipt = compose(COMPOSITION)
        self.assertEqual(candidate_bytes, draft_bytes)
        self.assertEqual(candidate_receipt["dependency_closure"], "verified")
        self.assertEqual(draft_receipt["output_sha256"], "82792275a9e120e1e9e794244ca72ef804c1b7f8c9ac39a4ae0c56493aad468a")

    def test_binding_keeps_p001_as_parent_and_p002_p003_as_counterexamples(self) -> None:
        registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
        self.assertEqual(registration["direct_parent"]["prompt_identity"], "portable-semantic-c147-portable-full-agent-r1")
        self.assertEqual(
            [entry["prompt_identity"] for entry in registration["counterexamples"]],
            [
                "p002-portable-full-agent-codex-validation-carrier-r1",
                "p003-portable-full-agent-codex-validation-plan-identity-carrier-r1",
            ],
        )
        self.assertTrue(all("直接親ではない" in entry["role"] for entry in registration["counterexamples"]))
        self.assertFalse(registration["preserved_boundary"]["case_oracle_rating_runtime_changed"])
        self.assertEqual(registration["state"], "candidate_bundle_bound_not_evaluated")

    def test_only_validation_plan_and_codex_contract_change_from_p003(self) -> None:
        p003 = json.loads(
            (COMPOSITION_ROOT / "full-agent-codex-validation-plan-identity-carrier-candidate-r1.composition.json").read_text(
                encoding="utf-8"
            )
        )
        p004 = json.loads(COMPOSITION.read_text(encoding="utf-8"))
        changed = [
            (before["id"], after["id"])
            for before, after in zip(p003["components"], p004["components"], strict=True)
            if before["sha256"] != after["sha256"]
        ]
        self.assertEqual(
            changed,
            [
                ("validation-plan-semantics-r2", "validation-plan-projection-r4"),
                ("validation-plan-identity-carrier-codex-r3", "validation-prebound-carrier-codex-r4"),
            ],
        )

    def test_platform_contract_and_failed_candidate_gate_are_bound(self) -> None:
        registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
        self.assertEqual(
            registration["platform_contract"]["capability_catalog"]["sha256"],
            "520092cb26dfc9da4cd53fa75e05e301d43dd8a9e3a0b97df2d332c3a7e46b17",
        )
        self.assertEqual(
            registration["platform_contract"]["schema_transport"]["sha256"],
            "a468155a10199c62cd05b9ee458cbbb357714345c4c5006214933a76cc6c0eb8",
        )
        profile = json.loads((TARGET_ROOT / "profiles/vcc6-p004-shared-runner-sol-medium-n1-r1.json").read_text(encoding="utf-8"))
        preflight = json.loads((TARGET_ROOT / "plans/vcc6-p004-shared-runner-n1-preflight-r1.json").read_text(encoding="utf-8"))
        result = json.loads((TARGET_ROOT / "results/vcc6-p004-shared-runner-n1-candidate-gate-r1.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["scope"]["profile_class"], "vcc6_prompt_only_shared_runner_n1")
        self.assertEqual(preflight["authorized_slot_count"], 6)
        self.assertEqual(preflight["issued_slot_count"], 0)
        self.assertEqual(result["summary"]["valid_results"], 6)
        self.assertEqual(result["summary"]["quality_score_distribution"], {"1": 1, "4": 5})
        self.assertFalse(result["candidate_gate"]["passed"])
        self.assertIsNone(result["allowed_next_profile_class"])
        self.assertEqual(result["state"], "candidate_only_gate_failed_stop")


if __name__ == "__main__":
    unittest.main()

import json
from pathlib import Path
import unittest

from scripts.compose_prompt import compose, verify_bundle_binding
from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
BUNDLE = TARGET_ROOT / "prompts/candidates/p006-portable-full-agent-codex-frontier-carrier-r1"
P005_BUNDLE = TARGET_ROOT / "prompts/candidates/p005-portable-full-agent-codex-validation-terminal-projection-r1"
COMPOSITION_ROOT = ROOT / "prompts/compositions/c147-portable-kernel-draft-r1"
DRAFT = COMPOSITION_ROOT / "full-agent-codex-frontier-carrier-draft-r6.composition.json"
COMPOSITION = COMPOSITION_ROOT / "full-agent-codex-frontier-carrier-candidate-r1.composition.json"
P005_COMPOSITION = COMPOSITION_ROOT / "full-agent-codex-validation-terminal-projection-candidate-r1.composition.json"
REGISTRATION = TARGET_ROOT / "registrations/p006-composition-binding-r1.json"
COVERAGE = COMPOSITION_ROOT / "frontier-carrier-codex-r1-coverage.json"


class CodexFrontierCarrierP006Test(unittest.TestCase):
    def test_candidate_bundle_is_bound_to_candidate_composition(self) -> None:
        bundle = verify_bundle(BUNDLE)
        receipt = verify_bundle_binding(COMPOSITION, BUNDLE)
        self.assertEqual(bundle["prompt_identity"], "p006-portable-full-agent-codex-frontier-carrier-r1")
        self.assertEqual(bundle["bundle_sha256"], "9ccd6ce5279831828e9a20685fc2aa78f62043b32471003db37dd43e3114afce")
        self.assertEqual(receipt["binding_status"], "verified")
        self.assertEqual(receipt["output_bytes_verified"], 14593)

    def test_candidate_and_management_draft_render_identical_bytes(self) -> None:
        draft_bytes, draft_receipt = compose(DRAFT)
        candidate_bytes, candidate_receipt = compose(COMPOSITION)
        self.assertEqual(candidate_bytes, draft_bytes)
        self.assertEqual(candidate_receipt["dependency_closure"], "verified")
        self.assertEqual(draft_receipt["output_sha256"], "669a66d8350e250260922eb25706a11f0e75b5aeb1064ca323a62a9be26c5c91")

    def test_p005_is_direct_parent_and_only_one_component_is_added(self) -> None:
        p005 = json.loads(P005_COMPOSITION.read_text(encoding="utf-8"))
        p006 = json.loads(COMPOSITION.read_text(encoding="utf-8"))
        self.assertEqual(p006["components"][:12], p005["components"][:12])
        self.assertEqual(p006["components"][13:], p005["components"][12:])
        self.assertEqual(p006["components"][12]["id"], "frontier-carrier-codex-r1")
        registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
        self.assertEqual(registration["direct_parent"]["prompt_identity"], "p005-portable-full-agent-codex-validation-terminal-projection-r1")
        self.assertEqual(registration["preserved_boundary"]["parent_components"], "13_of_13_byte_preserved")
        self.assertFalse(registration["preserved_boundary"]["case_oracle_rating_runtime_changed"])

    def test_parent_bytes_are_preserved_around_the_added_component(self) -> None:
        p005 = (P005_BUNDLE / "files/AGENTS.md.txt").read_bytes()
        p006 = (BUNDLE / "files/AGENTS.md.txt").read_bytes()
        component = (COMPOSITION_ROOT / "components/87-frontier-carrier-codex-r1.md").read_bytes()
        method = (COMPOSITION_ROOT / "components/90-method-recovery.md").read_bytes()
        self.assertTrue(p005.endswith(method))
        self.assertEqual(p006, p005[: -len(method)] + component + method)

    def test_frontier_result_ingress_edge_is_closed(self) -> None:
        prompt = (BUNDLE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertIn("全memberを一つのmodel outputから個別tool callとしてcommitする", prompt)
        self.assertIn("全memberのcommit前は個別result、progressまたは部分観測をmodel-visible input", prompt)
        self.assertIn("runtime上のtool開始・完了順はterminal条件にしない", prompt)
        self.assertIn("subsetへ縮退せず、そのfrontierを`unavailable`へbindする", prompt)
        self.assertIn("shell compound commandへ統合しない", prompt)

    def test_coverage_and_evaluation_state_are_fixed(self) -> None:
        coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
        registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
        self.assertEqual(coverage["covered_primitive_count"], coverage["required_primitive_count"])
        self.assertEqual(coverage["changed_parent_components"], 0)
        self.assertEqual(registration["state"], "candidate_bundle_bound_not_evaluated")
        self.assertFalse(registration["evaluation_boundary"]["preflight_created"])
        self.assertEqual(registration["evaluation_boundary"]["evaluation_slots_issued"], 0)


if __name__ == "__main__":
    unittest.main()

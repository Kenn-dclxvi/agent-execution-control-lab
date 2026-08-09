import hashlib
import json
import unittest
from pathlib import Path

from scripts.evaluation_loop import QUALITY_RATING_V14, validate_comparison_conditions


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evaluations" / "cases"
REVISION = "adversarial-design-review-r1"
SPEC_ID = "design_revision_7:semantic-sha256:e84906bf8e1c48446e305fbebbc3004e61da3865ff719ba90b1f6ddafe212f56"
EVAL_ID = "preimplementation-adversarial-design-review-targeted-evaluation-design-r10"
CASE_IDS = [
    "TC-ADR01",
    "TC-ADR02",
    "TC-ADR03",
    "TC-ADR04",
    "TC-ADR05",
    "TC-ADR06",
    "TC-ADR07",
    "TC-ADR08",
    "TC-ADR09",
]
PROFILE_R2 = ROOT / "evaluations/profiles/candidate147-preimplementation-adversarial-design-review-problem-qualification-r2-medium-m24-n5-cli0146.json"


def revision(case_id: str) -> Path:
    return CASES / case_id / REVISION


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def seeded_fixture(case_id: str):
    patch = (revision(case_id) / "private" / "seed.patch").read_text(encoding="utf-8")
    section = next(
        chunk
        for chunk in patch.split("diff --git ")
        if "b/evaluation-fixture/design-admission.json" in chunk
    )
    body = section.split("@@", 2)[2]
    payload = "\n".join(line[1:] for line in body.splitlines() if line.startswith("+")) + "\n"
    return json.loads(payload)


class PreimplementationAdversarialDesignReviewCasesTest(unittest.TestCase):
    def test_execution_profile_r2_uses_supported_rating_contract(self):
        profile = load_json(PROFILE_R2)
        self.assertEqual(profile["comparison_conditions"]["quality_rating"], QUALITY_RATING_V14)
        self.assertEqual(
            validate_comparison_conditions(profile["comparison_conditions"])["quality_rating"],
            QUALITY_RATING_V14,
        )

    def test_all_nine_cases_bind_fixed_identities(self):
        self.assertEqual(len(CASE_IDS), 9)
        for case_id in CASE_IDS:
            root = revision(case_id)
            private = load_json(root / "private" / "case-data.json")
            trial = load_json(root / "trial-prompt-input.json")
            self.assertEqual(private["case_id"], case_id)
            self.assertEqual(private["case_revision"], REVISION)
            self.assertEqual(private["oracle"]["general_design_spec_identity"], SPEC_ID)
            self.assertEqual(private["oracle"]["target_evaluation_design_identity"], EVAL_ID)
            self.assertIn("preimplementation_design_admission", trial["task_kind_goal_and_done_condition"])
            patch = root / "private" / "seed.patch"
            self.assertEqual(hashlib.sha256(patch.read_bytes()).hexdigest(), private["seed"]["artifact"]["raw_sha256"])

    def test_all_authorities_are_fixed_before_current_design(self):
        for case_id in CASE_IDS:
            fixture = seeded_fixture(case_id)
            self.assertEqual(fixture["authority"]["provenance"], "fixed-before-current-design")
            self.assertTrue(fixture["authority"]["identity"])
            self.assertTrue(fixture["authority"]["domain"])
            self.assertTrue(fixture["authority"]["closure_statement"])

    def test_adr07_and_adr09_are_one_axis_manifest_pair(self):
        success = seeded_fixture("TC-ADR07")
        unavailable = seeded_fixture("TC-ADR09")
        for key in ("task_contract", "authority", "general_design", "boundary_ledger", "required_validation", "consumer_inventory", "consumer_contracts", "artifacts"):
            self.assertEqual(success[key], unavailable[key], key)
        self.assertEqual(success["review_contract"]["required_review_scope_identities"], unavailable["review_contract"]["required_review_scope_identities"])
        left = success["review_contract"]["finite_evidence_manifest"]
        right = unavailable["review_contract"]["finite_evidence_manifest"]
        self.assertEqual(len(left), len(right))
        differences = []
        for a, b in zip(left, right, strict=True):
            for key in a:
                if a[key] != b[key]:
                    differences.append((a["observation_identity"], key, a[key], b[key]))
        self.assertEqual(differences, [])
        success_paths = {entry["path"] for entry in load_json(revision(CASE_IDS[6]) / "private" / "case-data.json")["seed"]["expected_post_seed_files"]}
        unavailable_paths = {entry["path"] for entry in load_json(revision(CASE_IDS[8]) / "private" / "case-data.json")["seed"]["expected_post_seed_files"]}
        self.assertIn("evaluation-fixture/paired-scope-evidence.json", success_paths)
        self.assertNotIn("evaluation-fixture/paired-scope-evidence.json", unavailable_paths)

    def test_adr06_canary_is_not_in_trial_packet(self):
        root = revision("TC-ADR06")
        trial = (root / "trial-prompt-input.json").read_text(encoding="utf-8")
        patch = (root / "private" / "seed.patch").read_text(encoding="utf-8")
        self.assertNotIn("FORBIDDEN-ADR06-PRIOR-FINDING-CANARY", trial)
        self.assertIn("FORBIDDEN-ADR06-PRIOR-FINDING-CANARY", patch)

    def test_adr08_denies_review_before_operation_creation(self):
        fixture = seeded_fixture("TC-ADR08")
        self.assertEqual(fixture["review_contract"]["permission"], "denied")
        self.assertEqual(len(fixture["boundary_ledger"]), 2)
        self.assertEqual(fixture["untrusted_prior_result"]["reviewed_boundaries"], ["B-MEMBERSHIP"])
        private = load_json(revision(CASE_IDS[7]) / "private" / "case-data.json")
        self.assertEqual(private["mechanism_expectation"]["permission_denied_review_operations"], 0)

    def test_boundary_ledgers_are_complete_and_case_ids_are_opaque(self):
        required = {
            "boundary_identity", "boundary_kind", "domain", "closure_source",
            "required_validation_coverage", "counterexample_effect", "direct_basis",
            "closure_authority_identity", "closure_authority_provenance",
            "counterexample_effect_basis",
        }
        for case_id in CASE_IDS:
            fixture = seeded_fixture(case_id)
            self.assertEqual(fixture["identity"]["case_identity"], f"{case_id}/{REVISION}")
            for entry in fixture["boundary_ledger"]:
                self.assertTrue(required.issubset(entry))
        self.assertEqual(
            [item["boundary_identity"] for item in seeded_fixture("TC-ADR04")["boundary_ledger"]],
            ["B-RETAINED-MEMBERSHIP", "B-RETAINED-STOP-APPLICABILITY"],
        )


if __name__ == "__main__":
    unittest.main()

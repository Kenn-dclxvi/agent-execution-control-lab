import hashlib
import json
import unittest
from pathlib import Path

from scripts.evaluation_loop import QUALITY_RATING_V14, validate_comparison_conditions


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evaluations/cases"
REVISION = "adversarial-design-review-r4"
EVAL_ID = "preimplementation-adversarial-design-review-targeted-evaluation-design-r13"
CASE_IDS = [f"TC-ADR{number:02d}" for number in range(1, 10)]
PROFILE = ROOT / "evaluations/profiles/candidate223-review-scope-exact-carrier-adr9-r4-medium-m24-n5-cli0146-r1.json"


def revision(case_id: str) -> Path:
    return CASES / case_id / REVISION


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def seeded_fixture(case_id: str):
    patch = (revision(case_id) / "private/seed.patch").read_text(encoding="utf-8")
    section = next(chunk for chunk in patch.split("diff --git ") if "b/evaluation-fixture/design-admission.json" in chunk)
    body = section.split("@@", 2)[2]
    payload = "\n".join(line[1:] for line in body.splitlines() if line.startswith("+")) + "\n"
    return json.loads(payload)


class PreimplementationAdversarialDesignReviewCasesR4Test(unittest.TestCase):
    def test_profile_binds_r4_and_supported_rating(self):
        profile = load_json(PROFILE)
        self.assertEqual(profile["evaluation_set"]["revision"], REVISION)
        self.assertEqual(profile["comparison_conditions"]["task_spec"]["source"], EVAL_ID)
        self.assertEqual(profile["comparison_conditions"]["quality_rating"], QUALITY_RATING_V14)
        self.assertEqual(validate_comparison_conditions(profile["comparison_conditions"])["quality_rating"], QUALITY_RATING_V14)

    def test_all_cases_bind_identity_and_seed_hash(self):
        for case_id in CASE_IDS:
            root = revision(case_id)
            private = load_json(root / "private/case-data.json")
            trial = load_json(root / "trial-prompt-input.json")
            self.assertEqual(private["case_id"], case_id)
            self.assertEqual(private["case_revision"], REVISION)
            self.assertEqual(private["oracle"]["target_evaluation_design_identity"], EVAL_ID)
            self.assertEqual(seeded_fixture(case_id)["identity"]["case_identity"], f"{case_id}/{REVISION}")
            patch = root / "private/seed.patch"
            self.assertEqual(hashlib.sha256(patch.read_bytes()).hexdigest(), private["seed"]["artifact"]["raw_sha256"])
            self.assertEqual(trial["review_scope_carrier_contract"]["schema_version"], "review-scope-carrier-contract/v2")

    def test_scope_specific_direct_carriers_are_exact(self):
        expected = {
            "TC-ADR01": [], "TC-ADR02": [],
            "TC-ADR03": ["OBS-INVENTORY", "OBS-CONSUMER-CONTRACTS"],
            "TC-ADR04": ["OBS-INVENTORY", "OBS-CONSUMER-CONTRACTS"],
            "TC-ADR05": ["OBS-INVENTORY", "OBS-CONSUMER-CONTRACTS"],
            "TC-ADR06": ["OBS-INVENTORY", "OBS-CONSUMER-CONTRACTS"],
            "TC-ADR07": ["OBS-PAIRED-SCOPE"],
            "TC-ADR08": [],
            "TC-ADR09": ["OBS-PAIRED-SCOPE"],
        }
        for case_id, observations in expected.items():
            contract = load_json(revision(case_id) / "trial-prompt-input.json")["review_scope_carrier_contract"]
            self.assertEqual([entry["observation_identity"] for entry in contract["reviewer_direct_entries"]], observations)
            self.assertEqual(contract["unlisted_manifest_targets"], "forbidden")
            self.assertEqual(contract["whole_container_or_ancestor_output"], "forbidden")

    def test_missing_paired_evidence_is_not_added(self):
        for case_id in ("TC-ADR03", "TC-ADR04", "TC-ADR05", "TC-ADR06", "TC-ADR09"):
            paths = {entry["path"] for entry in load_json(revision(case_id) / "private/case-data.json")["seed"]["expected_post_seed_files"]}
            self.assertNotIn("evaluation-fixture/paired-scope-evidence.json", paths)
        paths = {entry["path"] for entry in load_json(revision("TC-ADR07") / "private/case-data.json")["seed"]["expected_post_seed_files"]}
        self.assertIn("evaluation-fixture/paired-scope-evidence.json", paths)

    def test_r2_oracles_are_preserved(self):
        for case_id in CASE_IDS:
            r2 = load_json(CASES / case_id / "adversarial-design-review-r2/private/case-data.json")["oracle"]
            r4 = load_json(revision(case_id) / "private/case-data.json")["oracle"]
            for key in ("expected_artifact_route", "expected_disposition", "expected_review_result", "general_design_spec_identity"):
                self.assertEqual(r4[key], r2[key], (case_id, key))


if __name__ == "__main__":
    unittest.main()

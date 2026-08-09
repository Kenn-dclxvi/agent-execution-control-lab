from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evaluations" / "cases"
PROFILE = ROOT / "evaluations" / "profiles" / (
    "candidate166-prechange-repair-contract-problem-qualification-r1-medium-m24-n5-cli0146.json"
)

PAIRS = (
    ("TC-RC02-T4-NO-REPAIR-CLEAN", "TC-RC03-T4-NO-REPAIR-PERTURBED", "no_repair_required", "completion_ready"),
    ("TC-RC04-T6-REPAIR-CLEAN", "TC-RC05-T6-REPAIR-PERTURBED", "repair_contract_ready", "completion_ready"),
    ("TC-RC06-T6-EVIDENCE-UNAVAILABLE-CLEAN", "TC-RC07-T6-EVIDENCE-UNAVAILABLE-PERTURBED", "unavailable", "unavailable"),
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class PrechangeRepairContractCasesTest(unittest.TestCase):
    def test_pairs_change_only_prior_evaluation(self) -> None:
        for clean_id, perturbed_id, _, _ in PAIRS:
            clean = load_json(CASES / clean_id / "repair-contract-r1" / "trial-prompt-input.json")
            perturbed = load_json(CASES / perturbed_id / "repair-contract-r1" / "trial-prompt-input.json")
            self.assertNotEqual(clean["prior_evaluation_record"], perturbed["prior_evaluation_record"])
            clean_without_prior = dict(clean)
            perturbed_without_prior = dict(perturbed)
            clean_without_prior.pop("prior_evaluation_record")
            perturbed_without_prior.pop("prior_evaluation_record")
            self.assertEqual(clean_without_prior, perturbed_without_prior)

    def test_pairs_share_fixture_seed_and_oracle(self) -> None:
        for clean_id, perturbed_id, contract_state, disposition in PAIRS:
            clean_root = CASES / clean_id / "repair-contract-r1"
            perturbed_root = CASES / perturbed_id / "repair-contract-r1"
            clean = load_json(clean_root / "private" / "case-data.json")
            perturbed = load_json(perturbed_root / "private" / "case-data.json")
            self.assertEqual(clean["fixture"], perturbed["fixture"])
            self.assertEqual(clean["seed"], perturbed["seed"])
            self.assertEqual((clean_root / "private" / "seed.patch").read_bytes(), (perturbed_root / "private" / "seed.patch").read_bytes())
            for private in (clean, perturbed):
                self.assertEqual(private["oracle"]["expected_contract_state"], contract_state)
                self.assertEqual(private["oracle"]["expected_disposition"], disposition)
            clean_oracle = dict(clean["oracle"])
            perturbed_oracle = dict(perturbed["oracle"])
            clean_oracle.pop("condition")
            perturbed_oracle.pop("condition")
            self.assertEqual(clean_oracle, perturbed_oracle)

    def test_seed_hashes_match_private_metadata(self) -> None:
        for path in CASES.glob("TC-RC*/repair-contract-r1/private/case-data.json"):
            private = load_json(path)
            seed_path = path.parent / "seed.patch"
            digest = hashlib.sha256(seed_path.read_bytes()).hexdigest()
            self.assertEqual(private["seed"]["artifact"]["raw_sha256"], digest, path)

    def test_no_artificial_canary_is_added(self) -> None:
        for path in CASES.glob("TC-RC*/repair-contract-r1/trial-prompt-input.json"):
            visible = path.read_text(encoding="utf-8").lower()
            self.assertNotIn("canary=", visible, path)
            self.assertNotIn("prior-eval-", visible, path)

    def test_machine_control_is_not_applicable_and_requires_change(self) -> None:
        private = load_json(CASES / "TC-RC01-EXACT-MACHINE-REPAIR" / "repair-contract-r1" / "private" / "case-data.json")
        self.assertEqual(private["oracle"]["expected_contract_state"], "not_applicable")
        self.assertTrue(private["diagnostic_expectation"]["artifact_change_required"])
        self.assertEqual(private["diagnostic_expectation"]["expected_contract_route"], "no_human_repair_contract_judgement")

    def test_profile_fixes_candidate166_seven_cases_n5_m24(self) -> None:
        profile = load_json(PROFILE)
        expected = {"TC-RC01-EXACT-MACHINE-REPAIR"} | {case_id for pair in PAIRS for case_id in pair[:2]}
        self.assertEqual({case["id"] for case in profile["cases"]}, expected)
        self.assertEqual({case["revision"] for case in profile["cases"]}, {"repair-contract-r1"})
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["name"], "the-caption-3ce91a4-prior-evaluation-review-admission-r1")
        self.assertEqual(profile["evaluation_set"], {"set_id": "the-caption-prechange-repair-contract-r1", "revision": "repair-contract-r1"})
        commands = profile["comparison_conditions"]["executor_parameters"]["command_evidence_protocol"]["required_command_groups_by_case"]
        self.assertEqual(set(commands), expected)
        self.assertEqual(commands["TC-RC06-T6-EVIDENCE-UNAVAILABLE-CLEAN"], [])
        self.assertEqual(commands["TC-RC07-T6-EVIDENCE-UNAVAILABLE-PERTURBED"], [])


if __name__ == "__main__":
    unittest.main()

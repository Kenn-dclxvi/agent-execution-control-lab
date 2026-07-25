from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from scripts.evaluation_loop import QUALITY_RATING_CLICK_V1, QUALITY_RATING_V13, SUPPORTED_QUALITY_RATINGS


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ID = "click-outcome-abstract-condition-preserving-v1"
CONTRACT = ROOT / f"evaluations/targets/click/rating-contracts/{CONTRACT_ID}.json"
THE_CAPTION_V13 = (
    ROOT / "evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json"
)
CASE_ID = "CLICK-F01-ANSI-SEQUENCE-STRIP"


class ClickRatingContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_registered_in_supported_ratings(self) -> None:
        self.assertIn(QUALITY_RATING_CLICK_V1, SUPPORTED_QUALITY_RATINGS)
        self.assertEqual(QUALITY_RATING_CLICK_V1["contract_id"], CONTRACT_ID)

    def test_registered_sha256_matches_file(self) -> None:
        digest = hashlib.sha256(CONTRACT.read_bytes()).hexdigest()
        self.assertEqual(QUALITY_RATING_CLICK_V1["contract_sha256"], digest)

    def test_contract_id_matches_filename(self) -> None:
        self.assertEqual(self.contract["contract_id"], CONTRACT_ID)

    def test_case_rules_cover_only_click_cases(self) -> None:
        self.assertEqual(list(self.contract["case_quality_rules"]), [CASE_ID])
        self.assertEqual(self.contract["boundary_rules"], {})

    def test_no_the_caption_case_ids_leak_in(self) -> None:
        text = CONTRACT.read_text(encoding="utf-8")
        for leaked in ("TC-A01", "TC-A02", "TC-F01", "TC-F10", "TC-D01"):
            self.assertNotIn(leaked, text)

    def test_instance_independent_sections_match_v13(self) -> None:
        v13 = json.loads(THE_CAPTION_V13.read_text(encoding="utf-8"))
        self.assertEqual(self.contract["quality_score_rule"], v13["quality_score_rule"])
        self.assertEqual(self.contract["producer_evidence"], v13["producer_evidence"])
        self.assertEqual(self.contract["schema_version"], v13["schema_version"])

    def test_command_evidence_keeps_v13_policies_and_adds_cwd(self) -> None:
        v13 = json.loads(THE_CAPTION_V13.read_text(encoding="utf-8"))["command_evidence"]
        evidence = self.contract["command_evidence"]
        for key in ("collector_schema_version", "measurement_failure_policy", "quality_failure_policy", "required_binding"):
            self.assertEqual(evidence[key], v13[key])
        self.assertIn("repository root", evidence["working_directory_contract"])

    def test_owner_producer_evidence_stays_diagnostic_only(self) -> None:
        self.assertEqual(QUALITY_RATING_CLICK_V1["owner_producer_evidence_policy"], "diagnostic_only")
        self.assertEqual(
            QUALITY_RATING_CLICK_V1["producer_evidence_schema_version"],
            QUALITY_RATING_V13["producer_evidence_schema_version"],
        )
        self.assertFalse(self.contract["diagnostic_observations"]["affect_quality_score"])

    def test_rater_input_forbids_seed_provenance(self) -> None:
        forbidden = self.contract["rater_input"]["forbidden"]
        self.assertTrue(any("seed" in item for item in forbidden))

    def test_descriptor_points_at_this_contract(self) -> None:
        descriptor = json.loads(
            (ROOT / "evaluations/targets/click/target.json").read_text(encoding="utf-8")
        )
        self.assertEqual(descriptor["current_rating_contract"], CONTRACT_ID)

    def test_contract_sha256_is_indexed(self) -> None:
        index = (
            ROOT / "evaluations/targets/click/rating-contracts/README.md"
        ).read_text(encoding="utf-8")
        self.assertIn(QUALITY_RATING_CLICK_V1["contract_sha256"], index)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from scripts.evaluation_loop import (
    QUALITY_RATING_CLICK_V1,
    QUALITY_RATING_CLICK_V2,
    QUALITY_RATING_CLICK_V3,
    QUALITY_RATING_CLICK_V4,
    QUALITY_RATING_CLICK_V5,
    QUALITY_RATING_CLICK_V6,
    QUALITY_RATING_CLICK_V7,
    QUALITY_RATING_CLICK_V8,
    QUALITY_RATING_CLICK_V9,
    QUALITY_RATING_CLICK_V10,
    QUALITY_RATING_V13,
    SUPPORTED_QUALITY_RATINGS,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ID = "click-outcome-abstract-condition-preserving-v10"
CONTRACT = ROOT / f"evaluations/targets/click/rating-contracts/{CONTRACT_ID}.json"
CONTRACT_V1 = ROOT / "evaluations/targets/click/rating-contracts/click-outcome-abstract-condition-preserving-v1.json"
THE_CAPTION_V13 = (
    ROOT / "evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json"
)
CLICK_RATINGS = (
    QUALITY_RATING_CLICK_V1,
    QUALITY_RATING_CLICK_V2,
    QUALITY_RATING_CLICK_V3,
    QUALITY_RATING_CLICK_V4,
    QUALITY_RATING_CLICK_V5,
    QUALITY_RATING_CLICK_V6,
    QUALITY_RATING_CLICK_V7,
    QUALITY_RATING_CLICK_V8,
    QUALITY_RATING_CLICK_V9,
    QUALITY_RATING_CLICK_V10,
)
BOUNDARY_CASE_IDS = [
    "CLICK-A01-LATENT-CONTEXT-POLICY",
    "CLICK-A02-REPOSITORY-RESOLVABLE-TOX-ROUTING",
]
CASE_IDS = [
    "CLICK-F01-ANSI-SEQUENCE-STRIP",
    "CLICK-F02-STREAM-DEPRECATION-CONTRACT",
    "CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP",
    "CLICK-F04-NESTED-GROUP-COMPLETION",
    "CLICK-F05-CLARIFY-COMMAND-ORDER",
    "CLICK-F05-OS-PYPI-PUBLISH-BOUNDARY",
    "CLICK-F06-RESTORE-ECHO-COLOR-REGRESSION",
    "CLICK-F07-CANONICAL-TOX-RUNNER",
    "CLICK-F07-P-DEPENDENCY-LOCK-PAIR",
    "CLICK-F08-SHELL-COMPLETION-DOC-SYNC",
    "CLICK-F10-COMMAND-API-INVENTORY",
    "CLICK-F10-R-NESTED-COMPLETION-REVIEW",
]


class ClickRatingContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_registered_in_supported_ratings(self) -> None:
        for rating in CLICK_RATINGS:
            self.assertIn(rating, SUPPORTED_QUALITY_RATINGS)
        self.assertEqual(QUALITY_RATING_CLICK_V10["contract_id"], CONTRACT_ID)

    def test_registered_sha256_matches_file(self) -> None:
        digest = hashlib.sha256(CONTRACT.read_bytes()).hexdigest()
        self.assertEqual(QUALITY_RATING_CLICK_V10["contract_sha256"], digest)
        for rating in CLICK_RATINGS:
            path = ROOT / f"evaluations/targets/click/rating-contracts/{rating['contract_id']}.json"
            self.assertEqual(rating["contract_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_contract_id_matches_filename(self) -> None:
        self.assertEqual(self.contract["contract_id"], CONTRACT_ID)

    def test_case_rules_cover_only_click_cases(self) -> None:
        self.assertEqual(list(self.contract["case_quality_rules"]), CASE_IDS)
        self.assertEqual(list(self.contract["boundary_rules"]), BOUNDARY_CASE_IDS)

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
        self.assertEqual(QUALITY_RATING_CLICK_V10["owner_producer_evidence_policy"], "diagnostic_only")
        self.assertEqual(
            QUALITY_RATING_CLICK_V10["producer_evidence_schema_version"],
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
        for rating in CLICK_RATINGS:
            self.assertIn(rating["contract_sha256"], index)


if __name__ == "__main__":
    unittest.main()

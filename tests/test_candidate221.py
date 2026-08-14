from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-source-authority-closure-r1"
RESULT = ROOT / "evaluations/results/4511cbb39fb04bb2ad47d6219a12cf7e.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5-mechanism-audit-r1.json"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate221Test(unittest.TestCase):
    def test_bundle_identity_and_direct_base(self) -> None:
        manifest = verify_bundle(CANDIDATE)
        self.assertEqual(manifest["bundle_sha256"], "4e40da5f16466226a053b5bcc5efa31c5600219f4117a8bc0635c3c5a0196562")
        self.assertEqual(manifest["content_relation"]["source_prompt_identity"], "the-caption-3ce91a4-result-effect-scope-r1")
        self.assertEqual(manifest["content_relation"]["changed_targets"], ["AGENTS.md"])

    def test_only_root_agents_differs_and_c147_is_verbatim(self) -> None:
        base_manifest = verify_bundle(BASE)
        candidate_manifest = verify_bundle(CANDIDATE)
        base_files = {item["target"]: item for item in base_manifest["files"]}
        candidate_files = {item["target"]: item for item in candidate_manifest["files"]}
        self.assertEqual([target for target in base_files if base_files[target] != candidate_files[target]], ["AGENTS.md"])
        base_clauses = clauses((BASE / "files/AGENTS.md.txt").read_text())
        candidate_clauses = clauses((CANDIDATE / "files/AGENTS.md.txt").read_text())
        for label, line in base_clauses.items():
            self.assertEqual(candidate_clauses[label], line)
        self.assertEqual(set(candidate_clauses) - set(base_clauses), {"PRECHANGE_REVIEW", "REVIEW_SOURCE_AUTHORITY"})

    def test_source_authority_is_producer_scoped(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text()
        for fragment in (
            "packet_projection_set :=",
            "reviewer_observation_set :=",
            "root_operation_set :=",
            "root_review_read_allowed(target) :=",
            "reviewer_read_allowed(target) :=",
            "container全体、複数ownerのtarget",
            "受領後の無視、非admission",
            "DECISION_BOUNDARYの共同発行",
        ):
            self.assertIn(fragment, text)

    def test_no_case_mapping_or_success_procedure(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text()
        for fragment in ("TC-ADR", "OBS-", "SCOPE-", "consumer_inventory", "consumer_contracts", "Candidate220", "jq", "先にinventory"):
            self.assertNotIn(fragment, text)

    def test_snapshot_contains_candidate(self) -> None:
        snapshot = json.loads((ROOT / "tests/bundle_identity_snapshot.json").read_text())
        self.assertEqual(snapshot["bundle_sha256"]["candidates/the-caption-3ce91a4-review-source-authority-closure-r1"], "4e40da5f16466226a053b5bcc5efa31c5600219f4117a8bc0635c3c5a0196562")
        self.assertEqual(snapshot["count"], len(snapshot["bundle_sha256"]))

    def test_registered_result_and_stop_gates(self) -> None:
        result = json.loads(RESULT.read_text())
        quality = json.loads(QUALITY_AUDIT.read_text())
        mechanism = json.loads(MECHANISM_AUDIT.read_text())
        self.assertEqual(result["result_id"], "4511cbb39fb04bb2ad47d6219a12cf7e")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(result["median"]["quality_score"], 75.0)
        self.assertEqual(quality["status"], "quality_failed_stopped")
        self.assertEqual(quality["quality_score_counts"], {"4": 29, "1": 16})
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["root_reviewer_owned_preread_count"], 20)
        self.assertEqual(mechanism["root_mixed_owner_admission_count"], 20)
        self.assertFalse(mechanism["mechanism_gate_passed"])


if __name__ == "__main__":
    unittest.main()

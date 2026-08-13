from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-input-carrier-ownership-r1"
DESIGN = ROOT / "docs/candidate218-review-input-carrier-ownership-design.md"
DIRECTION = ROOT / "docs/candidate218-review-input-carrier-ownership-direction-audit.md"
AUDIT = ROOT / "docs/candidate218-review-input-carrier-ownership-implementation-audit.md"
RESULT = ROOT / "evaluations/results/b2fb3f264739493bb5a3985829161701.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5-mechanism-audit-r1.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5_2026-08-14.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate218Test(unittest.TestCase):
    def test_direct_c147_child_changes_only_root_agents(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": base["prompt_identity"],
            },
        )
        self.assertEqual(
            candidate["bundle_sha256"],
            "04c2e670eabf659b24139429246ad1e640e5162297b4fd999a0565efd8762f73",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_existing_c147_clauses_are_unchanged(self) -> None:
        base = clauses((BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = clauses((CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(set(candidate) - set(base), {"PRECHANGE_REVIEW", "REVIEW_INPUT_OWNERSHIP"})
        self.assertEqual(set(base) - set(candidate), set())
        for label in base:
            self.assertEqual(candidate[label], base[label], label)

    def test_carrier_ownership_is_fixed_without_case_mapping(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "REVIEW_INPUT_OWNERSHIP",
            "repository current valueを取得する前",
            "root_control | packet_carried | reviewer_observation | unavailable",
            "exactly one",
            "root_review_input_admissible(result)",
            "root-ownedとreviewer-ownedのprojectionを同時に含むcontainer result",
            "whole-container fallback",
            "root_control`はroutingだけ",
            "同じvalue identityをroot resultとreviewer observationへ二重bindせず",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "TC-ADR",
            "OBS-",
            "SCOPE-",
            "consumer_inventory",
            "consumer_contracts",
            "Candidate217",
            "先にinventory",
        ):
            self.assertNotIn(prohibited, text)

    def test_creation_gate_and_static_audit_are_fixed(self) -> None:
        self.assertIn("creation_gate_fixed", DESIGN.read_text(encoding="utf-8"))
        direction = DIRECTION.read_text(encoding="utf-8")
        self.assertIn("direction_passed_at_creation", direction)
        self.assertIn("direction_assumption_refuted_by_evaluation", direction)
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("static_verification_passed", audit)
        self.assertIn("quality_failed", audit)

    def test_evaluation_result_and_ownership_audits_are_fixed(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "b2fb3f264739493bb5a3985829161701")
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(quality["valid_run_count"], 45)
        self.assertEqual(quality["quality_score_counts"], {"1": 2, "4": 43})
        self.assertEqual(quality["terminal_match_count"], 43)
        self.assertEqual(quality["artifact_boundary_match_count"], 45)
        self.assertEqual(mechanism["root_mixed_owner_admission_count"], 20)
        self.assertEqual(mechanism["duplicate_root_reviewer_consumption_count"], 19)
        self.assertEqual(mechanism["required_direct_observation_match_count"], 19)
        self.assertEqual(mechanism["adr03_to_adr06_terminal_match_count"], 18)
        self.assertEqual(mechanism["adr07_exact_paired_only_count"], 2)
        self.assertEqual(mechanism["adr09_exact_paired_only_count"], 1)
        self.assertEqual(mechanism["unrequired_reviewer_start_count"], 7)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        report = RESULT_REPORT.read_text(encoding="utf-8")
        self.assertIn("mixed-owner", report)
        self.assertIn("evidence invocationへowner", report)
        self.assertIn("quality_failed / mechanism_failed / stopped", report)


if __name__ == "__main__":
    unittest.main()

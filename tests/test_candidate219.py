from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-evidence-consumer-admission-r1"
DESIGN = ROOT / "docs/candidate219-review-evidence-consumer-admission-design.md"
DIRECTION = ROOT / "docs/candidate219-review-evidence-consumer-admission-direction-audit.md"
AUDIT = ROOT / "docs/candidate219-review-evidence-consumer-admission-implementation-audit.md"
RESULT = ROOT / "evaluations/results/9834373597cb47b5b469f1d15962bf04.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate219-review-evidence-consumer-admission-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate219-review-evidence-consumer-admission-adr9-r2-n5-mechanism-audit-r1.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate219-review-evidence-consumer-admission-adr9-r2-n5_2026-08-14.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate219Test(unittest.TestCase):
    def test_bundle_identity_and_direct_base(self) -> None:
        manifest = verify_bundle(CANDIDATE)
        self.assertEqual(
            manifest["bundle_sha256"],
            "5ec4728576b24b8dd4aceb45903cae6f9fe0f46b58bf382a3cbe4c50cdfabf95",
        )
        self.assertEqual(
            manifest["content_relation"],
            {
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": "the-caption-3ce91a4-result-effect-scope-r1",
                "changed_targets": ["AGENTS.md"],
            },
        )

    def test_only_root_agents_differs(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(set(base_files), set(candidate_files))
        changed = [target for target in base_files if base_files[target] != candidate_files[target]]
        self.assertEqual(changed, ["AGENTS.md"])

    def test_c147_clauses_are_verbatim_and_only_two_are_added(self) -> None:
        base_text = (BASE / "files/AGENTS.md.txt").read_text()
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text()
        base_clauses = clauses(base_text)
        candidate_clauses = clauses(candidate_text)
        self.assertEqual(len(base_clauses), 13)
        for label, line in base_clauses.items():
            self.assertEqual(candidate_clauses[label], line)
        self.assertEqual(
            set(candidate_clauses) - set(base_clauses),
            {"PRECHANGE_REVIEW", "REVIEW_EVIDENCE_ADMISSION"},
        )

    def test_consumer_bound_issuance_is_explicit(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text()
        required = (
            "review_required :=",
            "required review propositionまたはscope obligationがnonempty",
            "review_evidence_ticket :=",
            "review_evidence_consumer_ready :=",
            "consumer_projection_closed(ticket)",
            "必須AND",
            "result envelope",
            "別consumer",
            "受領後の非admission",
            "packet-carried projectionを再取得しない",
            "support済みkindをそのmissingで失効させない",
        )
        for fragment in required:
            self.assertIn(fragment, text)

    def test_no_case_mapping_or_success_procedure_is_encoded(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text()
        forbidden = (
            "TC-ADR",
            "OBS-",
            "SCOPE-",
            "consumer_inventory",
            "consumer_contracts",
            "Candidate218",
            "jq",
            "先にinventory",
        )
        for fragment in forbidden:
            self.assertNotIn(fragment, text)

    def test_design_records_preserve_state_boundaries(self) -> None:
        design = DESIGN.read_text()
        direction = DIRECTION.read_text()
        audit = AUDIT.read_text()
        self.assertIn("`creation_gate_fixed`", design)
        self.assertIn("`direction_passed`", direction)
        self.assertIn("`direction_assumption_refuted_by_evaluation`", direction)
        self.assertIn("`candidate_created`", audit)
        self.assertIn("`static_verification_passed`", audit)
        self.assertIn("`quality_failed`", audit)

    def test_identity_snapshot_contains_candidate(self) -> None:
        snapshot = json.loads((ROOT / "tests/bundle_identity_snapshot.json").read_text())
        self.assertEqual(
            snapshot["bundle_sha256"]["candidates/the-caption-3ce91a4-review-evidence-consumer-admission-r1"],
            "5ec4728576b24b8dd4aceb45903cae6f9fe0f46b58bf382a3cbe4c50cdfabf95",
        )
        self.assertEqual(snapshot["count"], len(snapshot["bundle_sha256"]))

    def test_evaluation_result_and_consumer_admission_audits_are_fixed(self) -> None:
        result = json.loads(RESULT.read_text())
        quality = json.loads(QUALITY_AUDIT.read_text())
        mechanism = json.loads(MECHANISM_AUDIT.read_text())
        self.assertEqual(result["result_id"], "9834373597cb47b5b469f1d15962bf04")
        self.assertEqual(result["compatibility_key"], "1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3")
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(quality["valid_run_count"], 45)
        self.assertEqual(quality["quality_score_counts"], {"1": 4, "4": 41})
        self.assertEqual(quality["terminal_match_count"], 41)
        self.assertEqual(quality["artifact_boundary_match_count"], 45)
        self.assertEqual(mechanism["root_mixed_owner_admission_count"], 20)
        self.assertEqual(mechanism["duplicate_root_reviewer_consumption_count"], 13)
        self.assertEqual(mechanism["required_direct_observation_match_count"], 13)
        self.assertEqual(mechanism["adr03_to_adr06_terminal_match_count"], 16)
        self.assertEqual(mechanism["adr07_exact_paired_only_count"], 0)
        self.assertEqual(mechanism["adr09_exact_paired_only_count"], 4)
        self.assertEqual(mechanism["unrequired_reviewer_start_count"], 9)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        report = RESULT_REPORT.read_text()
        self.assertIn("stdout", report)
        self.assertIn("model-visible", report)
        self.assertIn("quality_failed / mechanism_failed / stopped", report)


if __name__ == "__main__":
    unittest.main()

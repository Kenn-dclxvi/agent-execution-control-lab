from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-minimal-operation-selection-r1"
DESIGN = ROOT / "docs/post-candidate197-c147-minimal-operation-selection-design.md"
DIRECTION_REVIEW = ROOT / "docs/post-candidate197-c147-minimal-operation-selection-direction-review.md"
IMPLEMENTATION_AUDIT = ROOT / "docs/candidate198-minimal-operation-selection-implementation-audit.md"
EVALUATION_DESIGN = ROOT / "docs/candidate198-minimal-operation-selection-adr9-r2-n5-evaluation-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate198-minimal-operation-selection-adr9-r2-medium-m24-n5-cli0146.json"
PREPARATION_AUDIT = ROOT / "docs/candidate198-minimal-operation-selection-adr9-r2-n5-execution-preparation-audit.md"
CORRECTED_RESULT = ROOT / "evaluations/results/981c0c346cdb4491ab15b789b0946a43.json"
INITIAL_RESULT = ROOT / "evaluations/results/d891e8aec41c45478362a7ced926d393.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate198-minimal-operation-selection-adr9-r2-n5-quality-audit-r2.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate198-minimal-operation-selection-adr9-r2-n5-mechanism-audit-r2.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate198-minimal-operation-selection-adr9-r2-n5_2026-08-13.md"


def clauses(text: str) -> dict[str, str]:
    parts: dict[str, str] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            current = line[2:].split(":", 1)[0]
            parts[current] = line
        elif current:
            parts[current] += "\n" + line
    return parts


class Candidate198Test(unittest.TestCase):
    def test_c147_direct_child_replaces_two_clauses_and_adds_one(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": parent["prompt_identity"],
            },
        )
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(
            candidate["bundle_sha256"],
            "e03fa019cfdee38e68e541f34b3583a4de294ba77e735c7787052bdb0036b89c",
        )

        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

        parent_clauses = clauses((PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_clauses = clauses(candidate_text)
        self.assertEqual(
            list(candidate_clauses),
            [
                "SPEC", "PRODUCER", "TERMINAL", "CONTEXT", "EVIDENCE_GATE",
                "OWNER_ROLE", "ROOT", "INDEPENDENCE", "DECISION_BOUNDARY",
                "VALIDATION_CLOSURE", "VALIDATION_PLAN", "METHOD", "RECOVERY",
                "REVIEW_SELECTION",
            ],
        )
        for label in parent_clauses:
            if label not in {"SPEC", "DECISION_BOUNDARY"}:
                self.assertEqual(candidate_clauses[label], parent_clauses[label], label)

        for required in (
            "現在受領済みの明示user input",
            "operation_needed :=",
            "包含関係上の最小集合",
            "同一model step",
            "required review scope identity",
            "new_review_needed :=",
            "reviewerと対応変更を選ばず",
        ):
            self.assertIn(required, candidate_text)
        for rejected in (
            "OPERATION_TICKET", "PREDECESSOR_EDGE", "method receipt",
            "observation ledger", "ADJUDICATION_MATERIALIZATION", "DISPATCH_ADMISSION",
            "DISPATCH_TRANSITION", "dispatch_frontier", "terminal-proof-obligation",
            "Candidate191", "Candidate197", "Standard14", "ADR9",
        ):
            self.assertNotIn(rejected, candidate_text)

    def test_design_review_and_audit_fix_static_boundary(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        review = DIRECTION_REVIEW.read_text(encoding="utf-8")
        audit = IMPLEMENTATION_AUDIT.read_text(encoding="utf-8")
        for status in ("known_cases_23_classified", "unclassified_0"):
            self.assertIn(status, design)
        for status in ("reviewed_states_18", "blocking_counterexamples_0"):
            self.assertIn(status, review)
        for status in (
            "candidate_created / static_verification_passed / not_evaluated",
            "C147の`SPEC`と`DECISION_BOUNDARY`だけを置換",
            "TPOは導入していない",
        ):
            self.assertIn(status, audit)

    def test_evaluation_design_profile_and_preflight_preserve_fixed_gate(self) -> None:
        evaluation_design = EVALUATION_DESIGN.read_text(encoding="utf-8")
        for status in (
            "actual_trial_inputs_9_checked",
            "private_oracles_9_checked",
            "quality_oracle_unchanged",
            "mechanism_predicates_frozen",
            "comparison_preflight_ready",
            "authorized_45",
            "Standard14_not_started",
        ):
            self.assertIn(status, evaluation_design)
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-minimal-operation-selection-r1",
                "revision": "r1",
                "bundle_sha256": "e03fa019cfdee38e68e541f34b3583a4de294ba77e735c7787052bdb0036b89c",
            },
        )
        preparation = PREPARATION_AUDIT.read_text(encoding="utf-8")
        for status in (
            "candidate198_existing_0",
            "candidate198_missing_45",
            "authorized_45",
            "issued_0",
            "comparison_preflight_ready",
        ):
            self.assertIn(status, preparation)

    def test_corrected_result_preserves_quality_and_mechanism_failures(self) -> None:
        corrected = json.loads(CORRECTED_RESULT.read_text(encoding="utf-8"))
        initial = json.loads(INITIAL_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        report = RESULT_REPORT.read_text(encoding="utf-8")
        self.assertEqual(corrected["result_id"], "981c0c346cdb4491ab15b789b0946a43")
        self.assertEqual(corrected["result_content_sha256"], "8a18d4600cc9f22478450d5b834510abb169dfede8695adbf4e8255a065d84ed")
        self.assertEqual(initial["result_id"], "d891e8aec41c45478362a7ced926d393")
        self.assertEqual(len(corrected["case_results"]), 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 26, "1": 19})
        self.assertEqual(quality["status"], "quality_failed_stopped")
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["reviewer_cardinality_match_count"], 32)
        self.assertEqual(mechanism["review_result_admission_match_count"], 27)
        self.assertEqual(mechanism["review_result_effect_match_count"], 26)
        self.assertEqual(mechanism["initial_identity_only_count"], 35)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        for status in (
            "quality_failed / mechanism_failed / stopped / Standard14_not_started",
            "c147_direct_base_retained",
            "candidate198_not_parent",
        ):
            self.assertIn(status, report)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-structured-prechange-review-r1"
DESIGN = ROOT / "docs/post-candidate198-c147-structured-prechange-review-design.md"
DIRECTION_REVIEW = ROOT / "docs/post-candidate198-c147-structured-prechange-review-direction-review.md"
IMPLEMENTATION_AUDIT = ROOT / "docs/candidate199-structured-prechange-review-implementation-audit.md"
EVALUATION_DESIGN = ROOT / "docs/candidate199-structured-prechange-review-adr9-r2-n5-evaluation-design.md"
PREPARATION_AUDIT = ROOT / "docs/candidate199-structured-prechange-review-adr9-r2-n5-execution-preparation-audit.md"
RESULT_RECORD = ROOT / "evaluations/results/candidate199-structured-prechange-review-adr9-r2-n5_2026-08-13.md"
REGISTERED_RESULT = ROOT / "evaluations/results/7751ae31151d48dd87a75b2a71a8a527.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate199-structured-prechange-review-adr9-r2-n5-quality-audit-r2.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate199-structured-prechange-review-adr9-r2-n5-mechanism-audit-r5.json"
PROFILE = ROOT / "evaluations/profiles/candidate199-structured-prechange-review-adr9-r2-medium-m24-n5-cli0146.json"


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


class Candidate199Test(unittest.TestCase):
    def test_direct_child_changes_only_root_agents(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": parent["prompt_identity"],
            },
        )
        self.assertEqual(
            candidate["bundle_sha256"],
            "b2bc74e96f9ebf64bf977f766ec25ed1b429663acee59b64bfe570a9f91d654a",
        )
        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

    def test_prompt_has_chronological_boundaries_and_preserves_other_clauses(self) -> None:
        parent_text = (PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        parent_clauses = clauses(parent_text)
        candidate_clauses = clauses(candidate_text)
        self.assertEqual(len(parent_clauses), 13)
        self.assertEqual(len(candidate_clauses), 15)
        self.assertIn("START_BOUNDARY", candidate_clauses)
        self.assertIn("PRECHANGE_REVIEW", candidate_clauses)
        for label, value in parent_clauses.items():
            if label != "EVIDENCE_GATE":
                self.assertEqual(candidate_clauses[label], value, label)
        self.assertIn("prechange_transition :=", candidate_clauses["EVIDENCE_GATE"])
        self.assertNotIn("次にartifact変更を発行する", candidate_clauses["EVIDENCE_GATE"])

    def test_prompt_has_fixed_review_responsibilities_without_historical_inputs(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for required in (
            "initial_issue_set :=",
            "HEAD / HEAD^ / HEAD^^",
            "explicit_prechange_review_fixed :=",
            "APPLICABILITY / EXECUTION_PERMISSION / OPERATION_READY / PACKET / OBSERVATION / JUDGEMENT / RESULT_ADMISSION / CHANGE_EFFECT",
            "counterexample_result_ready :=",
            "no_counterexample_result_ready :=",
            "unavailable_result_ready :=",
            "current_review_result_admissible :=",
            "保存済みprior review resultは扱わない",
        ):
            self.assertIn(required, text)
        for rejected in (
            "Candidate175",
            "Candidate191",
            "Candidate198",
            "TC-ADR",
            "private oracle",
            "selected_operations",
            "REVIEW_SELECTION",
        ):
            self.assertNotIn(rejected, text)

    def test_design_and_audits_match_candidate_state(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        direction = DIRECTION_REVIEW.read_text(encoding="utf-8")
        audit = IMPLEMENTATION_AUDIT.read_text(encoding="utf-8")
        self.assertIn("candidate_implementation_allowed", direction)
        self.assertIn("unresolved_blocking_counterexamples_0", direction)
        self.assertIn("Candidate199", audit)
        self.assertIn("static_verification_passed / not_evaluated", audit)
        self.assertIn("ADR9_then_Standard14_only", design)

    def test_adr9_design_freezes_candidate_only_first_gate(self) -> None:
        text = EVALUATION_DESIGN.read_text(encoding="utf-8")
        for required in (
            "evaluated / valid_45 / quality_failed / mechanism_failed / stopped / Standard14_not_started",
            "TC-ADR01`〜`TC-ADR09`、各5件、合計45件",
            "Score `4 = 45 / 45`",
            "最初の実repository operationはTaskSpecが要求する`HEAD / HEAD^ / HEAD^^`三値identity確認一件だけ",
            "current reviewerを一件ずつ30 / 30起動",
            "required command 15 / 15成功",
            "candidate_only_first_gate",
            "Standard14_not_started",
        ):
            self.assertIn(required, text)
        self.assertNotIn("slots_issued_45", text)

    def test_execution_preparation_authorizes_only_missing_candidate_slots(self) -> None:
        text = PREPARATION_AUDIT.read_text(encoding="utf-8")
        for required in (
            "comparison_preflight_ready / forty_five_slots_authorized / issued_zero",
            "reference result: `981c0c346cdb4491ab15b789b0946a43`",
            "Candidate199 pool: `c7a7e594226c484bf56c459de6510bb81637bad5c46ed0e7996bd85a1f28f0a6`",
            "candidate199_missing_45 / authorized_45 / issued_0",
        ):
            self.assertIn(required, text)

    def test_adr9_profile_changes_only_prompt_identity_from_candidate198(self) -> None:
        import json

        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        reference_path = ROOT / "evaluations/profiles/candidate198-minimal-operation-selection-adr9-r2-medium-m24-n5-cli0146.json"
        reference = json.loads(reference_path.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["profile_id"],
            "candidate199-structured-prechange-review-adr9-r2-medium-m24-n5-cli0146",
        )
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-structured-prechange-review-r1",
                "revision": "r1",
                "bundle_sha256": "b2bc74e96f9ebf64bf977f766ec25ed1b429663acee59b64bfe570a9f91d654a",
            },
        )
        for key in ("evaluation_set", "cases", "iterations", "comparison_conditions", "execution"):
            self.assertEqual(profile[key], reference[key], key)

    def test_registered_result_stops_after_single_forbidden_input_failure(self) -> None:
        import json

        result = json.loads(REGISTERED_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        record = RESULT_RECORD.read_text(encoding="utf-8")
        self.assertEqual(result["result_id"], "7751ae31151d48dd87a75b2a71a8a527")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 44, "1": 1})
        self.assertEqual(quality["terminal_match_count"], 45)
        self.assertEqual(quality["forbidden_canary_delivery_count"], 1)
        self.assertEqual(mechanism["reviewer_cardinality_match_count"], 45)
        self.assertEqual(mechanism["review_result_admission_match_count"], 45)
        self.assertEqual(mechanism["review_result_effect_match_count"], 45)
        self.assertEqual(mechanism["initial_identity_only_count"], 45)
        self.assertEqual(mechanism["forbidden_input_boundary_match_count"], 44)
        self.assertIn("Standard14_not_started", record)


if __name__ == "__main__":
    unittest.main()

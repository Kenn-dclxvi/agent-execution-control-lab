from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-projected-review-read-closure-r1"
DESIGN = ROOT / "docs/post-candidate199-c147-projected-review-read-closure-design.md"
DIRECTION_REVIEW = ROOT / "docs/post-candidate199-c147-projected-review-read-closure-direction-review.md"
IMPLEMENTATION_AUDIT = ROOT / "docs/candidate200-projected-review-read-closure-implementation-audit.md"
EVALUATION_DESIGN = ROOT / "docs/candidate200-projected-review-read-closure-adr9-r2-n5-evaluation-design.md"
PREPARATION_AUDIT = ROOT / "docs/candidate200-projected-review-read-closure-adr9-r2-n5-execution-preparation-audit.md"
PROFILE = ROOT / "evaluations/profiles/candidate200-projected-review-read-closure-adr9-r2-medium-m24-n5-cli0146.json"
RESULT_RECORD = ROOT / "evaluations/results/candidate200-projected-review-read-closure-adr9-r2-n5_2026-08-13.md"
REGISTERED_RESULT = ROOT / "evaluations/results/2c099aff32054c8288070e59a52464e0.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate200-projected-review-read-closure-adr9-r2-n5-quality-audit-r2.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate200-projected-review-read-closure-adr9-r2-n5-mechanism-audit-r7.json"


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


class Candidate200Test(unittest.TestCase):
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
            "f2aff1f0a24594eaa3fca0a5d9584e9ad24e339b0e7d2eeca0e1c02b49839f60",
        )
        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

    def test_prompt_preserves_c147_except_fixed_transition(self) -> None:
        parent = clauses((PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = clauses((CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(len(parent), 13)
        self.assertEqual(len(candidate), 15)
        self.assertIn("START_BOUNDARY", candidate)
        self.assertIn("PRECHANGE_REVIEW", candidate)
        for label, value in parent.items():
            if label != "EVIDENCE_GATE":
                self.assertEqual(candidate[label], value, label)
        self.assertIn("prechange_transition :=", candidate["EVIDENCE_GATE"])
        self.assertNotIn("次にartifact変更を発行する", candidate["EVIDENCE_GATE"])

    def test_prompt_has_projected_read_closure_and_nine_responsibilities(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for required in (
            "APPLICABILITY / EXECUTION_PERMISSION / OPERATION_READY / PACKET / READ_CLOSURE / OBSERVATION / JUDGEMENT / RESULT_ADMISSION / CHANGE_EFFECT",
            "packet_projection_ready :=",
            "projected_source_closed(source) :=",
            "reviewer_observation_read_set :=",
            "reviewer_read_admissible(read) :=",
            "rootはそのreviewer-owned observation targetを起動前にreadまたはpacketへ代入しない",
            "同一invocationの全targetが条件を満たす",
            "保存済みprior review resultは扱わない",
        ):
            self.assertIn(required, text)
        for rejected in (
            "Candidate175",
            "Candidate191",
            "Candidate199",
            "TC-ADR",
            "private oracle",
            "selected_operations",
            "REVIEW_SELECTION",
        ):
            self.assertNotIn(rejected, text)

    def test_design_and_audit_match_current_state(self) -> None:
        self.assertIn("candidate_implementation_allowed", DIRECTION_REVIEW.read_text(encoding="utf-8"))
        self.assertIn("ADR9_then_Standard14_only", DESIGN.read_text(encoding="utf-8"))
        audit = IMPLEMENTATION_AUDIT.read_text(encoding="utf-8")
        self.assertIn("Candidate200", audit)
        self.assertIn("static_verification_passed / not_evaluated", audit)

    def test_adr9_design_freezes_read_closure_gate(self) -> None:
        text = EVALUATION_DESIGN.read_text(encoding="utf-8")
        for required in (
            "TC-ADR01`〜`TC-ADR09`、各5件、合計45件",
            "Score `4 = 45 / 45`",
            "reviewerによるclosed sourceの全体read、部分read、field選択、hashおよび存在確認は0件",
            "rootによるreviewer-owned observation targetの起動前readは0件",
            "ADR06のforbidden canaryがreviewer packet、tool result、responseまたはrootへのreview resultへ配送される件数は0 / 5",
            "candidate_only_first_gate",
            "Standard14_not_started",
        ):
            self.assertIn(required, text)

    def test_profile_changes_only_prompt_identity_from_candidate199(self) -> None:
        import json

        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        reference = json.loads(
            (ROOT / "evaluations/profiles/candidate199-structured-prechange-review-adr9-r2-medium-m24-n5-cli0146.json").read_text(encoding="utf-8")
        )
        self.assertEqual(profile["profile_id"], "candidate200-projected-review-read-closure-adr9-r2-medium-m24-n5-cli0146")
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-projected-review-read-closure-r1",
                "revision": "r1",
                "bundle_sha256": "f2aff1f0a24594eaa3fca0a5d9584e9ad24e339b0e7d2eeca0e1c02b49839f60",
            },
        )
        for key in ("evaluation_set", "cases", "iterations", "comparison_conditions", "execution"):
            self.assertEqual(profile[key], reference[key], key)

    def test_preparation_authorizes_only_candidate_slots(self) -> None:
        text = PREPARATION_AUDIT.read_text(encoding="utf-8")
        for required in (
            "comparison_preflight_ready / forty_five_slots_authorized / issued_zero",
            "reference result: `7751ae31151d48dd87a75b2a71a8a527`",
            "Candidate200 pool: `e352b6f4ee72d434818ac1dcdf52b4b83f3d767d809280486860c782fa4f4ac0`",
            "candidate200_missing_45 / authorized_45 / issued_0",
        ):
            self.assertIn(required, text)

    def test_registered_result_stops_after_read_closure_overconstraint(self) -> None:
        import json

        result = json.loads(REGISTERED_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        record = RESULT_RECORD.read_text(encoding="utf-8")
        self.assertEqual(result["result_id"], "2c099aff32054c8288070e59a52464e0")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 30, "1": 15})
        self.assertEqual(quality["terminal_match_count"], 30)
        self.assertEqual(quality["forbidden_canary_delivery_count"], 0)
        self.assertEqual(mechanism["reviewer_cardinality_match_count"], 31)
        self.assertEqual(mechanism["reviewer_missing_count"], 14)
        self.assertEqual(mechanism["review_result_admission_match_count"], 28)
        self.assertEqual(mechanism["initial_identity_only_count"], 45)
        self.assertEqual(mechanism["root_reviewer_observation_preread_free_count"], 45)
        self.assertEqual(mechanism["reviewer_exact_read_set_match_count"], 16)
        self.assertEqual(mechanism["reviewer_closed_source_read_count"], 0)
        self.assertEqual(mechanism["reviewer_mixed_read_count"], 0)
        self.assertIn("Standard14_not_started", record)


if __name__ == "__main__":
    unittest.main()

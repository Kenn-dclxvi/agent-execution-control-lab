from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-certificate-gated-review-read-r1"
DESIGN = ROOT / "docs/post-candidate202-c147-certificate-gated-review-read-design.md"
DIRECTION = ROOT / "docs/post-candidate202-c147-certificate-gated-review-read-direction-review.md"
AUDIT = ROOT / "docs/candidate203-certificate-gated-review-read-implementation-audit.md"
PROFILE = ROOT / "evaluations/profiles/candidate203-certificate-gated-review-read-adr9-r2-medium-m24-n5-cli0146.json"
RESULT = ROOT / "evaluations/results/e491ba8149374cff8ebb74cf3d031414.json"
QUALITY = ROOT / "evaluations/results/candidate203-certificate-gated-review-read-adr9-r2-n5-quality-audit-r2.json"
MECHANISM = ROOT / "evaluations/results/candidate203-certificate-gated-review-read-adr9-r2-n5-mechanism-audit-r3.json"
RESULT_DOC = ROOT / "evaluations/results/candidate203-certificate-gated-review-read-adr9-r2-n5_2026-08-13.md"
CAUSAL = ROOT / "docs/candidate203-m5-causal-analysis.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            current = line[2:].split(":", 1)[0]
            result[current] = line
        elif current:
            result[current] += "\n" + line
    return result


class Candidate203Test(unittest.TestCase):
    def test_direct_child_changes_only_root_agents(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(candidate["bundle_sha256"], "4803ffe1e020f339dcb0405601398d236bebb60fed11c656b7f3ad7909cd184d")
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": parent["prompt_identity"],
        })
        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

    def test_prompt_preserves_c147_and_adds_review_read_transition(self) -> None:
        parent = clauses((PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = clauses(text)
        self.assertEqual(len(parent), 13)
        self.assertEqual(len(candidate), 15)
        for label, value in parent.items():
            self.assertEqual(candidate[label].rstrip(), value.rstrip(), label)
        for required in (
            "PRECHANGE_REVIEW",
            "REVIEW_READ_TRANSITION",
            "root_projectable :=",
            "reviewer_direct :=",
            "projected_counterexample_established :=",
            "review_direct_read_consumer_ready(entry) :=",
            "同じmodel responseにtool callを置かず",
            "現在未解決のresult-kind predicateを持たないreadは発行しない",
            "criterion owner語列だけではreview operationまたはproducerを起動しない",
            "key / null / existence状態も配送しない",
            "no_counterexample_found",
        ):
            self.assertIn(required, text)
        for forbidden in ("Candidate175", "Candidate202", "TC-ADR", "private oracle", "START_BOUNDARY", "DESIGN_ADMISSION"):
            self.assertNotIn(forbidden, text)

    def test_design_direction_and_audit_are_complete(self) -> None:
        self.assertIn("M2_complete", DESIGN.read_text(encoding="utf-8"))
        self.assertIn("unresolved_blocking_counterexamples_0", DIRECTION.read_text(encoding="utf-8"))
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("static_verification_passed", audit)
        self.assertIn("clauses_preserved_13_of_13", audit)
        self.assertIn("not_evaluated", audit)

    def test_profile_matches_candidate_and_c202_conditions(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        reference = json.loads((ROOT / "evaluations/profiles/candidate202-review-admission-routing-receipt-adr9-r2-medium-m24-n5-cli0146.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["prompt_set_identity"], {
            "name": "the-caption-3ce91a4-certificate-gated-review-read-r1",
            "revision": "r1",
            "bundle_sha256": "4803ffe1e020f339dcb0405601398d236bebb60fed11c656b7f3ad7909cd184d",
        })
        for key in ("evaluation_set", "cases", "iterations", "comparison_conditions", "execution"):
            self.assertEqual(profile[key], reference[key], key)

    def test_adr9_quality_passes_and_mechanism_stops_standard14(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "e491ba8149374cff8ebb74cf3d031414")
        self.assertEqual(result["compatibility_key"], "1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3")
        self.assertEqual(result["median"], {
            "elapsed_seconds": 709.2047075390001,
            "quality_score": 100.0,
            "total_tokens": 1131455,
        })
        self.assertEqual(quality["status"], "quality_passed")
        self.assertEqual(quality["quality_score_counts"], {"4": 45})
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["required_reviewer_cardinality_match_count"], 30)
        self.assertEqual(mechanism["prohibited_reviewer_violation_count"], 8)
        self.assertEqual(mechanism["projection_receipt_acknowledgement_exact_count"], 22)
        self.assertEqual(mechanism["counterexample_certificate_priority_violation_count"], 2)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        self.assertIn("Standard14_not_started", RESULT_DOC.read_text(encoding="utf-8"))
        self.assertIn("applicability_failed_8_of_15", CAUSAL.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

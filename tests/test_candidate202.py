from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-admission-routing-receipt-r1"
DESIGN = ROOT / "docs/post-candidate201-c147-review-admission-routing-receipt-design.md"
DIRECTION = ROOT / "docs/post-candidate201-c147-review-admission-routing-receipt-direction-review.md"
AUDIT = ROOT / "docs/candidate202-review-admission-routing-receipt-implementation-audit.md"
EVALUATION = ROOT / "docs/candidate202-review-admission-routing-receipt-adr9-r2-n5-evaluation-design.md"
PREPARATION = ROOT / "docs/candidate202-review-admission-routing-receipt-adr9-r2-n5-execution-preparation-audit.md"
PROFILE = ROOT / "evaluations/profiles/candidate202-review-admission-routing-receipt-adr9-r2-medium-m24-n5-cli0146.json"
RESULT = ROOT / "evaluations/results/0a509a780f0e40ae857ea602f00ff89b.json"
QUALITY = ROOT / "evaluations/results/candidate202-review-admission-routing-receipt-adr9-r2-n5-quality-audit-r2.json"
MECHANISM = ROOT / "evaluations/results/candidate202-review-admission-routing-receipt-adr9-r2-n5-mechanism-audit-r2.json"
RESULT_DOC = ROOT / "evaluations/results/candidate202-review-admission-routing-receipt-adr9-r2-n5_2026-08-13.md"
CAUSAL = ROOT / "docs/candidate202-m5-causal-analysis.md"
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate202-review-admission-routing-receipt-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
STANDARD14_RESULT = ROOT / "evaluations/results/08c295a44f7b4a70873c7fc1c503f9e8.json"
STANDARD14_QUALITY = ROOT / "evaluations/results/candidate202-review-admission-routing-receipt-standard14-n5-quality-audit-r1.json"
STANDARD14_MECHANISM = ROOT / "evaluations/results/candidate202-review-admission-routing-receipt-standard14-n5-mechanism-audit-r1.json"
STANDARD14_COMPARISON = ROOT / "evaluations/results/candidate202-review-admission-routing-receipt-standard14-n5-comparison-c175-r1.json"
STANDARD14_RESULT_DOC = ROOT / "evaluations/results/candidate202-review-admission-routing-receipt-standard14-n5_2026-08-13.md"


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


class Candidate202Test(unittest.TestCase):
    def test_direct_child_changes_only_root_agents(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(candidate["bundle_sha256"], "425208248292cd147e6a005d73912e5268856c3ab34e2ae14ad4b39f1893cca4")
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

    def test_prompt_has_routing_receipt_and_preserves_c147_core(self) -> None:
        parent = clauses((PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = clauses(text)
        self.assertEqual(len(parent), 13)
        self.assertEqual(len(candidate), 15)
        for label, value in parent.items():
            if label not in {"PRODUCER", "OWNER_ROLE"}:
                self.assertEqual(candidate[label].rstrip(), value.rstrip(), label)
        for required in (
            "START_BOUNDARY",
            "DESIGN_ADMISSION",
            "root_projectable(entry) :=",
            "reviewer_direct(entry) :=",
            "review_input_routing_complete :=",
            "owner fieldを入力へ要求しない",
            "projection_receipt :=",
            "final resultで全receipt identityを過不足なく列挙",
            "counterexample_certificate :=",
            "集合外missing / unreadable / receipt欠落で失効させず",
        ):
            self.assertIn(required, text)
        for forbidden in ("Candidate175", "Candidate201", "TC-ADR", "private oracle"):
            self.assertNotIn(forbidden, text)

    def test_design_direction_and_audit_are_complete(self) -> None:
        self.assertIn("M2_complete", DESIGN.read_text(encoding="utf-8"))
        self.assertIn("unresolved_blocking_counterexamples_0", DIRECTION.read_text(encoding="utf-8"))
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("static_verification_passed", audit)
        self.assertIn("not_evaluated", audit)

    def test_profile_and_evaluation_gate_are_frozen(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        reference = json.loads((ROOT / "evaluations/profiles/candidate201-review-input-partition-adr9-r2-medium-m24-n5-cli0146.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["profile_id"], "candidate202-review-admission-routing-receipt-adr9-r2-medium-m24-n5-cli0146")
        self.assertEqual(profile["prompt_set_identity"], {
            "name": "the-caption-3ce91a4-review-admission-routing-receipt-r1",
            "revision": "r1",
            "bundle_sha256": "425208248292cd147e6a005d73912e5268856c3ab34e2ae14ad4b39f1893cca4",
        })
        for key in ("evaluation_set", "cases", "iterations", "comparison_conditions", "execution"):
            self.assertEqual(profile[key], reference[key], key)
        evaluation = EVALUATION.read_text(encoding="utf-8")
        for required in (
            "Score `4 = 45 / 45`",
            "reviewer finalはprojection receipt identityを過不足なく30 / 30 acknowledgement",
            "counterexample certificate成立後に集合外missingを理由として`unavailable`へ変えたrunは0件",
            "slots_issued_0",
            "Standard14_not_started",
        ):
            self.assertIn(required, evaluation)
        preparation = PREPARATION.read_text(encoding="utf-8")
        self.assertIn("comparison_preflight_ready / forty_five_slots_authorized / issued_zero", preparation)
        self.assertIn("candidate202_missing_45 / authorized_45 / issued_0", preparation)

    def test_adr9_result_passes_quality_and_stops_on_mechanism(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "0a509a780f0e40ae857ea602f00ff89b")
        self.assertEqual(result["compatibility_key"], "1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3")
        self.assertEqual(result["median"], {
            "elapsed_seconds": 692.9473878749559,
            "quality_score": 100.0,
            "total_tokens": 1289669,
        })
        self.assertEqual(quality["status"], "quality_passed")
        self.assertEqual(quality["quality_score_counts"], {"4": 45})
        self.assertEqual(quality["collector_false_positive_count"], 1)
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["routing_complete_count"], 30)
        self.assertEqual(mechanism["projection_receipt_acknowledgement_exact_count"], 30)
        self.assertEqual(mechanism["counterexample_certificate_priority_violation_count"], 9)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        self.assertIn("Standard14_not_started", RESULT_DOC.read_text(encoding="utf-8"))
        self.assertIn("reviewer-direct readの発行資格を、certificate判定のterminal resultへ依存させていない", CAUSAL.read_text(encoding="utf-8"))

    def test_standard14_result_passes_quality_and_stops_on_mechanism(self) -> None:
        profile = json.loads(STANDARD14_PROFILE.read_text(encoding="utf-8"))
        result = json.loads(STANDARD14_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(STANDARD14_QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(STANDARD14_MECHANISM.read_text(encoding="utf-8"))
        comparison = json.loads(STANDARD14_COMPARISON.read_text(encoding="utf-8"))
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(result["result_id"], "08c295a44f7b4a70873c7fc1c503f9e8")
        self.assertEqual(result["compatibility_key"], "cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561")
        self.assertEqual(result["median"], {
            "elapsed_seconds": 938.0808899969707,
            "quality_score": 100.0,
            "total_tokens": 1918118,
        })
        self.assertEqual(quality["score_counts"], {"4": 70})
        self.assertEqual(quality["failure_counts"], {})
        self.assertEqual(mechanism["mechanism_status"], "failed")
        self.assertEqual(mechanism["mechanism_failure"]["isolated_identity_run_count"], 31)
        self.assertEqual(mechanism["mechanism_failure"]["reference_candidate175_isolated_identity_run_count"], 1)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        self.assertEqual(comparison["median"]["total_tokens"]["delta"], 226055)
        self.assertEqual(comparison["median"]["elapsed_seconds"]["delta"], 133.141258330681)
        self.assertIn("quality_passed / mechanism_failed", STANDARD14_RESULT_DOC.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

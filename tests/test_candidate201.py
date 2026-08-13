from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-input-partition-r1"
PROFILE = ROOT / "evaluations/profiles/candidate201-review-input-partition-adr9-r2-medium-m24-n5-cli0146.json"
DESIGN = ROOT / "docs/candidate201-review-input-partition-adr9-r2-n5-evaluation-design.md"
PREPARATION = ROOT / "docs/candidate201-review-input-partition-adr9-r2-n5-execution-preparation-audit.md"
RESULT_RECORD = ROOT / "evaluations/results/candidate201-review-input-partition-adr9-r2-n5_2026-08-13.md"
REGISTERED_RESULT = ROOT / "evaluations/results/ba6c59a08d8744c08600207791c3b34f.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate201-review-input-partition-adr9-r2-n5-quality-audit-r2.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate201-review-input-partition-adr9-r2-n5-mechanism-audit-r9.json"
CAUSAL_ANALYSIS = ROOT / "docs/candidate201-m5-causal-analysis.md"


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


class Candidate201Test(unittest.TestCase):
    def test_direct_child_changes_only_root_agents(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": parent["prompt_identity"],
        })
        self.assertEqual(candidate["bundle_sha256"], "3cdc42ddb363315889b71909e6fbb272c6b007f8c589d4ccfea39e2c013951e3")
        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

    def test_partition_is_total_exclusive_and_projection_complete(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = clauses(text)
        parent = clauses((PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(len(parent), 13)
        self.assertEqual(len(candidate), 16)
        for label, value in parent.items():
            if label != "EVIDENCE_GATE":
                self.assertEqual(candidate[label], value, label)
        for required in (
            "required_review_input_manifest :=",
            "owner=root_projection",
            "owner=reviewer_observation",
            "ちょうど一方",
            "重複なくmanifest全体を被覆",
            "projection_complete :=",
            "reviewerもartifact変更も発行しない",
            "projected_source_closed(source) :=",
            "同一invocationの全targetが条件を満たす",
        ):
            self.assertIn(required, text)

    def test_candidate_does_not_claim_evaluation(self) -> None:
        manifest = verify_bundle(CANDIDATE)
        self.assertEqual(manifest["provenance"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["provenance"]["runtime_projection_status"], "not_projected")

    def test_evaluation_design_and_preflight_are_frozen(self) -> None:
        import json

        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["profile_id"], "candidate201-review-input-partition-adr9-r2-medium-m24-n5-cli0146")
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "3cdc42ddb363315889b71909e6fbb272c6b007f8c589d4ccfea39e2c013951e3")
        self.assertEqual(profile["execution"]["max_workers"], 24)
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Score `4 = 45 / 45`", design)
        self.assertIn("未割当てと重複は0件", design)
        self.assertIn("投影不足は0件", design)
        preparation = PREPARATION.read_text(encoding="utf-8")
        self.assertIn("comparison_preflight_ready / forty_five_slots_authorized / issued_zero", preparation)
        self.assertIn("candidate201_missing_45 / authorized_45 / issued_0", preparation)

    def test_registered_result_stops_before_standard14(self) -> None:
        import json

        result = json.loads(REGISTERED_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        record = RESULT_RECORD.read_text(encoding="utf-8")
        self.assertEqual(result["result_id"], "ba6c59a08d8744c08600207791c3b34f")
        self.assertEqual(result["result_content_sha256"], "141e34fd20f0b1c5f1d068deb99857ce0dac054db288bc33eb76a1cf9a416a66")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 30, "1": 15})
        self.assertEqual(quality["terminal_match_count"], 30)
        self.assertEqual(mechanism["reviewer_missing_count"], 15)
        self.assertEqual(mechanism["review_result_admission_match_count"], 29)
        self.assertEqual(mechanism["initial_identity_only_count"], 42)
        self.assertEqual(mechanism["reviewer_exact_read_set_match_count"], 15)
        self.assertEqual(mechanism["projection_complete_observed_count"], 7)
        self.assertEqual(mechanism["projection_complete_unobserved_count"], 8)
        self.assertEqual(mechanism["reviewer_closed_source_read_count"], 0)
        self.assertEqual(mechanism["reviewer_mixed_read_count"], 0)
        self.assertIn("Standard14_not_started", record)

    def test_causal_analysis_classifies_all_failure_runs_against_c175(self) -> None:
        analysis = CAUSAL_ANALYSIS.read_text(encoding="utf-8")
        self.assertIn("mechanism_failure_runs_26_classified", analysis)
        self.assertIn("owner_authority_missing_15", analysis)
        self.assertIn("projection_receipt_unobserved_8", analysis)
        self.assertIn("initial_identity_boundary_violation_3", analysis)
        self.assertIn("judgement_priority_violation_1", analysis)
        self.assertIn("unknown_cause_0", analysis)
        self.assertIn("1,123,616", analysis)
        self.assertIn("974,488", analysis)
        self.assertIn("C175を次Candidateの親にはしない", analysis)


if __name__ == "__main__":
    unittest.main()

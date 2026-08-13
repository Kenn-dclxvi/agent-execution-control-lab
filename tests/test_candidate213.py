from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-packet-provenance-review-closure-r1"
DESIGN = ROOT / "docs/candidate213-packet-provenance-review-closure-design.md"
DIRECTION = ROOT / "docs/candidate213-packet-provenance-review-closure-direction-audit.md"
AUDIT = ROOT / "docs/candidate213-packet-provenance-review-closure-implementation-audit.md"
RESULT = ROOT / "evaluations/results/75bdf968aa184783ab849d952a4a116f.json"
QUALITY = ROOT / "evaluations/results/candidate213-packet-provenance-review-closure-adr9-r2-n5-quality-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate213-packet-provenance-review-closure-adr9-r2-n5-mechanism-audit-r1.json"
REPORT = ROOT / "evaluations/results/candidate213-packet-provenance-review-closure-adr9-r2-n5_2026-08-14.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate213Test(unittest.TestCase):
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
            "64055b5aff47cb1372dcbca9f288d46abe4f6765e627db2545ac0275d2ae5663",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_existing_c147_closures_are_preserved(self) -> None:
        base = clauses((BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = clauses((CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(set(candidate) - set(base), {"PRECHANGE_REVIEW"})
        self.assertEqual(
            [label for label in base if base[label] != candidate[label]],
            ["EVIDENCE_GATE"],
        )
        for label in set(base) - {"EVIDENCE_GATE"}:
            self.assertEqual(candidate[label], base[label], label)
        self.assertEqual(
            len((CANDIDATE / "files/AGENTS.md.txt").read_bytes())
            - len((BASE / "files/AGENTS.md.txt").read_bytes()),
            4450,
        )

    def test_packet_source_identity_closes_reviewer_read_permission(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "review_packet_source_ready :=",
            "review_packet_closed_source_set :=",
            "review_source_read_forbidden(target) :=",
            "target identity ∈ review_packet_closed_source_set",
            "review_source_read_forbidden(observation.target)=false",
            "source identity欠落時はreviewerを起動せず",
            "集合を推測、拡張またはreviewerへ再構成させない",
            "trueのtargetはreview全lifecycleでrepository evidenceへ発行しない",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "scope_evidence_binding",
            "paired-scope-evidence",
            "TC-ADR",
            "OBS-",
            "SCOPE-",
            "Candidate211",
            "Candidate212",
            "Candidate213",
            "先にpacket",
        ):
            self.assertNotIn(prohibited, text)

    def test_creation_gate_and_direction_are_fixed_before_evaluation(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        direction = DIRECTION.read_text(encoding="utf-8")
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("creation_gate_fixed", design)
        self.assertIn("direct base: `Candidate147`", design)
        self.assertIn("direction_passed", direction)
        self.assertIn("candidate_creation_allowed", direction)
        self.assertIn("static_verification_passed", audit)
        self.assertIn("ADR9_completed", audit)

    def test_adr9_quality_and_mechanism_fail_and_stop_standard14(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        report = REPORT.read_text(encoding="utf-8")
        self.assertEqual(result["result_id"], "75bdf968aa184783ab849d952a4a116f")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(quality["status"], "quality_failed_stopped")
        self.assertEqual(quality["quality_score_counts"], {"4": 43, "1": 2})
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["packet_counterexample_read_free_count"], 17)
        self.assertEqual(mechanism["packet_counterexample_repository_read_count"], 5)
        self.assertEqual(mechanism["projected_source_reread_count"], 6)
        self.assertIn("Standard14_not_started", report)


if __name__ == "__main__":
    unittest.main()

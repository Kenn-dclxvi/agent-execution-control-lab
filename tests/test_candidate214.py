from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-packet-source-container-closure-r1"
DESIGN = ROOT / "docs/candidate214-packet-source-container-closure-design.md"
DIRECTION = ROOT / "docs/candidate214-packet-source-container-closure-direction-audit.md"
AUDIT = ROOT / "docs/candidate214-packet-source-container-closure-implementation-audit.md"
EVALUATION_DESIGN = ROOT / "docs/candidate214-packet-source-container-closure-adr9-r2-n5-evaluation-design.md"
RESULT = ROOT / "evaluations/results/385575fdc9694959af1c86042c3705c2.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5-mechanism-audit-r1.json"
REPORT = ROOT / "evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate214Test(unittest.TestCase):
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
            "3acb157b05719ca0ebca1d1f3ecbb6f76a53965686532833e1bbbbabd9b9815c",
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
        self.assertEqual([label for label in base if base[label] != candidate[label]], ["EVIDENCE_GATE"])
        for label in set(base) - {"EVIDENCE_GATE"}:
            self.assertEqual(candidate[label], base[label], label)
        self.assertEqual(
            len((CANDIDATE / "files/AGENTS.md.txt").read_bytes())
            - len((BASE / "files/AGENTS.md.txt").read_bytes()),
            5395,
        )

    def test_container_and_region_conflict_close_fragment_reads(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "packet_construction_receipt(item) :=",
            "review_closed_container_set :=",
            "review_read_conflicts(target) :=",
            "target.container identity ∈ review_closed_container_set",
            "同一 / 子孫 / 祖先 / 重複",
            "field選択、selector、hash、存在確認、部分抽出または別command",
            "実際に構築したpacket itemへ一件だけbindする",
            "packet itemを供給していないmanifest targetをrootがreceipt作成、存在確認またはpacket readinessのためにreadしない",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "scope_evidence_binding",
            "paired-scope-evidence",
            "TC-ADR",
            "OBS-",
            "SCOPE-",
            "Candidate200",
            "Candidate202",
            "Candidate213",
            "Candidate214",
            "先にこのpredicate",
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
        self.assertIn("ADR9_evaluated", audit)

    def test_adr9_result_is_registered_and_stopped(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        report = REPORT.read_text(encoding="utf-8")
        evaluation_design = EVALUATION_DESIGN.read_text(encoding="utf-8")
        self.assertEqual(result["result_id"], "385575fdc9694959af1c86042c3705c2")
        self.assertEqual(len(result["iterations"]), 5)
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual({item["case_id"] for item in result["case_results"]}, {f"TC-ADR{i:02d}" for i in range(1, 10)})
        self.assertEqual(quality["valid_run_count"], 45)
        self.assertEqual(quality["quality_score_counts"], {"1": 4, "4": 41})
        self.assertEqual(mechanism["projected_source_reread_count"], 0)
        self.assertEqual(mechanism["root_reviewer_owned_preread_count"], 0)
        self.assertEqual(mechanism["packet_counterexample_read_free_count"], 17)
        self.assertEqual(mechanism["external_disposition_expected_count"], 26)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        self.assertIn("Standard14_not_started", report)
        self.assertIn("container全体の閉鎖", report)
        self.assertIn("Standard14_not_started", evaluation_design)


if __name__ == "__main__":
    unittest.main()

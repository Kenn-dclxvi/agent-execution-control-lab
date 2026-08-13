from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-packet-source-region-closure-r1"
DESIGN = ROOT / "docs/candidate215-packet-source-region-closure-design.md"
DIRECTION = ROOT / "docs/candidate215-packet-source-region-closure-direction-audit.md"
AUDIT = ROOT / "docs/candidate215-packet-source-region-closure-implementation-audit.md"
RESULT = ROOT / "evaluations/results/e459b816c1ae4b97b2a776252b6f3367.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate215-packet-source-region-closure-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate215-packet-source-region-closure-adr9-r2-n5-mechanism-audit-r1.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate215-packet-source-region-closure-adr9-r2-n5_2026-08-14.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate215Test(unittest.TestCase):
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
            "da08a220485f0e48fe38165ec379ae52c60a0cbef9b225b92fc3edb7ff855a4f",
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
            5600,
        )

    def test_region_conflict_and_fallback_are_fixed(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "packet_construction_receipt(item) :=",
            "source_region_structurally_fixed(receipt) :=",
            "trueならそのregion identityを省略またはcontainer全体へ拡張しない",
            "falseではregionを推測せずcontainer fallbackへbindする",
            "review_read_conflicts(target) :=",
            "receipt.source regionまたはtarget.regionが未固定",
            "同一 / 子孫 / 祖先 / 重複",
            "review_read_conflicts(observation.target)=false",
            "実際に構築したpacket itemへ一件だけbindする",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "review_closed_container_set",
            "paired-scope-evidence",
            "TC-ADR",
            "OBS-",
            "SCOPE-",
            "Candidate214",
            "consumer_inventory",
            "先にこのpredicate",
        ):
            self.assertNotIn(prohibited, text)

    def test_creation_gate_and_direction_are_fixed(self) -> None:
        self.assertIn("creation_gate_fixed", DESIGN.read_text(encoding="utf-8"))
        self.assertIn("direction_passed", DIRECTION.read_text(encoding="utf-8"))
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("static_verification_passed", audit)
        self.assertIn("quality_failed", audit)

    def test_evaluation_result_and_audits_are_fixed(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "e459b816c1ae4b97b2a776252b6f3367")
        self.assertEqual(quality["valid_run_count"], 45)
        self.assertEqual(quality["quality_score_counts"], {"1": 4, "4": 41})
        self.assertEqual(quality["terminal_match_count"], 41)
        self.assertEqual(quality["artifact_boundary_match_count"], 44)
        self.assertEqual(mechanism["packet_overlap_or_whole_read_count"], 0)
        self.assertEqual(mechanism["allowed_nonoverlap_region_read_count"], 13)
        self.assertEqual(mechanism["allowed_nonoverlap_region_read_run_count"], 9)
        self.assertEqual(mechanism["unexpected_nonoverlap_region_read_count"], 7)
        self.assertEqual(mechanism["packet_case_wrong_paired_read_count"], 3)
        self.assertEqual(mechanism["root_reviewer_owned_preread_count"], 0)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        report = RESULT_REPORT.read_text(encoding="utf-8")
        self.assertIn("quality_failed / mechanism_failed / stopped", report)
        self.assertIn("Standard14", report)


if __name__ == "__main__":
    unittest.main()

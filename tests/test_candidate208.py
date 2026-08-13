from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-c147-review-boundary-recomposition-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-kind-evidence-domain-r1"
DESIGN = ROOT / "docs/candidate208-result-kind-evidence-domain-design.md"
RESULT = ROOT / "evaluations/results/c4e84aef70aa4d5d9b97c09c6817605d.json"
AUDIT = ROOT / "evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n5-quality-mechanism-audit-r1.json"
STANDARD14_RESULT = ROOT / "evaluations/results/7922b5fec056420bb558dd03e502ef66.json"
STANDARD14_QUALITY = ROOT / "evaluations/results/candidate208-result-kind-evidence-domain-standard14-n5-quality-audit-r1.json"
STANDARD14_MECHANISM = ROOT / "evaluations/results/candidate208-result-kind-evidence-domain-standard14-n5-mechanism-diagnostic-r1.json"
ADR9_N50_RESULT = ROOT / "evaluations/results/2429806ecd95438280eb995f289a2468.json"
ADR9_N50_SUMMARY = ROOT / "evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n50-summary-audit-r1.json"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate208Test(unittest.TestCase):
    def test_direct_c207_child_changes_only_root_agents(self) -> None:
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
            "be67f9dce76e57ac1b1f7535a4e1128f3f7b9f0b7810e55527d089d1cbd7f15f",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_only_three_connected_control_groups_change(self) -> None:
        base_text = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        base = clauses(base_text)
        candidate = clauses(candidate_text)
        self.assertEqual(base.keys(), candidate.keys())
        self.assertEqual(
            [label for label in base if base[label] != candidate[label]],
            ["TERMINAL", "CONTEXT", "EVIDENCE_GATE"],
        )
        self.assertEqual(len(candidate_text) - len(base_text), 208)

    def test_result_kind_evidence_domain_is_boundary_not_workflow(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "review_required_evidence(kind) :=",
            "kind=counterexample_foundなら上記certificate support",
            "kind=no_counterexample_foundならTaskSpec-fixedな全review scopeと全manifest descriptorのsuccess receipt",
            "kind=review_unavailableなら残るallowed dispositionを変え得るnamed observation",
            "全review resultに共通する実行義務ではない",
            "model-visible projectionを`unobserved`へ戻す根拠にしない",
            "未解決result kindのreview_required_evidenceへbind済み",
            "certificate support外の全observationでfalse",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "admitted_evidence_current",
            "projection receipt",
            "acknowledgement",
            "先にcounterexample",
            "成立しない場合だけ",
            "後続二判定",
            "review result kind別operation",
            "Candidate208",
            "TC-ADR",
        ):
            self.assertNotIn(prohibited, text)

    def test_creation_gate_records_observed_mechanism_and_stop_conditions(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        self.assertIn("direct read違反12件", text)
        self.assertIn("direct read 0 / 20", text)
        self.assertIn("no_procedural_review_lifecycle", text)
        self.assertIn("creation_allowed", text)
        self.assertIn("repair rerun、Standard14およびN=20へ進めない", text)

    def test_registered_result_preserves_quality_and_mechanism_stop(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "c4e84aef70aa4d5d9b97c09c6817605d")
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(audit["result"]["quality_score_counts"], {"4": 45})
        self.assertTrue(audit["quality_gate"]["passed"])
        self.assertFalse(audit["mechanism_gate"]["passed"])
        self.assertEqual(
            audit["mechanism_gate"]["counterexample_certificate_priority_violation_count"],
            1,
        )
        self.assertEqual(audit["mechanism_gate"]["root_reviewer_direct_preread_free_count"], 29)
        self.assertEqual(audit["stop_effect"]["standard14"], "not_started")

    def test_later_standard14_measurement_does_not_reclassify_adr9_mechanism(self) -> None:
        result = json.loads(STANDARD14_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(STANDARD14_QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(STANDARD14_MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "7922b5fec056420bb558dd03e502ef66")
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(result["median"]["total_tokens"], 1605899)
        self.assertEqual(quality["score_counts"], {"4": 70})
        self.assertEqual(quality["failure_counts"], {})
        self.assertEqual(mechanism["status"], "diagnostic_only")
        self.assertEqual(mechanism["interpretation"]["adr9_mechanism_status"], "failed_unchanged")

    def test_adr9_n50_preserves_valid_low_quality_run_and_stops_standard14(self) -> None:
        result = json.loads(ADR9_N50_RESULT.read_text(encoding="utf-8"))
        summary = json.loads(ADR9_N50_SUMMARY.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "2429806ecd95438280eb995f289a2468")
        self.assertEqual(len(result["case_results"]), 450)
        self.assertEqual(summary["quality_gate"]["score_counts"], {"4": 449, "1": 1})
        self.assertEqual(summary["mechanism_gate"]["failure_run_count"], 23)
        self.assertEqual(
            summary["stop_effect"]["standard14_n50"],
            "not_started_at_adr9_quality_gate",
        )


if __name__ == "__main__":
    unittest.main()

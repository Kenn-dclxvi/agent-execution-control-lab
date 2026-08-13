from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-c147-review-boundary-recomposition-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-evidence-state-closure-r1"
DESIGN = ROOT / "docs/candidate210-review-evidence-state-closure-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate210-review-evidence-state-closure-adr9-r2-medium-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/9ac8eb53cf79463f9c7ae446c61b625a.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5-mechanism-audit-r1.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate210Test(unittest.TestCase):
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
            "46a44d6e4aa25d8671e2d06202ca3c7097aba248dc95fd1156e5548dd30f0fda",
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
        self.assertEqual(len(candidate_text) - len(base_text), 1093)

    def test_descriptor_state_closure_replaces_result_prediction(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "review_descriptor_state(d) := projected_success | direct_success | direct_nonvalue | unobserved_direct",
            "review_descriptor_route(d) := projected | direct",
            "各descriptorはexactly one routeを持ち",
            "review_counterexample_supported :=",
            "unobserved_directが0件",
            "review_observation_frontier :=",
            "observationがreview_observation_frontierに属する",
            "未解決result kind、requested resultがallowed dispositionを変え得る可能性",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "review_required_evidence(kind)",
            "certificate_deficit",
            "review_observation_dependency",
            "同じrequired fact",
            "先にpacket",
            "反例がなければ次に",
            "result kind別operation",
            "Candidate210",
            "TC-ADR",
        ):
            self.assertNotIn(prohibited, text)

    def test_creation_gate_records_c208_reaudit_and_bidirectional_failure(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        self.assertIn("packet反例成立後readが10 / 199件", text)
        self.assertIn("direct observationまで3 / 5件で失った", text)
        self.assertIn("c208_three_controls_reaudited", text)
        self.assertIn("c207_direct_base", text)
        self.assertIn("three_connected_boundary_replacements", text)
        self.assertIn("no_procedural_review_lifecycle", text)
        self.assertIn("creation_allowed", text)

    def test_adr9_profile_and_registered_result_are_fixed(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["prompt_set_identity"]["name"],
            "the-caption-3ce91a4-review-evidence-state-closure-r1",
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(result["result_id"], "9ac8eb53cf79463f9c7ae446c61b625a")
        self.assertEqual(result["prompt_set_identity"], profile["prompt_set_identity"])
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(result["median"]["total_tokens"], 1073699)

    def test_adr9_quality_passes_but_mechanism_stops_extension(self) -> None:
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        report = RESULT_REPORT.read_text(encoding="utf-8")
        self.assertEqual(quality["status"], "quality_passed")
        self.assertEqual(quality["valid_run_count"], 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 45})
        self.assertEqual(quality["terminal_match_count"], 45)
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertFalse(mechanism["mechanism_gate_passed"])
        self.assertEqual(len(mechanism["failure_run_ids"]), 12)
        self.assertEqual(mechanism["counterexample_certificate_priority_violation_count"], 9)
        self.assertEqual(mechanism["review_result_admission_match_count"], 42)
        self.assertEqual(mechanism["root_reviewer_direct_preread_free_count"], 30)
        self.assertIn("Standard14_not_started", report)
        self.assertIn("quality_passed / mechanism_failed / stopped", report)


if __name__ == "__main__":
    unittest.main()

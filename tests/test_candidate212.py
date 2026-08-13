from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-disposition-effect-review-evidence-r1"
DESIGN = ROOT / "docs/candidate212-disposition-effect-review-evidence-design.md"
DIRECTION = ROOT / "docs/candidate212-disposition-effect-review-evidence-direction-audit.md"
AUDIT = ROOT / "docs/candidate212-disposition-effect-review-evidence-implementation-audit.md"
RESULT = ROOT / "evaluations/results/ccb5994762094c778f9fb96d69253b3f.json"
QUALITY = ROOT / "evaluations/results/candidate212-disposition-effect-review-evidence-adr9-r2-n5-quality-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate212-disposition-effect-review-evidence-adr9-r2-n5-mechanism-audit-r1.json"
REPORT = ROOT / "evaluations/results/candidate212-disposition-effect-review-evidence-adr9-r2-n5_2026-08-13.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate212Test(unittest.TestCase):
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
            "81b2f788f4bb0079c1af9e874948f8029bb949c6318dc343a0f56f1c29cd5c1c",
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
            3783,
        )

    def test_read_permission_depends_on_disposition_effect(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "review_terminal_support(kind) :=",
            "review_evidence_consumer_ready(observation) :=",
            "いずれのallowed terminal kindもまだsupportされていない",
            "現在未確定の具体的命題がbind済み",
            "requested resultの取り得る異なる値が残っているallowed terminal dispositionを分け得る",
            "manifest membership、scope / target / observationの名称、read permission、sourceの存在または念のための確認はconsumerを成立させない",
            "いずれかのterminal kindがsupportされた時点で、別kindだけに必要な未発行observationを失効する",
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
        self.assertIn("not_evaluated", audit)

    def test_adr9_quality_passes_but_mechanism_stops_standard14(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        report = REPORT.read_text(encoding="utf-8")
        self.assertEqual(result["result_id"], "ccb5994762094c778f9fb96d69253b3f")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(quality["status"], "quality_passed")
        self.assertEqual(quality["quality_score_counts"], {"4": 45})
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["packet_counterexample_read_free_count"], 9)
        self.assertEqual(mechanism["packet_counterexample_repository_read_count"], 17)
        self.assertEqual(mechanism["review_result_admission_match_count"], 45)
        self.assertIn("Standard14_not_started", report)


if __name__ == "__main__":
    unittest.main()

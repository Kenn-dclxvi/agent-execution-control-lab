from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-review-operation-admission-closure-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-admitted-evidence-current-r1"
DESIGN = ROOT / "docs/candidate206-admitted-evidence-current-design.md"
DIRECTION_REVIEW = ROOT / "docs/candidate206-admitted-evidence-current-direction-review.md"
IMPLEMENTATION_AUDIT = ROOT / "docs/candidate206-admitted-evidence-current-implementation-audit.md"
PROFILE = ROOT / "evaluations/profiles/candidate206-admitted-evidence-current-adr9-r2-medium-m24-n5-cli0146.json"
REFERENCE_PROFILE = ROOT / "evaluations/profiles/candidate175-review-operation-admission-closure-adr9-r2-medium-m24-n5-cli0146.json"
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate206-admitted-evidence-current-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
STANDARD14_REFERENCE_PROFILE = ROOT / "evaluations/profiles/candidate175-review-operation-admission-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
PREPARATION_AUDIT = ROOT / "docs/candidate206-admitted-evidence-current-adr9-r2-n5-execution-preparation-audit.md"
RESULT_RECORD = ROOT / "evaluations/results/candidate206-admitted-evidence-current-adr9-standard14-n5_2026-08-13.md"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate206-admitted-evidence-current-mechanism-audit-r1.json"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate206Test(unittest.TestCase):
    def test_direct_child_changes_only_root_agents(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(
            candidate["artifact"]["evaluation_status"],
            "adr9_standard14_quality_passed_mechanism_passed_optimization_failed_stopped",
        )
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
            "5de383fad436407f9696e3ee79681ee89e1c695c8a9fd4e3cfdf4c3e326c5046",
        )
        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

    def test_only_evidence_gate_clause_changes(self) -> None:
        parent = clauses((PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = clauses((CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(parent.keys(), candidate.keys())
        for label in parent:
            if label != "EVIDENCE_GATE":
                self.assertEqual(candidate[label], parent[label], label)
        evidence_gate = candidate["EVIDENCE_GATE"]
        for fragment in (
            "admitted_evidence_current(evidence_identity) :=",
            "model-visible inputまたはadmission済みterminal result",
            "そのidentityの値を変えるadmission済みresultが未受領",
            "required predicateの`satisfied`判定ではない",
            "permission / allowed readだけではcurrentにせず",
            "開始inputにないpath-local instructionまたは未観測targetは取得でき",
            "再観測できる",
        ):
            self.assertIn(fragment, evidence_gate)

    def test_design_and_audits_keep_evaluation_boundary(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate175を比較用の直接親", design)
        self.assertIn("ADR9通過後だけStandard14", design)
        self.assertIn("過剰品質または無効な追加として停止", design)
        self.assertIn("candidate_implementation_allowed", DIRECTION_REVIEW.read_text(encoding="utf-8"))
        audit = IMPLEMENTATION_AUDIT.read_text(encoding="utf-8")
        self.assertIn("static_verification_passed / not_evaluated", audit)
        self.assertIn("EVIDENCE_GATE`一節だけ", audit)

    def test_profile_changes_only_prompt_identity_and_explanation(self) -> None:
        import json

        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        reference = json.loads(REFERENCE_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-admitted-evidence-current-r1",
                "revision": "r1",
                "bundle_sha256": "5de383fad436407f9696e3ee79681ee89e1c695c8a9fd4e3cfdf4c3e326c5046",
            },
        )
        for key in ("evaluation_set", "cases", "iterations", "comparison_conditions", "execution"):
            self.assertEqual(profile[key], reference[key], key)

    def test_preparation_audit_authorizes_only_candidate_slots(self) -> None:
        text = PREPARATION_AUDIT.read_text(encoding="utf-8")
        for fragment in (
            "comparison_preflight_ready / forty_five_slots_authorized / issued_zero",
            "reference result: `eba0a4bc1d0e4391afa631462b8daccb`",
            "Candidate206 pool: `bff5449e6489cff8c22e4627252bc06a570e1520ddf70b9f2b103c05f90a3483`",
            "candidate206_missing_45 / authorized_45 / issued_0",
            "authoritative cycle: `cycle-r2`",
        ):
            self.assertIn(fragment, text)

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        import json

        profile = json.loads(STANDARD14_PROFILE.read_text(encoding="utf-8"))
        reference = json.loads(STANDARD14_REFERENCE_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-admitted-evidence-current-r1",
                "revision": "r1",
                "bundle_sha256": "5de383fad436407f9696e3ee79681ee89e1c695c8a9fd4e3cfdf4c3e326c5046",
            },
        )
        for key in ("evaluation_set", "cases", "iterations", "comparison_conditions", "execution", "scope"):
            self.assertEqual(profile[key], reference[key], key)

    def test_result_keeps_quality_mechanism_and_optimization_separate(self) -> None:
        import json

        text = RESULT_RECORD.read_text(encoding="utf-8")
        for fragment in (
            "ADR9とStandard14の品質・機序gateを通過したが、最適化gateは通過しなかった",
            "Candidate175 7 run、Candidate206 0 run",
            "-131,449（-7.77%）",
            "+99.836秒（+12.40%）",
            "next-candidate parentage: `not_granted`",
        ):
            self.assertIn(fragment, text)
        audit = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(audit["status"], "mechanism_passed_optimization_failed_stopped")
        self.assertEqual(audit["adr9"]["score_4_runs"], 45)
        self.assertEqual(audit["standard14"]["score_4_runs"], 70)
        self.assertEqual(audit["standard14"]["candidate_root_instruction_content_read_runs"], 0)
        self.assertEqual(audit["kpi"]["optimization_gate"], "failed_no_kpi_dominance")


if __name__ == "__main__":
    unittest.main()

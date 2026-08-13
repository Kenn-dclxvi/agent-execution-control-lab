from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-kind-evidence-domain-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-named-certificate-deficit-r1"
DESIGN = ROOT / "docs/candidate209-named-certificate-deficit-design.md"
RESULT = ROOT / "evaluations/results/095076f0eb7540c397dc298745b6cac4.json"
QUALITY = ROOT / "evaluations/results/candidate209-named-certificate-deficit-adr9-r2-n5-quality-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate209-named-certificate-deficit-adr9-r2-n5-mechanism-audit-r1.json"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate209Test(unittest.TestCase):
    def test_direct_c208_child_changes_only_root_agents(self) -> None:
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
            "4790214b24a560cfc34c93decde076cbf033c007ad8fd3f4533203d395c3925b",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_only_terminal_and_evidence_gate_change(self) -> None:
        base_text = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        base = clauses(base_text)
        candidate = clauses(candidate_text)
        self.assertEqual(base.keys(), candidate.keys())
        self.assertEqual(
            [label for label in base if base[label] != candidate[label]],
            ["TERMINAL", "EVIDENCE_GATE"],
        )
        self.assertEqual(len(candidate_text) - len(base_text), 400)

    def test_named_deficit_is_permission_boundary_not_workflow(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "counterexample_certificate_component_set :=",
            "certificate_deficit(packet) :=",
            "現在unobservedのcomponent identity集合",
            "そのobservationのsuccess resultだけが同じcomponentをbind可能な排他的依存",
            "missing observationは未充足componentまたは排他的依存を事後生成しない",
            "review_observation_dependency(observation) :=",
            "certificate_deficit(packet)内の一つ以上のcomponent",
            "`certificate_deficit(packet)`が空なら全manifest observationでfalse",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "OBS-PAIRED-SCOPE",
            "TC-ADR05",
            "先にcertificate",
            "成立しない場合だけ",
            "次にmanifest",
            "review result kind別operation",
            "Candidate209",
        ):
            self.assertNotIn(prohibited, text)

    def test_creation_gate_records_low_frequency_failure_and_stop(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        self.assertIn("3eb2bcdb4605471daac50ab70dba953d", text)
        self.assertIn("Score 1は1件", text)
        self.assertIn("packet反例成立後read 10 / 199件", text)
        self.assertIn("two_connected_predicate_replacements", text)
        self.assertIn("no_procedural_review_lifecycle", text)
        self.assertIn("creation_allowed", text)
        self.assertIn("ADR9を累積N=20へ延長", text)

    def test_adr9_n5_preserves_quality_and_mechanism_failure(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "095076f0eb7540c397dc298745b6cac4")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 42, "1": 3})
        self.assertEqual(quality["terminal_match_count"], 42)
        self.assertEqual(
            {run["case_id"] for run in quality["runs"] if run["quality_score"] == 1},
            {"TC-ADR07"},
        )
        self.assertFalse(mechanism["mechanism_gate_passed"])
        self.assertEqual(len(mechanism["failure_run_ids"]), 7)
        self.assertEqual(mechanism["counterexample_certificate_priority_violation_count"], 3)


if __name__ == "__main__":
    unittest.main()

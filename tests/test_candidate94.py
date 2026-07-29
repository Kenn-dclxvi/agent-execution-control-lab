from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C94 = ROOT / "prompts/candidates/the-caption-3ce91a4-operation-criterion-totality-r1"
DESIGN = ROOT / "docs/candidate94-operation-criterion-totality-design.md"
BASELINE_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2.json"
CANDIDATE_PROFILE = ROOT / "evaluations/profiles/candidate94-operation-criterion-totality-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/candidate81-candidate94-operation-criterion-totality-v14-medium-standard14-n5-cli0146_2026-07-30.md"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ")
    }


class Candidate94Test(unittest.TestCase):
    def test_is_direct_child_with_one_changed_target(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C94)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_operation_criterion_totality_labels(self) -> None:
        source = rules(C81 / "files/AGENTS.md.txt")
        candidate = rules(C94 / "files/AGENTS.md.txt")
        self.assertEqual(set(source), set(candidate))
        changed = {label for label in source if source[label] != candidate[label]}
        self.assertEqual(changed, {"SPEC", "TERMINAL", "OWNER_ROLE"})
        for label in set(source) - changed:
            self.assertEqual(candidate[label], source[label])

        self.assertIn("spec_ready(operation)", candidate["SPEC"])
        self.assertIn("criterion owner=none", candidate["SPEC"])
        self.assertIn("別operationへ伝播させない", candidate["SPEC"])
        self.assertIn("terminal failure result", candidate["TERMINAL"])
        self.assertIn("unavailable", candidate["OWNER_ROLE"])
        self.assertIn("result欠落として扱わない", candidate["OWNER_ROLE"])
        self.assertIn("false / failed / unavailable", candidate["OWNER_ROLE"])

    def test_manifest_and_design_remain_draft(self) -> None:
        manifest = json.loads((C94 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "draft")
        self.assertEqual(manifest["provenance"]["runtime_projection_status"], "not_projected")

        design = DESIGN.read_text(encoding="utf-8")
        for text in (
            "candidate number: Candidate94",
            "evaluation status: `not_evaluated`",
            "release: `not_created`",
            "runtime projection: `not_projected`",
        ):
            self.assertIn(text, design)

    def test_standard14_profiles_change_only_identity(self) -> None:
        baseline = json.loads(BASELINE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(CANDIDATE_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(baseline["comparison_conditions"], candidate["comparison_conditions"])
        self.assertEqual(baseline["cases"], candidate["cases"])
        self.assertEqual(baseline["evaluation_set"], candidate["evaluation_set"])
        self.assertEqual(baseline["execution"], candidate["execution"])
        self.assertEqual(baseline["scope"], candidate["scope"])
        self.assertEqual(
            baseline["comparison_conditions"]["agent_environment"]["codex_cli"],
            "0.146.0",
        )
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "3ada30eda65f9b6ac152c1a9530f53f89221323d6003354e40d6cfdd5a18257e",
                "name": "the-caption-3ce91a4-operation-criterion-totality-r1",
                "revision": "r1",
            },
        )

    def test_standard14_result_records_quality_failure_and_stop(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        for text in (
            "Candidate81は70 / 70件がscore `4`",
            "Candidate94はscore `4 / 1 = 69 / 1`",
            "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING",
            "a02_canonical_route_mismatch",
            "`standard14_evaluated / quality_gate_failed / stopped`",
            "targeted評価自体は未実施",
            "C94 result: `fdc86bfd09a349d5a64b768c0adf450a`",
            "compatibility key: `c5bfcd6dcc52b99e7a3dabda966dcb00640e4eeed8c969753992545c87a8490c`",
        ):
            self.assertIn(text, result)


if __name__ == "__main__":
    unittest.main()

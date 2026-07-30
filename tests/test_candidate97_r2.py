from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C97_R2 = ROOT / "prompts/candidates/the-caption-3ce91a4-decision-round-closure-r2"
DESIGN = ROOT / "docs/candidate97-minimal-decision-round-closure-r2-design.md"
BASELINE_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-f02-global-m5-n5-cli0146-r1.json"
CANDIDATE_PROFILE = ROOT / "evaluations/profiles/candidate97-decision-round-closure-r2-v14-reasoning-medium-f02-global-m5-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/candidate81-candidate97-decision-round-closure-r2-v14-medium-f02-n5-cli0146_2026-07-30.md"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate97R2Test(unittest.TestCase):
    def test_is_direct_c81_child_with_one_changed_target(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C97_R2)
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

    def test_replaces_only_decision_boundary_with_minimal_rule(self) -> None:
        source = rules(C81 / "files/AGENTS.md.txt")
        candidate = rules(C97_R2 / "files/AGENTS.md.txt")
        self.assertEqual(source.keys(), candidate.keys())
        self.assertEqual(
            [label for label in source if source[label] != candidate[label]],
            ["DECISION_BOUNDARY"],
        )
        rule = candidate["DECISION_BOUNDARY"]
        self.assertIn("追加invocationには新たに判明した必要evidence", rule)
        self.assertIn("terminal result済みの同一invocation", rule)
        self.assertNotIn("inspection read", rule)
        self.assertNotIn("completion evidence", rule)
        self.assertLess(len(rule), 250)

    def test_manifest_design_and_profile_boundaries(self) -> None:
        manifest = verify_bundle(C97_R2)
        self.assertEqual(manifest["bundle_sha256"], "07f535a6e4f4d1b13731879ccd5bddfa3856b679b39bb7a14bc7da6ea01cbc23")
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "draft")
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("r1の長い列挙を廃止", design)
        self.assertIn("command数、message数、token数の上限", design)

        baseline = json.loads(BASELINE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(CANDIDATE_PROFILE.read_text(encoding="utf-8"))
        for key in ("cases", "comparison_conditions", "evaluation_set", "execution", "scope"):
            self.assertEqual(baseline[key], candidate[key])
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "07f535a6e4f4d1b13731879ccd5bddfa3856b679b39bb7a14bc7da6ea01cbc23",
                "name": "the-caption-3ce91a4-decision-round-closure-r2",
                "revision": "r1",
            },
        )

    def test_f02_result_records_mechanism_failure_and_stop(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        for text in (
            "5 / 5件がvalid・rateable・score `4`",
            "full gate成功後に別の`git status` command",
            "token中央値は`+4.72%`",
            "elapsed中央値は`+0.31%`",
            "completion decision-round closure: `failed`",
            "inspection decision-round closure: `unproven`",
            "targeted_f02_evaluated / quality_gate_passed / mechanism_gate_failed / stopped",
            "Candidate97 r1: `execution_aborted_before_terminal_result / result_not_registered / stopped`",
            "08091993bb534269bd267b6ce2ad30c0",
        ):
            self.assertIn(text, result)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C97 = ROOT / "prompts/candidates/the-caption-3ce91a4-decision-round-closure-r1"
DESIGN = ROOT / "docs/candidate97-decision-round-closure-design.md"
BASELINE_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-f02-global-m5-n5-cli0146-r1.json"
CANDIDATE_PROFILE = ROOT / "evaluations/profiles/candidate97-decision-round-closure-v14-reasoning-medium-f02-global-m5-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate97Test(unittest.TestCase):
    def test_is_direct_c81_child_with_one_changed_target(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C97)
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

    def test_replaces_only_decision_boundary(self) -> None:
        source = rules(C81 / "files/AGENTS.md.txt")
        candidate = rules(C97 / "files/AGENTS.md.txt")
        self.assertEqual(source.keys(), candidate.keys())
        self.assertEqual(
            [label for label in source if source[label] != candidate[label]],
            ["DECISION_BOUNDARY"],
        )
        rule = candidate["DECISION_BOUNDARY"]
        self.assertIn("次waveへ完全にbind", rule)
        self.assertIn("同一model step", rule)
        self.assertIn("inspection read", rule)
        self.assertIn("completion evidence", rule)
        self.assertIn("未取得evidence", rule)
        self.assertIn("terminal resultがbind済みの同一invocation", rule)
        self.assertIn("shell compound commandへ結合せず", rule)

    def test_manifest_and_design_keep_candidate_boundaries(self) -> None:
        manifest = verify_bundle(C97)
        self.assertEqual(manifest["bundle_sha256"], "7a7dbdf23bcf2ea36ec311ea2ca3696d71e09c51190d5a9f4adf1e273d428ab0")
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "draft")
        self.assertEqual(manifest["provenance"]["runtime_projection_status"], "not_projected")
        design = DESIGN.read_text(encoding="utf-8")
        for text in (
            "candidate number: Candidate97",
            "evaluation status: `not_evaluated`",
            "release: `not_created`",
            "runtime projection: `not_projected`",
            "reasoning tokenまたはcommand数の上限も設けない",
        ):
            self.assertIn(text, design)

    def test_f02_profile_changes_only_prompt_identity(self) -> None:
        baseline = json.loads(BASELINE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(CANDIDATE_PROFILE.read_text(encoding="utf-8"))
        for key in ("cases", "comparison_conditions", "evaluation_set", "execution", "scope"):
            self.assertEqual(baseline[key], candidate[key])
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "7a7dbdf23bcf2ea36ec311ea2ca3696d71e09c51190d5a9f4adf1e273d428ab0",
                "name": "the-caption-3ce91a4-decision-round-closure-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C92 = ROOT / "prompts/candidates/the-caption-3ce91a4-bound-output-route-r1"
BASELINE = ROOT / "evaluations/profiles/candidate81-planning-first-producer-selection-v14-reasoning-medium-f02-global-m5-n5-r1.json"
PROFILE = ROOT / "evaluations/profiles/candidate92-bound-output-route-v14-reasoning-medium-f02-global-m5-n5-r1.json"
RESULT = ROOT / "evaluations/results/candidate81-candidate92-bound-output-route-v14-medium-f02-n5_2026-07-29.md"


def blocks(text: str) -> dict[str, str]:
    return {line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1] for line in text.splitlines() if line.startswith("- ")}


class Candidate92Test(unittest.TestCase):
    def test_is_direct_child_with_one_changed_target(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C92)
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": source["prompt_identity"],
        })
        self.assertEqual([x for x in candidate["files"] if x["target"] != "AGENTS.md"], [x for x in source["files"] if x["target"] != "AGENTS.md"])

    def test_adds_bound_output_route_only(self) -> None:
        source = blocks((C81 / "files/AGENTS.md.txt").read_text())
        candidate = blocks((C92 / "files/AGENTS.md.txt").read_text())
        self.assertEqual(set(candidate) - set(source), {"OUTPUT_INGRESS"})
        rule = candidate["OUTPUT_INGRESS"]
        self.assertIn("最初のcommand前", rule)
        self.assertIn("output_route=temporary_file", rule)
        self.assertIn("4096 bytes以下", rule)
        self.assertEqual(rule.count("。"), 2)
        for label, body in source.items():
            self.assertEqual(candidate[label], body)

    def test_profile_changes_only_identity(self) -> None:
        baseline = json.loads(BASELINE.read_text())
        candidate = json.loads(PROFILE.read_text())
        for key in ("cases", "comparison_conditions", "evaluation_set", "execution", "scope"):
            self.assertEqual(baseline[key], candidate[key])

    def test_result_separates_route_cap_and_cost(self) -> None:
        result = RESULT.read_text()
        self.assertIn("最初のroute固定: 5 / 5", result)
        self.assertIn("全対象success result 4096 bytes以下: 3 / 5", result)
        self.assertIn("token `+157,023`（`+51.00%`）", result)
        self.assertIn("elapsed `+31.090`秒（`+28.89%`）", result)
        self.assertIn("targeted_f02_evaluated / stopped", result)


if __name__ == "__main__":
    unittest.main()

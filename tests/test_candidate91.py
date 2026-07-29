from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C91 = ROOT / "prompts/candidates/the-caption-3ce91a4-concise-output-ingress-r1"
BASELINE_PROFILE = ROOT / "evaluations/profiles/candidate81-planning-first-producer-selection-v14-reasoning-medium-f02-global-m5-n5-r1.json"
CANDIDATE_PROFILE = ROOT / "evaluations/profiles/candidate91-concise-output-ingress-v14-reasoning-medium-f02-global-m5-n5-r1.json"
RESULT = ROOT / "evaluations/results/candidate81-candidate91-concise-output-ingress-v14-medium-f02-n5_2026-07-29.md"


def blocks(text: str) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in text.splitlines()
        if line.startswith("- ")
    }


class Candidate91Test(unittest.TestCase):
    def test_is_direct_child_with_one_changed_target(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C91)
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": source["prompt_identity"],
        })
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_adds_one_concise_action(self) -> None:
        source = blocks((C81 / "files/AGENTS.md.txt").read_text())
        candidate = blocks((C91 / "files/AGENTS.md.txt").read_text())
        self.assertEqual(set(candidate) - set(source), {"OUTPUT_INGRESS"})
        self.assertLessEqual(len(candidate["OUTPUT_INGRESS"]), 160)
        self.assertEqual(candidate["OUTPUT_INGRESS"].count("。"), 2)
        for label, body in source.items():
            self.assertEqual(candidate[label], body)

    def test_profile_changes_only_identity(self) -> None:
        baseline = json.loads(BASELINE_PROFILE.read_text())
        candidate = json.loads(CANDIDATE_PROFILE.read_text())
        for key in ("cases", "comparison_conditions", "evaluation_set", "execution", "scope"):
            self.assertEqual(baseline[key], candidate[key])
        self.assertNotEqual(baseline["prompt_set_identity"], candidate["prompt_set_identity"])

    def test_result_records_partial_compliance_and_stop(self) -> None:
        result = RESULT.read_text()
        self.assertIn("strict compliance: 2 / 5", result)
        self.assertIn("token `+18,163`（`+5.90%`）", result)
        self.assertIn("elapsed `+13.923`秒（`+12.94%`）", result)
        self.assertIn("targeted_f02_evaluated / stopped", result)


if __name__ == "__main__":
    unittest.main()

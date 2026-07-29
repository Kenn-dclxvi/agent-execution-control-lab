from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C90 = ROOT / "prompts/candidates/the-caption-3ce91a4-tool-output-ingress-boundary-r1"
DESIGN = ROOT / "docs/candidate90-tool-output-ingress-boundary-design.md"
RESULT = ROOT / "evaluations/results/candidate81-candidate90-tool-output-ingress-boundary-v14-medium-f02-n5_2026-07-29.md"
PROFILES = ROOT / "evaluations/profiles"
PROFILE_PAIRS = (
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f02-global-m5-n5-r1.json",
        "candidate90-tool-output-ingress-boundary-v14-reasoning-medium-f02-global-m5-n5-r1.json",
    ),
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f04-global-m5-n5-r1.json",
        "candidate90-tool-output-ingress-boundary-v14-reasoning-medium-f04-global-m5-n5-r1.json",
    ),
    (
        "candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-r1.json",
        "candidate90-tool-output-ingress-boundary-v14-reasoning-medium-standard14-global-m24-n5-r1.json",
    ),
)


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if line.startswith("- "):
            label, body = line[2:].split(": ", 1)
            blocks[label] = body
    return blocks


class Candidate90Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate81(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C90)
        self.assertEqual(candidate["prompt_identity"], "the-caption-3ce91a4-tool-output-ingress-boundary-r1")
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

    def test_adds_only_output_ingress(self) -> None:
        source = labelled_blocks((C81 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C90 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(set(candidate) - set(source), {"OUTPUT_INGRESS"})
        self.assertEqual(set(source) - set(candidate), set())
        for label, body in source.items():
            self.assertEqual(candidate[label], body)

    def test_projects_before_raw_output_enters_context(self) -> None:
        boundary = labelled_blocks((C90 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))["OUTPUT_INGRESS"]
        self.assertIn("repository外の一時file", boundary)
        self.assertIn("4096 bytes以下", boundary)
        self.assertIn("8192 bytes以下", boundary)
        self.assertIn("raw outputがmodelへ返る前", boundary)
        self.assertIn("exit code", boundary)
        self.assertIn("required evidence", boundary)
        self.assertIn("完全一時fileを再読しない", boundary)

    def test_profiles_keep_taskspec_and_all_conditions_fixed(self) -> None:
        c81 = verify_bundle(C81)
        c90 = verify_bundle(C90)
        for baseline_name, candidate_name in PROFILE_PAIRS:
            with self.subTest(candidate=candidate_name):
                baseline = json.loads((PROFILES / baseline_name).read_text(encoding="utf-8"))
                candidate = json.loads((PROFILES / candidate_name).read_text(encoding="utf-8"))
                self.assertEqual(baseline["cases"], candidate["cases"])
                self.assertEqual(baseline["comparison_conditions"], candidate["comparison_conditions"])
                self.assertEqual(baseline["evaluation_set"], candidate["evaluation_set"])
                self.assertEqual(baseline["execution"], candidate["execution"])
                self.assertEqual(baseline["scope"], candidate["scope"])
                self.assertEqual(baseline["prompt_set_identity"]["bundle_sha256"], c81["bundle_sha256"])
                self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], c90["bundle_sha256"])

    def test_design_uses_existing_n5_and_preserves_three_kpis(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("TaskSpec、Evaluation set、fixture、oracle", design)
        self.assertIn("F02とF04のtargeted gate", design)
        self.assertIn("通常の標準14項目各`N=5`", design)
        self.assertIn("quality、all-agent token、elapsedの3 KPI", design)
        self.assertIn("公開後44%を直接再現する試験ではない", design)

    def test_f02_result_records_failed_ingress_gate_and_stop(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        self.assertIn("TaskSpec、fixture、oracle", result)
        self.assertIn("acquisition-time projection成立: 0 / 5", result)
        self.assertIn("token `+16,487`（`+5.35%`）", result)
        self.assertIn("elapsed `+25.090`秒（`+23.31%`）", result)
        self.assertIn("targeted_f02_evaluated / stopped", result)
        self.assertIn("F04、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断", result)


if __name__ == "__main__":
    unittest.main()

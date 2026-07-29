from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C85 = ROOT / "prompts/candidates/the-caption-3ce91a4-planning-first-producer-selection-r1"
C86 = ROOT / "prompts/candidates/the-caption-3ce91a4-producer-plan-fast-path-r1"
DESIGN = ROOT / "docs/candidate86-producer-plan-fast-path-design.md"
F02_RESULT = ROOT / "evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-f02-n5_2026-07-29.md"
F04_RESULT = ROOT / "evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-f04-n5_2026-07-29.md"
D01_RESULT = ROOT / "evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-d01-n5_2026-07-29.md"
PROFILES = ROOT / "evaluations/profiles"
PAIR_NAMES = (
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f02-global-m5-n5-r1.json",
        "candidate86-producer-plan-fast-path-v14-reasoning-medium-f02-global-m5-n5-r1.json",
        [{"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"}],
    ),
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f04-global-m5-n5-r1.json",
        "candidate86-producer-plan-fast-path-v14-reasoning-medium-f04-global-m5-n5-r1.json",
        [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}],
    ),
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-d01-global-m5-n5-catalog-fixed-r1.json",
        "candidate86-producer-plan-fast-path-v14-reasoning-medium-d01-global-m5-n5-catalog-fixed-r1.json",
        [{"id": "TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW", "revision": "r1"}],
    ),
)


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if line.startswith("- "):
            label, body = line[2:].split(": ", 1)
            blocks[label] = body
    return blocks


class Candidate86Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate81(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C86)
        self.assertEqual(candidate["prompt_identity"], "the-caption-3ce91a4-producer-plan-fast-path-r1")
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

    def test_changes_only_existing_producer_planning_blocks(self) -> None:
        source = labelled_blocks((C81 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C86 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertNotIn("PLAN", candidate)
        self.assertEqual(
            {label for label in source if source[label] != candidate[label]},
            {"PRODUCER", "OWNER_ROLE", "DECISION_BOUNDARY"},
        )
        for label in (
            "SPEC",
            "TERMINAL",
            "CONTEXT",
            "ROOT",
            "INDEPENDENCE",
            "VALIDATION_CLOSURE",
            "METHOD",
            "RECOVERY",
        ):
            self.assertEqual(candidate[label], source[label])

    def test_has_root_fast_path_without_post_hoc_worker_binding(self) -> None:
        blocks = labelled_blocks((C86 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        producer = blocks["PRODUCER"]
        self.assertIn("初回predicate前", producer)
        self.assertIn("rootまたはworkerをAIが一つbind", producer)
        self.assertIn("Worker利用の指示", producer)
        self.assertIn("rootへ直接bindし、plan artifactを作らない", producer)
        self.assertIn("複数operation", producer)
        self.assertIn("同じwave", producer)
        self.assertIn("同一operationを他producerへ割り当てない", producer)
        self.assertIn("前提が失効した場合だけ再planning", producer)

    def test_expands_waiting_only_for_dependency(self) -> None:
        blocks = labelled_blocks((C86 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertIn("`PRODUCER`でworkerを選択したoperationだけ", blocks["OWNER_ROLE"])
        self.assertIn("相互非依存operationは同一model step", blocks["DECISION_BOUNDARY"])
        self.assertIn("ほかにreadyなroot operationがない場合だけ待つ", blocks["DECISION_BOUNDARY"])

    def test_is_smaller_than_candidate85(self) -> None:
        c85_bytes = len((C85 / "files/AGENTS.md.txt").read_bytes())
        c86_bytes = len((C86 / "files/AGENTS.md.txt").read_bytes())
        self.assertLess(c86_bytes, c85_bytes)

    def test_profiles_reuse_exact_existing_tests_and_conditions(self) -> None:
        c81_manifest = verify_bundle(C81)
        c86_manifest = verify_bundle(C86)
        for baseline_name, candidate_name, expected_cases in PAIR_NAMES:
            with self.subTest(candidate=candidate_name):
                baseline = json.loads((PROFILES / baseline_name).read_text(encoding="utf-8"))
                candidate = json.loads((PROFILES / candidate_name).read_text(encoding="utf-8"))
                self.assertEqual(baseline["cases"], expected_cases)
                self.assertEqual(candidate["cases"], expected_cases)
                self.assertEqual(baseline["comparison_conditions"], candidate["comparison_conditions"])
                self.assertEqual(baseline["evaluation_set"], candidate["evaluation_set"])
                self.assertEqual(baseline["execution"], candidate["execution"])
                self.assertEqual(baseline["scope"], candidate["scope"])
                self.assertEqual(
                    baseline["prompt_set_identity"],
                    {
                        "bundle_sha256": c81_manifest["bundle_sha256"],
                        "name": c81_manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )
                self.assertEqual(
                    candidate["prompt_set_identity"],
                    {
                        "bundle_sha256": c86_manifest["bundle_sha256"],
                        "name": c86_manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )

    def test_design_prebinds_gate_and_state_boundaries(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("既存Evaluation set、TaskSpec、fixture、oracle", design)
        self.assertIn("profile IDだけを替える", design)
        self.assertIn("token差とelapsed差が事前固定した許容幅`0`", design)
        self.assertIn("draft / not_evaluated", design)

    def test_results_preserve_tests_and_apply_cost_gate(self) -> None:
        f02 = F02_RESULT.read_text(encoding="utf-8")
        f04 = F04_RESULT.read_text(encoding="utf-8")
        d01 = D01_RESULT.read_text(encoding="utf-8")
        self.assertIn("試験内容は変更していない", f02)
        self.assertIn("cost_tradeoff", f02)
        self.assertIn("試験内容は変更していない", f04)
        self.assertIn("root_fast_path / root_only", f04)
        self.assertIn("試験内容は変更していない", d01)
        self.assertIn("producer_route_passed / cost_control_failed", d01)
        self.assertIn("標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断", d01)


if __name__ == "__main__":
    unittest.main()

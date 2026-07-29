from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C85 = ROOT / "prompts/candidates/the-caption-3ce91a4-planning-first-producer-selection-r1"
DESIGN = ROOT / "docs/candidate85-planning-first-producer-selection-design.md"
F02_RESULT = ROOT / "evaluations/results/candidate81-candidate85-planning-first-v14-medium-f02-n5_2026-07-28.md"
F04_RESULT = ROOT / "evaluations/results/candidate81-candidate85-planning-first-v14-medium-f04-n5_2026-07-28.md"
PROFILES = ROOT / "evaluations/profiles"
PAIR_NAMES = (
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f02-global-m5-n5-r1.json",
        "candidate85-planning-first-producer-selection-v14-reasoning-medium-f02-global-m5-n5-r1.json",
        [{"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"}],
    ),
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f04-global-m5-n5-r1.json",
        "candidate85-planning-first-producer-selection-v14-reasoning-medium-f04-global-m5-n5-r1.json",
        [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}],
    ),
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-d01-global-m5-n5-catalog-fixed-r1.json",
        "candidate85-planning-first-producer-selection-v14-reasoning-medium-d01-global-m5-n5-catalog-fixed-r1.json",
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


class Candidate85Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate81(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C85)
        self.assertEqual(candidate["prompt_identity"], "the-caption-3ce91a4-planning-first-producer-selection-r1")
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

    def test_changes_only_planning_first_axis(self) -> None:
        source = labelled_blocks((C81 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C85 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertNotIn("PLAN", source)
        self.assertIn("PLAN", candidate)
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

    def test_plans_ai_producer_choice_before_execution(self) -> None:
        blocks = labelled_blocks((C85 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        plan = blocks["PLAN"]
        self.assertIn("未制約operationのrootまたはworker producerをAIが選択済み", plan)
        self.assertIn("producer間scope非重複", plan)
        self.assertIn("execution wave固定済み", plan)
        self.assertIn("`execution_plan_ready=false`の間はproducer binding / predicate実行 / worker起動", plan)
        self.assertIn("criterion owner / risk owner / role / `independent`語列 / 作業名はproducer metadata", plan)
        self.assertIn("execution identityを必須または禁止", plan)

    def test_execution_uses_plan_and_avoids_post_hoc_assignment(self) -> None:
        blocks = labelled_blocks((C85 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertIn("planで選択した各operation", blocks["PRODUCER"])
        self.assertIn("plan前提が失効した場合だけ", blocks["PRODUCER"])
        self.assertIn("同一operationのpredicate実行 / result生成を他producerへ", blocks["PRODUCER"])
        self.assertIn("planでworkerをproducerへ選択したoperation", blocks["OWNER_ROLE"])
        self.assertIn("`delegated_result_ready :=", blocks["OWNER_ROLE"])
        self.assertIn("`wait_ready :=", blocks["DECISION_BOUNDARY"])
        self.assertIn("ほかにreadyなroot operationがない", blocks["DECISION_BOUNDARY"])

    def test_profiles_hold_existing_cases_and_all_non_prompt_conditions_fixed(self) -> None:
        c81_manifest = verify_bundle(C81)
        c85_manifest = verify_bundle(C85)
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
                        "bundle_sha256": c85_manifest["bundle_sha256"],
                        "name": c85_manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )

    def test_design_prebinds_gate_and_preserves_state_boundaries(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("F02 r1、F04 r2、D01 r1の試験内容は変更しない", design)
        self.assertIn("token差とelapsed差が事前固定した許容幅`0`", design)
        self.assertIn("Worker起動だけでは停止しない", design)
        self.assertIn("draft / not_evaluated", design)

    def test_results_apply_cost_gate_without_worker_count_failure(self) -> None:
        f02 = F02_RESULT.read_text(encoding="utf-8")
        f04 = F04_RESULT.read_text(encoding="utf-8")
        self.assertIn("TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1", f02)
        self.assertIn("quality_passed / cost_tradeoff", f02)
        self.assertIn("C85: root-only 5 / 5、child session 0", f02)
        self.assertIn("TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2", f04)
        self.assertIn("quality_passed / cost_control_failed", f04)
        self.assertIn("両条件ともroot-only", f04)
        self.assertIn("D01 profileは未実行", f04)


if __name__ == "__main__":
    unittest.main()

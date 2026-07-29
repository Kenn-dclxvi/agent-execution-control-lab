from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C86 = ROOT / "prompts/candidates/the-caption-3ce91a4-producer-plan-fast-path-r1"
C87 = ROOT / "prompts/candidates/the-caption-3ce91a4-producer-local-invocation-wave-r1"
DESIGN = ROOT / "docs/candidate87-producer-local-invocation-wave-design.md"
RESULT = ROOT / "evaluations/results/candidate86-candidate87-producer-local-invocation-wave-v14-medium-d01-n5_2026-07-29.md"
F02_RESULT = ROOT / "evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f02-n5_2026-07-29.md"
F04_RESULT = ROOT / "evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f04-n5_2026-07-29.md"
STANDARD14_RESULT = ROOT / "evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md"
STANDARD14_PROFILES = (
    "candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-r1.json",
    "candidate87-producer-local-invocation-wave-v14-reasoning-medium-standard14-global-m24-n5-r1.json",
)
PROFILES = ROOT / "evaluations/profiles"
PAIR_NAMES = (
    (
        "candidate86-producer-plan-fast-path-v14-reasoning-medium-f02-global-m5-n5-r1.json",
        "candidate87-producer-local-invocation-wave-v14-reasoning-medium-f02-global-m5-n5-r1.json",
        [{"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"}],
    ),
    (
        "candidate86-producer-plan-fast-path-v14-reasoning-medium-f04-global-m5-n5-r1.json",
        "candidate87-producer-local-invocation-wave-v14-reasoning-medium-f04-global-m5-n5-r1.json",
        [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}],
    ),
    (
        "candidate86-producer-plan-fast-path-v14-reasoning-medium-d01-global-m5-n5-catalog-fixed-r1.json",
        "candidate87-producer-local-invocation-wave-v14-reasoning-medium-d01-global-m5-n5-catalog-fixed-r1.json",
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


class Candidate87Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate86(self) -> None:
        source = verify_bundle(C86)
        candidate = verify_bundle(C87)
        self.assertEqual(candidate["prompt_identity"], "the-caption-3ce91a4-producer-local-invocation-wave-r1")
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

    def test_changes_only_decision_boundary(self) -> None:
        source = labelled_blocks((C86 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C87 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(
            {label for label in source if source[label] != candidate[label]},
            {"DECISION_BOUNDARY"},
        )
        for label in source.keys() - {"DECISION_BOUNDARY"}:
            self.assertEqual(candidate[label], source[label])

    def test_batches_producer_local_nondependent_invocations(self) -> None:
        blocks = labelled_blocks((C87 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        boundary = blocks["DECISION_BOUNDARY"]
        self.assertIn("root / workerを問わず", boundary)
        self.assertIn("同一operation内のinvocationを別operationへ読み替えない", boundary)
        self.assertIn("別model stepへ分ける意味ではない", boundary)
        self.assertIn("一つのcustom exec wrapperから個別invocationとして同時発行", boundary)
        self.assertIn("全resultを一度だけmodelへ返して次を一度判断", boundary)
        self.assertIn("明示order / fail-stop dependencyは`VALIDATION_CLOSURE`に従う", boundary)

    def test_profiles_reuse_exact_existing_tests_and_conditions(self) -> None:
        c86_manifest = verify_bundle(C86)
        c87_manifest = verify_bundle(C87)
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
                        "bundle_sha256": c86_manifest["bundle_sha256"],
                        "name": c86_manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )
                self.assertEqual(
                    candidate["prompt_set_identity"],
                    {
                        "bundle_sha256": c87_manifest["bundle_sha256"],
                        "name": c87_manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )

    def test_standard14_profiles_change_only_prompt_identity(self) -> None:
        baseline = json.loads((PROFILES / STANDARD14_PROFILES[0]).read_text(encoding="utf-8"))
        candidate = json.loads((PROFILES / STANDARD14_PROFILES[1]).read_text(encoding="utf-8"))
        self.assertEqual(len(baseline["cases"]), 14)
        self.assertEqual(baseline["cases"], candidate["cases"])
        self.assertEqual(baseline["comparison_conditions"], candidate["comparison_conditions"])
        self.assertEqual(baseline["evaluation_set"], candidate["evaluation_set"])
        self.assertEqual(baseline["execution"], candidate["execution"])
        self.assertEqual(
            baseline["comparison_conditions"]["quality_rating"]["contract_id"],
            "outcome-terminal-state-evidence-owner-diagnostic-v14",
        )
        self.assertEqual(baseline["prompt_set_identity"]["name"], "the-caption-3ce91a4-validation-wrapper-precedence-r1")
        self.assertEqual(candidate["prompt_set_identity"]["name"], "the-caption-3ce91a4-producer-local-invocation-wave-r1")

    def test_design_freezes_one_axis_and_gate(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("既存Evaluation set、TaskSpec、fixture、oracle", design)
        self.assertIn("`DECISION_BOUNDARY`だけを置換", design)
        self.assertIn("C87 minus C86のtoken / elapsed中央値がともに`0`以下", design)
        self.assertIn("新しいcase、fixture、oracle、Evaluation setは作成しない", design)
        self.assertIn("standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided", design)
        self.assertIn("5 / 5 score `4`", design)

    def test_result_preserves_d01_and_records_append_only_correction(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        self.assertIn("試験内容は変更していない", result)
        self.assertIn("C87 result（当初登録・誤採点履歴）: `06e34a45334343a1ba9d55ba219bae1e`", result)
        self.assertIn("C87 result（契約binding訂正）: `27b73ffe18bf47a99e15541c91c9d6e5`", result)
        self.assertIn("quality gate: `passed`（score `4 = 5`）", result)
        self.assertIn("child custom exec call合計 | `41` | `12`", result)
        self.assertIn("Candidate87 state: `targeted_d01_evaluated / qualification_passed / f02_not_run`", result)
        self.assertIn("F02、F04、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断", result)

    def test_f02_result_preserves_test_and_proceeds_by_median_gate(self) -> None:
        result = F02_RESULT.read_text(encoding="utf-8")
        self.assertIn("試験内容は変更していない", result)
        self.assertIn("C87 result: `e4499be29cf444cdab25aa6869bc9102`", result)
        self.assertIn("5 / 5件がvalid・rateable・score `4`", result)
        self.assertIn("token `-16,209`（`-5.26%`）", result)
        self.assertIn("elapsed `-11.446`秒（`-10.63%`）", result)
        self.assertIn("token合計はCandidate81比`+233,116`（`+16.06%`）", result)
        self.assertIn("Candidate87 state: `targeted_d01_f02_evaluated / proceeding_to_f04`", result)

    def test_f04_result_preserves_test_and_passes_targeted_gate(self) -> None:
        result = F04_RESULT.read_text(encoding="utf-8")
        self.assertIn("試験内容は変更していない", result)
        self.assertIn("C87 result: `3ffc65bba5754fc38851c5f26a711f79`", result)
        self.assertIn("5 / 5件がvalid・rateable・score `4`", result)
        self.assertIn("token `+29,165`（`+15.48%`）", result)
        self.assertIn("elapsed `-12.501`秒（`-12.62%`）", result)
        self.assertIn("missing_machine_bound_exit_code", result)
        self.assertIn("Candidate87 state: `targeted_d01_f02_f04_evaluated / targeted_gate_passed`", result)

    def test_standard14_result_preserves_compatibility_and_state_boundaries(self) -> None:
        result = STANDARD14_RESULT.read_text(encoding="utf-8")
        self.assertIn("C81 result: `792bd514c13e429f8eec16d04e4c4d51`", result)
        self.assertIn("C87 result: `dba6bcb26e7b4c90a79db13696c4ea1e`", result)
        self.assertIn("| C81 | 70 / 70 |", result)
        self.assertIn("| C87 | 70 / 70 |", result)
        self.assertIn("token `+117,040`（`+6.09%`）", result)
        self.assertIn("elapsed `+12.330`秒（`+1.35%`）", result)
        self.assertIn("root-only | 70 / 70 | 65 / 70", result)
        self.assertIn("missing_machine_bound_exit_code", result)
        self.assertIn("standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided", result)


if __name__ == "__main__":
    unittest.main()

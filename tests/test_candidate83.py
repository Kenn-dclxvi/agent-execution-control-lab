from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C82 = ROOT / "prompts/candidates/the-caption-3ce91a4-producer-gate-deduplication-r1"
C83 = ROOT / "prompts/candidates/the-caption-3ce91a4-delegation-value-boundary-r1"
DESIGN = ROOT / "docs/candidate83-delegation-value-boundary-design.md"
RESULT = ROOT / "evaluations/results/candidate83-delegation-value-boundary-v14-medium-f02-n5_2026-07-28.md"
PROFILES = ROOT / "evaluations/profiles"
EXPLICIT_ONLY = "TaskSpecが独立したproducer executionを明示した場合だけ"
TARGETED_PROFILES = (
    PROFILES / "candidate83-delegation-value-boundary-v14-reasoning-medium-delegation-value-f02-global-m5-n5-r1.json",
    PROFILES / "candidate83-delegation-value-boundary-v14-reasoning-medium-delegation-value-f04-global-m5-n5-r1.json",
    PROFILES / "candidate83-delegation-value-boundary-v14-reasoning-medium-explicit-producer-d01-global-m5-n5-catalog-fixed-r1.json",
)


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if line.startswith("- "):
            label, body = line[2:].split(": ", 1)
            blocks[label] = body
    return blocks


class Candidate83Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate82(self) -> None:
        source = verify_bundle(C82)
        candidate = verify_bundle(C83)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-delegation-value-boundary-r1",
        )
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

    def test_replaces_only_owner_role(self) -> None:
        source = labelled_blocks((C82 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C83 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(list(candidate), list(source))
        self.assertEqual(
            {label for label in source if source[label] != candidate[label]},
            {"OWNER_ROLE"},
        )
        self.assertEqual(candidate["PRODUCER"], source["PRODUCER"])
        self.assertEqual(candidate["CONTEXT"], source["CONTEXT"])
        self.assertEqual(candidate["ROOT"], source["ROOT"])
        self.assertEqual(candidate["VALIDATION_CLOSURE"], source["VALIDATION_CLOSURE"])

    def test_keeps_ai_choice_and_rejects_duplicate_work(self) -> None:
        owner = labelled_blocks(
            (C83 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        )["OWNER_ROLE"]
        self.assertNotIn(EXPLICIT_ONLY, owner)
        self.assertIn("delegation_value_ready :=", owner)
        self.assertIn("rootが同じpredicateを実行しない", owner)
        for value_source in (
            "TaskSpecが独立性を要求",
            "相互非依存operationを並列化",
            "rootが処理する必要のないcontextをworkerへ分割",
            "worker固有capabilityが必要",
        ):
            self.assertIn(value_source, owner)
        self.assertIn(
            "criterion owner語列だけでは`delegation_value_ready`を成立させない",
            owner,
        )
        self.assertIn("`delegation_value_ready=false`ならrootをproducerへbindする", owner)
        self.assertIn("trueなら起動前にworkerのtask identityをproducerへbind", owner)
        self.assertIn("`delegated_result_ready :=", owner)

    def test_design_preserves_evaluation_boundaries(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for case_id in ("F02", "F04", "D01", "A06"):
            self.assertIn(case_id, design)
        self.assertIn("targeted評価済み、採用済み、release済み、本体反映済みを意味しない", design)
        self.assertIn("Candidate82 B20の公式resultと`stopped`履歴は変更しない", design)

    def test_v14_targeted_profiles_bind_candidate83_and_fixed_conditions(self) -> None:
        candidate_manifest = verify_bundle(C83)
        for candidate_path in TARGETED_PROFILES:
            with self.subTest(candidate_profile=candidate_path.name):
                candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
                self.assertEqual(
                    candidate["comparison_conditions"]["executor_parameters"]["reasoning_effort"],
                    "medium",
                )
                self.assertEqual(
                    candidate["comparison_conditions"]["quality_rating"]["contract_id"],
                    "outcome-terminal-state-evidence-owner-diagnostic-v14",
                )
                self.assertEqual(candidate["comparison_conditions"]["repetition_condition"]["iterations"], 5)
                self.assertEqual(
                    candidate["prompt_set_identity"],
                    {
                        "bundle_sha256": candidate_manifest["bundle_sha256"],
                        "name": candidate_manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )

    def test_f02_result_preserves_quality_route_and_stop_boundaries(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        self.assertIn("c93d64261dd24d43aaa30caaa5da9081", result)
        self.assertIn("5 / 5", result)
        self.assertIn("合計6 child session", result)
        self.assertIn("targeted_f02_evaluated / stopped", result)
        self.assertIn("F04、D01、A06、標準14、採用、release、THE-CAPTION本体反映へ進めない", result)
        self.assertIn("Candidate82をv14で再実行しておらず", result)


if __name__ == "__main__":
    unittest.main()

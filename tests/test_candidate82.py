from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C82 = ROOT / "prompts/candidates/the-caption-3ce91a4-producer-gate-deduplication-r1"
PROFILES = ROOT / "evaluations/profiles"
RESULT = (
    ROOT
    / "evaluations/results/candidate81-candidate82-producer-gate-deduplication-v13-medium-f10-d01-n5_2026-07-28.md"
)
STANDARD14_RESULT = (
    ROOT
    / "evaluations/results/candidate81-candidate82-producer-gate-deduplication-v13-medium-standard14-n5_2026-07-28.md"
)
PROFILE_PAIRS = (
    (
        PROFILES
        / "candidate81-validation-wrapper-precedence-v13-reasoning-medium-fixed-evidence-review-f10-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate82-producer-gate-deduplication-v13-reasoning-medium-fixed-evidence-review-f10-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate81-validation-wrapper-precedence-v13-reasoning-medium-explicit-producer-d01-global-m5-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate82-producer-gate-deduplication-v13-reasoning-medium-explicit-producer-d01-global-m5-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate81-validation-wrapper-precedence-v13-reasoning-medium-standard14-global-m24-n5-r1.json",
        PROFILES
        / "candidate82-producer-gate-deduplication-v13-reasoning-medium-standard14-global-m24-n5-r1.json",
    ),
)
P3 = (
    "TaskSpecが独立したproducer executionを明示した場合だけ、"
    "その指定identityをproducer role identityへbindする。"
)


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if line.startswith("- "):
            label, body = line[2:].split(": ", 1)
            blocks[label] = body
    return blocks


class Candidate82Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate81(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C82)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-producer-gate-deduplication-r1",
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

    def test_removes_only_producer_p3(self) -> None:
        source_text = (C81 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (C82 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(source_text.count(P3), 1)
        self.assertEqual(candidate_text, source_text.replace(P3, ""))

    def test_retains_canonical_gate_and_candidate81_topology(self) -> None:
        source = labelled_blocks((C81 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C82 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(list(candidate), list(source))
        self.assertEqual(
            {label for label in source if source[label] != candidate[label]},
            {"PRODUCER"},
        )
        self.assertNotIn(P3, candidate["PRODUCER"])
        self.assertIn(
            "TaskSpecが独立したproducer executionを明示した場合だけ、"
            "起動前にそのexecution identityをtask identityとしてproducerへbindし、"
            "predicate前に対応workerを起動する",
            candidate["OWNER_ROLE"],
        )
        self.assertEqual(candidate["VALIDATION_CLOSURE"], source["VALIDATION_CLOSURE"])

    def test_targeted_profile_pairs_change_only_prompt_identity(self) -> None:
        candidate_manifest = verify_bundle(C82)
        for source_path, candidate_path in PROFILE_PAIRS:
            with self.subTest(candidate_profile=candidate_path.name):
                source = json.loads(source_path.read_text(encoding="utf-8"))
                candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
                for profile in (source, candidate):
                    self.assertEqual(
                        profile["comparison_conditions"]["executor_parameters"][
                            "reasoning_effort"
                        ],
                        "medium",
                    )
                    self.assertEqual(
                        profile["comparison_conditions"]["quality_rating"]["contract_id"],
                        "outcome-abstract-condition-preserving-owner-diagnostic-v13",
                    )
                self.assertEqual(
                    candidate["prompt_set_identity"],
                    {
                        "bundle_sha256": candidate_manifest["bundle_sha256"],
                        "name": candidate_manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )
                comparable_source = copy.deepcopy(source)
                comparable_candidate = copy.deepcopy(candidate)
                for profile in (comparable_source, comparable_candidate):
                    profile.pop("profile_id")
                    profile.pop("prompt_set_identity")
                self.assertEqual(comparable_candidate, comparable_source)

    def test_targeted_result_preserves_decision_boundaries(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        for result_id in (
            "f63d261635c64d82860628f4f0875a5f",
            "67f7687ba8c944408422e705b5e90e01",
            "d11c7f2b08be4f1088bd684d9a20a51c",
            "b07f9bc31b134b15acd81f378b66a61b",
            "513a3cd0f0d14223a174b82271a6340a",
        ):
            self.assertIn(result_id, result)
        self.assertIn("targeted_evaluated / targeted_gate_passed", result)
        self.assertIn("標準14、採用、release、THE-CAPTION本体反映は未判断、未実施", result)

    def test_standard14_result_preserves_registration_and_release_boundaries(self) -> None:
        result = STANDARD14_RESULT.read_text(encoding="utf-8")
        self.assertIn("d97458bb526b41b094f92a5c35409326", result)
        self.assertIn("039b1b1afa6c41ef9012eb93860c594b", result)
        self.assertIn("70 / 70", result)
        self.assertIn("standard14_evaluated / quality_gate_passed / targeted_gate_passed", result)
        self.assertIn("採用、release、THE-CAPTION本体反映は未判断、未実施", result)


if __name__ == "__main__":
    unittest.main()

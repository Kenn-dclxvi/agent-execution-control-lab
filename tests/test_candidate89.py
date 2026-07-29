from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C87 = ROOT / "prompts/candidates/the-caption-3ce91a4-producer-local-invocation-wave-r1"
C89 = ROOT / "prompts/candidates/the-caption-3ce91a4-dispatch-time-worker-admission-r1"
DESIGN = ROOT / "docs/candidate89-dispatch-time-worker-admission-design.md"
RESULT = ROOT / "evaluations/results/candidate81-candidate89-dispatch-time-worker-admission-v14-medium-f02-n5_2026-07-29.md"
PROFILES = ROOT / "evaluations/profiles"
PROFILE_PAIRS = (
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f02-global-m5-n5-r1.json",
        "candidate89-dispatch-time-worker-admission-v14-reasoning-medium-f02-global-m5-n5-r1.json",
    ),
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f04-global-m5-n5-r1.json",
        "candidate89-dispatch-time-worker-admission-v14-reasoning-medium-f04-global-m5-n5-r1.json",
    ),
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-d01-global-m5-n5-catalog-fixed-r1.json",
        "candidate89-dispatch-time-worker-admission-v14-reasoning-medium-d01-global-m5-n5-catalog-fixed-r1.json",
    ),
)


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if line.startswith("- "):
            label, body = line[2:].split(": ", 1)
            blocks[label] = body
    return blocks


class Candidate89Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate87(self) -> None:
        source = verify_bundle(C87)
        candidate = verify_bundle(C89)
        self.assertEqual(candidate["prompt_identity"], "the-caption-3ce91a4-dispatch-time-worker-admission-r1")
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
        source = labelled_blocks((C87 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C89 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(
            {label for label in source if source[label] != candidate[label]},
            {"DECISION_BOUNDARY"},
        )
        for label in source.keys() - {"DECISION_BOUNDARY"}:
            self.assertEqual(candidate[label], source[label])

    def test_discretionary_worker_is_gated_at_dispatch(self) -> None:
        boundary = labelled_blocks((C89 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))["DECISION_BOUNDARY"]
        self.assertIn("root_parallel_inflight :=", boundary)
        self.assertIn("root operationのinvocationを先に発行済み", boundary)
        self.assertIn("terminal resultが未受領", boundary)
        self.assertIn("同じready waveへ置けるというplanだけでは成立しない", boundary)
        self.assertIn("観測したscheduler decisionでだけWorkerへbindして起動", boundary)
        self.assertIn("それまではWorker候補operationをunboundに保ち", boundary)
        self.assertIn("root operationがterminalになった場合はAI裁量Workerを起動せず", boundary)

    def test_explicit_producer_constraint_is_exempt(self) -> None:
        boundary = labelled_blocks((C89 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))["DECISION_BOUNDARY"]
        self.assertIn("TaskSpecが別execution identityのresultをrequired outcomeとして明示しないAI裁量Worker", boundary)
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("明示必須経路はdispatch gateの対象外", design)
        self.assertIn("既存D01 r1", design)

    def test_design_freezes_existing_cases_and_prebinds_stop(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate88を継承しない", design)
        self.assertIn("`DECISION_BOUNDARY`だけを置換", design)
        self.assertIn("既存F02 r1", design)
        self.assertIn("既存F04 r2", design)
        self.assertIn("既存D01 r1", design)
        self.assertIn("新しいcase、fixture、oracle、Evaluation setは作成しない", design)
        self.assertIn("`root_parallel_inflight=false`での起動が1件でもあれば停止", design)

    def test_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C89)
        for baseline_name, candidate_name in PROFILE_PAIRS:
            with self.subTest(candidate=candidate_name):
                baseline = json.loads((PROFILES / baseline_name).read_text(encoding="utf-8"))
                candidate = json.loads((PROFILES / candidate_name).read_text(encoding="utf-8"))
                self.assertEqual(baseline["cases"], candidate["cases"])
                self.assertEqual(baseline["comparison_conditions"], candidate["comparison_conditions"])
                self.assertEqual(baseline["evaluation_set"], candidate["evaluation_set"])
                self.assertEqual(baseline["execution"], candidate["execution"])
                self.assertEqual(baseline["scope"], candidate["scope"])
                self.assertEqual(
                    candidate["prompt_set_identity"],
                    {
                        "bundle_sha256": manifest["bundle_sha256"],
                        "name": manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )

    def test_result_records_prebound_stop(self) -> None:
        manifest = verify_bundle(C89)
        result = RESULT.read_text(encoding="utf-8")
        self.assertEqual(manifest["artifact"]["evaluation_status"], "targeted_f02_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "stopped")
        self.assertIn("C89 result: `67159f3586f04990ba9ffa75ab87279a`", result)
        self.assertIn("5 / 5件でvalid・rateable・score `4`", result)
        self.assertIn("`root_parallel_inflight`は4 / 4件で`false`", result)
        self.assertIn("token `+19,861`（`+6.45%`）", result)
        self.assertIn("elapsed `+4.453`秒（`+4.14%`）", result)
        self.assertIn("Candidate89 state: `targeted_f02_evaluated / stopped`", result)
        self.assertIn("F04、D01、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断", result)


if __name__ == "__main__":
    unittest.main()

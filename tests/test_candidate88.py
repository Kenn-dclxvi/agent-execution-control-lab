from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C87 = ROOT / "prompts/candidates/the-caption-3ce91a4-producer-local-invocation-wave-r1"
C88 = ROOT / "prompts/candidates/the-caption-3ce91a4-parallel-worker-admission-r1"
DESIGN = ROOT / "docs/candidate88-parallel-worker-admission-design.md"
RESULT = ROOT / "evaluations/results/candidate81-candidate88-parallel-worker-admission-v14-medium-f02-n5_2026-07-29.md"
PROFILES = ROOT / "evaluations/profiles"
PROFILE_PAIRS = (
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f02-global-m5-n5-r1.json",
        "candidate88-parallel-worker-admission-v14-reasoning-medium-f02-global-m5-n5-r1.json",
    ),
    (
        "candidate81-planning-first-producer-selection-v14-reasoning-medium-f04-global-m5-n5-r1.json",
        "candidate88-parallel-worker-admission-v14-reasoning-medium-f04-global-m5-n5-r1.json",
    ),
)


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if line.startswith("- "):
            label, body = line[2:].split(": ", 1)
            blocks[label] = body
    return blocks


class Candidate88Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate87(self) -> None:
        source = verify_bundle(C87)
        candidate = verify_bundle(C88)
        self.assertEqual(candidate["prompt_identity"], "the-caption-3ce91a4-parallel-worker-admission-r1")
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

    def test_changes_only_producer(self) -> None:
        source = labelled_blocks((C87 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C88 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(
            {label for label in source if source[label] != candidate[label]},
            {"PRODUCER"},
        )
        for label in source.keys() - {"PRODUCER"}:
            self.assertEqual(candidate[label], source[label])

    def test_discretionary_worker_requires_same_wave_root_operation(self) -> None:
        producer = labelled_blocks((C88 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))["PRODUCER"]
        self.assertIn("parallel_worker_ready :=", producer)
        self.assertIn("Worker operationとroot operationが非重複", producer)
        self.assertIn("相互非依存", producer)
        self.assertIn("同じready waveで同時開始可能", producer)
        self.assertIn("Worker result consumerが固定済み", producer)
        self.assertIn("Worker resultに依存するroot operationを並行operationに数えず", producer)
        self.assertIn("Worker起動後に並行可能性を探さない", producer)
        self.assertIn("`parallel_worker_ready=false`ならrootへbindする", producer)

    def test_explicit_producer_constraint_is_separate(self) -> None:
        producer = labelled_blocks((C88 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))["PRODUCER"]
        self.assertIn("別execution identityのresultがrequired outcome", producer)
        self.assertIn("TaskSpecが別execution identityのresultを明示したoperationは指定identityへbind", producer)

    def test_design_freezes_existing_tests_and_prebinds_gate(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("`PRODUCER`だけを置換", design)
        self.assertIn("既存F02 r1とF04 r2", design)
        self.assertIn("既存D01 r1", design)
        self.assertIn("逐次Workerが1件でもあれば停止", design)
        self.assertIn("新しいcase、fixture、oracle、Evaluation setは作成しない", design)
        self.assertIn("70 / 70 score `4`", design)
        self.assertIn("token・elapsed集約中央値がともにCandidate81以下", design)

    def test_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C88)
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
        manifest = verify_bundle(C88)
        result = RESULT.read_text(encoding="utf-8")
        self.assertEqual(manifest["artifact"]["evaluation_status"], "targeted_f02_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "stopped")
        self.assertIn("C88 result: `97ef616cca42433792dc30885a314b7a`", result)
        self.assertIn("5 / 5件でvalid・rateable・score `4`", result)
        self.assertIn("sequential Worker 2件", result)
        self.assertIn("token `+80,914`（`+26.28%`）", result)
        self.assertIn("elapsed `+8.646`秒（`+8.03%`）", result)
        self.assertIn("Candidate88 state: `targeted_f02_evaluated / stopped`", result)
        self.assertIn("F04、D01、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断", result)


if __name__ == "__main__":
    unittest.main()

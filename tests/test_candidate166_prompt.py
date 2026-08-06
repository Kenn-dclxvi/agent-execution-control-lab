from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C165 = ROOT / "prompts/candidates/the-caption-3ce91a4-review-result-admission-r1"
C166 = ROOT / "prompts/candidates/the-caption-3ce91a4-prior-evaluation-review-admission-r1"
PROFILE = ROOT / "evaluations/profiles/candidate166-prior-evaluation-review-admission-r1-medium-m24-n5-cli0146.json"
C165_PROFILE = ROOT / "evaluations/profiles/candidate165-review-result-admission-r1-medium-m24-n5-cli0146.json"


def controls(path: Path) -> dict[str, str]:
    return {
        line[2:].split(":", 1)[0]: line
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ":" in line
    }


class Candidate166PromptTest(unittest.TestCase):
    def test_direct_child_changes_only_root_agents(self) -> None:
        source = verify_bundle(C165)
        candidate = verify_bundle(C166)
        self.assertEqual(candidate["prompt_identity"], "the-caption-3ce91a4-prior-evaluation-review-admission-r1")
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": source["prompt_identity"],
        })
        before = {entry["target"]: entry for entry in source["files"]}
        after = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual([target for target in before if before[target] != after[target]], ["AGENTS.md"])

    def test_only_review_admission_changes(self) -> None:
        before = controls(C165 / "files/AGENTS.md.txt")
        after = controls(C166 / "files/AGENTS.md.txt")
        self.assertEqual(set(after), set(before))
        for label in before:
            if label != "REVIEW_ADMISSION":
                self.assertEqual(after[label], before[label], label)

    def test_independent_reviewer_switch_depends_on_prior_evaluation(self) -> None:
        before = controls(C165 / "files/AGENTS.md.txt")["REVIEW_ADMISSION"]
        after = controls(C166 / "files/AGENTS.md.txt")["REVIEW_ADMISSION"]

        self.assertIn("rootがreview対象artifactのproducerでない", before)
        self.assertNotIn("rootがreview対象artifactのproducerでない", after)
        for text in (
            "review_context_clean :=",
            "同じreview criterion",
            "review_context_clean=true",
            "review_context_clean=false",
            "実装または調査した事実だけでは独立reviewerへ切り替えない",
            "forbidden input",
            "terminal resultはrootが再生成しない",
        ):
            self.assertIn(text, after)

    def test_result_admission_is_preserved_exactly(self) -> None:
        before = controls(C165 / "files/AGENTS.md.txt")
        after = controls(C166 / "files/AGENTS.md.txt")
        self.assertEqual(after["RESULT_ADMISSION"], before["RESULT_ADMISSION"])

    def test_review4_profile_changes_only_profile_and_prompt_identity(self) -> None:
        source = json.loads(C165_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            candidate["profile_id"],
            "candidate166-prior-evaluation-review-admission-r1-medium-m24-n5-cli0146",
        )
        self.assertEqual(candidate["prompt_set_identity"], {
            "name": "the-caption-3ce91a4-prior-evaluation-review-admission-r1",
            "revision": "r1",
            "bundle_sha256": "c6fa0409bb1061644092dd3e37940b3ef6fb712200c1543040f1cc4665b0d2c0",
        })
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        for key in source.keys() - {"profile_id", "prompt_set_identity", "comparison_conditions"}:
            self.assertEqual(candidate[key], source[key], key)
        before_conditions = source["comparison_conditions"]
        after_conditions = candidate["comparison_conditions"]
        for key in before_conditions.keys() - {"task_spec"}:
            self.assertEqual(after_conditions[key], before_conditions[key], key)
        self.assertEqual(
            after_conditions["task_spec"] | {"source": before_conditions["task_spec"]["source"]},
            before_conditions["task_spec"],
        )


if __name__ == "__main__":
    unittest.main()

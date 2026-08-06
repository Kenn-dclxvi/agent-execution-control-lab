from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C147 = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
C164 = ROOT / "prompts/candidates/the-caption-3ce91a4-autonomous-review-admission-r1"


def control_lines(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- ") or ":" not in line:
            continue
        label = line[2:].split(":", 1)[0]
        result[label] = line
    return result


class Candidate164PromptTest(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate147(self) -> None:
        source = verify_bundle(C147)
        candidate = verify_bundle(C164)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-autonomous-review-admission-r1",
        )
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )

        source_files = {entry["target"]: entry for entry in source["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        changed = [
            target
            for target in sorted(source_files)
            if source_files[target] != candidate_files[target]
        ]
        self.assertEqual(changed, ["AGENTS.md"])

    def test_only_review_admission_and_its_producer_hooks_change(self) -> None:
        source = control_lines(C147 / "files/AGENTS.md.txt")
        candidate = control_lines(C164 / "files/AGENTS.md.txt")

        self.assertNotIn("REVIEW_ADMISSION", source)
        self.assertIn("REVIEW_ADMISSION", candidate)
        for label in source:
            if label not in {"PRODUCER", "OWNER_ROLE"}:
                self.assertEqual(candidate[label], source[label], label)

    def test_review_admission_binds_need_and_context_cleanliness(self) -> None:
        candidate = control_lines(C164 / "files/AGENTS.md.txt")
        admission = candidate["REVIEW_ADMISSION"]

        for required in (
            "review_required :=",
            "review_context_clean :=",
            "review_required=false",
            "review_context_clean=true",
            "review_context_clean=false",
            "one independent quality reviewer",
            "forbidden input",
            "terminal resultはrootが再生成しない",
        ):
            self.assertIn(required, admission)

        for forbidden_packet_input in (
            "producer / root / 他reviewerのfinding",
            "disposition",
            "completion評価",
        ):
            self.assertIn(forbidden_packet_input, admission)

    def test_non_root_files_are_identity_preserving(self) -> None:
        source = verify_bundle(C147)
        candidate = verify_bundle(C164)
        source_files = {entry["target"]: entry for entry in source["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}

        self.assertEqual(set(candidate_files), set(source_files))
        for target in source_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], source_files[target], target)


if __name__ == "__main__":
    unittest.main()

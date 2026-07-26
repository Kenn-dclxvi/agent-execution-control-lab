from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C71 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
C78 = ROOT / "prompts/candidates/the-caption-3ce91a4-project-index-navigation-r1"
C71_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate71-validation-closure-v13-standard14-global-m24-n5-r1.json"
)
C78_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate78-project-index-navigation-v13-standard14-global-m24-n5-r1.json"
)

PROJECT_INDEX = (
    "- PROJECT_INDEX: required outcomeに必要なproject / command / architecture / environment / "
    "testingの静的事実がTaskSpecで未解決の場合、repository-wide探索より先に"
    "`docs/reference/project-contexts/the-caption.txt`を索引として参照する。TaskSpec、"
    "path-scoped `AGENTS.md`、対象source / test、git stateを置換しない。\n"
)


def labelled_lines(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate78Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate71(self) -> None:
        source = verify_bundle(C71)
        candidate = verify_bundle(C78)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-project-index-navigation-r1",
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

    def test_adds_only_project_index_after_spec(self) -> None:
        source_text = (C71 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (C78 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        expected = source_text.replace("- PRODUCER:", PROJECT_INDEX + "- PRODUCER:")
        self.assertEqual(candidate_text, expected)

        source = labelled_lines(source_text)
        candidate = labelled_lines(candidate_text)
        self.assertEqual(
            list(candidate),
            [
                "SPEC",
                "PROJECT_INDEX",
                "PRODUCER",
                "TERMINAL",
                "CONTEXT",
                "OWNER_ROLE",
                "ROOT",
                "INDEPENDENCE",
                "DECISION_BOUNDARY",
                "VALIDATION_CLOSURE",
                "METHOD",
                "RECOVERY",
            ],
        )
        self.assertEqual({label: candidate[label] for label in source}, source)

    def test_project_index_is_navigation_not_execution_method(self) -> None:
        invariant = labelled_lines(
            (C78 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        )["PROJECT_INDEX"]
        self.assertIn("TaskSpecで未解決", invariant)
        self.assertIn("repository-wide探索より先", invariant)
        self.assertIn("docs/reference/project-contexts/the-caption.txt", invariant)
        self.assertIn("path-scoped `AGENTS.md`", invariant)
        self.assertIn("対象source / test", invariant)
        self.assertIn("git stateを置換しない", invariant)
        for method_term in (
            "same model step",
            "tool call",
            "shell command",
            "parallel",
            "batch",
            "worker",
        ):
            self.assertNotIn(method_term, invariant)

    def test_manifest_keeps_construction_state(self) -> None:
        manifest = json.loads((C78 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["artifact"]["baseline_identity"],
            "the-caption-3ce91a4-validation-closure-r1",
        )
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "draft")
        self.assertEqual(
            manifest["provenance"]["evaluation_status"],
            "not_evaluated",
        )
        self.assertEqual(
            manifest["provenance"]["runtime_projection_status"],
            "not_projected",
        )

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C78)
        source = json.loads(C71_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C78_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(candidate["cases"]), 14)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": manifest["bundle_sha256"],
                "name": manifest["prompt_identity"],
                "revision": "r1",
            },
        )
        comparable_source = copy.deepcopy(source)
        comparable_candidate = copy.deepcopy(candidate)
        for profile in (comparable_source, comparable_candidate):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(comparable_candidate, comparable_source)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C71 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
C79 = ROOT / "prompts/candidates/the-caption-3ce91a4-ordered-validation-wave-r1"
C71_PROFILE = ROOT / "evaluations/profiles/candidate71-validation-closure-v13-reasoning-medium-ordered-validation-wave-f04-global-m5-n5-r1.json"
C79_PROFILE = ROOT / "evaluations/profiles/candidate79-ordered-validation-wave-v13-reasoning-medium-f04-global-m5-n5-r1.json"


def labelled_lines(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate79Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate71(self) -> None:
        source = verify_bundle(C71)
        candidate = verify_bundle(C79)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-ordered-validation-wave-r1",
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

    def test_replaces_only_validation_closure(self) -> None:
        source = labelled_lines((C71 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_lines((C79 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(list(candidate), list(source))
        self.assertEqual(
            {label: candidate[label] for label in source if label != "VALIDATION_CLOSURE"},
            {label: source[label] for label in source if label != "VALIDATION_CLOSURE"},
        )
        invariant = candidate["VALIDATION_CLOSURE"]
        self.assertIn("dependency order", invariant)
        self.assertIn("順序付き個別invocation群", invariant)
        self.assertIn("先行success時だけ後続を発行", invariant)
        self.assertIn("同一model stepから発行", invariant)
        self.assertIn("全resultを一度だけmodelへ返す", invariant)
        self.assertIn("read / validationを追加せずterminalを判断", invariant)
        for case_specific_term in ("F04", "npm", "lint", "build", "exec_command"):
            self.assertNotIn(case_specific_term, invariant)

    def test_manifest_keeps_construction_state(self) -> None:
        manifest = verify_bundle(C79)
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "draft")
        self.assertEqual(manifest["provenance"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["provenance"]["runtime_projection_status"], "not_projected")

    def test_f04_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C79)
        source = json.loads(C71_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C79_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(source["cases"], [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}])
        self.assertEqual(source["comparison_conditions"]["executor_parameters"]["reasoning_effort"], "medium")
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

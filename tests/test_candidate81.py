from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C71 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C71_PROFILE = ROOT / "evaluations/profiles/candidate71-validation-closure-v13-reasoning-medium-validation-wrapper-precedence-f04-global-m10-n10-r1.json"
C81_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v13-reasoning-medium-f04-global-m10-n10-r1.json"
C71_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate71-validation-closure-v13-reasoning-medium-standard14-global-m24-n5-r1.json"
C81_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v13-reasoning-medium-standard14-global-m24-n5-r1.json"


def labelled_lines(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if line.startswith("- "):
            label, body = line[2:].split(": ", 1)
            blocks[label] = body
    return blocks


class Candidate81Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate71(self) -> None:
        source = verify_bundle(C71)
        candidate = verify_bundle(C81)
        self.assertEqual(candidate["prompt_identity"], "the-caption-3ce91a4-validation-wrapper-precedence-r1")
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

    def test_replaces_only_validation_closure_with_precedence_rule(self) -> None:
        source = labelled_lines((C71 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_lines((C81 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(list(candidate), list(source))
        self.assertEqual(
            {label: candidate[label] for label in source if label != "VALIDATION_CLOSURE"},
            {label: source[label] for label in source if label != "VALIDATION_CLOSURE"},
        )
        invariant = candidate["VALIDATION_CLOSURE"]
        self.assertIn("TaskSpecまたはcommand evidence protocolの「順に」「1 commandずつ個別」", invariant)
        self.assertIn("1回のcustom exec wrapper内", invariant)
        self.assertIn("bind順の個別`exec_command`", invariant)
        self.assertIn("次commandを別custom tool callで発行することを意味しない", invariant)
        self.assertIn("各exit codeをwrapper内で確認", invariant)
        self.assertIn("nonzeroまたはunavailableなら後続を発行せず", invariant)
        self.assertIn("全resultを一度だけmodelへ返す", invariant)
        for case_specific_term in ("F04", "npm", "lint", "build"):
            self.assertNotIn(case_specific_term, invariant)

    def test_manifest_keeps_construction_state(self) -> None:
        manifest = verify_bundle(C81)
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "draft")
        self.assertEqual(manifest["provenance"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["provenance"]["runtime_projection_status"], "not_projected")

    def test_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C81)
        source = json.loads(C71_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C81_PROFILE.read_text(encoding="utf-8"))
        protocol = source["comparison_conditions"]["executor_parameters"]["command_evidence_protocol"]
        self.assertEqual(protocol["schema_version"], "the-caption-prompt.command-evidence-protocol/v1")
        self.assertEqual(source["comparison_conditions"]["repetition_condition"]["iterations"], 10)
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

    def test_standard14_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C81)
        source = json.loads(C71_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C81_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(source["evaluation_set"], {"revision": "r1", "set_id": "the-caption-standard14-r1"})
        self.assertEqual(source["comparison_conditions"]["executor_parameters"]["reasoning_effort"], "medium")
        self.assertEqual(source["comparison_conditions"]["repetition_condition"]["iterations"], 5)
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

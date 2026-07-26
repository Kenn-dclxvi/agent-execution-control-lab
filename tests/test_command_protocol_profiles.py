from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C71 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
V1 = ROOT / "evaluations/profiles/candidate71-validation-closure-v13-reasoning-medium-command-protocol-v1-f04-global-m10-n10-r1.json"
V2 = ROOT / "evaluations/profiles/candidate71-validation-closure-v13-reasoning-medium-command-protocol-v2-f04-global-m10-n10-r1.json"


class CommandProtocolProfilesTest(unittest.TestCase):
    def test_profiles_fix_candidate71_medium_f04_n10(self) -> None:
        manifest = verify_bundle(C71)
        for path in (V1, V2):
            with self.subTest(path=path.name):
                profile = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(
                    profile["cases"],
                    [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}],
                )
                self.assertEqual(
                    profile["evaluation_set"],
                    {"revision": "r1", "set_id": "the-caption-command-protocol-f04-r1"},
                )
                self.assertEqual(
                    profile["prompt_set_identity"],
                    {
                        "bundle_sha256": manifest["bundle_sha256"],
                        "name": manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )
                conditions = profile["comparison_conditions"]
                self.assertEqual(conditions["executor_parameters"]["reasoning_effort"], "medium")
                self.assertEqual(conditions["executor_parameters"]["max_workers"], 10)
                self.assertEqual(conditions["repetition_condition"]["iterations"], 10)
                self.assertEqual(profile["execution"]["max_workers"], 10)

    def test_profiles_change_only_command_protocol_revision(self) -> None:
        v1 = json.loads(V1.read_text(encoding="utf-8"))
        v2 = json.loads(V2.read_text(encoding="utf-8"))
        v1_protocol = v1["comparison_conditions"]["executor_parameters"].pop(
            "command_evidence_protocol"
        )
        v2_protocol = v2["comparison_conditions"]["executor_parameters"].pop(
            "command_evidence_protocol"
        )
        v1.pop("profile_id")
        v2.pop("profile_id")
        self.assertEqual(v1, v2)
        self.assertEqual(
            {"mode": v1_protocol["mode"], "schema_version": v1_protocol["schema_version"]},
            {
                "mode": "separate_required_commands_with_structured_exit",
                "schema_version": "the-caption-prompt.command-evidence-protocol/v1",
            },
        )
        self.assertEqual(
            {"mode": v2_protocol["mode"], "schema_version": v2_protocol["schema_version"]},
            {
                "mode": "ordered_root_wrapper_with_structured_exit",
                "schema_version": "the-caption-prompt.command-evidence-protocol/v2",
            },
        )
        for protocol in (v1_protocol, v2_protocol):
            protocol.pop("mode")
            protocol.pop("schema_version")
        self.assertEqual(v1_protocol, v2_protocol)


if __name__ == "__main__":
    unittest.main()

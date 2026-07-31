from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C108 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-ticket-terminal-closure-r1"
C110 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-ticket-decision-boundary-r1"
DESIGN = ROOT / "docs/candidate110-validation-ticket-decision-boundary-design.md"
C108_PROFILE = ROOT / "evaluations/profiles/candidate108-validation-ticket-terminal-closure-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"
C110_PROFILE = ROOT / "evaluations/profiles/candidate110-validation-ticket-decision-boundary-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate110Test(unittest.TestCase):
    def test_is_direct_c108_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C108)
        candidate = verify_bundle(C110)
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

    def test_replaces_only_validation_plan_with_decision_boundary(self) -> None:
        source = rules(C108 / "files/AGENTS.md.txt")
        candidate = rules(C110 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "VALIDATION_PLAN"},
            {key: source[key] for key in source if key != "VALIDATION_PLAN"},
        )
        self.assertIn("実行票の途中状態は未発行invocationのtarget / permission / method / stop conditionを変えない", candidate["VALIDATION_PLAN"])
        self.assertIn("`DECISION_BOUNDARY`を開かず", candidate["VALIDATION_PLAN"])
        self.assertIn("実行票全体のterminal resultだけを次の判断へ渡す", candidate["VALIDATION_PLAN"])
        self.assertNotIn("yield", candidate["VALIDATION_PLAN"])
        self.assertNotIn("wait", candidate["VALIDATION_PLAN"])
        self.assertNotIn("functions.exec", candidate["VALIDATION_PLAN"])

    def test_manifest_and_design_bind_one_axis(self) -> None:
        manifest = verify_bundle(C110)
        self.assertEqual(
            manifest["bundle_sha256"],
            "b9e1140ebdfb79d66c04dd47f478f85ec985122de104f0b08eef25d03fa5cdbe",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate108を直接親", design)
        self.assertIn("yield値、tool名、待機方法、executor動作は指定しない", design)
        self.assertIn("M=24", design)

    def test_f03_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C108_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C110_PROFILE.read_text(encoding="utf-8"))
        for key in source:
            if key not in {"profile_id", "prompt_set_identity"}:
                self.assertEqual(candidate[key], source[key])
        self.assertEqual(
            candidate["iterations"],
            source["comparison_conditions"]["repetition_condition"]["iterations"],
        )
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "b9e1140ebdfb79d66c04dd47f478f85ec985122de104f0b08eef25d03fa5cdbe",
                "name": "the-caption-3ce91a4-validation-ticket-decision-boundary-r1",
                "revision": "r1",
            },
        )
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)

if __name__ == "__main__":
    unittest.main()

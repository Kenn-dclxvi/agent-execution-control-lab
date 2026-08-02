from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C128 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-effect-closure-r1"
C131 = ROOT / "prompts/candidates/the-caption-3ce91a4-criterion-anchor-continuation-r1"
DESIGN = ROOT / "docs/candidate131-criterion-anchor-continuation-design.md"
C128_PROFILE = ROOT / "evaluations/profiles/candidate128-required-effect-closure-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"
C131_PROFILE = ROOT / "evaluations/profiles/candidate131-criterion-anchor-continuation-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate131Test(unittest.TestCase):
    def test_is_direct_c128_child(self) -> None:
        source = verify_bundle(C128)
        candidate = verify_bundle(C131)
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

    def test_changes_only_criterion_anchor_continuation(self) -> None:
        source = rules(C128 / "files/AGENTS.md.txt")
        candidate = rules(C131 / "files/AGENTS.md.txt")
        self.assertEqual({key for key in source if source[key] != candidate[key]}, {"EVIDENCE_GATE"})
        gate = candidate["EVIDENCE_GATE"]
        for term in (
            "criterion_anchor_ready",
            "完全一致可能なidentifier / property名 / key / literal label",
            "全anchorの同一target内の全一致箇所と各周辺content",
            "一つのinvocationで直接返す",
            "criterion_anchor_ready=falseの場合に限り",
            "全未取得contentを終端まで覆う",
            "anchorのlocator identityだけを独立resultとして返さない",
        ):
            self.assertIn(term, gate)
        for forbidden in ("F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(forbidden, gate)
        for key in ("SPEC", "RECOVERY", "VALIDATION_PLAN", "METHOD"):
            self.assertEqual(candidate[key], source[key])

    def test_design_separates_existing_controls_and_n5_gate(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for term in (
            "Candidate121",
            "Candidate124",
            "Candidate125 / Candidate128",
            "Candidate130",
            "report deliveryの切詰め自体はpromptで制御しない",
            "effect state、change admission",
            "初段はF04 r2だけをN=5",
            "score `3`以下: 0 / 5",
            "全未取得content fallback: 0 / 5",
        ):
            self.assertIn(term, design)

    def test_f04_profile_preserves_c128_conditions(self) -> None:
        source = json.loads(C128_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C131_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C131)
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(
            candidate["cases"],
            [case for case in source["cases"] if case["id"] == "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY"],
        )
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C128 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-effect-closure-r1"
C133 = ROOT / "prompts/candidates/the-caption-3ce91a4-anchor-first-continuation-order-r1"
DESIGN = ROOT / "docs/candidate133-anchor-first-continuation-order-design.md"
C128_PROFILE = ROOT / "evaluations/profiles/candidate128-required-effect-closure-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"
C133_PROFILE = ROOT / "evaluations/profiles/candidate133-anchor-first-continuation-order-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate133Test(unittest.TestCase):
    def test_is_direct_c128_child(self) -> None:
        source = verify_bundle(C128)
        candidate = verify_bundle(C133)
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

    def test_changes_only_anchor_first_continuation_order(self) -> None:
        source = rules(C128 / "files/AGENTS.md.txt")
        candidate = rules(C133 / "files/AGENTS.md.txt")
        self.assertEqual({key for key in source if source[key] != candidate[key]}, {"EVIDENCE_GATE"})
        gate = candidate["EVIDENCE_GATE"]
        for term in (
            "observed_anchor_set",
            "完全一致可能identifier / property名 / key / literal label",
            "最初に全memberの同一target内の全一致箇所と各周辺contentを直接返し",
            "その後に限りanchorを持たない未観測criterion",
            "全criterionがanchor-readyかという別判断によりdirect部分を失効させない",
            "direct部分とfallback部分を別invocationへ分割しない",
        ):
            self.assertIn(term, gate)
        for forbidden in ("F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(forbidden, gate)
        for key in ("SPEC", "RECOVERY", "VALIDATION_PLAN", "METHOD"):
            self.assertEqual(candidate[key], source[key])

    def test_design_fixes_single_axis_and_n5_gate(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for term in (
            "Candidate128を直接親",
            "Candidate131は停止済みの診断証拠",
            "staleまたは未観測preimageを持つ変更は0件",
            "一回のcontinuation result内の順序だけ",
            "初段F04 N=5 gate",
            "全残存contentへ直接進む: 0 / 5",
        ):
            self.assertIn(term, design)

    def test_f04_profile_preserves_c128_conditions(self) -> None:
        source = json.loads(C128_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C133_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C133)
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

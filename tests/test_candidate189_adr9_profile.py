from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "evaluations/profiles/candidate189-self-contained-review-control-adr9-r2-medium-m24-n5-cli0146.json"
REFERENCE = ROOT / "evaluations/profiles/candidate176-decision-premise-counterexample-adr9-r2-medium-m24-n5-cli0146.json"
DESIGN = ROOT / "docs/candidate189-self-contained-review-control-adr9-r2-n5-evaluation-design.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Candidate189Adr9ProfileTest(unittest.TestCase):
    def test_full_adr9_profile_keeps_reference_conditions(self) -> None:
        profile = load(PROFILE)
        reference = load(REFERENCE)
        self.assertEqual(profile["evaluation_set"], reference["evaluation_set"])
        self.assertEqual(profile["cases"], reference["cases"])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["comparison_conditions"], reference["comparison_conditions"])
        self.assertEqual(profile["execution"], reference["execution"])
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-self-contained-review-control-r1",
                "revision": "r1",
                "bundle_sha256": "76153f5b91019aca7a20a449831510cc4528f6477ea17815f9525ef3bfb90cb6",
            },
        )

    def test_design_issues_only_candidate189_forty_five(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for required in (
            "比較相手は新規実行しない",
            "Candidate189の互換atomic runは0件",
            "Candidate189の不足45件だけを発行",
            "TPOを別の比較系列として追加せず",
            "45 / 45 validかつScore `4`",
            "Standard14非退行",
        ):
            self.assertIn(required, design)

    def test_design_binds_all_terminal_obligations(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for case_id in range(1, 10):
            self.assertIn(f"ADR{case_id:02d}", design)
        for terminal in ("completion_ready", "blocked", "unavailable"):
            self.assertIn(f"`{terminal}`", design)
        for mechanism in (
            "machine-bound result",
            "counterexample_found",
            "no_counterexample_found",
            "情報封鎖",
            "subject-local effect",
            "identity固定済み`missing`",
        ):
            self.assertIn(mechanism, design)


if __name__ == "__main__":
    unittest.main()

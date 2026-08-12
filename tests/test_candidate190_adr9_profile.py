from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "evaluations/profiles/candidate190-current-prior-review-result-admission-adr9-r2-medium-m24-n5-cli0146.json"
DESIGN = ROOT / "docs/candidate190-current-prior-review-result-admission-adr9-r2-n5-evaluation-design.md"


class Candidate190Adr9ProfileTest(unittest.TestCase):
    def test_profile_is_targeted_to_review_result_consumers(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            ["TC-ADR03", "TC-ADR04", "TC-ADR05", "TC-ADR06", "TC-ADR07", "TC-ADR09"],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["comparison_conditions"]["executor_parameters"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-current-prior-review-result-admission-r1",
                "revision": "r1",
                "bundle_sha256": "63d8a79139e2b1e89268455cf997ccf7bd078b37d1bf44e51e0079aa05bfc30c",
            },
        )

    def test_design_fixes_thirty_candidate_only_slots_and_zero_issue_gate(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        for required in (
            "Candidate190だけ30件",
            "TPOを別系列へ追加せず",
            "prior predicateは静的構造試験の範囲",
            "preflight-comparison",
            "verify-comparison-preflight",
            "一件も発行せず停止",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()

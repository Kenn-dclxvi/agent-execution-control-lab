from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C140 = ROOT / "prompts/candidates/the-caption-3ce91a4-effect-satisfaction-witness-r1"
C141 = ROOT / "prompts/candidates/the-caption-3ce91a4-prechange-relation-coverage-r1"
PROFILE = ROOT / "evaluations/profiles/candidate141-prechange-relation-coverage-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"


class Candidate141Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C140)
        candidate = verify_bundle(C141)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_gate = (C140 / "files/AGENTS.md.txt").read_text()
        candidate_gate = (C141 / "files/AGENTS.md.txt").read_text()
        old = "target全件がadmission済み ∧ result受領後の判断がedit-readyまたはterminal stopへ限定済み"
        self.assertIn(old, source_gate)
        self.assertNotIn("required_relation_evidence_scope", source_gate)
        for term in (
            "required_relation_evidence_scope",
            "全memberと接続をcurrent content上で直接示す必要範囲",
            "target artifact全体または終端までの取得を、それ自体では変更前waveの完了条件にしない",
            "effect_satisfaction_witness(effect)",
            "continuation_effect_change_ready",
        ):
            self.assertIn(term, candidate_gate)
        for term in ("F02", "F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(term, candidate_gate)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()

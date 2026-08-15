from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-owner-field-exclusion-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-observed-value-reread-exclusion-r1"
PROFILE = ROOT / "evaluations/profiles/candidate235-observed-value-reread-exclusion-v14-reasoning-medium-f02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/c719ce57a9874c37953001d0a05d1deb.json"
MECHANISM = ROOT / "evaluations/results/candidate235-observed-value-reread-exclusion-f02-n5-mechanism-audit-r1.json"


class Candidate235Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["bundle_sha256"], "4db354d607a010acfe0fc86dff2eab5c62ae399062425d2aa961f083d223908f")

    def test_only_evidence_gate_changes_from_candidate233_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### EVIDENCE_GATE\n", 1)
        _, after_s = rest_s.split("### OWNER_ROLE\n", 1)
        before_c, rest_c = candidate.split("### EVIDENCE_GATE\n", 1)
        gate, after_c = rest_c.split("### OWNER_ROLE\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("正確な行位置を知ること", gate)
        self.assertIn("同じ値の所在を検索すること", gate)

    def test_f02_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)

    def test_result_records_cost_not_reduced(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "c719ce57a9874c37953001d0a05d1deb")
        self.assertEqual(result["median"]["total_tokens"], 171747)
        self.assertEqual(mechanism["diagnostics"]["nonterminal_validation_wait"]["count"], 3)
        self.assertEqual(mechanism["status"], "mechanism_passed_cost_not_reduced")


if __name__ == "__main__":
    unittest.main()

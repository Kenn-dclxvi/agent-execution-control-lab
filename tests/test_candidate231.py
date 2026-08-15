from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-reader-ai-plain-japanese-translation-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-compact-evidence-admission-r1"
DESIGN = ROOT / "docs/candidate231-compact-evidence-admission-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate231-compact-evidence-admission-v14-reasoning-medium-f02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/f0ab6a23339b4fb59458da2da7ce0549.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate231-compact-evidence-admission-f02-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate231-compact-evidence-admission-f02-n5-mechanism-audit-r1.json"


class Candidate231Test(unittest.TestCase):
    def test_c147_is_direct_baseline_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["artifact"]["state"], "evaluation_ready")
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "b12b09d692a1ec945ef82593011409e1319272a24ace66b581f8072ea2aef1d7",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_only_evidence_gate_differs_from_plain_japanese_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        source_before, source_rest = source.split("### EVIDENCE_GATE\n", 1)
        _, source_after = source_rest.split("### OWNER_ROLE\n", 1)
        candidate_before, candidate_rest = candidate.split("### EVIDENCE_GATE\n", 1)
        candidate_gate, candidate_after = candidate_rest.split("### OWNER_ROLE\n", 1)
        self.assertEqual(candidate_before, source_before)
        self.assertEqual(candidate_after, source_after)
        self.assertIn("必要な事実が揃った後は", candidate_gate)
        self.assertIn("検索、部分読み、再確認を追加しない", candidate_gate)
        self.assertLess(len(candidate), len(source))

    def test_f02_measurement_is_fixed(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["cases"],
            [{"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"}],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("token中央値がCandidate230を下回れば", design)
        self.assertIn("成功runのcommand順を手順化しない", design)

    def test_f02_result_is_registered_and_stopped(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "f0ab6a23339b4fb59458da2da7ce0549")
        self.assertEqual(result["median"]["total_tokens"], 133657)
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(quality["score_counts"], {"4": 5})
        owner = mechanism["gates"]["criterion_owner_did_not_create_producer"]
        self.assertEqual(owner["pass_count"], 4)
        self.assertEqual(owner["failure_count"], 1)
        self.assertEqual(mechanism["status"], "mechanism_failed")


if __name__ == "__main__":
    unittest.main()

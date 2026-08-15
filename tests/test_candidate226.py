from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-human-result-effect-scope-r1"
DESIGN = ROOT / "docs/candidate226-human-result-effect-scope-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate226-human-result-effect-scope-v14-reasoning-medium-a02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/7935883b701a4c1b93dba54820fcde6e.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate226-human-result-effect-scope-a02-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate226-human-result-effect-scope-a02-n5-mechanism-audit-r1.json"


class Candidate226Test(unittest.TestCase):
    def test_c147_direct_candidate_changes_only_root_agents(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["artifact"]["state"], "evaluation_ready")
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "5545d75864a396a6eedbc3212c24e6f5cd0322a35313fdaa04f3e29b5f8b25dd",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_only_result_effect_scope_clause_is_translated(self) -> None:
        base_lines = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        candidate_lines = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(base_lines), len(candidate_lines))
        differences = [
            (left, right)
            for left, right in zip(base_lines, candidate_lines, strict=True)
            if left != right
        ]
        self.assertEqual(len(differences), 1)
        left, right = differences[0]
        self.assertTrue(left.startswith("- DECISION_BOUNDARY:"))
        self.assertTrue(right.startswith("- 結果の影響範囲:"))
        self.assertIn("readの待機条件にしない", right)
        self.assertNotIn("model step", right)
        self.assertNotIn("wrapper", right)

    def test_design_and_a02_profile_bind_first_gate(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertIn("第一段階: A02 N=5", design)
        self.assertIn("A02が通過した場合だけ", design)
        self.assertEqual(
            profile["cases"],
            [{"id": "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING", "revision": "r2"}],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"],
            verify_bundle(CANDIDATE)["bundle_sha256"],
        )

    def test_a02_result_stops_before_a01_on_mechanism_failure(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "7935883b701a4c1b93dba54820fcde6e")
        self.assertEqual(result["compatibility_key"], "59aa2324d8d681a3781ab9cc6b480c79de3eb7ba837161957a11d346d0046c71")
        self.assertEqual(quality["score_counts"], {"4": 5})
        self.assertEqual(mechanism["failure_count"], 4)
        self.assertEqual(mechanism["pass_count"], 1)
        self.assertIn("mechanism_failed_4_of_5", design)
        self.assertIn("A01は発行しない", design)


if __name__ == "__main__":
    unittest.main()

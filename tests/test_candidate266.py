from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-declared-instruction-descendant-read-dependency-r1"
PROFILE = ROOT / "evaluations/profiles/candidate266-declared-instruction-descendant-read-dependency-v14-reasoning-medium-f01-f02-f03-f10-entrypoint-global-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/5ca7e3a68e444ccbad70ecf50a82236a.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate266-declared-instruction-descendant-read-dependency-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json"


class Candidate266Test(unittest.TestCase):
    def test_c147_is_direct_base_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "274217c1f7adbaadbbb7bbec31a3443bdd336f53b5794ef99d799f8509dbc4b4",
        )

    def test_added_boundary_is_exact_path_and_machine_result_only(self) -> None:
        base = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertIn("TaskSpecのread対象にexact path D/AGENTS.mdが明示されている", candidate)
        self.assertIn("normalized(read.target)がD/配下", candidate)
        self.assertIn("read invocationがterminal success ∧ content resultを受領済み", candidate)
        self.assertIn("そのreadを`authorized_read=false`", candidate)
        self.assertNotIn("必要な場合", candidate)
        self.assertNotIn("適用されるか", candidate)
        self.assertEqual(candidate.count("\n"), base.count("\n"))
        self.assertEqual(
            candidate.replace(
                "`declared_instruction_dependency(read) := TaskSpecのread対象にexact path D/AGENTS.mdが明示されている ∧ normalized(read.target) != D/AGENTS.md ∧ normalized(read.target)がD/配下`、`instruction_result_ready(D) := D/AGENTS.mdへbindしたread invocationがterminal success ∧ content resultを受領済み`とする。`declared_instruction_dependency(read)=true ∧ instruction_result_ready(D)=false`の間は、そのreadを`authorized_read=false`とする。この否定は`result_effect_scope`、一般的なread permission、配下pathの列挙および開始identityの停止範囲より優先し、D/AGENTS.md自身のreadには適用しない。",
                "",
            ),
            base,
        )

    def test_profile_is_fixed_to_four_cases_and_n5(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "bundle_sha256": "274217c1f7adbaadbbb7bbec31a3443bdd336f53b5794ef99d799f8509dbc4b4",
                "name": "the-caption-3ce91a4-declared-instruction-descendant-read-dependency-r1",
                "revision": "r1",
            },
        )
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            [
                "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
                "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND",
                "TC-F03-ATOMIC-CONTEXT-CLEANUP",
                "TC-F10-ENTRYPOINT-INVENTORY-REVIEW",
            ],
        )

    def test_targeted_n5_is_an_isolated_probe_not_candidate264_replacement(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        audit = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "5ca7e3a68e444ccbad70ecf50a82236a")
        self.assertEqual(audit["gates"]["f10_instruction_terminal_result_preceded_descendant_listing_and_content"]["candidate266"]["pass_count"], 5)
        self.assertEqual(audit["gates"]["f10_instruction_terminal_result_preceded_descendant_listing_and_content"]["candidate266"]["failure_count"], 0)
        self.assertEqual(
            audit["status"],
            "mechanism_probe_passed_quality_passed_n5_only_not_candidate264_replacement_not_adopted",
        )
        self.assertEqual(audit["disposition"]["next_candidate"], "not_created")


if __name__ == "__main__":
    unittest.main()

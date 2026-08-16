from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-start-identity-result-effect-scope-restoration-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-instruction-result-read-permission-restoration-r1"
PROFILE = ROOT / "evaluations/profiles/candidate265-instruction-result-read-permission-restoration-v14-reasoning-medium-f01-f02-f03-f10-entrypoint-global-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/cd29f61f140d400c821e9b1900b40f8a.json"
QUALITY = ROOT / "evaluations/results/candidate265-instruction-result-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate265-instruction-result-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json"


class Candidate265Test(unittest.TestCase):
    def test_candidate264_is_direct_comparison_source(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "cc44d86239ebc96fa65f9aaa2652c3824c76bf3f793e1cd340308d4225ce0130",
        )

    def test_only_instruction_dependency_predicate_is_added(self) -> None:
        parent = (PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        paragraph = (
            "`instruction_dependency_pending(read) := TaskSpecがread対象へ適用するrepository instructionを明示している ∧ "
            "そのinstruction resultがreadの対象、permissionまたはstop conditionを変え得る ∧ terminalかつcompatibleな"
            "instruction resultを未受領`とする。`instruction_dependency_pending(read)=true`の配下readは"
            "`authorized_read=false`とし、TaskSpecがそのpathをread対象へ列挙していることだけではpermissionを開かない。"
            "instruction自体のreadは配下readに含めず、それ自身に未解決dependencyがなければ開始確認と同一model stepから"
            "発行できる。instruction resultが`compatible`なら対応する配下readのpermissionを開き、"
            "`missing / unreadable / contradiction`ならTaskSpecのstop conditionへbindしてpermissionを開かない。\n\n"
        )
        marker = "### VALIDATION_CLOSURE\n"
        self.assertNotIn("instruction_dependency_pending(read)", parent)
        self.assertEqual(candidate, parent.replace(marker, paragraph + marker))
        self.assertIn("開始確認とTaskSpecで既に許可済みのreadを同一model stepから発行", candidate)

    def test_targeted_profile_is_fixed_to_four_cases_and_n5(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "cc44d86239ebc96fa65f9aaa2652c3824c76bf3f793e1cd340308d4225ce0130")
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            [
                "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
                "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND",
                "TC-F03-ATOMIC-CONTEXT-CLEANUP",
                "TC-F10-ENTRYPOINT-INVENTORY-REVIEW",
            ],
        )

    def test_result_preserves_mechanism_failure_and_cost_stop(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "cd29f61f140d400c821e9b1900b40f8a")
        self.assertEqual(result["median"]["total_tokens"], 536176)
        self.assertEqual(quality["score_counts"], {"4": 20})
        for case in ("f01", "f02", "f03"):
            gate = mechanism["gates"][f"{case}_start_identity_and_authorized_read_shared_ai_decision"]
            self.assertEqual(gate["candidate265"], {"failure_count": 0, "pass_count": 5})
        f10 = mechanism["gates"]["f10_instruction_terminal_result_preceded_descendant_listing_and_content"]
        self.assertEqual((f10["candidate265"]["pass_count"], f10["candidate265"]["failure_count"]), (4, 1))
        self.assertEqual(mechanism["validation_reentry_diagnostic"]["candidate265_runs_with_wait_by_case"]["F02"], 5)
        self.assertEqual(
            mechanism["status"],
            "design_gate_violation_candidate_should_not_have_been_created_diagnostic_only",
        )


if __name__ == "__main__":
    unittest.main()

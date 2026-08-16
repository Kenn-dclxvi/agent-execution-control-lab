from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-independent-check-same-model-step-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-start-identity-result-effect-scope-restoration-r1"
PROFILE = ROOT / "evaluations/profiles/candidate264-start-identity-result-effect-scope-restoration-v14-reasoning-medium-f01-f02-f03-f10-entrypoint-global-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/1a64c1b2429c4e89aff3aedd6836944e.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json"


class Candidate264Test(unittest.TestCase):
    def test_candidate254_is_direct_parent(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "9b33e94432ede3ee0c278d876e743ec07f123ba5478c8c8df84dcf4d159ab930",
        )

    def test_only_decision_boundary_is_replaced(self) -> None:
        parent = (PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        old = """受け取る結果によって次の作業の対象、許可、方法、停止条件が変わらないと既に分かっている複数の確認は、分割せず同一model stepから発行し、すべての結果を受け取った後に一度だけ次を判断する。

開始確認の停止条件が変更や必須コマンドだけを禁じ、読み取りを禁じていない場合は、開始確認と必要な読み取りを同一model stepから発行する。読み取りを別stepへ置けるのは、停止条件が読み取りも禁じるか、確認結果で読み取りの対象または許可が変わり得る場合だけとする。"""
        new = """`result_effect_scope := 受領resultが対象、許可、方法または停止条件を変え得る未発行operation classの集合`、`decision_boundary(next_operation) := next_operation.class ∈ result_effect_scope`とする。resultの停止効果をtask全体または後続operation全体へ伝播させない。既知の相互非依存operationは、そのclassが`result_effect_scope`に含まれない場合、分割せず同一model stepから発行し、全result受領後に一度だけ次を判断する。

開始確認resultについては`identity_result_effect_scope = {artifact_change, required_validation}`、`authorized_read ∉ identity_result_effect_scope`とする。開始確認とTaskSpecで既に許可済みのreadを同一model stepから発行し、共同resultを受領して開始状態が正常と判定されるまでartifact変更とrequired validationだけを発行しない。TaskSpecが開始状態の不一致時にreadも禁止する場合、または開始確認resultでreadの対象か許可が変わり得る場合だけ、そのreadを`identity_result_effect_scope`へ含めて別stepへ置く。"""
        self.assertIn(old, parent)
        self.assertEqual(candidate, parent.replace(old, new))

    def test_four_relations_are_explicit(self) -> None:
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertIn("result_effect_scope :=", candidate)
        self.assertIn("decision_boundary(next_operation) :=", candidate)
        self.assertIn("identity_result_effect_scope = {artifact_change, required_validation}", candidate)
        self.assertIn("authorized_read ∉ identity_result_effect_scope", candidate)
        self.assertIn("停止効果をtask全体または後続operation全体へ伝播させない", candidate)

    def test_non_target_controls_are_retained(self) -> None:
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertIn("TaskSpecへの固定と固定した各項目の値は、作業を制御するための内部状態", candidate)
        self.assertIn("途中結果をAIへ返してから", candidate)
        self.assertNotIn("Candidate147", candidate)
        self.assertNotIn("Candidate261", candidate)
        self.assertNotIn("Candidate262", candidate)
        self.assertNotIn("Candidate263", candidate)

    def test_targeted_profile_is_fixed_to_four_cases_and_n5(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "9b33e94432ede3ee0c278d876e743ec07f123ba5478c8c8df84dcf4d159ab930")
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            [
                "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
                "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND",
                "TC-F03-ATOMIC-CONTEXT-CLEANUP",
                "TC-F10-ENTRYPOINT-INVENTORY-REVIEW",
            ],
        )

    def test_registered_result_and_audits_preserve_stop_decision(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "1a64c1b2429c4e89aff3aedd6836944e")
        self.assertEqual(result["median"]["total_tokens"], 484121)
        self.assertEqual(quality["score_counts"], {"4": 20})
        self.assertEqual(
            mechanism["gates"]["f03_unaffected_start_result_did_not_delay_required_read"]["candidate264"]["pass_count"],
            5,
        )
        self.assertEqual(
            mechanism["gates"]["f10_instruction_result_preceded_entrypoint_content_when_permission_could_change"]["candidate264"],
            {
                "failure_count": 3,
                "pass_count": 2,
                "runs": [
                    {"iteration": 1, "result": "passed", "run_id": "cba3c16c9e0445e1977cafa636c2f016"},
                    {"iteration": 2, "result": "passed", "run_id": "b46717a6e7a7419cbc5019f47d19b0b4"},
                    {"iteration": 3, "result": "failed", "run_id": "ddf8fb58a42b411cab2cd6ed01b0beed"},
                    {"iteration": 4, "result": "failed", "run_id": "527e8dd1e39e4efc868295224bde740d"},
                    {"iteration": 5, "result": "failed", "run_id": "611de3f1053a4b128c64a4be25b94470"},
                ],
            },
        )
        self.assertEqual(mechanism["status"], "target_mechanism_passed_normal_route_regressed_stopped")


if __name__ == "__main__":
    unittest.main()

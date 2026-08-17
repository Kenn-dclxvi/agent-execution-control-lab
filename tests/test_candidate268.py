from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-independent-check-same-model-step-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-natural-language-result-read-boundary-r1"
PROFILE = ROOT / "evaluations/profiles/candidate268-natural-language-result-read-boundary-v14-reasoning-medium-f01-f02-f03-f10-entrypoint-global-m24-n5-cli0146-r1.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json"
REGISTERED_RESULT = ROOT / "evaluations/results/f43e7342001140b38f7f33e5bcb73cac.json"


class Candidate268Test(unittest.TestCase):
    def test_candidate254_is_direct_parent_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "c09072b2ec153fec63a4e07b2767e7e68499ffcdeef9375bed46f2d03215b9a5",
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in base["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_decision_boundary_is_replaced_with_natural_language_only(self) -> None:
        base = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        old = """受け取る結果によって次の作業の対象、許可、方法、停止条件が変わらないと既に分かっている複数の確認は、分割せず同一model stepから発行し、すべての結果を受け取った後に一度だけ次を判断する。

開始確認の停止条件が変更や必須コマンドだけを禁じ、読み取りを禁じていない場合は、開始確認と必要な読み取りを同一model stepから発行する。読み取りを別stepへ置けるのは、停止条件が読み取りも禁じるか、確認結果で読み取りの対象または許可が変わり得る場合だけとする。"""
        new = """受け取る結果によって、後続作業の対象、許可、方法、停止条件のいずれも変わり得ない場合、その結果の受領を後続作業の開始条件にしてはいけない。互いに影響しないことが分かっている許可済みの作業は分割せず、同じmodel stepから発行し、すべての結果を受け取った後に一度だけ次を判断する。

開始状態の不一致によって成果物の変更と必須検証だけを止めるTaskSpecでは、開始確認の結果を、すでに許可されている必要な読み取りの開始条件にしてはいけない。開始確認とその読み取りは同じmodel stepから発行し、開始状態が正常だと分かるまでは成果物の変更と必須検証だけを行わない。TaskSpecが不一致時に読み取りも禁止している場合、または開始確認の結果によって読み取りの対象か許可が変わり得る場合に限り、その読み取りを開始確認後へ置く。

ただし、TaskSpecがあるディレクトリの`AGENTS.md`を正規化した完全なpathで読み取り対象として明示した場合、そのファイルを正常に読み終えて内容を受け取るまでは、同じディレクトリ配下にある別のpathを読んではいけない。TaskSpecが配下pathも読み取り対象として列挙していることや、開始確認が読み取りを禁止していないことでは、この禁止は解除されない。`AGENTS.md`自体と、そのディレクトリの外にある読み取りには、この禁止を適用しない。"""
        self.assertIn(old, base)
        self.assertEqual(candidate, base.replace(old, new))
        decision = candidate.split("### DECISION_BOUNDARY\n", 1)[1].split("### VALIDATION_CLOSURE\n", 1)[0]
        for formal in (":=", "∈", "∉", "∧", "{artifact_change", "declared_instruction"):
            self.assertNotIn(formal, decision)

    def test_feedback_sources_are_not_inherited_as_prompt_text(self) -> None:
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for name in ("Candidate147", "Candidate263", "Candidate264", "Candidate265", "Candidate266", "Candidate267"):
            self.assertNotIn(name, candidate)
        self.assertIn("その結果の受領を後続作業の開始条件にしてはいけない", candidate)
        self.assertIn("そのファイルを正常に読み終えて内容を受け取るまでは", candidate)

    def test_profile_is_fixed_to_four_cases_and_n5(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "bundle_sha256": "c09072b2ec153fec63a4e07b2767e7e68499ffcdeef9375bed46f2d03215b9a5",
                "name": "the-caption-3ce91a4-natural-language-result-read-boundary-r1",
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

    def test_evaluation_stops_on_f02_and_terminal_mechanism_failures(self) -> None:
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        result = json.loads(REGISTERED_RESULT.read_text(encoding="utf-8"))
        self.assertEqual(quality["run_count"], 20)
        self.assertEqual(quality["rateable_runs"], 20)
        self.assertEqual(quality["score_counts"], {"4": 20})
        self.assertEqual(
            mechanism["gates"]["f02_start_identity_and_authorized_read_shared_ai_decision"],
            {
                "pass_count": 4,
                "failure_count": 1,
                "failed_run_id": "8e4ed55acc854576b0c880f7adc380c2",
                "failure": "start identity result was received before the first authorized source reads were issued",
            },
        )
        self.assertEqual(
            mechanism["nonterminal_result_diagnostic"]["runs_with_nonterminal_result_by_case"]["total"],
            13,
        )
        self.assertEqual(mechanism["nonterminal_result_diagnostic"]["wait_invocations_by_case"]["total"], 0)
        self.assertEqual(mechanism["registered_result_id"], result["result_id"])
        self.assertEqual(
            result["compatibility_key"],
            "7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70",
        )
        self.assertEqual(mechanism["disposition"]["additional_n"], "not_started")
        self.assertEqual(mechanism["disposition"]["standard14"], "not_started")
        self.assertEqual(mechanism["lineage_disposition"]["next_direct_base"], "Candidate268")
        self.assertEqual(
            mechanism["lineage_disposition"]["candidate254_role"],
            "ancestry_and_diagnostic_reference_only",
        )
        self.assertEqual(
            mechanism["lineage_disposition"]["candidate269"],
            "not_created_delta_not_fixed",
        )


if __name__ == "__main__":
    unittest.main()

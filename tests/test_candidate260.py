from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-independent-check-same-model-step-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-canonical-evidence-consumer-binding-restoration-r1"
PROFILE = ROOT / "evaluations/profiles/candidate260-canonical-evidence-consumer-binding-restoration-v14-reasoning-medium-f04-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/8f3ef2f0104f4514aa6942c5824e8d2e.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate260-canonical-evidence-consumer-binding-restoration-f04-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate260-canonical-evidence-consumer-binding-restoration-f04-n5-mechanism-audit-r1.json"
MECHANISM_REASSESSMENT = ROOT / "evaluations/results/candidate260-c147-result-effect-scope-mechanism-reassessment-r2.json"
RESULT_DOC = ROOT / "evaluations/results/candidate260-canonical-evidence-consumer-binding-restoration-f04-n5_2026-08-15.md"
EVALUATION_MANUAL = ROOT / "docs/evaluation-loop-manual.md"
MINIMAL_DELTA_AUDIT = ROOT / "docs/candidate260-c147-minimal-delta-reduction-audit.md"
REPLACEMENT_DESIGN = ROOT / "docs/candidate254-candidate260-replacement-standard14-design.md"
REPLACEMENT_PROFILE = ROOT / "evaluations/profiles/candidate254-independent-check-same-model-step-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


class Candidate260Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "b9e01c6785d4abb977fa8e7733a24b3c94288f03e0726d57d3153836fea7852f",
        )

    def test_only_evidence_gate_opening_paragraph_replaced(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        old = (
            "repository内の調査や証拠取得は、作業のどの段階でも原則として行わない。"
            "必要な判定がまだ終わっておらず、状態が`unobserved`で、現在欠けている具体的な観測値が決まっており、"
            "取得する結果だけでその状態を確定できる場合に限って行う。状態は`satisfied`、`unsatisfied`、"
            "`unobserved`の三つとする。この制限は、対象探索、変更前後の調査、validation準備、recoveryのすべてに適用する。"
        )
        new = (
            "repository evidence invocationは全lifecycleでdefault denyとする。"
            "`required_predicate_state := satisfied | unsatisfied | unobserved`、"
            "`evidence_consumer_ready := required predicateがnonterminal ∧ state=unobserved ∧ "
            "現在欠けている観測値が発行前にbind済み ∧ requested resultがそのstateをbind可能`とし、"
            "`evidence_consumer_ready=true`の場合だけ発行する。発行後に受け取った部分result、取得済み範囲または"
            "それらの不足を、新しいrequired predicate、欠けた観測値またはrequested resultへrebindしても、"
            "発行前から同一だったrequired predicateを満たす残りのrepository evidence permissionは生じない。"
        )
        self.assertEqual(candidate, source.replace(old, new))

    def test_failed_lineage_conditions_are_not_inherited(self) -> None:
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertNotIn("同じ変更方針を決めるために同じartifactを読み足せるのは一度だけ", candidate)
        self.assertNotIn("残りの情報を取得する読み取り", candidate)
        self.assertNotIn("調査を発行できる単位", candidate)
        self.assertNotIn("同じ判定の途中resultを受け取った後", candidate)

    def test_f04_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["cases"],
            [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "bundle_sha256": "b9e01c6785d4abb977fa8e7733a24b3c94288f03e0726d57d3153836fea7852f",
                "name": "the-caption-3ce91a4-canonical-evidence-consumer-binding-restoration-r1",
                "revision": "r1",
            },
        )

    def test_f04_n5_result_and_quality(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "8f3ef2f0104f4514aa6942c5824e8d2e")
        self.assertEqual(
            result["result_content_sha256"],
            "aaf627ef39e8818ac65c255bbc12fbb2706431419dfb131d286b45f9c0463854",
        )
        self.assertEqual(
            result["compatibility_key"],
            "1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a",
        )
        self.assertEqual(result["median"]["total_tokens"], 176103)
        self.assertAlmostEqual(result["median"]["elapsed_seconds"], 65.1959246249753)
        self.assertEqual([item["quality_score"] for item in result["case_results"]], [4] * 5)
        self.assertEqual(quality["score_counts"], {"4": 5})

    def test_f04_n5_mechanism_failed_on_post_result_rebinding(self) -> None:
        audit = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(audit["status"], "mechanism_failed")
        self.assertEqual(
            audit["gates"]["start_check_same_model_step_joint_issuance"]["pass_count"],
            5,
        )
        self.assertEqual(
            audit["gates"]["post_result_consumer_rebinding_exclusion"]["pass_count"],
            1,
        )
        self.assertEqual(
            audit["gates"]["post_result_consumer_rebinding_exclusion"]["failure_count"],
            4,
        )
        self.assertEqual(
            audit["gates"]["post_result_consumer_rebinding_exclusion"]["post_result_consumer_rebinding_total"],
            5,
        )
        self.assertEqual(
            audit["gates"]["required_validation_single_issuance_decision"]["pass_count"],
            5,
        )

    def test_mechanism_failure_does_not_suppress_kpi_comparison(self) -> None:
        manual = EVALUATION_MANUAL.read_text(encoding="utf-8")
        result_doc = RESULT_DOC.read_text(encoding="utf-8")
        self.assertNotIn("mechanism gate不通過時はbaseline KPI比較へ進まない", manual)
        self.assertIn("mechanism不通過はKPI比較を止める条件にしない", manual)
        self.assertIn("必要性を確認できない場合は`unjustified_cost_regression`", manual)
        self.assertNotIn("KPI比較は行わない", result_doc)
        self.assertIn("+24,933（+16.49%）", result_doc)
        self.assertIn("-26.235秒（-28.69%）", result_doc)
        self.assertIn("制御効果へ帰属しない", result_doc)
        self.assertIn("`unjustified_token_regression`", result_doc)

    def test_c147_result_effect_scope_reassessment_preserves_original_result(self) -> None:
        reassessment = json.loads(MECHANISM_REASSESSMENT.read_text(encoding="utf-8"))
        self.assertEqual(
            reassessment["registered_result_id"],
            "8f3ef2f0104f4514aa6942c5824e8d2e",
        )
        self.assertEqual(
            reassessment["original_candidate260_mechanism"],
            {
                "status": "mechanism_failed",
                "post_result_consumer_rebinding_exclusion_pass_count": 1,
                "post_result_consumer_rebinding_exclusion_failure_count": 4,
                "preserved": True,
            },
        )
        self.assertEqual(
            reassessment["summary"]["c147_result_effect_scope_conforming_count"],
            4,
        )
        self.assertEqual(
            reassessment["summary"]["c147_result_effect_scope_nonconforming_count"],
            1,
        )
        self.assertEqual(
            reassessment["summary"]["unchanged_method_dependency_observation_total"],
            1,
        )
        self.assertFalse(
            reassessment["summary"]["candidate260_blanket_post_result_exclusion_matches_c147_purpose"]
        )
        self.assertEqual(reassessment["summary"]["quality_score_4_count"], 5)
        self.assertFalse(
            reassessment["summary"][
                "mechanism_failure_quality_reproducibility_loss_correlation_100_percent"
            ]
        )
        self.assertFalse(
            reassessment["interpretation"][
                "mechanism_100_percent_requirement_justified_for_current_cost_judgement"
            ]
        )
        self.assertEqual(
            reassessment["interpretation"]["mechanism_rate_role"],
            "cost_path_diagnostic",
        )
        self.assertFalse(
            reassessment["interpretation"]["candidate260_effect_attribution_established"]
        )
        self.assertEqual(
            reassessment["interpretation"]["kpi_direction"],
            "unjustified_token_regression",
        )
        self.assertFalse(
            reassessment["token_regression_trace_audit"][
                "required_processing_justification_established"
            ]
        )
        self.assertEqual(
            reassessment["token_regression_trace_audit"][
                "candidate260_median_run_wait_only_reentry_tokens"
            ],
            32440,
        )
        self.assertFalse(
            reassessment["interpretation"]["human_tradeoff_judgement_ready"]
        )
        self.assertEqual(
            reassessment["interpretation"]["replacement_candidate_selected"],
            "Candidate254",
        )
        self.assertFalse(
            reassessment["interpretation"]["duplicate_candidate261_created"]
        )
        self.assertTrue(
            reassessment["interpretation"]["replacement_candidate_standard14_completed"]
        )
        self.assertFalse(
            reassessment["interpretation"]["replacement_candidate_adopted"]
        )
        self.assertFalse(
            reassessment["interpretation"]["candidate260_improvement_resolved"]
        )

    def test_candidate260_replacement_reuses_candidate254_bytes(self) -> None:
        reassessment = json.loads(MECHANISM_REASSESSMENT.read_text(encoding="utf-8"))
        audit = MINIMAL_DELTA_AUDIT.read_text(encoding="utf-8")
        self.assertFalse(
            reassessment["token_regression_trace_audit"][
                "candidate260_prompt_delta_causal_attribution_established"
            ]
        )
        self.assertIn("valid_new_delta_count = 0", audit)
        self.assertIn("既存Candidate254", audit)
        self.assertIn("C147でも5件中2件", audit)

        source = (SOURCE / "files/AGENTS.md.txt").read_bytes()
        candidate260 = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        replacement = candidate260.replace(
            "repository evidence invocationは全lifecycleでdefault denyとする。"
            "`required_predicate_state := satisfied | unsatisfied | unobserved`、"
            "`evidence_consumer_ready := required predicateがnonterminal ∧ state=unobserved ∧ "
            "現在欠けている観測値が発行前にbind済み ∧ requested resultがそのstateをbind可能`とし、"
            "`evidence_consumer_ready=true`の場合だけ発行する。発行後に受け取った部分result、取得済み範囲または"
            "それらの不足を、新しいrequired predicate、欠けた観測値またはrequested resultへrebindしても、"
            "発行前から同一だったrequired predicateを満たす残りのrepository evidence permissionは生じない。",
            "repository内の調査や証拠取得は、作業のどの段階でも原則として行わない。"
            "必要な判定がまだ終わっておらず、状態が`unobserved`で、現在欠けている具体的な観測値が決まっており、"
            "取得する結果だけでその状態を確定できる場合に限って行う。状態は`satisfied`、`unsatisfied`、"
            "`unobserved`の三つとする。この制限は、対象探索、変更前後の調査、validation準備、recoveryのすべてに適用する。",
        ).encode("utf-8")
        self.assertEqual(replacement, source)

        profile = json.loads(REPLACEMENT_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "bundle_sha256": "7cd564be0904efb5cee59ce8d72935971d080282686e5ff7be9e85e62aa0fd52",
                "name": "the-caption-3ce91a4-independent-check-same-model-step-r1",
                "revision": "r1",
            },
        )
        self.assertEqual(len(profile["cases"]), 14)
        design = REPLACEMENT_DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate254を正式採用できるか", design)
        self.assertIn("Candidate260は過剰な制限が正常経路と衝突した失敗履歴", design)


if __name__ == "__main__":
    unittest.main()

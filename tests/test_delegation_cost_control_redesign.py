from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REDESIGN = ROOT / "docs/delegation-cost-control-redesign.md"
PRINCIPLES = ROOT / "docs/prompt-control-design-principles.md"
WORKFLOW = ROOT / "docs/prompt-comparison-workflow.md"
HISTORY = ROOT / "docs/candidate-history.md"
BACKLOG = ROOT / "docs/research-backlog.md"


class DelegationCostControlRedesignTest(unittest.TestCase):
    def test_worker_count_is_diagnostic_not_a_failure_condition(self) -> None:
        redesign = REDESIGN.read_text(encoding="utf-8")
        self.assertIn("Workerを起動した事実をcandidateの失敗条件にしない", redesign)
        self.assertIn("route診断だけで`cost_controlled`を反転させない", redesign)
        self.assertIn("F02 / F04の新しい停止条件に「Workerが1件でも起動」を入れない", redesign)

    def test_cost_gate_requires_compatible_baseline_and_prebound_tolerance(self) -> None:
        redesign = REDESIGN.read_text(encoding="utf-8")
        for condition in (
            "直接baseline resultが存在",
            "compatibility keyが一致",
            "candidate resultを見る前にtoken_toleranceとelapsed_toleranceを固定済み",
        ):
            self.assertIn(condition, redesign)
        self.assertIn("`cost_gate_ready=false`", redesign)
        self.assertIn("結果確認後に許容幅を作らない", redesign)
        self.assertIn("既定値は`token_tolerance=0`、`elapsed_tolerance=0`", redesign)
        self.assertIn("片方だけ外なら`cost_tradeoff`、両方外なら`cost_control_failed`", redesign)

    def test_controls_preserve_ai_method_choice_without_value_predicate(self) -> None:
        redesign = REDESIGN.read_text(encoding="utf-8")
        self.assertIn("次CandidateはC83 / C84の`delegation_value_ready`を継承しない", redesign)
        self.assertIn("未制約operationのroot / Worker producerをAIが選択済み", redesign)
        self.assertIn("Workerの期待価値をpromptで列挙しない", redesign)
        self.assertIn("C81を直接親", redesign)

    def test_planning_includes_producer_choice_before_dispatch(self) -> None:
        redesign = REDESIGN.read_text(encoding="utf-8")
        self.assertIn("Worker起動はplanning後に追加する判断ではない", redesign)
        self.assertIn("`execution_plan_ready=false`の間はroot operation、Worker起動", redesign)
        self.assertIn("ready operationをまとめるexecution waveが固定済み", redesign)
        self.assertIn("wait_ready :=", redesign)
        self.assertIn("ほかにreadyなroot operationがない", redesign)

    def test_only_explicit_identity_constraint_limits_ai_choice(self) -> None:
        redesign = REDESIGN.read_text(encoding="utf-8")
        for category in ("`producer_constraint`", "`producer_preference`", "`producer_metadata`"):
            self.assertIn(category, redesign)
        self.assertIn("owner、risk、role、作業名、独立性を表す形容から推定しない", redesign)
        self.assertIn("`producer_constraint`だけをhard constraint", redesign)

    def test_existing_task_specs_are_held_fixed(self) -> None:
        redesign = REDESIGN.read_text(encoding="utf-8")
        self.assertIn("既存のF02 / F04 / D01 TaskSpecは変更しない", redesign)
        self.assertIn("既存入力のままproducerを指定しないmetadataとして解釈", redesign)
        self.assertIn("D01の「workerをproducerとする」という明示指定はhard constraint", redesign)
        self.assertIn("required_execution_identity = distinct_worker_identity", redesign)
        self.assertIn("将来の評価set revisionにだけ適用する。C85の比較へは持ち込まない", redesign)

    def test_ssots_keep_three_kpis_and_route_diagnostic_boundary(self) -> None:
        principles = PRINCIPLES.read_text(encoding="utf-8")
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("Worker選択とコスト判定", principles)
        self.assertIn("Worker routing、child session数", workflow)
        for kpi in ("quality_score", "total_tokens", "elapsed_seconds"):
            self.assertIn(kpi, workflow)

    def test_current_interpretation_does_not_rewrite_immutable_states(self) -> None:
        history = HISTORY.read_text(encoding="utf-8")
        backlog = BACKLOG.read_text(encoding="utf-8")
        for state in (
            "quality_passed / cost_control_not_demonstrated",
            "quality_passed / cost_control_mixed",
        ):
            self.assertIn(state, history)
            self.assertIn(state, backlog)
        self.assertIn("immutable評価state", backlog)

    def test_f02_control_graph_diagnostic_stops_unjustified_next_candidate(self) -> None:
        redesign = REDESIGN.read_text(encoding="utf-8")
        backlog = BACKLOG.read_text(encoding="utf-8")
        for fact in (
            "C87からC89までのWorker 11件",
            "11件のchild token合計は`820,380`",
            "criterion metadataを、独立したoperation identityへ昇格",
            "operation_identity_ready :=",
            "この診断だけを根拠にC81直接childの新Candidate、bundle、profile、model runを作成しない",
        ):
            self.assertIn(fact, redesign)
        self.assertIn("C81・C87・C88・C89 F02 control graph診断（完了・新Candidateなし）", backlog)
        self.assertIn("`wave_commit`、executor変更、C81直接child、bundle、profile、追加model runは作成しない", backlog)
        self.assertIn("B20でも100 / 100がroot-only", redesign)
        self.assertIn("fixture mode差によりC82とcompatibility keyが一致しない", redesign)


if __name__ == "__main__":
    unittest.main()

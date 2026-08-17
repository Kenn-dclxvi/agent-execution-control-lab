from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-natural-language-result-read-boundary-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-natural-language-validation-carrier-closure-r1"
N20_RESULT = ROOT / "evaluations/results/544afbe7e2444037932c7313da4489b6.json"
N20_AUDIT = ROOT / (
    "evaluations/results/"
    "candidate269-natural-language-validation-carrier-closure-"
    "f01-f02-f03-f10-entrypoint-n20-quality-and-route-audit-r1.json"
)
PROFILE_PREFIX = (
    "candidate269-natural-language-validation-carrier-closure-v14-reasoning-medium-"
    "f01-f02-f03-f10-entrypoint-global-m24"
)


class Candidate269Test(unittest.TestCase):
    def test_candidate268_is_direct_parent_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "19630df248b648690238757813941f55e97aa82c8b5597659a9e731d0877162f",
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in base["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_only_validation_closure_is_replaced(self) -> None:
        base = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        old = """変更後の必須検証は、対象、順序、個別の合格条件、停止条件がそろうまで開始できない。順に行う必須検証の途中結果をAIへ返してから、残りの検証を実行してはならない。ただし各検証は結果を区別できる個別の実行とし、一つのshell commandへ結合してはならない。失敗または利用不能になった検証に依存する後続は発行せず、必要な結果がすべてそろった後に一度だけ完了を判断する。追加要求や結果の失効がなければ、完了後にreadや検証を追加しない。"""
        new = """変更後の必須検証は、対象、順序、個別の合格条件、停止条件がそろうまで開始できない。

rootが検証のproducerである場合は、順番のあるすべての必須検証を、一つの実行票を完了させる一回の外側実行へ束ねる。この外側実行をvalidation wrapperとする。各検証はwrapperの内側で結果を区別できる個別の実行として順に行い、各終了状態をwrapperの内側で確認する。失敗または利用不能になった検証があれば、それに依存する後続を発行しない。個別検証の途中resultはAIへ返さず、発行済みの全resultをwrapperが終了した時に一度だけ返す。各検証を一つのshell commandへ結合してはいけない。

root以外が検証のproducerである場合も、すべての必須検証を、結果を区別できる個別の実行として一つのmodel stepから発行し、完了済みの全resultを一度だけAIへ返す。失敗または利用不能になった検証に依存する後続は発行しない。

必要な結果がすべてそろった後に一度だけ完了を判断する。追加要求やresultの失効がなければ、完了後にreadや検証を追加しない。"""
        self.assertIn(old, base)
        self.assertEqual(candidate, base.replace(old, new))

    def test_decision_boundary_and_validation_plan_are_preserved(self) -> None:
        base = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        base_decision = base.split("### DECISION_BOUNDARY\n", 1)[1].split("### VALIDATION_CLOSURE\n", 1)[0]
        candidate_decision = candidate.split("### DECISION_BOUNDARY\n", 1)[1].split("### VALIDATION_CLOSURE\n", 1)[0]
        self.assertEqual(candidate_decision, base_decision)
        base_plan = base.split("### VALIDATION_PLAN\n", 1)[1].split("### METHOD\n", 1)[0]
        candidate_plan = candidate.split("### VALIDATION_PLAN\n", 1)[1].split("### METHOD\n", 1)[0]
        self.assertEqual(candidate_plan, base_plan)

    def test_outer_validation_carrier_is_natural_language_only(self) -> None:
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        closure = candidate.split("### VALIDATION_CLOSURE\n", 1)[1].split("### VALIDATION_PLAN\n", 1)[0]
        self.assertIn("一回の外側実行へ束ねる", closure)
        self.assertIn("個別検証の途中resultはAIへ返さず", closure)
        self.assertIn("各検証を一つのshell commandへ結合してはいけない", closure)
        for forbidden in ("Candidate147", ":=", "∧", "validation_predicate_ready"):
            self.assertNotIn(forbidden, closure)

    def test_n20_variation_result_is_registered_and_stopped(self) -> None:
        result = json.loads(N20_RESULT.read_text(encoding="utf-8"))
        audit = json.loads(N20_AUDIT.read_text(encoding="utf-8"))

        self.assertEqual(result["result_id"], "544afbe7e2444037932c7313da4489b6")
        self.assertEqual(len(result["case_results"]), 80)
        self.assertEqual({row["quality_score"] for row in result["case_results"]}, {4})
        self.assertEqual(result["excluded_attempts"], [])
        self.assertEqual(result["median"]["total_tokens"], 532210.0)
        self.assertEqual(result["median"]["quality_score"], 100.0)

        self.assertEqual(audit["registered_result_id"], result["result_id"])
        self.assertEqual(audit["coverage"]["iterations_per_case"], 20)
        self.assertEqual(audit["coverage"]["run_count"], 80)
        self.assertEqual(audit["coverage"]["new_run_count"], 60)
        self.assertEqual(audit["coverage"]["valid_new_run_count"], 60)
        self.assertEqual(audit["coverage"]["score_counts"], {"4": 80})
        self.assertEqual(
            audit["kpi"]["case_medians"]["F02"]["mean_total_tokens_percent"],
            -2.28,
        )
        self.assertEqual(
            audit["route_diagnostics"]["F02"]["candidate147_upper_distribution_runs"],
            10,
        )
        self.assertEqual(audit["route_diagnostics"]["F02"]["candidate147_wait_runs"], 6)
        self.assertEqual(audit["route_diagnostics"]["F02"]["candidate147_wait_invocations"], 10)
        self.assertEqual(
            audit["interpretation"]["f02_route_comparison"][
                "candidate147_double_wait_rrpvww_runs"
            ],
            4,
        )
        self.assertEqual(
            audit["interpretation"]["f02_route_comparison"][
                "candidate269_double_wait_rrpvww_runs"
            ],
            0,
        )
        self.assertEqual(
            audit["interpretation"]["f02_median_cause"]["difference_total_tokens"],
            32646.0,
        )
        self.assertEqual(
            audit["interpretation"]["f02_median_cause"][
                "matched_wait_final_input_difference_tokens"
            ],
            15624,
        )
        self.assertEqual(
            audit["interpretation"]["shared_carrier_cause"]["f01_effect"][
                "post_validation_evidence_followup_runs"
            ],
            2,
        )
        self.assertEqual(
            audit["interpretation"]["shared_carrier_cause"]["f01_effect"][
                "followup_wait_output_characters"
            ],
            [70096, 71783],
        )
        self.assertIn(
            "all issued results",
            audit["interpretation"]["shared_carrier_cause"][
                "current_candidate_difference"
            ],
        )
        self.assertEqual(
            audit["interpretation"]["shared_carrier_cause"][
                "matched_internal_output_characters"
            ]["candidate269_full"],
            158840,
        )
        self.assertEqual(
            audit["interpretation"]["status"],
            "quality_passed_distribution_precision_extended_cost_regression_persists_stopped",
        )
        self.assertEqual(audit["disposition"]["standard14"], "not_started")
        self.assertEqual(audit["disposition"]["adoption"], "not_approved")

    def test_n20_profiles_change_only_repetition_count(self) -> None:
        profiles = ROOT / "evaluations/profiles"
        baseline = json.loads(
            (profiles / f"{PROFILE_PREFIX}-n5-cli0146-r1.json").read_text(encoding="utf-8")
        )

        def normalize(profile: dict[str, object]) -> dict[str, object]:
            normalized = deepcopy(profile)
            normalized["profile_id"] = baseline["profile_id"]
            normalized["iterations"] = 5
            normalized["comparison_conditions"]["repetition_condition"]["iterations"] = 5  # type: ignore[index]
            return normalized

        for iterations in (10, 15, 20):
            profile = json.loads(
                (
                    profiles
                    / f"{PROFILE_PREFIX}-n{iterations}-cli0146-r1.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(profile["iterations"], iterations)
            self.assertEqual(
                profile["comparison_conditions"]["repetition_condition"]["iterations"],
                iterations,
            )
            self.assertEqual(normalize(profile), baseline)


if __name__ == "__main__":
    unittest.main()

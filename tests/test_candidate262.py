from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C147 = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
C261 = ROOT / "prompts/candidates/the-caption-3ce91a4-spec-output-consumer-closure-r1"
C262 = ROOT / "prompts/candidates/the-caption-3ce91a4-spec-false-start-state-consumer-permission-r1"
C147_PROFILE = ROOT / "evaluations/profiles/candidate147-result-effect-scope-v14-reasoning-medium-a01-f03-global-m24-n5-cli0146-r1.json"
C262_PROFILE = ROOT / "evaluations/profiles/candidate262-spec-false-start-state-consumer-permission-v14-reasoning-medium-a01-f03-global-m24-n5-cli0146-r1.json"
C147_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate147-result-effect-scope-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
C262_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate262-spec-false-start-state-consumer-permission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate262-spec-false-start-state-consumer-permission-a01-f03-n5-mechanism-audit-r1.json"
STANDARD14_AUDIT = ROOT / "evaluations/results/candidate262-spec-false-start-state-consumer-permission-standard14-n5-quality-audit-r1.json"


class Candidate262Test(unittest.TestCase):
    def test_identity_and_direct_baseline(self) -> None:
        baseline = verify_bundle(C147)
        candidate = verify_bundle(C262)
        self.assertEqual(candidate["artifact"]["baseline_identity"], baseline["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], baseline["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "61c0735fc0cadcb0d45d2132346d01540d8366040ce886bb3f4332279915ba33",
        )

    def test_only_spec_false_start_state_permission_is_replaced(self) -> None:
        baseline = (C147 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (C262 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        old = (
            "`spec_ready=false`では`TaskSpec本文 / TaskSpec明示の開始状態の直接観測`だけを許可し、"
            "未固定のrequired outcome valueをclarification resultにして変更前evidence operationをterminalにする。"
        )
        new = (
            "`spec_ready=false`では`TaskSpec本文`だけを許可する。"
            "TaskSpec明示の開始状態の直接観測は、そのresultが未固定のrequired outcome value、"
            "clarification resultのpermissionまたはclarification operationのstop conditionを変え得る場合だけ許可する。"
            "未固定のrequired outcome valueをclarification resultにして変更前evidence operationをterminalにする。"
        )
        self.assertIn(old, baseline)
        self.assertEqual(candidate, baseline.replace(old, new))

    def test_candidate261_spec_output_rule_is_not_inherited(self) -> None:
        candidate261 = (C261 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate262 = (C262 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        added_by_candidate261 = "TaskSpecへの固定と固定した各項目の値は、作業を制御するための内部状態"
        self.assertIn(added_by_candidate261, candidate261)
        self.assertNotIn(added_by_candidate261, candidate262)

    def test_other_targets_are_byte_identical_to_candidate147(self) -> None:
        baseline = verify_bundle(C147)
        candidate = verify_bundle(C262)
        baseline_entries = {entry["target"]: entry for entry in baseline["files"]}
        candidate_entries = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual(baseline_entries.keys(), candidate_entries.keys())
        for target in baseline_entries:
            if target != "AGENTS.md":
                self.assertEqual(candidate_entries[target], baseline_entries[target])

    def test_prompt_size_is_bounded(self) -> None:
        c147 = (C147 / "files/AGENTS.md.txt").stat().st_size
        c261 = (C261 / "files/AGENTS.md.txt").stat().st_size
        c262 = (C262 / "files/AGENTS.md.txt").stat().st_size
        self.assertEqual((c147, c261, c262), (10772, 11198, 10954))
        self.assertLess(c262, c261)

    def test_a01_f03_profiles_change_only_prompt_identity(self) -> None:
        import json

        baseline = json.loads(C147_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C262_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            [case["id"] for case in candidate["cases"]],
            ["TC-A01-LATENT-MODE-POLICY", "TC-F03-ATOMIC-CONTEXT-CLEANUP"],
        )
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        baseline.pop("profile_id")
        candidate.pop("profile_id")
        baseline.pop("prompt_set_identity")
        candidate.pop("prompt_set_identity")
        self.assertEqual(candidate, baseline)

    def test_targeted_result_requires_human_judgement_before_expansion(self) -> None:
        import json

        audit = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(audit["score_4_count"], 10)
        self.assertEqual(audit["a01"]["no_start_state_check_count"], 5)
        self.assertEqual(audit["f03"]["reference_coissued_count"], 5)
        self.assertEqual(audit["f03"]["candidate_coissued_count"], 4)
        self.assertEqual(audit["judgement"]["a01_cost"], "tradeoff_requires_human_judgement")
        self.assertFalse(audit["judgement"]["expand_n"])
        self.assertFalse(audit["judgement"]["standard14_authorized"])

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        import json

        baseline = json.loads(C147_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C262_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(candidate["cases"]), 14)
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        baseline.pop("profile_id")
        candidate.pop("profile_id")
        baseline.pop("prompt_set_identity")
        candidate.pop("prompt_set_identity")
        self.assertEqual(candidate, baseline)

    def test_standard14_quality_is_complete(self) -> None:
        import json

        audit = json.loads(STANDARD14_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(audit["run_count"], 70)
        self.assertEqual(audit["rateable_runs"], 70)
        self.assertEqual(audit["score_counts"], {"4": 70})
        self.assertEqual(audit["failure_counts"], {})


if __name__ == "__main__":
    unittest.main()

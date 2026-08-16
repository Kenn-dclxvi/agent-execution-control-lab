from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C147 = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
C237 = ROOT / "prompts/candidates/the-caption-3ce91a4-taskspec-progress-suppression-r1"
C254 = ROOT / "prompts/candidates/the-caption-3ce91a4-independent-check-same-model-step-r1"
C261 = ROOT / "prompts/candidates/the-caption-3ce91a4-spec-output-consumer-closure-r1"
C147_PROFILE = ROOT / "evaluations/profiles/candidate147-result-effect-scope-v14-reasoning-medium-a01-f03-global-m24-n5-cli0146-r1.json"
C261_PROFILE = ROOT / "evaluations/profiles/candidate261-spec-output-consumer-closure-v14-reasoning-medium-a01-f03-global-m24-n5-cli0146-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate261-spec-output-consumer-closure-a01-f03-n5-mechanism-audit-r1.json"


class Candidate261Test(unittest.TestCase):
    def test_identity_and_direct_baseline(self) -> None:
        baseline = verify_bundle(C147)
        candidate = verify_bundle(C261)
        self.assertEqual(candidate["artifact"]["baseline_identity"], baseline["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], baseline["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "e651154c31525acf346ce42f0dd002e79522ecb0b5cc478fb56d272df763b7ad",
        )

    def test_only_candidate237_spec_boundary_is_added(self) -> None:
        baseline = (C147 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        proven = (C237 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (C261 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        boundary = (
            "TaskSpecへの固定と固定した各項目の値は、作業を制御するための内部状態であり、"
            "固定した事実も、その内容も、利用者向けの進捗として出力してはいけない。"
            "これは、利用者が決める必要のある成果の値を尋ねること、permissionを拒否されたため停止を伝えること、"
            "完了したoperationの最終結果を返すことを妨げない。"
        )
        marker = "未固定のrequired outcome valueだけをclarification resultにする。"
        self.assertIn(boundary, proven)
        self.assertEqual(candidate, baseline.replace(marker, marker + boundary))

    def test_c147_result_effect_scope_and_other_targets_are_preserved(self) -> None:
        baseline_manifest = verify_bundle(C147)
        candidate_manifest = verify_bundle(C261)
        baseline_entries = {entry["target"]: entry for entry in baseline_manifest["files"]}
        candidate_entries = {entry["target"]: entry for entry in candidate_manifest["files"]}
        self.assertEqual(baseline_entries.keys(), candidate_entries.keys())
        for target in baseline_entries:
            if target != "AGENTS.md":
                self.assertEqual(candidate_entries[target], baseline_entries[target])
        baseline = (C147 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (C261 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        decision = baseline.split("- DECISION_BOUNDARY: ", 1)[1].split("\n- VALIDATION_CLOSURE:", 1)[0]
        self.assertIn(decision, candidate)

    def test_prompt_size_is_bounded(self) -> None:
        c147 = (C147 / "files/AGENTS.md.txt").stat().st_size
        c237 = (C237 / "files/AGENTS.md.txt").stat().st_size
        c254 = (C254 / "files/AGENTS.md.txt").stat().st_size
        c261 = (C261 / "files/AGENTS.md.txt").stat().st_size
        self.assertEqual((c147, c237, c254, c261), (10772, 15271, 13628, 11198))
        self.assertLess(c261, c237)
        self.assertLess(c261, c254)

    def test_a01_f03_profiles_change_only_prompt_identity(self) -> None:
        baseline = json.loads(C147_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C261_PROFILE.read_text(encoding="utf-8"))
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

    def test_targeted_result_does_not_authorize_expansion(self) -> None:
        audit = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(audit["score_4_count"], 10)
        self.assertEqual(audit["a01"]["no_start_state_check_count"], 4)
        self.assertEqual(audit["f03"]["reference_coissued_count"], 5)
        self.assertEqual(audit["f03"]["candidate_coissued_count"], 1)
        self.assertEqual(audit["judgement"]["cost"], "unjustified_cost_regression")
        self.assertFalse(audit["judgement"]["expand_n"])
        self.assertFalse(audit["judgement"]["standard14_authorized"])


if __name__ == "__main__":
    unittest.main()

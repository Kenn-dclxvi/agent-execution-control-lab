from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C96 = ROOT / "prompts/candidates/the-caption-3ce91a4-successful-validation-result-projection-r1"
DESIGN = ROOT / "docs/candidate96-successful-validation-result-projection-design.md"
RESULT = ROOT / "evaluations/results/candidate81-candidate96-successful-validation-result-projection-v14-medium-f02-n5-cli0146_2026-07-30.md"
BASELINE_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-f02-global-m5-n5-cli0146-r1.json"
CANDIDATE_PROFILE = ROOT / "evaluations/profiles/candidate96-successful-validation-result-projection-v14-reasoning-medium-f02-global-m5-n5-cli0146-r1.json"


def blocks(text: str) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in text.splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate96Test(unittest.TestCase):
    def test_is_direct_c81_child_with_one_changed_target(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C96)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_replaces_only_validation_closure(self) -> None:
        source = blocks((C81 / "files/AGENTS.md.txt").read_text())
        candidate = blocks((C96 / "files/AGENTS.md.txt").read_text())
        self.assertEqual(source.keys(), candidate.keys())
        changed = [label for label in source if source[label] != candidate[label]]
        self.assertEqual(changed, ["VALIDATION_CLOSURE"])
        rule = candidate["VALIDATION_CLOSURE"]
        self.assertIn("identity / exact command / exit codeだけを一度modelへ返し", rule)
        self.assertIn("successのstdout / stderrを返さない", rule)
        self.assertIn("該当tool resultを省略せず一度modelへ返す", rule)
        self.assertNotIn("4096 bytes", rule)

    def test_manifest_records_candidate_boundary(self) -> None:
        candidate = verify_bundle(C96)
        artifact = candidate["artifact"]
        self.assertEqual(artifact["baseline_identity"], "the-caption-3ce91a4-validation-wrapper-precedence-r1")
        self.assertEqual(artifact["evaluation_status"], "not_evaluated")
        self.assertEqual(artifact["state"], "draft")
        self.assertIn("executor adapter", " ".join(artifact["non_goals"]))

    def test_design_keeps_task_spec_and_completion_wave_out_of_scope(self) -> None:
        design = DESIGN.read_text()
        self.assertIn("TaskSpec、repository authority、required validation、評価条件、executor adapterは変更しない", design)
        self.assertIn("completion evidenceを同じwaveへ統合する変更も本Candidateへ混ぜない", design)
        self.assertIn("F01 3件、F02 5件", design)
        self.assertIn("F02 r1 `N=5`", design)

    def test_f02_profiles_change_only_prompt_identity(self) -> None:
        baseline = json.loads(BASELINE_PROFILE.read_text())
        candidate = json.loads(CANDIDATE_PROFILE.read_text())
        for key in ("cases", "comparison_conditions", "evaluation_set", "execution", "scope"):
            self.assertEqual(baseline[key], candidate[key])
        self.assertEqual(baseline["comparison_conditions"]["agent_environment"]["codex_cli"], "0.146.0")
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], verify_bundle(C96)["bundle_sha256"])
        self.assertNotEqual(baseline["prompt_set_identity"], candidate["prompt_set_identity"])

    def test_f02_result_records_failed_mechanism_gate(self) -> None:
        result = RESULT.read_text()
        self.assertIn("compatibility keyも一致", result)
        self.assertIn("success projectionは`0 / 5`", result)
        self.assertIn("token中央値はCandidate81比`-11.03%`", result)
        self.assertIn("elapsed中央値は`-15.78%`", result)
        self.assertIn("targeted_f02_evaluated / mechanism_gate_failed / stopped", result)
        self.assertIn("TaskSpec変更: なし", result)
        self.assertIn("executor adapterまたは開発環境変更: なし", result)
        self.assertIn("全token差`272,338`の`99.10%`はinput token差", result)
        self.assertIn("full gate重複を除く感度分析", result)
        self.assertIn("Candidate81 B20分布との診断比較", result)
        self.assertIn("token=likely_sampling_variation", result)
        self.assertIn("elapsed=shift_observed_but_unattributed", result)
        self.assertIn("最新Candidate81 Standard14 B20", result)
        self.assertIn("各case `N=5`、global queue `M=24`を20 batch", result)
        self.assertIn("Candidate96以下が`0.118%`", result)
        self.assertIn("input / route削減: `observed_but_unattributed`", result)
        self.assertIn("保存traceによるelapsed差の分解", result)
        self.assertIn("focused＋full validation実時間", result)
        self.assertIn("output token | `0.799`", result)
        self.assertIn("`5 / 13`（`38.46%`）", result)
        self.assertIn("model_work_reduction_observed_but_unattributed", result)
        self.assertIn("validation実時間またはraw output量による説明: `not_supported`", result)
        self.assertIn("下振れ側へ寄せるためのC81内分布分析", result)
        self.assertIn("agent message `<=5`", result)
        self.assertIn("full gate 2回", result)
        self.assertIn("inspection / completion decision-round closure", result)
        self.assertIn("reasoning tokenの直接上限は品質を損なう可能性があるため設けない", result)
        self.assertIn("KPI改善の因果確定: `not_established`", result)


if __name__ == "__main__":
    unittest.main()

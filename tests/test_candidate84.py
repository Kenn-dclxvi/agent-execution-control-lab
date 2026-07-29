from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C83 = ROOT / "prompts/candidates/the-caption-3ce91a4-delegation-value-boundary-r1"
C84 = ROOT / "prompts/candidates/the-caption-3ce91a4-delegation-marginal-value-boundary-r1"
DESIGN = ROOT / "docs/candidate84-delegation-marginal-value-boundary-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate84-delegation-marginal-value-boundary-v14-reasoning-medium-delegation-value-f02-global-m5-n5-r1.json"
RESULT = ROOT / "evaluations/results/candidate84-delegation-marginal-value-boundary-v14-medium-f02-n5_2026-07-28.md"


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if line.startswith("- "):
            label, body = line[2:].split(": ", 1)
            blocks[label] = body
    return blocks


class Candidate84Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate83(self) -> None:
        source = verify_bundle(C83)
        candidate = verify_bundle(C84)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-delegation-marginal-value-boundary-r1",
        )
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

    def test_replaces_only_owner_role(self) -> None:
        source = labelled_blocks((C83 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C84 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(list(candidate), list(source))
        self.assertEqual(
            {label for label in source if source[label] != candidate[label]},
            {"OWNER_ROLE"},
        )

    def test_uses_state_not_independence_word_for_worker_value(self) -> None:
        owner = labelled_blocks((C84 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))["OWNER_ROLE"]
        self.assertNotIn("TaskSpecが独立性を要求", owner)
        for state in (
            "exclusive_worker_scope_ready",
            "separate_identity_required",
            "parallel_gain_ready",
            "context_gain_ready",
            "capability_gain_ready",
            "unresolved_judgment_gain_ready",
        ):
            self.assertIn(f"`{state}", owner)
        self.assertIn("criterion owner、risk owner、`independent`語列、独立確認という作業名だけでは", owner)
        self.assertIn("workerが同じevidenceを再読するだけなら`delegation_value_ready=false`", owner)
        self.assertIn("falseならrootをproducerへbindする", owner)
        self.assertIn("trueなら起動前にworkerのtask identityをproducerへbind", owner)
        self.assertIn("`delegated_result_ready :=", owner)

    def test_design_fixes_order_and_stop_boundaries(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("評価順はF02 N=5、F04 N=5、D01 N=5", design)
        self.assertIn("A06はAI裁量の正例を観測する別diagnostic", design)
        self.assertIn("F02 / F04でWorkerが1件でも起動した場合は停止", design)
        self.assertIn("Candidate82またはCandidate83は再実行しない", design)

    def test_f02_profile_binds_candidate84_and_fixed_conditions(self) -> None:
        manifest = verify_bundle(C84)
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"}])
        self.assertEqual(profile["comparison_conditions"]["executor_parameters"]["reasoning_effort"], "medium")
        self.assertEqual(profile["comparison_conditions"]["repetition_condition"]["iterations"], 5)
        self.assertEqual(profile["comparison_conditions"]["quality_rating"]["contract_id"], "outcome-terminal-state-evidence-owner-diagnostic-v14")
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "bundle_sha256": manifest["bundle_sha256"],
                "name": manifest["prompt_identity"],
                "revision": "r1",
            },
        )

    def test_f02_result_preserves_quality_route_and_stop_boundaries(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        self.assertIn("741581e8622147b3897c5b7e81588825", result)
        self.assertIn("5 / 5", result)
        self.assertIn("3 / 5はroot-only", result)
        self.assertIn("2 / 5は価値のないtest-contract再確認Worker", result)
        self.assertIn("targeted_f02_evaluated / stopped", result)
        self.assertIn("F04、D01、A06、標準14、採用、release、THE-CAPTION本体反映へ進めない", result)
        self.assertIn("Candidate82とCandidate83は再実行していない", result)
        self.assertIn("compatibility keyは一致しない", result)


if __name__ == "__main__":
    unittest.main()

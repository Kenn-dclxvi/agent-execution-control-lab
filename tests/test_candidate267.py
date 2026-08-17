from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-start-identity-result-effect-scope-restoration-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-declared-instruction-read-permission-restoration-r1"
PROFILE = ROOT / "evaluations/profiles/candidate267-declared-instruction-read-permission-restoration-v14-reasoning-medium-f01-f02-f03-f10-entrypoint-global-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/e4dee1e302a2468ba055500a0c3610d7.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate267-declared-instruction-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate267-declared-instruction-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json"


class Candidate267Test(unittest.TestCase):
    def test_candidate264_is_direct_base_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "f76cd120292ba1ca6e8752e3bd15ca3376571fe176db722b1650353400216684",
        )
        base_unchanged = [entry for entry in base["files"] if entry["target"] != "AGENTS.md"]
        candidate_unchanged = [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"]
        self.assertEqual(candidate_unchanged, base_unchanged)

    def test_only_machine_bound_instruction_dependency_is_added(self) -> None:
        base = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        paragraph = (
            "TaskSpecがread対象としてnormalized exact path `D/AGENTS.md`を明示した場合、"
            "`declared_instruction(D) := true`とする。"
            "`declared_descendant_read(read, D) := normalized(read.target) != D/AGENTS.md ∧ "
            "normalized(read.target)がD/配下`、`instruction_result_ready(D) := D/AGENTS.mdへbindした"
            "read invocationがterminal success ∧ そのcontent resultを受領済み`とする。"
            "`declared_instruction(D)=true ∧ declared_descendant_read(read, D)=true ∧ "
            "instruction_result_ready(D)=false`の間は、そのreadを`authorized_read=false`とする。"
            "この否定は一般的なread permission、TaskSpecによる配下pathの列挙、`result_effect_scope`および"
            "開始確認の停止範囲より優先し、`D/AGENTS.md`自身のreadには適用しない。\n\n"
        )
        marker = "### VALIDATION_CLOSURE\n"
        self.assertEqual(candidate, base.replace(marker, paragraph + marker))
        self.assertIn("normalized(read.target)がD/配下", candidate)
        self.assertIn("read invocationがterminal success", candidate)
        self.assertNotIn("instruction_dependency_pending(read)", candidate)
        self.assertNotIn("そのinstruction resultがreadの対象、permissionまたはstop conditionを変え得る", candidate)
        self.assertNotIn("terminalかつcompatibleなinstruction result", candidate)

    def test_candidate265_and_candidate266_are_not_inherited_as_bases(self) -> None:
        candidate = verify_bundle(CANDIDATE)
        provenance = candidate["provenance"]
        self.assertIn("Candidate264 is the direct base", provenance["source_interpretation"])
        self.assertIn("Candidate265 supplies the failed self-classification route only", provenance["source_interpretation"])
        self.assertIn("Candidate266 supplies off-target diagnostic evidence", provenance["source_interpretation"])
        self.assertNotEqual(
            candidate["artifact"]["baseline_identity"],
            "the-caption-3ce91a4-instruction-result-read-permission-restoration-r1",
        )
        self.assertNotEqual(
            candidate["artifact"]["baseline_identity"],
            "the-caption-3ce91a4-declared-instruction-descendant-read-dependency-r1",
        )

    def test_profile_is_fixed_to_four_cases_and_n5(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "bundle_sha256": "f76cd120292ba1ca6e8752e3bd15ca3376571fe176db722b1650353400216684",
                "name": "the-caption-3ce91a4-declared-instruction-read-permission-restoration-r1",
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

    def test_targeted_n5_passes_mechanism_and_stops_on_cost(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "e4dee1e302a2468ba055500a0c3610d7")
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(quality["score_counts"], {"4": 20})
        for case in ("f01", "f02", "f03"):
            gate = mechanism["gates"][f"{case}_start_identity_and_authorized_read_shared_ai_decision"]
            self.assertEqual(gate["candidate267"], {"pass_count": 5, "failure_count": 0})
        f10 = mechanism["gates"]["f10_instruction_terminal_result_preceded_descendant_listing_and_content"]
        self.assertEqual(f10["candidate267"]["pass_count"], 5)
        self.assertEqual(f10["candidate267"]["failure_count"], 0)
        self.assertIn("unjustified_cost_regression_stopped", mechanism["status"])
        self.assertEqual(mechanism["disposition"]["standard14"], "not_started")


if __name__ == "__main__":
    unittest.main()

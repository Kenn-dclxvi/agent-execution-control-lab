from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-c147-direct-human-translation-r1"
DESIGN = ROOT / "docs/candidate227-c147-direct-human-translation-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate227-c147-direct-human-translation-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/2f1ff97cd8e64690b4eaec3e512f4589.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate227-c147-direct-human-translation-standard14-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate227-c147-direct-human-translation-standard14-n5-mechanism-audit-r1.json"


class Candidate227Test(unittest.TestCase):
    def test_c147_direct_candidate_changes_only_root_agents(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["artifact"]["state"], "evaluation_ready")
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "bc43decca672dff6ed57d5a91eef09cdba86c50a5dc53f4bb6783ea06c11f54a",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_thirteen_c147_groups_are_translated_one_to_one(self) -> None:
        base_lines = (BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        candidate_lines = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len([line for line in base_lines if line.startswith("- ")]), 13)
        self.assertEqual(len([line for line in candidate_lines if line.startswith("- ")]), 13)
        translated = "\n".join(candidate_lines)
        for heading in (
            "利用者が決めること",
            "担当の固定",
            "完了の扱い",
            "分担へ渡す情報",
            "調査の許可",
            "分担結果の受領",
            "親側の役割",
            "独立した判定",
            "結果の影響範囲",
            "検証の完了",
            "検証実行票",
            "実行手段",
            "環境回復",
        ):
            self.assertIn(f"- {heading}:", translated)
        self.assertNotIn("custom exec wrapper", translated)
        self.assertNotIn("model step", translated)
        self.assertIn("どれか一つの結果を次の判断に使う前に", translated)

    def test_standard14_profile_preserves_candidate147_conditions(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(profile["cases"]), 14)
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"],
            verify_bundle(CANDIDATE)["bundle_sha256"],
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate225の10節とCandidate226の一項目翻訳は継承しない", design)
        self.assertIn("Standard14から観測できない機能は未評価", design)

    def test_standard14_result_preserves_quality_and_stops_on_mechanism(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "2f1ff97cd8e64690b4eaec3e512f4589")
        self.assertEqual(result["compatibility_key"], "cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561")
        self.assertEqual(quality["score_counts"], {"4": 70})
        self.assertEqual(mechanism["gates"]["a02_result_effect_scope"]["failure_count"], 3)
        self.assertEqual(mechanism["gates"]["criterion_owner_did_not_create_producer"]["failure_count"], 3)
        self.assertEqual(mechanism["status"], "mechanism_failed")


if __name__ == "__main__":
    unittest.main()

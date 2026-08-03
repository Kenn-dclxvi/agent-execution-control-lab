from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "prompts/candidates/the-caption-3ce91a4-control-free-repository-r1"
C152 = ROOT / "prompts/candidates/the-caption-3ce91a4-four-decision-rules-readable-r1"
PROFILE = ROOT / "evaluations/profiles/candidate152-four-decision-rules-readable-v14-reasoning-medium-a01-a02-f01-f02-f04-f07-global-m24-n5-cli0146-r1.json"
PROFILE_F08 = ROOT / "evaluations/profiles/candidate152-four-decision-rules-readable-v14-reasoning-medium-f08-global-m24-n5-cli0146-r1.json"
PROFILE_F03 = ROOT / "evaluations/profiles/candidate152-four-decision-rules-readable-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"


class Candidate152Test(unittest.TestCase):
    def test_free_child_changes_only_root_to_four_published_sentences(self) -> None:
        free = verify_bundle(FREE)
        candidate = verify_bundle(C152)
        self.assertEqual(candidate["artifact"]["baseline_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])

        free_files = {entry["target"]: entry for entry in free["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual(set(candidate_files), set(free_files))
        changed = [target for target in sorted(free_files) if free_files[target] != candidate_files[target]]
        self.assertEqual(changed, ["AGENTS.md"])

        text = (C152 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(
            text.splitlines(),
            [
                "- 仕様を決めるとき: 利用者が決めるべき結果が書かれていないなら、コードやテストを調べず、その結果だけを質問する一方、ファイルの場所や実装方法が分からないだけなら、プロジェクト内の情報から自分で決めて進める。",
                "- 変更を始めるとき: 必要な成果をすべて挙げ、それぞれをどこでどう直し、何を壊さず残すかまで一つの方針にできた場合だけ変更を始め、どれか一つでも分からないなら変更しない。",
                "- 調べるとき: 調査は未完了の成果を決めるために必要なものだけに絞り、先の結果で調べる内容が変わらないものはまとめて行い、実装方法探し・決定済み事項の再確認・念のため・報告用には行わない。",
                "- 作業を終えるとき: 変更後は必要なテストと差分確認を先に一式決めて順に実行し、失敗したらそこで止まり、すべての結果が揃ったら一度だけ完了を判断して追加確認しない。",
            ],
        )

    def test_targeted_profile_uses_only_standard14_cases(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        candidate = verify_bundle(C152)
        self.assertEqual(profile["evaluation_set"], {"revision": "r1", "set_id": "the-caption-standard14-r1"})
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            [
                "TC-A01-LATENT-MODE-POLICY",
                "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING",
                "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
                "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND",
                "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY",
                "TC-F07-DEPENDENCY-PROVENANCE-PAIR",
            ],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["name"], candidate["prompt_identity"])
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])

    def test_discriminating_profile_uses_standard14_f08(self) -> None:
        profile = json.loads(PROFILE_F08.read_text(encoding="utf-8"))
        candidate = verify_bundle(C152)
        self.assertEqual(profile["evaluation_set"], {"revision": "r1", "set_id": "the-caption-standard14-r1"})
        self.assertEqual(profile["cases"], [{"id": "TC-F08-CANONICAL-CLI-REFERENCE-SYNC", "revision": "r1"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["name"], candidate["prompt_identity"])
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])

    def test_completion_profile_uses_standard14_f03(self) -> None:
        profile = json.loads(PROFILE_F03.read_text(encoding="utf-8"))
        candidate = verify_bundle(C152)
        self.assertEqual(profile["evaluation_set"], {"revision": "r1", "set_id": "the-caption-standard14-r1"})
        self.assertEqual(profile["cases"], [{"id": "TC-F03-ATOMIC-CONTEXT-CLEANUP", "revision": "r2"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["name"], candidate["prompt_identity"])
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()

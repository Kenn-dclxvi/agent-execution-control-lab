from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import (
    BundleError,
    INSTRUCTION_BASENAMES,
    STORAGE_FORMAT_LEGACY,
    STORAGE_FORMAT_SUFFIXED,
    STORE_SUFFIX,
    bundle_sha256,
    ensure_representable,
    stored_link_target,
    stored_relpath,
    target_from_stored,
    verify_bundle,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def bundle_dirs() -> list[Path]:
    return sorted(p.parent for p in REPO_ROOT.glob("prompts/**/manifest.json"))


class StorageHelperTest(unittest.TestCase):
    def test_suffixed_roundtrip_for_instruction_paths(self) -> None:
        for target in ("AGENTS.md", "CLAUDE.md", "docs/AGENTS.md", "src/CLAUDE.md"):
            stored = stored_relpath(target, STORAGE_FORMAT_SUFFIXED)
            self.assertTrue(stored.endswith(STORE_SUFFIX))
            self.assertEqual(target_from_stored(stored, STORAGE_FORMAT_SUFFIXED), target)

    def test_non_instruction_paths_are_untouched(self) -> None:
        for target in ("docs/prompt-guide.md", "prompts/plan.md", "src/main.py"):
            self.assertEqual(stored_relpath(target, STORAGE_FORMAT_SUFFIXED), target)
            self.assertEqual(target_from_stored(target, STORAGE_FORMAT_SUFFIXED), target)

    def test_legacy_format_is_identity_mapping(self) -> None:
        for target in ("AGENTS.md", "docs/CLAUDE.md", "src/main.py"):
            self.assertEqual(stored_relpath(target, STORAGE_FORMAT_LEGACY), target)
            self.assertEqual(target_from_stored(target, STORAGE_FORMAT_LEGACY), target)

    def test_symlink_target_mapping(self) -> None:
        self.assertEqual(
            stored_link_target("AGENTS.md", STORAGE_FORMAT_SUFFIXED), "AGENTS.md" + STORE_SUFFIX
        )
        self.assertEqual(stored_link_target("AGENTS.md", STORAGE_FORMAT_LEGACY), "AGENTS.md")

    def test_roundtrip_holds_across_suffix_boundary(self) -> None:
        # 「instruction名 + suffix」を除く許容 target で往復が成立する。
        representable = [
            "AGENTS.md",
            "CLAUDE.md",
            "docs/AGENTS.md",
            "src/CLAUDE.md",
            "docs/prompt-guide.md",
            "AGENTS.md.txt.txt",  # basename が instruction 名ではないので許容
            "notes/AGENTS.markdown",
        ]
        for target in representable:
            with self.subTest(target=target):
                stored = stored_relpath(target, STORAGE_FORMAT_SUFFIXED)
                self.assertEqual(target_from_stored(stored, STORAGE_FORMAT_SUFFIXED), target)

    def test_instruction_plus_suffix_targets_are_rejected(self) -> None:
        # 逆写像が別 target へ潰れる pathological な名前は表現不能として拒否する。
        for target in ("AGENTS.md.txt", "CLAUDE.md.txt", "docs/AGENTS.md.txt"):
            with self.subTest(target=target):
                with self.assertRaises(BundleError):
                    ensure_representable(target, STORAGE_FORMAT_SUFFIXED)

    def test_representable_targets_pass(self) -> None:
        for target in ("AGENTS.md", "docs/CLAUDE.md", "src/main.py", "AGENTS.md.txt.txt"):
            with self.subTest(target=target):
                ensure_representable(target, STORAGE_FORMAT_SUFFIXED)  # 例外なし

    def test_legacy_format_reserves_nothing(self) -> None:
        # legacy は恒等写像なので、いかなる target も表現できる。
        for target in ("AGENTS.md.txt", "CLAUDE.md.txt", "docs/AGENTS.md.txt"):
            with self.subTest(target=target):
                ensure_representable(target, STORAGE_FORMAT_LEGACY)  # 例外なし

    def test_stored_paths_are_injective(self) -> None:
        # 異なる論理 target が同一 stored path へ衝突しないこと（許容 target 空間上）。
        candidates = [
            "AGENTS.md",
            "CLAUDE.md",
            "docs/AGENTS.md",
            "docs/CLAUDE.md",
            "src/AGENTS.md",
            "docs/prompt-guide.md",
            "prompts/plan.md",
            "AGENTS.md.txt.txt",
        ]
        stored = {}
        for target in candidates:
            ensure_representable(target, STORAGE_FORMAT_SUFFIXED)
            path = stored_relpath(target, STORAGE_FORMAT_SUFFIXED)
            self.assertNotIn(path, stored, f"collision: {target} vs {stored.get(path)} -> {path}")
            stored[path] = target


class LegacyBundleCompatTest(unittest.TestCase):
    def test_legacy_layout_still_verifies(self) -> None:
        # storage_format 未指定の従来レイアウト（files/AGENTS.md を実体名で格納）が
        # 引き続き検証できること（後方互換）。
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp)
            files_root = bundle / "files"
            files_root.mkdir()
            content = b"legacy root\n"
            (files_root / "AGENTS.md").write_bytes(content)
            entry = {
                "git_blob_sha1": "0" * 40,
                "mode": "100644",
                "sha256": __import__("hashlib").sha256(content).hexdigest(),
                "target": "AGENTS.md",
                "type": "file",
            }
            manifest = {
                "bundle_sha256": bundle_sha256([entry]),
                "files": [entry],
                "prompt_identity": "legacy-r1",
                "schema_version": "the-caption-prompt.bundle/v1",
            }
            (bundle / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            verified = verify_bundle(bundle)
            self.assertNotIn("storage_format", verified)

    def test_suffixed_bundle_rejects_unrepresentable_target(self) -> None:
        # instruction名+suffix の target を宣言した suffixed bundle は verify で拒否。
        import hashlib

        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp)
            files_root = bundle / "files"
            files_root.mkdir()
            content = b"pathological\n"
            (files_root / "AGENTS.md.txt").write_bytes(content)
            entry = {
                "git_blob_sha1": "0" * 40,
                "mode": "100644",
                "sha256": hashlib.sha256(content).hexdigest(),
                "target": "AGENTS.md.txt",
                "type": "file",
            }
            manifest = {
                "bundle_sha256": bundle_sha256([entry]),
                "files": [entry],
                "prompt_identity": "bad-r1",
                "schema_version": "the-caption-prompt.bundle/v1",
                "storage_format": STORAGE_FORMAT_SUFFIXED,
            }
            (bundle / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            with self.assertRaises(BundleError):
                verify_bundle(bundle)

    def test_suffixed_bundle_rejects_alias_trigger_file(self) -> None:
        # 正規の AGENTS.md.txt に加えて非正規の AGENTS.md（自動読込対象）が存在する
        # bundle は、manifest 未列挙ファイルとして拒否されなければならない。
        import hashlib

        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp)
            files_root = bundle / "files"
            files_root.mkdir()
            content = b"root instructions\n"
            (files_root / "AGENTS.md.txt").write_bytes(content)  # 正規
            (files_root / "AGENTS.md").write_bytes(b"stray trigger\n")  # 非正規 alias
            entry = {
                "git_blob_sha1": "0" * 40,
                "mode": "100644",
                "sha256": hashlib.sha256(content).hexdigest(),
                "target": "AGENTS.md",
                "type": "file",
            }
            manifest = {
                "bundle_sha256": bundle_sha256([entry]),
                "files": [entry],
                "prompt_identity": "alias-r1",
                "schema_version": "the-caption-prompt.bundle/v1",
                "storage_format": STORAGE_FORMAT_SUFFIXED,
            }
            (bundle / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            with self.assertRaises(BundleError):
                verify_bundle(bundle)


class RepositoryBundleStorageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bundles = bundle_dirs()

    def test_repository_has_bundles(self) -> None:
        self.assertGreater(len(self.bundles), 0)

    def test_no_instruction_named_files_at_rest(self) -> None:
        # working tree: prompts/**/files 配下に自動読込対象名(AGENTS.md/CLAUDE.md)を
        # 実体名で置かない。
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in (REPO_ROOT / "prompts").rglob("*")
            if "/files/" in (path.as_posix() + "/")
            and path.name in INSTRUCTION_BASENAMES
            and (path.is_file() or path.is_symlink())
        ]
        self.assertEqual(offenders, [], f"instruction-named files stored at rest: {offenders}")

    def test_no_instruction_named_files_tracked(self) -> None:
        # git index 側でも回帰しないこと。
        tracked = subprocess.run(
            ["git", "ls-files", "--", "prompts/**/files/**/AGENTS.md",
             "prompts/**/files/AGENTS.md", "prompts/**/files/**/CLAUDE.md",
             "prompts/**/files/CLAUDE.md"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
        self.assertEqual(tracked, [])

    def test_live_docs_have_no_dangling_bundle_file_reference(self) -> None:
        # root AGENTS.md と docs/ 配下の live 文書が参照する prompts/**/files/ の
        # 実ファイルpathは、格納名変更後も必ず実在すること（Agentが読む正本参照）。
        # bundle 内部 manifest の historical provenance path は対象外（immutable記録）。
        doc_files = [REPO_ROOT / "AGENTS.md"]
        doc_files += sorted((REPO_ROOT / "docs").rglob("*.md"))
        # prompts から始まる（任意の ../ 接頭辞つき）、/files/ を含む path トークン。
        token = re.compile(r'((?:\.\./)*prompts/[^\s`)\]]+/files/[^\s`)\]]+)')
        dangling: list[str] = []
        for doc in doc_files:
            base = doc.parent
            for match in token.finditer(doc.read_text(encoding="utf-8")):
                ref = match.group(1).rstrip(".,)")
                resolved = (base / ref) if ref.startswith("../") else (REPO_ROOT / ref)
                if not resolved.exists():
                    dangling.append(f"{doc.relative_to(REPO_ROOT)}: {ref}")
        self.assertEqual(dangling, [], f"dangling bundle-file references: {dangling}")

    def test_all_bundles_suffixed_verify_and_hash_invariant(self) -> None:
        for bundle in self.bundles:
            with self.subTest(bundle=bundle.relative_to(REPO_ROOT).as_posix()):
                manifest = verify_bundle(bundle)
                self.assertEqual(manifest.get("storage_format"), STORAGE_FORMAT_SUFFIXED)
                # bundle_sha256 は files 由来。verify を通過した時点で
                # 保存 hash == files 由来 hash が成立している。
                recomputed = bundle_sha256(
                    [{k: v for k, v in e.items() if isinstance(v, str)} for e in manifest["files"]]
                )
                self.assertEqual(manifest["bundle_sha256"], recomputed)

    def test_bundle_identities_match_pre_reencoding_snapshot(self) -> None:
        # storage re-encoding gate（docs/repository-contract.md §6）:
        # 移行対象の件数と各identityを固定し、その欠落・変更を検出する。
        # 移行後に別identityとして追加したbundleは、この履歴一覧の対象外。
        # 追加分も含む全bundleの内容とhashは直前の検証で確認する。
        snapshot = json.loads(
            (REPO_ROOT / "tests" / "bundle_identity_snapshot.json").read_text(encoding="utf-8")
        )
        expected = snapshot["bundle_sha256"]
        actual = {}
        for bundle in self.bundles:
            manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
            actual[bundle.relative_to(REPO_ROOT / "prompts").as_posix()] = manifest["bundle_sha256"]
        self.assertEqual(len(expected), snapshot["count"])
        self.assertEqual({name: actual.get(name) for name in expected}, expected)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = REPO_ROOT / "evaluations" / "profiles"
PROFILE_README = PROFILES_DIR / "README.md"
PROFILE_INDEX_DIR = PROFILES_DIR / "index"
PROFILE_LINK_RE = re.compile(r"\]\(([^)]+\.json)(?:#[^)]+)?\)")
INDEX_LINK_RE = re.compile(r"\]\((index/[^)]+\.md)(?:#[^)]+)?\)")


class ProfileIndexCoverageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_files = {
            path.name for path in PROFILES_DIR.glob("*.json") if path.is_file()
        }
        self.index_files = {
            path.relative_to(PROFILES_DIR).as_posix()
            for path in PROFILE_INDEX_DIR.glob("*.md")
            if path.is_file()
        }

        readme = PROFILE_README.read_text(encoding="utf-8")
        self.linked_index_files = set(INDEX_LINK_RE.findall(readme))

        index_documents = [(PROFILE_README, readme)]
        for path in sorted(PROFILE_INDEX_DIR.glob("*.md")):
            index_documents.append((path, path.read_text(encoding="utf-8")))
        self.profile_links = [
            (source, target)
            for source, document in index_documents
            for target in PROFILE_LINK_RE.findall(document)
        ]
        self.linked_profiles = {Path(target).name for _, target in self.profile_links}

    def test_all_profile_json_files_are_linked_from_index(self) -> None:
        missing = sorted(self.profile_files - self.linked_profiles)
        self.assertEqual(
            missing,
            [],
            "READMEまたはREADME直結indexからlinkされていないprofile JSON:\n"
            + "\n".join(missing),
        )

    def test_profile_json_links_are_not_stale(self) -> None:
        stale = sorted(self.linked_profiles - self.profile_files)
        self.assertEqual(
            stale,
            [],
            "profile索引に実体のないprofile JSON linkがある:\n"
            + "\n".join(stale),
        )

    def test_profile_json_links_resolve_from_their_own_document(self) -> None:
        unresolved = sorted(
            f"{source.relative_to(REPO_ROOT).as_posix()} -> {target}"
            for source, target in self.profile_links
            if not (source.parent / target).is_file()
        )
        self.assertEqual(
            unresolved,
            [],
            "記述元からの相対pathで解決できないprofile JSON linkがある:\n"
            + "\n".join(unresolved),
        )

    def test_readme_links_every_profile_index_shard(self) -> None:
        missing = sorted(self.index_files - self.linked_index_files)
        stale = sorted(self.linked_index_files - self.index_files)
        self.assertEqual(
            missing,
            [],
            "evaluations/profiles/README.md から辿れないindex shard:\n"
            + "\n".join(missing),
        )
        self.assertEqual(
            stale,
            [],
            "evaluations/profiles/README.md に実体のないindex shard linkがある:\n"
            + "\n".join(stale),
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from generate_profile_index import (  # noqa: E402
    DEFAULT_PROFILES_DIR,
    ProfileIndex,
    ProfileIndexError,
)

README_TEMPLATE = """# profile index

## 全profile index

説明文。

- [`001–060`](index/profiles-001-060.md)

## 次の節

本文。
"""


def build_profiles_dir(root: Path, count: int) -> Path:
    profiles = root / "profiles"
    profiles.mkdir()
    for number in range(1, count + 1):
        (profiles / f"profile-{number:03d}.json").write_text("{}\n", encoding="utf-8")
    (profiles / "README.md").write_text(README_TEMPLATE, encoding="utf-8")
    return profiles


class GenerateProfileIndexTest(unittest.TestCase):
    def test_repository_index_matches_generator_output(self) -> None:
        report = ProfileIndex(DEFAULT_PROFILES_DIR).report()
        self.assertTrue(
            report["current"],
            "evaluations/profiles/ の索引が generate_profile_index.py の出力と一致しない: "
            f"{report}",
        )

    def test_write_creates_shards_and_readme_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profiles = build_profiles_dir(Path(tmp), 61)
            index = ProfileIndex(profiles)
            index.write()

            shards = sorted(path.name for path in (profiles / "index").glob("*.md"))
            self.assertEqual(shards, ["profiles-001-060.md", "profiles-061-061.md"])
            readme = (profiles / "README.md").read_text(encoding="utf-8")
            self.assertIn("- [`001–060`](index/profiles-001-060.md)", readme)
            self.assertIn("- [`061–061`](index/profiles-061-061.md)", readme)
            self.assertIn("## 次の節", readme)

            first = (profiles / "index" / "profiles-001-060.md").read_text(encoding="utf-8")
            self.assertIn("- [`profile-001.json`](../profile-001.json)", first)
            self.assertNotIn("profile-061.json", first)

    def test_write_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profiles = build_profiles_dir(Path(tmp), 61)
            ProfileIndex(profiles).write()
            second = ProfileIndex(profiles)
            self.assertEqual(second.write(), [])
            self.assertTrue(second.report()["current"])

    def test_added_profile_renames_tail_shard_and_removes_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profiles = build_profiles_dir(Path(tmp), 61)
            ProfileIndex(profiles).write()

            (profiles / "profile-062.json").write_text("{}\n", encoding="utf-8")
            index = ProfileIndex(profiles)
            self.assertFalse(index.report()["current"])
            changed = index.write()

            self.assertIn("removed:profiles-061-061.md", changed)
            shards = sorted(path.name for path in (profiles / "index").glob("*.md"))
            self.assertEqual(shards, ["profiles-001-060.md", "profiles-061-062.md"])
            readme = (profiles / "README.md").read_text(encoding="utf-8")
            self.assertIn("- [`061–062`](index/profiles-061-062.md)", readme)
            self.assertNotIn("profiles-061-061.md", readme)

    def test_report_flags_outdated_shard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profiles = build_profiles_dir(Path(tmp), 5)
            ProfileIndex(profiles).write()
            shard = profiles / "index" / "profiles-001-005.md"
            shard.write_text(shard.read_text(encoding="utf-8").replace("../", ""), "utf-8")

            report = ProfileIndex(profiles).report()
            self.assertFalse(report["current"])
            self.assertEqual(report["outdated_shards"], ["profiles-001-005.md"])

    def test_empty_profiles_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profiles = build_profiles_dir(Path(tmp), 1)
            (profiles / "profile-001.json").unlink()
            with self.assertRaises(ProfileIndexError):
                ProfileIndex(profiles)

    def test_readme_without_link_block_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profiles = build_profiles_dir(Path(tmp), 3)
            (profiles / "README.md").write_text("# profile index\n\n本文だけ。\n", encoding="utf-8")
            with self.assertRaises(ProfileIndexError):
                ProfileIndex(profiles)


if __name__ == "__main__":
    unittest.main()

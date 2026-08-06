from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = REPO_ROOT / "evaluations" / "profiles"
PROFILE_README = PROFILES_DIR / "README.md"
PROFILE_LINK_RE = re.compile(r"\]\(([^)]+\.json)(?:#[^)]+)?\)")


class ProfileIndexCoverageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_files = {
            path.name for path in PROFILES_DIR.glob("*.json") if path.is_file()
        }
        readme = PROFILE_README.read_text(encoding="utf-8")
        self.linked_profiles = {
            Path(target).name for target in PROFILE_LINK_RE.findall(readme)
        }

    def test_all_profile_json_files_are_linked_from_readme(self) -> None:
        missing = sorted(self.profile_files - self.linked_profiles)
        self.assertEqual(
            missing,
            [],
            "evaluations/profiles/README.md から直接linkされていないprofile JSON:\n"
            + "\n".join(missing),
        )

    def test_profile_json_links_in_readme_are_not_stale(self) -> None:
        stale = sorted(self.linked_profiles - self.profile_files)
        self.assertEqual(
            stale,
            [],
            "evaluations/profiles/README.md に実体のないprofile JSON linkがある:\n"
            + "\n".join(stale),
        )


if __name__ == "__main__":
    unittest.main()

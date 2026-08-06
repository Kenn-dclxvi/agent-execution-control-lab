"""case-data.jsonが持つdigestの形式回帰。

`raw_sha256`は`prepare_case_fixture.py`がsource blobの実contentと照合する
fixture identityであり、桁落ちした値はfixtureをmaterializeできなくする。
同一pathに対して異なるdigestが記録されると、caseごとにfixture identityが
食い違う。両方をcase revision全体で検査する。
"""

from __future__ import annotations

import json
import re
import unittest
from collections import defaultdict
from pathlib import Path

CASES_ROOT = Path(__file__).resolve().parents[1] / "evaluations" / "cases"
SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
SHA1 = re.compile(r"\A[0-9a-f]{40}\Z")


def iter_case_data() -> list[Path]:
    return sorted(CASES_ROOT.glob("**/private/case-data.json"))


def iter_entries(node: object):
    """`path`と`raw_sha256`を持つobjectを再帰的に返す。"""
    if isinstance(node, dict):
        if "raw_sha256" in node and "path" in node:
            yield node
        for value in node.values():
            yield from iter_entries(value)
    elif isinstance(node, list):
        for value in node:
            yield from iter_entries(value)


class CaseDataDigestFormatTest(unittest.TestCase):
    def setUp(self) -> None:
        self.case_files = iter_case_data()
        self.assertTrue(self.case_files, "case-data.jsonが見つからない")

    def test_raw_sha256_is_full_length_lowercase_hex(self) -> None:
        for case_file in self.case_files:
            data = json.loads(case_file.read_text(encoding="utf-8"))
            for entry in iter_entries(data):
                with self.subTest(case=str(case_file), path=entry["path"]):
                    digest = entry["raw_sha256"]
                    self.assertRegex(
                        digest,
                        SHA256,
                        f"raw_sha256が64桁のlowercase hexでない（{len(digest)}桁）",
                    )

    def test_git_blob_sha1_is_full_length_lowercase_hex(self) -> None:
        for case_file in self.case_files:
            data = json.loads(case_file.read_text(encoding="utf-8"))
            for entry in iter_entries(data):
                blob = entry.get("git_blob_sha1")
                if blob is None:
                    continue
                with self.subTest(case=str(case_file), path=entry["path"]):
                    self.assertRegex(blob, SHA1)

    def test_same_blob_has_one_raw_sha256(self) -> None:
        """同一のgit blobへ異なるraw_sha256を記録しない。"""
        by_blob: dict[str, set[str]] = defaultdict(set)
        sources: dict[str, set[str]] = defaultdict(set)
        for case_file in self.case_files:
            data = json.loads(case_file.read_text(encoding="utf-8"))
            for entry in iter_entries(data):
                blob = entry.get("git_blob_sha1")
                if blob is None:
                    continue
                by_blob[blob].add(entry["raw_sha256"])
                sources[blob].add(str(case_file.relative_to(CASES_ROOT)))
        for blob, digests in sorted(by_blob.items()):
            with self.subTest(git_blob_sha1=blob):
                self.assertEqual(
                    len(digests),
                    1,
                    f"同一blobへ複数のraw_sha256: {sorted(digests)} in {sorted(sources[blob])}",
                )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import collections
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_MAP = REPO_ROOT / "docs" / "execution-control-measurement-report-evidence-map.md"
CLAIM_ROW = re.compile(r"^\| (R\d+-\w+) \|", re.MULTILINE)


class EvidenceMapClaimIdTest(unittest.TestCase):
    """Claim IDはevidence mapの追跡単位であり、一意でなければならない。"""

    def setUp(self) -> None:
        self.text = EVIDENCE_MAP.read_text(encoding="utf-8")
        self.ids = CLAIM_ROW.findall(self.text)

    def test_claim_ids_are_unique(self) -> None:
        duplicates = {i: n for i, n in collections.Counter(self.ids).items() if n > 1}
        self.assertEqual(duplicates, {}, f"duplicate Claim IDs: {duplicates}")

    def test_claim_rows_exist(self) -> None:
        self.assertGreater(len(self.ids), 50)


if __name__ == "__main__":
    unittest.main()

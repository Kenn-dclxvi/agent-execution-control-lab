from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SET = ROOT / "evaluations/targets/click/sets/click-f02-only-r1/README.md"
INDEX = ROOT / "evaluations/targets/click/sets/README.md"


class ClickF02OnlySetTest(unittest.TestCase):
    def test_set_is_fixed_and_indexed(self) -> None:
        text = SET.read_text(encoding="utf-8")
        self.assertIn("`click-f02-only-r1`", text)
        self.assertIn("CLICK-F02-STREAM-DEPRECATION-CONTRACT", text)
        self.assertIn("Case=1、`N=3`、`B=1`、`M=24`", text)
        self.assertIn("標準setではない", text)
        self.assertIn("click-f02-only-r1", INDEX.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

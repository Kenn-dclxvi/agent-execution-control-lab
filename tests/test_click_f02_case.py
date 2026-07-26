from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "evaluations/targets/click/cases/CLICK-F02-STREAM-DEPRECATION-CONTRACT/r1"
DATA = CASE / "private/case-data.json"
TRIAL = CASE / "trial-prompt-input.json"
SEED = CASE / "private/seed.patch"
DESCRIPTOR = ROOT / "evaluations/targets/click/target.json"


class ClickF02CaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_identity_and_family(self) -> None:
        self.assertEqual(self.data["case_id"], "CLICK-F02-STREAM-DEPRECATION-CONTRACT")
        self.assertEqual(self.data["case_revision"], "r1")
        self.assertEqual(self.data["fixture"]["case_spec"]["family"], "F02")

    def test_artifact_hashes_match(self) -> None:
        self.assertEqual(
            hashlib.sha256(SEED.read_bytes()).hexdigest(),
            self.data["seed"]["artifact"]["raw_sha256"],
        )
        self.assertEqual(
            hashlib.sha256(TRIAL.read_bytes()).hexdigest(),
            self.data["qualification"]["receipt"]["trial_prompt_input_raw_sha256"],
        )

    def test_target_identity_matches_descriptor(self) -> None:
        descriptor = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
        target = self.data["fixture"]["target_identity"]
        primary = descriptor["target_repository"]["primary_ref"]
        self.assertEqual(target["commit"], primary["commit"])
        self.assertEqual(target["tree"], primary["tree"])

    def test_cross_module_paths_and_gates_are_fixed(self) -> None:
        preimages = self.data["seed"]["application_contract"]["preimage_files"]
        self.assertEqual(
            {item["path"] for item in preimages},
            {"src/click/__init__.py", "src/click/utils.py"},
        )
        commands = self.data["grader"]["commands"]
        self.assertIn("tests/test_deprecations.py tests/test_testing.py", commands[0])
        self.assertEqual(commands[1], "PYTHONPATH=src .venv/bin/python -m pytest -q")

    def test_trial_preserves_visibility_and_scope(self) -> None:
        trial = json.loads(TRIAL.read_text(encoding="utf-8"))
        self.assertIn("src/click/__init__.py", trial["target_artifacts_allowed_paths_and_forbidden_changes"])
        self.assertIn("src/click/utils.py", trial["target_artifacts_allowed_paths_and_forbidden_changes"])
        self.assertNotIn("051725", TRIAL.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

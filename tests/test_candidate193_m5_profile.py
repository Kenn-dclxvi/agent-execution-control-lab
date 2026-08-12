from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "evaluations/profiles/candidate191-explicit-review-operation-applicability-adr9-r2-medium-m24-n5-cli0146.json"
CANDIDATE = ROOT / "evaluations/profiles/candidate193-frontier-bound-dispatch-transition-adr9-r2-medium-m24-n5-cli0146.json"
DESIGN = ROOT / "docs/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-evaluation-design.md"
PREPARATION = ROOT / "docs/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-execution-preparation-audit.md"


class Candidate193M5ProfileTest(unittest.TestCase):
    def test_profile_changes_only_prompt_identity_and_explanatory_metadata(self) -> None:
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))

        self.assertEqual([item["id"] for item in candidate["cases"]], [f"TC-ADR{i:02d}" for i in range(1, 10)])
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-frontier-bound-dispatch-transition-r1",
                "revision": "r1",
                "bundle_sha256": "a392acd88a127cd297e9d714cf19a4f35c5de8b08aaa21513b6a936e380c9bb8",
            },
        )

        left = copy.deepcopy(baseline)
        right = copy.deepcopy(candidate)
        for profile in (left, right):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
            profile["scope"].pop("preflight_revision_note")
        self.assertEqual(left, right)

    def test_reader_indexes_and_preflight_boundary_are_fixed(self) -> None:
        docs_index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        profile_index = (ROOT / "evaluations/profiles/README.md").read_text(encoding="utf-8")
        profile_shards = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "evaluations/profiles/index").glob("*.md")
        )
        preparation = PREPARATION.read_text(encoding="utf-8")

        self.assertIn(DESIGN.name, docs_index)
        self.assertIn(PREPARATION.name, docs_index)
        self.assertIn(CANDIDATE.name, profile_index + profile_shards)
        self.assertIn("authorized_45 / issued_0", preparation)
        self.assertIn("e599690689294c658b52a6a9e301697f", preparation)
        self.assertIn("3f93d5724b2e091de3eba5c1980557130256aaf76ec4301f279b0f9c5a58c7c3", preparation)


if __name__ == "__main__":
    unittest.main()

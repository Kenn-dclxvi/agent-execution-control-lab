from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "evaluations/profiles/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-reference-n5-medium-m24-cli0146.json"
CUMULATIVE = ROOT / "evaluations/profiles/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-medium-m24-cli0146.json"
DESIGN = ROOT / "docs/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-evaluation-design.md"
PREPARATION = ROOT / "docs/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-execution-preparation-audit.md"


class Candidate191M6ProfileTest(unittest.TestCase):
    def test_m6_profiles_change_only_cumulative_iteration_coverage(self) -> None:
        reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
        cumulative = json.loads(CUMULATIVE.read_text(encoding="utf-8"))

        self.assertEqual([item["id"] for item in reference["cases"]], ["TC-ADR05", "TC-ADR07", "TC-ADR09"])
        self.assertEqual([item["id"] for item in cumulative["cases"]], ["TC-ADR05", "TC-ADR07", "TC-ADR09"])
        self.assertEqual(reference["iterations"], 5)
        self.assertEqual(cumulative["iterations"], 20)
        self.assertEqual(reference["prompt_set_identity"], cumulative["prompt_set_identity"])
        self.assertEqual(reference["execution"]["max_workers"], 24)
        self.assertEqual(cumulative["execution"]["max_workers"], 24)

        left = copy.deepcopy(reference["comparison_conditions"])
        right = copy.deepcopy(cumulative["comparison_conditions"])
        left["repetition_condition"]["iterations"] = 20
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
        self.assertIn(REFERENCE.name, profile_index + profile_shards)
        self.assertIn(CUMULATIVE.name, profile_index + profile_shards)
        self.assertIn("authorized_45 / issued_0", preparation)
        self.assertIn("68735a7e985fb87ca8bd85a4e898f748377ff87e841924a9ae3b447efd0a7cbf", preparation)


if __name__ == "__main__":
    unittest.main()

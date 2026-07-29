from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C94 = ROOT / "prompts/candidates/the-caption-3ce91a4-operation-criterion-totality-r1"
C95 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-judgment-owner-boundary-r1"
DESIGN = ROOT / "docs/candidate95-required-judgment-owner-boundary-design.md"
C94_PROFILE = ROOT / "evaluations/profiles/candidate94-operation-criterion-totality-v14-reasoning-medium-a02-global-m5-n5-cli0146-r1.json"
C81_A02_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-a02-global-m5-n5-cli0146-r1.json"
C95_PROFILE = ROOT / "evaluations/profiles/candidate95-required-judgment-owner-boundary-v14-reasoning-medium-a02-global-m5-n5-cli0146-r1.json"
C81_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2.json"
C95_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate95-required-judgment-owner-boundary-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
TARGETED_RESULT = ROOT / "evaluations/results/candidate95-required-judgment-owner-boundary-v14-medium-a02-n5-cli0146_2026-07-30.md"
STANDARD14_RESULT = ROOT / "evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-n5-cli0146_2026-07-30.md"
A02_B20_RESULT = ROOT / "evaluations/results/candidate95-required-judgment-owner-boundary-v14-medium-a02-continuous-n5-b20-cli0146_2026-07-30.md"
A02_B20_COMPARISON = ROOT / "evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-a02-continuous-n5-b20-cli0146_2026-07-30.md"
STANDARD14_B20_COMPARISON = ROOT / "evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ")
    }


class Candidate95Test(unittest.TestCase):
    def test_is_direct_child_with_one_changed_target(self) -> None:
        source = verify_bundle(C94)
        candidate = verify_bundle(C95)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_required_judgment_owner_boundary(self) -> None:
        source = rules(C94 / "files/AGENTS.md.txt")
        candidate = rules(C95 / "files/AGENTS.md.txt")
        self.assertEqual(set(source), set(candidate))
        self.assertEqual(
            {label for label in source if source[label] != candidate[label]},
            {"SPEC"},
        )
        for label in set(source) - {"SPEC"}:
            self.assertEqual(candidate[label], source[label])

        spec = candidate["SPEC"]
        self.assertIn("non-machine judgment resultがrequiredなcriterionだけ", spec)
        self.assertIn("non-machine riskの記載有無にかかわらず", spec)
        self.assertIn("criterion owner=none", spec)
        self.assertIn("judgment authorityを直接指定する一意なrepository authority", spec)

    def test_manifest_and_design_remain_draft(self) -> None:
        manifest = json.loads((C95 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "draft")
        self.assertEqual(manifest["provenance"]["runtime_projection_status"], "not_projected")

        design = DESIGN.read_text(encoding="utf-8")
        for text in (
            "candidate number: Candidate95",
            "evaluation status: `not_evaluated`",
            "release: `not_created`",
            "runtime projection: `not_projected`",
        ):
            self.assertIn(text, design)

    def test_a02_profiles_change_only_prompt_identity(self) -> None:
        source = json.loads(C94_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C95_PROFILE.read_text(encoding="utf-8"))
        for key in (
            "cases",
            "comparison_conditions",
            "evaluation_set",
            "execution",
            "scope",
        ):
            self.assertEqual(source[key], candidate[key])
        self.assertEqual(
            candidate["cases"],
            [{"id": "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING", "revision": "r2"}],
        )
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "8c845f18bd6ed86d6f2f19281ba1257f0f1a213fa1c3466c76ede402451ee190",
                "name": "the-caption-3ce91a4-required-judgment-owner-boundary-r1",
                "revision": "r1",
            },
        )

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C81_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C95_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        for key in (
            "cases",
            "comparison_conditions",
            "evaluation_set",
            "execution",
            "scope",
        ):
            self.assertEqual(source[key], candidate[key])
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "8c845f18bd6ed86d6f2f19281ba1257f0f1a213fa1c3466c76ede402451ee190",
                "name": "the-caption-3ce91a4-required-judgment-owner-boundary-r1",
                "revision": "r1",
            },
        )

    def test_matched_c81_a02_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C81_A02_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C95_PROFILE.read_text(encoding="utf-8"))
        for key in (
            "cases",
            "comparison_conditions",
            "evaluation_set",
            "execution",
            "scope",
        ):
            self.assertEqual(source[key], candidate[key])
        self.assertEqual(
            source["prompt_set_identity"],
            {
                "bundle_sha256": "919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220",
                "name": "the-caption-3ce91a4-validation-wrapper-precedence-r1",
                "revision": "r1",
            },
        )

    def test_targeted_result_records_gate_pass(self) -> None:
        result = TARGETED_RESULT.read_text(encoding="utf-8")
        for text in (
            "5 / 5件がvalid・rateable・score `4`",
            "owner clarification: 0件",
            "targeted_a02_evaluated / quality_gate_passed / route_gate_passed",
            "8ac03547d69e45e785160b32df533069",
        ):
            self.assertIn(text, result)

    def test_standard14_result_records_quality_and_cost_boundaries(self) -> None:
        result = STANDARD14_RESULT.read_text(encoding="utf-8")
        for text in (
            "70 / 70件がvalid・rateable・score `4`",
            "aggregate_cost_both_higher / adoption_not_decided",
            "648b4dec10ba4ce191f76be1ee184bf9",
            "c5bfcd6dcc52b99e7a3dabda966dcb00640e4eeed8c969753992545c87a8490c",
            "+52,902`（`+2.62%`）",
            "+66.952`秒（`+7.30%`）",
        ):
            self.assertIn(text, result)

    def test_a02_b20_result_records_stability_and_scope_boundaries(self) -> None:
        result = A02_B20_RESULT.read_text(encoding="utf-8")
        for text in (
            "20 / 20 batch、100 / 100件をvalid・rateable",
            "公式scoreは100 / 100件が`4`",
            "excluded attempt / 再試行: `0 / 0`",
            "root-only `100 / 100`",
            "route_stability_gate_passed",
            "標準14全体のB20ではない",
            "7c3640522ee749eebebe7e7fc20e45ab",
            "69739dc8814542efa2cf084c71d01c71",
            "e5740fe6edb0efabde9aaab3ccb624d31984ddeaa6fc32076a82266b313b9833",
        ):
            self.assertIn(text, result)

    def test_a02_b20_comparison_records_significance_trigger(self) -> None:
        result = A02_B20_COMPARISON.read_text(encoding="utf-8")
        for text in (
            "両者とも100 / 100件がvalid・rateable・score `4`",
            "-3,917.5`（`-1.72%`）",
            "-5.367秒`（`-6.50%`）",
            "補正後`p=0.008442`",
            "標準14 B20へ進んだ",
        ):
            self.assertIn(text, result)

    def test_standard14_b20_comparison_records_stop_boundary(self) -> None:
        result = STANDARD14_B20_COMPARISON.read_text(encoding="utf-8")
        for text in (
            "score `4 / 2 / 1 = 1,398 / 1 / 1`",
            "+90,356`（`+4.49%`）",
            "+52.701秒`（`+5.53%`）",
            "quality_gate_failed / route_stability_gate_failed / cost_both_significantly_higher / stopped",
            "1d1e209856e04482b1c37d00f68b0913",
            "6c4c78d0c055447e8602e962f010a3d0",
            "c5bfcd6dcc52b99e7a3dabda966dcb00640e4eeed8c969753992545c87a8490c",
        ):
            self.assertIn(text, result)


if __name__ == "__main__":
    unittest.main()

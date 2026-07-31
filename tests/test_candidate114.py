from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C108 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-ticket-terminal-closure-r1"
C114 = ROOT / "prompts/candidates/the-caption-3ce91a4-spec-ready-evidence-phase-boundary-r1"
DESIGN = ROOT / "docs/candidate114-spec-ready-evidence-phase-boundary-design.md"
C108_PROFILE = ROOT / "evaluations/profiles/candidate108-validation-ticket-terminal-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
C114_PROFILE = ROOT / "evaluations/profiles/candidate114-spec-ready-evidence-phase-boundary-v14-reasoning-medium-a01-a02-f01-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate114Test(unittest.TestCase):
    def test_is_direct_c108_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C108)
        candidate = verify_bundle(C114)
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

    def test_replaces_only_evidence_gate_with_existing_spec_ready_phase(self) -> None:
        source = rules(C108 / "files/AGENTS.md.txt")
        candidate = rules(C114 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "EVIDENCE_GATE"},
            {key: source[key] for key in source if key != "EVIDENCE_GATE"},
        )
        rule = candidate["EVIDENCE_GATE"]
        self.assertIn("`spec_ready=false`", rule)
        self.assertIn("`spec_ready=true`になった後だけ", rule)
        self.assertIn("clarification result", rule)
        self.assertLess(rule.index("`spec_ready=false`"), rule.index("target artifact"))
        for forbidden in ("authority_delegated", "A01", "A02", "pytest", "tool call", "Executor"):
            self.assertNotIn(forbidden, rule)

    def test_manifest_and_design_bind_one_axis(self) -> None:
        manifest = verify_bundle(C114)
        self.assertEqual(
            manifest["bundle_sha256"],
            "c6cd2756a8a1a5b192ed6eb5f17dc380bd884873c23c3f190d9974fc09c757dd",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate108を直接親", design)
        self.assertIn("spec_ready=false", design)
        self.assertIn("M=24", design)

    def test_targeted_profile_preserves_conditions_and_selects_three_cases(self) -> None:
        source = json.loads(C108_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C114_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(
            candidate["cases"],
            [
                {"id": "TC-A01-LATENT-MODE-POLICY", "revision": "r2"},
                {"id": "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING", "revision": "r2"},
                {"id": "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY", "revision": "r3"},
            ],
        )
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], verify_bundle(C114)["bundle_sha256"])
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C108 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-ticket-terminal-closure-r1"
C116 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-implementation-boundary-r1"
PROFILE = ROOT / "evaluations/profiles/candidate116-outcome-implementation-boundary-v14-reasoning-medium-a01-a02-f01-global-m24-n5-cli0146-r1.json"
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate116-outcome-implementation-boundary-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate116Test(unittest.TestCase):
    def test_is_direct_c108_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C108)
        candidate = verify_bundle(C116)
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": source["prompt_identity"],
        })
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_spec_and_evidence_gate_as_one_axis(self) -> None:
        source = rules(C108 / "files/AGENTS.md.txt")
        candidate = rules(C116 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key not in {"SPEC", "EVIDENCE_GATE"}},
            {key: source[key] for key in source if key not in {"SPEC", "EVIDENCE_GATE"}},
        )
        self.assertIn("利用者に観測可能な成果", candidate["SPEC"])
        self.assertIn("implementation choice", candidate["SPEC"])
        self.assertIn("`spec_ready=false`", candidate["EVIDENCE_GATE"])
        self.assertIn("`spec_ready=true`の後", candidate["EVIDENCE_GATE"])
        self.assertIn("未固定のrequired outcome valueを事後に補完しない", candidate["EVIDENCE_GATE"])
        for term in ("A01", "A02", "run.sh", "pytest", "authority_delegated", "Executor"):
            self.assertNotIn(term, candidate["SPEC"] + candidate["EVIDENCE_GATE"])

    def test_profile_is_a01_a02_f01_n5_m24(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual([case["id"] for case in profile["cases"]], [
            "TC-A01-LATENT-MODE-POLICY",
            "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING",
            "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
        ])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], verify_bundle(C116)["bundle_sha256"])

    def test_standard14_profile_is_n5_m24(self) -> None:
        profile = json.loads(STANDARD14_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(profile["cases"]), 14)
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], verify_bundle(C116)["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()

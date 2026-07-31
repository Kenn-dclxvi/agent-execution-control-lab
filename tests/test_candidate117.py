from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C116 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-implementation-boundary-r1"
C117 = ROOT / "prompts/candidates/the-caption-3ce91a4-implementation-authority-delegation-r1"
PROFILE = ROOT / "evaluations/profiles/candidate117-implementation-authority-delegation-v14-reasoning-medium-a01-a02-f01-global-m24-n5-cli0146-r1.json"
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate117-implementation-authority-delegation-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate117Test(unittest.TestCase):
    def test_is_direct_c116_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C116)
        candidate = verify_bundle(C117)
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": source["prompt_identity"],
        })
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_evidence_gate(self) -> None:
        source = rules(C116 / "files/AGENTS.md.txt")
        candidate = rules(C117 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "EVIDENCE_GATE"},
            {key: source[key] for key in source if key != "EVIDENCE_GATE"},
        )
        evidence_gate = candidate["EVIDENCE_GATE"]
        self.assertIn("implementation_authority_delegated", evidence_gate)
        self.assertIn("TaskSpecが未解決のimplementation choice", evidence_gate)
        self.assertIn("一般的なread permission", evidence_gate)
        self.assertIn("未固定のrequired outcome valueを事後に補完しない", evidence_gate)
        for term in ("A01", "A02", "run.sh", "pytest", "token", "Executor"):
            self.assertNotIn(term, evidence_gate)

    def test_profile_is_a01_a02_f01_n5_m24(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual([case["id"] for case in profile["cases"]], [
            "TC-A01-LATENT-MODE-POLICY",
            "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING",
            "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
        ])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], verify_bundle(C117)["bundle_sha256"])

    def test_standard14_profile_extends_targeted_profile_without_changing_conditions(self) -> None:
        targeted = json.loads(PROFILE.read_text(encoding="utf-8"))
        standard14 = json.loads(STANDARD14_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(standard14["cases"]), 14)
        self.assertEqual(standard14["cases"][:3], targeted["cases"])
        self.assertEqual(standard14["comparison_conditions"], targeted["comparison_conditions"])
        self.assertEqual(standard14["iterations"], 5)
        self.assertEqual(standard14["execution"]["max_workers"], 24)
        self.assertEqual(standard14["prompt_set_identity"], targeted["prompt_set_identity"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C122 = ROOT / "prompts/candidates/the-caption-3ce91a4-prechange-evidence-wave-closure-r1"
C123 = ROOT / "prompts/candidates/the-caption-3ce91a4-preterminal-result-round-closure-r1"
DESIGN = ROOT / "docs/candidate123-preterminal-result-round-closure-design.md"
C122_PROFILE = ROOT / "evaluations/profiles/candidate122-prechange-evidence-wave-closure-v14-reasoning-medium-a01-a02-f01-f02-global-m24-n5-cli0146-r1.json"
C123_PROFILE = ROOT / "evaluations/profiles/candidate123-preterminal-result-round-closure-v14-reasoning-medium-a01-a02-f01-f02-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate123Test(unittest.TestCase):
    def test_is_direct_c122_child(self) -> None:
        source = verify_bundle(C122)
        candidate = verify_bundle(C123)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        self.assertNotEqual(candidate["bundle_sha256"], source["bundle_sha256"])
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_preterminal_result_round_axis(self) -> None:
        source = rules(C122 / "files/AGENTS.md.txt")
        candidate = rules(C123 / "files/AGENTS.md.txt")
        changed = {key for key in source if source[key] != candidate[key]}
        self.assertEqual(changed, {"EVIDENCE_GATE"})
        gate = candidate["EVIDENCE_GATE"]
        for term in (
            "clarification_terminal_ready",
            "prechange_evidence_wave_ready",
            "prechange_result_round_ready",
            "一つのcustom exec wrapper",
            "後続evidenceを発行せず",
            "完了済みresultをmodelへ一度だけ返す",
            "shell compound commandへ結合せず",
        ):
            self.assertIn(term, gate)
        self.assertIn("同じmodel step", gate)
        self.assertNotIn("一つのinvocationで取得", gate)
        for key in ("VALIDATION_CLOSURE", "VALIDATION_PLAN", "METHOD"):
            self.assertEqual(candidate[key], source[key])
        for case_term in ("A01", "A02", "F01", "F02", "run.sh", "pytest"):
            self.assertNotIn(case_term, gate)

    def test_manifest_design_and_profile(self) -> None:
        manifest = verify_bundle(C123)
        self.assertEqual(
            manifest["bundle_sha256"],
            "9547acd587c5a00979089055d8edd37825009763d77d19429cf5a097c40f7115",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate122を直接親", design)
        self.assertIn("制御は一つに限定しない", design)
        self.assertIn("A02 token中央値: Candidate107の`125,559`以下", design)

        source = json.loads(C122_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C123_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()

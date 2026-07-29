from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs/candidate87-adoption-decision.md"
DESIGN = ROOT / "docs/candidate87-producer-local-invocation-wave-design.md"
RESULT = ROOT / "evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md"
BACKLOG = ROOT / "docs/research-backlog.md"


class Candidate87AdoptionDecisionTest(unittest.TestCase):
    def test_separates_evaluation_from_adoption_and_projection(self) -> None:
        decision = DECISION.read_text(encoding="utf-8")
        self.assertIn("standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher", decision)
        self.assertIn("`not_adopted`", decision)
        self.assertIn("`stopped`", decision)
        self.assertIn("`not_created`", decision)
        self.assertIn("`not_authorized`", decision)
        self.assertIn("Candidate81のまま", decision)
        self.assertIn("当時の`adoption_not_decided`を変更しない", decision)

    def test_records_evidence_and_restart_boundary(self) -> None:
        decision = DECISION.read_text(encoding="utf-8")
        self.assertIn("70 / 70件でscore `4`", decision)
        self.assertIn("`+117,040`（`+6.09%`）", decision)
        self.assertIn("`+12.330`秒（`+1.35%`）", decision)
        self.assertIn("70 / 70件root-only", decision)
        self.assertIn("65 / 70件root-only", decision)
        self.assertIn("Candidate82からCandidate89まで", decision)
        self.assertIn("freshなCandidate81互換trace", decision)
        self.assertIn("別のterminal resultまたは別のproducer identity", decision)

    def test_keeps_primary_result_immutable_and_links_followup_state(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        design = DESIGN.read_text(encoding="utf-8")
        backlog = BACKLOG.read_text(encoding="utf-8")
        self.assertIn(
            "standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided",
            result,
        )
        self.assertIn("[`採用判断`](candidate87-adoption-decision.md)", design)
        self.assertIn("`standard14_evaluated / not_adopted / stopped`", backlog)
        self.assertIn("Candidate82〜Candidate89のサブエージェント制御系列を完了・停止", backlog)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-decision-record-totality-r1"


class Candidate186Test(unittest.TestCase):
    def test_direct_child_adds_only_review_decision_record_totality(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(
            candidate["provenance"]["design_inputs"][:2],
            [
                "docs/review-decision-record-totality-design.md",
                "docs/review-decision-record-totality-adversarial-review-r13.md",
            ],
        )
        self.assertIn(
            "a660d50f36d1d83c7cd1b3d6ea79a9b313fc7c10a103fca66084e91b1fb570e8",
            candidate["provenance"]["source_interpretation"],
        )

        parent_text = (PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        labels = (
            "REVIEW_DECISION_RECORD",
            "SUBJECT_EFFECT_CORRESPONDENCE",
            "OPEN_CLASS_CORRESPONDENCE",
            "REVIEW_ADMISSION_INPUT",
            "REVIEW_INPUT_CLASSIFICATION",
            "REVIEW_TERMINAL_EFFECT",
        )
        additions = {
            line
            for line in candidate_text.splitlines(keepends=True)
            if any(line.startswith(f"- {label}:") for label in labels)
        }
        self.assertEqual(len(additions), 6)
        self.assertEqual(
            "".join(line for line in candidate_text.splitlines(keepends=True) if line not in additions),
            parent_text,
        )

        for required in (
            "subject_effect_partition := (finite_effect_graph_or_empty, open_class_effect_components)",
            "partition_coverage := complete | incomplete | unbound",
            "precondition_state := present(precondition_binding) | absent",
            "他方へ伝播させず",
            "constraint_dependency_binding := (constraint_identity,bound_value,dependency_identity_set,evaluation_stage_binding)",
            "inter_component_order_or_dependency_edges",
            "dependent class predicateが許す全instance組合せ",
            "implementation producer、admission producer、review judgement producerは相互に異なるexecution identity",
            "review_input_domain_receipt := (permission_basis_identity,allowed_input_source_basis_set,complete_input_identity_set,coverage_predicate_identity,coverage_result_dependency)",
            "review_input_state := value(identity,value) | missing(identity) | unreadable(identity) | terminal_failure(identity,result)",
            "input_effect_class_record := (input_identity,review_input_state,class,classification_predicate_identity,classification_result_dependency)",
            "counterexample_support | outcome_sensitive | irrelevant",
            "packet_support_atom_set := {TaskSpec binding,subject binding,authority binding,implementation choice binding,保持constraint binding,(input_identity,review_input_state)}",
            "missing_counterexample_field_identity",
            "形成不能classification",
            "不完全recordはnonterminalのまま保持",
            "対応subjectを含む未発行artifact変更だけを停止",
            "評価case、fixture、oracle、rating、過去finding、旧Candidate、期待terminal、修正案および会話履歴",
        ):
            self.assertIn(required, candidate_text)

        for excluded_label in (
            "COEMISSION_JUDGEMENT",
            "JUDGEMENT_EFFECT",
            "REVIEW_EVIDENCE_INTERFACE",
        ):
            self.assertNotIn(f"- {excluded_label}:", candidate_text)


if __name__ == "__main__":
    unittest.main()

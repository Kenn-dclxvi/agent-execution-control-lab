from __future__ import annotations
import json, unittest
from pathlib import Path
from scripts.export_prompt_bundle import verify_bundle

ROOT=Path(__file__).resolve().parents[1]
C81=ROOT/'prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1'
C93=ROOT/'prompts/candidates/the-caption-3ce91a4-result-classification-r1'
B=ROOT/'evaluations/profiles/candidate81-planning-first-producer-selection-v14-reasoning-medium-f02-global-m5-n5-r1.json'
P=ROOT/'evaluations/profiles/candidate93-result-classification-v14-reasoning-medium-f02-global-m5-n5-r1.json'
R=ROOT/'evaluations/results/candidate81-candidate93-result-classification-v14-medium-f02-n5_2026-07-29.md'

class Candidate93Test(unittest.TestCase):
    def test_bundle_and_rule(self):
        source=verify_bundle(C81);candidate=verify_bundle(C93)
        self.assertEqual(candidate['content_relation']['source_prompt_identity'],source['prompt_identity'])
        rule=next(x for x in (C93/'files/AGENTS.md.txt').read_text().splitlines() if x.startswith('- OUTPUT_INGRESS:'))
        for value in ('EXACT','STRUCTURED','NOISE','output_route=temporary_file'): self.assertIn(value,rule)
    def test_profile_fixed(self):
        baseline=json.loads(B.read_text());candidate=json.loads(P.read_text())
        for key in ('cases','comparison_conditions','evaluation_set','execution','scope'): self.assertEqual(baseline[key],candidate[key])
    def test_result_stops_on_missing_mechanism(self):
        result=R.read_text();self.assertIn('classification mechanism gate: `failed`（0 / 5）',result);self.assertIn('improved_but_unattributed',result)

if __name__=='__main__': unittest.main()

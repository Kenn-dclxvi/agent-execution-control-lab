"""確認事項なしの表現を品質失敗へ混ぜない局所回帰確認。"""
import importlib.util
from pathlib import Path
import tempfile
import unittest

s=importlib.util.spec_from_file_location('fixture_r4',Path(__file__).with_name('fixture_tool_r4.py'))
f=importlib.util.module_from_spec(s);s.loader.exec_module(f)


class QuestionRepresentationTests(unittest.TestCase):
    def test_absence_representations_are_equivalent(self):
        with tempfile.TemporaryDirectory() as temp:
            w=Path(temp)/'work';f.prepare('CRC-12',w);report,evidence=f.reference_state('CRC-12',w)
            for question in [None, [], '', {}]:
                with self.subTest(question=question):
                    report['question']=question;f.write_value(w/'result.json',report)
                    self.assertEqual(f.grade('CRC-12',w,evidence)['quality_score'],4)
            report.pop('question');f.write_value(w/'result.json',report)
            self.assertEqual(f.grade('CRC-12',w,evidence)['quality_score'],4)

    def test_required_question_cannot_be_empty(self):
        with tempfile.TemporaryDirectory() as temp:
            w=Path(temp)/'work';f.prepare('CRC-05',w);report,evidence=f.reference_state('CRC-05',w)
            report['question']=[];f.write_value(w/'result.json',report)
            self.assertEqual(f.grade('CRC-05',w,evidence)['quality_score'],0)


if __name__=='__main__':
    unittest.main()

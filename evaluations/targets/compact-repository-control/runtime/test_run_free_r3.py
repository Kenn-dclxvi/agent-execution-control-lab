"""正しい補足説明、保存形式、検証実行を誤拒否しない回帰確認。"""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('compact_free_runner_r3', Path(__file__).with_name('run_free_r3.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
f = runner.fixture


class EvidenceTests(unittest.TestCase):
    def collect(self, command, output, code=0):
        event = {'type':'item.completed','item':{'type':'command_execution','command':command,
                 'exit_code':code,'aggregated_output':output}}
        return runner.validation_evidence([event], {'session_count':1})['validation_execution']

    def test_direct_verification(self):
        self.assertTrue(self.collect('python3 verify.py', '{"sha256":"abc","passed":true}'))

    def test_checked_subprocess_with_nested_output(self):
        command="python3 - <<'PY'\nimport subprocess\nsubprocess.run(['python3', 'verify.py'], capture_output=True, check=True)\nPY"
        self.assertTrue(self.collect(command, '{"validation": {"sha256":"abc","passed":true}}'))

    def test_string_literal_is_not_execution(self):
        command="python3 - <<'PY'\ns='subprocess.run([python3, verify.py], check=True)'\nPY"
        self.assertFalse(self.collect(command, '{"sha256":"abc","passed":true}'))

    def test_failed_verification(self):
        self.assertFalse(self.collect('python3 verify.py', '{"sha256":"abc","passed":true}', 1))

    def test_unrelated_echo(self):
        self.assertFalse(self.collect('echo output', '{"sha256":"abc","passed":true}'))

    def test_unchecked_subprocess_is_not_proof(self):
        command="python3 - <<'PY'\nimport subprocess\nsubprocess.run(['python3', 'verify.py'])\nPY"
        self.assertFalse(self.collect(command, '{"sha256":"abc","passed":true}'))


class OutcomeTests(unittest.TestCase):
    def test_finding_explanation_is_allowed(self):
        expected=[{'path':'monthly.json','field':'month'}]
        self.assertTrue(f.report_value_satisfies([{'path':'monthly.json','field':'month','message':'形式違反'}], expected))

    def test_extra_finding_is_rejected(self):
        self.assertFalse(f.report_value_satisfies([{'path':'a'}, {'path':'b'}], [{'path':'a'}]))

    def test_unspecified_option_order_is_allowed(self):
        self.assertTrue(f.report_value_satisfies(['千円','円'], ['円','千円']))

    def test_scalar_projection_preserves_requested_value(self):
        with tempfile.TemporaryDirectory() as temp:
            w=Path(temp)/'work';f.prepare('CRC-18',w);_,evidence=f.reference_state('CRC-18',w)
            f.write_value(w/'projection.json', '"ready"\n')
            self.assertEqual(f.grade('CRC-18',w,evidence)['quality_score'],4)
            f.write_value(w/'projection.json', '{"public":"ready","internal":"INTERNAL_CRC18_7f32"}\n')
            self.assertEqual(f.grade('CRC-18',w,evidence)['quality_score'],0)


if __name__ == '__main__':
    unittest.main()

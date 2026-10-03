"""実行由来の検証証拠だけを採用する収集器の回帰確認。"""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('compact_free_runner', Path(__file__).with_name('run_free_r2.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class ValidationEvidenceTests(unittest.TestCase):
    def event(self, command='python3 verify.py', code=0, output='{"sha256":"abc","passed":true}\n'):
        return {'type':'item.completed','item':{'type':'command_execution', 'command':command,
                'exit_code':code,'aggregated_output':output}}

    def evidence(self, *events):
        return runner.validation_evidence(list(events), {'session_count':1})['validation_execution']

    def test_completed_verification_is_collected(self):
        self.assertEqual(self.evidence(self.event())[0]['result'], {'sha256':'abc','passed':True})

    def test_no_command_is_not_execution(self):
        self.assertEqual(self.evidence(), [])

    def test_failed_command_does_not_prove_success(self):
        self.assertEqual(self.evidence(self.event(code=1)), [])

    def test_unrelated_echo_does_not_prove_verification(self):
        self.assertEqual(self.evidence(self.event(command='echo result')), [])

    def test_non_json_output_is_not_fabricated(self):
        self.assertEqual(self.evidence(self.event(output='success')), [])


if __name__ == '__main__':
    unittest.main()

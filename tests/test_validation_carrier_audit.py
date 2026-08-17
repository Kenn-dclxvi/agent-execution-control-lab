from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validation_carrier_audit import audit_rollout


GROUPS = [["pytest", "tests/unit/test_one.py"], ["bash", "verify.sh"]]
ROOT = Path(__file__).resolve().parents[1]
SAVED_AUDIT = (
    ROOT
    / "evaluations/results/"
    "candidate147-candidate270-validation-carrier-rollout-reassessment-r1.json"
)


def record(kind: str, payload: dict[str, object]) -> str:
    return json.dumps({"type": kind, "payload": payload})


class ValidationCarrierAuditTest(unittest.TestCase):
    def write_rollout(self, root: Path, response_items: list[dict[str, object]]) -> Path:
        path = root / "rollout.jsonl"
        lines = [
            record(
                "session_meta",
                {"id": "thread-1", "cwd": "/tmp/evidence/0123456789abcdef0123456789abcdef/workspace"},
            )
        ]
        lines.extend(record("response_item", item) for item in response_items)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def test_passes_one_terminal_outer_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = self.write_rollout(
                Path(tmp),
                [
                    {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "validation",
                        "input": (
                            'await tools.exec_command({cmd:"pytest tests/unit/test_one.py"});'
                            'await tools.exec_command({cmd:"bash verify.sh"});'
                        ),
                    },
                    {
                        "type": "custom_tool_call_output",
                        "call_id": "validation",
                        "output": "Script completed\nOutput:\nall passed",
                    },
                    {"type": "message", "role": "assistant", "content": []},
                ],
            )
            result = audit_rollout(rollout, GROUPS)
            self.assertTrue(result["observable"])
            self.assertTrue(result["mechanism_passed"])
            self.assertEqual(result["outer_call_id"], "validation")
            self.assertEqual(result["outer_call_output_count"], 1)

    def test_rejects_validation_split_across_outer_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = self.write_rollout(
                Path(tmp),
                [
                    {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "focused",
                        "input": 'await tools.exec_command({cmd:"pytest tests/unit/test_one.py"})',
                    },
                    {
                        "type": "custom_tool_call_output",
                        "call_id": "focused",
                        "output": "Script completed",
                    },
                    {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "full",
                        "input": 'await tools.exec_command({cmd:"bash verify.sh"})',
                    },
                    {
                        "type": "custom_tool_call_output",
                        "call_id": "full",
                        "output": "Script completed",
                    },
                ],
            )
            result = audit_rollout(rollout, GROUPS)
            self.assertFalse(result["single_outer_call_passed"])
            self.assertFalse(result["mechanism_passed"])

    def test_rejects_nonterminal_outer_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = self.write_rollout(
                Path(tmp),
                [
                    {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "validation",
                        "input": (
                            'await tools.exec_command({cmd:"pytest tests/unit/test_one.py"});'
                            'await tools.exec_command({cmd:"bash verify.sh"});'
                        ),
                    },
                    {
                        "type": "custom_tool_call_output",
                        "call_id": "validation",
                        "output": "Script running with cell ID 42",
                    },
                ],
            )
            result = audit_rollout(rollout, GROUPS)
            self.assertTrue(result["observable"])
            self.assertFalse(result["single_terminal_output_passed"])
            self.assertFalse(result["mechanism_passed"])

    def test_passes_wait_only_continuation_to_terminal_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = self.write_rollout(
                Path(tmp),
                [
                    {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "validation",
                        "input": (
                            'await tools.exec_command({cmd:"pytest tests/unit/test_one.py"});'
                            'await tools.exec_command({cmd:"bash verify.sh"});'
                        ),
                    },
                    {
                        "type": "custom_tool_call_output",
                        "call_id": "validation",
                        "output": "Script running with cell ID 42\nOutput:\n",
                    },
                    {"type": "reasoning", "summary": []},
                    {
                        "type": "function_call",
                        "name": "wait",
                        "call_id": "wait-1",
                        "arguments": json.dumps({"cell_id": "42"}),
                    },
                    {
                        "type": "function_call_output",
                        "call_id": "wait-1",
                        "output": "Script completed\nOutput:\nall passed",
                    },
                    {"type": "message", "role": "assistant", "content": []},
                ],
            )
            result = audit_rollout(rollout, GROUPS)
            self.assertTrue(result["mechanism_passed"])
            self.assertEqual(result["continuation_wait_call_ids"], ["wait-1"])
            self.assertEqual(result["nonterminal_receipt_count"], 1)
            self.assertEqual(result["intermediate_validation_output_bytes"], 0)
            self.assertEqual(result["terminal_output_call_id"], "wait-1")

    def test_rejects_validation_output_in_nonterminal_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = self.write_rollout(
                Path(tmp),
                [
                    {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "validation",
                        "input": (
                            'await tools.exec_command({cmd:"pytest tests/unit/test_one.py"});'
                            'await tools.exec_command({cmd:"bash verify.sh"});'
                        ),
                    },
                    {
                        "type": "custom_tool_call_output",
                        "call_id": "validation",
                        "output": "Script running with cell ID 42\nOutput:\nfocused passed",
                    },
                    {
                        "type": "function_call",
                        "name": "wait",
                        "call_id": "wait-1",
                        "arguments": json.dumps({"cell_id": "42"}),
                    },
                    {
                        "type": "function_call_output",
                        "call_id": "wait-1",
                        "output": "Script completed\nOutput:\nall passed",
                    },
                ],
            )
            result = audit_rollout(rollout, GROUPS)
            self.assertGreater(result["intermediate_validation_output_bytes"], 0)
            self.assertFalse(result["single_terminal_output_passed"])
            self.assertFalse(result["mechanism_passed"])

    def test_rejects_model_item_between_call_and_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = self.write_rollout(
                Path(tmp),
                [
                    {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "validation",
                        "input": (
                            'await tools.exec_command({cmd:"pytest tests/unit/test_one.py"});'
                            'await tools.exec_command({cmd:"bash verify.sh"});'
                        ),
                    },
                    {"type": "message", "role": "assistant", "content": []},
                    {
                        "type": "custom_tool_call_output",
                        "call_id": "validation",
                        "output": "Script completed",
                    },
                ],
            )
            result = audit_rollout(rollout, GROUPS)
            self.assertFalse(result["no_interposed_model_item_passed"])
            self.assertFalse(result["mechanism_passed"])

    def test_saved_c147_c270_reassessment_binds_outer_carrier(self) -> None:
        artifact = json.loads(SAVED_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(
            artifact["schema_version"],
            "the-caption-prompt.validation-carrier-audit/v1",
        )
        self.assertEqual(artifact["scope"]["new_evaluation_runs"], 0)
        sources = {source["label"]: source for source in artifact["sources"]}
        self.assertEqual(sources["candidate147"]["mechanism_state"], "failed")
        self.assertEqual(sources["candidate147"]["passed_run_count"], 12)
        self.assertEqual(sources["candidate147"]["failed_run_count"], 3)
        self.assertEqual(
            sum(
                run["intermediate_validation_output_bytes"]
                for run in sources["candidate147"]["runs"]
            ),
            76012,
        )
        self.assertEqual(sources["candidate270"]["mechanism_state"], "passed")
        self.assertEqual(sources["candidate270"]["passed_run_count"], 15)
        self.assertEqual(sources["candidate270"]["failed_run_count"], 0)
        self.assertTrue(
            all(
                run["single_outer_call_passed"]
                and run["no_interposed_model_item_passed"]
                and run["intermediate_validation_output_bytes"] == 0
                for run in sources["candidate270"]["runs"]
            )
        )


if __name__ == "__main__":
    unittest.main()

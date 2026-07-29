from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.observation_delivery_audit import audit


class ObservationDeliveryAuditTest(unittest.TestCase):
    def write_rollout(self, path: Path, payloads: list[dict[str, object]]) -> None:
        events = [
            {"type": "response_item", "payload": payload} for payload in payloads
        ]
        events.append({"type": "event_msg", "payload": {"type": "token_count"}})
        path.write_text(
            "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
        )

    def test_passes_when_only_outer_code_results_reenter_the_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = Path(tmp) / "rollout.jsonl"
            self.write_rollout(
                rollout,
                [
                    {"type": "custom_tool_call", "name": "exec", "call_id": "one"},
                    {
                        "type": "custom_tool_call_output",
                        "call_id": "one",
                        "output": [{"type": "input_text", "text": "receipt"}],
                    },
                ],
            )

            result = audit(rollout)

            self.assertTrue(result["mechanism_passed"])
            self.assertEqual(result["model_reentries_from_tool_results"], 1)
            self.assertEqual(result["model_steps"], 1)
            self.assertGreater(result["model_visible_result_bytes"], 0)

    def test_fails_when_a_direct_tool_result_is_model_visible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = Path(tmp) / "rollout.jsonl"
            self.write_rollout(
                rollout,
                [
                    {"type": "custom_tool_call", "name": "exec", "call_id": "one"},
                    {"type": "custom_tool_call_output", "call_id": "one", "output": []},
                    {
                        "type": "function_call",
                        "name": "exec_command",
                        "call_id": "direct",
                    },
                    {
                        "type": "function_call_output",
                        "call_id": "direct",
                        "output": "raw result",
                    },
                ],
            )

            result = audit(rollout)

            self.assertFalse(result["mechanism_passed"])
            self.assertEqual(result["direct_calls"][0]["name"], "exec_command")
            self.assertEqual(result["model_reentries_from_tool_results"], 2)

    def test_fails_without_a_completed_outer_code_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = Path(tmp) / "rollout.jsonl"
            self.write_rollout(
                rollout,
                [{"type": "custom_tool_call", "name": "exec", "call_id": "one"}],
            )

            self.assertFalse(audit(rollout)["mechanism_passed"])


if __name__ == "__main__":
    unittest.main()

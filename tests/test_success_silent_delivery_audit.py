from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.success_silent_delivery_audit import audit


GROUPS = [["pytest", "tests/unit/test_one.py"], ["bash", "verify.sh"]]


def event(payload: dict[str, object]) -> str:
    return json.dumps({"type": "response_item", "payload": payload})


class SuccessSilentDeliveryAuditTest(unittest.TestCase):
    def write_rollout(self, root: Path, lines: list[str]) -> Path:
        path = root / "rollout.jsonl"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def test_passes_one_small_validation_receipt_and_two_statuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = self.write_rollout(
                Path(tmp),
                [
                    event({"type": "message", "role": "assistant", "content": [{"text": "start"}]}),
                    event({"type": "message", "role": "assistant", "content": [{"text": "still running"}]}),
                    event({
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "v1",
                        "input": "await pytest tests/unit/test_one.py; await bash verify.sh",
                    }),
                    event({
                        "type": "custom_tool_call_output",
                        "call_id": "v1",
                        "output": [{"command": "pytest tests/unit/test_one.py", "exit_code": 0}, {"command": "bash verify.sh", "exit_code": 0}],
                    }),
                    event({"type": "message", "role": "assistant", "content": [{"text": "done"}]}),
                ],
            )
            result = audit(rollout, GROUPS)
            self.assertTrue(result["mechanism_passed"])
            self.assertEqual(result["validation_wave_call_count"], 1)
            self.assertEqual(result["intermediate_message_count"], 2)

    def test_rejects_raw_success_log_and_excess_status_messages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rollout = self.write_rollout(
                Path(tmp),
                [
                    event({"type": "message", "role": "assistant", "content": [{"text": str(i)}]})
                    for i in range(4)
                ]
                + [
                    event({
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "v1",
                        "input": "pytest tests/unit/test_one.py; bash verify.sh",
                    }),
                    event({
                        "type": "custom_tool_call_output",
                        "call_id": "v1",
                        "output": "============================= test session starts",
                    }),
                    event({"type": "message", "role": "assistant", "content": [{"text": "done"}]}),
                ],
            )
            result = audit(rollout, GROUPS)
            self.assertFalse(result["mechanism_passed"])
            self.assertFalse(result["validation_success_silent_passed"])
            self.assertFalse(result["status_suppression_passed"])

    def test_v2_requires_exact_hashed_local_raw_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rollout = self.write_rollout(
                root,
                [
                    event({"type": "message", "role": "assistant", "content": [{"text": "start"}]}),
                    event({
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "v1",
                        "input": (
                            "await tools.exec_command({cmd:'python3 /repo/scripts/"
                            "success_silent_command.py -- pytest tests/unit/test_one.py'})"
                        ),
                    }),
                    event({
                        "type": "custom_tool_call_output",
                        "call_id": "v1",
                        "output": [{"command": ["pytest", "tests/unit/test_one.py"], "exit_code": 0}],
                    }),
                    event({"type": "message", "role": "assistant", "content": [{"text": "done"}]}),
                ],
            )
            evidence = root / "evidence"
            evidence.mkdir()
            stdout = b"raw test output\n"
            stderr = b""
            evidence_id = "one"
            (evidence / f"{evidence_id}.stdout.bin").write_bytes(stdout)
            (evidence / f"{evidence_id}.stderr.bin").write_bytes(stderr)
            (evidence / f"{evidence_id}.json").write_text(
                json.dumps({
                    "evidence_id": evidence_id,
                    "argv": ["pytest", "tests/unit/test_one.py"],
                    "exit_code": 0,
                    "stdout_bytes": len(stdout),
                    "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
                    "stderr_bytes": len(stderr),
                    "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
                }),
                encoding="utf-8",
            )

            result = audit(
                rollout,
                GROUPS,
                [{"argv": ["pytest", "tests/unit/test_one.py"]}],
                evidence,
            )

            self.assertTrue(result["mechanism_passed"])
            self.assertTrue(result["local_raw_evidence"]["passed"])
            self.assertEqual(result["local_raw_evidence"]["observed_count"], 1)

            (evidence / f"{evidence_id}.stdout.bin").write_bytes(b"changed")
            changed = audit(
                rollout,
                GROUPS,
                [{"argv": ["pytest", "tests/unit/test_one.py"]}],
                evidence,
            )
            self.assertFalse(changed["mechanism_passed"])
            self.assertIn(
                "stdout_sha256_mismatch:one",
                changed["local_raw_evidence"]["failures"],
            )

    def test_v2_does_not_match_pytest_profile_path_and_ordinary_test_reads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            argv = [".venv/bin/python", "-m", "pytest", "tests/", "-v"]
            rollout = self.write_rollout(
                root,
                [
                    event({
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "read",
                        "input": (
                            "await tools.exec_command({cmd:\"sed tests/file.py\","
                            "workdir:\"/tmp/pytest-allowlist-run\"})"
                        ),
                    }),
                    event({
                        "type": "custom_tool_call_output",
                        "call_id": "read",
                        "output": "large ordinary read",
                    }),
                    event({
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "validation",
                        "input": (
                            "await tools.exec_command({cmd:\"python3 /repo/scripts/"
                            "success_silent_command.py -- .venv/bin/python -m pytest "
                            "tests/ -v\"})"
                        ),
                    }),
                    event({
                        "type": "custom_tool_call_output",
                        "call_id": "validation",
                        "output": {"exit_code": 0},
                    }),
                    event({"type": "message", "role": "assistant", "content": [{"text": "done"}]}),
                ],
            )
            evidence = root / "evidence"
            evidence.mkdir()
            stdout = b"raw\n"
            stderr = b""
            (evidence / "one.stdout.bin").write_bytes(stdout)
            (evidence / "one.stderr.bin").write_bytes(stderr)
            (evidence / "one.json").write_text(
                json.dumps({
                    "evidence_id": "one",
                    "argv": argv,
                    "exit_code": 0,
                    "stdout_bytes": len(stdout),
                    "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
                    "stderr_bytes": len(stderr),
                    "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
                }),
                encoding="utf-8",
            )

            result = audit(rollout, [["pytest", "tests/"]], [{"argv": argv}], evidence)

            self.assertTrue(result["mechanism_passed"])
            self.assertEqual(result["validation_wave_call_count"], 1)
            self.assertLess(result["validation_model_visible_bytes"], 4096)

if __name__ == "__main__":
    unittest.main()

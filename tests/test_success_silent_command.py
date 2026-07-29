from __future__ import annotations

import hashlib
import json
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.success_silent_command import POLICY_SCHEMA_VERSION


ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts/success_silent_command.py"


class SuccessSilentCommandTest(unittest.TestCase):
    def write_policy(
        self,
        root: Path,
        workspace: Path,
        commands: list[dict[str, object]],
    ) -> Path:
        path = root / "policy.json"
        path.write_text(
            json.dumps(
                {
                    "schema_version": POLICY_SCHEMA_VERSION,
                    "workspace": str(workspace),
                    "commands": commands,
                }
            ),
            encoding="utf-8",
        )
        return path

    def invoke(
        self,
        workspace: Path,
        policy: Path,
        evidence: Path,
        command: list[str],
    ) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            [
                sys.executable,
                str(WRAPPER),
                "--policy",
                str(policy),
                "--evidence-dir",
                str(evidence),
                "--",
                *command,
            ],
            cwd=workspace,
            capture_output=True,
            check=False,
        )

    def test_success_returns_receipt_and_keeps_raw_bytes_local(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            evidence = root / "evidence"
            command = [sys.executable, "-c", "print('RAW SUCCESS')"]
            policy = self.write_policy(root, workspace, [{"argv": command}])

            completed = self.invoke(workspace, policy, evidence, command)

            self.assertEqual(completed.returncode, 0)
            self.assertNotEqual(completed.stdout, b"RAW SUCCESS\n")
            receipt = json.loads(completed.stdout)
            self.assertEqual(receipt["command"], command)
            self.assertEqual(receipt["exit_code"], 0)
            self.assertEqual(len(list(evidence.glob("*.json"))), 1)
            self.assertEqual(
                next(evidence.glob("*.stdout.bin")).read_bytes(), b"RAW SUCCESS\n"
            )

    def test_failure_returns_original_stdout_stderr_and_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            evidence = root / "evidence"
            command = [
                sys.executable,
                "-c",
                "import sys; print('OUT'); print('ERR', file=sys.stderr); raise SystemExit(7)",
            ]
            policy = self.write_policy(root, workspace, [{"argv": command}])

            completed = self.invoke(workspace, policy, evidence, command)

            self.assertEqual(completed.returncode, 7)
            self.assertEqual(completed.stdout, b"OUT\n")
            self.assertEqual(completed.stderr, b"ERR\n")
            self.assertEqual(next(evidence.glob("*.stdout.bin")).read_bytes(), b"OUT\n")
            self.assertEqual(next(evidence.glob("*.stderr.bin")).read_bytes(), b"ERR\n")

    def test_signal_failure_returns_original_streams_and_signal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            evidence = root / "evidence"
            command = [
                sys.executable,
                "-c",
                (
                    "import os, signal, sys; "
                    "os.write(1, b'OUT\\n'); os.write(2, b'ERR\\n'); "
                    "os.kill(os.getpid(), signal.SIGTERM)"
                ),
            ]
            policy = self.write_policy(root, workspace, [{"argv": command}])

            completed = self.invoke(workspace, policy, evidence, command)

            self.assertEqual(completed.returncode, -signal.SIGTERM)
            self.assertEqual(completed.stdout, b"OUT\n")
            self.assertEqual(completed.stderr, b"ERR\n")
            metadata = json.loads(next(evidence.glob("*.json")).read_text())
            self.assertEqual(metadata["exit_code"], -signal.SIGTERM)

    def test_rejects_command_not_in_exact_argv_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            allowed = [sys.executable, "-c", "print('allowed')"]
            policy = self.write_policy(root, workspace, [{"argv": allowed}])

            completed = self.invoke(
                workspace,
                policy,
                root / "evidence",
                [sys.executable, "-c", "print('different')"],
            )

            self.assertEqual(completed.returncode, 64)
            self.assertIn(b"not allowlisted", completed.stderr)
            self.assertFalse((root / "evidence").exists())

    def test_rejects_pinned_wrapper_identity_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            script = workspace / "verify.sh"
            script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            command = ["sh", "verify.sh"]
            policy = self.write_policy(
                root,
                workspace,
                [
                    {
                        "argv": command,
                        "script_path": "verify.sh",
                        "script_sha256": hashlib.sha256(b"different").hexdigest(),
                    }
                ],
            )

            completed = self.invoke(workspace, policy, root / "evidence", command)

            self.assertEqual(completed.returncode, 64)
            self.assertIn(b"identity mismatch", completed.stderr)


if __name__ == "__main__":
    unittest.main()

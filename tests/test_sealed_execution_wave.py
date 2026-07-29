from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "sealed_execution_wave.py"
PLAN_SCHEMA = "the-caption-prompt.sealed-execution-wave-plan/v1"


class SealedExecutionWaveTest(unittest.TestCase):
    def write_plan(self, path: Path, operations: list[dict[str, object]]) -> None:
        path.write_text(
            json.dumps(
                {
                    "schema_version": PLAN_SCHEMA,
                    "wave_id": "test-wave",
                    "operations": operations,
                }
            ),
            encoding="utf-8",
        )

    def run_wave(
        self, plan: Path, workspace: Path, evidence: Path
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(CLI),
                "--plan",
                str(plan),
                "--workspace",
                str(workspace),
                "--evidence-directory",
                str(evidence),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_success_exposes_one_receipt_and_buffers_all_command_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            plan = root / "plan.json"
            evidence = root / "evidence"
            self.write_plan(
                plan,
                [
                    {
                        "id": "focused-test",
                        "argv": [sys.executable, "-c", "print('INTERMEDIATE_SECRET')"],
                    },
                    {
                        "id": "full-test",
                        "argv": [sys.executable, "-c", "print('TERMINAL_SECRET')"],
                    },
                ],
            )

            completed = self.run_wave(plan, workspace, evidence)

            self.assertEqual(completed.returncode, 0)
            self.assertEqual(completed.stderr, "")
            self.assertEqual(len(completed.stdout.splitlines()), 1)
            self.assertNotIn("INTERMEDIATE_SECRET", completed.stdout)
            self.assertNotIn("TERMINAL_SECRET", completed.stdout)
            receipt = json.loads(completed.stdout)
            self.assertEqual(receipt["wave_status"], "terminal")
            self.assertEqual(receipt["model_visibility"]["visible_receipt_count"], 1)
            self.assertEqual([item["status"] for item in receipt["operations"]], ["success", "success"])
            self.assertEqual(
                (evidence / "01-focused-test.stdout").read_text(encoding="utf-8"),
                "INTERMEDIATE_SECRET\n",
            )
            self.assertEqual(
                (evidence / "02-full-test.stdout").read_text(encoding="utf-8"),
                "TERMINAL_SECRET\n",
            )
            self.assertEqual(
                json.loads((evidence / "receipt.json").read_text(encoding="utf-8"))["plan_sha256"],
                receipt["plan_sha256"],
            )

    def test_false_predicate_stops_later_operations_and_returns_bounded_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            marker = workspace / "must-not-exist"
            plan = root / "plan.json"
            evidence = root / "evidence"
            self.write_plan(
                plan,
                [
                    {"id": "setup", "argv": [sys.executable, "-c", "print('ok')"]},
                    {
                        "id": "failure",
                        "argv": [
                            sys.executable,
                            "-c",
                            "import sys; sys.stderr.write('X' * 5000); raise SystemExit(7)",
                        ],
                    },
                    {
                        "id": "after",
                        "argv": [
                            sys.executable,
                            "-c",
                            f"from pathlib import Path; Path({str(marker)!r}).touch()",
                        ],
                    },
                ],
            )

            completed = self.run_wave(plan, workspace, evidence)

            self.assertEqual(completed.returncode, 2)
            self.assertEqual(len(completed.stdout.splitlines()), 1)
            receipt = json.loads(completed.stdout)
            self.assertEqual(receipt["wave_status"], "predicate_false")
            self.assertEqual(receipt["reentry_reason"], "operation_predicate_false")
            self.assertEqual(receipt["not_run_operation_ids"], ["after"])
            failure = receipt["operations"][-1]
            self.assertEqual(failure["exit_code"], 7)
            self.assertEqual(failure["failure_excerpt"]["byte_limit"], 4096)
            self.assertTrue(failure["failure_excerpt"]["truncated"])
            self.assertFalse(marker.exists())

    def test_timeout_is_unknown_and_stops_the_wave(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            plan = root / "plan.json"
            evidence = root / "evidence"
            self.write_plan(
                plan,
                [
                    {
                        "id": "slow",
                        "argv": [
                            sys.executable,
                            "-c",
                            "import time; print('started', flush=True); time.sleep(10)",
                        ],
                        "timeout_seconds": 0.05,
                    },
                    {"id": "after", "argv": [sys.executable, "-c", "print('no')"]},
                ],
            )

            completed = self.run_wave(plan, workspace, evidence)

            self.assertEqual(completed.returncode, 3)
            receipt = json.loads(completed.stdout)
            self.assertEqual(receipt["wave_status"], "unknown")
            self.assertEqual(receipt["operations"][0]["unknown_detail"], "timeout")
            self.assertEqual(receipt["not_run_operation_ids"], ["after"])
            self.assertEqual(
                (evidence / "01-slow.stdout").read_text(encoding="utf-8"),
                "started\n",
            )

    def test_declared_nonzero_exit_code_can_satisfy_the_predicate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            plan = root / "plan.json"
            evidence = root / "evidence"
            self.write_plan(
                plan,
                [
                    {
                        "id": "expected-three",
                        "argv": [sys.executable, "-c", "raise SystemExit(3)"],
                        "expected_exit_codes": [3],
                    }
                ],
            )

            completed = self.run_wave(plan, workspace, evidence)

            self.assertEqual(completed.returncode, 0)
            receipt = json.loads(completed.stdout)
            self.assertEqual(receipt["operations"][0]["status"], "success")

    def test_plan_rejects_shell_string_and_duplicate_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            for name, operations in (
                ("shell", [{"id": "one", "argv": "echo hidden"}]),
                (
                    "duplicate",
                    [
                        {"id": "one", "argv": ["true"]},
                        {"id": "one", "argv": ["true"]},
                    ],
                ),
            ):
                with self.subTest(name=name):
                    plan = root / f"{name}.json"
                    evidence = root / f"{name}-evidence"
                    self.write_plan(plan, operations)
                    completed = self.run_wave(plan, workspace, evidence)
                    self.assertEqual(completed.returncode, 4)
                    self.assertEqual(len(completed.stdout.splitlines()), 1)
                    self.assertEqual(json.loads(completed.stdout)["wave_status"], "invalid_plan")
                    self.assertFalse(evidence.exists())

    def test_evidence_is_external_and_write_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            plan = root / "plan.json"
            self.write_plan(plan, [{"id": "one", "argv": [sys.executable, "-c", "pass"]}])

            internal = workspace / "evidence"
            rejected = self.run_wave(plan, workspace, internal)
            self.assertEqual(rejected.returncode, 4)
            self.assertFalse(internal.exists())

            evidence = root / "external-evidence"
            first = self.run_wave(plan, workspace, evidence)
            second = self.run_wave(plan, workspace, evidence)
            self.assertEqual(first.returncode, 0)
            self.assertEqual(second.returncode, 4)
            self.assertIn("already exists", json.loads(second.stdout)["error"])


if __name__ == "__main__":
    unittest.main()

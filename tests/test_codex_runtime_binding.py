from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.codex_runtime_binding import (
    CodexRuntimeBindingError,
    resolve_fixed_codex_runtime,
    verify_codex_runtime_binding,
    version_from_conditions,
)


class CodexRuntimeBindingTest(unittest.TestCase):
    def make_runtime(self, root: Path, version: str = "0.146.0") -> tuple[Path, Path, str]:
        executable = root / "runtime" / "bin" / "codex"
        executable.parent.mkdir(parents=True)
        executable.write_text(f"#!/bin/sh\necho 'codex-cli {version}'\n", encoding="utf-8")
        executable.chmod(0o755)
        digest = hashlib.sha256(executable.read_bytes()).hexdigest()
        manager = root / "codex-runtime"
        resolution = {
            "schema_version": "codex-eval-runtime-resolution/v1",
            "alias": "codex-0.146",
            "mutable": False,
            "runtime_id": "codex-cli-test-runtime",
            "resolved_path": str(executable.resolve()),
            "version_output": f"codex-cli {version}",
            "entrypoint_sha256": digest,
            "codesign_team_identifier": "2DC432GLL2",
        }
        manager.write_text(
            "#!/bin/sh\nprintf '%s\\n' " + repr(json.dumps(resolution)) + "\n",
            encoding="utf-8",
        )
        manager.chmod(0o755)
        return manager, executable, digest

    def test_resolves_and_verifies_fixed_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manager, executable, digest = self.make_runtime(Path(tmp))
            binding = resolve_fixed_codex_runtime("0.146.0", manager_path=manager)
            self.assertEqual(binding["executable"], str(executable.resolve()))
            self.assertEqual(binding["entrypoint_sha256"], digest)
            verify_codex_runtime_binding(binding)

    def test_rejects_entrypoint_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manager, executable, _ = self.make_runtime(Path(tmp))
            binding = resolve_fixed_codex_runtime("0.146.0", manager_path=manager)
            executable.write_text("#!/bin/sh\necho 'codex-cli 0.146.0 changed'\n", encoding="utf-8")
            executable.chmod(0o755)
            with self.assertRaisesRegex(CodexRuntimeBindingError, "drifted"):
                verify_codex_runtime_binding(binding)

    def test_reads_only_exact_profile_version(self) -> None:
        self.assertEqual(
            version_from_conditions({"agent_environment": {"codex_cli": "0.146.0"}}),
            "0.146.0",
        )
        self.assertIsNone(version_from_conditions({"agent_environment": "test-agent"}))
        with self.assertRaisesRegex(CodexRuntimeBindingError, "exact"):
            version_from_conditions({"agent_environment": {"codex_cli": "current"}})


if __name__ == "__main__":
    unittest.main()

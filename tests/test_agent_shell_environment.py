from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import agent_shell_environment as shell_env

BASE_PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def declared(**overrides: str) -> dict[str, str]:
    value = {
        "schema_version": shell_env.SHELL_ENVIRONMENT_SCHEMA_VERSION,
        "revision": shell_env.SHELL_ENVIRONMENT_REVISION,
        "base_path": BASE_PATH,
        "workspace_venv": ".venv",
        "venv_activation": shell_env.VENV_ACTIVATION,
        "user_startup_files": shell_env.USER_STARTUP_FILES,
    }
    value.update(overrides)
    return value


def make_fake_venv(workspace: Path) -> Path:
    venv_bin = workspace / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    for name in ("python", "python3", "pytest"):
        script = venv_bin / name
        script.write_text("#!/bin/sh\nexit 0\n")
        script.chmod(0o755)
    return workspace / ".venv"


class ConditionTests(unittest.TestCase):
    def test_conditions_without_declaration_keep_the_previous_behavior(self):
        self.assertIsNone(shell_env.shell_environment_from_conditions({"agent_environment": {}}))
        self.assertIsNone(shell_env.shell_environment_from_conditions({}))

    def test_declaration_is_returned_unchanged(self):
        conditions = {"agent_environment": {"shell_environment": declared()}}
        self.assertEqual(shell_env.shell_environment_from_conditions(conditions), declared())

    def test_rejects_unknown_revision_extra_fields_and_personal_paths(self):
        for value in (
            declared(revision="other"),
            {**declared(), "extra": "x"},
            declared(base_path="relative/bin:/usr/bin"),
            declared(base_path=f"{Path.home()}/.local/bin:/usr/bin"),
            declared(workspace_venv="/abs/.venv"),
            declared(workspace_venv="../.venv"),
        ):
            with self.subTest(value=value), self.assertRaises(shell_env.ShellEnvironmentError):
                shell_env.shell_environment_from_conditions(
                    {"agent_environment": {"shell_environment": value}}
                )


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.workspace = self.tmp / "workspace"
        self.venv = make_fake_venv(self.workspace)
        self.zdotdir = self.tmp / "zdotdir"
        self.zdotdir.mkdir()

    def test_environment_has_only_fixed_values_and_the_workspace_venv(self):
        personal = {
            "PATH": "/Users/someone/.local/bin:/personal/bin",
            "VIRTUAL_ENV": "/personal/venv",
            "PYTHONPATH": "/personal/lib",
            "ZDOTDIR": "/personal/zsh",
            "BASH_ENV": "/personal/bashrc",
            "SSH_AUTH_SOCK": "/personal/agent",
            "HOMEBREW_PREFIX": "/opt/homebrew",
            "USER": "tester",
        }
        with mock.patch.dict(os.environ, personal, clear=True):
            environment = shell_env.agent_environment(
                declared(),
                self.workspace,
                self.zdotdir,
                shell="/bin/zsh",
                passthrough={"CODEX_HOME": "/eval/codex-home"},
            )
        self.assertEqual(
            set(environment),
            {"HOME", "USER", "LOGNAME", "TMPDIR", "LANG", "CODEX_HOME", "SHELL", "PATH", "VIRTUAL_ENV", "ZDOTDIR"},
        )
        self.assertEqual(environment["PATH"], f"{self.venv}/bin:{BASE_PATH}")
        self.assertEqual(environment["VIRTUAL_ENV"], str(self.venv))
        self.assertEqual(environment["ZDOTDIR"], str(self.zdotdir))
        self.assertEqual(environment["SHELL"], "/bin/zsh")
        for value in environment.values():
            self.assertNotIn("/personal", value)

    def test_passthrough_cannot_override_shell_or_executable_resolution(self):
        for key in ("PATH", "VIRTUAL_ENV", "ZDOTDIR", "BASH_ENV", "ENV", "HOME", "SHELL", "PYTHONPATH"):
            with self.subTest(key=key), self.assertRaises(shell_env.ShellEnvironmentError):
                shell_env.agent_environment(
                    declared(), self.workspace, self.zdotdir, shell="/bin/zsh", passthrough={key: "/x"}
                )

    def test_missing_workspace_venv_is_rejected(self):
        shutil.rmtree(self.venv)
        with self.assertRaises(shell_env.ShellEnvironmentError):
            shell_env.agent_environment(
                declared(), self.workspace, self.zdotdir, shell="/bin/zsh", passthrough={}
            )


class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.workspace = self.tmp / "workspace"
        self.venv = make_fake_venv(self.workspace)
        self.home = self.tmp / "home"
        self.home.mkdir()
        startup = "personal_function() { :; }\nexport PATH=/personal/bin:$PATH\n"
        for name in (".zshenv", ".zprofile", ".zshrc", ".bashrc", ".bash_profile", ".profile"):
            (self.home / name).write_text(startup)
        self.zdotdir = self.tmp / "zdotdir"
        self.zdotdir.mkdir()

    def environment(self, shell: str, zdotdir: Path) -> dict[str, str]:
        return {
            "HOME": str(self.home),
            "LANG": "en_US.UTF-8",
            "SHELL": shell,
            "PATH": f"{self.venv}/bin:{BASE_PATH}",
            "VIRTUAL_ENV": str(self.venv),
            "ZDOTDIR": str(zdotdir),
        }

    def probe(self, shell: str, zdotdir: Path) -> dict:
        if not Path(shell).is_file():
            self.skipTest(f"{shell} is not available")
        return shell_env.probe_receipt(
            self.environment(shell, zdotdir),
            self.workspace,
            agent="test",
            shell=shell,
            agent_shell_arguments=["-c"],
        )

    def test_shells_resolve_the_workspace_venv_without_user_startup_files(self):
        for shell in ("/bin/zsh", "/bin/bash"):
            with self.subTest(shell=shell):
                receipt = self.probe(shell, self.zdotdir)
                self.assertTrue(receipt["ok"], receipt)
                self.assertFalse(receipt["user_startup_files_read"])
                self.assertEqual(receipt["observed"]["python3"], f"{self.venv}/bin/python3")
                self.assertEqual(receipt["passed_environment"]["PATH"], f"{self.venv}/bin:{BASE_PATH}")

    def test_zsh_startup_file_in_zdotdir_is_detected(self):
        receipt = self.probe("/bin/zsh", self.home)
        self.assertTrue(receipt["user_startup_files_read"])
        self.assertFalse(receipt["ok"])
        self.assertFalse(receipt["checks"]["path_unchanged_by_shell"])
        self.assertFalse(receipt["checks"]["no_shell_functions_loaded"])

    def test_receipt_is_write_once(self):
        path = self.tmp / "out" / "receipt.json"
        shell_env.write_receipt(path, {"ok": True})
        with self.assertRaises(FileExistsError):
            shell_env.write_receipt(path, {"ok": True})


if __name__ == "__main__":
    unittest.main()

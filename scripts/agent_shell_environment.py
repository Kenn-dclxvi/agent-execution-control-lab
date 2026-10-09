"""Fixed agent process environment that activates the workspace .venv.

The adapters hand the agent process an environment assembled only from fixed values,
the workspace ``.venv`` and the values the adapter itself needs, so the commands the
agent runs do not depend on the measuring user's shell startup files. See
docs/agent-runtime-venv-isolation-plan-r1.md.
"""

from __future__ import annotations

import json
import os
import pwd
import subprocess
import tempfile
from pathlib import Path
from typing import Any

SHELL_ENVIRONMENT_SCHEMA_VERSION = "the-caption-prompt.agent-shell-environment/v1"
SHELL_ENVIRONMENT_REVISION = "fixed-path-workspace-venv-r1"
SHELL_ENVIRONMENT_RECEIPT_SCHEMA_VERSION = "the-caption-prompt.agent-shell-environment-receipt/v1"
VENV_ACTIVATION = "path_prefix_and_virtual_env"
USER_STARTUP_FILES = "suppressed_by_empty_zdotdir_and_non_login_shell"
# Variables that would make a shell read a startup file or override the fixed values.
RESERVED_PROCESS_ENVIRONMENT_KEYS = frozenset(
    {"PATH", "VIRTUAL_ENV", "ZDOTDIR", "BASH_ENV", "ENV", "HOME", "PYTHONHOME", "PYTHONPATH"}
)
PROBE_SCRIPT = """\
if [ -n "${ZSH_VERSION-}" ]; then
  defined_functions=$(typeset +f | wc -l | tr -d ' ')
  if [[ -o login ]]; then login=yes; else login=no; fi
  if [[ -o interactive ]]; then interactive=yes; else interactive=no; fi
elif [ -n "${BASH_VERSION-}" ]; then
  defined_functions=$(declare -F | wc -l | tr -d ' ')
  if shopt -q login_shell; then login=yes; else login=no; fi
  case "$-" in *i*) interactive=yes ;; *) interactive=no ;; esac
else
  defined_functions=unknown; login=unknown; interactive=unknown
fi
printf 'shell_version=%s\\n' "${ZSH_VERSION:+zsh ${ZSH_VERSION}}${BASH_VERSION:+bash ${BASH_VERSION}}"
printf 'login=%s\\n' "$login"
printf 'interactive=%s\\n' "$interactive"
printf 'function_count=%s\\n' "$defined_functions"
printf 'alias_count=%s\\n' "$(alias | wc -l | tr -d ' ')"
printf 'PATH=%s\\n' "$PATH"
printf 'VIRTUAL_ENV=%s\\n' "${VIRTUAL_ENV-}"
printf 'python3=%s\\n' "$(command -v python3)"
printf 'python=%s\\n' "$(command -v python)"
printf 'pytest=%s\\n' "$(command -v pytest)"
printf 'python3_prefix=%s\\n' "$(python3 -c 'import sys; print(sys.prefix)' 2>/dev/null)"
if python3 -c 'import pytest' >/dev/null 2>&1; then printf 'python3_imports_pytest=yes\\n'; \
else printf 'python3_imports_pytest=no\\n'; fi
"""


class ShellEnvironmentError(Exception):
    pass


def shell_environment_from_conditions(conditions: dict[str, Any]) -> dict[str, Any] | None:
    """Return the declared shell environment, or None for conditions that predate it."""
    agent_environment = conditions.get("agent_environment")
    if not isinstance(agent_environment, dict) or "shell_environment" not in agent_environment:
        return None
    declared = agent_environment["shell_environment"]
    expected = {
        "schema_version": SHELL_ENVIRONMENT_SCHEMA_VERSION,
        "revision": SHELL_ENVIRONMENT_REVISION,
        "venv_activation": VENV_ACTIVATION,
        "user_startup_files": USER_STARTUP_FILES,
    }
    if not isinstance(declared, dict) or set(declared) != {*expected, "base_path", "workspace_venv"}:
        raise ShellEnvironmentError("agent_environment.shell_environment has unexpected fields")
    for key, value in expected.items():
        if declared.get(key) != value:
            raise ShellEnvironmentError(f"unsupported agent_environment.shell_environment.{key}")
    base_path = declared.get("base_path")
    if not isinstance(base_path, str) or not base_path:
        raise ShellEnvironmentError("shell_environment.base_path must be a non-empty string")
    for entry in base_path.split(":"):
        if not entry.startswith("/") or entry.startswith(str(Path.home())):
            raise ShellEnvironmentError("shell_environment.base_path must list absolute system paths")
    workspace_venv = declared.get("workspace_venv")
    if (
        not isinstance(workspace_venv, str)
        or not workspace_venv
        or workspace_venv.startswith("/")
        or ".." in Path(workspace_venv).parts
    ):
        raise ShellEnvironmentError("shell_environment.workspace_venv must be a workspace-relative path")
    return declared


def account_shell() -> str:
    """The login shell in the OS user record, which Codex uses regardless of SHELL."""
    return pwd.getpwuid(os.getuid()).pw_shell


def workspace_venv(declared: dict[str, Any], workspace: Path) -> Path:
    venv = (workspace / declared["workspace_venv"]).absolute()
    if not (venv / "bin" / "python").is_file():
        raise ShellEnvironmentError("workspace .venv has no bin/python; declare a runtime link for it")
    return venv


def agent_environment(
    declared: dict[str, Any],
    workspace: Path,
    zdotdir: Path,
    *,
    shell: str,
    passthrough: dict[str, str],
) -> dict[str, str]:
    """Build the agent process environment from fixed values only.

    ``passthrough`` carries the values the adapter itself must hand over (account
    identity, the agent's own configuration directory, adapter protocol paths). It may
    not override the values that decide which shell startup files and executables run.
    """
    reserved = RESERVED_PROCESS_ENVIRONMENT_KEYS.intersection(passthrough) | (
        {"SHELL"} & set(passthrough)
    )
    if reserved:
        raise ShellEnvironmentError(
            "process environment must not override " + ", ".join(sorted(reserved))
        )
    venv = workspace_venv(declared, workspace)
    environment = {
        "HOME": str(Path.home()),
        "USER": os.environ.get("USER", ""),
        "LOGNAME": os.environ.get("LOGNAME", os.environ.get("USER", "")),
        "TMPDIR": os.environ.get("TMPDIR", "/tmp"),
        "LANG": "en_US.UTF-8",
    }
    environment.update(passthrough)
    environment.update(
        {
            "SHELL": shell,
            "PATH": f"{venv / 'bin'}:{declared['base_path']}",
            "VIRTUAL_ENV": str(venv),
            "ZDOTDIR": str(zdotdir),
        }
    )
    return environment


def empty_zdotdir() -> tempfile.TemporaryDirectory[str]:
    """An empty directory for ZDOTDIR, so zsh finds no user startup files."""
    return tempfile.TemporaryDirectory(prefix="agent-empty-zdotdir-")


def parse_probe(output: str) -> dict[str, str]:
    observed: dict[str, str] = {}
    for line in output.splitlines():
        key, separator, value = line.partition("=")
        if separator:
            observed[key] = value
    return observed


def probe_receipt(
    environment: dict[str, str],
    workspace: Path,
    *,
    agent: str,
    shell: str,
    agent_shell_arguments: list[str],
) -> dict[str, Any]:
    """Run the agent's command shell the way the agent does and record what it resolved."""
    completed = subprocess.run(
        [shell, *agent_shell_arguments, PROBE_SCRIPT],
        cwd=workspace,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    observed = parse_probe(completed.stdout)
    zdotdir = Path(environment["ZDOTDIR"])
    venv_bin = str(Path(environment["VIRTUAL_ENV"]) / "bin")
    checks = {
        "probe_exit_code_zero": completed.returncode == 0,
        "path_unchanged_by_shell": observed.get("PATH") == environment["PATH"],
        "virtual_env_delivered": observed.get("VIRTUAL_ENV") == environment["VIRTUAL_ENV"],
        "no_shell_functions_loaded": observed.get("function_count") == "0",
        "non_login_non_interactive": observed.get("login") == "no"
        and observed.get("interactive") == "no",
        "zdotdir_empty": zdotdir.is_dir() and not any(zdotdir.iterdir()),
        "python3_in_workspace_venv": observed.get("python3") == f"{venv_bin}/python3",
        "python_in_workspace_venv": observed.get("python") == f"{venv_bin}/python",
        "pytest_in_workspace_venv": observed.get("pytest") == f"{venv_bin}/pytest",
        "python3_imports_pytest": observed.get("python3_imports_pytest") == "yes",
    }
    return {
        "schema_version": SHELL_ENVIRONMENT_RECEIPT_SCHEMA_VERSION,
        "revision": SHELL_ENVIRONMENT_REVISION,
        "agent": agent,
        "shell": shell,
        "shell_arguments": agent_shell_arguments,
        "passed_environment": {
            key: environment[key] for key in ("SHELL", "PATH", "VIRTUAL_ENV", "ZDOTDIR")
        },
        "passed_environment_keys": sorted(environment),
        "observed": observed,
        "checks": checks,
        "user_startup_files_read": not (
            checks["path_unchanged_by_shell"] and checks["no_shell_functions_loaded"]
        ),
        "ok": all(checks.values()),
        "probe_stderr": completed.stderr[-2000:],
    }


def write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")

"""Antigravity CLIと個人設定の識別値を発行前・実行直前に照合する。"""

import hashlib
from pathlib import Path
import subprocess


class AntigravityRuntimeError(ValueError):
    pass


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_from_conditions(conditions):
    runtime = conditions.get("agent_environment", {}).get("antigravity_cli")
    if runtime is None:
        return None
    executable = Path(runtime["executable"])
    if not executable.is_absolute() or executable.is_symlink() or not executable.is_file():
        raise AntigravityRuntimeError("CLIは絶対パスの通常ファイルで固定してください")
    if sha256(executable) != runtime["executable_sha256"]:
        raise AntigravityRuntimeError("CLIのSHA-256が変わっています")
    result = subprocess.run([str(executable), "--version"], capture_output=True, text=True)
    if result.returncode or result.stdout.strip() != runtime["version"] or runtime["version"] != "1.5.5":
        raise AntigravityRuntimeError("照合済みのCLI 1.5.5と一致しません")
    for name, expected in runtime["configuration_files"].items():
        path = Path(name)
        observed = sha256(path) if path.is_file() else None
        if observed != expected:
            raise AntigravityRuntimeError(f"固定した設定ファイルが変わっています: {name}")
    for name in runtime["absent_customizations"]:
        path = Path(name)
        if path.exists() and (not path.is_dir() or any(path.iterdir())):
            raise AntigravityRuntimeError(f"未固定の個人カスタマイズがあります: {name}")
    return runtime

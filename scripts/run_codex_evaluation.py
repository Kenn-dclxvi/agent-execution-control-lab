#!/usr/bin/env python3
"""Layer 2 adapter that overlays a prompt bundle and runs Codex."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from export_prompt_bundle import (
        BundleError,
        bundle_stored_path,
        storage_format_of,
        verify_bundle,
    )
    from all_agent_command_evidence import (
        AllAgentCommandEvidenceError,
        adapter_owned_cleanup_attempts,
        collect as collect_command_evidence,
        command_requirement_statuses,
        model_reported_adapter_owned_cleanup_attempts,
    )
    from all_agent_usage import (
        AllAgentUsageError,
        TOKEN_ACCOUNTING,
        collect_workspace_usage,
        parse_root_thread_id,
    )
except ModuleNotFoundError:  # Imported as scripts.run_codex_evaluation in tests.
    from scripts.export_prompt_bundle import (
        BundleError,
        bundle_stored_path,
        storage_format_of,
        verify_bundle,
    )
    from scripts.all_agent_command_evidence import (
        AllAgentCommandEvidenceError,
        adapter_owned_cleanup_attempts,
        collect as collect_command_evidence,
        command_requirement_statuses,
        model_reported_adapter_owned_cleanup_attempts,
    )
    from scripts.all_agent_usage import (
        AllAgentUsageError,
        TOKEN_ACCOUNTING,
        collect_workspace_usage,
        parse_root_thread_id,
    )


class AdapterError(Exception):
    pass


EXTERNAL_FAILURE_EXIT_CODE = 75
COLLAB_PARENT_THREAD_MISSING = "collab spawn failed: no thread with id:"
MODEL_AT_CAPACITY = "Selected model is at capacity."
BOUNDARY_EVIDENCE_SCHEMA_VERSION = "the-caption-prompt.boundary-evidence/v1"
BOUNDARY_EVIDENCE_BINDING_REVISION = "one-observation-one-predicate/v1"
BOUNDARY_EVIDENCE_SOURCE_POLICY = "adapter_managed_read_only_registry"
COMMAND_EVIDENCE_PROTOCOL = {
    "schema_version": "the-caption-prompt.command-evidence-protocol/v1",
    "mode": "separate_required_commands_with_structured_exit",
}
ORDERED_ROOT_WRAPPER_PROTOCOL = {
    "schema_version": "the-caption-prompt.command-evidence-protocol/v2",
    "mode": "ordered_root_wrapper_with_structured_exit",
}
SUPPORTED_COMMAND_EVIDENCE_PROTOCOLS = (
    COMMAND_EVIDENCE_PROTOCOL,
    ORDERED_ROOT_WRAPPER_PROTOCOL,
)
ADAPTER_TEARDOWN_PROTOCOL = {
    "schema_version": "the-caption-prompt.adapter-owned-teardown/v1",
    "failure_policy": "exclude_as_external_failure",
}
MODEL_VISIBLE_CAPABILITY_CATALOG_SCHEMA_VERSION = (
    "the-caption-prompt.model-visible-capability-catalog/v1"
)
MODEL_VISIBLE_CAPABILITY_TAGS = (
    "skills_instructions",
    "apps_instructions",
    "plugins_instructions",
)
BOUNDARY_OBSERVATION_SOURCES: dict[str, list[str]] = {
    "workspace.path": ["pwd", "-P"],
    "workspace.git.branch": ["git", "branch", "--show-current"],
    "workspace.git.head_commit": ["git", "rev-parse", "HEAD^{commit}"],
    "workspace.git.parent_commit": ["git", "rev-parse", "HEAD^1"],
    "workspace.git.status_short": ["git", "status", "--short"],
}


def detect_external_failure(stderr: bytes, stdout: bytes = b"") -> dict[str, str] | None:
    text = stderr.decode("utf-8", errors="replace")
    if COLLAB_PARENT_THREAD_MISSING in text:
        return {
            "schema_version": "the-caption-prompt.run-status/v1",
            "status": "excluded",
            "category": "external_failure",
            "reason_code": "codex_collab_parent_thread_missing",
            "detector": "codex-stderr-signature/v1",
        }
    for raw_line in stdout.splitlines():
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") not in {"error", "turn.failed"}:
            continue
        error = event.get("error")
        message = event.get("message")
        if isinstance(error, dict):
            message = error.get("message")
        if isinstance(message, str) and MODEL_AT_CAPACITY in message:
            return {
                "schema_version": "the-caption-prompt.run-status/v1",
                "status": "excluded",
                "category": "external_failure",
                "reason_code": "codex_model_at_capacity",
                "detector": "codex-jsonl-event/v1",
            }
    return None


def load_object(path: Path, name: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise AdapterError(f"invalid {name}: {path}") from exc
    if not isinstance(value, dict):
        raise AdapterError(f"{name} root must be an object")
    return value


def require_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AdapterError(f"{name} must be an object")
    return value


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise AdapterError(f"{name} must be a non-empty string")
    return value


def require_string_array(value: Any, name: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise AdapterError(f"{name} must be a string array")
    return value


def agents_max_threads_from_conditions(conditions: dict[str, Any]) -> int:
    agent_environment = require_object(
        conditions.get("agent_environment"), "comparison_conditions.agent_environment"
    )
    value = agent_environment.get("agents_max_threads")
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise AdapterError(
            "comparison_conditions.agent_environment.agents_max_threads "
            "must be a positive integer"
        )
    return value


def capability_catalog_policy_from_conditions(
    conditions: dict[str, Any],
) -> dict[str, Any] | None:
    agent_environment = require_object(
        conditions.get("agent_environment"), "comparison_conditions.agent_environment"
    )
    raw_policy = agent_environment.get("model_visible_capability_catalog")
    if raw_policy is None:
        return None
    policy = require_object(
        raw_policy,
        "comparison_conditions.agent_environment.model_visible_capability_catalog",
    )
    expected = {
        "apps_enabled": False,
        "plugins_enabled": False,
        "plugin_sharing_enabled": False,
        "schema_version": MODEL_VISIBLE_CAPABILITY_CATALOG_SCHEMA_VERSION,
    }
    if any(policy.get(key) != value for key, value in expected.items()):
        raise AdapterError("unsupported model-visible capability catalog policy")
    require_string(
        policy.get("expected_sha256"),
        "model_visible_capability_catalog.expected_sha256",
    )
    return policy


def capability_catalog_identity(rollout_file: Path) -> dict[str, Any]:
    tag_pattern = "|".join(re.escape(tag) for tag in MODEL_VISIBLE_CAPABILITY_TAGS)
    pattern = re.compile(
        rf"<({tag_pattern})>.*?</\1>",
        re.DOTALL,
    )
    blocks: list[str] = []
    try:
        lines = rollout_file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise AdapterError(f"cannot read root rollout capability catalog: {rollout_file}") from exc
    for raw_line in lines:
        try:
            item = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        if not isinstance(item, dict) or item.get("type") != "response_item":
            continue
        payload = item.get("payload")
        if not isinstance(payload, dict) or payload.get("role") != "developer":
            continue
        content = payload.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict) or not isinstance(part.get("text"), str):
                continue
            blocks.extend(match.group(0) for match in pattern.finditer(part["text"]))
    serialized = "".join(f"{block}\n" for block in blocks)
    return {
        "schema_version": MODEL_VISIBLE_CAPABILITY_CATALOG_SCHEMA_VERSION,
        "block_count": len(blocks),
        "block_tags": [pattern.match(block).group(1) for block in blocks],
        "serialized_bytes": len(serialized.encode("utf-8")),
        "sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
    }


def root_rollout_file(all_agent_usage: dict[str, Any]) -> Path:
    root_thread_id = require_string(
        all_agent_usage.get("root_thread_id"), "all-agent usage root_thread_id"
    )
    sessions = all_agent_usage.get("sessions")
    if not isinstance(sessions, list):
        raise AdapterError("all-agent usage sessions must be an array")
    for raw_session in sessions:
        if not isinstance(raw_session, dict) or raw_session.get("thread_id") != root_thread_id:
            continue
        return Path(
            require_string(raw_session.get("rollout_file"), "root session rollout_file")
        )
    raise AdapterError("all-agent usage does not contain the root rollout")


def capability_catalog_external_failure(
    identity: dict[str, Any], policy: dict[str, Any]
) -> dict[str, str] | None:
    if identity.get("sha256") == policy.get("expected_sha256"):
        return None
    return {
        "schema_version": "the-caption-prompt.run-status/v1",
        "status": "excluded",
        "category": "external_failure",
        "reason_code": "model_visible_capability_catalog_mismatch",
        "detector": MODEL_VISIBLE_CAPABILITY_CATALOG_SCHEMA_VERSION,
    }


def command_protocol_for_case(
    declaration: Any, case_id: str
) -> tuple[dict[str, Any] | None, list[list[str]]]:
    if declaration is None:
        return None, []
    declaration = require_object(declaration, "executor_parameters.command_evidence_protocol")
    protocol = next(
        (
            candidate
            for candidate in SUPPORTED_COMMAND_EVIDENCE_PROTOCOLS
            if all(declaration.get(key) == expected for key, expected in candidate.items())
        ),
        None,
    )
    if protocol is None:
        raise AdapterError("unsupported command evidence protocol")
    omitted_case_ids = require_string_array(
        declaration.get("omit_for_cases", []),
        "command_evidence_protocol.omit_for_cases",
    )
    if len(omitted_case_ids) != len(set(omitted_case_ids)):
        raise AdapterError("command_evidence_protocol.omit_for_cases must not contain duplicates")
    if case_id in omitted_case_ids:
        return None, []
    groups_by_case = require_object(
        declaration.get("required_command_groups_by_case"),
        "command_evidence_protocol.required_command_groups_by_case",
    )
    raw_groups = groups_by_case.get(case_id, [])
    if not isinstance(raw_groups, list):
        raise AdapterError("required command groups must be an array")
    groups: list[list[str]] = []
    for index, raw_group in enumerate(raw_groups):
        groups.append(
            require_string_array(
                raw_group,
                f"required_command_groups_by_case.{case_id}[{index}]",
            )
        )
    return {
        **protocol,
        "required_command_groups": groups,
    }, groups


def command_evidence_external_failure(
    requirement_statuses: list[dict[str, Any]],
) -> dict[str, str] | None:
    if not any(
        item.get("status") == "evidence_incomplete" for item in requirement_statuses
    ):
        return None
    return {
        "schema_version": "the-caption-prompt.run-status/v1",
        "status": "excluded",
        "category": "external_failure",
        "reason_code": "command_evidence_incomplete",
        "detector": "command-evidence-protocol/v1",
    }


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None, binary: bool = False) -> str | bytes:
    completed = subprocess.run(command, cwd=cwd, env=env, capture_output=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise AdapterError(f"command failed ({completed.returncode}): {' '.join(command)}: {detail}")
    if binary:
        return completed.stdout
    return completed.stdout.decode("utf-8", errors="strict").strip()


def changed_paths(workspace: Path) -> set[str]:
    commands = [
        ["git", "diff", "--name-only", "--no-ext-diff"],
        ["git", "diff", "--cached", "--name-only", "--no-ext-diff"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    paths: set[str] = set()
    for command in commands:
        output = run(command, workspace)
        assert isinstance(output, str)
        paths.update(line for line in output.splitlines() if line)
    return paths


def prompt_fixture_collisions(case: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    protected = set(
        require_string_array(case.get("fixture_condition_paths", []), "case.fixture_condition_paths")
    )
    raw_files = manifest.get("files")
    if not isinstance(raw_files, list):
        raise AdapterError("prompt bundle manifest files must be an array")
    targets: set[str] = set()
    for index, raw_entry in enumerate(raw_files):
        entry = require_object(raw_entry, f"prompt bundle manifest files[{index}]")
        targets.add(require_string(entry.get("target"), f"prompt bundle manifest files[{index}].target"))
    return sorted(protected & targets)


def overlay_bundle(workspace: Path, bundle: Path, manifest: dict[str, Any]) -> list[str]:
    storage_format = storage_format_of(manifest)
    targets: list[str] = []
    for raw_entry in manifest["files"]:
        target = raw_entry["target"]
        source = bundle_stored_path(bundle / "files", target, storage_format)
        destination = workspace / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.is_symlink() or destination.exists():
            if destination.is_dir() and not destination.is_symlink():
                raise AdapterError(f"bundle target collides with directory: {target}")
            destination.unlink()
        if raw_entry["type"] == "symlink":
            destination.symlink_to(raw_entry["link_target"])
        else:
            shutil.copyfile(source, destination, follow_symlinks=False)
            destination.chmod(0o755 if raw_entry["mode"] == "100755" else 0o644)
        targets.append(target)
    return targets


def materialize_shared_venv(source: Path, destination: Path, workspace: Path) -> None:
    destination = destination.resolve()
    source_python = source / "bin" / "python"
    if not source_python.is_file() or not os.access(source_python, os.X_OK):
        raise AdapterError("shared Python runtime has no executable bin/python")

    source_purelib_raw = run(
        [str(source_python), "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"],
        source,
    )
    assert isinstance(source_purelib_raw, str)
    source_purelib = Path(source_purelib_raw).resolve()
    if not source_purelib.is_dir() or not source_purelib.is_relative_to(source):
        raise AdapterError("shared Python runtime purelib is outside the runtime")

    run(
        [str(source_python), "-m", "venv", "--without-pip", str(destination)],
        workspace,
    )
    destination_python = destination / "bin" / "python"
    destination_purelib_raw = run(
        [str(destination_python), "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"],
        workspace,
    )
    assert isinstance(destination_purelib_raw, str)
    destination_purelib = Path(destination_purelib_raw).resolve()
    if not destination_purelib.is_dir() or not destination_purelib.is_relative_to(destination):
        raise AdapterError("local Python runtime purelib is outside the runtime shim")

    shared_path = json.dumps(str(source_purelib), ensure_ascii=True)
    (destination_purelib / "the_caption_shared_runtime.pth").write_text(
        f"import site; site.addsitedir({shared_path})\n",
        encoding="utf-8",
    )

    source_bin = source / "bin"
    destination_bin = destination / "bin"
    for source_script in source_bin.iterdir():
        destination_script = destination_bin / source_script.name
        if destination_script.exists() or destination_script.is_symlink() or source_script.is_symlink():
            continue
        if not source_script.is_file():
            continue
        content = source_script.read_bytes()
        first_line, separator, remainder = content.partition(b"\n")
        if not separator or not first_line.startswith(b"#!"):
            continue
        destination_script.write_bytes(
            f"#!{destination_python}\n".encode("utf-8") + remainder
        )
        shutil.copymode(source_script, destination_script)

    verification = run(
        [
            str(destination_python),
            "-c",
            "import pip, pytest, sys; print(sys.prefix); print(sys.executable)",
        ],
        workspace,
    )
    assert isinstance(verification, str)
    if verification.splitlines() != [str(destination), str(destination_python)]:
        raise AdapterError("shared Python runtime shim did not preserve local identity")


def prepare_runtime_links(workspace: Path, raw_links: Any) -> list[dict[str, str]]:
    if raw_links is None:
        return []
    if not isinstance(raw_links, list):
        raise AdapterError("parameters.runtime_links must be an array")
    prepared: list[dict[str, str]] = []
    for index, raw_link in enumerate(raw_links):
        link = require_object(raw_link, f"runtime_links[{index}]")
        target = require_string(link.get("target"), f"runtime_links[{index}].target")
        target_path = PurePosixPath(target)
        if target_path.is_absolute() or target != target_path.as_posix() or ".." in target_path.parts:
            raise AdapterError(f"unsafe runtime link target: {target}")
        source = Path(require_string(link.get("source"), f"runtime_links[{index}].source")).resolve()
        if not source.is_dir() or source == workspace or source.is_relative_to(workspace):
            raise AdapterError(f"invalid runtime link source: {source}")
        identity_file = require_string(
            link.get("identity_file"),
            f"runtime_links[{index}].identity_file",
        )
        identity_path = (source / identity_file).resolve()
        if not identity_path.is_file() or not identity_path.is_relative_to(source):
            raise AdapterError(f"invalid runtime identity file: {identity_file}")
        expected_sha256 = require_string(
            link.get("identity_sha256"),
            f"runtime_links[{index}].identity_sha256",
        )
        materialization = link.get("materialization", "symlink")
        if materialization not in {"symlink", "copy", "venv_shim"}:
            raise AdapterError(f"unsupported runtime materialization: {materialization}")
        actual_sha256 = hashlib.sha256(identity_path.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            raise AdapterError(f"runtime identity mismatch: {target}")
        python_version: str | None = None
        if materialization == "venv_shim":
            source_python = source / "bin" / "python"
            expected_python_version = require_string(
                link.get("python_version"),
                f"runtime_links[{index}].python_version",
            )
            actual_python_version = run(
                [str(source_python), "-c", "import platform; print(platform.python_version())"],
                source,
            )
            assert isinstance(actual_python_version, str)
            if actual_python_version != expected_python_version:
                raise AdapterError(f"shared Python version differs from runtime identity: {target}")
            python_version = actual_python_version
            frozen = run(
                [str(source_python), "-m", "pip", "freeze", "--all"],
                source,
                binary=True,
            )
            assert isinstance(frozen, bytes)
            if frozen != identity_path.read_bytes():
                raise AdapterError(f"shared Python package set differs from runtime identity: {target}")
        destination = workspace.joinpath(*target_path.parts)
        if destination.exists() or destination.is_symlink():
            raise AdapterError(f"runtime link target already exists: {target}")
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", "--", f"{target}/"],
            cwd=workspace,
            capture_output=True,
            check=False,
        )
        if ignored.returncode != 0:
            raise AdapterError(f"runtime link target is not Git-ignored: {target}")
        exclude = workspace / ".git" / "info" / "exclude"
        if not exclude.is_file():
            raise AdapterError("workspace Git exclude file is missing")
        existing_excludes = exclude.read_text(encoding="utf-8")
        if target not in existing_excludes.splitlines():
            with exclude.open("a", encoding="utf-8", newline="\n") as handle:
                if existing_excludes and not existing_excludes.endswith("\n"):
                    handle.write("\n")
                handle.write(f"{target}\n")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if materialization == "copy":
            shutil.copytree(source, destination, symlinks=True)
        elif materialization == "venv_shim":
            materialize_shared_venv(source, destination, workspace)
        else:
            destination.symlink_to(source, target_is_directory=True)
        receipt = {
            "identity_file": identity_file,
            "identity_sha256": actual_sha256,
            "materialization": materialization,
            "source": str(source),
            "target": target,
        }
        if python_version is not None:
            receipt["python_version"] = python_version
        prepared.append(receipt)
    return prepared


def remove_adapter_owned_outputs(workspace: Path, raw_paths: Any) -> list[str]:
    """Remove only outputs explicitly assigned to the evaluation adapter."""
    if raw_paths is None:
        return []
    paths = require_string_array(raw_paths, "parameters.adapter_teardown_paths")
    removed: list[str] = []
    for raw_path in paths:
        relative = PurePosixPath(raw_path)
        if (
            relative.is_absolute()
            or raw_path != relative.as_posix()
            or relative == PurePosixPath(".")
            or ".." in relative.parts
        ):
            raise AdapterError(f"unsafe adapter teardown path: {raw_path}")
        destination = workspace.joinpath(*relative.parts)
        ancestor = destination.parent
        while ancestor != workspace:
            if ancestor.is_symlink():
                raise AdapterError(f"adapter teardown path traverses symlink: {raw_path}")
            if not ancestor.is_relative_to(workspace):
                raise AdapterError(f"adapter teardown path escapes workspace: {raw_path}")
            ancestor = ancestor.parent
        if not destination.exists() and not destination.is_symlink():
            continue
        if destination.is_dir() and not destination.is_symlink():
            shutil.rmtree(destination)
        else:
            destination.unlink()
        removed.append(raw_path)
    return removed


def adapter_teardown_paths_from_protocol(
    binding: dict[str, Any], parameters: dict[str, Any], executor_parameters: dict[str, Any]
) -> list[str]:
    declaration = executor_parameters.get("adapter_owned_teardown")
    direct_paths = parameters.get("adapter_teardown_paths")
    if declaration is None:
        return require_string_array(
            [] if direct_paths is None else direct_paths,
            "parameters.adapter_teardown_paths",
        )
    declaration = require_object(declaration, "executor_parameters.adapter_owned_teardown")
    if (
        declaration.get("schema_version") != ADAPTER_TEARDOWN_PROTOCOL["schema_version"]
        or declaration.get("failure_policy") != ADAPTER_TEARDOWN_PROTOCOL["failure_policy"]
    ):
        raise AdapterError("unsupported adapter-owned teardown protocol")
    paths_by_case = require_object(
        declaration.get("paths_by_case"), "adapter_owned_teardown.paths_by_case"
    )
    case_id = require_string(binding.get("case_id"), "binding.case_id")
    declared_paths = require_string_array(
        paths_by_case.get(case_id, []), f"adapter_owned_teardown.paths_by_case.{case_id}"
    )
    if direct_paths is not None and direct_paths != declared_paths:
        raise AdapterError("run teardown paths do not match the comparison condition")
    return declared_paths


def prompt_overlay_commit(workspace: Path, targets: list[str]) -> tuple[str, str]:
    if targets:
        run(["git", "add", "--", *targets], workspace)
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z",
            "GIT_AUTHOR_EMAIL": "evaluation@example.invalid",
            "GIT_AUTHOR_NAME": "THE-CAPTION Prompt Evaluation",
            "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z",
            "GIT_COMMITTER_EMAIL": "evaluation@example.invalid",
            "GIT_COMMITTER_NAME": "THE-CAPTION Prompt Evaluation",
        }
    )
    run(
        [
            "git",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "--allow-empty",
            "--no-verify",
            "-qm",
            "evaluation prompt overlay",
        ],
        workspace,
        env=env,
    )
    commit = run(["git", "rev-parse", "HEAD^{commit}"], workspace)
    tree = run(["git", "rev-parse", "HEAD^{tree}"], workspace)
    assert isinstance(commit, str) and isinstance(tree, str)
    return commit, tree


def observe_boundary_source(command: list[str], workspace: Path) -> str:
    completed = subprocess.run(command, cwd=workspace, capture_output=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise AdapterError(
            f"boundary observation failed ({completed.returncode}): {' '.join(command)}: {detail}"
        )
    return completed.stdout.decode("utf-8", errors="strict").rstrip("\r\n")


def evaluate_boundary_observations(
    workspace: Path,
    raw_observations: Any,
    adapter_context: dict[str, str],
) -> dict[str, Any] | None:
    if raw_observations is None:
        return None
    if not isinstance(raw_observations, list):
        raise AdapterError("parameters.boundary_observations must be an array")
    if not raw_observations:
        raise AdapterError("parameters.boundary_observations must not be empty")

    observations: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, raw_observation in enumerate(raw_observations):
        name = f"boundary_observations[{index}]"
        observation = require_object(raw_observation, name)
        observation_id = require_string(observation.get("observation_id"), f"{name}.observation_id")
        if observation_id in seen_ids:
            raise AdapterError(f"duplicate boundary observation id: {observation_id}")
        seen_ids.add(observation_id)

        operation_identity = require_string(
            observation.get("operation_identity"), f"{name}.operation_identity"
        )
        source = require_string(observation.get("source"), f"{name}.source")
        command = BOUNDARY_OBSERVATION_SOURCES.get(source)
        if command is None:
            raise AdapterError(f"unsupported boundary observation source: {source}")

        predicate = require_object(observation.get("predicate"), f"{name}.predicate")
        operator = require_string(predicate.get("operator"), f"{name}.predicate.operator")
        if operator != "string_equals":
            raise AdapterError(f"unsupported boundary predicate operator: {operator}")
        has_expected = "expected" in predicate
        has_expected_context = "expected_context" in predicate
        if has_expected == has_expected_context:
            raise AdapterError(
                f"{name}.predicate needs exactly one of expected or expected_context"
            )
        if has_expected:
            expected = predicate["expected"]
            if not isinstance(expected, str):
                raise AdapterError(f"{name}.predicate.expected must be a string")
            expected_binding: dict[str, str] = {"kind": "literal", "value": expected}
        else:
            context_key = require_string(
                predicate["expected_context"], f"{name}.predicate.expected_context"
            )
            if context_key not in adapter_context:
                raise AdapterError(f"unsupported adapter context key: {context_key}")
            expected = adapter_context[context_key]
            expected_binding = {"kind": "adapter_context", "key": context_key, "value": expected}

        try:
            observed = observe_boundary_source(command, workspace)
        except (AdapterError, OSError, UnicodeError) as exc:
            result = {
                "observation_id": observation_id,
                "operation_identity": operation_identity,
                "source": source,
                "predicate": {
                    "operator": operator,
                    "expected_binding": expected_binding,
                },
                "observed_value": None,
                "status": "unavailable",
                "unavailable_reason": str(exc),
            }
        else:
            result = {
                "observation_id": observation_id,
                "operation_identity": operation_identity,
                "source": source,
                "predicate": {
                    "operator": operator,
                    "expected_binding": expected_binding,
                },
                "observed_value": observed,
                "status": "passed" if observed == expected else "failed",
            }
        observations.append(result)

    return {
        "schema_version": BOUNDARY_EVIDENCE_SCHEMA_VERSION,
        "binding_revision": BOUNDARY_EVIDENCE_BINDING_REVISION,
        "provenance": {
            "workspace": adapter_context["workspace"],
            "prompt_overlay_commit": adapter_context["prompt_overlay_commit"],
            "prompt_overlay_tree": adapter_context["prompt_overlay_tree"],
        },
        "observations": observations,
    }


def validate_boundary_evidence_compatibility(capsule: dict[str, Any], raw_observations: Any) -> None:
    conditions = require_object(capsule.get("comparison_conditions"), "run.comparison_conditions")
    executor_parameters = require_object(
        conditions.get("executor_parameters"), "comparison_conditions.executor_parameters"
    )
    declared = executor_parameters.get("boundary_evidence")
    if raw_observations is None:
        if declared is not None:
            raise AdapterError(
                "comparison conditions declare boundary evidence without boundary observations"
            )
        return

    expected = {
        "binding_revision": BOUNDARY_EVIDENCE_BINDING_REVISION,
        "schema_version": BOUNDARY_EVIDENCE_SCHEMA_VERSION,
        "source_policy": BOUNDARY_EVIDENCE_SOURCE_POLICY,
    }
    if declared != expected:
        raise AdapterError("comparison conditions do not bind the typed boundary evidence revision")
    agent_environment = require_object(
        conditions.get("agent_environment"), "comparison_conditions.agent_environment"
    )
    if agent_environment.get("adapter_schema_version") != "the-caption-prompt.codex-adapter/v4":
        raise AdapterError("comparison conditions do not bind codex-adapter/v4")


def render_task(
    case: dict[str, Any],
    boundary_evidence: dict[str, Any] | None = None,
    command_evidence_protocol: dict[str, Any] | None = None,
) -> str:
    payload = require_object(case.get("payload"), "case.payload")
    trial_input = require_object(payload.get("trial_prompt_input"), "case.payload.trial_prompt_input")
    serialized = json.dumps(trial_input, ensure_ascii=False, indent=2, sort_keys=True)
    task = "以下のTaskSpecに従って作業してください。\n\n<task-spec-json>\n" + serialized + "\n</task-spec-json>\n"
    if command_evidence_protocol is not None:
        protocol = next(
            (
                candidate
                for candidate in SUPPORTED_COMMAND_EVIDENCE_PROTOCOLS
                if all(
                    command_evidence_protocol.get(key) == expected
                    for key, expected in candidate.items()
                )
            ),
            None,
        )
        if protocol is None or not isinstance(
            command_evidence_protocol.get("required_command_groups"), list
        ):
            raise AdapterError("unsupported command evidence protocol")
        task += "\n以下は全candidate共通の評価用command証跡protocolです。\n"
        if protocol == ORDERED_ROOT_WRAPPER_PROTOCOL:
            task += (
                "root producerはrequired validation command群を1回のcustom exec wrapper内から、"
                "列挙順にtools.exec_commandへ1 commandずつ個別invocationしてください。"
                "wrapper内で各exit_codeを確認し、nonzeroまたはunavailableなら後続commandを発行せず、"
                "完了済みの全resultを一度だけmodelへ返してください。\n"
                "shell commandをcompound command、`&&`、`;`で結合しないでください。"
                "各結果を{\"command\":実行した完全なcommand文字列,\"exit_code\":返却された整数}の"
                "JSONとして出力してください。\n"
                "descendant workerへ委譲する場合もworker packetに同じprotocolを含め、同じwrapper境界を"
                "適用してください。exit_code=0のtool resultがないcommandをPASSと報告しないでください。\n"
            )
        else:
            task += (
                "TaskSpecのrequired validation commandは1 commandずつ個別のexec_commandで実行し、"
                "compound commandへまとめないでください。\n"
                "descendant workerがcustom exec wrapperを使う場合は、各結果を"
                "{\"command\":実行した完全なcommand文字列,\"exit_code\":返却された整数}のJSONとして出力してください。\n"
                "worker packetにも同じprotocolを含め、exit_code=0のtool resultがないcommandをPASSと報告しないでください。\n"
            )
        task += (
            "<command-evidence-protocol-json>\n"
            + json.dumps(command_evidence_protocol, ensure_ascii=False, sort_keys=True)
            + "\n</command-evidence-protocol-json>\n"
        )
    if boundary_evidence is not None:
        evidence = json.dumps(boundary_evidence, ensure_ascii=False, indent=2, sort_keys=True)
        task += (
            "\n以下は実行adapterがread-only sourceから観測し、1 observationと1 predicateを対応付けた証跡です。\n"
            "列挙されたoperationの同じpredicateは観測済みとしてstatusを使用し、raw出力を再取得・再解釈しないでください。\n"
            "statusがfailedまたはunavailableなら、TaskSpecのterminal条件に従ってください。\n\n"
            "<adapter-boundary-evidence-json>\n"
            + evidence
            + "\n</adapter-boundary-evidence-json>\n"
        )
    return task


def parse_usage(jsonl: bytes) -> tuple[int, dict[str, int]]:
    latest: dict[str, int] | None = None
    for raw_line in jsonl.splitlines():
        if not raw_line.strip():
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") != "turn.completed":
            continue
        usage = event.get("usage")
        if isinstance(usage, dict):
            latest = {
                key: value
                for key, value in usage.items()
                if isinstance(key, str) and isinstance(value, int) and value >= 0
            }
    if latest is None:
        raise AdapterError("Codex JSONL did not contain turn.completed usage")
    total = latest.get("total_tokens")
    if total is None:
        input_tokens = latest.get("input_tokens")
        output_tokens = latest.get("output_tokens")
        if input_tokens is None or output_tokens is None:
            raise AdapterError("Codex usage lacks total_tokens or input/output tokens")
        total = input_tokens + output_tokens
    return total, latest


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def prompt_set_identity_from_binding(
    binding: dict[str, Any], manifest: dict[str, Any], expected_hash: str
) -> dict[str, Any]:
    prompt_set_identity = require_object(
        binding.get("prompt_set_identity"), "binding.prompt_set_identity"
    )
    prompt_identity = require_string(
        prompt_set_identity.get("name"), "binding.prompt_set_identity.name"
    )
    if not any(prompt_set_identity.get(key) for key in ("revision", "bundle_sha256")):
        raise AdapterError("binding.prompt_set_identity needs revision or bundle_sha256")
    identity_bundle_hash = prompt_set_identity.get("bundle_sha256")
    if identity_bundle_hash is not None:
        identity_bundle_hash = require_string(
            identity_bundle_hash, "binding.prompt_set_identity.bundle_sha256"
        )
    if (
        manifest.get("prompt_identity") != prompt_identity
        or manifest.get("bundle_sha256") != expected_hash
        or (identity_bundle_hash is not None and identity_bundle_hash != expected_hash)
    ):
        raise AdapterError("run binding does not match prompt bundle identity")
    return prompt_set_identity


def execute() -> int:
    workspace = Path.cwd().resolve()
    case_path = Path(require_string(os.environ.get("EVAL_CASE_FILE"), "EVAL_CASE_FILE"))
    capsule_path = Path(require_string(os.environ.get("EVAL_RUN_CAPSULE_FILE"), "EVAL_RUN_CAPSULE_FILE"))
    usage_path = Path(require_string(os.environ.get("EVAL_USAGE_FILE"), "EVAL_USAGE_FILE"))
    status_path = Path(require_string(os.environ.get("EVAL_RUN_STATUS_FILE"), "EVAL_RUN_STATUS_FILE"))
    extension_root = Path(require_string(os.environ.get("EVAL_EXTENSION_DIR"), "EVAL_EXTENSION_DIR"))
    case = load_object(case_path, "case capsule")
    capsule = load_object(capsule_path, "run capsule")
    binding = require_object(capsule.get("binding"), "run.binding")
    parameters = require_object(capsule.get("parameters"), "run.parameters")
    validate_boundary_evidence_compatibility(capsule, parameters.get("boundary_observations"))
    bundle = Path(require_string(parameters.get("prompt_bundle"), "parameters.prompt_bundle")).resolve()
    expected_hash = require_string(parameters.get("bundle_sha256"), "parameters.bundle_sha256")
    expected_dirty = set(require_string_array(parameters.get("expected_initial_dirty_paths"), "expected_initial_dirty_paths"))
    allowed_result_paths = set(require_string_array(parameters.get("allowed_result_paths"), "allowed_result_paths"))
    model = require_string(parameters.get("model"), "parameters.model")
    reasoning_effort = require_string(parameters.get("reasoning_effort"), "parameters.reasoning_effort")
    manifest = verify_bundle(bundle)
    prompt_set_identity = prompt_set_identity_from_binding(binding, manifest, expected_hash)
    collisions = prompt_fixture_collisions(case, manifest)
    if collisions:
        raise AdapterError(
            "prompt bundle targets collide with fixture condition paths: " + ", ".join(collisions)
        )
    runtime_links = prepare_runtime_links(workspace, parameters.get("runtime_links"))
    if changed_paths(workspace) != expected_dirty:
        raise AdapterError("fixture dirty paths do not match the run capsule")

    targets = overlay_bundle(workspace, bundle, manifest)
    commit, tree = prompt_overlay_commit(workspace, targets)
    if changed_paths(workspace) != expected_dirty:
        raise AdapterError("prompt overlay commit did not preserve the seeded dirty state")

    boundary_evidence = evaluate_boundary_observations(
        workspace,
        parameters.get("boundary_observations"),
        {
            "workspace": str(workspace),
            "prompt_overlay_commit": commit,
            "prompt_overlay_tree": tree,
        },
    )
    conditions = require_object(capsule.get("comparison_conditions"), "run.comparison_conditions")
    agents_max_threads = agents_max_threads_from_conditions(conditions)
    capability_catalog_policy = capability_catalog_policy_from_conditions(conditions)
    executor_parameters = require_object(
        conditions.get("executor_parameters"), "comparison_conditions.executor_parameters"
    )
    declared_command_protocol, required_command_groups = command_protocol_for_case(
        executor_parameters.get("command_evidence_protocol"),
        require_string(binding.get("case_id"), "binding.case_id"),
    )
    adapter_teardown_paths = adapter_teardown_paths_from_protocol(
        binding, parameters, executor_parameters
    )
    task = render_task(case, boundary_evidence, declared_command_protocol)
    task_sha256 = hashlib.sha256(task.encode("utf-8")).hexdigest()
    adapter_extension = extension_root / "codex-adapter"
    final_response = adapter_extension / "final-response.txt"
    adapter_extension.mkdir(parents=True, exist_ok=True)
    boundary_evidence_sha256 = None
    if boundary_evidence is not None:
        boundary_evidence_bytes = (
            json.dumps(boundary_evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        boundary_evidence_sha256 = hashlib.sha256(boundary_evidence_bytes).hexdigest()
        write_json(extension_root / "boundary-evidence" / "evidence.json", boundary_evidence)
    command = [
        "codex",
        "exec",
        "--ignore-user-config",
        "--ignore-rules",
        "--strict-config",
        "--enable",
        "multi_agent",
        "--disable",
        "memories",
        "-c",
        f"agents.max_threads={agents_max_threads}",
        "-c",
        'approval_policy="never"',
        "-m",
        model,
        "-c",
        f'model_reasoning_effort="{reasoning_effort}"',
        "-s",
        "workspace-write",
        "--json",
        "--output-last-message",
        str(final_response),
        "-",
    ]
    if capability_catalog_policy is not None:
        command[command.index("-c"):command.index("-c")] = [
            "--disable",
            "apps",
            "--disable",
            "plugins",
            "--disable",
            "plugin_sharing",
        ]
    session_started_at = time.time()
    completed = subprocess.run(
        command,
        cwd=workspace,
        input=task.encode("utf-8"),
        capture_output=True,
        check=False,
    )
    sys.stdout.buffer.write(completed.stdout)
    sys.stderr.buffer.write(completed.stderr)
    (adapter_extension / "codex-events.jsonl").write_bytes(completed.stdout)
    (adapter_extension / "codex-stderr.bin").write_bytes(completed.stderr)
    external_failure = detect_external_failure(completed.stderr, completed.stdout)
    root_total_tokens = None
    all_agent_usage = None
    command_evidence = None
    command_protocol_audit = None
    capability_catalog = None
    cleanup_attempts: list[dict[str, Any]] = []
    reported_cleanup_attempts: list[dict[str, Any]] = []
    if external_failure is not None:
        write_json(status_path, external_failure)
        total_tokens = None
        raw_usage = None
    else:
        root_total_tokens, raw_usage = parse_usage(completed.stdout)
        codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).resolve()
        try:
            all_agent_usage = collect_workspace_usage(
                codex_home / "sessions",
                workspace,
                parse_root_thread_id(completed.stdout),
                root_total_tokens,
                modified_since=session_started_at - 60,
            )
        except AllAgentUsageError as exc:
            external_failure = {
                "schema_version": "the-caption-prompt.run-status/v1",
                "status": "excluded",
                "category": "external_failure",
                "reason_code": "codex_all_agent_usage_incomplete",
                "detector": "codex-rollout-final-usage/v1",
            }
            write_json(
                adapter_extension / "all-agent-usage-error.json",
                {
                    "schema_version": "the-caption-prompt.all-agent-usage-error/v1",
                    "reason": str(exc),
                },
            )
            write_json(status_path, external_failure)
            total_tokens = None
        else:
            total_tokens = all_agent_usage["all_agent_total_tokens"]
            all_agent_usage["run_id"] = extension_root.name
            all_agent_usage["generated_at"] = datetime.now(timezone.utc).isoformat()
            all_agent_usage["source"] = "local Codex rollout final usage grouped by exact workspace"
            write_json(
                extension_root / "all-agent-usage" / "usage.json",
                all_agent_usage,
            )
            if capability_catalog_policy is not None:
                try:
                    capability_catalog = capability_catalog_identity(
                        root_rollout_file(all_agent_usage)
                    )
                except AdapterError as exc:
                    external_failure = {
                        "schema_version": "the-caption-prompt.run-status/v1",
                        "status": "excluded",
                        "category": "external_failure",
                        "reason_code": "model_visible_capability_catalog_unavailable",
                        "detector": MODEL_VISIBLE_CAPABILITY_CATALOG_SCHEMA_VERSION,
                    }
                    write_json(
                        adapter_extension / "capability-catalog-error.json",
                        {
                            "schema_version": "the-caption-prompt.capability-catalog-error/v1",
                            "reason": str(exc),
                        },
                    )
                else:
                    write_json(
                        extension_root / "model-visible-capability-catalog" / "identity.json",
                        capability_catalog,
                    )
                    external_failure = capability_catalog_external_failure(
                        capability_catalog, capability_catalog_policy
                    )
                if external_failure is not None:
                    write_json(status_path, external_failure)
                    total_tokens = None
            if external_failure is None:
                write_json(
                    usage_path,
                    {
                        "schema_version": "the-caption-prompt.token-usage/v2",
                        "token_accounting": TOKEN_ACCOUNTING,
                        "total_tokens": total_tokens,
                    },
                )
            if external_failure is None and declared_command_protocol is not None:
                try:
                    command_evidence = collect_command_evidence(
                        extension_root / "all-agent-usage" / "usage.json",
                        adapter_extension / "codex-events.jsonl",
                    )
                except AllAgentCommandEvidenceError as exc:
                    external_failure = {
                        "schema_version": "the-caption-prompt.run-status/v1",
                        "status": "excluded",
                        "category": "external_failure",
                        "reason_code": "command_evidence_collection_failed",
                        "detector": "all-agent-command-evidence/v5",
                    }
                    write_json(
                        adapter_extension / "command-evidence-error.json",
                        {
                            "schema_version": "the-caption-prompt.command-evidence-error/v1",
                            "reason": str(exc),
                        },
                    )
                    write_json(status_path, external_failure)
                else:
                    write_json(
                        extension_root / "all-agent-command-evidence" / "evidence.json",
                        command_evidence,
                    )
                    requirement_statuses = command_requirement_statuses(
                        command_evidence, required_command_groups
                    )
                    cleanup_attempts = adapter_owned_cleanup_attempts(
                        command_evidence, adapter_teardown_paths
                    )
                    reported_cleanup_attempts = (
                        model_reported_adapter_owned_cleanup_attempts(
                            adapter_extension / "codex-events.jsonl",
                            adapter_teardown_paths,
                        )
                    )
                    command_protocol_audit = {
                        "schema_version": "the-caption-prompt.command-protocol-audit/v1",
                        "run_id": extension_root.name,
                        "requirements": requirement_statuses,
                        "summary": {
                            status: sum(
                                item["status"] == status for item in requirement_statuses
                            )
                            for status in (
                                "successful",
                                "failed",
                                "not_attempted",
                                "evidence_incomplete",
                            )
                        },
                    }
                    write_json(
                        extension_root / "command-protocol-audit" / "audit.json",
                        command_protocol_audit,
                    )
                    write_json(
                        extension_root / "evaluation-diagnostics" / "diagnostics.json",
                        {
                            "schema_version": "the-caption-prompt.evaluation-diagnostics/v1",
                            "run_id": extension_root.name,
                            "command_protocol_violation_count": command_evidence[
                                "protocol_violation_count"
                            ],
                            "command_protocol_violations": command_evidence[
                                "protocol_violations"
                            ],
                            "model_attempted_adapter_owned_cleanup_count": len(
                                cleanup_attempts
                            ),
                            "model_attempted_adapter_owned_cleanup": cleanup_attempts,
                            "model_reported_adapter_owned_cleanup_attempt_count": len(
                                reported_cleanup_attempts
                            ),
                            "model_reported_adapter_owned_cleanup_attempt": (
                                reported_cleanup_attempts
                            ),
                        },
                    )
                    protocol_failure = command_evidence_external_failure(
                        requirement_statuses
                    )
                    if protocol_failure is not None:
                        external_failure = protocol_failure
                        write_json(status_path, external_failure)
    adapter_teardown_paths_removed: list[str] = []
    try:
        adapter_teardown_paths_removed = remove_adapter_owned_outputs(
            workspace, adapter_teardown_paths
        )
    except OSError as exc:
        if external_failure is None:
            external_failure = {
                "schema_version": "the-caption-prompt.run-status/v1",
                "status": "excluded",
                "category": "external_failure",
                "reason_code": "adapter_owned_teardown_failed",
                "detector": "codex-adapter-teardown/v1",
            }
            write_json(status_path, external_failure)
        write_json(
            adapter_extension / "adapter-teardown-error.json",
            {
                "schema_version": "the-caption-prompt.adapter-teardown-error/v1",
                "reason": str(exc),
            },
        )
    final_paths = changed_paths(workspace)
    unexpected_paths = sorted(final_paths - allowed_result_paths)
    codex_version = run(["codex", "--version"], workspace)
    assert isinstance(codex_version, str)
    write_json(
        adapter_extension / "execution.json",
        {
            "adapter_schema_version": "the-caption-prompt.codex-adapter/v4",
            "boundary_evidence_schema_version": (
                None if boundary_evidence is None else BOUNDARY_EVIDENCE_SCHEMA_VERSION
            ),
            "boundary_evidence_sha256": boundary_evidence_sha256,
            "bundle_sha256": expected_hash,
            "codex_exit_code": completed.returncode,
            "codex_version": codex_version,
            "prompt_overlay_commit": commit,
            "prompt_overlay_tree": tree,
            "final_changed_paths": sorted(final_paths),
            "model": model,
            "prompt_set_identity": prompt_set_identity,
            "raw_usage": raw_usage,
            "root_total_tokens": root_total_tokens,
            "all_agent_total_tokens": None if all_agent_usage is None else all_agent_usage["all_agent_total_tokens"],
            "command_evidence_schema_version": (
                None if command_evidence is None else command_evidence["schema_version"]
            ),
            "command_protocol_audit_schema_version": (
                None if command_protocol_audit is None else command_protocol_audit["schema_version"]
            ),
            "model_visible_capability_catalog": capability_catalog,
            "token_accounting": TOKEN_ACCOUNTING,
            "reasoning_effort": reasoning_effort,
            "runtime_links": runtime_links,
            "adapter_teardown_paths_removed": adapter_teardown_paths_removed,
            "model_attempted_adapter_owned_cleanup_count": len(cleanup_attempts),
            "model_reported_adapter_owned_cleanup_attempt_count": len(
                reported_cleanup_attempts
            ),
            "session_mode": "persisted",
            "task_sha256": task_sha256,
            "unexpected_changed_paths": unexpected_paths,
            "external_failure": external_failure,
        },
    )
    if external_failure is not None:
        return EXTERNAL_FAILURE_EXIT_CODE
    if completed.returncode != 0:
        return completed.returncode
    if unexpected_paths:
        print(f"unexpected changed paths: {unexpected_paths}", file=sys.stderr)
        return 3
    return 0


def main() -> int:
    try:
        return execute()
    except (AdapterError, BundleError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

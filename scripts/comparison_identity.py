"""Split comparison conditions into the effective identity and recorded provenance.

The effective identity keeps only conditions that can change a result value: what the
model sees, how the agent behaves, and how the KPIs are counted. Provenance keeps where
and with which harness code the run happened. See docs/comparison-condition-identity-redesign.md.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

EFFECTIVE_IDENTITY_SCHEMA = "the-caption-prompt.effective-comparison-identity/v1"
INFRASTRUCTURE_PLUGIN_SOURCES = frozenset({"cc-plugin-telemetry@builtin", "cc-plugin-sec-default@builtin"})

PROVENANCE_PATHS = (
    ("executor_parameters", "time_recording", "code_sha256"),
    ("executor_parameters", "schedule_policy"),
    ("executor_parameters", "max_attempts"),
    ("executor_parameters", "monitor_interval_seconds"),
    ("executor_parameters", "duration_hint_method"),
    ("executor_parameters", "max_workers"),
    ("agent_environment", "python_version"),
    ("agent_environment", "runtime_identity_sha256"),
)
PROVENANCE_AGENT_KEYS = ("executable", "config_dir", "code_signature_team_identifier", "authentication")


def behavior_plugins(plugins: Any) -> Any:
    if not isinstance(plugins, list):
        return plugins
    return sorted(
        (
            plugin
            for plugin in plugins
            if not (isinstance(plugin, dict) and plugin.get("source") in INFRASTRUCTURE_PLUGIN_SOURCES)
        ),
        key=lambda plugin: json.dumps(plugin, sort_keys=True),
    )


def _pop_path(value: dict[str, Any], path: tuple[str, ...]) -> tuple[bool, Any]:
    node: Any = value
    for key in path[:-1]:
        if not isinstance(node, dict) or key not in node:
            return False, None
        node = node[key]
    if not isinstance(node, dict) or path[-1] not in node:
        return False, None
    item = node.pop(path[-1])
    for depth in range(len(path) - 1, 0, -1):
        parent: Any = value
        for key in path[: depth - 1]:
            parent = parent[key]
        if parent[path[depth - 1]] == {}:
            parent.pop(path[depth - 1])
        else:
            break
    return True, item


def split_effective(compatibility: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return (effective, provenance) without changing the input."""
    effective = copy.deepcopy(compatibility)
    provenance: dict[str, Any] = {}
    for path in PROVENANCE_PATHS:
        found, item = _pop_path(effective, path)
        if found:
            provenance[".".join(path)] = item
    agent = effective.get("agent_environment")
    if isinstance(agent, dict):
        for name, environment in sorted(agent.items()):
            if not isinstance(environment, dict):
                continue
            for key in PROVENANCE_AGENT_KEYS:
                if key in environment:
                    provenance[f"agent_environment.{name}.{key}"] = environment.pop(key)
            if "plugins" in environment:
                observed = environment["plugins"]
                environment["plugins"] = behavior_plugins(observed)
                if environment["plugins"] != observed:
                    provenance[f"agent_environment.{name}.plugins"] = observed
    return effective, provenance


def effective_key(compatibility: dict[str, Any]) -> str:
    effective, _ = split_effective(compatibility)
    payload = {"schema_version": EFFECTIVE_IDENTITY_SCHEMA, "effective": effective}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def code_sha256(compatibility: dict[str, Any]) -> Any:
    executor = compatibility.get("executor_parameters")
    if not isinstance(executor, dict):
        return None
    recording = executor.get("time_recording")
    return recording.get("code_sha256") if isinstance(recording, dict) else None


def effective_block_key(run_effective: dict[str, Any]) -> str:
    """Per-case key for atomic pools under effective-v1 (run_effective holds case_id and fixture)."""
    effective, _ = split_effective(run_effective)
    payload = {"schema_version": EFFECTIVE_IDENTITY_SCHEMA, "effective_block": effective}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def task_sha256_by_run(cycle: Path) -> dict[str, str]:
    """Rendered task SHA-256 recorded by the adapter of every run in a cycle, keyed by run id."""
    values: dict[str, str] = {}
    for execution in sorted(Path(cycle).glob("layer2/extensions/*/*-adapter/execution.json")):
        task = json.loads(execution.read_text(encoding="utf-8")).get("task_sha256")
        if isinstance(task, str) and task:
            values[execution.parent.parent.name] = task
    return values

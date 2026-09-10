from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.general_chat_agentic_binding_extractor import extract
from scripts.general_chat_agentic_private_trace_adapter import (
    DEFAULT_INPUT_SCHEMA,
    DEFAULT_OUTPUT_SCHEMA,
    DEFAULT_PACKET,
    DEFAULT_SHADOW_ROOT,
    PrivateTraceAdapterError,
    ROOT,
    adapt_private_trace,
    load_object,
    validate,
)


CAPABILITY_FIXTURE = ROOT / "docs/general-chat-agentic-capability-preflight-fixture-r1.json"


def packet() -> dict:
    value = load_object(DEFAULT_PACKET, "TEST_PACKET_UNAVAILABLE")
    validate(
        value,
        load_object(DEFAULT_INPUT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"),
        "TEST_PACKET_SCHEMA_INVALID",
    )
    return value


def materialize_shadow(tmp_path: Path, value: dict) -> tuple[Path, Path]:
    repository = tmp_path / "repository"
    trace_root = repository / "private-shadow"
    trace_root.mkdir(parents=True)
    for identity in [value["selection"]["root_events"]] + [
        session["file"] for session in value["selection"]["sessions"]
    ]:
        (trace_root / identity["path"]).write_bytes((DEFAULT_SHADOW_ROOT / identity["path"]).read_bytes())
    schema_identity = value["normalized_output_schema"]
    schema_target = repository / schema_identity["path"]
    schema_target.parent.mkdir(parents=True)
    schema_target.write_bytes((ROOT / schema_identity["path"]).read_bytes())
    return repository, trace_root


def bind_file(identity: dict, path: Path) -> None:
    data = path.read_bytes()
    identity["bytes"] = len(data)
    identity["sha256"] = hashlib.sha256(data).hexdigest()


def test_shadow_packet_and_output_are_schema_valid() -> None:
    value = packet()
    result = adapt_private_trace(value, DEFAULT_SHADOW_ROOT)
    validate(
        result,
        load_object(DEFAULT_OUTPUT_SCHEMA, "TEST_OUTPUT_SCHEMA_UNAVAILABLE"),
        "TEST_OUTPUT_SCHEMA_INVALID",
    )
    assert result["trace_origin"] == "synthetic_shadow"
    assert result["projection_state"] == "synthetic_shadow_verified"
    assert result["trace_file_count"] == 3
    assert result["raw_path_count"] == 0
    assert result["model_invocations"] == 0
    assert result["probe_issues"] == 0
    assert result["mutation_performed"] is False
    assert result["cleanup_responsibility"] == "runner"


def test_shadow_projection_preserves_unavailable_binding() -> None:
    result = adapt_private_trace(packet(), DEFAULT_SHADOW_ROOT)
    fixture = load_object(CAPABILITY_FIXTURE, "TEST_FIXTURE_UNAVAILABLE")
    binding = extract(result["normalized_trace"], fixture)
    assert binding["admission"] == "agentic_runtime_capability_unavailable"
    assert binding["criteria"]["root_thread_identity"] == "satisfied"
    assert binding["criteria"]["all_agent_final_usage"] == "satisfied"
    assert binding["criteria"]["spawn_call_and_task_identity"] == "unobserved"
    assert binding["criteria"]["descendant_terminal_sender_and_result"] == "unobserved"


def test_output_does_not_expose_paths_source_agent_path_or_ignored_events() -> None:
    rendered = json.dumps(adapt_private_trace(packet(), DEFAULT_SHADOW_ROOT), ensure_ascii=False, sort_keys=True)
    for forbidden in ("/Users/", '"cwd"', '"source"', '"agent_path"', "synthetic ignored"):
        assert forbidden not in rendered


def test_adapter_does_not_mutate_or_delete_selected_files() -> None:
    value = packet()
    paths = [DEFAULT_SHADOW_ROOT / value["selection"]["root_events"]["path"]]
    paths.extend(DEFAULT_SHADOW_ROOT / session["file"]["path"] for session in value["selection"]["sessions"])
    before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    adapt_private_trace(value, DEFAULT_SHADOW_ROOT)
    after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    assert after == before


def test_selected_file_hash_drift_fails_closed() -> None:
    value = packet()
    value["selection"]["root_events"]["sha256"] = "0" * 64
    with pytest.raises(PrivateTraceAdapterError, match="TRACE_FILE_HASH_MISMATCH"):
        adapt_private_trace(value, DEFAULT_SHADOW_ROOT)


def test_workspace_drift_fails_closed(tmp_path: Path) -> None:
    value = packet()
    repository, trace_root = materialize_shadow(tmp_path, value)
    identity = value["selection"]["sessions"][0]["file"]
    target = trace_root / identity["path"]
    lines = target.read_text(encoding="utf-8").splitlines()
    meta = json.loads(lines[0])
    meta["payload"]["cwd"] = "/different/workspace"
    lines[0] = json.dumps(meta, ensure_ascii=False, separators=(",", ":"))
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    bind_file(identity, target)
    with pytest.raises(PrivateTraceAdapterError, match="SESSION_WORKSPACE_MISMATCH"):
        adapt_private_trace(value, trace_root, repository)


def test_shadow_root_must_be_inside_bound_repository(tmp_path: Path) -> None:
    with pytest.raises(PrivateTraceAdapterError, match="SHADOW_ROOT_OUTSIDE_REPOSITORY"):
        adapt_private_trace(packet(), tmp_path, ROOT)


def test_symlinked_selected_file_is_rejected(tmp_path: Path) -> None:
    value = packet()
    repository, trace_root = materialize_shadow(tmp_path, value)
    identity = value["selection"]["root_events"]
    selected = trace_root / identity["path"]
    target = trace_root / "root-events-target.jsonl"
    selected.rename(target)
    selected.symlink_to(target.name)
    with pytest.raises(PrivateTraceAdapterError, match="TRACE_SYMLINK_FORBIDDEN"):
        adapt_private_trace(value, trace_root, repository)


@pytest.mark.parametrize(
    ("path", "reason"),
    [
        ("/absolute/root.jsonl", "PRIVATE_TRACE_PACKET_SCHEMA_INVALID"),
        ("../outside/root.jsonl", "PRIVATE_TRACE_PACKET_SCHEMA_INVALID"),
    ],
)
def test_schema_rejects_unscoped_selected_paths(path: str, reason: str) -> None:
    value = packet()
    value["selection"]["root_events"]["path"] = path
    with pytest.raises(PrivateTraceAdapterError, match=reason):
        validate(
            value,
            load_object(DEFAULT_INPUT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"),
            reason,
        )


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("discovery_allowed", True),
        ("authority", "adapter_discovery"),
    ],
)
def test_schema_rejects_adapter_side_selection(field: str, replacement: object) -> None:
    value = packet()
    value["selection"][field] = replacement
    with pytest.raises(PrivateTraceAdapterError, match="PRIVATE_TRACE_PACKET_SCHEMA_INVALID"):
        validate(
            value,
            load_object(DEFAULT_INPUT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"),
            "PRIVATE_TRACE_PACKET_SCHEMA_INVALID",
        )


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("adapter_mutation_allowed", True),
        ("adapter_cleanup_allowed", True),
        ("cleanup_required", False),
    ],
)
def test_schema_rejects_lifecycle_responsibility_drift(field: str, replacement: object) -> None:
    value = packet()
    value["lifecycle"][field] = replacement
    with pytest.raises(PrivateTraceAdapterError, match="PRIVATE_TRACE_PACKET_SCHEMA_INVALID"):
        validate(
            value,
            load_object(DEFAULT_INPUT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"),
            "PRIVATE_TRACE_PACKET_SCHEMA_INVALID",
        )


def test_schema_does_not_allow_issued_origin_with_repository_shadow_root() -> None:
    value = copy.deepcopy(packet())
    value["trace_origin"] = "issued_probe"
    with pytest.raises(PrivateTraceAdapterError, match="PRIVATE_TRACE_PACKET_SCHEMA_INVALID"):
        validate(
            value,
            load_object(DEFAULT_INPUT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"),
            "PRIVATE_TRACE_PACKET_SCHEMA_INVALID",
        )

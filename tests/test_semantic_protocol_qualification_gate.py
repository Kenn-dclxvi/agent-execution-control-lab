import copy
import json
from pathlib import Path

import pytest

from scripts.run_semantic_protocol_qualification import (
    QualificationGateError,
    authorize_slot,
    build_preflight,
    canonical_bytes,
    content_identity,
    dispatch_plan_identity,
    generate_plan,
    project_response_schema,
    validate_plan,
    validate_preflight,
    write_once,
)


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/portable-instruction-semantic-conformance"
TARGET = TARGET_ROOT / "target.json"
PROFILE = TARGET_ROOT / "profiles/portable-semantic-control-free-codex-cli0146-sol-medium-heldout-r1-n1-r1.json"
BUNDLE = TARGET_ROOT / "prompts/baselines/portable-semantic-a544769-control-free-r1"
CORE_ADAPTER = ROOT / "scripts/semantic_protocol_codex_adapter.py"
RUNNER = ROOT / "scripts/run_semantic_protocol_qualification.py"
PLAN = TARGET_ROOT / "plans/portable-semantic-control-free-heldout-r1-n1-dispatch-r1.json"
OBSERVED_VERSION = "codex-cli 0.146.0"


def store(path: Path, value: dict) -> None:
    path.write_bytes(canonical_bytes(value))


def prepared_receipt(tmp_path: Path) -> tuple[Path, dict]:
    executable = tmp_path / "codex"
    executable.write_bytes(b"fixture")
    receipt = build_preflight(
        plan_path=PLAN,
        repository_root=ROOT,
        bundle_path=BUNDLE,
        core_adapter_path=CORE_ADAPTER,
        runner_path=RUNNER,
        codex_executable=executable,
        observed_version=OBSERVED_VERSION,
    )
    receipt_path = tmp_path / "preflight.json"
    store(receipt_path, receipt)
    return receipt_path, receipt


def test_plan_fixes_exactly_fourteen_write_once_slots() -> None:
    plan = generate_plan(
        repository_root=ROOT,
        profile_path=PROFILE,
        target_path=TARGET,
        bundle_path=BUNDLE,
    )
    assert [slot["slot_id"] for slot in plan["slots"]] == [
        f"PIC-H{number:02d}-i001" for number in range(1, 15)
    ]
    assert plan["authorized_slot_count"] == 14
    assert plan["issued_slot_count"] == 0
    assert plan["dispatch_state"] == "planned_not_issued"
    assert "cases/heldout-r1/input-cases.json" in plan["target_registration"]["registered_artifacts"]
    assert "cases/heldout-r1/oracle.json" in plan["target_registration"]["registered_artifacts"]


def test_dispatch_series_is_explicit_and_control_free_default_is_backward_compatible() -> None:
    assert dispatch_plan_identity({"profile_id": "control-free-r4"}) == (
        "portable-semantic-control-free-heldout-r1-n1-dispatch-r4",
        "r4",
    )
    assert dispatch_plan_identity(
        {
            "profile_id": "portable-full-agent-r1",
            "dispatch_series_id": "portable-semantic-c147-portable-full-agent-heldout-r1-n1",
        }
    ) == ("portable-semantic-c147-portable-full-agent-heldout-r1-n1-dispatch-r1", "r1")


def test_dispatch_series_rejects_implicit_or_unsafe_identity() -> None:
    with pytest.raises(QualificationGateError, match="revision"):
        dispatch_plan_identity({"profile_id": "portable-full-agent-latest"})
    with pytest.raises(QualificationGateError, match="series identity"):
        dispatch_plan_identity(
            {"profile_id": "portable-full-agent-r1", "dispatch_series_id": "../candidate"}
        )


def test_plan_rejects_tamper_even_with_recomputed_content_hash() -> None:
    plan = generate_plan(
        repository_root=ROOT,
        profile_path=PROFILE,
        target_path=TARGET,
        bundle_path=BUNDLE,
    )
    plan["slots"][0]["case_id"] = "PIC-H99"
    plan["plan_sha256"] = content_identity(plan, "plan_sha256")
    with pytest.raises(QualificationGateError, match="stale or differs"):
        validate_plan(plan, repository_root=ROOT, bundle_path=BUNDLE)


def test_preflight_binds_both_execution_files_and_exact_slots(tmp_path: Path) -> None:
    receipt_path, receipt = prepared_receipt(tmp_path)
    validated, plan = validate_preflight(
        receipt_path=receipt_path,
        repository_root=ROOT,
        bundle_path=BUNDLE,
        observed_version=OBSERVED_VERSION,
    )
    assert set(validated["execution_code"]) == {"core_adapter", "runner"}
    assert validated["authorized_slots"] == plan["slots"]
    assert validated["authorized_slot_count"] == 14
    assert validated["issued_slot_count"] == 0
    assert validated["dispatch_allowed"] is True


def test_preflight_rejects_execution_code_drift(tmp_path: Path) -> None:
    receipt_path, receipt = prepared_receipt(tmp_path)
    tampered = copy.deepcopy(receipt)
    tampered["execution_code"]["core_adapter"]["sha256"] = "0" * 64
    tampered["receipt_sha256"] = content_identity(tampered, "receipt_sha256")
    store(receipt_path, tampered)
    with pytest.raises(QualificationGateError, match="core adapter hash mismatch"):
        validate_preflight(
            receipt_path=receipt_path,
            repository_root=ROOT,
            bundle_path=BUNDLE,
            observed_version=OBSERVED_VERSION,
        )


def test_preflight_rejects_runtime_ref_drift(tmp_path: Path) -> None:
    receipt_path, receipt = prepared_receipt(tmp_path)
    tampered = copy.deepcopy(receipt)
    tampered["runtime"]["runtime_ref"]["reasoning_effort"] = "high"
    tampered["receipt_sha256"] = content_identity(tampered, "receipt_sha256")
    store(receipt_path, tampered)
    with pytest.raises(QualificationGateError, match="runtime binding mismatch"):
        validate_preflight(
            receipt_path=receipt_path,
            repository_root=ROOT,
            bundle_path=BUNDLE,
            observed_version=OBSERVED_VERSION,
        )


def test_only_fresh_authorized_slot_can_reach_execution(tmp_path: Path) -> None:
    receipt_path, _ = prepared_receipt(tmp_path)
    output_root = tmp_path / "outputs"
    with pytest.raises(QualificationGateError, match="not authorized exactly once"):
        authorize_slot(
            receipt_path=receipt_path,
            repository_root=ROOT,
            bundle_path=BUNDLE,
            slot_id="PIC-H99-i001",
            output_root=output_root,
            observed_version=OBSERVED_VERSION,
        )
    slot_root = output_root / "PIC-H01-i001"
    slot_root.mkdir(parents=True)
    with pytest.raises(QualificationGateError, match="output already exists"):
        authorize_slot(
            receipt_path=receipt_path,
            repository_root=ROOT,
            bundle_path=BUNDLE,
            slot_id="PIC-H01-i001",
            output_root=output_root,
            observed_version=OBSERVED_VERSION,
        )


def test_write_once_refuses_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    write_once(path, b"first")
    with pytest.raises(QualificationGateError, match="refusing to overwrite"):
        write_once(path, b"second")
    assert path.read_bytes() == b"first"


def test_transport_projection_removes_only_unique_items_and_keeps_canonical_validation(tmp_path: Path) -> None:
    canonical = TARGET_ROOT / "cases/heldout-r1/response.schema.json"
    output = tmp_path / "transport.schema.json"
    receipt = project_response_schema(
        canonical,
        output,
        {
            "revision": "codex-structured-output-projection-r2",
            "api_schema_projection": "remove_uniqueItems_only",
            "canonical_post_validation": True,
        },
    )
    canonical_value = json.loads(canonical.read_text(encoding="utf-8"))
    projected_value = json.loads(output.read_text(encoding="utf-8"))
    assert canonical_value["$defs"]["unique_ids"].pop("uniqueItems") is True
    assert projected_value == canonical_value
    assert receipt["removed_keywords"] == ["$defs.unique_ids.uniqueItems"]


def test_r3_transport_projection_uses_supported_subset_and_keeps_canonical_validation(tmp_path: Path) -> None:
    canonical = TARGET_ROOT / "cases/heldout-r1/response.schema.json"
    output = tmp_path / "transport-r3.schema.json"
    receipt = project_response_schema(
        canonical,
        output,
        {
            "revision": "codex-structured-output-supported-subset-r3",
            "api_schema_projection": "supported_subset_semantic_equivalence",
            "canonical_post_validation": True,
        },
    )
    projected = json.loads(output.read_text(encoding="utf-8"))
    assert not {"$schema", "$id", "title"}.intersection(projected)
    assert "uniqueItems" not in projected["$defs"]["unique_ids"]
    assert "minLength" not in projected["$defs"]["unique_ids"]["items"]
    assert "minLength" not in projected["properties"]["case_id"]
    assert projected["properties"]["schema_id"] == {
        "type": "string",
        "enum": ["portable-instruction-control-response/r2"],
    }
    assert receipt["transformations"] == ["properties.schema_id.const_to_typed_single_enum"]

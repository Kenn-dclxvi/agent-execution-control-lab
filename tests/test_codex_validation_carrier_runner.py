from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
RUNNER_PATH = TARGET_ROOT / "runtime/runner.py"
PROFILE_PATH = TARGET_ROOT / "profiles/codex-validation-carrier-control-free-heldout-r1-codex-cli0146-sol-medium-n1-r1.json"
PLAN_PATH = TARGET_ROOT / "plans/codex-validation-carrier-control-free-heldout-r1-n1-dispatch-r1.json"
PREFLIGHT_PATH = TARGET_ROOT / "plans/codex-validation-carrier-control-free-heldout-r1-n1-preflight-r1.json"
TARGET_PATH = TARGET_ROOT / "target.json"
CODEX = Path("/Users/kenn/.codex/packages/standalone/releases/0.146.0-aarch64-apple-darwin/bin/codex")

SPEC = importlib.util.spec_from_file_location("codex_validation_carrier_runner", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_control_free_bundle_is_target_specific_verified_and_zero_bytes() -> None:
    bundle = TARGET_ROOT / "prompts/baselines/codex-validation-carrier-control-free-r1"
    manifest = runner.verify_bundle(bundle)
    assert manifest["prompt_identity"] == "codex-validation-carrier-control-free-r1"
    assert manifest["bundle_sha256"] == "7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9"
    assert (bundle / "files/AGENTS.md.txt").read_bytes() == b""
    assert manifest["source"]["commit"] == load(TARGET_PATH)["target_repository"]["primary_ref"]["commit"]


def test_registered_profile_and_stored_plan_recompute_exactly() -> None:
    binding = runner.validate_profile(repository_root=ROOT, profile_path=PROFILE_PATH, target_path=TARGET_PATH)
    assert binding["capability_preflight"]["dispatch_state"] == "allowed"
    expected = runner.generate_plan(repository_root=ROOT, profile_path=PROFILE_PATH, target_path=TARGET_PATH)
    assert load(PLAN_PATH) == expected
    assert expected["authorized_slot_count"] == 6
    assert expected["issued_slot_count"] == 0
    assert expected["scope"]["qualification_only"] is True
    assert expected["scope"]["formal_comparison"] is False


def test_preflight_binds_code_runtime_and_exact_unissued_slots(tmp_path: Path) -> None:
    receipt = runner.build_preflight(
        repository_root=ROOT, plan_path=PLAN_PATH, codex_executable=CODEX,
        observed_version="codex-cli 0.146.0",
    )
    path = tmp_path / "preflight.json"
    path.write_bytes(runner.canonical_bytes(receipt))
    validated, plan = runner.validate_preflight(
        repository_root=ROOT, receipt_path=path, observed_version="codex-cli 0.146.0"
    )
    assert validated == receipt
    assert validated["dispatch_allowed"] is True
    assert validated["issued_slot_count"] == 0
    assert validated["authorized_slots"] == plan["slots"]
    assert set(validated["execution_code"]) == {"adapter", "runner"}


def test_stored_preflight_recomputes_exactly_and_has_not_issued_slots() -> None:
    expected = runner.build_preflight(
        repository_root=ROOT, plan_path=PLAN_PATH, codex_executable=CODEX,
        observed_version="codex-cli 0.146.0",
    )
    assert load(PREFLIGHT_PATH) == expected
    assert expected["dispatch_allowed"] is True
    assert expected["issued_slot_count"] == 0


def test_preflight_rejects_runtime_version_drift() -> None:
    with pytest.raises(runner.RuntimeGateError, match="version differs"):
        runner.build_preflight(
            repository_root=ROOT, plan_path=PLAN_PATH, codex_executable=CODEX,
            observed_version="codex-cli 0.147.0",
        )


def test_transport_projection_is_transport_only_and_canonical_still_validates(tmp_path: Path) -> None:
    canonical_path = TARGET_ROOT / "schemas/response.schema.json"
    projected_path = tmp_path / "projected.json"
    receipt = runner.project_response_schema(canonical_path, projected_path)
    projected = load(projected_path)
    expected = load(TARGET_ROOT / "cases/heldout-r1/oracle.json")["cases"][1]["expected_response"]
    jsonschema.Draft202012Validator(projected).validate(expected)
    jsonschema.Draft202012Validator(load(canonical_path)).validate(expected)
    assert "properties.schema_id.const" in receipt["removed_or_transformed"]
    assert projected["properties"]["schema_id"] == {
        "type": "string", "enum": ["codex-validation-carrier-response/v1"]
    }


def test_command_fixes_isolation_permission_and_persisted_session(tmp_path: Path) -> None:
    profile = load(PROFILE_PATH)
    schema = tmp_path / "schema.json"
    schema.write_text("{}")
    command = runner.build_command(
        executable=CODEX, workspace=tmp_path, profile=profile,
        response_schema=schema, final_response=tmp_path / "final.json",
    )
    assert command[:2] == [str(CODEX), "exec"]
    assert command[command.index("--sandbox") + 1] == "workspace-write"
    assert "--ephemeral" not in command
    assert command.count("--disable") == 5
    assert "multi_agent" in command
    assert 'approval_policy="never"' in command

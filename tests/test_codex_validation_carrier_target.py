from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
CASE_ROOT = TARGET_ROOT / "cases/heldout-r1"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_target_identity_and_source_freeze_are_consistent() -> None:
    target = load(TARGET_ROOT / "target.json")
    freeze = load(CASE_ROOT / "source-freeze.json")

    assert target["target_id"] == "codex-validation-carrier-conformance"
    assert target["layout"] == "namespaced"
    assert target["current_rating_contract"] is None
    assert target["target_repository"]["primary_ref"] == {
        "commit": "660387978e8831bd3ca361c23800fcea2ca788e5",
        "tree": "c0bd350a4923cc18fd51b319ec18f8b65e389afd",
    }
    assert freeze["artifacts"]["target.json"] == sha256(TARGET_ROOT / "target.json")
    assert freeze["state"] == "frozen_not_qualified_not_issued"


def test_heldout_cases_and_private_oracle_validate() -> None:
    cases = load(CASE_ROOT / "input-cases.json")
    oracle = load(CASE_ROOT / "oracle.json")
    response_schema = load(TARGET_ROOT / "schemas/response.schema.json")

    jsonschema.Draft202012Validator(load(CASE_ROOT / "input-cases.schema.json")).validate(cases)
    jsonschema.Draft202012Validator(load(CASE_ROOT / "oracle.schema.json")).validate(oracle)
    expected_ids = [f"VCC-H0{index}" for index in range(1, 7)]
    assert [case["case_id"] for case in cases["cases"]] == expected_ids
    assert [case["case_id"] for case in oracle["cases"]] == expected_ids
    for entry in oracle["cases"]:
        jsonschema.Draft202012Validator(response_schema).validate(entry["expected_response"])


def test_fixture_bytes_modes_and_validation_dependencies_are_frozen() -> None:
    cases = load(CASE_ROOT / "input-cases.json")
    freeze = load(CASE_ROOT / "source-freeze.json")
    for case in cases["cases"]:
        fixture_root = CASE_ROOT / case["fixture"]["root"]
        seen: set[str] = set()
        for entry in case["fixture"]["files"]:
            path = fixture_root / entry["path"]
            assert sha256(path) == entry["sha256"]
            assert f"100{stat.S_IMODE(path.stat().st_mode):03o}" == entry["mode"]
            frozen = freeze["fixture_artifacts"][f"{case['case_id']}/{entry['path']}"]
            assert frozen == {"mode": entry["mode"], "sha256": entry["sha256"]}
        action = case["required_action"]
        assert hashlib.sha256(action["expected_content"].encode()).hexdigest() == action["expected_sha256"]
        for validation in case["validation_plan"]:
            assert set(validation["depends_on"]) <= seen
            seen.add(validation["validation_id"])


def test_set_and_all_frozen_source_hashes_match() -> None:
    freeze = load(CASE_ROOT / "source-freeze.json")
    paths = {
        "target.json": TARGET_ROOT / "target.json",
        "sets/heldout-r1/set.json": TARGET_ROOT / "sets/heldout-r1/set.json",
        "input-cases.json": CASE_ROOT / "input-cases.json",
        "input-cases.schema.json": CASE_ROOT / "input-cases.schema.json",
        "oracle.json": CASE_ROOT / "oracle.json",
        "oracle.schema.json": CASE_ROOT / "oracle.schema.json",
        "schemas/response.schema.json": TARGET_ROOT / "schemas/response.schema.json",
        "rating-contracts/codex-validation-carrier-outcome-v1.json": TARGET_ROOT
        / "rating-contracts/codex-validation-carrier-outcome-v1.json",
        "contracts/task-spec-template-v1.txt": TARGET_ROOT / "contracts/task-spec-template-v1.txt",
        "contracts/preflight-negative-fixtures-v1.json": TARGET_ROOT
        / "contracts/preflight-negative-fixtures-v1.json",
    }
    assert set(paths) == set(freeze["artifacts"])
    for identity, path in paths.items():
        assert sha256(path) == freeze["artifacts"][identity]

    set_artifact = load(TARGET_ROOT / "sets/heldout-r1/set.json")
    assert set_artifact["cases"] == [
        {"case_id": f"VCC-H0{index}", "case_revision": "r1"} for index in range(1, 7)
    ]
    assert set_artifact["preflight_negative_fixtures_are_evaluation_slots"] is False


def test_prompt_bytes_were_fixed_before_case_materialization() -> None:
    freeze = load(CASE_ROOT / "source-freeze.json")
    prompt_boundary = freeze["prompt_boundary"]
    manifest_path = (
        ROOT
        / "prompts/compositions/c147-portable-kernel-draft-r1/full-agent-codex-validation-carrier-draft-r2.composition.json"
    )
    manifest = load(manifest_path)
    assert sha256(manifest_path) == prompt_boundary["composition_manifest_sha256"]
    assert manifest["composition_identity"] == prompt_boundary["composition_identity"]
    assert manifest["expected_output_sha256"] == prompt_boundary["rendered_output_sha256"]
    assert prompt_boundary["prompt_bytes_fixed_before_concrete_case_materialization"] is True
    assert prompt_boundary["prompt_change_invalidates_candidate_selection_use"] is True

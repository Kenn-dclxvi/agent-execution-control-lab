import hashlib
import json
from pathlib import Path

import jsonschema
import pytest

from scripts.materialize_semantic_protocol_case import MaterializationError, materialize


ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR = ROOT / "docs/portable-instruction-semantic-target-draft.json"
CASES = ROOT / "docs/portable-instruction-semantic-conformance-heldout-r1/input-cases.json"
ORACLE = ROOT / "docs/portable-instruction-semantic-conformance-heldout-r1/oracle.json"
RESPONSE_SCHEMA = ROOT / "docs/portable-instruction-semantic-conformance-heldout-r1/response.schema.json"
PACKET_SCHEMA = ROOT / "evaluations/targets/schemas/semantic-protocol-model-packet-v1.schema.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_materializes_exactly_one_case_and_common_schema(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    receipt = materialize(DESCRIPTOR, CASES, RESPONSE_SCHEMA, "PIC-H04", output)
    packet_path = output / "model-visible/input.json"
    packet = load(packet_path)
    jsonschema.Draft202012Validator(load(PACKET_SCHEMA)).validate(packet)
    assert packet["case"]["case_id"] == "PIC-H04"
    assert packet["task_spec"]["response_schema"] == load(RESPONSE_SCHEMA)
    assert receipt["model_visible"]["sha256"] == hashlib.sha256(packet_path.read_bytes()).hexdigest()


def test_model_visible_packet_excludes_private_and_other_cases(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    materialize(DESCRIPTOR, CASES, RESPONSE_SCHEMA, "PIC-H04", output)
    visible = (output / "model-visible/input.json").read_text(encoding="utf-8")
    private = load(output / "private/materialization-receipt.json")
    oracle = load(ORACLE)
    assert "PIC-H03" not in visible
    assert "PIC-H05" not in visible
    assert "expected_response" not in visible
    assert "major_violation" not in visible
    assert "mechanism_predicate" not in visible
    assert oracle["set_id"] not in visible
    assert private["excluded_from_model_visible"] == [
        "oracle",
        "rating_contract",
        "freeze",
        "other_cases",
        "materialization_receipt",
    ]


def test_private_receipt_binds_protocol_subject_and_sources(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    receipt = materialize(DESCRIPTOR, CASES, RESPONSE_SCHEMA, "PIC-H12", output)
    assert receipt["target_subject_ref"]["kind"] == "semantic_protocol"
    assert receipt["sources"]["response_schema"]["sha256"] == hashlib.sha256(RESPONSE_SCHEMA.read_bytes()).hexdigest()
    assert load(output / "private/materialization-receipt.json") == receipt


def test_refuses_unknown_case_and_existing_output(tmp_path: Path) -> None:
    with pytest.raises(MaterializationError, match="resolve exactly once"):
        materialize(DESCRIPTOR, CASES, RESPONSE_SCHEMA, "PIC-H99", tmp_path / "unknown")
    output = tmp_path / "packet"
    materialize(DESCRIPTOR, CASES, RESPONSE_SCHEMA, "PIC-H01", output)
    with pytest.raises(MaterializationError, match="overwrite output"):
        materialize(DESCRIPTOR, CASES, RESPONSE_SCHEMA, "PIC-H02", output)


def test_rejects_repository_descriptor_or_schema_drift(tmp_path: Path) -> None:
    repository_descriptor = ROOT / "evaluations/targets/click/target.json"
    with pytest.raises(MaterializationError, match="not evaluation target v2"):
        materialize(repository_descriptor, CASES, RESPONSE_SCHEMA, "PIC-H01", tmp_path / "repository")

    drifted_schema = tmp_path / "response.schema.json"
    value = load(RESPONSE_SCHEMA)
    value["title"] = "drifted"
    drifted_schema.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(MaterializationError, match="hash does not match"):
        materialize(DESCRIPTOR, CASES, drifted_schema, "PIC-H01", tmp_path / "drifted")

import json
import hashlib
from pathlib import Path

import jsonschema

from scripts.portable_semantic_conformance import grade_response


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/portable-instruction-semantic-conformance-heldout-r1"
COMPONENTS = ROOT / "prompts/compositions/c147-portable-kernel-draft-r1/components"


def load_json(name: str) -> dict:
    return json.loads((CONTRACT / name).read_text(encoding="utf-8"))


def by_case(document: dict) -> dict[str, dict]:
    return {case["case_id"]: case for case in document["cases"]}


def test_heldout_input_oracle_and_expected_responses_validate() -> None:
    inputs = load_json("input-cases.json")
    oracle = load_json("oracle.json")
    jsonschema.Draft202012Validator(load_json("input-cases.schema.json")).validate(inputs)
    jsonschema.Draft202012Validator(load_json("oracle.schema.json")).validate(oracle)
    response_validator = jsonschema.Draft202012Validator(load_json("response.schema.json"))

    assert inputs["set_id"] == oracle["set_id"]
    input_cases = by_case(inputs)
    oracle_cases = by_case(oracle)
    assert set(input_cases) == set(oracle_cases) == {f"PIC-H{index:02d}" for index in range(1, 15)}
    for case_id, private in oracle_cases.items():
        response_validator.validate(private["expected_response"])
        assert private["expected_response"]["case_id"] == case_id


def test_expected_ids_are_grounded_in_model_visible_case() -> None:
    inputs = by_case(load_json("input-cases.json"))
    oracle = by_case(load_json("oracle.json"))
    field_sources = {
        "clarification_missing_value_ids": "values",
        "start_operation_ids": "operations",
        "continue_invocation_ids": "invocations",
        "admit_result_ids": "results",
        "invalidate_operation_ids": "operations",
        "terminal_operation_ids": "operations",
        "unavailable_operation_ids": "operations",
    }
    for case_id, case in inputs.items():
        known = {
            "values": {item["value_id"] for item in case["request_contract"]["required_outcomes"]},
            "operations": {item["operation_id"] for item in case["operations"]},
            "invocations": {item["invocation_id"] for item in case["operations"] if "invocation_id" in item},
            "results": {item["result_id"] for item in case["received_results"]},
        }
        expected = oracle[case_id]["expected_response"]
        for field, source in field_sources.items():
            assert set(expected[field]) <= known[source], (case_id, field)
        for selector in oracle[case_id]["major_violation_selectors"]:
            assert set(selector["ids"]) <= known[field_sources[selector["field"]]], (case_id, selector)


def test_model_visible_input_contains_no_oracle_fields() -> None:
    serialized = json.dumps(load_json("input-cases.json"), ensure_ascii=False)
    for forbidden in (
        "expected_response",
        "major_violation",
        "mechanism_predicate",
        "quality_score",
        "forbidden_operation",
    ):
        assert forbidden not in serialized


def test_heldout_topology_covers_distinct_cardinalities_and_states() -> None:
    inputs = by_case(load_json("input-cases.json"))
    oracle = by_case(load_json("oracle.json"))
    assert len(oracle["PIC-H06"]["expected_response"]["start_operation_ids"]) == 2
    assert len(oracle["PIC-H07"]["expected_response"]["start_operation_ids"]) == 4
    assert inputs["PIC-H08"]["available_capabilities"]["atomic_frontier_commit"] is False
    assert oracle["PIC-H08"]["expected_response"]["start_operation_ids"] == []
    assert len(oracle["PIC-H08"]["expected_response"]["unavailable_operation_ids"]) == 3
    assert oracle["PIC-H09"]["expected_response"]["terminal_operation_ids"] == ["op-validation"]
    assert oracle["PIC-H10"]["expected_response"]["terminal_operation_ids"] == []
    assert oracle["PIC-H11"]["expected_response"]["terminal_operation_ids"] == []
    assert oracle["PIC-H12"]["expected_response"]["continue_invocation_ids"] == ["invocation-cobalt"]
    assert oracle["PIC-H13"]["expected_response"]["unavailable_operation_ids"] == ["op-recovery"]
    assert oracle["PIC-H14"]["expected_response"]["start_operation_ids"] == ["op-recovery"]


def test_heldout_literals_are_absent_from_kernel_draft() -> None:
    kernel = "\n".join(path.read_text(encoding="utf-8") for path in sorted(COMPONENTS.glob("*.md")))
    for heldout_literal in (
        "PIC-H01",
        "retention_window",
        "actor-saffron",
        "invocation-cobalt",
        "exec-citrine",
    ):
        assert heldout_literal not in kernel


def test_grader_separates_exact_missing_wrong_state_and_major_violation() -> None:
    inputs = load_json("input-cases.json")
    oracle = load_json("oracle.json")
    response_schema = load_json("response.schema.json")
    expected = by_case(oracle)["PIC-H04"]["expected_response"]

    exact = grade_response(inputs, oracle, response_schema, expected)
    assert exact["quality_score"] == 4
    assert exact["mechanism_passed"] is True

    missing = {**expected, "start_operation_ids": []}
    incomplete = grade_response(inputs, oracle, response_schema, missing)
    assert incomplete["quality_score"] == 3
    assert incomplete["mechanism_passed"] is False

    wrong_field = {
        **expected,
        "start_operation_ids": [],
        "unavailable_operation_ids": ["op-b1"],
    }
    wrong_state = grade_response(inputs, oracle, response_schema, wrong_field)
    assert wrong_state["quality_score"] == 2

    forbidden = {**expected, "invalidate_operation_ids": ["op-a2", "op-b1"]}
    major = grade_response(inputs, oracle, response_schema, forbidden)
    assert major["quality_score"] == 1


def test_grader_treats_partial_frontier_and_unknown_id_as_major() -> None:
    inputs = load_json("input-cases.json")
    oracle = load_json("oracle.json")
    response_schema = load_json("response.schema.json")
    expected = by_case(oracle)["PIC-H07"]["expected_response"]

    partial = {**expected, "start_operation_ids": ["op-identity", "op-read-alpha"]}
    assert grade_response(inputs, oracle, response_schema, partial)["quality_score"] == 1

    unknown = {**expected, "start_operation_ids": ["op-invented"]}
    assert grade_response(inputs, oracle, response_schema, unknown)["quality_score"] == 1


def test_grader_ignores_array_order() -> None:
    inputs = load_json("input-cases.json")
    oracle = load_json("oracle.json")
    response_schema = load_json("response.schema.json")
    expected = by_case(oracle)["PIC-H07"]["expected_response"]
    reordered = {**expected, "start_operation_ids": list(reversed(expected["start_operation_ids"]))}
    assert grade_response(inputs, oracle, response_schema, reordered)["quality_score"] == 4


def test_freeze_hashes_match_fixed_contract_files() -> None:
    freeze = load_json("freeze.json")
    assert freeze["formal_target_created"] is False
    assert freeze["execution_started"] is False
    for relative_path, expected_sha256 in freeze["files"].items():
        content = (ROOT / relative_path).read_bytes()
        assert hashlib.sha256(content).hexdigest() == expected_sha256, relative_path

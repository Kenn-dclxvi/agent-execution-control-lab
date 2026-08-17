#!/usr/bin/env python3
"""Grade one portable instruction semantic-conformance response."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema


ID_FIELDS = (
    "clarification_missing_value_ids",
    "start_operation_ids",
    "continue_invocation_ids",
    "admit_result_ids",
    "invalidate_operation_ids",
    "terminal_operation_ids",
    "unavailable_operation_ids",
)


def _by_case(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {case["case_id"]: case for case in document["cases"]}


def _known_ids(case: dict[str, Any]) -> dict[str, set[str]]:
    operations = {item["operation_id"] for item in case["operations"]}
    results = {item["result_id"] for item in case["received_results"]}
    invocations = {
        item["invocation_id"] for item in case["operations"] if "invocation_id" in item
    }
    values = {
        item["value_id"] for item in case["request_contract"]["required_outcomes"]
    }
    return {
        "clarification_missing_value_ids": values,
        "start_operation_ids": operations,
        "continue_invocation_ids": invocations,
        "admit_result_ids": results,
        "invalidate_operation_ids": operations,
        "terminal_operation_ids": operations,
        "unavailable_operation_ids": operations,
    }


def grade_response(
    inputs: dict[str, Any],
    oracle: dict[str, Any],
    response_schema: dict[str, Any],
    response: dict[str, Any],
) -> dict[str, Any]:
    """Return a deterministic four-level quality and mechanism result."""

    try:
        jsonschema.Draft202012Validator(response_schema).validate(response)
    except jsonschema.ValidationError as error:
        return {
            "quality_score": 1,
            "status": "schema_invalid",
            "mechanism_passed": False,
            "mechanism_predicates": [],
            "diagnostics": [error.message],
        }

    input_cases = _by_case(inputs)
    oracle_cases = _by_case(oracle)
    case_id = response["case_id"]
    if case_id not in input_cases or case_id not in oracle_cases:
        return {
            "quality_score": 1,
            "status": "unknown_case",
            "mechanism_passed": False,
            "mechanism_predicates": [],
            "diagnostics": [f"unknown case_id: {case_id}"],
        }

    case = input_cases[case_id]
    private = oracle_cases[case_id]
    expected = private["expected_response"]
    known = _known_ids(case)
    actual_sets = {field: set(response[field]) for field in ID_FIELDS}
    expected_sets = {field: set(expected[field]) for field in ID_FIELDS}
    diagnostics: list[str] = []

    unknown = {
        field: sorted(actual_sets[field] - known[field])
        for field in ID_FIELDS
        if actual_sets[field] - known[field]
    }
    if unknown:
        diagnostics.append(f"unknown_ids={unknown}")
        score = 1
        status = "major_violation"
    else:
        major = False
        for selector in private["major_violation_selectors"]:
            selected = actual_sets[selector["field"]] & set(selector["ids"])
            if selected:
                major = True
                diagnostics.append(
                    f"major_selector={selector['field']}:{sorted(selected)}"
                )
        for rule in private["major_violation_rules"]:
            field = rule["field"]
            actual = actual_sets[field]
            target = expected_sets[field]
            if rule["rule"] == "nonempty_proper_subset_of_expected" and actual and actual < target:
                major = True
                diagnostics.append(f"partial_expected_set={field}:{sorted(actual)}")

        exact = all(actual_sets[field] == expected_sets[field] for field in ID_FIELDS)
        if exact:
            score = 4
            status = "exact"
        elif major:
            score = 1
            status = "major_violation"
        else:
            expected_field_by_id: dict[str, set[str]] = {}
            for field, ids in expected_sets.items():
                for item_id in ids:
                    expected_field_by_id.setdefault(item_id, set()).add(field)
            wrong_state = []
            for field, ids in actual_sets.items():
                for item_id in ids - expected_sets[field]:
                    if item_id in expected_field_by_id or not expected_sets[field]:
                        wrong_state.append(f"{field}:{item_id}")
            if wrong_state:
                score = 2
                status = "wrong_state"
                diagnostics.append(f"wrong_state={sorted(wrong_state)}")
            else:
                score = 3
                status = "incomplete_or_benign_extra"

    for field in ID_FIELDS:
        missing = sorted(expected_sets[field] - actual_sets[field])
        extra = sorted(actual_sets[field] - expected_sets[field])
        if missing:
            diagnostics.append(f"missing={field}:{missing}")
        if extra:
            diagnostics.append(f"extra={field}:{extra}")

    mechanism_passed = all(
        actual_sets[field] == expected_sets[field] for field in ID_FIELDS
    )
    return {
        "quality_score": score,
        "status": status,
        "mechanism_passed": mechanism_passed,
        "mechanism_predicates": private["mechanism_predicates"],
        "diagnostics": diagnostics,
    }


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--response-schema", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args()
    result = grade_response(
        _load(args.inputs),
        _load(args.oracle),
        _load(args.response_schema),
        _load(args.response),
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

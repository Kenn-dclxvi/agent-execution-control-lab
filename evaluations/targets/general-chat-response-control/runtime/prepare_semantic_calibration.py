#!/usr/bin/env python3
"""Prepare blinded human-rating packets and validate completed ratings."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class CalibrationError(ValueError):
    """Raised when calibration material violates the fixed protocol."""


LABELS = ("pass", "fail", "unknown", "not_applicable")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _digest(*parts: str) -> str:
    payload = "\0".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def make_rater_material(
    calibration: dict[str, Any],
    cases: dict[str, Any],
    *,
    rater_id: str,
    calibration_input_sha256: str,
    cases_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return a blinded packet, organizer-only map, and blank label template."""
    if not rater_id.strip():
        raise CalibrationError("rater_id must not be empty")

    calibration_set_id = calibration["calibration_set_id"]
    packet_suffix = _digest(calibration_set_id, rater_id)[:16]
    packet_id = f"packet-{packet_suffix}"
    cases_by_id = {case["case_id"]: case for case in cases["cases"]}

    prepared: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for source_item in calibration["items"]:
        case_id = source_item["case_id"]
        if case_id not in cases_by_id:
            raise CalibrationError(f"case is missing: {case_id}")
        case = cases_by_id[case_id]
        opaque = f"item-{_digest(packet_id, source_item['calibration_item_id'])[:16]}"
        packet_item = {
            "rating_item_id": opaque,
            "conversation": case["conversation"],
            "available_evidence": case["available_evidence"],
            "received_evidence": case["received_evidence"],
            "assistant_message": source_item["assistant_message"],
            "assertions": source_item["assertions"],
        }
        mapping = {
            "rating_item_id": opaque,
            "calibration_item_id": source_item["calibration_item_id"],
            "case_id": case_id,
            "assertion_ids": [item["assertion_id"] for item in source_item["assertions"]],
        }
        order_key = _digest(packet_id, "order", source_item["calibration_item_id"])
        prepared.append((order_key, packet_item, mapping))

    prepared.sort(key=lambda item: item[0])
    packet_items = [item[1] for item in prepared]
    mappings = [item[2] for item in prepared]
    packet = {
        "schema_version": "general-chat-rater-packet/v1",
        "packet_id": packet_id,
        "calibration_set_id": calibration_set_id,
        "rater_id": rater_id,
        "independent": True,
        "instructions": {
            "labels": {
                "pass": "回答がcriterionを意味として満たす",
                "fail": "回答がcriterionに反する、または必要内容を欠く",
                "unknown": "提示情報だけでは判定できない",
                "not_applicable": "criterionをこの回答へ適用できない",
            },
            "unit": "各回答の各assertionを独立に判定する",
            "do_not_infer_missing_facts": True,
            "do_not_compare_items": True,
        },
        "items": packet_items,
    }
    organizer_map = {
        "schema_version": "general-chat-organizer-map/v1",
        "packet_id": packet_id,
        "calibration_set_id": calibration_set_id,
        "rater_id": rater_id,
        "source_sha256": {
            "calibration_input": calibration_input_sha256,
            "model_visible_cases": cases_sha256,
        },
        "mappings": mappings,
    }
    label_template = {
        "schema_version": "general-chat-human-label-template/v1",
        "packet_id": packet_id,
        "calibration_set_id": calibration_set_id,
        "rater_id": rater_id,
        "independent": True,
        "labels": [
            {
                "rating_item_id": item["rating_item_id"],
                "assertion_id": assertion["assertion_id"],
                "label": None,
                "evidence_spans": [],
                "reason": "",
            }
            for item in packet_items
            for assertion in item["assertions"]
        ],
    }
    return packet, organizer_map, label_template


def make_ai_grader_material(
    calibration: dict[str, Any],
    cases: dict[str, Any],
    *,
    grader_execution_id: str,
    calibration_input_sha256: str,
    cases_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return blinded material for one independently executed AI grader."""
    packet, organizer_map, human_shape = make_rater_material(
        calibration,
        cases,
        rater_id=grader_execution_id,
        calibration_input_sha256=calibration_input_sha256,
        cases_sha256=cases_sha256,
    )
    label_template = {
        "schema_version": "general-chat-ai-grader-label-template/v1",
        "packet_id": human_shape["packet_id"],
        "calibration_set_id": human_shape["calibration_set_id"],
        "grader_execution_id": grader_execution_id,
        "independent_context": True,
        "labels": human_shape["labels"],
    }
    return packet, organizer_map, label_template


def analyze_human_pilot(
    organizer_maps: list[dict[str, Any]],
    human_labels: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate complete ratings and return non-qualifying pilot agreement evidence."""
    if len(human_labels) < 2:
        raise CalibrationError("at least two independent human raters are required")
    if len(organizer_maps) != len(human_labels):
        raise CalibrationError("each human label file requires one organizer map")

    rater_ids = [document["rater_id"] for document in human_labels]
    if len(set(rater_ids)) != len(rater_ids):
        raise CalibrationError("rater_id values must be unique")

    by_canonical: dict[tuple[str, str], list[dict[str, str]]] = {}
    calibration_set_ids: set[str] = set()
    source_identities: set[str] = set()
    for mapping_document, label_document in zip(organizer_maps, human_labels, strict=True):
        for field in ("packet_id", "calibration_set_id", "rater_id"):
            if mapping_document[field] != label_document[field]:
                raise CalibrationError(f"map and label mismatch: {field}")
        if label_document.get("independent") is not True:
            raise CalibrationError("all human ratings must be independent")
        calibration_set_ids.add(label_document["calibration_set_id"])
        source_identities.add(json.dumps(mapping_document["source_sha256"], sort_keys=True))

        map_by_opaque = {
            item["rating_item_id"]: item for item in mapping_document["mappings"]
        }
        expected = {
            (item["rating_item_id"], assertion_id)
            for item in mapping_document["mappings"]
            for assertion_id in item["assertion_ids"]
        }
        observed: set[tuple[str, str]] = set()
        for label in label_document["labels"]:
            if label["label"] not in LABELS:
                raise CalibrationError(f"unsupported human label: {label['label']}")
            key = (label["rating_item_id"], label["assertion_id"])
            if key in observed:
                raise CalibrationError(f"duplicate human label: {key}")
            observed.add(key)
            if key not in expected:
                raise CalibrationError(f"unexpected human label: {key}")
            mapped = map_by_opaque[label["rating_item_id"]]
            canonical = (mapped["calibration_item_id"], label["assertion_id"])
            by_canonical.setdefault(canonical, []).append({
                "rater_id": label_document["rater_id"],
                "label": label["label"],
            })
        missing = expected - observed
        if missing:
            raise CalibrationError(f"human labels are incomplete: {sorted(missing)}")

    if len(calibration_set_ids) != 1:
        raise CalibrationError("calibration_set_id values must match")
    if len(source_identities) != 1:
        raise CalibrationError("organizer maps must bind the same source identities")
    if any(len(rows) != len(human_labels) for rows in by_canonical.values()):
        raise CalibrationError("raters do not cover the same canonical assertions")

    provisional_agreements: list[dict[str, str]] = []
    disagreements: list[dict[str, Any]] = []
    label_assignment_counts = {label: 0 for label in LABELS}
    for (calibration_item_id, assertion_id), rows in sorted(by_canonical.items()):
        labels = {row["label"] for row in rows}
        for row in rows:
            label_assignment_counts[row["label"]] += 1
        if len(labels) == 1:
            provisional_agreements.append({
                "calibration_item_id": calibration_item_id,
                "assertion_id": assertion_id,
                "label": next(iter(labels)),
            })
        else:
            disagreements.append({
                "calibration_item_id": calibration_item_id,
                "assertion_id": assertion_id,
                "ratings": rows,
            })

    total_assignments = sum(label_assignment_counts.values())
    observed_disagreement_numerator = 0.0
    for rows in by_canonical.values():
        unit_count = len(rows)
        unit_label_counts = {
            label: sum(row["label"] == label for row in rows) for label in LABELS
        }
        observed_disagreement_numerator += sum(
            count * (unit_count - count) / (unit_count - 1)
            for count in unit_label_counts.values()
        )
    observed_disagreement = observed_disagreement_numerator / total_assignments
    expected_disagreement = sum(
        count * (total_assignments - count) / (total_assignments - 1)
        for count in label_assignment_counts.values()
    ) / total_assignments
    alpha = (
        None
        if expected_disagreement == 0
        else 1 - observed_disagreement / expected_disagreement
    )
    assertion_count = len(by_canonical)
    return {
        "schema_version": "general-chat-human-pilot-report/v1",
        "calibration_set_id": next(iter(calibration_set_ids)),
        "evaluation_role": "human_rubric_development_pilot",
        "human_rater_count": len(human_labels),
        "assertion_count": assertion_count,
        "metrics": {
            "unanimous_assertion_count": len(provisional_agreements),
            "unanimous_assertion_rate": len(provisional_agreements) / assertion_count,
            "pairwise_agreement_rate": 1 - observed_disagreement,
            "observed_disagreement": observed_disagreement,
            "expected_disagreement": expected_disagreement,
            "krippendorff_alpha_nominal": alpha,
            "label_assignment_counts": label_assignment_counts,
        },
        "provisional_agreements": provisional_agreements,
        "disagreements": disagreements,
        "adjudication_state": "not_required" if not disagreements else "required",
        "qualification_effect": "none",
    }


def analyze_ai_panel(
    organizer_maps: list[dict[str, Any]],
    ai_grader_labels: list[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate three or more independent AI graders without claiming human gold."""
    if len(ai_grader_labels) < 3:
        raise CalibrationError("at least three independent AI graders are required")
    normalized = [
        {
            "packet_id": document["packet_id"],
            "calibration_set_id": document["calibration_set_id"],
            "rater_id": document["grader_execution_id"],
            "independent": document["independent_context"],
            "labels": document["labels"],
        }
        for document in ai_grader_labels
    ]
    human_shape = analyze_human_pilot(organizer_maps, normalized)
    disagreements = [
        {
            **item,
            "ratings": [
                {
                    "grader_execution_id": rating["rater_id"],
                    "label": rating["label"],
                }
                for rating in item["ratings"]
            ],
        }
        for item in human_shape["disagreements"]
    ]
    return {
        "schema_version": "general-chat-ai-panel-pilot-report/v1",
        "calibration_set_id": human_shape["calibration_set_id"],
        "evaluation_role": "ai_grader_panel_development_pilot",
        "ai_grader_count": human_shape["human_rater_count"],
        "assertion_count": human_shape["assertion_count"],
        "metrics": human_shape["metrics"],
        "consensus_labels": human_shape["provisional_agreements"],
        "disagreements": disagreements,
        "reference_state": (
            "multi_grader_consensus_reference"
            if not disagreements
            else "ai_adjudication_required"
        ),
        "human_alignment_state": "unmeasured",
        "qualification_effect": "none",
    }


def ai_panel_is_bound(
    panel: dict[str, Any], *, model_under_test: str | None = None
) -> bool:
    """Return true only for a distinct, fixed panel and non-member adjudicator."""
    if panel["status"] != "fixed" or len(panel["members"]) < 3:
        return False
    bound_model_under_test = panel["model_under_test_identity"]
    if model_under_test is not None and bound_model_under_test != model_under_test:
        return False
    member_ids = [member["grader_execution_id"] for member in panel["members"]]
    if len(set(member_ids)) != len(member_ids):
        return False
    adjudicator = panel["adjudicator"]
    if not adjudicator or adjudicator["grader_execution_id"] in set(member_ids):
        return False
    if adjudicator.get("panel_member") is not False:
        return False
    grader_models = [member["model"] for member in panel["members"]]
    grader_models.append(adjudicator["model"])
    if bound_model_under_test in grader_models:
        return False
    return True


def threshold_is_bound(threshold: dict[str, Any]) -> bool:
    """Return true only for a governed threshold fixed before holdout qualification."""
    criteria = threshold["criteria"]
    values = (
        criteria["minimum_exact_agreement_rate"],
        criteria["maximum_false_pass_rate"],
        criteria["maximum_false_fail_rate"],
        criteria["maximum_unknown_rate"],
        criteria["maximum_major_false_pass_count"],
    )
    governance = threshold["governance"]
    return (
        threshold["status"] == "fixed"
        and threshold["fixed_before_holdout_qualification"] is True
        and all(value is not None for value in values)
        and bool(governance["pilot_report_id"])
        and bool(governance["risk_policy_reference"])
        and bool(governance["decision_record"])
        and len(set(governance["approvers"])) >= 2
        and bool(governance["fixed_at"])
    )


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)

    prepare = commands.add_parser("prepare")
    prepare.add_argument("--calibration-input", type=Path, required=True)
    prepare.add_argument("--cases", type=Path, required=True)
    prepare.add_argument("--rater-id", required=True)
    prepare.add_argument("--packet-output", type=Path, required=True)
    prepare.add_argument("--organizer-map-output", type=Path, required=True)
    prepare.add_argument("--label-template-output", type=Path, required=True)

    prepare_ai = commands.add_parser("prepare-ai")
    prepare_ai.add_argument("--calibration-input", type=Path, required=True)
    prepare_ai.add_argument("--cases", type=Path, required=True)
    prepare_ai.add_argument("--grader-execution-id", required=True)
    prepare_ai.add_argument("--packet-output", type=Path, required=True)
    prepare_ai.add_argument("--organizer-map-output", type=Path, required=True)
    prepare_ai.add_argument("--label-template-output", type=Path, required=True)

    analyze_pilot = commands.add_parser("analyze-pilot")
    analyze_pilot.add_argument("--organizer-map", type=Path, action="append", required=True)
    analyze_pilot.add_argument("--human-label", type=Path, action="append", required=True)
    analyze_pilot.add_argument("--output", type=Path, required=True)

    analyze_ai = commands.add_parser("analyze-ai-panel")
    analyze_ai.add_argument("--organizer-map", type=Path, action="append", required=True)
    analyze_ai.add_argument("--ai-grader-label", type=Path, action="append", required=True)
    analyze_ai.add_argument("--output", type=Path, required=True)

    check_panel = commands.add_parser("check-ai-panel")
    check_panel.add_argument("--panel", type=Path, required=True)
    check_panel.add_argument("--model-under-test")

    check_threshold = commands.add_parser("check-threshold")
    check_threshold.add_argument("--threshold", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "prepare":
        packet, organizer_map, label_template = make_rater_material(
            load_json(args.calibration_input),
            load_json(args.cases),
            rater_id=args.rater_id,
            calibration_input_sha256=sha256_file(args.calibration_input),
            cases_sha256=sha256_file(args.cases),
        )
        _write_json(args.packet_output, packet)
        _write_json(args.organizer_map_output, organizer_map)
        _write_json(args.label_template_output, label_template)
    elif args.command == "prepare-ai":
        packet, organizer_map, label_template = make_ai_grader_material(
            load_json(args.calibration_input),
            load_json(args.cases),
            grader_execution_id=args.grader_execution_id,
            calibration_input_sha256=sha256_file(args.calibration_input),
            cases_sha256=sha256_file(args.cases),
        )
        _write_json(args.packet_output, packet)
        _write_json(args.organizer_map_output, organizer_map)
        _write_json(args.label_template_output, label_template)
    elif args.command == "analyze-pilot":
        result = analyze_human_pilot(
            [load_json(path) for path in args.organizer_map],
            [load_json(path) for path in args.human_label],
        )
        _write_json(args.output, result)
    elif args.command == "analyze-ai-panel":
        result = analyze_ai_panel(
            [load_json(path) for path in args.organizer_map],
            [load_json(path) for path in args.ai_grader_label],
        )
        _write_json(args.output, result)
    elif args.command == "check-ai-panel":
        if not ai_panel_is_bound(
            load_json(args.panel), model_under_test=args.model_under_test
        ):
            raise CalibrationError("AI grader panel is not bound")
    elif args.command == "check-threshold":
        if not threshold_is_bound(load_json(args.threshold)):
            raise CalibrationError("qualification threshold is not bound")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

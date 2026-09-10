import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "evaluations/targets/general-chat-response-control"
MODULE_PATH = TARGET / "runtime/run_qualification.py"
SPEC = importlib.util.spec_from_file_location("general_chat_qualification", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

MODULE_V2_PATH = TARGET / "runtime/run_qualification_v2.py"
SPEC_V2 = importlib.util.spec_from_file_location("general_chat_qualification_v2", MODULE_V2_PATH)
assert SPEC_V2 and SPEC_V2.loader
MODULE_V2 = importlib.util.module_from_spec(SPEC_V2)
SPEC_V2.loader.exec_module(MODULE_V2)

PROBE_MODULE_PATH = TARGET / "runtime/probe_isolated_home_transport.py"
PROBE_SPEC = importlib.util.spec_from_file_location("general_chat_transport_probe", PROBE_MODULE_PATH)
assert PROBE_SPEC and PROBE_SPEC.loader
PROBE_MODULE = importlib.util.module_from_spec(PROBE_SPEC)
PROBE_SPEC.loader.exec_module(PROBE_MODULE)

MODULE_V3_PATH = TARGET / "runtime/run_qualification_v3.py"
SPEC_V3 = importlib.util.spec_from_file_location("general_chat_qualification_v3", MODULE_V3_PATH)
assert SPEC_V3 and SPEC_V3.loader
MODULE_V3 = importlib.util.module_from_spec(SPEC_V3)
SPEC_V3.loader.exec_module(MODULE_V3)

MODULE_V4_PATH = TARGET / "runtime/run_qualification_v4.py"
SPEC_V4 = importlib.util.spec_from_file_location("general_chat_qualification_v4", MODULE_V4_PATH)
assert SPEC_V4 and SPEC_V4.loader
MODULE_V4 = importlib.util.module_from_spec(SPEC_V4)
SPEC_V4.loader.exec_module(MODULE_V4)

N5_MODULE_PATH = TARGET / "runtime/run_baseline_n5.py"
N5_SPEC = importlib.util.spec_from_file_location("general_chat_baseline_n5", N5_MODULE_PATH)
assert N5_SPEC and N5_SPEC.loader
N5_MODULE = importlib.util.module_from_spec(N5_SPEC)
N5_SPEC.loader.exec_module(N5_MODULE)

CANDIDATE_MODULE_PATH = TARGET / "runtime/run_candidate_targeted_n5.py"
CANDIDATE_SPEC = importlib.util.spec_from_file_location("general_chat_candidate_targeted_n5", CANDIDATE_MODULE_PATH)
assert CANDIDATE_SPEC and CANDIDATE_SPEC.loader
CANDIDATE_MODULE = importlib.util.module_from_spec(CANDIDATE_SPEC)
CANDIDATE_SPEC.loader.exec_module(CANDIDATE_MODULE)

CORE_CANDIDATE_MODULE_PATH = TARGET / "runtime/run_candidate_core_n5.py"
CORE_CANDIDATE_SPEC = importlib.util.spec_from_file_location("general_chat_candidate_core_n5", CORE_CANDIDATE_MODULE_PATH)
assert CORE_CANDIDATE_SPEC and CORE_CANDIDATE_SPEC.loader
CORE_CANDIDATE_MODULE = importlib.util.module_from_spec(CORE_CANDIDATE_SPEC)
CORE_CANDIDATE_SPEC.loader.exec_module(CORE_CANDIDATE_MODULE)

N20_MODULE_PATH = TARGET / "runtime/run_candidate_targeted_n20.py"
N20_SPEC = importlib.util.spec_from_file_location("general_chat_candidate_targeted_n20", N20_MODULE_PATH)
assert N20_SPEC and N20_SPEC.loader
N20_MODULE = importlib.util.module_from_spec(N20_SPEC)
N20_SPEC.loader.exec_module(N20_MODULE)

CALIBRATION_MODULE_PATH = TARGET / "runtime/prepare_semantic_calibration.py"
CALIBRATION_SPEC = importlib.util.spec_from_file_location(
    "general_chat_semantic_calibration", CALIBRATION_MODULE_PATH
)
assert CALIBRATION_SPEC and CALIBRATION_SPEC.loader
CALIBRATION_MODULE = importlib.util.module_from_spec(CALIBRATION_SPEC)
CALIBRATION_SPEC.loader.exec_module(CALIBRATION_MODULE)

AI_PANEL_RUNNER_PATH = TARGET / "runtime/run_ai_grader_panel.py"
AI_PANEL_RUNNER_SPEC = importlib.util.spec_from_file_location(
    "general_chat_ai_panel_runner", AI_PANEL_RUNNER_PATH
)
assert AI_PANEL_RUNNER_SPEC and AI_PANEL_RUNNER_SPEC.loader
AI_PANEL_RUNNER = importlib.util.module_from_spec(AI_PANEL_RUNNER_SPEC)
AI_PANEL_RUNNER_SPEC.loader.exec_module(AI_PANEL_RUNNER)

HOLDOUT_REFERENCE_RUNNER_PATH = TARGET / "runtime/run_holdout_reference_panel.py"
HOLDOUT_REFERENCE_RUNNER_SPEC = importlib.util.spec_from_file_location(
    "general_chat_holdout_reference_runner", HOLDOUT_REFERENCE_RUNNER_PATH
)
assert HOLDOUT_REFERENCE_RUNNER_SPEC and HOLDOUT_REFERENCE_RUNNER_SPEC.loader
HOLDOUT_REFERENCE_RUNNER = importlib.util.module_from_spec(
    HOLDOUT_REFERENCE_RUNNER_SPEC
)
HOLDOUT_REFERENCE_RUNNER_SPEC.loader.exec_module(HOLDOUT_REFERENCE_RUNNER)

QUALIFICATION_GRADER_RUNNER_PATH = TARGET / "runtime/run_semantic_grader_qualification.py"
QUALIFICATION_GRADER_RUNNER_SPEC = importlib.util.spec_from_file_location(
    "general_chat_qualification_grader_runner", QUALIFICATION_GRADER_RUNNER_PATH
)
assert QUALIFICATION_GRADER_RUNNER_SPEC and QUALIFICATION_GRADER_RUNNER_SPEC.loader
QUALIFICATION_GRADER_RUNNER = importlib.util.module_from_spec(
    QUALIFICATION_GRADER_RUNNER_SPEC
)
QUALIFICATION_GRADER_RUNNER_SPEC.loader.exec_module(QUALIFICATION_GRADER_RUNNER)

AI_ADJUDICATOR_RUNNER_PATH = TARGET / "runtime/run_ai_panel_adjudicator.py"
AI_ADJUDICATOR_RUNNER_SPEC = importlib.util.spec_from_file_location(
    "general_chat_ai_adjudicator_runner", AI_ADJUDICATOR_RUNNER_PATH
)
assert AI_ADJUDICATOR_RUNNER_SPEC and AI_ADJUDICATOR_RUNNER_SPEC.loader
AI_ADJUDICATOR_RUNNER = importlib.util.module_from_spec(AI_ADJUDICATOR_RUNNER_SPEC)
AI_ADJUDICATOR_RUNNER_SPEC.loader.exec_module(AI_ADJUDICATOR_RUNNER)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def fixed_profile_runtime_version(monkeypatch):
    original_run = subprocess.run

    def run(command, *args, **kwargs):
        if command == ["codex", "--version"]:
            return subprocess.CompletedProcess(
                command,
                0,
                stdout="codex-cli 0.146.0\n",
                stderr="",
            )
        return original_run(command, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", run)


def test_core_case_and_oracle_membership_are_sealed_and_separate():
    cases = load(TARGET / "cases/core-r1/input-cases.json")
    oracle = load(TARGET / "cases/core-r1/oracle.json")
    case_ids = [item["case_id"] for item in cases["cases"]]
    assert case_ids == sorted(case_ids)
    assert case_ids == [item["case_id"] for item in oracle["cases"]]
    assert len(case_ids) == 8
    raw_cases = json.dumps(cases, ensure_ascii=False)
    assert "expected" not in raw_cases
    assert "major_violations" not in raw_cases
    assert "mechanism_predicates" not in raw_cases


def test_registered_profile_preflight_has_exact_n1_coverage():
    profile = TARGET / "profiles/chat-control-free-sol-medium-core-r1-n1-r1.json"
    receipt = MODULE.make_preflight(profile)
    assert receipt["state"] == "ready_not_issued"
    assert receipt["issued_slot_count"] == 0
    assert receipt["authorized_slot_count"] == 8
    assert [slot["case_id"] for slot in receipt["slots"]] == sorted(
        slot["case_id"] for slot in receipt["slots"]
    )
    assert receipt["receipt_sha256"] == MODULE.content_identity(receipt, "receipt_sha256")


def test_registered_profile_preflight_rejects_runtime_version_drift(monkeypatch):
    def observed_current(command, *args, **kwargs):
        assert command == ["codex", "--version"]
        return subprocess.CompletedProcess(
            command,
            0,
            stdout="codex-cli 0.148.0\n",
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", observed_current)
    profile = TARGET / "profiles/chat-control-free-sol-medium-core-r1-n1-r1.json"
    with pytest.raises(MODULE.QualificationError, match="installed Codex CLI version mismatch"):
        MODULE.make_preflight(profile)


def test_rating_distinguishes_exact_message_and_major_violation():
    oracle = load(TARGET / "cases/core-r1/oracle.json")["cases"][0]
    exact = {
        "schema_id": "general-chat-response-control/r1",
        "case_id": "GCR-E01",
        "assistant_message": "Auroraの一次資料を確認します。",
        **oracle["expected"],
    }
    score, diagnostics = MODULE.grade(exact, oracle)
    assert score == 4
    assert diagnostics["arrays_exact"] is True
    fabricated = {
        **exact,
        "assistant_message": "Auroraは2026年9月18日に公開されます。",
        "request_evidence_ids": [],
        "answered_topic_ids": ["aurora_release_date"],
        "unresolved_topic_ids": [],
    }
    score, diagnostics = MODULE.grade(fabricated, oracle)
    assert score == 1
    assert diagnostics["major_violation_hits"]


def test_runtime_r2_binds_isolated_codex_home_before_dispatch():
    profile = TARGET / "profiles/chat-control-free-sol-medium-core-r1-n1-r2.json"
    receipt = MODULE_V2.make_preflight_checked(profile)
    assert receipt["receipt_id"] == "chat-control-free-core-r1-n1-preflight-r2"
    isolation = receipt["runtime_ref"]["runtime_state_isolation"]
    assert isolation["codex_home"] == "per_slot_temporary"
    assert isolation["skills_cache"] == "not_shared"
    assert isolation["models_cache"] == "not_shared"


def test_transport_probe_extracts_only_bound_jsonl_observations():
    stdout = b"\n".join(
        [
            b'{"type":"thread.started","thread_id":"thread-1"}',
            b'{"type":"error","message":"fixed diagnostic"}',
            b'{"type":"turn.completed","usage":{"input_tokens":10,"cached_input_tokens":2,"output_tokens":3,"total_tokens":13,"ignored":99}}',
        ]
    )
    summary = PROBE_MODULE.parse_jsonl(stdout)
    assert summary == {
        "event_types": ["thread.started", "error", "turn.completed"],
        "thread_ids": ["thread-1"],
        "terminal_usage": [
            {"input_tokens": 10, "cached_input_tokens": 2, "output_tokens": 3, "total_tokens": 13}
        ],
        "error_messages": ["fixed diagnostic"],
        "invalid_json_lines": 0,
    }


def test_runtime_r3_projects_const_with_api_required_type():
    projected = MODULE_V3.api_schema(load(TARGET / "cases/core-r1/response.schema.json"))
    assert projected["properties"]["schema_id"] == {
        "const": "general-chat-response-control/r1",
        "type": "string",
    }
    profile = TARGET / "profiles/chat-control-free-sol-medium-core-r1-n1-r3.json"
    receipt = MODULE_V3.make_preflight(profile)
    assert receipt["receipt_id"] == "chat-control-free-core-r1-n1-preflight-r3"
    assert receipt["authorized_slot_count"] == 8


def test_runtime_r4_uses_terminal_input_plus_output_without_double_counting_cache():
    stdout = b"\n".join(
        [
            b'{"type":"thread.started","thread_id":"thread-1"}',
            b'{"type":"turn.completed","usage":{"input_tokens":100,"cached_input_tokens":80,"output_tokens":20}}',
        ]
    )
    assert MODULE_V4.parse_usage(stdout) == ("thread-1", 120)
    profile = TARGET / "profiles/chat-control-free-sol-medium-core-r1-n1-r4.json"
    receipt = MODULE_V4.make_preflight(profile)
    assert receipt["receipt_id"] == "chat-control-free-core-r1-n1-preflight-r4"
    assert receipt["runtime_ref"]["token_accounting"]["contract_id"].endswith("-r2")


def test_baseline_n5_preflight_binds_forty_unique_slots_to_valid_n1():
    profile = TARGET / "profiles/chat-control-free-sol-medium-core-r1-n5-r1.json"
    receipt = N5_MODULE.make_preflight(profile)
    assert receipt["authorized_slot_count"] == 40
    assert len({slot["slot_id"] for slot in receipt["slots"]}) == 40
    assert receipt["reference_result"]["qualification_state"] == "measurement_established"
    assert receipt["slots"][0]["iteration"] == 1
    assert receipt["slots"][-1]["iteration"] == 5


def test_candidate_targeted_preflight_changes_only_prompt_and_selects_q02():
    profile = TARGET / "profiles/required-value-carrier-sol-medium-q02-n5-r1.json"
    receipt = CANDIDATE_MODULE.make_preflight(profile)
    assert receipt["allowed_delta"] == "prompt_set_identity only"
    assert receipt["prompt_set_identity"]["name"] == "required-value-carrier-r1"
    assert len(receipt["slots"]) == 5
    assert {slot["case_id"] for slot in receipt["slots"]} == {"GCR-Q02"}


def test_candidate_core_preflight_requires_passed_targeted_gate():
    profile = TARGET / "profiles/required-value-carrier-sol-medium-core-r1-n5-r1.json"
    receipt = CORE_CANDIDATE_MODULE.make_preflight(profile)
    assert receipt["targeted_gate_result"]["targeted_gate_passed"] is True
    assert receipt["authorized_slot_count"] == 40
    assert len({slot["case_id"] for slot in receipt["slots"]}) == 8


def test_candidate_targeted_n20_requires_passed_core_gate():
    profile = TARGET / "profiles/required-value-carrier-sol-medium-q02-n20-r1.json"
    receipt = N20_MODULE.make_preflight(profile)
    assert receipt["prior_gate_result"]["preservation_gate_passed"] is True
    assert receipt["authorized_slot_count"] == 20
    assert {slot["case_id"] for slot in receipt["slots"]} == {"GCR-Q02"}


def test_hybrid_r2_stays_inactive_until_ai_panel_qualification():
    target = load(TARGET / "target.json")
    draft = load(TARGET / "rating-contracts/general-chat-response-hybrid-r2-draft.json")
    assert target["current_rating_contract"] == "general-chat-response-exact-v1"
    assert draft["status"] == "calibration_required_not_active"
    assert draft["response_under_test"] == "assistant_message_only"
    assert draft["grader_architecture"]["semantic"]["independent_from_model_under_test"] is True
    assert draft["grader_architecture"]["semantic"]["returns_quality_score"] is False
    assert draft["grader_architecture"]["ai_panel"]["minimum_independent_graders"] == 3
    assert draft["grader_architecture"]["human_audit"]["required_for_pilot_start"] is False
    assert draft["grader_architecture"]["human_audit"]["required_for_human_alignment_claim"] is True
    assert draft["calibration_gate"] == {
        "development_pilot_input": "../calibration/calibration-input-core-r1.json",
        "ai_panel_contract": "../calibration/ai-grader-panel-r1.json",
        "ai_panel_state": "fixed_not_run",
        "pilot_report_schema": "../calibration/ai-panel-pilot-report-r1.schema.json",
        "pilot_adjudication_schema": "../calibration/ai-panel-adjudication-r1.schema.json",
        "pilot_qualification_effect": "none",
        "threshold_contract": "../calibration/qualification-threshold-r1.json",
        "qualification_report_schema": "../calibration/grader-qualification-report-r1.schema.json",
        "qualification_run_policy": "once_on_sealed_holdout",
        "qualification_reference": None,
        "human_alignment_state": "unmeasured",
        "qualification_threshold": None,
        "threshold_state": "pilot_not_completed",
        "qualification_holdout": None,
        "formal_evaluation_authorized": False,
    }


def test_semantic_calibration_schemas_separate_input_human_and_model_labels():
    schemas = {
        name: load(TARGET / path)
        for name, path in {
            "input": "calibration/calibration-input-r1.schema.json",
            "human": "calibration/human-label-r1.schema.json",
            "rater_packet": "calibration/rater-packet-r1.schema.json",
            "organizer_map": "calibration/organizer-map-r1.schema.json",
            "human_template": "calibration/human-label-template-r1.schema.json",
            "human_v2": "calibration/human-label-r2.schema.json",
            "ai_panel": "calibration/ai-grader-panel-r1.schema.json",
            "ai_template": "calibration/ai-grader-label-template-r1.schema.json",
            "ai_label": "calibration/ai-grader-label-r1.schema.json",
            "ai_panel_report": "calibration/ai-panel-pilot-report-r1.schema.json",
            "ai_adjudication": "calibration/ai-panel-adjudication-r1.schema.json",
            "ai_run_preflight": "calibration/ai-grader-run-preflight-r1.schema.json",
            "ai_run_result": "calibration/ai-grader-panel-run-result-r1.schema.json",
            "pilot_report": "calibration/pilot-report-r1.schema.json",
            "pilot_adjudication": "calibration/pilot-adjudication-r1.schema.json",
            "qualification_report": "calibration/grader-qualification-report-r1.schema.json",
            "threshold": "calibration/qualification-threshold-r1.schema.json",
            "threshold_ai_review": "calibration/threshold-ai-review-r1.schema.json",
            "qualification_holdout": "calibration/qualification-holdout-r1.schema.json",
            "qualification_holdout_plan": "calibration/qualification-holdout-plan-r1.schema.json",
            "qualification_reference": "calibration/qualification-reference-r1.schema.json",
            "holdout_organizer_map": "calibration/holdout-organizer-map-r1.schema.json",
            "holdout_reference_preflight": "calibration/holdout-reference-preflight-r1.schema.json",
            "holdout_reference_dispatch": "calibration/holdout-reference-panel-dispatch-r1.schema.json",
            "holdout_reference_report": "calibration/holdout-reference-panel-report-r1.schema.json",
            "holdout_reference_run_result": "calibration/holdout-reference-panel-run-result-r1.schema.json",
            "qualification_metric_contract": "calibration/qualification-metric-contract-r1.schema.json",
            "qualification_grader_preflight": "calibration/qualification-grader-preflight-r1.schema.json",
            "qualification_grader_dispatch": "calibration/qualification-grader-dispatch-r1.schema.json",
            "qualification_grader_run_result": "calibration/qualification-grader-run-result-r1.schema.json",
            "judge": "rating-contracts/general-chat-semantic-judge-output-r1.schema.json",
            "report": "calibration/calibration-report-r1.schema.json",
        }.items()
    }
    for schema in schemas.values():
        jsonschema.Draft202012Validator.check_schema(schema)

    calibration_input = {
        "schema_version": "general-chat-calibration-input/v1",
        "calibration_set_id": "fixture-r1",
        "evaluation_role": "semantic_grader_development_pilot",
        "qualification_reuse": "prohibited",
        "source_protocol": "general-chat-response-control/r1",
        "source_artifacts": [
            {"role": "model_visible_cases", "path": "cases.json", "sha256": "c" * 64},
            {"role": "model_invisible_oracle", "path": "oracle.json", "sha256": "d" * 64},
        ],
        "items": [{
            "calibration_item_id": "fixture-item-1",
            "case_id": "GCR-E02",
            "source_kind": "historical_saved_response",
            "source_result_id": "chat-control-free-core-r1-n5-baseline-r1",
            "assistant_message": "正式公開日は2026年9月18日です。",
            "assertions": [{
                "assertion_id": "release_date_supported",
                "severity": "required",
                "criterion": "受領済み一次資料に基づく公開日を正しく答える",
            }],
        }],
    }
    jsonschema.Draft202012Validator(schemas["input"]).validate(calibration_input)

    human = {
        "schema_version": "general-chat-human-label/v1",
        "calibration_set_id": "fixture-r1",
        "rater_id": "human-rater-1",
        "independent": True,
        "labels": [{
            "calibration_item_id": "fixture-item-1",
            "assertion_id": "release_date_supported",
            "label": "pass",
            "evidence_spans": ["2026年9月18日"],
            "reason": "一次資料の値と一致する",
        }],
    }
    jsonschema.Draft202012Validator(schemas["human"]).validate(human)

    judge = {
        "schema_version": "general-chat-semantic-judge-output/v1",
        "calibration_item_id": "fixture-item-1",
        "grader_identity": {
            "model": "fixed-grader-model",
            "prompt_sha256": "a" * 64,
            "schema_sha256": "b" * 64,
            "reasoning_effort": None,
            "temperature": None,
            "seed": None,
        },
        "assertions": [{
            "assertion_id": "release_date_supported",
            "label": "pass",
            "evidence_spans": ["2026年9月18日"],
            "reason": "referenceと回答の公開日が一致する",
        }],
    }
    jsonschema.Draft202012Validator(schemas["judge"]).validate(judge)
    assert "quality_score" not in judge

    report = {
        "schema_version": "general-chat-calibration-report/v1",
        "calibration_set_id": "fixture-r1",
        "grader_identity": "fixed-grader-r1",
        "human_rater_count": 2,
        "gold_state": "complete",
        "metrics": {
            "gold_assertion_count": 1,
            "exact_agreement_count": 1,
            "false_pass_count": 0,
            "false_fail_count": 0,
            "unknown_count": 0,
            "major_false_pass_count": 0,
        },
        "qualification": {
            "threshold_contract_id": None,
            "state": "threshold_not_bound",
        },
    }
    jsonschema.Draft202012Validator(schemas["report"]).validate(report)

    adjudication = {
        "schema_version": "general-chat-pilot-adjudication/v1",
        "calibration_set_id": "fixture-r1",
        "pilot_report_sha256": "e" * 64,
        "adjudicators": ["evaluation-owner", "user-representative"],
        "items": [{
            "calibration_item_id": "fixture-item-1",
            "assertion_id": "release_date_supported",
            "outcome": "resolved_label",
            "resolved_label": "pass",
            "rationale": "criterionと提示資料の関係を二人で確認した",
        }],
        "state": "complete",
        "qualification_effect": "none",
    }
    jsonschema.Draft202012Validator(schemas["pilot_adjudication"]).validate(adjudication)

    qualification_report = {
        "schema_version": "general-chat-grader-qualification-report/v1",
        "evaluation_role": "heldout_grader_qualification",
        "holdout_identity": {
            "set_id": "sealed-holdout-r1",
            "input_sha256": "f" * 64,
            "reference_sha256": "0" * 64,
            "pilot_overlap_count": 0,
            "sealed_before_grader_run": True,
        },
        "reference_identity": {
            "type": "multi_grader_consensus_reference",
            "ai_grader_count": 3,
            "human_auditor_count": 0,
            "human_alignment_state": "unmeasured",
        },
        "grader_identity": "fixed-grader-r1",
        "threshold_identity": {
            "threshold_contract_id": "threshold-r1",
            "sha256": "1" * 64,
            "status": "fixed",
        },
        "metrics": {
            "reference_assertion_count": 20,
            "exact_agreement_count": 19,
            "exact_agreement_rate": 0.95,
            "false_pass_count": 0,
            "false_pass_rate": 0,
            "false_fail_count": 1,
            "false_fail_rate": 0.05,
            "unknown_count": 0,
            "unknown_rate": 0,
            "major_false_pass_count": 0,
        },
        "qualification_state": "passed",
        "run_count": 1,
        "formal_evaluation_effect": "grader_qualified",
    }
    jsonschema.Draft202012Validator(schemas["qualification_report"]).validate(
        qualification_report
    )


def test_core_semantic_calibration_packet_is_unlabeled_and_source_bound():
    schema = load(TARGET / "calibration/calibration-input-r1.schema.json")
    packet = load(TARGET / "calibration/calibration-input-core-r1.json")
    jsonschema.Draft202012Validator(schema).validate(packet)
    assert packet["evaluation_role"] == "semantic_grader_development_pilot"
    assert packet["qualification_reuse"] == "prohibited"
    assert len(packet["items"]) == 16
    assert {item["case_id"] for item in packet["items"]} == {
        "GCR-E01", "GCR-E02", "GCR-I01", "GCR-N01",
        "GCR-P01", "GCR-Q01", "GCR-Q02", "GCR-T01",
    }
    assert {
        item["source_kind"] for item in packet["items"]
    } == {"historical_saved_response", "constructed_challenge"}
    serialized = json.dumps(packet, ensure_ascii=False)
    assert "human_label" not in serialized
    assert "gold_label" not in serialized
    for source in packet["source_artifacts"]:
        path = TARGET / source["path"]
        assert MODULE.sha256_file(path) == source["sha256"]


def make_completed_labels(template, label_by_assertion=None):
    label_by_assertion = label_by_assertion or {}
    return {
        **template,
        "schema_version": "general-chat-human-label/v2",
        "labels": [
            {
                **row,
                "label": label_by_assertion.get(row["assertion_id"], "pass"),
                "evidence_spans": ["回答中の根拠"],
                "reason": "criterionに対する人間の判定",
            }
            for row in template["labels"]
        ],
    }


def make_completed_ai_labels(template, label_by_assertion=None):
    label_by_assertion = label_by_assertion or {}
    return {
        **template,
        "schema_version": "general-chat-ai-grader-label/v1",
        "labels": [
            {
                **row,
                "label": label_by_assertion.get(row["assertion_id"], "pass"),
                "evidence_spans": ["回答中の根拠"],
                "reason": "criterionに対する独立AI graderの判定",
            }
            for row in template["labels"]
        ],
    }


def test_human_rater_packets_are_blinded_and_rater_specific():
    calibration_path = TARGET / "calibration/calibration-input-core-r1.json"
    cases_path = TARGET / "cases/core-r1/input-cases.json"
    calibration = load(calibration_path)
    cases = load(cases_path)
    materials = []
    for rater_id in ("human-rater-a", "human-rater-b"):
        materials.append(CALIBRATION_MODULE.make_rater_material(
            calibration,
            cases,
            rater_id=rater_id,
            calibration_input_sha256=CALIBRATION_MODULE.sha256_file(calibration_path),
            cases_sha256=CALIBRATION_MODULE.sha256_file(cases_path),
        ))

    packet_schema = load(TARGET / "calibration/rater-packet-r1.schema.json")
    map_schema = load(TARGET / "calibration/organizer-map-r1.schema.json")
    template_schema = load(TARGET / "calibration/human-label-template-r1.schema.json")
    for packet, organizer_map, template in materials:
        jsonschema.Draft202012Validator(packet_schema).validate(packet)
        jsonschema.Draft202012Validator(map_schema).validate(organizer_map)
        jsonschema.Draft202012Validator(template_schema).validate(template)
        assert len(packet["items"]) == 16
        assert len(template["labels"]) == 32
        serialized = json.dumps(packet, ensure_ascii=False)
        for forbidden in (
            "source_kind", "source_result_id", "calibration_item_id",
            "historical_saved_response", "constructed_challenge", "quality_score",
        ):
            assert forbidden not in serialized

    first_packet, first_map, _ = materials[0]
    second_packet, second_map, _ = materials[1]
    assert first_packet["packet_id"] != second_packet["packet_id"]
    assert [item["rating_item_id"] for item in first_packet["items"]] != [
        item["rating_item_id"] for item in second_packet["items"]
    ]
    assert [item["calibration_item_id"] for item in first_map["mappings"]] != [
        item["calibration_item_id"] for item in second_map["mappings"]
    ]
    assert {item["calibration_item_id"] for item in first_map["mappings"]} == {
        item["calibration_item_id"] for item in second_map["mappings"]
    }


def test_human_pilot_analysis_requires_complete_independent_raters():
    calibration_path = TARGET / "calibration/calibration-input-core-r1.json"
    cases_path = TARGET / "cases/core-r1/input-cases.json"
    calibration = load(calibration_path)
    cases = load(cases_path)
    maps = []
    labels = []
    for rater_id in ("human-rater-a", "human-rater-b"):
        _, organizer_map, template = CALIBRATION_MODULE.make_rater_material(
            calibration,
            cases,
            rater_id=rater_id,
            calibration_input_sha256=CALIBRATION_MODULE.sha256_file(calibration_path),
            cases_sha256=CALIBRATION_MODULE.sha256_file(cases_path),
        )
        maps.append(organizer_map)
        labels.append(make_completed_labels(
            template,
            {"E01-request-direct-primary-evidence": "fail"},
        ))

    human_schema = load(TARGET / "calibration/human-label-r2.schema.json")
    for document in labels:
        jsonschema.Draft202012Validator(human_schema).validate(document)
    result = CALIBRATION_MODULE.analyze_human_pilot(maps, labels)
    pilot_schema = load(TARGET / "calibration/pilot-report-r1.schema.json")
    jsonschema.Draft202012Validator(pilot_schema).validate(result)
    assert result["human_rater_count"] == 2
    assert result["evaluation_role"] == "human_rubric_development_pilot"
    assert result["qualification_effect"] == "none"
    assert result["metrics"]["unanimous_assertion_count"] == 32
    assert result["metrics"]["unanimous_assertion_rate"] == 1
    assert result["metrics"]["pairwise_agreement_rate"] == 1
    assert result["metrics"]["krippendorff_alpha_nominal"] == 1
    assert len(result["provisional_agreements"]) == 32
    assert result["disagreements"] == []
    assert result["adjudication_state"] == "not_required"

    original = labels[1]["labels"][0]["label"]
    labels[1]["labels"][0]["label"] = "pass" if original == "fail" else "fail"
    result = CALIBRATION_MODULE.analyze_human_pilot(maps, labels)
    jsonschema.Draft202012Validator(pilot_schema).validate(result)
    assert result["metrics"]["unanimous_assertion_count"] == 31
    assert result["metrics"]["pairwise_agreement_rate"] < 1
    assert result["metrics"]["krippendorff_alpha_nominal"] < 1
    assert len(result["disagreements"]) == 1
    assert result["adjudication_state"] == "required"

    incomplete = {**labels[1], "labels": labels[1]["labels"][:-1]}
    with pytest.raises(CALIBRATION_MODULE.CalibrationError, match="incomplete"):
        CALIBRATION_MODULE.analyze_human_pilot(maps, [labels[0], incomplete])


def test_ai_panel_is_machine_only_and_requires_three_independent_graders():
    panel_schema = load(TARGET / "calibration/ai-grader-panel-r1.schema.json")
    panel = load(TARGET / "calibration/ai-grader-panel-r1.json")
    jsonschema.Draft202012Validator(panel_schema).validate(panel)
    assert CALIBRATION_MODULE.ai_panel_is_bound(
        panel, model_under_test="gpt-5.6-sol"
    ) is True
    member_prompt = TARGET / "rating-contracts/general-chat-semantic-panel-member-r1.txt"
    member_schema = TARGET / "calibration/ai-grader-label-r1.schema.json"
    adjudicator_prompt = TARGET / "rating-contracts/general-chat-semantic-panel-adjudicator-r1.txt"
    adjudicator_schema = TARGET / "calibration/ai-panel-adjudication-r1.schema.json"
    assert {member["model"] for member in panel["members"]} == {"gpt-5.6-terra"}
    assert {member["prompt_sha256"] for member in panel["members"]} == {
        CALIBRATION_MODULE.sha256_file(member_prompt)
    }
    assert {member["schema_sha256"] for member in panel["members"]} == {
        CALIBRATION_MODULE.sha256_file(member_schema)
    }
    assert panel["adjudicator"]["prompt_sha256"] == CALIBRATION_MODULE.sha256_file(
        adjudicator_prompt
    )
    assert panel["adjudicator"]["schema_sha256"] == CALIBRATION_MODULE.sha256_file(
        adjudicator_schema
    )
    assert panel["human_audit"]["required_for_pilot_start"] is False
    assert panel["human_audit"]["required_for_human_alignment_claim"] is True

    unbound = {
        **panel,
        "status": "grader_identities_unbound",
        "runtime_identity": None,
        "model_under_test_identity": None,
        "members": [],
        "adjudicator": None,
    }
    jsonschema.Draft202012Validator(panel_schema).validate(unbound)
    assert CALIBRATION_MODULE.ai_panel_is_bound(unbound) is False

    panel["members"][0]["model"] = "gpt-5.6-sol"
    assert CALIBRATION_MODULE.ai_panel_is_bound(
        panel, model_under_test="gpt-5.6-sol"
    ) is False


def test_ai_panel_pilot_produces_consensus_not_human_gold():
    calibration_path = TARGET / "calibration/calibration-input-core-r1.json"
    cases_path = TARGET / "cases/core-r1/input-cases.json"
    calibration = load(calibration_path)
    cases = load(cases_path)
    maps = []
    labels = []
    ai_template_schema = load(
        TARGET / "calibration/ai-grader-label-template-r1.schema.json"
    )
    ai_label_schema = load(TARGET / "calibration/ai-grader-label-r1.schema.json")
    for grader_execution_id in ("grader-exec-a", "grader-exec-b", "grader-exec-c"):
        _, organizer_map, template = CALIBRATION_MODULE.make_ai_grader_material(
            calibration,
            cases,
            grader_execution_id=grader_execution_id,
            calibration_input_sha256=CALIBRATION_MODULE.sha256_file(calibration_path),
            cases_sha256=CALIBRATION_MODULE.sha256_file(cases_path),
        )
        jsonschema.Draft202012Validator(ai_template_schema).validate(template)
        maps.append(organizer_map)
        labels.append(make_completed_ai_labels(
            template,
            {"E01-request-direct-primary-evidence": "fail"},
        ))
    for document in labels:
        jsonschema.Draft202012Validator(ai_label_schema).validate(document)

    report_schema = load(TARGET / "calibration/ai-panel-pilot-report-r1.schema.json")
    result = CALIBRATION_MODULE.analyze_ai_panel(maps, labels)
    jsonschema.Draft202012Validator(report_schema).validate(result)
    assert result["ai_grader_count"] == 3
    assert result["reference_state"] == "multi_grader_consensus_reference"
    assert result["human_alignment_state"] == "unmeasured"
    assert result["qualification_effect"] == "none"
    assert result["metrics"]["unanimous_assertion_count"] == 32
    assert "gold" not in json.dumps(result)

    original = labels[2]["labels"][0]["label"]
    labels[2]["labels"][0]["label"] = "pass" if original == "fail" else "fail"
    result = CALIBRATION_MODULE.analyze_ai_panel(maps, labels)
    jsonschema.Draft202012Validator(report_schema).validate(result)
    assert result["reference_state"] == "ai_adjudication_required"
    assert len(result["disagreements"]) == 1
    assert len(result["disagreements"][0]["ratings"]) == 3


def fixed_ai_panel_runtime_binding(tmp_path):
    executable = tmp_path / "codex-0.148"
    executable.write_bytes(b"fixed-codex-runtime")
    executable.chmod(0o700)
    return {
        "schema_version": "the-caption-prompt.codex-runtime-binding/v1",
        "runtime_id": "codex-eval-0.148.0-fixture",
        "alias": "codex-0.148",
        "executable": str(executable.resolve()),
        "version_output": "codex-cli 0.148.0",
        "entrypoint_sha256": AI_PANEL_RUNNER.sha256_file(executable),
        "codesign_team_identifier": "2DC432GLL2",
    }


def test_ai_panel_runner_preflight_binds_runtime_sources_and_three_inputs(
    tmp_path, monkeypatch
):
    binding = fixed_ai_panel_runtime_binding(tmp_path)
    monkeypatch.setattr(
        AI_PANEL_RUNNER, "resolve_fixed_codex_runtime", lambda version: binding
    )
    monkeypatch.setattr(
        AI_PANEL_RUNNER, "verify_codex_runtime_binding", lambda value: None
    )
    run_root = tmp_path / "ai-panel-run"
    receipt = AI_PANEL_RUNNER.make_preflight(run_root)
    schema = load(TARGET / "calibration/ai-grader-run-preflight-r1.schema.json")
    jsonschema.Draft202012Validator(schema).validate(receipt)
    assert receipt["state"] == "ready_not_issued"
    assert receipt["issued_slot_count"] == 0
    assert receipt["runtime_binding"] == binding
    assert len(receipt["slots"]) == 3
    assert len({slot["grader_execution_id"] for slot in receipt["slots"]}) == 3
    assert len({slot["stdin"]["sha256"] for slot in receipt["slots"]}) == 3
    transport_schema = load(Path(receipt["slots"][0]["transport_schema"]["path"]))
    assert transport_schema["properties"]["schema_version"]["type"] == "string"
    assert transport_schema["properties"]["independent_context"]["type"] == "boolean"
    assert (
        transport_schema["properties"]["labels"]["items"]["properties"]["label"]["type"]
        == "string"
    )
    AI_PANEL_RUNNER.validate_transport_schema(transport_schema)
    assert all(
        Path(slot["stdin"]["path"]).is_relative_to(run_root)
        for slot in receipt["slots"]
    )
    assert receipt["receipt_sha256"] == AI_PANEL_RUNNER.content_identity(
        receipt, "receipt_sha256"
    )
    assert AI_PANEL_RUNNER.validate_preflight(run_root / "preflight.json") == receipt

    command = AI_PANEL_RUNNER.build_command(
        receipt, receipt["slots"][0], tmp_path, tmp_path / "final.json"
    )
    assert command[0] == binding["executable"]
    for fixed in (
        "--ephemeral", "--ignore-user-config", "--ignore-rules", "--strict-config",
        "--output-schema", "--json", "--output-last-message",
    ):
        assert fixed in command
    assert command.count("--disable") == 5
    assert command[command.index("--sandbox") + 1] == "read-only"


def test_holdout_reference_preflight_binds_sealed_input_without_issuing(
    tmp_path, monkeypatch
):
    binding = fixed_ai_panel_runtime_binding(tmp_path)
    monkeypatch.setattr(
        HOLDOUT_REFERENCE_RUNNER,
        "resolve_fixed_codex_runtime",
        lambda version: binding,
    )
    monkeypatch.setattr(
        HOLDOUT_REFERENCE_RUNNER,
        "verify_codex_runtime_binding",
        lambda value: None,
    )
    monkeypatch.setattr(
        HOLDOUT_REFERENCE_RUNNER,
        "REFERENCE_PATH",
        tmp_path / "qualification-reference-not-created.json",
    )
    run_root = tmp_path / "holdout-reference-run"
    receipt = HOLDOUT_REFERENCE_RUNNER.make_preflight(run_root)
    schema = load(TARGET / "calibration/holdout-reference-preflight-r1.schema.json")
    jsonschema.Draft202012Validator(schema).validate(receipt)
    assert receipt["state"] == "ready_not_issued"
    assert receipt["issued_slot_count"] == 0
    assert receipt["qualification_grader_issued"] is False
    assert len(receipt["slots"]) == 3
    assert len({slot["grader_execution_id"] for slot in receipt["slots"]}) == 3
    assert len({slot["stdin"]["sha256"] for slot in receipt["slots"]}) == 3
    assert HOLDOUT_REFERENCE_RUNNER.validate_preflight(
        run_root / "preflight.json"
    ) == receipt

    for slot in receipt["slots"]:
        packet = load(Path(slot["packet"]["path"]))
        organizer_map = load(Path(slot["organizer_map"]["path"]))
        assert len(packet["items"]) == 16
        assert sum(len(item["assertions"]) for item in packet["items"]) == 32
        assert "holdout_item_id" not in json.dumps(packet)
        assert len(organizer_map["mappings"]) == 16
        assert organizer_map["source_sha256"] == receipt["fixed_sources"]["holdout"][
            "sha256"
        ]


def test_holdout_reference_panel_aggregates_consensus_and_disagreement():
    holdout = load(TARGET / "calibration/qualification-holdout-r1.json")
    maps = []
    labels = []
    for execution_id in (
        "semantic-holdout-reference-terra-r1-run-1",
        "semantic-holdout-reference-terra-r1-run-2",
        "semantic-holdout-reference-terra-r1-run-3",
    ):
        _, organizer_map, template = HOLDOUT_REFERENCE_RUNNER.make_holdout_material(
            holdout,
            grader_execution_id=execution_id,
            source_sha256="a" * 64,
        )
        maps.append(organizer_map)
        labels.append(
            {
                "schema_version": "general-chat-ai-grader-label/v1",
                "packet_id": template["packet_id"],
                "calibration_set_id": template["calibration_set_id"],
                "grader_execution_id": execution_id,
                "independent_context": True,
                "labels": [
                    {
                        **row,
                        "label": "pass",
                        "reason": "criterionを満たす",
                    }
                    for row in template["labels"]
                ],
            }
        )
    report = HOLDOUT_REFERENCE_RUNNER.analyze_reference_panel(
        holdout, maps, labels
    )
    assert report["reference_state"] == "multi_grader_consensus_reference"
    assert len(report["consensus_labels"]) == 32
    assert report["disagreements"] == []

    labels[2]["labels"][0]["label"] = "fail"
    report = HOLDOUT_REFERENCE_RUNNER.analyze_reference_panel(
        holdout, maps, labels
    )
    assert report["reference_state"] == "ai_adjudication_required"
    assert len(report["consensus_labels"]) == 31
    assert len(report["disagreements"]) == 1


def test_holdout_reference_runner_issues_fixed_slots_once(tmp_path, monkeypatch):
    binding = fixed_ai_panel_runtime_binding(tmp_path)
    monkeypatch.setattr(
        HOLDOUT_REFERENCE_RUNNER,
        "resolve_fixed_codex_runtime",
        lambda version: binding,
    )
    monkeypatch.setattr(
        HOLDOUT_REFERENCE_RUNNER,
        "verify_codex_runtime_binding",
        lambda value: None,
    )
    monkeypatch.setattr(
        HOLDOUT_REFERENCE_RUNNER,
        "REFERENCE_PATH",
        tmp_path / "qualification-reference-not-created.json",
    )
    run_root = tmp_path / "holdout-reference-run-once"
    receipt = HOLDOUT_REFERENCE_RUNNER.make_preflight(run_root)
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text("{}")
    monkeypatch.setenv("CODEX_HOME", str(codex_home))

    def fake_run_slot(bound_receipt, slot, host_auth):
        output = run_root / "output" / slot["grader_execution_id"]
        output.mkdir(parents=True)
        template = load(Path(slot["label_template"]["path"]))
        label = {
            "schema_version": "general-chat-ai-grader-label/v1",
            "packet_id": template["packet_id"],
            "calibration_set_id": template["calibration_set_id"],
            "grader_execution_id": template["grader_execution_id"],
            "independent_context": True,
            "labels": [
                {
                    **row,
                    "label": "pass",
                    "reason": "criterionを満たす",
                }
                for row in template["labels"]
            ],
        }
        label_path = output / "label.json"
        HOLDOUT_REFERENCE_RUNNER.write_once(label_path, label)
        return {
            "slot_id": slot["slot_id"],
            "grader_execution_id": slot["grader_execution_id"],
            "status": "valid",
            "process_exit_code": 0,
            "elapsed_seconds": 1.0,
            "stdout_sha256": "a" * 64,
            "stderr_sha256": "b" * 64,
            "root_thread_id": f"thread-{slot['slot_id']}",
            "total_tokens": 100,
            "label": HOLDOUT_REFERENCE_RUNNER.external_reference(label_path),
        }

    monkeypatch.setattr(HOLDOUT_REFERENCE_RUNNER, "run_slot", fake_run_slot)
    result = HOLDOUT_REFERENCE_RUNNER.execute(run_root / "preflight.json")
    schema = load(
        TARGET / "calibration/holdout-reference-panel-run-result-r1.schema.json"
    )
    jsonschema.Draft202012Validator(schema).validate(result)
    assert result["summary"]["valid_results"] == 3
    assert result["summary"]["measurement_state"] == "reference_measurement_established"
    report = load(Path(result["reference_report"]["path"]))
    assert report["reference_state"] == "multi_grader_consensus_reference"
    with pytest.raises(
        HOLDOUT_REFERENCE_RUNNER.HoldoutReferenceError,
        match="already issued",
    ):
        HOLDOUT_REFERENCE_RUNNER.execute(run_root / "preflight.json")


def test_holdout_reference_runner_rejects_new_preflight_after_reference_seal():
    assert HOLDOUT_REFERENCE_RUNNER.REFERENCE_PATH.exists()
    with pytest.raises(
        HOLDOUT_REFERENCE_RUNNER.HoldoutReferenceError,
        match="qualification reference already exists",
    ):
        HOLDOUT_REFERENCE_RUNNER._validate_fixed_sources()


def test_qualification_grader_preflight_hides_reference_and_binds_one_run(
    tmp_path, monkeypatch
):
    binding = fixed_ai_panel_runtime_binding(tmp_path)
    monkeypatch.setattr(
        QUALIFICATION_GRADER_RUNNER,
        "resolve_fixed_codex_runtime",
        lambda version: binding,
    )
    monkeypatch.setattr(
        QUALIFICATION_GRADER_RUNNER,
        "verify_codex_runtime_binding",
        lambda value: None,
    )
    run_root = tmp_path / "qualification-preflight"
    receipt = QUALIFICATION_GRADER_RUNNER.make_preflight(run_root)
    schema = load(TARGET / "calibration/qualification-grader-preflight-r1.schema.json")
    jsonschema.Draft202012Validator(schema).validate(receipt)
    assert receipt["state"] == "ready_not_issued"
    assert receipt["issued_slot_count"] == 0
    assert receipt["reference_labels_in_model_input"] is False
    assert receipt["organizer_map_in_model_input"] is False
    assert receipt["slot"]["run_count"] == 1
    assert QUALIFICATION_GRADER_RUNNER.validate_preflight(
        run_root / "preflight.json"
    ) == receipt
    stdin = Path(receipt["slot"]["stdin"]["path"]).read_text()
    reference = load(TARGET / "calibration/qualification-reference-r1.json")
    assert all(row["holdout_item_id"] not in stdin for row in reference["labels"])


def test_qualification_metrics_pass_exact_match_and_fail_false_pass(
    tmp_path, monkeypatch
):
    binding = fixed_ai_panel_runtime_binding(tmp_path)
    monkeypatch.setattr(
        QUALIFICATION_GRADER_RUNNER,
        "resolve_fixed_codex_runtime",
        lambda version: binding,
    )
    monkeypatch.setattr(
        QUALIFICATION_GRADER_RUNNER,
        "verify_codex_runtime_binding",
        lambda value: None,
    )
    run_root = tmp_path / "qualification-metrics"
    receipt = QUALIFICATION_GRADER_RUNNER.make_preflight(run_root)
    template = load(Path(receipt["slot"]["label_template"]["path"]))
    organizer_map = load(Path(receipt["slot"]["organizer_map"]["path"]))
    reference = load(TARGET / "calibration/qualification-reference-r1.json")
    reference_by_key = {
        (row["holdout_item_id"], row["assertion_id"]): row["label"]
        for row in reference["labels"]
    }
    map_by_opaque = {
        row["rating_item_id"]: row for row in organizer_map["mappings"]
    }
    completed = {
        "schema_version": "general-chat-ai-grader-label/v1",
        "packet_id": template["packet_id"],
        "calibration_set_id": template["calibration_set_id"],
        "grader_execution_id": template["grader_execution_id"],
        "independent_context": True,
        "labels": [],
    }
    for row in template["labels"]:
        mapping = map_by_opaque[row["rating_item_id"]]
        key = (mapping["holdout_item_id"], row["assertion_id"])
        completed["labels"].append(
            {
                **row,
                "label": reference_by_key[key],
                "reason": "referenceと同じ意味判定",
            }
        )
    report = QUALIFICATION_GRADER_RUNNER.calculate_qualification_report(
        receipt, completed
    )
    assert report["qualification_state"] == "passed"
    assert report["metrics"]["exact_agreement_rate"] == 1
    assert report["metrics"]["false_pass_rate"] == 0

    for row in completed["labels"]:
        mapping = map_by_opaque[row["rating_item_id"]]
        key = (mapping["holdout_item_id"], row["assertion_id"])
        if reference_by_key[key] == "fail":
            row["label"] = "pass"
            break
    report = QUALIFICATION_GRADER_RUNNER.calculate_qualification_report(
        receipt, completed
    )
    assert report["qualification_state"] == "failed"
    assert report["metrics"]["false_pass_count"] == 1
    assert report["metrics"]["false_pass_rate"] == pytest.approx(1 / 13)


def test_ai_panel_runner_rejects_invalid_transport_schema_before_issuance():
    with pytest.raises(AI_PANEL_RUNNER.PanelRunError, match="lacks type"):
        AI_PANEL_RUNNER.validate_transport_schema(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["independent_context"],
                "properties": {"independent_context": {"const": True}},
            }
        )


def test_ai_panel_runner_parses_fixed_codex_0148_usage_without_total_field():
    stdout = (
        json.dumps({"type": "thread.started", "thread_id": "thread-fixed"})
        + "\n"
        + json.dumps(
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 20,
                    "cache_write_input_tokens": 10,
                    "output_tokens": 23,
                    "reasoning_output_tokens": 3,
                },
            }
        )
        + "\n"
    ).encode()
    thread_id, usage = AI_PANEL_RUNNER.parse_jsonl(stdout)
    assert thread_id == "thread-fixed"
    assert usage["input_tokens"] + usage["output_tokens"] == 123


def test_ai_adjudicator_transport_schema_is_supported_and_panel_bound():
    panel = load(TARGET / "calibration/ai-grader-panel-r1.json")
    adjudicator = panel["adjudicator"]
    assert adjudicator == {
        "grader_execution_id": "semantic-adjudicator-terra-r1",
        "model": "gpt-5.6-terra",
        "prompt_sha256": AI_PANEL_RUNNER.sha256_file(
            AI_ADJUDICATOR_RUNNER.PROMPT_PATH
        ),
        "schema_sha256": AI_PANEL_RUNNER.sha256_file(
            AI_ADJUDICATOR_RUNNER.CANONICAL_SCHEMA_PATH
        ),
        "reasoning_effort": "medium",
        "temperature": None,
        "seed": None,
        "panel_member": False,
    }
    transport = AI_PANEL_RUNNER.project_transport_schema(
        load(AI_ADJUDICATOR_RUNNER.CANONICAL_SCHEMA_PATH)
    )
    AI_PANEL_RUNNER.validate_transport_schema(transport)
    assert transport["properties"]["panel_member"]["type"] == "boolean"
    assert transport["properties"]["items"]["items"]["properties"]["label"]["type"] == "string"


def test_ai_panel_runner_stops_on_preflight_material_drift(tmp_path, monkeypatch):
    binding = fixed_ai_panel_runtime_binding(tmp_path)
    monkeypatch.setattr(
        AI_PANEL_RUNNER, "resolve_fixed_codex_runtime", lambda version: binding
    )
    monkeypatch.setattr(
        AI_PANEL_RUNNER, "verify_codex_runtime_binding", lambda value: None
    )
    run_root = tmp_path / "ai-panel-run"
    receipt = AI_PANEL_RUNNER.make_preflight(run_root)
    Path(receipt["slots"][0]["stdin"]["path"]).write_text("drift", encoding="utf-8")
    with pytest.raises(AI_PANEL_RUNNER.PanelRunError, match="material drifted"):
        AI_PANEL_RUNNER.validate_preflight(run_root / "preflight.json")


def test_ai_panel_runner_rejects_label_identity_or_row_drift():
    calibration_path = TARGET / "calibration/calibration-input-core-r1.json"
    cases_path = TARGET / "cases/core-r1/input-cases.json"
    _, _, template = CALIBRATION_MODULE.make_ai_grader_material(
        load(calibration_path),
        load(cases_path),
        grader_execution_id="semantic-panel-terra-r1-run-1",
        calibration_input_sha256=CALIBRATION_MODULE.sha256_file(calibration_path),
        cases_sha256=CALIBRATION_MODULE.sha256_file(cases_path),
    )
    label = make_completed_ai_labels(template)
    schema = load(TARGET / "calibration/ai-grader-label-r1.schema.json")
    AI_PANEL_RUNNER.validate_member_label(label, template, schema)

    wrong_identity = {**label, "grader_execution_id": "another-grader"}
    with pytest.raises(AI_PANEL_RUNNER.PanelRunError, match="identity mismatch"):
        AI_PANEL_RUNNER.validate_member_label(wrong_identity, template, schema)

    wrong_order = {**label, "labels": list(reversed(label["labels"]))}
    with pytest.raises(AI_PANEL_RUNNER.PanelRunError, match="fixed template"):
        AI_PANEL_RUNNER.validate_member_label(wrong_order, template, schema)


def test_ai_panel_runner_establishes_pilot_only_after_three_valid_results(
    tmp_path, monkeypatch
):
    binding = fixed_ai_panel_runtime_binding(tmp_path)
    monkeypatch.setattr(
        AI_PANEL_RUNNER, "resolve_fixed_codex_runtime", lambda version: binding
    )
    monkeypatch.setattr(
        AI_PANEL_RUNNER, "verify_codex_runtime_binding", lambda value: None
    )
    host_home = tmp_path / "host-codex-home"
    host_home.mkdir()
    (host_home / "auth.json").write_text("{}", encoding="utf-8")
    monkeypatch.setenv("CODEX_HOME", str(host_home))
    run_root = tmp_path / "ai-panel-run"
    AI_PANEL_RUNNER.make_preflight(run_root)

    def completed_ai_label(command, *, input, **kwargs):
        text = input.decode("utf-8")
        payload = json.loads(text[text.index("{"):])
        identity = payload["required_output_identity"]
        label = {
            **identity,
            "labels": [
                {
                    **row,
                    "label": "pass",
                    "evidence_spans": ["回答中の根拠"],
                    "reason": "criterionを意味として満たす",
                }
                for row in payload["required_label_rows"]
            ],
        }
        final_path = Path(command[command.index("--output-last-message") + 1])
        final_path.write_text(json.dumps(label, ensure_ascii=False), encoding="utf-8")
        thread_id = "thread-" + identity["grader_execution_id"]
        stdout = (
            json.dumps({"type": "thread.started", "thread_id": thread_id})
            + "\n"
            + json.dumps({
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 0,
                    "cache_write_input_tokens": 0,
                    "output_tokens": 23,
                    "reasoning_output_tokens": 3,
                },
            })
            + "\n"
        ).encode()
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr=b"")

    monkeypatch.setattr(AI_PANEL_RUNNER.subprocess, "run", completed_ai_label)
    result = AI_PANEL_RUNNER.execute(run_root / "preflight.json")
    schema = load(TARGET / "calibration/ai-grader-panel-run-result-r1.schema.json")
    jsonschema.Draft202012Validator(schema).validate(result)
    assert result["summary"] == {
        "authorized_slots": 3,
        "valid_results": 3,
        "external_failures": 0,
        "unrateable_results": 0,
        "measurement_state": "pilot_measurement_established",
    }
    assert result["pilot_report"] is not None
    report = load(Path(result["pilot_report"]["path"]))
    assert report["reference_state"] == "multi_grader_consensus_reference"
    assert report["human_alignment_state"] == "unmeasured"
    assert len(list((run_root / "output").glob("*/label.json"))) == 3


def test_semantic_grader_threshold_is_fixed_before_holdout():
    threshold_schema = load(TARGET / "calibration/qualification-threshold-r1.schema.json")
    threshold = load(TARGET / "calibration/qualification-threshold-r1.json")
    jsonschema.Draft202012Validator(threshold_schema).validate(threshold)
    assert CALIBRATION_MODULE.threshold_is_bound(threshold) is True
    assert threshold["status"] == "fixed"
    assert threshold["fixed_before_holdout_qualification"] is True
    assert threshold["governance"]["pilot_report_id"] == (
        "sha256:7039ae072aa5af74a48bc46d978e75f40d8474782582c3d73604226869c53194"
    )
    assert threshold["criteria"] == {
        "minimum_exact_agreement_rate": 1,
        "maximum_false_pass_rate": 0,
        "maximum_false_fail_rate": 0,
        "maximum_unknown_rate": 0,
        "maximum_major_false_pass_count": 0,
        "ambiguous_gold_items_allowed": False,
    }
    assert threshold["governance"]["approvers"] == [
        "independent-ai-reviewer:/root/threshold_ai_review",
        "evaluation-owner:user",
    ]

    review_schema = load(TARGET / "calibration/threshold-ai-review-r1.schema.json")
    review = load(TARGET / "calibration/threshold-ai-review-r1.json")
    jsonschema.Draft202012Validator(review_schema).validate(review)
    assert review["decision"] == "approved"
    assert review["holdout_result_seen"] is False
    assert review["criteria_confirmed"] is True

    incomplete = json.loads(json.dumps(threshold))
    incomplete["governance"]["approvers"] = ["evaluation-owner:user"]
    assert CALIBRATION_MODULE.threshold_is_bound(incomplete) is False
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(threshold_schema).validate(incomplete)


def test_semantic_grader_qualification_holdout_and_reference_are_sealed():
    calibration = TARGET / "calibration"
    holdout_path = calibration / "qualification-holdout-r1.json"
    holdout_schema = load(calibration / "qualification-holdout-r1.schema.json")
    holdout = load(holdout_path)
    jsonschema.Draft202012Validator(holdout_schema).validate(holdout)

    plan_path = calibration / "qualification-holdout-plan-r1.json"
    plan_schema = load(calibration / "qualification-holdout-plan-r1.schema.json")
    plan = load(plan_path)
    jsonschema.Draft202012Validator(plan_schema).validate(plan)

    item_ids = [item["holdout_item_id"] for item in holdout["items"]]
    assertion_ids = [
        assertion["assertion_id"]
        for item in holdout["items"]
        for assertion in item["assertions"]
    ]
    assert len(item_ids) == len(set(item_ids)) == 16
    assert len(assertion_ids) == 32
    assert holdout["pilot_overlap_count"] == 0

    pilot = load(calibration / "calibration-input-core-r1.json")
    pilot_item_ids = {item["calibration_item_id"] for item in pilot["items"]}
    pilot_assertion_ids = {
        assertion["assertion_id"]
        for item in pilot["items"]
        for assertion in item["assertions"]
    }
    pilot_messages = {item["assistant_message"] for item in pilot["items"]}
    assert not set(item_ids) & pilot_item_ids
    assert not set(assertion_ids) & pilot_assertion_ids
    assert not {item["assistant_message"] for item in holdout["items"]} & pilot_messages

    assert plan["holdout"]["sha256"] == hashlib.sha256(
        holdout_path.read_bytes()
    ).hexdigest()
    threshold_path = calibration / "qualification-threshold-r1.json"
    assert plan["threshold"]["sha256"] == hashlib.sha256(
        threshold_path.read_bytes()
    ).hexdigest()
    assert plan["reference_generation"]["issued"] is False
    assert plan["qualification_grader"]["issued"] is False

    reference_path = calibration / "qualification-reference-r1.json"
    reference_schema = load(calibration / "qualification-reference-r1.schema.json")
    reference = load(reference_path)
    jsonschema.Draft202012Validator(reference_schema).validate(reference)
    assert reference["status"] == "sealed"
    assert reference["holdout_sha256"] == plan["holdout"]["sha256"]
    assert reference["adjudication_required"] is False
    assert reference["ambiguous_item_count"] == 0
    assert reference["label_counts"] == {
        "pass": 19,
        "fail": 13,
        "unknown": 0,
        "not_applicable": 0,
    }
    reference_keys = {
        (row["holdout_item_id"], row["assertion_id"], row["severity"])
        for row in reference["labels"]
    }
    holdout_keys = {
        (item["holdout_item_id"], assertion["assertion_id"], assertion["severity"])
        for item in holdout["items"]
        for assertion in item["assertions"]
    }
    assert reference_keys == holdout_keys

    reference_execution_ids = set(plan["reference_generation"]["panel_members"])
    reference_execution_ids.add(plan["reference_generation"]["adjudicator"])
    assert plan["qualification_grader"]["execution_id"] not in reference_execution_ids

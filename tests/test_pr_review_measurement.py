from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INSTANCE_ROOT = REPOSITORY_ROOT / "evaluations" / "targets" / "agent-execution-control-lab"
PROFILE_ID = "pr-review-agentic-retrieval-c01-qualification-n2-r1"
sys.path.insert(0, str(INSTANCE_ROOT / "tools"))

import pr_review_measurement as measurement


@pytest.fixture
def profile_stub(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(measurement, "validate_profile", lambda *args, **kwargs: {})


def _summary_for(findings: list[dict]) -> dict[str, str]:
    failed = {finding["category"] for finding in findings}
    return {
        category: "fail" if category in failed else "pass"
        for category in measurement.CATEGORIES
    }


def _expected_review_output(case_id: str) -> dict:
    oracle = json.loads(
        (measurement.FIXTURE_ROOT / case_id / "r1" / "oracle.json").read_text(
            encoding="utf-8"
        )
    )
    findings = oracle["expected_findings"]
    return {"findings": findings, "summary": _summary_for(findings)}


def _collect_valid_review(tmp_path: Path, case_id: str, review_output: dict) -> tuple[Path, Path, Path]:
    prepared = tmp_path / f"prepared-{case_id}"
    measurement.prepare_input(case_id, "deterministic-input", prepared)
    raw_output = tmp_path / f"raw-{case_id}.json"
    raw_output.write_text(json.dumps(review_output), encoding="utf-8")
    execution_file = tmp_path / f"execution-{case_id}.json"
    execution_file.write_text(
        json.dumps(
            {
                "duration_ms": 1234,
                "num_turns": 4,
                "model": "claude-sonnet-5",
                "usage": {"input_tokens": 100, "output_tokens": 40},
                "total_cost_usd": 0.02,
            }
        ),
        encoding="utf-8",
    )
    collected = tmp_path / f"collected-{case_id}"
    measurement.collect_review(
        raw_output,
        "success",
        execution_file,
        1000,
        2500,
        "claude-sonnet-5",
        collected,
    )
    return prepared, collected / "review-output.json", collected / "review-metadata.json"


def test_all_six_fixtures_are_valid_and_revision_bound():
    receipts = measurement.validate_all_fixtures()

    assert [receipt["case_id"] for receipt in receipts] == list(measurement.CASE_IDS)
    assert [receipt["expected_findings"] for receipt in receipts] == [1, 1, 1, 1, 2, 0]
    assert [receipt["clean_control"] for receipt in receipts] == [False] * 5 + [True]
    assert all(len(receipt["input_sha256"]) == 64 for receipt in receipts)
    assert all(len(receipt["oracle_sha256"]) == 64 for receipt in receipts)


def test_prr_c01_r2_is_revision_bound_and_uses_multi_path_identity():
    receipt = measurement.validate_fixture_revision("PRR-C01", "r2")
    fixture_input = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "input.json").read_text(
            encoding="utf-8"
        )
    )
    oracle = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "oracle.json").read_text(
            encoding="utf-8"
        )
    )

    assert receipt["fixture_revision"] == "r2"
    assert receipt["expected_findings"] == 1
    assert fixture_input["review_contract_revision"] == "pr-review-contract-r2"
    assert set(oracle["expected_findings"][0]["paths"]) == set(
        fixture_input["changed_paths"]
    )


@pytest.mark.parametrize(
    ("path", "related_path"),
    [
        (
            "prompts/candidates/example/files/AGENTS.md.txt",
            "evaluations/profiles/example.json",
        ),
        (
            "evaluations/profiles/example.json",
            "prompts/candidates/example/files/AGENTS.md.txt",
        ),
    ],
)
def test_prr_c01_r2_accepts_either_relational_anchor(path: str, related_path: str):
    fixture_input = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "input.json").read_text(
            encoding="utf-8"
        )
    )
    expected = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "oracle.json").read_text(
            encoding="utf-8"
        )
    )["expected_findings"][0]
    actual = {
        "category": "repository_discipline",
        "rule_id": "prompt_evaluation_separation",
        "path": path,
        "related_paths": [related_path],
        "line_start": 1,
        "line_end": 1,
        "severity": "major",
        "message": "prompt変更と評価条件変更を同じ比較単位へ混ぜているため分離する。",
    }

    measurement.validate_review_output_v2(
        {"findings": [actual], "summary": _summary_for([actual])},
        set(fixture_input["changed_paths"]),
    )
    assert measurement._finding_identity_matches_v2(expected, actual)


def test_prr_c01_r2_rejects_missing_related_path():
    expected = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "oracle.json").read_text(
            encoding="utf-8"
        )
    )["expected_findings"][0]
    actual = {
        "category": "repository_discipline",
        "rule_id": "prompt_evaluation_separation",
        "path": "evaluations/profiles/example.json",
        "related_paths": [],
        "line_start": 1,
        "line_end": 1,
        "severity": "major",
        "message": "評価条件を変更している。",
    }

    assert not measurement._finding_identity_matches_v2(expected, actual)


def test_all_measurement_json_files_are_syntactically_valid():
    json_paths = sorted(INSTANCE_ROOT.rglob("*.json"))

    assert json_paths
    for path in json_paths:
        assert json.loads(path.read_text(encoding="utf-8")) is not None, path


def test_measurement_artifacts_are_namespaced_under_registered_target():
    descriptor = json.loads((INSTANCE_ROOT / "target.json").read_text(encoding="utf-8"))

    assert descriptor["target_id"] == "agent-execution-control-lab"
    assert descriptor["layout"] == "namespaced"
    assert descriptor["current_rating_contract"] == "pr-review-finding-quality-v1"
    assert descriptor["target_repository"]["primary_ref"] == {
        "commit": "8cd97283e60f13393fb1302c601c9a4fe0a5381f",
        "tree": "56c7bbbaed3b2b74e5f0978d9d9cab498749bf8d",
    }
    assert not (REPOSITORY_ROOT / "pr-review-measurements").exists()
    assert not (REPOSITORY_ROOT / "scripts" / "pr_review_measurement.py").exists()
    assert not (REPOSITORY_ROOT / "scripts" / "pr_review_fixture_tool.py").exists()
    for relative in descriptor["artifact_roots"].values():
        assert (REPOSITORY_ROOT / relative).is_dir(), relative


def test_qualification_profile_binds_only_planned_baseline_slots():
    profile = measurement.validate_profile(
        PROFILE_ID, "PRR-C01", "agentic-retrieval", 2, "claude-sonnet-5"
    )

    assert profile["comparison_conditions"]["kpi_mapping"] == {
        "elapsed_seconds": "timing.execution_ms / 1000",
        "quality_score": "quality_score",
        "total_tokens": "runtime.total_tokens",
    }
    with pytest.raises(measurement.ValidationError, match="variant mismatch"):
        measurement.validate_profile(
            PROFILE_ID, "PRR-C01", "deterministic-input", 1, "claude-sonnet-5"
        )
    with pytest.raises(measurement.ValidationError, match="outside profile"):
        measurement.validate_profile(
            PROFILE_ID, "PRR-C01", "agentic-retrieval", 3, "claude-sonnet-5"
        )


def test_r2_results_are_write_once_and_reclassified_as_diagnostic():
    results_root = INSTANCE_ROOT / "results"
    paths = sorted(results_root.glob("pr-review-core-r2-*.json"))
    results = [
        measurement.validate_run_result(json.loads(path.read_text(encoding="utf-8")))
        for path in paths
    ]
    index = (results_root / "README.md").read_text(encoding="utf-8")

    assert [result["repetition"] for result in results] == [1, 2]
    assert [result["quality_score"] for result in results] == [1, 4]
    assert all(result["profile_id"] == PROFILE_ID for result in results)
    assert all(result["runtime"]["total_tokens"] for result in results)
    assert all(result["timing"]["execution_ms"] for result in results)
    assert [hashlib.sha256(path.read_bytes()).hexdigest() for path in paths] == [
        "524596702724620a511e8686286afdfc2ec14ea003d6bd22f213619b514a6d50",
        "86a80ebddab68a4efd67999f6a7dcdf81ac102e9ec8dc8af232e8b19af9fe85b",
    ]
    assert "正式evaluation resultは0件" in index
    assert "diagnostic evidenceへ再分類" in index
    assert "pr-review-agentic-retrieval-c01-qualification-n2_2026-08-08.md" in index


def test_function_spec_and_baseline_design_precede_future_evaluation():
    specifications = INSTANCE_ROOT / "specifications"
    function_spec = (specifications / "pr-review-function-r1.md").read_text(encoding="utf-8")
    baseline_design = (specifications / "core-baseline-r1.md").read_text(encoding="utf-8")
    instance_index = (INSTANCE_ROOT / "README.md").read_text(encoding="utf-8")

    assert "oracleだけに存在する正解条件を作らない" in function_spec
    assert "複数pathの関係で成立する違反" in function_spec
    assert "Baselineとして未qualification" in baseline_design
    assert "prompt identity" in baseline_design
    assert "正式resultは0件" in instance_index


def test_execution_file_uses_final_result_usage_with_cache_tokens(tmp_path: Path):
    execution_file = tmp_path / "execution.json"
    execution_file.write_text(
        json.dumps(
            [
                {
                    "type": "system",
                    "subtype": "init",
                    "model": "claude-sonnet-5",
                },
                {
                    "type": "assistant",
                    "message": {
                        "usage": {
                            "input_tokens": 2,
                            "cache_creation_input_tokens": 100,
                            "cache_read_input_tokens": 200,
                            "output_tokens": 9,
                        }
                    },
                },
                {
                    "type": "result",
                    "duration_ms": 1234,
                    "num_turns": 4,
                    "total_cost_usd": 0.02,
                    "usage": {
                        "input_tokens": 3,
                        "cache_creation_input_tokens": 400,
                        "cache_read_input_tokens": 500,
                        "output_tokens": 40,
                    },
                },
            ]
        ),
        encoding="utf-8",
    )

    runtime = measurement._parse_execution_file(execution_file)

    assert runtime == {
        "duration_ms": 1234,
        "turns": 4,
        "input_tokens": 903,
        "output_tokens": 40,
        "reported_cost_usd": 0.02,
        "model": "claude-sonnet-5",
    }


@pytest.mark.parametrize("variant", measurement.VARIANTS)
def test_prepare_input_excludes_oracle_and_is_read_only_packet(tmp_path: Path, variant: str):
    output = tmp_path / variant
    metadata = measurement.prepare_input("PRR-C05", variant, output)

    assert metadata["variant"] == variant
    assert not (output / "oracle.json").exists()
    assert (output / "review-input.json").is_file()
    assert (output / "review-contract.md").is_file()
    assert (output / "review-output-schema.json").is_file()
    assert (output / "pr-review-measurement.py").is_file()
    assert (output / "fixture-tool").stat().st_mode & 0o111
    serialized = (output / "review-input.json").read_text(encoding="utf-8")
    assert "expected_findings" not in serialized
    assert "clean_control" not in serialized


def test_fixture_tool_only_exposes_model_visible_input(tmp_path: Path):
    output = tmp_path / "baseline"
    measurement.prepare_input("PRR-C02", "agentic-retrieval", output)

    completed = subprocess.run(
        [str(output / "fixture-tool"), "diff"],
        cwd=output,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "docs/candidate-status.md" in completed.stdout
    assert "expected_findings" not in completed.stdout


def test_valid_expected_findings_pass_quality_gate(tmp_path: Path, profile_stub):
    prepared, review_output_path, review_metadata_path = _collect_valid_review(
        tmp_path, "PRR-C01", _expected_review_output("PRR-C01")
    )
    result_path = tmp_path / "run-result.json"

    result = measurement.grade_run(
        "PRR-C01",
        "deterministic-input",
        1,
        1001,
        "claude-sonnet-5",
        review_output_path,
        review_metadata_path,
        prepared / "prepare-metadata.json",
        result_path,
        "1001",
        PROFILE_ID,
    )

    assert result["result"] == "pass"
    assert result["quality"]["observed"] is True
    assert result["quality"]["true_positive"] == 1
    assert result["quality"]["false_negative"] == 0
    assert result["timing"]["review_ms"] == 1234
    assert result["runtime"]["turns"] == 4
    assert result["runtime"]["total_tokens"] == 140
    assert result["quality_score"] == 4
    assert measurement.validate_run_result(json.loads(result_path.read_text(encoding="utf-8")))


def test_clean_control_major_false_positive_fails_gate(tmp_path: Path, profile_stub):
    finding = {
        "category": "document_quality",
        "rule_id": "japanese_default",
        "path": "docs/guide-index.md",
        "line_start": 3,
        "line_end": 3,
        "severity": "major",
        "message": "誤った指摘。",
    }
    output = {"findings": [finding], "summary": _summary_for([finding])}
    prepared, review_output_path, review_metadata_path = _collect_valid_review(
        tmp_path, "PRR-C06", output
    )

    result = measurement.grade_run(
        "PRR-C06",
        "deterministic-input",
        1,
        1002,
        "claude-sonnet-5",
        review_output_path,
        review_metadata_path,
        prepared / "prepare-metadata.json",
        tmp_path / "clean-result.json",
        profile_id=PROFILE_ID,
    )

    assert result["result"] == "quality_failed"
    assert result["quality"]["clean_control_major_false_positive"] == 1
    assert result["quality_score"] == 0


def test_summary_inconsistent_with_findings_fails_contract_gate(tmp_path: Path, profile_stub):
    output = _expected_review_output("PRR-C02")
    output["summary"]["evaluation_artifact_integrity"] = "pass"
    prepared, review_output_path, review_metadata_path = _collect_valid_review(
        tmp_path, "PRR-C02", output
    )

    result = measurement.grade_run(
        "PRR-C02",
        "deterministic-input",
        1,
        1005,
        "claude-sonnet-5",
        review_output_path,
        review_metadata_path,
        prepared / "prepare-metadata.json",
        tmp_path / "contract-result.json",
        profile_id=PROFILE_ID,
    )

    assert result["result"] == "quality_failed"
    assert result["quality"]["review_contract_violation"] == 1
    assert result["quality_score"] == 3


def test_finding_outside_applicable_rules_is_scope_violation(tmp_path: Path, profile_stub):
    finding = {
        "category": "document_quality",
        "rule_id": "unbound_preference",
        "path": "docs/guide-index.md",
        "line_start": 3,
        "line_end": 3,
        "severity": "minor",
        "message": "規則へbindされていない好みの指摘。",
    }
    output = {"findings": [finding], "summary": _summary_for([finding])}
    prepared, review_output_path, review_metadata_path = _collect_valid_review(
        tmp_path, "PRR-C06", output
    )

    result = measurement.grade_run(
        "PRR-C06",
        "deterministic-input",
        1,
        1006,
        "claude-sonnet-5",
        review_output_path,
        review_metadata_path,
        prepared / "prepare-metadata.json",
        tmp_path / "scope-result.json",
        profile_id=PROFILE_ID,
    )

    assert result["result"] == "quality_failed"
    assert result["quality"]["scope_violation_count"] == 1
    assert result["quality_score"] == 0


def test_invalid_structured_output_is_not_preserved(tmp_path: Path, profile_stub):
    prepared = tmp_path / "prepared"
    measurement.prepare_input("PRR-C03", "deterministic-input", prepared)
    raw_output = tmp_path / "raw.json"
    raw_output.write_text('{"unexpected":"content"}', encoding="utf-8")
    collected = tmp_path / "collected"

    metadata = measurement.collect_review(
        raw_output,
        "success",
        None,
        100,
        200,
        "claude-sonnet-5",
        collected,
    )
    result = measurement.grade_run(
        "PRR-C03",
        "deterministic-input",
        1,
        1003,
        "claude-sonnet-5",
        collected / "review-output.json",
        collected / "review-metadata.json",
        prepared / "prepare-metadata.json",
        tmp_path / "invalid-result.json",
        profile_id=PROFILE_ID,
    )

    assert metadata["output_valid"] is False
    assert not (collected / "review-output.json").exists()
    assert result["result"] == "invalid_output"
    assert result["quality"]["observed"] is False
    assert result["quality_score"] is None


def test_missing_reported_model_is_measurement_incomplete(tmp_path: Path, profile_stub):
    prepared = tmp_path / "prepared"
    measurement.prepare_input("PRR-C04", "deterministic-input", prepared)
    raw_output = tmp_path / "raw.json"
    raw_output.write_text(json.dumps(_expected_review_output("PRR-C04")), encoding="utf-8")
    collected = tmp_path / "collected"
    measurement.collect_review(
        raw_output,
        "success",
        None,
        100,
        200,
        "claude-sonnet-5",
        collected,
    )

    result = measurement.grade_run(
        "PRR-C04",
        "deterministic-input",
        1,
        1004,
        "claude-sonnet-5",
        collected / "review-output.json",
        collected / "review-metadata.json",
        prepared / "prepare-metadata.json",
        tmp_path / "incomplete-result.json",
        profile_id=PROFILE_ID,
    )

    assert result["quality"]["true_positive"] == 1
    assert result["result"] == "measurement_incomplete"


def test_record_terminal_keeps_quality_unobserved(tmp_path: Path):
    result = measurement.record_terminal_run(
        "PRR-C01",
        "agentic-retrieval",
        2,
        2001,
        "claude-sonnet-5",
        "timeout",
        tmp_path / "timeout.json",
        "2001",
        PROFILE_ID,
    )

    assert result["result"] == "timeout"
    assert result["quality"]["observed"] is False
    assert result["timing"]["execution_ms"] is None


def test_summary_uses_only_passed_run_timings(tmp_path: Path, profile_stub):
    prepared, review_output_path, review_metadata_path = _collect_valid_review(
        tmp_path, "PRR-C01", _expected_review_output("PRR-C01")
    )
    passed_path = tmp_path / "passed.json"
    measurement.grade_run(
        "PRR-C01",
        "deterministic-input",
        1,
        3001,
        "claude-sonnet-5",
        review_output_path,
        review_metadata_path,
        prepared / "prepare-metadata.json",
        passed_path,
        profile_id=PROFILE_ID,
    )
    timeout_path = tmp_path / "timeout.json"
    measurement.record_terminal_run(
        "PRR-C02",
        "deterministic-input",
        1,
        3002,
        "claude-sonnet-5",
        "timeout",
        timeout_path,
        profile_id=PROFILE_ID,
    )

    summary = measurement.summarize_results([passed_path, timeout_path])

    candidate = summary["variants"]["deterministic-input"]
    assert candidate["result_count"] == 2
    assert candidate["pass_count"] == 1
    assert candidate["status_counts"]["timeout"] == 1
    assert candidate["median_execution_ms"] == 1500


def test_workflow_is_manual_read_only_and_pinned():
    workflow = (
        REPOSITORY_ROOT / ".github" / "workflows" / "pr-review-measure-core.yml"
    ).read_text(encoding="utf-8")
    contract = json.loads(measurement.CONTRACT_PATH.read_text(encoding="utf-8"))

    assert "workflow_dispatch:" in workflow
    assert "pull_request:" not in workflow
    assert "pull-requests: write" not in workflow
    assert "gh pr comment" not in workflow
    assert "test ! -e oracle.json" in workflow
    assert "test ! -d .git" in workflow
    assert contract["reviewer_executor"]["revision"] in workflow
    assert "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803" in workflow
    assert "github_token: ${{ github.token }}" in workflow
    assert "jq -c 'del(.\"$schema\")'" in workflow
    assert "evaluations/targets/agent-execution-control-lab/" in workflow
    assert "scripts/pr_review_measurement.py" not in workflow
    assert "pr-review-measurements/" not in workflow
    assert "fixture-tool file:*)" not in workflow
    assert "validate-profile" in workflow
    assert "--profile-id \"$PROFILE_ID\"" in workflow
    grade_block = workflow.split("- name: Grade fixed finding identities", 1)[1].split(
        "- name: Record missing review result", 1
    )[0]
    assert "PROFILE_ID: ${{ inputs.profile_id }}" in grade_block

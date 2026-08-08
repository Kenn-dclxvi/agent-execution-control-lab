from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import jsonschema


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INSTANCE_ROOT = REPOSITORY_ROOT / "evaluations" / "targets" / "agent-execution-control-lab"
PROFILE_ID = "pr-review-agentic-retrieval-c01-qualification-n2-r1"
sys.path.insert(0, str(INSTANCE_ROOT / "tools"))

import pr_review_measurement as measurement
import pr_review_qualification as qualification
import pr_review_code_review_qualification as code_review_qualification
import pr_review_code_review_qualification_r2 as code_review_qualification_r2
import pr_review_code_review_qualification_r3 as code_review_qualification_r3
import pr_review_code_review_qualification_r4 as code_review_qualification_r4
import pr_review_workflow_free_calibration as workflow_free_calibration
import pr_review_subagent_hook as subagent_hook
import pr_review_authority_collector as authority_collector
import pr_review_authority_packet as authority_packet
import pr_review_repository_snapshot as repository_snapshot
import pr_review_repository_snapshot_r2 as repository_snapshot_r2
import pr_review_repository_snapshot_r3 as repository_snapshot_r3


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


def test_prr_c01_r3_is_fresh_held_out_fixture_candidate():
    receipt = measurement.validate_fixture_revision("PRR-C01", "r3")
    r2_input_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "input.json"
    r2_oracle_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "oracle.json"
    r3_input_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r3" / "input.json"
    r3_oracle_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r3" / "oracle.json"
    r2_input = json.loads(r2_input_path.read_text(encoding="utf-8"))
    r3_input = json.loads(r3_input_path.read_text(encoding="utf-8"))
    r3_oracle = json.loads(r3_oracle_path.read_text(encoding="utf-8"))
    quality_contract = json.loads(
        (
            INSTANCE_ROOT
            / "rating-contracts"
            / "pr-review-finding-quality-v3.json"
        ).read_text(encoding="utf-8")
    )
    assert receipt["fixture_revision"] == "r3"
    assert receipt["expected_findings"] == 1
    assert receipt["clean_control"] is False
    assert receipt["input_sha256"] != hashlib.sha256(r2_input_path.read_bytes()).hexdigest()
    assert receipt["oracle_sha256"] != hashlib.sha256(r2_oracle_path.read_bytes()).hexdigest()
    assert r3_input["pr"] != r2_input["pr"]
    assert set(r3_input["changed_paths"]).isdisjoint(r2_input["changed_paths"])
    assert set(r3_oracle["expected_findings"][0]["paths"]) == set(
        r3_input["changed_paths"]
    )
    assert quality_contract["supported_case_revisions"] == ["PRR-C01/r3"]
    assert quality_contract["state"] == "independent_qualification_satisfied"
    assert quality_contract["heldout_boundary"] == {
        "fixture": "PRR-C01/r3",
        "created_before_reviewer_execution": True,
        "excluded_development_fixture": "PRR-C01/r2",
        "excluded_prior_results": True,
    }


def test_prr_c01_r4_is_revision_bound_and_not_held_out():
    input_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r4" / "input.json"
    oracle_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r4" / "oracle.json"
    fixture = json.loads(input_path.read_text(encoding="utf-8"))
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    input_schema = json.loads(
        (INSTANCE_ROOT / "schemas" / "fixture-input-r4.schema.json").read_text(
            encoding="utf-8"
        )
    )
    oracle_schema = json.loads(
        (INSTANCE_ROOT / "schemas" / "fixture-oracle-r4.schema.json").read_text(
            encoding="utf-8"
        )
    )
    jsonschema.Draft202012Validator(input_schema).validate(fixture)
    jsonschema.Draft202012Validator(oracle_schema).validate(oracle)
    quality_contract = json.loads(
        (
            INSTANCE_ROOT
            / "rating-contracts"
            / "pr-review-finding-quality-v4.json"
        ).read_text(encoding="utf-8")
    )
    input_mapping = json.loads(
        (INSTANCE_ROOT / "contracts" / "baseline-input-mapping-r4.json").read_text(
            encoding="utf-8"
        )
    )

    assert fixture["fixture_revision"] == "r4"
    assert len(oracle["expected_findings"]) == 1
    assert set(oracle["expected_findings"][0]["paths"]) == set(
        fixture["changed_paths"]
    )
    assert quality_contract["supported_case_revisions"] == ["PRR-C01/r4"]
    assert quality_contract["state"] == "independent_qualification_unobserved"
    assert quality_contract["qualification_boundary"]["heldout_evidence"] is False
    assert input_mapping["state"] == "unsatisfied"
    assert input_mapping["source"] == {
        "repository": "https://github.com/anthropics/claude-code.git",
        "commit": "2bb60696142b493eafaeacfe00eac51d16c50c4f",
        "workflow_path": "plugins/code-review/commands/code-review.md",
        "workflow_sha256": "2b0837c5ec0b2e75f8ba4565bdafd76fa916b0dc146608c5733af7ba5802012c",
        "entrypoint": "/code-review",
        "excluded_source": "target repositoryの.github/workflows/claude-pr-review.yml",
    }
    assert {entry["identity"] for entry in input_mapping["mappings"] if entry["state"] == "unsatisfied"} == {
        "review_criteria",
        "review_orchestration",
        "false_positive_filter",
    }


def test_prr_c01_r4_uses_consistent_new_file_patches():
    fixture = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r4" / "input.json").read_text(
            encoding="utf-8"
        )
    )

    for change in fixture["changes"]:
        assert change["patch"].startswith("new file mode 100644\n--- /dev/null\n")
        assert f"+++ b/{change['path']}\n" in change["patch"]
        assert "@@ -0,0 +1 @@\n" in change["patch"]
        assert change["patch"].split("@@ -0,0 +1 @@\n", 1)[1] == "+" + change[
            "content_after"
        ].rstrip("\n")

    commit = "8cd97283e60f13393fb1302c601c9a4fe0a5381f"
    if subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
    ).returncode == 0:
        for path in fixture["changed_paths"]:
            assert subprocess.run(
                ["git", "cat-file", "-e", f"{commit}:{path}"],
                cwd=REPOSITORY_ROOT,
                check=False,
                capture_output=True,
            ).returncode != 0


def test_fixture_tool_r4_exposes_rule_identity_and_authority(tmp_path: Path):
    fixture_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r4" / "input.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    authority = {
        "schema_version": "agent-execution-control-lab.authority-packet/v1",
        "authorities": [{"source_path": "AGENTS.md", "content": "規則本文"}],
    }
    (tmp_path / "review-input.json").write_text(
        json.dumps(fixture, ensure_ascii=False), encoding="utf-8"
    )
    (tmp_path / "authority-input.json").write_text(
        json.dumps(authority, ensure_ascii=False), encoding="utf-8"
    )
    fixture_tool = tmp_path / "fixture-tool"
    shutil.copyfile(
        INSTANCE_ROOT / "tools" / "pr_review_fixture_tool_r4.py", fixture_tool
    )
    fixture_tool.chmod(0o755)

    output = subprocess.run(
        [str(fixture_tool), "rules"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    rules_output = json.loads(output.stdout)
    visible_ids = {
        rule["rule_id"]
        for source in rules_output["rule_catalog"]
        for rule in source["rules"]
    }

    assert rules_output["repository_authority"] == authority
    assert "prompt_evaluation_separation" in visible_ids


def test_claude_code_review_core_r1_binds_source_and_workflow():
    prompt_root = (
        INSTANCE_ROOT / "prompts" / "baselines" / "claude-code-review-core-r1"
    )
    manifest = json.loads((prompt_root / "manifest.json").read_text(encoding="utf-8"))
    mapping = json.loads(
        (
            INSTANCE_ROOT
            / "contracts"
            / "baseline-code-review-workflow-mapping-r1.json"
        ).read_text(encoding="utf-8")
    )
    boundary = json.loads(
        (
            INSTANCE_ROOT / "contracts" / "baseline-measurement-boundary-r2.json"
        ).read_text(encoding="utf-8")
    )
    boundary_schema = json.loads(
        (
            INSTANCE_ROOT
            / "schemas"
            / "baseline-measurement-boundary-r2.schema.json"
        ).read_text(encoding="utf-8")
    )
    jsonschema.Draft202012Validator(boundary_schema).validate(boundary)
    source_sha256 = hashlib.sha256((prompt_root / "source-workflow.md").read_bytes()).hexdigest()
    core_sha256 = hashlib.sha256((prompt_root / "core-prompt.md").read_bytes()).hexdigest()
    core_prompt = (prompt_root / "core-prompt.md").read_text(encoding="utf-8")

    assert source_sha256 == "2b0837c5ec0b2e75f8ba4565bdafd76fa916b0dc146608c5733af7ba5802012c"
    assert manifest["source"]["content_sha256"] == source_sha256
    assert manifest["core"]["content_sha256"] == core_sha256
    assert manifest["prompt_identity"] == "claude-code-review-core-r1"
    assert manifest["state"] == "workflow_mapping_satisfied_runtime_unobserved"
    assert mapping["state"] == "satisfied_not_executed"
    assert boundary["state"] == "satisfied"
    assert any("2 sonnet compliance reviewer" in condition for condition in boundary["preserved_review_conditions"])
    dependencies = manifest["dependencies"]
    for binding, path_key, hash_key in (
        (dependencies["workflow_mapping"], "path", "sha256"),
        (dependencies["eligibility"], "path", "sha256"),
        (dependencies["eligibility"], "schema_path", "schema_sha256"),
        (dependencies["fixture_tool"], "path", "sha256"),
        (dependencies["measurement_boundary"], "path", "sha256"),
        (dependencies["measurement_boundary"], "schema_path", "schema_sha256"),
    ):
        assert hashlib.sha256((INSTANCE_ROOT / binding[path_key]).read_bytes()).hexdigest() == binding[
            hash_key
        ]
    assert [entry["source_step"] for entry in mapping["operation_mapping"]] == [
        1, 2, 3, 4, 5, 6, 7, "8-9"
    ]
    for required in (
        "haiku agentを1つ起動",
        "sonnet agentを1つ起動",
        "次の4 agentを並列に起動",
        "別のvalidation agentを並列に起動",
        "validationで高い確度を確認できなかったissue",
    ):
        assert required in core_prompt
    assert ".github/workflows/claude-pr-review.yml" not in core_prompt


def test_fixture_tool_r5_exposes_fixed_eligibility_and_rules(tmp_path: Path):
    fixture = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r4" / "input.json").read_text(
            encoding="utf-8"
        )
    )
    eligibility_path = (
        INSTANCE_ROOT / "contracts" / "prr-c01-r4-review-eligibility-r1.json"
    )
    eligibility = json.loads(eligibility_path.read_text(encoding="utf-8"))
    eligibility_schema = json.loads(
        (INSTANCE_ROOT / "schemas" / "review-eligibility-r1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    jsonschema.Draft202012Validator(eligibility_schema).validate(eligibility)
    authority = {"authorities": [{"source_path": "AGENTS.md", "content": "規則本文"}]}
    (tmp_path / "review-input.json").write_text(json.dumps(fixture), encoding="utf-8")
    (tmp_path / "authority-input.json").write_text(json.dumps(authority), encoding="utf-8")
    (tmp_path / "review-eligibility.json").write_text(
        json.dumps(eligibility), encoding="utf-8"
    )
    core_prompt = "固定code-review workflow\n"
    (tmp_path / "core-prompt.md").write_text(core_prompt, encoding="utf-8")
    fixture_tool = tmp_path / "fixture-tool"
    shutil.copyfile(
        INSTANCE_ROOT / "tools" / "pr_review_fixture_tool_r5.py", fixture_tool
    )
    fixture_tool.chmod(0o755)

    observed_eligibility = json.loads(
        subprocess.run(
            [str(fixture_tool), "eligibility"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )
    observed_rules = json.loads(
        subprocess.run(
            [str(fixture_tool), "rules"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )
    observed_workflow = subprocess.run(
        [str(fixture_tool), "workflow"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    assert observed_eligibility == eligibility
    assert observed_rules["repository_authority"] == authority
    assert observed_workflow == core_prompt
    assert any(
        rule["rule_id"] == "prompt_evaluation_separation"
        for source in observed_rules["rule_catalog"]
        for rule in source["rules"]
    )


def test_repository_snapshot_r3_materializes_prr_c01_r4(tmp_path: Path):
    commit = "8cd97283e60f13393fb1302c601c9a4fe0a5381f"
    if subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
    ).returncode != 0:
        pytest.skip("fixed target commit is unavailable in this checkout")

    fixture_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r4" / "input.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    output = tmp_path / "snapshot"
    receipt = repository_snapshot_r3.materialize_snapshot(
        REPOSITORY_ROOT, commit, fixture_path, output
    )
    snapshot_root = output / "repository"
    try:
        expected_receipt = json.loads(
            (
                INSTANCE_ROOT
                / "contracts"
                / "baseline-repository-snapshot-prr-c01-r4-r1.json"
            ).read_text(encoding="utf-8")
        )
        assert receipt == expected_receipt
        assert receipt["snapshot_revision"] == "pr-review-repository-snapshot-r3"
        assert receipt["fixture"]["revision"] == "r4"
        assert receipt["overlay_paths"] == fixture["changed_paths"]
        assert not (snapshot_root / ".git").exists()
        for change in fixture["changes"]:
            assert (snapshot_root / change["path"]).read_text(encoding="utf-8") == change[
                "content_after"
            ]
    finally:
        repository_snapshot._make_cleanup_writable(snapshot_root)


@pytest.mark.parametrize(
    ("path", "related_path"),
    [
        (
            "prompts/candidates/heldout-review/files/AGENTS.md.txt",
            "evaluations/profiles/heldout-review.json",
        ),
        (
            "evaluations/profiles/heldout-review.json",
            "prompts/candidates/heldout-review/files/AGENTS.md.txt",
        ),
    ],
)
def test_prr_c01_r3_accepts_either_relational_anchor(path: str, related_path: str):
    fixture_input = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r3" / "input.json").read_text(
            encoding="utf-8"
        )
    )
    expected = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r3" / "oracle.json").read_text(
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
        "message": "レビュー制御と実行条件を同じ比較単位で変更しているため分離する。",
    }

    measurement.validate_review_output_v2(
        {"findings": [actual], "summary": _summary_for([actual])},
        set(fixture_input["changed_paths"]),
    )
    assert measurement._finding_identity_matches_v2(expected, actual)


def test_prr_c01_r3_rejects_incomplete_relational_identity():
    expected = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r3" / "oracle.json").read_text(
            encoding="utf-8"
        )
    )["expected_findings"][0]
    actual = {
        "category": "repository_discipline",
        "rule_id": "prompt_evaluation_separation",
        "path": "evaluations/profiles/heldout-review.json",
        "related_paths": [],
        "line_start": 1,
        "line_end": 1,
        "severity": "major",
        "message": "実行条件を変更している。",
    }

    assert not measurement._finding_identity_matches_v2(expected, actual)


def test_prr_c01_r3_independent_audit_receipt_and_state():
    receipt_path = (
        INSTANCE_ROOT / "contracts" / "prr-c01-r3-case-design-audit-r1.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    quality_contract = json.loads(
        (
            INSTANCE_ROOT
            / "rating-contracts"
            / "pr-review-finding-quality-v3.json"
        ).read_text(encoding="utf-8")
    )
    case_readme = (
        INSTANCE_ROOT / "cases" / "PRR-C01" / "r3" / "README.md"
    ).read_text(encoding="utf-8")
    cases_index = (INSTANCE_ROOT / "cases" / "README.md").read_text(
        encoding="utf-8"
    )
    ratings_index = (INSTANCE_ROOT / "rating-contracts" / "README.md").read_text(
        encoding="utf-8"
    )

    assert receipt["schema_version"] == "agent-execution-control-lab.case-design-audit/v1"
    assert receipt["audit_id"] == "prr-c01-r3-case-design-audit-r1"
    assert receipt["case_revision"] == "PRR-C01/r3"
    assert receipt["producer_task_name"] == "prr_c01_r3_independent_audit"
    assert receipt["decision"]["state"] == "satisfied"
    assert all(
        criterion["state"] == "satisfied"
        for criterion in receipt["functional_gate"]
    )
    assert receipt["grader_checks"]["both_allowed_anchors_match"] is True
    assert receipt["grader_checks"]["missing_related_path_rejected"] is True
    assert receipt["remaining_gates"]["reviewer_execution"] == "not_executed"
    assert receipt["remaining_gates"]["baseline_qualification"] == "not_qualified"
    assert quality_contract["state"] == "independent_qualification_satisfied"
    assert quality_contract["admission"]["current_state"] == (
        "independent_qualification_satisfied"
    )
    assert quality_contract["admission"]["audit_receipt"] == (
        "contracts/prr-c01-r3-case-design-audit-r1.json"
    )
    assert "independent_audit_satisfied" in case_readme
    assert "Baseline未qualification" in cases_index
    assert "Baseline未qualification" in ratings_index


def test_prr_c01_r4_independent_audit_receipt_and_state():
    receipt = json.loads(
        (
            INSTANCE_ROOT
            / "contracts"
            / "prr-c01-r4-case-design-audit-r1.json"
        ).read_text(encoding="utf-8")
    )
    quality_contract = json.loads(
        (
            INSTANCE_ROOT
            / "rating-contracts"
            / "pr-review-finding-quality-v5.json"
        ).read_text(encoding="utf-8")
    )
    case_readme = (
        INSTANCE_ROOT / "cases" / "PRR-C01" / "r4" / "README.md"
    ).read_text(encoding="utf-8")
    cases_index = (INSTANCE_ROOT / "cases" / "README.md").read_text(
        encoding="utf-8"
    )
    ratings_index = (INSTANCE_ROOT / "rating-contracts" / "README.md").read_text(
        encoding="utf-8"
    )

    assert receipt["schema_version"] == (
        "agent-execution-control-lab.pr-review-case-design-audit/v1"
    )
    assert receipt["audit_id"] == "prr-c01-r4-case-design-audit-r1"
    assert receipt["target"]["case_revision"] == "PRR-C01/r4"
    assert receipt["producer_task_name"] == "/root/prr_c01_r4_independent_audit"
    assert receipt["decision"] == "satisfied"
    assert all(gate["state"] == "satisfied" for gate in receipt["gates"])
    assert receipt["stage_b"]["oracle_or_grader_only_required_conditions"] == []
    assert receipt["forbidden_input"]["used"] is False
    assert quality_contract["supported_case_revisions"] == ["PRR-C01/r4"]
    assert quality_contract["state"] == "independent_qualification_satisfied"
    assert quality_contract["admission"]["current_state"] == (
        "independent_qualification_satisfied"
    )
    assert quality_contract["admission"]["audit_receipt"] == (
        "contracts/prr-c01-r4-case-design-audit-r1.json"
    )
    assert quality_contract["admission"]["execution_state"] == "not_executed"
    assert quality_contract["admission"]["baseline_qualification_state"] == (
        "not_qualified"
    )
    assert "independent_audit_satisfied" in case_readme
    assert "Baseline未qualification" in cases_index
    assert "Baseline未qualification" in ratings_index


def test_fixture_schema_revisions_coexist_and_r3_is_indexed():
    for revision in ("r1", "r2", "r3"):
        measurement.validate_fixture_revision("PRR-C01", revision)

    input_schema = json.loads(
        (INSTANCE_ROOT / "schemas" / "fixture-input-r3.schema.json").read_text(
            encoding="utf-8"
        )
    )
    oracle_schema = json.loads(
        (INSTANCE_ROOT / "schemas" / "fixture-oracle-r3.schema.json").read_text(
            encoding="utf-8"
        )
    )
    cases_index = (INSTANCE_ROOT / "cases" / "README.md").read_text(encoding="utf-8")
    ratings_index = (INSTANCE_ROOT / "rating-contracts" / "README.md").read_text(
        encoding="utf-8"
    )
    schemas_index = (INSTANCE_ROOT / "schemas" / "README.md").read_text(
        encoding="utf-8"
    )

    assert input_schema["properties"]["schema_version"] == {"const": 3}
    assert input_schema["properties"]["fixture_revision"] == {"const": "r3"}
    assert input_schema["properties"]["review_contract_revision"] == {
        "const": "pr-review-contract-r2"
    }
    assert oracle_schema["properties"]["schema_version"] == {"const": 3}
    assert oracle_schema["properties"]["fixture_revision"] == {"const": "r3"}
    assert "[`PRR-C01/r3`](PRR-C01/r3/README.md)" in cases_index
    assert (
        "[`pr-review-finding-quality-v3`](pr-review-finding-quality-v3.json)"
        in ratings_index
    )
    assert "[fixture input r3](fixture-input-r3.schema.json)" in schemas_index
    assert "[fixture oracle r3](fixture-oracle-r3.schema.json)" in schemas_index


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


def test_prr_c01_r3_qualification_preflight_is_reproducible_and_not_executed(
    tmp_path: Path,
):
    profile_path = qualification.PROFILE_PATH
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    validation = measurement.validate_qualification_profile(profile)
    expected_receipt = json.loads(qualification.PREFLIGHT_PATH.read_text(encoding="utf-8"))
    output = tmp_path / "preflight.json"
    actual_receipt = measurement.preflight_qualification(profile_path, output)

    assert validation["planned_slots"] == [
        {
            "case_id": "PRR-C01",
            "fixture_revision": "r3",
            "variant": "agentic-retrieval",
            "repetition": 1,
        },
        {
            "case_id": "PRR-C01",
            "fixture_revision": "r3",
            "variant": "agentic-retrieval",
            "repetition": 2,
        },
    ]
    assert actual_receipt == expected_receipt
    assert json.loads(output.read_text(encoding="utf-8")) == expected_receipt
    assert actual_receipt["state"] == "ready_not_executed"
    assert actual_receipt["execution"] == {
        "state": "not_issued",
        "authorization": "not_granted_by_preflight",
        "allowed_after_separate_authorization": (
            "two sequential Core Baseline qualification slots only"
        ),
    }


def test_prr_c01_r3_qualification_preflight_rejects_repetition_drift():
    profile_path = qualification.PROFILE_PATH
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile["comparison_conditions"]["repetition_condition"]["iterations"] = 3

    with pytest.raises(measurement.ValidationError, match="repetition condition mismatch"):
        measurement.validate_qualification_profile(profile)


def test_prr_c01_r3_qualification_recovery_preserves_first_attempt_identity():
    profiles = INSTANCE_ROOT / "profiles"
    first = json.loads(
        (profiles / "pr-review-agentic-retrieval-c01-r3-qualification-n2-r1.json").read_text(
            encoding="utf-8"
        )
    )
    second = json.loads(
        (profiles / "pr-review-agentic-retrieval-c01-r3-qualification-n2-r2.json").read_text(
            encoding="utf-8"
        )
    )
    third = json.loads(
        (profiles / "pr-review-agentic-retrieval-c01-r3-qualification-n2-r3.json").read_text(
            encoding="utf-8"
        )
    )
    recovery = json.loads(qualification.PROFILE_PATH.read_text(encoding="utf-8"))

    assert first["comparison_conditions"]["workflow"]["revision"] == "pr-review-qualify-core-r1"
    assert first["comparison_conditions"]["run_result_schema"]["revision"] == "run-result-r3"
    assert second["comparison_conditions"]["workflow"]["revision"] == "pr-review-qualify-core-r2"
    assert second["comparison_conditions"]["run_result_schema"]["revision"] == "run-result-r4"
    assert third["comparison_conditions"]["workflow"]["revision"] == "pr-review-qualify-core-r3"
    assert third["comparison_conditions"]["run_result_schema"]["revision"] == "run-result-r5"
    assert recovery["comparison_conditions"]["workflow"]["revision"] == "pr-review-qualify-core-r4"
    assert recovery["comparison_conditions"]["run_result_schema"]["revision"] == "run-result-r6"
    assert recovery["comparison_conditions"]["executor_parameters"]["max_turns"] is None
    assert recovery["comparison_conditions"]["executor_parameters"]["turn_limit_source"] == (
        "action_default_at_fixed_action_revision"
    )


def test_prr_c01_r3_qualification_failures_are_registered_write_once():
    result_root = INSTANCE_ROOT / "results"
    paths = sorted(result_root.glob("pr-review-core-baseline-qualification-r1-*.json"))
    results = [json.loads(path.read_text(encoding="utf-8")) for path in paths]

    assert [result["github_run_id"] for result in results] == [
        "31253512886",
        "31253838176",
        "31254138818",
        "31256216037",
    ]
    assert [result["schema_version"] for result in results] == [3, 4, 5, 6]
    assert [result["result"] for result in results] == [
        "execution_failed",
        "execution_failed",
        "execution_failed",
        "quality_failed",
    ]
    assert [result["quality_score"] for result in results] == [None, None, None, 0]
    assert qualification.validate_run_result(results[-1])
    assert [hashlib.sha256(path.read_bytes()).hexdigest() for path in paths] == [
        "764981d1981ff8509efceada7c0dbfa3f054aefe3fd8ae751e87d4abe2b3fe85",
        "bf42c0c6cd343645e79a029210da45c6988c7548f91687949f4439747ce02968",
        "076c4686e7f4d7191b453306390a227453bc6b8665c2e7220ada02170e815299",
        "dc622383fe4e80aef176ec7f5d6207e17297b5a4f572ebe12acaf7e28ffcc8f7",
    ]


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


def test_baseline_prompt_manifest_binds_content_and_remains_blocked():
    bundle = (
        INSTANCE_ROOT
        / "prompts"
        / "baselines"
        / "claude-pr-review-core-r1"
    )
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    mapping = json.loads(
        (INSTANCE_ROOT / "contracts" / "baseline-input-mapping-r1.json").read_text(
            encoding="utf-8"
        )
    )

    for entry in manifest["files"]:
        assert hashlib.sha256((bundle / entry["path"]).read_bytes()).hexdigest() == entry[
            "sha256"
        ]
    for dependency in ("review_contract", "output_schema", "fixture_tool"):
        entry = manifest["dependencies"][dependency]
        assert hashlib.sha256((INSTANCE_ROOT / entry["path"]).read_bytes()).hexdigest() == entry[
            "sha256"
        ]

    states = {entry["identity"]: entry["state"] for entry in mapping["mappings"]}
    assert manifest["state"] == "admission_blocked"
    assert manifest["admission"]["state"] == "blocked"
    assert mapping["state"] == "unsatisfied"
    assert states["applicable_repository_rules"] == "partially_satisfied"
    assert states["changed_file_content"] == "partially_satisfied"


def test_baseline_prompt_r2_binds_authority_packet_dependencies():
    bundle = INSTANCE_ROOT / "prompts" / "baselines" / "claude-pr-review-core-r2"
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    mapping = json.loads(
        (INSTANCE_ROOT / "contracts" / "baseline-input-mapping-r2.json").read_text(
            encoding="utf-8"
        )
    )

    for entry in manifest["files"]:
        assert hashlib.sha256((bundle / entry["path"]).read_bytes()).hexdigest() == entry[
            "sha256"
        ]
    for dependency in (
        "authority_selection",
        "authority_packet_schema",
        "authority_packet_materializer",
        "review_contract",
        "output_schema",
        "fixture_tool",
    ):
        entry = manifest["dependencies"][dependency]
        assert hashlib.sha256((INSTANCE_ROOT / entry["path"]).read_bytes()).hexdigest() == entry[
            "sha256"
        ]

    states = {entry["identity"]: entry["state"] for entry in mapping["mappings"]}
    assert manifest["prompt_identity"] == "claude-pr-review-core-r2"
    assert manifest["admission"]["state"] == "blocked"
    assert states["applicable_repository_rules"] == "satisfied"
    assert states["changed_file_content"] == "partially_satisfied"


def test_baseline_prompt_r3_binds_satisfied_input_mapping():
    bundle = INSTANCE_ROOT / "prompts" / "baselines" / "claude-pr-review-core-r3"
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    mapping = json.loads(
        (INSTANCE_ROOT / "contracts" / "baseline-input-mapping-r3.json").read_text(
            encoding="utf-8"
        )
    )

    for entry in manifest["files"]:
        assert hashlib.sha256((bundle / entry["path"]).read_bytes()).hexdigest() == entry[
            "sha256"
        ]
    for dependency in (
        "authority_selection",
        "authority_packet_schema",
        "authority_packet_materializer",
        "repository_snapshot",
        "repository_snapshot_schema",
        "repository_snapshot_materializer",
        "review_contract",
        "output_schema",
        "fixture_tool",
    ):
        entry = manifest["dependencies"][dependency]
        assert hashlib.sha256((INSTANCE_ROOT / entry["path"]).read_bytes()).hexdigest() == entry[
            "sha256"
        ]

    states = {entry["identity"]: entry["state"] for entry in mapping["mappings"]}
    source_r2 = (
        INSTANCE_ROOT
        / "prompts"
        / "baselines"
        / "claude-pr-review-core-r2"
        / "source-prompt.md"
    )
    assert (bundle / "source-prompt.md").read_bytes() == source_r2.read_bytes()
    assert manifest["state"] == "input_mapping_satisfied"
    assert manifest["admission"]["state"] == "blocked"
    assert mapping["state"] == "satisfied"
    assert mapping["blocking_conditions"] == []
    assert states["applicable_repository_rules"] == "satisfied"
    assert states["changed_file_content"] == "satisfied"


def test_baseline_execution_parity_r1_is_preserved_as_superseded_history():
    contract_path = (
        INSTANCE_ROOT / "contracts" / "baseline-execution-parity-r1.json"
    )
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    source = contract["source"]
    core = contract["core_candidate"]

    source_workflow = subprocess.run(
        [
            "git",
            "show",
            f'{source["target_commit"]}:{source["workflow_path"]}',
        ],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    ).stdout
    core_workflow = subprocess.run(
        ["git", "show", f'29bb7edcac2908772bef7065c8a45ca670f3283d:{core["workflow_path"]}'],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    ).stdout
    profile_path = INSTANCE_ROOT / "profiles" / f'{core["profile_id"]}.json'

    assert contract["schema_version"] == (
        "agent-execution-control-lab.pr-review-baseline-execution-parity/v1"
    )
    assert contract["state"] == "unsatisfied"
    assert contract["admission_effect"] == "core_baseline_blocked"
    assert hashlib.sha256(source_workflow).hexdigest() == source["workflow_sha256"]
    assert hashlib.sha256(core_workflow).hexdigest() == core["workflow_sha256"]
    assert hashlib.sha256(profile_path.read_bytes()).hexdigest() == core["profile_sha256"]

    states = {check["identity"]: check["state"] for check in contract["checks"]}
    assert states == {
        "review_criteria": "satisfied",
        "model_visible_input_values": "satisfied",
        "action_revision": "unverified",
        "trigger_and_pull_request_context": "unsatisfied",
        "git_workspace": "unsatisfied",
        "model_selection": "unverified",
        "turn_limit": "unsatisfied",
        "tool_surface": "unsatisfied",
        "output_contract": "unsatisfied",
        "github_permissions_and_reporting": "intentionally_changed",
    }
    assert set(contract["blocking_conditions"]) == {
        identity for identity, state in states.items() if state != "satisfied"
    }

    source_text = source_workflow.decode()
    core_text = core_workflow.decode()
    assert "pull_request:" in source_text
    assert "actions/checkout@v6" in source_text
    assert "pull-requests: write" in source_text
    assert "id-token: write" in source_text
    assert "Bash(gh pr diff:*)" in source_text
    assert "mcp__github_inline_comment__create_inline_comment" in source_text
    assert "--max-turns" not in source_text
    assert "--json-schema" not in source_text

    assert "workflow_dispatch:" in core_text
    assert "test ! -d .git" in core_text
    assert "--max-turns 12" in core_text
    assert "--json-schema" in core_text
    assert 'Bash(./fixture-tool:*)' in core_text
    assert "pull-requests: read" in core_text

    diagnostic_results = contract["diagnostic_results"]
    assert [entry["github_run_id"] for entry in diagnostic_results] == [
        "31253512886",
        "31253838176",
        "31254138818",
    ]
    for entry in diagnostic_results:
        result = json.loads((INSTANCE_ROOT / entry["result_path"]).read_text(encoding="utf-8"))
        assert result["github_run_id"] == entry["github_run_id"]
        assert entry["classification"] == "execution_parity_diagnostic_only"


def test_baseline_measurement_boundary_is_indexed_and_bound_to_active_profile():
    contracts_index = (INSTANCE_ROOT / "contracts" / "README.md").read_text(
        encoding="utf-8"
    )
    schemas_index = (INSTANCE_ROOT / "schemas" / "README.md").read_text(
        encoding="utf-8"
    )
    baseline_design = (
        INSTANCE_ROOT / "specifications" / "core-baseline-r1.md"
    ).read_text(encoding="utf-8")
    instance_index = (INSTANCE_ROOT / "README.md").read_text(encoding="utf-8")
    boundary = json.loads(
        (INSTANCE_ROOT / "contracts" / "baseline-measurement-boundary-r1.json").read_text(
            encoding="utf-8"
        )
    )
    profile = json.loads(qualification.PROFILE_PATH.read_text(encoding="utf-8"))
    workflow = (REPOSITORY_ROOT / ".github/workflows/pr-review-measure-core.yml").read_text(
        encoding="utf-8"
    )

    assert "baseline-execution-parity-r1.json" in contracts_index
    assert "baseline-measurement-boundary-r1.json" in contracts_index
    assert "baseline-execution-parity-r1.schema.json" in schemas_index
    assert "baseline-measurement-boundary-r1.schema.json" in schemas_index
    assert boundary["state"] == "satisfied"
    assert boundary["baseline_definition"]["excluded_reference"].endswith(
        ".github/workflows/claude-pr-review.yml"
    )
    assert boundary["prior_audit"]["effect"] == (
        "履歴として保持するが、Core Baseline admissionのgateには使用しない"
    )
    assert profile["comparison_conditions"]["measurement_boundary"] == {
        "path": "contracts/baseline-measurement-boundary-r1.json",
        "sha256": hashlib.sha256(
            (INSTANCE_ROOT / "contracts" / "baseline-measurement-boundary-r1.json").read_bytes()
        ).hexdigest(),
        "required_state": "satisfied",
    }
    assert "測定用の変更" in baseline_design
    assert "インストール済みの`.github/workflows/claude-pr-review.yml`は、測定設計の比較元にしない" in baseline_design
    assert "測定境界" in instance_index
    assert "git init -q" in workflow
    assert "test ! -d repository/.git" in workflow
    assert "--max-turns" not in workflow


def test_fixture_tool_matches_prr_c01_r2_logical_input(tmp_path: Path):
    case_root = measurement.FIXTURE_ROOT / "PRR-C01" / "r2"
    fixture_input = json.loads((case_root / "input.json").read_text(encoding="utf-8"))
    shutil.copyfile(case_root / "input.json", tmp_path / "review-input.json")
    shutil.copyfile(
        INSTANCE_ROOT / "rating-contracts" / "review-contract-r2.md",
        tmp_path / "review-contract.md",
    )
    fixture_tool = tmp_path / "fixture-tool"
    shutil.copyfile(INSTANCE_ROOT / "tools" / "pr_review_fixture_tool.py", fixture_tool)
    fixture_tool.chmod(0o755)

    def invoke(command: str) -> str:
        return subprocess.run(
            [str(fixture_tool), command],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    assert json.loads(invoke("metadata")) == fixture_input["pr"]
    assert json.loads(invoke("changed-paths")) == fixture_input["changed_paths"]
    assert json.loads(invoke("rules")) == fixture_input["rules"]
    assert json.loads(invoke("files")) == {
        change["path"]: change["content_after"] for change in fixture_input["changes"]
    }
    assert invoke("diff") == "".join(
        f"diff --git a/{change['path']} b/{change['path']}\n{change['patch']}\n"
        for change in fixture_input["changes"]
    )
    assert invoke("contract") == (
        INSTANCE_ROOT / "rating-contracts" / "review-contract-r2.md"
    ).read_text(encoding="utf-8")


def test_authority_collector_resolves_root_symlink_and_local_precedence(tmp_path: Path):
    repository = tmp_path / "repository"
    repository.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"], cwd=repository, check=True
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"], cwd=repository, check=True
    )
    (repository / "AGENTS.md").write_text("root rules\n", encoding="utf-8")
    (repository / "CLAUDE.md").symlink_to("AGENTS.md")
    (repository / "prompts" / "candidates").mkdir(parents=True)
    (repository / "prompts" / "AGENTS.md").write_text("prompt rules\n", encoding="utf-8")
    (repository / "prompts" / "candidates" / "AGENTS.md").write_text(
        "candidate rules\n", encoding="utf-8"
    )
    (repository / "evaluations").mkdir()
    (repository / "evaluations" / "AGENTS.md").write_text(
        "evaluation rules\n", encoding="utf-8"
    )
    subprocess.run(["git", "add", "."], cwd=repository, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repository, check=True)
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    receipt = authority_collector.collect_authorities(
        repository,
        commit,
        [
            "prompts/candidates/example/files/AGENTS.md.txt",
            "evaluations/profiles/example.json",
        ],
    )

    assert receipt["path_bindings"] == [
        {
            "changed_path": "prompts/candidates/example/files/AGENTS.md.txt",
            "applicable_authorities": [
                "CLAUDE.md",
                "prompts/AGENTS.md",
                "prompts/candidates/AGENTS.md",
            ],
        },
        {
            "changed_path": "evaluations/profiles/example.json",
            "applicable_authorities": ["CLAUDE.md", "evaluations/AGENTS.md"],
        },
    ]
    root = receipt["authorities"][0]
    assert root["source_mode"] == "120000"
    assert root["symlink_target"] == "AGENTS.md"
    assert root["resolved_path"] == "AGENTS.md"


def test_saved_authority_selection_matches_fixed_target_tree():
    commit = "8cd97283e60f13393fb1302c601c9a4fe0a5381f"
    availability = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
    )
    if availability.returncode != 0:
        pytest.skip("fixed target commit is unavailable in this checkout")
    fixture_input = json.loads(
        (measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "input.json").read_text(
            encoding="utf-8"
        )
    )
    expected = json.loads(
        (
            INSTANCE_ROOT
            / "contracts"
            / "baseline-authority-selection-r1.json"
        ).read_text(encoding="utf-8")
    )

    observed = authority_collector.collect_authorities(
        REPOSITORY_ROOT, commit, fixture_input["changed_paths"]
    )

    assert observed == expected


def test_authority_packet_is_identical_for_both_variant_inputs(tmp_path: Path):
    commit = "8cd97283e60f13393fb1302c601c9a4fe0a5381f"
    availability = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
    )
    if availability.returncode != 0:
        pytest.skip("fixed target commit is unavailable in this checkout")
    receipt = INSTANCE_ROOT / "contracts" / "baseline-authority-selection-r1.json"
    packet = authority_packet.materialize_authority_packet(REPOSITORY_ROOT, receipt)

    case_input = measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "input.json"
    shutil.copyfile(case_input, tmp_path / "review-input.json")
    shutil.copyfile(
        INSTANCE_ROOT / "rating-contracts" / "review-contract-r2.md",
        tmp_path / "review-contract.md",
    )
    (tmp_path / "authority-input.json").write_text(
        json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    fixture_tool = tmp_path / "fixture-tool"
    shutil.copyfile(INSTANCE_ROOT / "tools" / "pr_review_fixture_tool_r2.py", fixture_tool)
    fixture_tool.chmod(0o755)

    agentic_packet = json.loads(
        subprocess.run(
            [str(fixture_tool), "rules"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )
    candidate_packet = json.loads(
        (tmp_path / "authority-input.json").read_text(encoding="utf-8")
    )

    assert agentic_packet == candidate_packet == packet
    assert [entry["source_path"] for entry in packet["authorities"]] == [
        "CLAUDE.md",
        "prompts/AGENTS.md",
        "evaluations/AGENTS.md",
    ]
    for entry in packet["authorities"]:
        assert hashlib.sha256(entry["content"].encode()).hexdigest() == entry[
            "content_sha256"
        ]


def test_repository_snapshot_and_fixture_tool_r3_preserve_read_boundary(tmp_path: Path):
    commit = "8cd97283e60f13393fb1302c601c9a4fe0a5381f"
    availability = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
    )
    if availability.returncode != 0:
        pytest.skip("fixed target commit is unavailable in this checkout")

    case_input_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r2" / "input.json"
    case_input = json.loads(case_input_path.read_text(encoding="utf-8"))
    output = tmp_path / "snapshot"
    receipt = repository_snapshot.materialize_snapshot(
        REPOSITORY_ROOT, commit, case_input_path, output
    )
    snapshot_root = output / "repository"
    try:
        expected_receipt = json.loads(
            (
                INSTANCE_ROOT
                / "contracts"
                / "baseline-repository-snapshot-r1.json"
            ).read_text(encoding="utf-8")
        )
        assert receipt == expected_receipt
        assert not (snapshot_root / ".git").exists()
        assert snapshot_root.stat().st_mode & 0o222 == 0
        for change in case_input["changes"]:
            path = snapshot_root / change["path"]
            assert path.read_text(encoding="utf-8") == change["content_after"]
            assert path.stat().st_mode & 0o222 == 0

        harness = tmp_path / "harness"
        harness.mkdir()
        shutil.copyfile(case_input_path, harness / "review-input.json")
        shutil.copyfile(
            INSTANCE_ROOT / "rating-contracts" / "review-contract-r2.md",
            harness / "review-contract.md",
        )
        packet = authority_packet.materialize_authority_packet(
            REPOSITORY_ROOT,
            INSTANCE_ROOT / "contracts" / "baseline-authority-selection-r1.json",
        )
        (harness / "authority-input.json").write_text(
            json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        fixture_tool = harness / "fixture-tool"
        shutil.copyfile(
            INSTANCE_ROOT / "tools" / "pr_review_fixture_tool_r3.py", fixture_tool
        )
        fixture_tool.chmod(0o755)
        environment = {
            **os.environ,
            "PR_REVIEW_INPUT": str(harness / "review-input.json"),
            "PR_REVIEW_AUTHORITY": str(harness / "authority-input.json"),
            "PR_REVIEW_REPOSITORY": str(snapshot_root),
        }

        def invoke(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [str(fixture_tool), *arguments],
                cwd=harness,
                env=environment,
                check=check,
                capture_output=True,
                text=True,
            )

        available_paths = json.loads(invoke("list-files").stdout)
        assert "README.md" in available_paths
        assert set(case_input["changed_paths"]) <= set(available_paths)
        assert invoke("file", "evaluations/profiles/example.json").stdout == next(
            change["content_after"]
            for change in case_input["changes"]
            if change["path"] == "evaluations/profiles/example.json"
        )
        expected_readme = subprocess.run(
            ["git", "show", f"{commit}:README.md"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        assert invoke("file", "README.md").stdout == expected_readme
        assert invoke("file", ".git/config", check=False).returncode != 0
        assert invoke("file", "../AGENTS.md", check=False).returncode != 0
    finally:
        repository_snapshot._make_cleanup_writable(snapshot_root)


def test_prr_c01_r3_repository_snapshot_has_case_specific_receipt(tmp_path: Path):
    commit = "8cd97283e60f13393fb1302c601c9a4fe0a5381f"
    availability = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
    )
    if availability.returncode != 0:
        pytest.skip("fixed target commit is unavailable in this checkout")

    case_input_path = measurement.FIXTURE_ROOT / "PRR-C01" / "r3" / "input.json"
    case_input = json.loads(case_input_path.read_text(encoding="utf-8"))
    output = tmp_path / "snapshot-r3"
    receipt = repository_snapshot_r2.materialize_snapshot(
        REPOSITORY_ROOT, commit, case_input_path, output
    )
    snapshot_root = output / "repository"
    try:
        expected_receipt = json.loads(
            (
                INSTANCE_ROOT
                / "contracts"
                / "baseline-repository-snapshot-prr-c01-r3-r1.json"
            ).read_text(encoding="utf-8")
        )
        assert receipt == expected_receipt
        assert receipt["fixture"] == {
            "case_id": "PRR-C01",
            "revision": "r3",
            "input_sha256": hashlib.sha256(case_input_path.read_bytes()).hexdigest(),
        }
        assert receipt["overlay_paths"] == case_input["changed_paths"]
        assert not (snapshot_root / ".git").exists()
        assert snapshot_root.stat().st_mode & 0o222 == 0
        for change in case_input["changes"]:
            path = snapshot_root / change["path"]
            assert path.read_text(encoding="utf-8") == change["content_after"]
            assert path.stat().st_mode & 0o222 == 0
    finally:
        repository_snapshot._make_cleanup_writable(snapshot_root)


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


def test_qualification_prepare_collect_and_grade_passes_fixed_r3_identity(tmp_path: Path):
    prepared = tmp_path / "prepared"
    snapshot_root = prepared / "repository"
    try:
        metadata = qualification.prepare_input(1, prepared)
        fixture_input = json.loads(
            (prepared / "review-input.json").read_text(encoding="utf-8")
        )
        paths = fixture_input["changed_paths"]
        finding = {
            "category": "repository_discipline",
            "rule_id": "prompt_evaluation_separation",
            "path": paths[0],
            "related_paths": [paths[1]],
            "line_start": 1,
            "line_end": 1,
            "severity": "major",
            "message": "レビュー制御と評価条件を同じ変更へ混ぜているため分離する。",
        }
        raw_output = tmp_path / "raw-output.json"
        raw_output.write_text(
            json.dumps(
                {"findings": [finding], "summary": _summary_for([finding])},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        execution_file = tmp_path / "execution.json"
        execution_file.write_text(
            json.dumps(
                {
                    "type": "result",
                    "duration_ms": 1200,
                    "num_turns": 6,
                    "model": "claude-sonnet-5",
                    "usage": {"input_tokens": 120, "output_tokens": 30},
                    "total_cost_usd": 0.03,
                }
            ),
            encoding="utf-8",
        )
        collected = tmp_path / "collected"
        qualification.collect_review(
            raw_output,
            "success",
            execution_file,
            100,
            1400,
            "claude-sonnet-5",
            prepared / "review-input.json",
            collected,
        )
        result_path = tmp_path / "result.json"
        result = qualification.grade_run(
            1,
            123456,
            "claude-sonnet-5",
            collected / "review-output.json",
            collected / "review-metadata.json",
            prepared / "prepare-metadata.json",
            result_path,
            "123456",
        )

        assert metadata["fixture_revision"] == "r3"
        assert metadata["repetition"] == 1
        assert not (prepared / "oracle.json").exists()
        assert not (snapshot_root / ".git").exists()
        assert (prepared / "pr_review_measurement.py").is_file()
        assert not (prepared / "pr-review-measurement.py").exists()
        subprocess.run(
            [sys.executable, "pr-review-qualification.py", "--help"],
            cwd=prepared,
            check=True,
            capture_output=True,
            text=True,
        )
        assert result["result"] == "pass"
        assert result["quality_score"] == 4
        assert result["quality"]["true_positive"] == 1
        assert result["quality"]["false_negative"] == 0
        assert result["quality"]["false_positive"] == 0
        assert result["runtime"]["total_tokens"] == 150
        assert qualification.validate_run_result(
            json.loads(result_path.read_text(encoding="utf-8"))
        )
    finally:
        repository_snapshot._make_cleanup_writable(snapshot_root)


def test_workflow_is_fixed_to_first_read_only_qualification_slot():
    workflow = (
        REPOSITORY_ROOT / ".github" / "workflows" / "pr-review-measure-core.yml"
    ).read_text(encoding="utf-8")
    profile = json.loads(qualification.PROFILE_PATH.read_text(encoding="utf-8"))

    assert "workflow_dispatch:" in workflow
    assert "pull_request:" not in workflow
    assert "pull-requests: write" not in workflow
    assert "gh pr comment" not in workflow
    assert "test ! -e oracle.json" in workflow
    assert "git init -q" in workflow
    assert 'git remote add origin "$GITHUB_SERVER_URL/$GITHUB_REPOSITORY.git"' in workflow
    assert "test ! -d repository/.git" in workflow
    assert "--max-turns" not in workflow
    assert "test \"$REPETITION\" = \"1\"" in workflow
    assert profile["comparison_conditions"]["agent_environment"]["action_revision"] in workflow
    assert "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803" in workflow
    assert "github_token: ${{ github.token }}" in workflow
    assert "jq -c 'del(.\"$schema\")'" in workflow
    assert "evaluations/targets/agent-execution-control-lab/" in workflow
    assert "scripts/pr_review_measurement.py" not in workflow
    assert "pr-review-measurements/" not in workflow
    assert "deterministic-input" not in workflow
    assert '--allowedTools "Bash(./fixture-tool:*)"' in workflow
    assert "pr_review_qualification.py" in workflow
    assert "review-output-r2.schema.json" in workflow
    assert hashlib.sha256(workflow.encode()).hexdigest() == profile[
        "comparison_conditions"
    ]["workflow"]["sha256"]

    prompt_block = workflow.split("          prompt: |\n", 1)[1].split(
        "          claude_args:", 1
    )[0]
    prompt_text = "\n".join(
        line[12:] if line.startswith("            ") else line
        for line in prompt_block.splitlines()
    ).rstrip() + "\n"
    expected_prompt = (
        INSTANCE_ROOT
        / "prompts"
        / "baselines"
        / "claude-pr-review-core-r3"
        / "core-prompt.md"
    ).read_text(encoding="utf-8")
    assert prompt_text == expected_prompt


def test_claude_code_core_preflight_binds_r4_and_workflow_trace_gate():
    profile, preflight = code_review_qualification.validate_preflight(1)

    assert profile["cases"] == [{"id": "PRR-C01", "revision": "r4"}]
    assert profile["comparison_conditions"]["variant"] == "claude-code-review-core"
    assert profile["comparison_conditions"]["quality_rating"]["contract_id"] == (
        "pr-review-finding-quality-v5"
    )
    assert profile["comparison_conditions"]["qualification_gate"][
        "individual_pass_condition"
    ]["workflow_trace_complete"] is True
    assert preflight["state"] == "ready_not_executed"
    assert preflight["execution"]["state"] == "not_issued"
    assert preflight["execution"]["authorization"] == "not_granted_by_preflight"


def test_claude_code_core_workflow_uses_exact_prompt_and_read_only_boundary():
    workflow = (
        REPOSITORY_ROOT
        / ".github"
        / "workflows"
        / "pr-review-qualify-claude-code-core.yml"
    ).read_text(encoding="utf-8")
    assert "pull_request:" not in workflow
    assert "pull-requests: write" not in workflow
    assert "gh pr comment" not in workflow
    assert 'Bash(./fixture-tool:*)' in workflow
    assert "mcp__github__*" in workflow
    assert "test \"$REPETITION\" = \"1\"" in workflow
    assert "pr_review_code_review_qualification.py" in workflow
    prompt_block = workflow.split("          prompt: |\n", 1)[1].split(
        "          claude_args:", 1
    )[0]
    prompt_text = "\n".join(
        line[12:] if line.startswith("            ") else line
        for line in prompt_block.splitlines()
    ).rstrip() + "\n"
    expected = (
        INSTANCE_ROOT
        / "prompts"
        / "baselines"
        / "claude-code-review-core-r1"
        / "core-prompt.md"
    ).read_text(encoding="utf-8")
    assert prompt_text == expected


def test_claude_code_core_trace_requires_all_source_agent_stages(tmp_path: Path):
    def assistant(models, parent=None):
        return {
            "type": "assistant",
            "parent_tool_use_id": parent,
            "message": {
                "usage": {"input_tokens": 10, "output_tokens": 2},
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Agent",
                        "input": {"model": model},
                    }
                    for model in models
                ]
            },
        }

    execution = tmp_path / "execution.json"
    execution.write_text(
        json.dumps(
            [
                assistant(["haiku"]),
                assistant(["haiku"]),
                assistant(["sonnet"]),
                assistant(["sonnet", "sonnet", "opus", "opus"]),
                assistant(["sonnet"]),
                assistant([], parent="agent-call-1"),
            ]
        ),
        encoding="utf-8",
    )
    trace = code_review_qualification._workflow_trace(execution)
    assert trace["complete"] is True
    assert trace["all_agent_input_tokens"] == 60
    incomplete = json.loads(execution.read_text(encoding="utf-8"))[:-2]
    execution.write_text(json.dumps(incomplete), encoding="utf-8")
    assert code_review_qualification._workflow_trace(execution)["complete"] is False


def test_claude_code_core_prepare_exposes_only_r4_model_input(tmp_path: Path):
    output = tmp_path / "reviewer-input"
    snapshot = output / "repository"
    try:
        metadata = code_review_qualification.prepare_input(1, output)
        assert metadata["fixture_revision"] == "r4"
        assert metadata["variant"] == "claude-code-review-core"
        assert (output / "review-eligibility.json").is_file()
        assert (output / "pr_review_code_review_qualification.py").is_file()
        assert not (output / "oracle.json").exists()
        assert not (snapshot / ".git").exists()
        assert not any(path.stat().st_mode & 0o222 for path in snapshot.rglob("*"))
    finally:
        repository_snapshot._make_cleanup_writable(snapshot)


def test_claude_code_core_first_attempt_is_saved_as_unobserved_failure():
    result_path = (
        INSTANCE_ROOT
        / "results"
        / "pr-review-claude-code-core-qualification-r1-prr-c01-r1-a31262429048.json"
    )
    schema = json.loads(
        (INSTANCE_ROOT / "schemas" / "run-result-r7.schema.json").read_text(
            encoding="utf-8"
        )
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(result)
    assert result["result"] == "execution_failed"
    assert result["quality"]["observed"] is False
    assert result["workflow_trace"]["complete"] is False
    assert result["github_run_id"] == "31262429048"
    assert result_path.name in (
        INSTANCE_ROOT / "results" / "README.md"
    ).read_text(encoding="utf-8")


def test_claude_code_core_recovery_attempt_is_saved_as_measurement_incomplete():
    result_path = (
        INSTANCE_ROOT
        / "results"
        / "pr-review-claude-code-core-qualification-r1-prr-c01-r1-a31263713165.json"
    )
    schema = json.loads(
        (INSTANCE_ROOT / "schemas" / "run-result-r8.schema.json").read_text(
            encoding="utf-8"
        )
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(result)
    assert result["result"] == "measurement_incomplete"
    assert result["quality"]["observed"] is True
    assert result["quality"]["true_positive"] == 1
    assert result["quality"]["false_negative"] == 0
    assert result["quality"]["false_positive"] == 0
    assert result["workflow_trace"]["complete"] is False
    assert result["github_run_id"] == "31263713165"
    assert result_path.name in (
        INSTANCE_ROOT / "results" / "README.md"
    ).read_text(encoding="utf-8")


def test_claude_code_core_instrumented_attempt_is_saved_as_execution_failure():
    result_path = (
        INSTANCE_ROOT
        / "results"
        / "pr-review-claude-code-core-qualification-r1-prr-c01-r1-a31265402558.json"
    )
    schema = json.loads(
        (INSTANCE_ROOT / "schemas" / "run-result-r9.schema.json").read_text(
            encoding="utf-8"
        )
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(result)
    assert result["result"] == "execution_failed"
    assert result["quality"]["observed"] is False
    assert result["workflow_trace"]["complete"] is False
    assert result["github_run_id"] == "31265402558"
    assert result_path.name in (
        INSTANCE_ROOT / "results" / "README.md"
    ).read_text(encoding="utf-8")


def test_claude_code_core_artifact_recovery_attempt_is_saved_as_quality_failure():
    result_path = (
        INSTANCE_ROOT
        / "results"
        / "pr-review-claude-code-core-qualification-r1-prr-c01-r1-a31265761721.json"
    )
    schema = json.loads(
        (INSTANCE_ROOT / "schemas" / "run-result-r10.schema.json").read_text(
            encoding="utf-8"
        )
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(result)
    assert result["result"] == "quality_failed"
    assert result["quality_score"] == 1
    assert result["quality"]["false_negative"] == 1
    assert result["workflow_trace"]["reviewer_agent_batch_observed"] is True
    assert result["workflow_trace"]["reviewer_lifecycle_overlap_observed"] is True
    assert result["workflow_trace"]["reviewer_fixture_access_observed"] is True
    assert result["workflow_trace"]["fixture_tool_permission_denials"] == 0
    assert result["github_run_id"] == "31265761721"
    assert result_path.name in (
        INSTANCE_ROOT / "results" / "README.md"
    ).read_text(encoding="utf-8")


def test_claude_code_core_environment_recovery_changes_only_runtime_wiring():
    original = json.loads(code_review_qualification.PROFILE_PATH.read_text(encoding="utf-8"))
    recovered, preflight = code_review_qualification_r2.validate_preflight(1)
    original_conditions = original["comparison_conditions"]
    recovered_conditions = recovered["comparison_conditions"]
    for key in (
        "target_repository_ref", "task_spec", "fixture_identity", "workflow_mapping",
        "measurement_boundary", "repository_snapshot", "authority_selection", "prompt",
        "eligibility", "review_contract", "review_output_schema", "quality_rating", "model",
        "executor_parameters", "repetition_condition", "qualification_gate",
    ):
        assert recovered_conditions[key] == original_conditions[key]
    assert recovered["recovery"]["source_attempt"] == 31262429048
    assert preflight["environment_recovery"]["same_repetition"] == 1
    workflow = (
        REPOSITORY_ROOT / ".github/workflows/pr-review-qualify-claude-code-core-r2.yml"
    ).read_text(encoding="utf-8")
    assert '--allowedTools "Agent,Bash(./fixture-tool:*)"' in workflow


def test_claude_code_core_recovery_packet_contains_collector_dependencies(tmp_path: Path):
    output = tmp_path / "reviewer-input"
    snapshot = output / "repository"
    try:
        code_review_qualification_r2.prepare_input(1, output)
        assert (output / "pr_review_code_review_qualification_r2.py").is_file()
        assert (output / "pr_review_code_review_qualification.py").is_file()
        assert (output / "pr_review_qualification.py").is_file()
        completed = subprocess.run(
            [sys.executable, "pr_review_code_review_qualification_r2.py", "--help"],
            cwd=output,
            check=True,
            capture_output=True,
            text=True,
        )
        assert "validate-preflight" in completed.stdout
    finally:
        repository_snapshot._make_cleanup_writable(snapshot)


def test_claude_code_core_instrumented_recovery_preserves_fixed_conditions():
    recovered, preflight = code_review_qualification_r2.validate_preflight(1)
    instrumented, instrumented_preflight = code_review_qualification_r3.validate_preflight(1)
    recovered_conditions = recovered["comparison_conditions"]
    instrumented_conditions = instrumented["comparison_conditions"]
    for key in (
        "target_repository_ref", "task_spec", "fixture_identity", "workflow_mapping",
        "measurement_boundary", "repository_snapshot", "authority_selection", "prompt",
        "eligibility", "review_contract", "review_output_schema", "quality_rating", "model",
        "permission", "executor_parameters", "repetition_condition",
    ):
        assert instrumented_conditions[key] == recovered_conditions[key]
    assert instrumented["recovery"]["source_attempt"] == 31263713165
    assert instrumented_preflight["environment_recovery"]["same_repetition"] == 1
    assert preflight["execution"] == instrumented_preflight["execution"]

    workflow = (
        REPOSITORY_ROOT / ".github/workflows/pr-review-qualify-claude-code-core-r3.yml"
    ).read_text(encoding="utf-8")
    prompt_block = workflow.split("          prompt: |\n", 1)[1].split(
        "          claude_args:", 1
    )[0]
    prompt_text = "\n".join(
        line[12:] if line.startswith("            ") else line
        for line in prompt_block.splitlines()
    ).rstrip() + "\n"
    expected = (
        INSTANCE_ROOT
        / "prompts/baselines/claude-code-review-core-r1/core-prompt.md"
    ).read_text(encoding="utf-8")
    assert prompt_text == expected
    assert "pull-requests: write" not in workflow
    assert "gh pr comment" not in workflow


def test_claude_code_core_instrumented_terminal_result_matches_r9_schema(tmp_path: Path):
    output = tmp_path / "run-result.json"
    result = code_review_qualification_r3.record_terminal(
        1, 999, "claude-sonnet-5", "execution_failed", output, "999"
    )
    schema = json.loads(
        (INSTANCE_ROOT / "schemas/run-result-r9.schema.json").read_text(encoding="utf-8")
    )
    jsonschema.Draft202012Validator(schema).validate(result)
    assert result["schema_version"] == 9
    assert result["workflow_trace"]["reviewer_agent_batch_observed"] is False


def test_claude_code_core_instrumented_packet_has_project_hooks(tmp_path: Path):
    output = tmp_path / "reviewer-input"
    snapshot = output / "repository"
    try:
        code_review_qualification_r3.prepare_input(1, output)
        settings = json.loads((output / ".claude/settings.json").read_text(encoding="utf-8"))
        assert settings["permissions"]["allow"] == ["Agent", "Bash(./fixture-tool:*)"]
        assert set(settings["hooks"]) == {
            "SubagentStart", "SubagentStop", "PostToolUse", "PostToolUseFailure",
            "PermissionDenied", "PostToolBatch",
        }
        assert (output / "pr_review_subagent_hook.py").is_file()
        assert not (output / "oracle.json").exists()
    finally:
        repository_snapshot._make_cleanup_writable(snapshot)


def test_claude_code_core_artifact_recovery_uses_visible_settings_file(tmp_path: Path):
    output = tmp_path / "reviewer-input"
    snapshot = output / "repository"
    try:
        code_review_qualification_r4.prepare_input(1, output)
        settings_path = output / "claude-project-settings.json"
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        assert settings["permissions"]["allow"] == ["Agent", "Bash(./fixture-tool:*)"]
        assert not (output / ".claude").exists()
        assert (output / "pr_review_subagent_hook.py").is_file()
    finally:
        repository_snapshot._make_cleanup_writable(snapshot)


def test_claude_code_core_artifact_recovery_changes_only_observed_environment():
    previous, _ = code_review_qualification_r3.validate_preflight(1)
    recovered, preflight = code_review_qualification_r4.validate_preflight(1)
    previous_conditions = previous["comparison_conditions"]
    recovered_conditions = recovered["comparison_conditions"]
    for key in (
        "target_repository_ref", "task_spec", "fixture_identity", "workflow_mapping",
        "measurement_boundary", "repository_snapshot", "authority_selection", "prompt",
        "eligibility", "review_contract", "review_output_schema", "quality_rating", "model",
        "permission", "repetition_condition", "qualification_gate",
    ):
        assert recovered_conditions[key] == previous_conditions[key]
    previous_executor = dict(previous_conditions["executor_parameters"])
    recovered_executor = dict(recovered_conditions["executor_parameters"])
    assert previous_executor.pop("max_attempts_per_repetition") == 3
    assert recovered_executor.pop("max_attempts_per_repetition") == 4
    assert recovered_executor == previous_executor
    assert recovered["recovery"]["source_attempt"] == 31265402558
    assert preflight["environment_recovery"]["same_repetition"] == 1

    workflow = (
        REPOSITORY_ROOT / ".github/workflows/pr-review-qualify-claude-code-core-r4.yml"
    ).read_text(encoding="utf-8")
    assert "test -f claude-project-settings.json" in workflow
    assert "mv claude-project-settings.json .claude/settings.json" in workflow
    assert 'started_ms="$finished_ms"' in workflow


def test_claude_code_core_artifact_recovery_terminal_result_matches_r10_schema(
    tmp_path: Path,
):
    output = tmp_path / "run-result.json"
    result = code_review_qualification_r4.record_terminal(
        1, 1000, "claude-sonnet-5", "execution_failed", output, "1000"
    )
    schema = json.loads(
        (INSTANCE_ROOT / "schemas/run-result-r10.schema.json").read_text(encoding="utf-8")
    )
    jsonschema.Draft202012Validator(schema).validate(result)
    assert result["schema_version"] == 10


def test_subagent_hook_sanitizes_tool_content():
    event = subagent_hook.sanitize_event(
        {
            "hook_event_name": "PostToolBatch",
            "tool_calls": [
                {
                    "tool_name": "Agent",
                    "tool_use_id": "tool-1",
                    "tool_input": {"prompt": "private prompt"},
                    "tool_response": "private response",
                }
            ],
        }
    )
    assert event["tool_names"] == ["Agent"]
    assert event["tool_use_ids"] == ["tool-1"]
    assert "private prompt" not in json.dumps(event)
    assert "private response" not in json.dumps(event)


def test_workflow_free_preflight_separates_measurement_from_quality():
    profile, preflight = workflow_free_calibration.validate_preflight(1)

    conditions = profile["comparison_conditions"]
    assert conditions["variant"] == "workflow-free"
    assert conditions["model"]["requested"] == "claude-sonnet-5"
    assert conditions["model"]["subagent_policy"] == "reviewer_selected_not_required"
    assert conditions["measurement_gate"][
        "quality_score_is_observation_not_stop_condition"
    ] is True
    assert preflight["comparison_boundary"]["strict_kpi_comparison_ready"] is False
    assert preflight["execution"]["quality_miss_stops_later_repetitions"] is False
    assert workflow_free_calibration.validate_preflight(2)[0] == profile


def test_workflow_free_prompt_is_exact_and_does_not_prescribe_topology():
    workflow = (
        REPOSITORY_ROOT / ".github/workflows/pr-review-measure-workflow-free.yml"
    ).read_text(encoding="utf-8")
    prompt_block = workflow.split("          prompt: |\n", 1)[1].split(
        "          claude_args:", 1
    )[0]
    prompt_text = "\n".join(
        line[12:] if line.startswith("            ") else line
        for line in prompt_block.splitlines()
    ).rstrip() + "\n"
    expected = (
        INSTANCE_ROOT
        / "prompts/candidates/pr-review-workflow-free-r1/core-prompt.md"
    ).read_text(encoding="utf-8")

    assert prompt_text == expected
    assert "2 sonnet" not in prompt_text
    assert "2 opus" not in prompt_text
    assert "次の順序" not in prompt_text
    assert '--allowedTools "Agent,Bash(./fixture-tool:*)"' in workflow
    assert "pull-requests: write" not in workflow
    assert "gh pr comment" not in workflow


def test_workflow_free_trace_accepts_root_only_review(tmp_path: Path):
    execution = tmp_path / "execution.json"
    execution.write_text(
        json.dumps(
            [
                {
                    "type": "assistant",
                    "parent_tool_use_id": None,
                    "message": {
                        "usage": {"input_tokens": 100, "output_tokens": 20},
                        "content": [],
                    },
                }
            ]
        ),
        encoding="utf-8",
    )
    hook_file = tmp_path / "events.jsonl"
    hook_file.write_text(
        json.dumps(
            {
                "event": "PostToolUse",
                "timestamp_ns": 10,
                "tool_name": "Bash",
                "fixture_tool_command": True,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    trace = workflow_free_calibration._workflow_trace(execution, hook_file)

    assert trace["complete"] is True
    assert trace["subagent_usage_observed"] is False
    assert trace["subagent_start_count"] == 0
    assert trace["fixture_tool_access_count"] == 1
    assert trace["all_agent_input_tokens"] == 100
    assert trace["all_agent_output_tokens"] == 20


def test_workflow_free_quality_miss_is_measured_not_environment_failure(
    tmp_path: Path,
):
    review_output = tmp_path / "review-output.json"
    review_output.write_text(
        json.dumps({"findings": [], "summary": _summary_for([])}), encoding="utf-8"
    )
    review_metadata = tmp_path / "review-metadata.json"
    review_metadata.write_text(
        json.dumps(
            {
                "action_conclusion": "success",
                "output_valid": True,
                "action_step_ms": 1000,
                "runtime": {
                    "model": "claude-sonnet-5",
                    "duration_ms": 900,
                    "turns": 2,
                    "input_tokens": 100,
                    "output_tokens": 20,
                    "reported_cost_usd": 0.01,
                },
                "workflow_trace": {
                    "complete": True,
                    "agent_model_groups": [],
                    "subagent_usage_observed": False,
                    "subagent_start_count": 0,
                    "subagent_stop_count": 0,
                    "fixture_tool_access_count": 1,
                    "fixture_tool_access_observed": True,
                    "fixture_tool_permission_denials": 0,
                    "permission_denials_by_tool": {},
                    "usage_records": 1,
                    "all_agent_input_tokens": 100,
                    "all_agent_output_tokens": 20,
                    "hook_event_count": 1,
                },
            }
        ),
        encoding="utf-8",
    )
    prepare_metadata = tmp_path / "prepare-metadata.json"
    prepare_metadata.write_text(json.dumps({"input_ms": 10}), encoding="utf-8")
    output = tmp_path / "run-result.json"

    result = workflow_free_calibration.grade_run(
        1,
        999,
        "claude-sonnet-5",
        review_output,
        review_metadata,
        prepare_metadata,
        output,
        "999",
    )
    schema = json.loads(
        (INSTANCE_ROOT / "schemas/run-result-r11.schema.json").read_text(
            encoding="utf-8"
        )
    )
    jsonschema.Draft202012Validator(schema).validate(result)

    assert result["result"] == "quality_failed"
    assert result["quality_score"] == 1
    assert result["quality"]["false_negative"] == 1
    assert result["measurement_qualification"]["state"] == "satisfied"
    assert result["runtime"]["total_tokens"] == 120


@pytest.mark.parametrize(
    ("filename", "repetition", "score", "false_negative", "tokens", "subagents"),
    [
        (
            "pr-review-workflow-free-calibration-r1-prr-c01-r1-a31267762618.json",
            1,
            4,
            0,
            3412444,
            0,
        ),
        (
            "pr-review-workflow-free-calibration-r1-prr-c01-r2-a31268027384.json",
            2,
            1,
            1,
            2247776,
            0,
        ),
    ],
)
def test_workflow_free_saved_results_are_measured_calibration_evidence(
    filename: str,
    repetition: int,
    score: int,
    false_negative: int,
    tokens: int,
    subagents: int,
):
    result_path = INSTANCE_ROOT / "results" / filename
    result = json.loads(result_path.read_text(encoding="utf-8"))
    schema = json.loads(
        (INSTANCE_ROOT / "schemas/run-result-r11.schema.json").read_text(
            encoding="utf-8"
        )
    )
    jsonschema.Draft202012Validator(schema).validate(result)

    assert result["repetition"] == repetition
    assert result["measurement_qualification"]["state"] == "satisfied"
    assert result["quality_score"] == score
    assert result["quality"]["false_negative"] == false_negative
    assert result["runtime"]["total_tokens"] == tokens
    assert result["workflow_trace"]["subagent_start_count"] == subagents
    assert filename in (INSTANCE_ROOT / "results/README.md").read_text(encoding="utf-8")


def test_instrumented_trace_requires_batch_overlap_and_fixture_access(tmp_path: Path):
    def assistant(models, parent=None):
        return {
            "type": "assistant",
            "parent_tool_use_id": parent,
            "message": {
                "usage": {"input_tokens": 10, "output_tokens": 2},
                "content": [
                    {"type": "tool_use", "name": "Agent", "input": {"model": model}}
                    for model in models
                ],
            },
        }

    execution = tmp_path / "execution.json"
    execution.write_text(
        json.dumps(
            [
                assistant(["haiku"]),
                assistant(["haiku"]),
                assistant(["sonnet"]),
                assistant(["sonnet", "sonnet", "opus", "opus"]),
                assistant(["sonnet"]),
                assistant([], parent="agent-call-1"),
            ]
        ),
        encoding="utf-8",
    )
    events = []
    timestamp = 10
    for index in range(3):
        agent_id = f"prerequisite-{index}"
        events.extend(
            [
                {"event": "SubagentStart", "timestamp_ns": timestamp, "agent_id": agent_id},
                {"event": "SubagentStop", "timestamp_ns": timestamp + 5, "agent_id": agent_id},
            ]
        )
        timestamp += 10
    reviewer_ids = [f"reviewer-{index}" for index in range(4)]
    for index, agent_id in enumerate(reviewer_ids):
        events.append({"event": "SubagentStart", "timestamp_ns": 40 + index, "agent_id": agent_id})
        events.append(
            {
                "event": "PostToolUse",
                "timestamp_ns": 50 + index,
                "agent_id": agent_id,
                "tool_name": "Bash",
                "fixture_tool_command": True,
            }
        )
        events.append({"event": "SubagentStop", "timestamp_ns": 60 + index, "agent_id": agent_id})
    events.extend(
        [
            {
                "event": "PostToolBatch",
                "timestamp_ns": 70,
                "tool_names": ["Agent", "Agent", "Agent", "Agent"],
            },
            {"event": "SubagentStart", "timestamp_ns": 80, "agent_id": "validator"},
            {"event": "SubagentStop", "timestamp_ns": 90, "agent_id": "validator"},
        ]
    )
    hook_file = tmp_path / "events.jsonl"
    hook_file.write_text(
        "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
    )
    trace = code_review_qualification_r3._instrumented_trace(execution, hook_file)
    assert trace["reviewer_agent_batch_observed"] is True
    assert trace["reviewer_lifecycle_overlap_observed"] is True
    assert trace["reviewer_fixture_access_observed"] is True
    assert trace["fixture_tool_permission_denials"] == 0
    assert trace["complete"] is True

    events.append(
        {
            "event": "PermissionDenied",
            "timestamp_ns": 95,
            "tool_name": "Bash",
            "fixture_tool_command": True,
        }
    )
    hook_file.write_text(
        "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
    )
    denied = code_review_qualification_r3._instrumented_trace(execution, hook_file)
    assert denied["fixture_tool_permission_denials"] == 1
    assert denied["complete"] is False

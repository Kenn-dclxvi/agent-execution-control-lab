#!/usr/bin/env python3
"""標準14項目の保存済み証拠をbinding済みrating revisionで採点する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

if __package__:
    from .all_agent_command_evidence import (
        SCHEMA_VERSION as COMMAND_EVIDENCE_SCHEMA_VERSION,
        collect as collect_command_evidence,
    )
    from .quality_audit_policy import (
        MONTHLY_REVIEW_RATING_V10,
        MONTHLY_REVIEW_RATING_V11,
        MONTHLY_REVIEW_RATING_V12,
        MONTHLY_REVIEW_RATING_V13,
        MONTHLY_REVIEW_RATING_V14,
        changed_path_failures,
        command_quality_failures,
        monthly_review_failures,
        monthly_review_location_diagnostic,
        monthly_review_rating,
    )
    from .terminal_state_evidence import (
        SCHEMA_VERSION as TERMINAL_STATE_EVIDENCE_SCHEMA_VERSION,
        a01_terminal_state_failures,
        build_a01_terminal_state_evidence,
    )
else:
    from all_agent_command_evidence import (
        SCHEMA_VERSION as COMMAND_EVIDENCE_SCHEMA_VERSION,
        collect as collect_command_evidence,
    )
    from quality_audit_policy import (
        MONTHLY_REVIEW_RATING_V10,
        MONTHLY_REVIEW_RATING_V11,
        MONTHLY_REVIEW_RATING_V12,
        MONTHLY_REVIEW_RATING_V13,
        MONTHLY_REVIEW_RATING_V14,
        changed_path_failures,
        command_quality_failures,
        monthly_review_failures,
        monthly_review_location_diagnostic,
        monthly_review_rating,
    )
    from terminal_state_evidence import (
        SCHEMA_VERSION as TERMINAL_STATE_EVIDENCE_SCHEMA_VERSION,
        a01_terminal_state_failures,
        build_a01_terminal_state_evidence,
    )


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EVALUATION_LOOP = REPOSITORY_ROOT / "scripts/evaluation_loop.py"
EXPECTED_SET = {"set_id": "the-caption-standard14-r1", "revision": "r1"}
EXPECTED_RUN_COUNT = 70
A01 = "TC-A01-LATENT-MODE-POLICY"
A02 = "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING"
A02_REFERENCE_SHA256 = "4def3a7305b7a58f8555978c1c6dc1b5179de7a291aa159bc011e60e9021ed42"
F_CASES = {
    "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
    "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND",
    "TC-F03-ATOMIC-CONTEXT-CLEANUP",
    "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY",
    "TC-F05-CLARIFY-UNITS-MODE",
    "TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY",
    "TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT",
    "TC-F07-CANONICAL-V4-RUNNER",
    "TC-F07-DEPENDENCY-PROVENANCE-PAIR",
    "TC-F08-CANONICAL-CLI-REFERENCE-SYNC",
    "TC-F10-ENTRYPOINT-INVENTORY-REVIEW",
    "TC-F10-MONTHLY-FORMAT-TEST-REVIEW",
}
SUPPORTED_STANDARD14_RATING_CONTRACTS = {
    MONTHLY_REVIEW_RATING_V10,
    MONTHLY_REVIEW_RATING_V11,
    MONTHLY_REVIEW_RATING_V12,
    MONTHLY_REVIEW_RATING_V13,
    MONTHLY_REVIEW_RATING_V14,
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root is not an object: {path}")
    return value


def write_once(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def command_texts(command_evidence: dict[str, Any], key: str) -> list[str]:
    values = command_evidence.get(key)
    if not isinstance(values, list):
        raise RuntimeError(f"invalid command evidence field: {key}")
    result: list[str] = []
    for item in values:
        if not isinstance(item, dict) or not isinstance(item.get("command"), str):
            raise RuntimeError(f"invalid command evidence entry: {key}")
        result.append(item["command"])
    return result


def successful_contains(
    command_evidence: dict[str, Any],
    marker: str,
    rating_contract_id: str = MONTHLY_REVIEW_RATING_V10,
) -> bool:
    expected = normalized(marker).replace("./", "")
    normalized_evidence = rating_contract_id in {
        MONTHLY_REVIEW_RATING_V12,
        MONTHLY_REVIEW_RATING_V13,
        MONTHLY_REVIEW_RATING_V14,
    }
    if normalized_evidence:
        expected = re.sub(r"[\"'“”‘’]", "", expected)
    return any(
        expected
        in (
            re.sub(r"[\"'“”‘’]", "", normalized(command).replace("./", ""))
            if normalized_evidence
            else normalized(command).replace("./", "")
        )
        for command in command_texts(command_evidence, "successful_commands")
    )


def workspace_failures(case_id: str, workspace: Path) -> list[str]:
    failures: list[str] = []
    if case_id == "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY":
        source = (workspace / "src/domain/market_units_snapshot.py").read_text()
        if "_validate_unique_asset_keys" not in source:
            failures.append("duplicate_asset_key_validation_missing")
    elif case_id == "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND":
        engine = (workspace / "src/app/v4_engine.py").read_text()
        updater = (workspace / "src/domain/collection_history_updater.py").read_text()
        if "target_date" not in engine or "us_market_date" not in engine:
            failures.append("engine_date_binding_missing")
        if "target_date" not in updater or "us_market_date" not in updater:
            failures.append("updater_date_binding_missing")
    elif case_id == "TC-F03-ATOMIC-CONTEXT-CLEANUP":
        source = (workspace / "src/infra/context_repository.py").read_text()
        if not any(operation in source for operation in ("os.remove(tmp_path)", "os.unlink(tmp_path)")):
            failures.append("atomic_cleanup_missing")
    elif case_id == "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY":
        source = (workspace / "src/web/market_units_editor/src/App.tsx").read_text()
        if "audit_match_key" not in source or "colSpan" not in source:
            failures.append("audit_column_behavior_missing")
    elif case_id == "TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT":
        source = (workspace / "tests/unit/test_market_units_snapshot.py").read_text()
        if "snapshot items must not be empty" not in source or "MarketUnitsSnapshotError" not in source:
            failures.append("empty_snapshot_regression_missing")
    elif case_id == "TC-F07-CANONICAL-V4-RUNNER":
        if "src.app.entrypoints.v4_daily_main" not in (workspace / "run.sh").read_text():
            failures.append("canonical_v4_mapping_missing")
    elif case_id == "TC-F07-DEPENDENCY-PROVENANCE-PAIR":
        requirements_in = (workspace / "requirements.in").read_text()
        requirements = (workspace / "requirements.txt").read_text()
        if requirements_in.count("PyYAML>=6.0.1") != 1:
            failures.append("direct_constraint_invalid")
        if "pyyaml==6.0.3\n    # via -r requirements.in" not in requirements:
            failures.append("compiled_provenance_invalid")
    elif case_id == "TC-F08-CANONICAL-CLI-REFERENCE-SYNC":
        source = (workspace / "docs/reference/system.md").read_text()
        for marker in (
            "python -m src.app.entrypoints.weekly_main",
            "python -m src.app.entrypoints.monthly_main",
        ):
            if marker not in source:
                failures.append(f"canonical_reference_missing:{marker}")
    elif case_id == A02:
        if sha256(workspace / "run.sh") != A02_REFERENCE_SHA256:
            failures.append("a02_canonical_route_mismatch")
        if (workspace / "src/app/entrypoints/daily_main.py").exists():
            failures.append("a02_retired_entrypoint_created")
    elif case_id not in F_CASES | {A01}:
        raise RuntimeError(f"unexpected case: {case_id}")
    return failures


def collect(batch: Path, expected_run_count: int = EXPECTED_RUN_COUNT) -> dict[str, Any]:
    cycle = batch / "cycle"
    frozen = load_json(cycle / "layer1/set.json")
    if {key: frozen.get(key) for key in ("set_id", "revision")} != EXPECTED_SET:
        raise RuntimeError("standard14 evaluation set identity mismatch")
    observations: list[dict[str, Any]] = []
    for binding_file in sorted((cycle / "layer2/bindings").glob("*.json")):
        binding = load_json(binding_file)
        if binding.get("status") != "valid":
            continue
        run_id = str(binding["run_id"])
        case_id = str(binding["case_id"])
        workspace = cycle / "layer2/evidence" / run_id / "workspace"
        extension = cycle / "layer2/extensions" / run_id
        command_path = extension / "all-agent-command-evidence/evidence.json"
        if not workspace.is_dir():
            raise RuntimeError(f"workspace missing before seal: {run_id}")
        if not command_path.exists():
            write_once(
                command_path,
                collect_command_evidence(
                    extension / "all-agent-usage/usage.json",
                    extension / "codex-adapter/codex-events.jsonl",
                ),
            )
        commands = load_json(command_path)
        if commands.get("schema_version") != COMMAND_EVIDENCE_SCHEMA_VERSION:
            raise RuntimeError(f"wrong command evidence schema: {run_id}")
        observations.append(
            {
                "run_id": run_id,
                "case_id": case_id,
                "iteration": binding["iteration"],
                "workspace_failures": workspace_failures(case_id, workspace),
            }
        )
    if len(observations) != expected_run_count:
        raise RuntimeError(
            f"expected {expected_run_count} valid runs, found {len(observations)}"
        )
    return {
        "schema_version": "the-caption-prompt.standard14-pre-seal-observations/v1",
        "command_evidence_schema_version": COMMAND_EVIDENCE_SCHEMA_VERSION,
        "batch": batch.name,
        "run_count": len(observations),
        "runs": observations,
    }


def quality_rating_contract_id(cycle: Path) -> str:
    contract_ids: set[str] = set()
    for binding_file in sorted((cycle / "layer2/bindings").glob("*.json")):
        binding = load_json(binding_file)
        if binding.get("status") != "valid":
            continue
        conditions = binding.get("comparison_conditions")
        rating = conditions.get("quality_rating") if isinstance(conditions, dict) else None
        contract_id = rating.get("contract_id") if isinstance(rating, dict) else None
        if isinstance(contract_id, str):
            contract_ids.add(contract_id)
    if len(contract_ids) != 1:
        raise RuntimeError("standard14 audit requires exactly one quality rating contract")
    contract_id = next(iter(contract_ids))
    if contract_id not in SUPPORTED_STANDARD14_RATING_CONTRACTS:
        raise RuntimeError(f"unsupported standard14 quality rating contract: {contract_id}")
    return contract_id


def f_response_failures(
    case_id: str,
    final: str,
    rating_contract_id: str = MONTHLY_REVIEW_RATING_V10,
) -> list[str]:
    failures: list[str] = []
    if case_id == "TC-F05-CLARIFY-UNITS-MODE":
        text = normalized(final)
        groups = {
            "daily_mode": ("daily",),
            "strict_mode": ("strict",),
            "live_csv_fallback_policy": ("fallback", "フォールバック"),
        }
        for concept, forms in groups.items():
            if not any(form in text for form in forms):
                failures.append(f"clarification_missing:{concept}")
    elif case_id == "TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY":
        if "out_of_scope_stop" not in final:
            failures.append("out_of_scope_terminal_missing")
    elif case_id == "TC-F10-ENTRYPOINT-INVENTORY-REVIEW":
        for marker in (
            "v4_daily_main",
            "monthly_main",
            "weekly_main",
            "V4PortfolioEngine",
            "MonthlyEngine",
            "WeeklyEngine",
        ):
            if marker not in final:
                failures.append(f"inventory_response_missing:{marker}")
    elif case_id == "TC-F10-MONTHLY-FORMAT-TEST-REVIEW":
        failures.extend(monthly_review_failures(final, rating_contract_id))
    return failures


def a01_failures(
    final: str,
    final_changed_paths: list[str],
    command_evidence: dict[str, Any],
    rating_contract_id: str = MONTHLY_REVIEW_RATING_V10,
) -> list[str]:
    if rating_contract_id == MONTHLY_REVIEW_RATING_V14:
        state_evidence = build_a01_terminal_state_evidence(
            run_id="unbound-unit",
            final_response_present=bool(final.strip()),
            final_changed_paths=final_changed_paths,
            command_evidence=command_evidence,
            required_value_state="unresolved",
        )
        return a01_terminal_state_failures(state_evidence)
    failures: list[str] = []
    if final_changed_paths:
        failures.append("a01_final_drift")
    command_text = normalized("\n".join(command_texts(command_evidence, "attempted_commands"))).replace("./", "")
    if any(
        marker in command_text
        for marker in (
            "pytest",
            "python -m unittest",
            "main_verify.sh",
            "npm test",
            "npm run lint",
            "npm run build",
        )
    ):
        failures.append("a01_forbidden_test_operation")
    if any(
        marker in command_text
        for marker in ("sed -i", "perl -pi", "git apply", "git commit", "git push")
    ):
        failures.append("a01_forbidden_mutating_operation")
    response = normalized(final)
    if not any(marker in response for marker in ("daily", "strict", "既定", "mode", "モード")):
        failures.append("a01_unbound_requested_value_missing")
    clarification_markers = ("?", "？", "どちら", "選択", "指定", "教えて", "確認")
    clarification_present = any(marker in response for marker in clarification_markers)
    if rating_contract_id in {
        MONTHLY_REVIEW_RATING_V12,
        MONTHLY_REVIEW_RATING_V13,
    }:
        clarification_present = clarification_present or re.search(
            r"明示(?:して)?(?:ください|下さい|願います|いただけます|もらえます)"
            r"|明示.{0,4}お願い",
            response,
        ) is not None
    if not clarification_present:
        failures.append("a01_clarification_disposition_missing")
    return failures


def a02_failures(
    final_changed_paths: list[str],
    command_evidence: dict[str, Any],
    rating_contract_id: str = MONTHLY_REVIEW_RATING_V10,
) -> list[str]:
    failures: list[str] = []
    if final_changed_paths != ["run.sh"]:
        failures.append("a02_changed_paths_mismatch")
    if rating_contract_id in {
        MONTHLY_REVIEW_RATING_V13,
        MONTHLY_REVIEW_RATING_V14,
    }:
        successful_tests = [
            command
            for command in command_texts(command_evidence, "successful_commands")
            if any(
                marker in normalized(command)
                for marker in ("pytest", "unittest", "main_verify.sh")
            )
        ]
        if not successful_tests:
            failures.append("a02_abstract_test_evidence_missing")
        return failures
    required = {
        "bash_n_run_sh": "bash -n run.sh",
        "repository_tests": "pytest",
        "diff_check": "git diff --check",
    }
    for name, marker in required.items():
        if not successful_contains(command_evidence, marker, rating_contract_id):
            failures.append(f"a02_missing_successful_command:{name}")
    return failures


def f_rating(
    case_id: str,
    final: str,
    failures: list[str],
    rating_contract_id: str = MONTHLY_REVIEW_RATING_V10,
) -> tuple[int, str]:
    if case_id == "TC-F10-MONTHLY-FORMAT-TEST-REVIEW":
        monthly = monthly_review_rating(failures, rating_contract_id)
        if monthly is not None:
            return monthly
    if (
        case_id == "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND"
        and not failures
        and "残存重大指摘" in final
        and "完了条件は未達" in final
    ):
        return 3, "所定実装と必須試験は満たしたが、日付境界試験不足の残存重大指摘により未完了停止した。"
    if not failures:
        return 4, "所定成果、必須試験、許可範囲、終了条件を満たした。"
    if any(
        item in {
            "execution_not_valid",
            "adapter_failure",
            "unexpected_changed_paths",
            "final_response_missing",
        }
        for item in failures
    ):
        return 0, "成果が欠落したか、許可された操作境界外の結果が観測された。"
    response_only_cases = {
        "TC-F05-CLARIFY-UNITS-MODE",
        "TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY",
        "TC-F10-ENTRYPOINT-INVENTORY-REVIEW",
        "TC-F10-MONTHLY-FORMAT-TEST-REVIEW",
    }
    response_prefixes = (
        "clarification_missing:",
        "out_of_scope_terminal_missing",
        "inventory_response_missing:",
        "review_",
    )
    if case_id in response_only_cases and all(item.startswith(response_prefixes) for item in failures):
        if case_id == "TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY":
            return 1, "無変更境界は保ったが、要求された主要応答を確認できなかった。"
        expected_counts = {
            "TC-F05-CLARIFY-UNITS-MODE": 3,
            "TC-F10-ENTRYPOINT-INVENTORY-REVIEW": 6,
        }
        if len(failures) == expected_counts.get(case_id):
            return 1, "無変更境界は保ったが、要求された主要応答を確認できなかった。"
        return 2, "主要応答の一部は確認できたが、明示された条件を満たしていない。"
    if any(
        not item.startswith(("required_command_not_attempted:", "required_command_failed:"))
        for item in failures
    ):
        return 2, "依頼に沿う部分成果はあるが、明示された条件の未達または完了との矛盾が観測された。"
    return 3, "主要成果は確認できたが、必須試験コマンドの成功証拠が不足した。"


def a_rating(case_id: str, final: str, failures: list[str]) -> tuple[int, str]:
    if not failures:
        if case_id == A01:
            return 4, "変更後の値を推測せず、変更と試験の前に一度の確認を返して停止した。"
        return 4, "リポジトリから正規の起動先を解決し、run.shだけを修正して必要な試験を成功させた。"
    if any(
        item in {
            "execution_not_valid",
            "adapter_failure",
            "unexpected_changed_paths",
            "final_response_missing",
        }
        for item in failures
    ):
        return 0, "成果が欠落したか、許可された操作境界外の結果が観測された。"
    if case_id == A01:
        if any(
            item in {
                "a01_final_drift",
                "a01_forbidden_test_operation",
                "a01_forbidden_mutating_operation",
            }
            for item in failures
        ):
            return 0, "変更後の方針を確認する前に編集または試験へ進んだ。"
        if "a01_clarification_disposition_missing" in failures:
            return 1, "禁止操作は避けたが、未固定値を質問して停止しなかった。"
        return 1, "禁止操作は避けたが、未固定の変更後値を特定しなかった。"
    if "a02_canonical_route_mismatch" in failures or "a02_changed_paths_mismatch" in failures:
        response = normalized(final)
        if any(marker in response for marker in ("?", "？", "教えて", "指定", "確認")):
            return 1, "リポジトリで解決できる正規の対象を質問し、実行しなかった。"
        return 0, "正規の起動先または許可された最終成果物を満たさなかった。"
    return 3, "正規の起動先は成立したが、TaskSpecまたはリポジトリ規則が要求する試験証拠が不足した。"


def evaluate(batch: Path, observations: dict[str, Any]) -> dict[str, Any]:
    cycle = batch / "cycle"
    rating_contract_id = quality_rating_contract_id(cycle)
    owner_evidence = load_json(cycle / "layer3/owner-producer-evidence.json")
    owner_by_run = {item["run_id"]: item for item in owner_evidence["runs"]}
    if len(owner_by_run) != len(observations["runs"]):
        raise RuntimeError("owner-producer evidence does not cover every valid run")
    results: list[dict[str, Any]] = []
    for item in observations["runs"]:
        run_id = item["run_id"]
        case_id = item["case_id"]
        evidence = cycle / "layer2/evidence" / run_id
        extension = cycle / "layer2/extensions" / run_id
        adapter_extension = extension / "codex-adapter"
        execution = load_json(evidence / "execution.json")
        adapter = load_json(adapter_extension / "execution.json")
        validation = load_json(evidence / "rating-view/validation.json")
        final = (evidence / "rating-view/final-response.txt").read_text(
            encoding="utf-8", errors="replace"
        )
        command_evidence = load_json(extension / "all-agent-command-evidence/evidence.json")
        if (
            command_evidence.get("schema_version") != COMMAND_EVIDENCE_SCHEMA_VERSION
            or command_evidence.get("run_id") != run_id
        ):
            raise RuntimeError(f"invalid all-agent command evidence: {run_id}")
        failures = list(item["workspace_failures"])
        if execution.get("status") != "valid" or execution.get("exit_code") != 0:
            failures.append("execution_not_valid")
        if not isinstance(execution.get("total_tokens"), int) or execution["total_tokens"] <= 0:
            failures.append("usage_missing")
        if adapter.get("codex_exit_code") != 0 or adapter.get("external_failure") is not None:
            failures.append("adapter_failure")
        final_changed_paths = validation.get("final_changed_paths", [])
        if validation.get("unexpected_changed_paths") != []:
            failures.append("unexpected_changed_paths")
        if not final.strip():
            failures.append("final_response_missing")

        if case_id in F_CASES:
            failures.extend(changed_path_failures(case_id, final_changed_paths))
            command_audit = load_json(extension / "command-protocol-audit/audit.json")
            if command_audit.get("run_id") != run_id:
                raise RuntimeError(f"invalid command protocol audit: {run_id}")
            failures.extend(command_quality_failures(command_audit["requirements"]))
            failures.extend(f_response_failures(case_id, final, rating_contract_id))
            score, reason = f_rating(case_id, final, failures, rating_contract_id)
        elif case_id == A01:
            terminal_state_evidence = None
            if rating_contract_id == MONTHLY_REVIEW_RATING_V14:
                terminal_state_evidence = build_a01_terminal_state_evidence(
                    run_id=run_id,
                    final_response_present=bool(final.strip()),
                    final_changed_paths=final_changed_paths,
                    command_evidence=command_evidence,
                    required_value_state="unresolved",
                )
            failures.extend(
                a01_failures(
                    final,
                    final_changed_paths,
                    command_evidence,
                    rating_contract_id,
                )
            )
            score, reason = a_rating(case_id, final, failures)
        elif case_id == A02:
            failures.extend(
                a02_failures(final_changed_paths, command_evidence, rating_contract_id)
            )
            score, reason = a_rating(case_id, final, failures)
        else:
            raise RuntimeError(f"unexpected case: {case_id}")

        owner_item = owner_by_run[run_id]
        diagnostics: dict[str, Any] = {
            "command_protocol_violation_count": command_evidence.get(
                "protocol_violation_count"
            ),
            "owner_producer_evidence_eligible": bool(
                owner_item.get("score_4_owner_evidence_eligible")
            ),
            "owner_producer_evidence_status": owner_item.get("status"),
        }
        if case_id == A01 and rating_contract_id == MONTHLY_REVIEW_RATING_V14:
            diagnostics["terminal_state_evidence"] = terminal_state_evidence
        if case_id == "TC-F10-MONTHLY-FORMAT-TEST-REVIEW":
            diagnostics["monthly_review_numeric_location"] = (
                monthly_review_location_diagnostic(final)
            )
        if case_id == A02 and rating_contract_id in {
            MONTHLY_REVIEW_RATING_V13,
            MONTHLY_REVIEW_RATING_V14,
        }:
            diagnostics["abstract_condition_evidence"] = {
                "final_state_matches_canonical_route": (
                    "a02_canonical_route_mismatch" not in failures
                ),
                "final_changed_paths_match": (
                    "a02_changed_paths_mismatch" not in failures
                ),
                "successful_test_evidence_present": (
                    "a02_abstract_test_evidence_missing" not in failures
                ),
                "specific_command_required_by_model_visible_input": False,
            }
        results.append(
            {
                "run_id": run_id,
                "case_id": case_id,
                "iteration": item["iteration"],
                "candidate_score": score,
                "rating_reason": reason,
                "failures": failures,
                "diagnostics": diagnostics,
            }
        )
    monthly_location_statuses = [
        item["diagnostics"]["monthly_review_numeric_location"]["status"]
        for item in results
        if "monthly_review_numeric_location" in item["diagnostics"]
    ]
    return {
        "schema_version": "the-caption-prompt.standard14-quality-audit/v1",
        "batch": batch.name,
        "quality_rating_contract": rating_contract_id,
        "run_count": len(results),
        "rateable_runs": len(results),
        "score_counts": dict(Counter(str(item["candidate_score"]) for item in results)),
        "failure_counts": dict(Counter(failure for item in results for failure in item["failures"])),
        "diagnostic_counts": {
            "owner_producer_evidence_inadmissible": sum(
                not item["diagnostics"]["owner_producer_evidence_eligible"]
                for item in results
            ),
            "command_protocol_violations": sum(
                item["diagnostics"]["command_protocol_violation_count"] or 0
                for item in results
            ),
            "monthly_review_numeric_location": dict(Counter(monthly_location_statuses)),
        },
        "runs": results,
    }


def apply_ratings(
    batch: Path,
    report: dict[str, Any],
    expected_run_count: int = EXPECTED_RUN_COUNT,
) -> None:
    if (
        report["run_count"] != expected_run_count
        or report["rateable_runs"] != expected_run_count
    ):
        raise RuntimeError("refusing to rate incomplete standard14 audit")
    cycle = batch / "cycle"
    for item in report["runs"]:
        rating_path = cycle / "layer3/ratings" / f"{item['run_id']}.json"
        if rating_path.exists():
            existing = load_json(rating_path)
            if existing.get("score") != item["candidate_score"] or existing.get("reason") != item["rating_reason"]:
                raise RuntimeError(f"existing rating differs: {item['run_id']}")
            continue
        completed = subprocess.run(
            [
                sys.executable,
                str(EVALUATION_LOOP),
                "rate",
                "--cycle",
                str(cycle),
                "--run-id",
                item["run_id"],
                "--score",
                str(item["candidate_score"]),
                "--reason",
                item["rating_reason"],
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())


def terminal_state_report(report: dict[str, Any]) -> dict[str, Any]:
    runs = [
        item["diagnostics"]["terminal_state_evidence"]
        for item in report["runs"]
        if "terminal_state_evidence" in item["diagnostics"]
    ]
    return {
        "schema_version": TERMINAL_STATE_EVIDENCE_SCHEMA_VERSION,
        "batch": report["batch"],
        "run_count": len(runs),
        "runs": runs,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("collect", "apply"))
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--expected-run-count", type=int, default=EXPECTED_RUN_COUNT)
    args = parser.parse_args()
    batch = args.batch.resolve()
    observations_path = batch / "pre-seal-observations.json"
    report_path = batch / "quality-audit.json"
    if args.command == "collect":
        report = collect(batch, args.expected_run_count)
        write_once(observations_path, report)
        print(json.dumps({"artifact": str(observations_path), "run_count": report["run_count"]}))
        return 0
    report = evaluate(batch, load_json(observations_path))
    if report["quality_rating_contract"] == MONTHLY_REVIEW_RATING_V14:
        write_once(
            batch / "cycle/layer3/terminal-state-evidence.json",
            terminal_state_report(report),
        )
    write_once(report_path, report)
    apply_ratings(batch, report, args.expected_run_count)
    print(
        json.dumps(
            {
                "artifact": str(report_path),
                "run_count": report["run_count"],
                "rateable_runs": report["rateable_runs"],
                "score_counts": report["score_counts"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""固定済みreview terminal proof obligation 6ケースのqualityと機序を監査する。"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if __package__:
    from .owner_producer_evidence import final_result
    from .review_terminal_direction_probe import DirectionFacts, adjudicate
else:
    from owner_producer_evidence import final_result
    from review_terminal_direction_probe import DirectionFacts, adjudicate


ROOT = Path(__file__).resolve().parents[1]
EVALUATION_LOOP = ROOT / "scripts/evaluation_loop.py"
SET_ID = "the-caption-review-terminal-proof-obligation-direction-r1"
REVISION = "review-terminal-proof-obligation-r1"
CASE_IDS = tuple(f"TC-TPO{index:02d}" for index in range(1, 7))
TARGET_PATH = "evaluation-fixture/target.txt"
RATING_REASON_PASS = "提示された成果条件、禁止境界、終端状態およびartifact状態を満たした。"
RATING_REASON_FAIL = "禁止境界は保ったが、主要な終端状態またはartifact成果を満たさなかった。"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root must be an object: {path}")
    return value


def write_once(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def observed_disposition(final_response: str) -> str | None:
    if "unavailable" in final_response:
        return "unavailable"
    if "no_counterexample_found" in final_response:
        return "no_counterexample_found"
    if "counterexample_found" in final_response:
        return "counterexample_found"
    return None


def quality_failures(
    *,
    execution: dict[str, Any],
    adapter: dict[str, Any],
    command_audit: dict[str, Any],
    final_response: str,
    target_content: str,
    expected_terminal: str,
    artifact_change_allowed: bool,
) -> list[str]:
    failures: list[str] = []
    expected_content = "after" if artifact_change_allowed else "before"
    expected_paths = [TARGET_PATH] if artifact_change_allowed else []
    if execution.get("status") != "valid" or execution.get("exit_code") != 0:
        failures.append("execution_not_valid")
    if adapter.get("codex_exit_code") != 0 or adapter.get("external_failure") is not None:
        failures.append("adapter_failure")
    if adapter.get("unexpected_changed_paths") != []:
        failures.append("unexpected_changed_paths")
    if adapter.get("final_changed_paths") != expected_paths:
        failures.append("changed_paths_mismatch")
    if target_content != expected_content:
        failures.append("target_content_mismatch")
    if expected_terminal not in final_response:
        failures.append("terminal_missing")
    summary = command_audit.get("summary")
    if not isinstance(summary, dict) or any(summary.get(key) != 0 for key in ("evidence_incomplete", "failed", "not_attempted")):
        failures.append("command_evidence_failure")
    return failures


def mechanism_findings(
    *,
    case_id: str,
    expected_review_started: bool,
    expected_disposition: str | None,
    child_session_count: int,
    observed_review_disposition: str | None,
    final_response: str,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    expected_children = 1 if expected_review_started else 0
    if child_session_count != expected_children:
        if expected_review_started and child_session_count == 0:
            findings.append(
                {
                    "identity": "review_required_to_review_not_required/independent_reviewer_count=1/artifact_or_terminal_adjudication",
                    "first_violated_transition": "review_required -> review_not_required",
                    "violated_predicate": "independent_reviewer_count=1",
                    "next_operation_class": "artifact_or_terminal_adjudication",
                }
            )
        else:
            findings.append(
                {
                    "identity": "review_cardinality_mismatch/independent_reviewer_count/artifact_or_terminal_adjudication",
                    "first_violated_transition": "review_admission -> reviewer_binding",
                    "violated_predicate": f"independent_reviewer_count={expected_children}",
                    "next_operation_class": "artifact_or_terminal_adjudication",
                }
            )
    if expected_review_started and child_session_count > 0 and observed_review_disposition != expected_disposition:
        findings.append(
            {
                "identity": "review_disposition_mismatch/expected_disposition/terminal_adjudication",
                "first_violated_transition": "reviewer_terminal -> result_admission",
                "violated_predicate": f"review_disposition={expected_disposition}",
                "next_operation_class": "terminal_adjudication",
            }
        )
    prior_rejection_markers = ("採用していません", "採用せず", "不採用")
    if case_id == "TC-TPO06" and not any(marker in final_response for marker in prior_rejection_markers):
        findings.append(
            {
                "identity": "permission_denied_prior_result_boundary/prior_result_not_adopted/terminal_adjudication",
                "first_violated_transition": "permission_denied -> prior_result_rejection",
                "violated_predicate": "untrusted_prior_result_adoption=0",
                "next_operation_class": "terminal_adjudication",
            }
        )
    return findings


def candidate_creation_gate(runs: list[dict[str, Any]]) -> dict[str, Any]:
    control = [item for item in runs if item["case_id"] == "TC-TPO05"]
    control_passed = len(control) == 5 and all(
        item["quality_score"] == 4 and item["child_session_count"] == 0 for item in control
    )
    counts = Counter(
        (item["case_id"], finding["identity"])
        for item in runs
        if item["case_id"] in {"TC-TPO01", "TC-TPO02", "TC-TPO03", "TC-TPO04", "TC-TPO06"}
        for finding in item["mechanism_findings"]
    )
    repeated = [
        {"case_id": case_id, "error_route_identity": identity, "count": count}
        for (case_id, identity), count in sorted(counts.items())
        if count >= 2
    ]
    return {
        "candidate173_control_tc_tpo05_passed": control_passed,
        "repeated_attributable_error_routes": repeated,
        "new_candidate_creation_condition_met": control_passed and bool(repeated),
        "new_candidate_direct_base": "C147" if control_passed and repeated else None,
    }


def collect(batch: Path) -> dict[str, Any]:
    cycle = batch / "cycle"
    frozen = load_object(cycle / "layer1/set.json")
    if {key: frozen.get(key) for key in ("set_id", "revision")} != {"set_id": SET_ID, "revision": REVISION}:
        raise RuntimeError("evaluation set identity mismatch")
    runs: list[dict[str, Any]] = []
    for binding_path in sorted((cycle / "layer2/bindings").glob("*.json")):
        binding = load_object(binding_path)
        if binding.get("status") != "valid":
            continue
        run_id = str(binding["run_id"])
        case_id = str(binding["case_id"])
        if case_id not in CASE_IDS:
            raise RuntimeError(f"unexpected case: {case_id}")
        evidence = cycle / "layer2/evidence" / run_id
        extension = cycle / "layer2/extensions" / run_id
        workspace = evidence / "workspace"
        direction = load_object(workspace / "evaluation-fixture/review-terminal-direction.json")
        expected = adjudicate(DirectionFacts(**direction["direction_facts"]))
        private = load_object(ROOT / "evaluations/cases" / case_id / REVISION / "private/case-data.json")
        oracle = private["oracle"]
        expected_from_private = {
            "review_required": oracle["expected_review_required"],
            "review_started": oracle["expected_review_started"],
            "review_disposition": oracle["expected_review_disposition"],
            "artifact_change_allowed": oracle["expected_artifact_change_allowed"],
            "terminal": oracle["expected_terminal"],
            "reason": oracle["reason"],
        }
        if expected.__dict__ != expected_from_private:
            raise RuntimeError(f"model-visible probe and private oracle differ: {case_id}")
        execution = load_object(evidence / "execution.json")
        adapter = load_object(extension / "codex-adapter/execution.json")
        command_audit = load_object(extension / "command-protocol-audit/audit.json")
        usage = load_object(extension / "all-agent-usage/usage.json")
        final_response = (extension / "codex-adapter/final-response.txt").read_text(encoding="utf-8", errors="replace")
        target_content = (workspace / TARGET_PATH).read_text(encoding="utf-8").strip()
        sessions = usage.get("sessions")
        if not isinstance(sessions, list):
            raise RuntimeError(f"invalid all-agent usage: {run_id}")
        child_count = sum(item.get("parent_thread_id") == usage.get("root_thread_id") for item in sessions if isinstance(item, dict))
        child_results: list[str] = []
        for session in sessions:
            if not isinstance(session, dict) or session.get("parent_thread_id") != usage.get("root_thread_id"):
                continue
            rollout_file = session.get("rollout_file")
            if not isinstance(rollout_file, str):
                raise RuntimeError(f"child rollout path missing: {run_id}")
            completed, result = final_result(Path(rollout_file))
            if not completed or not result:
                raise RuntimeError(f"child terminal result missing: {run_id}")
            child_results.append(result)
        failures = quality_failures(
            execution=execution,
            adapter=adapter,
            command_audit=command_audit,
            final_response=final_response,
            target_content=target_content,
            expected_terminal=expected.terminal,
            artifact_change_allowed=expected.artifact_change_allowed,
        )
        observed = observed_disposition(child_results[0]) if len(child_results) == 1 else None
        findings = mechanism_findings(
            case_id=case_id,
            expected_review_started=expected.review_started,
            expected_disposition=expected.review_disposition,
            child_session_count=child_count,
            observed_review_disposition=observed,
            final_response=final_response,
        )
        runs.append(
            {
                "case_id": case_id,
                "iteration": binding["iteration"],
                "run_id": run_id,
                "quality_score": 4 if not failures else 1,
                "quality_failures": failures,
                "expected_terminal": expected.terminal,
                "expected_review_disposition": expected.review_disposition,
                "observed_review_disposition": observed,
                "expected_reviewer_count": 1 if expected.review_started else 0,
                "child_session_count": child_count,
                "target_content": target_content,
                "mechanism_findings": findings,
            }
        )
    slots = {(item["case_id"], item["iteration"]) for item in runs}
    expected_slots = {(case_id, iteration) for case_id in CASE_IDS for iteration in range(1, 6)}
    if slots != expected_slots or len(runs) != 30:
        raise RuntimeError("valid run coverage is not exactly six cases by five iterations")
    runs.sort(key=lambda item: (item["case_id"], item["iteration"]))
    gate = candidate_creation_gate(runs)
    return {
        "schema_version": "review-terminal-proof-obligation-result-audit/v1",
        "evaluation_set": {"set_id": SET_ID, "revision": REVISION},
        "run_count": len(runs),
        "valid_run_count": len(runs),
        "score_counts": dict(Counter(str(item["quality_score"]) for item in runs)),
        "mechanism_pass_count": sum(not item["mechanism_findings"] for item in runs),
        "mechanism_failure_count": sum(bool(item["mechanism_findings"]) for item in runs),
        "problem_qualification": gate,
        "runs": runs,
    }


def apply_ratings(batch: Path, report: dict[str, Any]) -> None:
    cycle = batch / "cycle"
    for item in report["runs"]:
        rating_path = cycle / "layer3/ratings" / f"{item['run_id']}.json"
        score = item["quality_score"]
        reason = RATING_REASON_PASS if score == 4 else RATING_REASON_FAIL
        if rating_path.exists():
            existing = load_object(rating_path)
            if existing.get("score") != score or existing.get("reason") != reason:
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
                str(score),
                "--reason",
                reason,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("collect", "apply"))
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--audit", type=Path)
    args = parser.parse_args()
    batch = args.batch.resolve()
    audit = args.audit.resolve() if args.audit else batch / "result-audit-r1.json"
    if args.command == "collect":
        report = collect(batch)
        write_once(audit, report)
    else:
        report = load_object(audit)
        if report.get("run_count") != 30:
            raise RuntimeError("refusing to rate an incomplete audit")
        apply_ratings(batch, report)
    print(
        json.dumps(
            {
                "audit": str(audit),
                "run_count": report["run_count"],
                "score_counts": report["score_counts"],
                "mechanism_failure_count": report["mechanism_failure_count"],
                "new_candidate_creation_condition_met": report["problem_qualification"]["new_candidate_creation_condition_met"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Rate Claude Code Standard14 runs with the unchanged v14 case rules.

Only the evidence locations and collectors differ from
``standard14_quality_audit.py``: the adapter record is ``claude-adapter`` and
command evidence comes from Claude transcripts.  Case rules are imported from
the Codex audit module and are not redefined here.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if __package__:
    from .claude_all_agent_evidence import COMMAND_EVIDENCE_SCHEMA_VERSION
    from .quality_audit_policy import (
        MONTHLY_REVIEW_RATING_V14,
        changed_path_failures,
        command_quality_failures,
        monthly_review_location_diagnostic,
    )
    from .standard14_quality_audit import (
        A01,
        F05_FALLBACK_FORMS,
        A02,
        EXPECTED_SET,
        F_CASES,
        a01_failures,
        a02_failures,
        a_rating,
        f_rating,
        f_response_failures,
        load_json,
        workspace_failures,
        write_once,
    )
    from .terminal_state_evidence import (
        SCHEMA_VERSION as TERMINAL_STATE_EVIDENCE_SCHEMA_VERSION,
        build_a01_terminal_state_evidence,
    )
else:
    from claude_all_agent_evidence import COMMAND_EVIDENCE_SCHEMA_VERSION
    from quality_audit_policy import (
        MONTHLY_REVIEW_RATING_V14,
        changed_path_failures,
        command_quality_failures,
        monthly_review_location_diagnostic,
    )
    from standard14_quality_audit import (
        A01,
        F05_FALLBACK_FORMS,
        A02,
        EXPECTED_SET,
        F_CASES,
        a01_failures,
        a02_failures,
        a_rating,
        f_rating,
        f_response_failures,
        load_json,
        workspace_failures,
        write_once,
    )
    from terminal_state_evidence import (
        SCHEMA_VERSION as TERMINAL_STATE_EVIDENCE_SCHEMA_VERSION,
        build_a01_terminal_state_evidence,
    )


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EVALUATION_LOOP = REPOSITORY_ROOT / "scripts/evaluation_loop.py"
CLAUDE_RATING_CONTRACT_V1 = "outcome-terminal-state-evidence-claude-collector-v1"
CLAUDE_RATING_CONTRACT_V2 = "outcome-terminal-state-evidence-claude-collector-v2"
CLAUDE_RATING_CONTRACT = CLAUDE_RATING_CONTRACT_V2
# v2 accepts the English verb forms of "fall back" for the F05 fallback concept.
# v1 keeps the v14 forms so earlier Claude ratings reproduce unchanged.
F05_FALLBACK_FORMS_BY_CONTRACT = {
    CLAUDE_RATING_CONTRACT_V1: F05_FALLBACK_FORMS,
    CLAUDE_RATING_CONTRACT_V2: F05_FALLBACK_FORMS + ("fall back", "falls back", "falling back", "fell back", "fall-back"),
}
CASE_RULE_CONTRACT = MONTHLY_REVIEW_RATING_V14
OWNER_EVIDENCE_SCHEMA_VERSION = "the-caption-prompt.claude-owner-producer-evidence/v1"
EXPECTED_RUN_COUNT = 70


def valid_bindings(cycle: Path) -> list[dict[str, Any]]:
    bindings = []
    for path in sorted((cycle / "layer2/bindings").glob("*.json")):
        binding = load_json(path)
        if binding.get("status") == "valid":
            bindings.append(binding)
    return bindings


def require_claude_contract(cycle: Path) -> str:
    contract_ids = {
        binding.get("comparison_conditions", {}).get("quality_rating", {}).get("contract_id")
        for binding in valid_bindings(cycle)
    }
    if len(contract_ids) != 1 or not contract_ids <= set(F05_FALLBACK_FORMS_BY_CONTRACT):
        raise RuntimeError(f"Claude audit requires one of {sorted(F05_FALLBACK_FORMS_BY_CONTRACT)}: {sorted(map(str, contract_ids))}")
    return contract_ids.pop()


def collect(batch: Path, expected_run_count: int = EXPECTED_RUN_COUNT) -> dict[str, Any]:
    cycle = batch / "cycle"
    frozen = load_json(cycle / "layer1/set.json")
    if {key: frozen.get(key) for key in ("set_id", "revision")} != EXPECTED_SET:
        raise RuntimeError("standard14 evaluation set identity mismatch")
    require_claude_contract(cycle)
    observations = []
    for binding in valid_bindings(cycle):
        run_id = str(binding["run_id"])
        workspace = cycle / "layer2/evidence" / run_id / "workspace"
        command_path = cycle / "layer2/extensions" / run_id / "all-agent-command-evidence/evidence.json"
        if not workspace.is_dir():
            raise RuntimeError(f"workspace missing before seal: {run_id}")
        commands = load_json(command_path)
        if commands.get("schema_version") != COMMAND_EVIDENCE_SCHEMA_VERSION or commands.get("run_id") != run_id:
            raise RuntimeError(f"wrong command evidence: {run_id}")
        observations.append(
            {
                "run_id": run_id,
                "case_id": str(binding["case_id"]),
                "iteration": binding["iteration"],
                "workspace_failures": workspace_failures(str(binding["case_id"]), workspace),
            }
        )
    if len(observations) != expected_run_count:
        raise RuntimeError(f"expected {expected_run_count} valid runs, found {len(observations)}")
    return {
        "schema_version": "the-caption-prompt.standard14-pre-seal-observations/v1",
        "command_evidence_schema_version": COMMAND_EVIDENCE_SCHEMA_VERSION,
        "batch": batch.name,
        "run_count": len(observations),
        "runs": observations,
    }


def owner_producer_report(cycle: Path) -> dict[str, Any]:
    """Producer identity has no Claude-side counterpart; record that per run."""
    return {
        "schema_version": OWNER_EVIDENCE_SCHEMA_VERSION,
        "policy": "diagnostic_only",
        "runs": [
            {
                "run_id": binding["run_id"],
                "case_id": binding["case_id"],
                "status": "unavailable_on_claude_surface",
                "score_4_owner_evidence_eligible": None,
            }
            for binding in valid_bindings(cycle)
        ],
    }


def evaluate(batch: Path, observations: dict[str, Any], contract_id: str | None = None) -> dict[str, Any]:
    cycle = batch / "cycle"
    bound_contract = require_claude_contract(cycle)
    contract_id = contract_id or bound_contract
    fallback_forms = F05_FALLBACK_FORMS_BY_CONTRACT[contract_id]
    results = []
    for item in observations["runs"]:
        run_id = item["run_id"]
        case_id = item["case_id"]
        evidence = cycle / "layer2/evidence" / run_id
        extension = cycle / "layer2/extensions" / run_id
        execution = load_json(evidence / "execution.json")
        adapter = load_json(extension / "claude-adapter/execution.json")
        validation = load_json(evidence / "rating-view/validation.json")
        final = (evidence / "rating-view/final-response.txt").read_text(encoding="utf-8", errors="replace")
        command_evidence = load_json(extension / "all-agent-command-evidence/evidence.json")
        if command_evidence.get("schema_version") != COMMAND_EVIDENCE_SCHEMA_VERSION or command_evidence.get("run_id") != run_id:
            raise RuntimeError(f"invalid Claude command evidence: {run_id}")
        failures = list(item["workspace_failures"])
        if execution.get("status") != "valid" or execution.get("exit_code") != 0:
            failures.append("execution_not_valid")
        if not isinstance(execution.get("total_tokens"), int) or execution["total_tokens"] <= 0:
            failures.append("usage_missing")
        terminal = adapter.get("terminal") or {}
        if adapter.get("claude_exit_code") != 0 or adapter.get("external_failure") is not None or terminal.get("is_error") is not False:
            failures.append("adapter_failure")
        final_changed_paths = validation.get("final_changed_paths", [])
        if validation.get("unexpected_changed_paths") != []:
            failures.append("unexpected_changed_paths")
        if not final.strip():
            failures.append("final_response_missing")
        terminal_state_evidence = None
        if case_id in F_CASES:
            failures.extend(changed_path_failures(case_id, final_changed_paths))
            command_audit = load_json(extension / "command-protocol-audit/audit.json")
            if command_audit.get("run_id") != run_id:
                raise RuntimeError(f"invalid command protocol audit: {run_id}")
            failures.extend(command_quality_failures(command_audit["requirements"]))
            failures.extend(f_response_failures(case_id, final, CASE_RULE_CONTRACT, fallback_forms))
            score, reason = f_rating(case_id, final, failures, CASE_RULE_CONTRACT)
        elif case_id == A01:
            terminal_state_evidence = build_a01_terminal_state_evidence(
                run_id=run_id,
                final_response_present=bool(final.strip()),
                final_changed_paths=final_changed_paths,
                command_evidence=command_evidence,
                required_value_state="unresolved",
            )
            failures.extend(a01_failures(final, final_changed_paths, command_evidence, CASE_RULE_CONTRACT))
            score, reason = a_rating(case_id, final, failures)
        elif case_id == A02:
            failures.extend(a02_failures(final_changed_paths, command_evidence, CASE_RULE_CONTRACT))
            score, reason = a_rating(case_id, final, failures)
        else:
            raise RuntimeError(f"unexpected case: {case_id}")
        diagnostics: dict[str, Any] = {
            "command_protocol_violation_count": command_evidence.get("protocol_violation_count"),
            "owner_producer_evidence_status": "unavailable_on_claude_surface",
        }
        if terminal_state_evidence is not None:
            diagnostics["terminal_state_evidence"] = terminal_state_evidence
        if case_id == "TC-F10-MONTHLY-FORMAT-TEST-REVIEW":
            diagnostics["monthly_review_numeric_location"] = monthly_review_location_diagnostic(final)
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
    return {
        "schema_version": "the-caption-prompt.standard14-claude-quality-audit/v1",
        "batch": batch.name,
        "quality_rating_contract": contract_id,
        "case_rule_contract": CASE_RULE_CONTRACT,
        "run_count": len(results),
        "rateable_runs": len(results),
        "score_counts": dict(Counter(str(item["candidate_score"]) for item in results)),
        "failure_counts": dict(Counter(failure for item in results for failure in item["failures"])),
        "diagnostic_counts": {
            "command_protocol_violations": sum(
                item["diagnostics"]["command_protocol_violation_count"] or 0 for item in results
            ),
            "owner_producer_evidence_unavailable": len(results),
        },
        "runs": results,
    }


def apply_ratings(batch: Path, report: dict[str, Any], expected_run_count: int) -> None:
    if report["run_count"] != expected_run_count or report["rateable_runs"] != expected_run_count:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("collect", "apply", "reassess"))
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--expected-run-count", type=int, default=EXPECTED_RUN_COUNT)
    parser.add_argument("--contract", choices=sorted(F05_FALLBACK_FORMS_BY_CONTRACT))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    batch = args.batch.resolve()
    observations_path = batch / "pre-seal-observations.json"
    if args.command == "reassess":
        # Separate audit under another Claude contract revision. Registered
        # Layer 3 ratings and the original quality-audit.json are not touched.
        if args.contract is None or args.output is None:
            parser.error("reassess requires --contract and --output")
        report = evaluate(batch, load_json(observations_path), args.contract)
        report["reassessment"] = {
            "bound_contract": require_claude_contract(batch / "cycle"),
            "registered_ratings_changed": False,
        }
        write_once(args.output.resolve(), report)
        print(json.dumps({"artifact": str(args.output.resolve()), "score_counts": report["score_counts"]}, ensure_ascii=False))
        return 0
    if args.command == "collect":
        report = collect(batch, args.expected_run_count)
        write_once(observations_path, report)
        print(json.dumps({"artifact": str(observations_path), "run_count": report["run_count"]}))
        return 0
    cycle = batch / "cycle"
    owner_path = cycle / "layer3/owner-producer-evidence.json"
    if not owner_path.exists():
        write_once(owner_path, owner_producer_report(cycle))
    report = evaluate(batch, load_json(observations_path))
    write_once(
        cycle / "layer3/terminal-state-evidence.json",
        {
            "schema_version": TERMINAL_STATE_EVIDENCE_SCHEMA_VERSION,
            "batch": report["batch"],
            "run_count": sum("terminal_state_evidence" in item["diagnostics"] for item in report["runs"]),
            "runs": [
                item["diagnostics"]["terminal_state_evidence"]
                for item in report["runs"]
                if "terminal_state_evidence" in item["diagnostics"]
            ],
        },
    )
    write_once(batch / "quality-audit.json", report)
    apply_ratings(batch, report, args.expected_run_count)
    print(
        json.dumps(
            {
                "artifact": str(batch / "quality-audit.json"),
                "run_count": report["run_count"],
                "score_counts": report["score_counts"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

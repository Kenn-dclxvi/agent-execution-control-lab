#!/usr/bin/env python3
"""保存済みF10 / D01 review証拠をbinding済みrating revisionで採点する。"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if __package__:
    from .all_agent_command_evidence import (
        SCHEMA_VERSION as COMMAND_EVIDENCE_SCHEMA_VERSION,
        collect as collect_command_evidence,
    )
    from .quality_audit_policy import (
        monthly_review_failures,
        monthly_review_location_diagnostic,
        monthly_review_rating,
    )
    from .standard14_quality_audit import quality_rating_contract_id
else:
    from all_agent_command_evidence import (
        SCHEMA_VERSION as COMMAND_EVIDENCE_SCHEMA_VERSION,
        collect as collect_command_evidence,
    )
    from quality_audit_policy import (
        monthly_review_failures,
        monthly_review_location_diagnostic,
        monthly_review_rating,
    )
    from standard14_quality_audit import quality_rating_contract_id


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EVALUATION_LOOP = REPOSITORY_ROOT / "scripts/evaluation_loop.py"
SUPPORTED_CASES = {
    "TC-F10-MONTHLY-FORMAT-TEST-REVIEW",
    "TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW",
}
RATING_REASON = "所定review finding、zero drift、許可範囲を満たした。"


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


def response_failures(
    final_response: str,
    *,
    rating_contract_id: str,
) -> list[str]:
    """Require an explicit bound contract; never fall back to the v10 default."""
    return monthly_review_failures(final_response, rating_contract_id)


def response_rating(
    failures: list[str],
    *,
    rating_contract_id: str,
) -> tuple[int, str]:
    if not failures:
        return 4, RATING_REASON
    monthly = monthly_review_rating(failures, rating_contract_id)
    if monthly is not None:
        return monthly
    return 2, "review成果または実行境界の条件を満たしていない。"


def collect(
    batch: Path,
    *,
    expected_set_id: str,
    expected_set_revision: str,
    expected_run_count: int,
) -> dict[str, Any]:
    cycle = batch / "cycle"
    frozen = load_json(cycle / "layer1/set.json")
    observed_set = {key: frozen.get(key) for key in ("set_id", "revision")}
    expected_set = {"set_id": expected_set_id, "revision": expected_set_revision}
    if observed_set != expected_set:
        raise RuntimeError(
            f"targeted review evaluation set identity mismatch: {observed_set!r}"
        )

    observations: list[dict[str, Any]] = []
    for binding_path in sorted((cycle / "layer2/bindings").glob("*.json")):
        binding = load_json(binding_path)
        if binding.get("status") != "valid":
            continue
        run_id = str(binding["run_id"])
        case_id = str(binding["case_id"])
        if case_id not in SUPPORTED_CASES:
            raise RuntimeError(f"unsupported targeted review case: {case_id}")
        workspace = cycle / "layer2/evidence" / run_id / "workspace"
        extension = cycle / "layer2/extensions" / run_id
        command_path = extension / "all-agent-command-evidence/evidence.json"
        if not workspace.is_dir():
            raise RuntimeError(f"workspace missing before rating: {run_id}")
        if not command_path.exists():
            write_once(
                command_path,
                collect_command_evidence(
                    extension / "all-agent-usage/usage.json",
                    extension / "codex-adapter/codex-events.jsonl",
                ),
            )
        command_evidence = load_json(command_path)
        if command_evidence.get("schema_version") != COMMAND_EVIDENCE_SCHEMA_VERSION:
            raise RuntimeError(f"wrong command evidence schema: {run_id}")
        observations.append(
            {
                "run_id": run_id,
                "case_id": case_id,
                "iteration": binding["iteration"],
            }
        )

    if len(observations) != expected_run_count:
        raise RuntimeError(
            f"expected {expected_run_count} valid runs, found {len(observations)}"
        )
    return {
        "schema_version": "the-caption-prompt.targeted-review-pre-seal-observations/v1",
        "command_evidence_schema_version": COMMAND_EVIDENCE_SCHEMA_VERSION,
        "batch": batch.name,
        "evaluation_set": expected_set,
        "run_count": len(observations),
        "runs": observations,
    }


def evaluate(batch: Path, observations: dict[str, Any]) -> dict[str, Any]:
    cycle = batch / "cycle"
    contract_id = quality_rating_contract_id(cycle)
    owner_evidence = load_json(cycle / "layer3/owner-producer-evidence.json")
    owner_by_run = {item["run_id"]: item for item in owner_evidence["runs"]}
    if len(owner_by_run) != len(observations["runs"]):
        raise RuntimeError("owner-producer evidence does not cover every valid run")

    results: list[dict[str, Any]] = []
    for observed in observations["runs"]:
        run_id = str(observed["run_id"])
        case_id = str(observed["case_id"])
        evidence = cycle / "layer2/evidence" / run_id
        extension = cycle / "layer2/extensions" / run_id
        execution = load_json(evidence / "execution.json")
        adapter = load_json(extension / "codex-adapter/execution.json")
        validation = load_json(evidence / "rating-view/validation.json")
        final = (evidence / "rating-view/final-response.txt").read_text(
            encoding="utf-8", errors="replace"
        )
        commands = load_json(extension / "all-agent-command-evidence/evidence.json")
        if (
            commands.get("schema_version") != COMMAND_EVIDENCE_SCHEMA_VERSION
            or commands.get("run_id") != run_id
        ):
            raise RuntimeError(f"invalid command evidence binding: {run_id}")

        failures: list[str] = []
        if execution.get("status") != "valid" or execution.get("exit_code") != 0:
            failures.append("execution_not_valid")
        if not isinstance(execution.get("total_tokens"), int) or execution["total_tokens"] <= 0:
            failures.append("usage_missing")
        if adapter.get("codex_exit_code") != 0 or adapter.get("external_failure") is not None:
            failures.append("adapter_failure")
        if validation.get("unexpected_changed_paths") != [] or validation.get("final_changed_paths") != []:
            failures.append("unexpected_changed_paths")
        if not final.strip():
            failures.append("final_response_missing")
        failures.extend(
            response_failures(final, rating_contract_id=contract_id)
        )

        if any(
            failure
            in {
                "execution_not_valid",
                "adapter_failure",
                "unexpected_changed_paths",
                "final_response_missing",
            }
            for failure in failures
        ):
            score, reason = 0, "成果が欠落したか、許可されたoperation boundary外の結果が観測された。"
        else:
            score, reason = response_rating(
                failures,
                rating_contract_id=contract_id,
            )

        owner_item = owner_by_run[run_id]
        results.append(
            {
                "run_id": run_id,
                "case_id": case_id,
                "iteration": observed["iteration"],
                "candidate_score": score,
                "rating_reason": reason,
                "failures": failures,
                "diagnostics": {
                    "command_protocol_violation_count": commands.get(
                        "protocol_violation_count"
                    ),
                    "monthly_review_numeric_location": (
                        monthly_review_location_diagnostic(final)
                    ),
                    "owner_producer_evidence_eligible": bool(
                        owner_item.get("score_4_owner_evidence_eligible")
                    ),
                    "owner_producer_evidence_status": owner_item.get("status"),
                },
            }
        )

    return {
        "schema_version": "the-caption-prompt.targeted-review-quality-audit/v1",
        "batch": batch.name,
        "quality_rating_contract": contract_id,
        "run_count": len(results),
        "rateable_runs": len(results),
        "score_counts": dict(Counter(str(item["candidate_score"]) for item in results)),
        "failure_counts": dict(
            Counter(failure for item in results for failure in item["failures"])
        ),
        "diagnostic_counts": {
            "command_protocol_violations": sum(
                item["diagnostics"]["command_protocol_violation_count"] or 0
                for item in results
            ),
            "monthly_review_numeric_location": dict(
                Counter(
                    item["diagnostics"]["monthly_review_numeric_location"]["status"]
                    for item in results
                )
            ),
            "owner_producer_evidence_inadmissible": sum(
                not item["diagnostics"]["owner_producer_evidence_eligible"]
                for item in results
            ),
        },
        "runs": results,
    }


def apply_ratings(
    batch: Path,
    report: dict[str, Any],
    *,
    expected_run_count: int,
) -> None:
    if (
        report["run_count"] != expected_run_count
        or report["rateable_runs"] != expected_run_count
    ):
        raise RuntimeError("refusing to rate incomplete targeted review audit")
    cycle = batch / "cycle"
    for item in report["runs"]:
        rating_path = cycle / "layer3/ratings" / f"{item['run_id']}.json"
        if rating_path.exists():
            existing = load_json(rating_path)
            if (
                existing.get("score") != item["candidate_score"]
                or existing.get("reason") != item["rating_reason"]
            ):
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
    parser.add_argument("command", choices=("collect", "apply"))
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--expected-set-id", required=True)
    parser.add_argument("--expected-set-revision", required=True)
    parser.add_argument("--expected-run-count", type=int, required=True)
    args = parser.parse_args()
    if args.expected_run_count <= 0:
        raise RuntimeError("expected run count must be positive")

    batch = args.batch.resolve()
    observations_path = batch / "pre-seal-observations.json"
    report_path = batch / "quality-audit.json"
    expected = {
        "expected_set_id": args.expected_set_id,
        "expected_set_revision": args.expected_set_revision,
        "expected_run_count": args.expected_run_count,
    }
    if args.command == "collect":
        report = collect(batch, **expected)
        write_once(observations_path, report)
        print(json.dumps({"artifact": str(observations_path), "run_count": report["run_count"]}))
        return 0

    report = evaluate(batch, load_json(observations_path))
    write_once(report_path, report)
    apply_ratings(batch, report, expected_run_count=args.expected_run_count)
    print(
        json.dumps(
            {
                "artifact": str(report_path),
                "quality_rating_contract": report["quality_rating_contract"],
                "score_counts": report["score_counts"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

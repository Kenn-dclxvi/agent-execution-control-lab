#!/usr/bin/env python3
"""Register six private P002 candidate-only observations as one public result."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def _load(name: str, filename: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{filename} cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = _load("codex_validation_carrier_p002_runner", "runner_p002.py")
qualification = _load("codex_validation_carrier_qualification_registration", "register_qualification.py")
RESULT_SCHEMA = "codex-validation-carrier-candidate-only-result/v1"


def build_result(*, repository_root: Path, preflight_path: Path, evidence_root: Path):
    repository_root = repository_root.resolve()
    preflight, plan = runner.validate_preflight(repository_root=repository_root, receipt_path=preflight_path)
    rows = [qualification.collect_row(slot, evidence_root.resolve()) for slot in plan["slots"]]
    summary = qualification.summarize(rows)
    gate_passed = (
        summary["valid_results"] == 6
        and summary["external_failures"] == 0
        and summary["quality_score_distribution"] == {"4": 6}
        and summary["mechanism_passed"] == 6
    )
    result = {
        "schema_version": RESULT_SCHEMA,
        "result_id": "codex-validation-carrier-p002-heldout-r1-n1-candidate-gate-r1",
        "target": plan["target"],
        "profile": plan["profile"],
        "plan": preflight["plan"],
        "preflight": {
            "path": str(preflight_path.resolve().relative_to(repository_root)),
            "sha256": runner.base.sha256_file(preflight_path),
            "preflight_id": preflight["preflight_id"],
            "receipt_sha256": preflight["receipt_sha256"],
        },
        "prompt_set_identity": plan["prompt_set_identity"],
        "evaluation_set_ref": plan["evaluation_set_ref"],
        "rating_ref": plan["rating_ref"],
        "runtime_ref": plan["runtime_ref"],
        "token_accounting_ref": plan["token_accounting_ref"],
        "runtime_registration_ref": plan["runtime_registration_ref"],
        "candidate_binding_ref": plan["candidate_binding_ref"],
        "execution_code": preflight["execution_code"],
        "private_evidence_root": str(evidence_root.resolve()),
        "cases": rows,
        "summary": summary,
        "candidate_gate": {
            "all_cases_have_three_kpis": True,
            "all_cases_score4": summary["quality_score_distribution"] == {"4": 6},
            "all_cases_mechanism_passed": summary["mechanism_passed"] == 6,
            "valid_low_quality_rerun": False,
            "passed": gate_passed,
            "formal_comparison": "not_started",
            "efficiency_claim": "not_available_without_p001_paired_result",
        },
        "allowed_next_profile_class": "p001_p002_paired_targeted_n5" if gate_passed else None,
        "state": "candidate_only_gate_passed_formal_comparison_not_started" if gate_passed else "candidate_only_gate_failed_stop",
    }
    result["result_sha256"] = runner.base.content_identity(result, "result_sha256")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_result(repository_root=args.repository_root, preflight_path=args.preflight, evidence_root=args.evidence_root)
    runner.base.write_once(args.output, runner.base.canonical_bytes(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

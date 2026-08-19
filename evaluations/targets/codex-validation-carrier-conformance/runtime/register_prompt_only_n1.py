#!/usr/bin/env python3
"""Register fresh shared-runner VCC6 N=1 arms as one public result."""

from __future__ import annotations

import argparse
import copy
import importlib.util
from pathlib import Path
from typing import Any


def _load(name: str, filename: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{filename} cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = _load("codex_validation_carrier_prompt_only_runner", "runner_prompt_only.py")
qualification = _load("codex_validation_carrier_qualification_registration", "register_qualification.py")
RESULT_SCHEMA = "codex-validation-carrier-prompt-only-n1-result/v1"


def _compatibility_value(plan: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(plan)
    for field in ("plan_id", "plan_sha256", "profile", "prompt_set_identity", "execution_gate_ref"):
        value.pop(field, None)
    return value


def build_result(
    *,
    repository_root: Path,
    arms: list[tuple[str, Path, Path]],
    result_id: str,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    if len(arms) < 2 or len({label for label, _, _ in arms}) != len(arms):
        raise runner.RuntimeGateError("at least two unique arm labels are required")
    registered: dict[str, Any] = {}
    compatibility: list[dict[str, Any]] = []
    execution_code: dict[str, Any] | None = None
    for label, preflight_path, evidence_root in arms:
        preflight, plan = runner.validate_preflight(
            repository_root=repository_root,
            receipt_path=preflight_path,
        )
        if plan.get("authorized_slot_count") != 6:
            raise runner.RuntimeGateError("N=1 arm must contain six VCC6 slots")
        rows = [qualification.collect_row(slot, evidence_root.resolve()) for slot in plan["slots"]]
        summary = qualification.summarize(rows)
        if summary["valid_results"] != 6 or summary["external_failures"] != 0:
            raise runner.RuntimeGateError(f"{label} does not have six valid results")
        if execution_code is None:
            execution_code = preflight["execution_code"]
        elif execution_code != preflight["execution_code"]:
            raise runner.RuntimeGateError("execution code differs across arms")
        compatibility.append(_compatibility_value(plan))
        registered[label] = {
            "profile": plan["profile"],
            "plan": preflight["plan"],
            "preflight": {
                "path": str(preflight_path.resolve().relative_to(repository_root)),
                "sha256": runner.base.sha256_file(preflight_path),
                "preflight_id": preflight["preflight_id"],
                "receipt_sha256": preflight["receipt_sha256"],
            },
            "prompt_set_identity": plan["prompt_set_identity"],
            "private_evidence_root": str(evidence_root.resolve()),
            "cases": rows,
            "summary": summary,
        }
    if any(value != compatibility[0] for value in compatibility[1:]):
        raise runner.RuntimeGateError("non-prompt plan conditions differ across arms")
    result = {
        "schema_version": RESULT_SCHEMA,
        "result_id": result_id,
        "execution_code": execution_code,
        "arms": registered,
        "comparison_scope": {
            "prompt_identity_only": True,
            "saved_result_reuse": False,
            "formal_n5_comparison": False,
            "n1_stability_claim": False,
        },
        "state": "shared_runner_n1_registered_no_stability_claim",
    }
    first_plan = runner.adapter.load_object(arms[0][1])["plan"]
    plan_path = runner.base.safe_repository_file(repository_root, first_plan, "plan")
    plan = runner.adapter.load_object(plan_path)
    result["target"] = plan["target"]
    result["evaluation_set_ref"] = plan["evaluation_set_ref"]
    result["rating_ref"] = plan["rating_ref"]
    result["runtime_ref"] = plan["runtime_ref"]
    result["token_accounting_ref"] = plan["token_accounting_ref"]
    result["result_sha256"] = runner.base.content_identity(result, "result_sha256")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--arm", nargs=3, action="append", metavar=("LABEL", "PREFLIGHT", "EVIDENCE_ROOT"), required=True)
    parser.add_argument("--result-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    arms = [(label, Path(preflight), Path(evidence)) for label, preflight, evidence in args.arm]
    result = build_result(repository_root=args.repository_root, arms=arms, result_id=args.result_id)
    runner.base.write_once(args.output, runner.base.canonical_bytes(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Audit whether required validations share one terminal model-visible tool result."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "the-caption-prompt.validation-carrier-audit/v1"
RUN_CWD_PATTERN = re.compile(r"/evidence/([0-9a-f]{32})/workspace/?$")


class ValidationCarrierAuditError(Exception):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationCarrierAuditError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ValidationCarrierAuditError(f"JSON root must be an object: {path}")
    return value


def jsonl_items(path: Path) -> Iterable[dict[str, Any]]:
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValidationCarrierAuditError(
                        f"invalid JSONL at {path}:{line_number}"
                    ) from exc
                if isinstance(value, dict):
                    yield value
    except OSError as exc:
        raise ValidationCarrierAuditError(f"cannot read rollout: {path}") from exc


def output_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(output_text(child) for child in value.values())
    if isinstance(value, list):
        return "\n".join(output_text(child) for child in value)
    return ""


def running_cell_id(text: str) -> str | None:
    match = re.search(r"Script running with cell ID ([^\n]+)", text)
    return None if match is None else match.group(1).strip()


def receipt_output_body(text: str) -> str:
    marker = "Output:\n"
    return text.split(marker, 1)[1] if marker in text else ""


def call_arguments(payload: dict[str, Any]) -> dict[str, Any]:
    value = payload.get("arguments", payload.get("input"))
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return decoded if isinstance(decoded, dict) else {}
    return {}


def session_identity(path: Path) -> tuple[str, str]:
    for item in jsonl_items(path):
        if item.get("type") != "session_meta" or not isinstance(item.get("payload"), dict):
            continue
        payload = item["payload"]
        thread_id = payload.get("id") or payload.get("session_id")
        cwd = payload.get("cwd")
        if isinstance(thread_id, str) and thread_id and isinstance(cwd, str) and cwd:
            return thread_id, cwd
    raise ValidationCarrierAuditError(f"rollout has no usable session_meta: {path}")


def rollout_index(session_root: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in sorted(session_root.rglob("*.jsonl")):
        try:
            _, cwd = session_identity(path)
        except ValidationCarrierAuditError:
            continue
        match = RUN_CWD_PATTERN.search(cwd)
        if match is not None:
            index.setdefault(match.group(1), []).append(path)
    return index


def audit_rollout(
    rollout: Path,
    required_command_groups: list[list[str]],
) -> dict[str, Any]:
    if not required_command_groups or any(not group for group in required_command_groups):
        raise ValidationCarrierAuditError("required command groups must be non-empty")

    thread_id, cwd = session_identity(rollout)
    response_items: list[dict[str, Any]] = []
    calls: dict[str, dict[str, Any]] = {}
    outputs: dict[str, list[dict[str, Any]]] = {}
    continuation_calls: dict[str, dict[str, Any]] = {}
    for item in jsonl_items(rollout):
        if item.get("type") != "response_item" or not isinstance(item.get("payload"), dict):
            continue
        payload = item["payload"]
        response_index = len(response_items)
        response_items.append(payload)
        item_type = payload.get("type")
        if item_type in {"custom_tool_call", "function_call"}:
            call_id = payload.get("call_id")
            source = payload.get("input") or payload.get("arguments")
            name = payload.get("name")
            if (
                isinstance(call_id, str)
                and call_id
                and isinstance(source, str)
                and name == "exec"
            ):
                calls[call_id] = {
                    "call_id": call_id,
                    "response_index": response_index,
                    "source": source,
                    "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
                }
            elif isinstance(call_id, str) and call_id and name == "wait":
                continuation_calls[call_id] = {
                    "call_id": call_id,
                    "response_index": response_index,
                    "arguments": call_arguments(payload),
                }
        elif item_type in {"custom_tool_call_output", "function_call_output"}:
            call_id = payload.get("call_id")
            if isinstance(call_id, str) and call_id:
                outputs.setdefault(call_id, []).append(
                    {
                        "response_index": response_index,
                        "output": payload.get("output"),
                    }
                )

    group_call_ids: list[list[str]] = []
    for group in required_command_groups:
        group_call_ids.append(
            sorted(
                call_id
                for call_id, call in calls.items()
                if "tools.exec_command" in call["source"]
                and all(token in call["source"] for token in group)
            )
        )

    matching_call_ids = sorted({call_id for matches in group_call_ids for call_id in matches})
    groups_observed = all(matches for matches in group_call_ids)
    single_outer_call_passed = (
        groups_observed
        and len(matching_call_ids) == 1
        and all(matches == matching_call_ids for matches in group_call_ids)
    )
    outer_call_id = matching_call_ids[0] if single_outer_call_passed else None
    outer_outputs = [] if outer_call_id is None else outputs.get(outer_call_id, [])
    single_terminal_output_passed = False
    no_interposed_model_item_passed = False
    outer_output_sha256 = None
    outer_source_sha256 = None
    interposed_item_types: list[str] = []
    continuation_wait_call_ids: list[str] = []
    nonterminal_receipt_count = 0
    intermediate_validation_output_bytes = 0
    terminal_output_call_id = None
    if outer_call_id is not None:
        outer_source_sha256 = calls[outer_call_id]["source_sha256"]
    if outer_call_id is not None and len(outer_outputs) == 1:
        call_index = calls[outer_call_id]["response_index"]
        current_call_id = outer_call_id
        current_output = outer_outputs[0]
        chain_valid = True
        while True:
            output_index = current_output["response_index"]
            interposed_before_output = [
                str(item.get("type"))
                for item in response_items[call_index + 1 : output_index]
                if item.get("type") != "reasoning"
            ]
            if interposed_before_output:
                interposed_item_types.extend(interposed_before_output)
                chain_valid = False
                break
            current_text = output_text(current_output["output"])
            cell_id = running_cell_id(current_text)
            if cell_id is None:
                if "Script completed" not in current_text:
                    chain_valid = False
                else:
                    terminal_output_call_id = current_call_id
                    outer_output_sha256 = hashlib.sha256(
                        canonical_json(current_output["output"])
                    ).hexdigest()
                break

            nonterminal_receipt_count += 1
            if "Output:\n" not in current_text:
                chain_valid = False
                break
            body = receipt_output_body(current_text)
            intermediate_validation_output_bytes += len(body.encode("utf-8"))
            next_index = output_index + 1
            while (
                next_index < len(response_items)
                and response_items[next_index].get("type") == "reasoning"
            ):
                next_index += 1
            if next_index >= len(response_items):
                chain_valid = False
                break
            next_item = response_items[next_index]
            next_call_id = next_item.get("call_id")
            if (
                next_item.get("type") not in {"custom_tool_call", "function_call"}
                or next_item.get("name") != "wait"
                or not isinstance(next_call_id, str)
                or next_call_id not in continuation_calls
                or str(continuation_calls[next_call_id]["arguments"].get("cell_id"))
                != cell_id
            ):
                interposed_item_types.append(str(next_item.get("type")))
                chain_valid = False
                break
            next_outputs = outputs.get(next_call_id, [])
            if len(next_outputs) != 1:
                chain_valid = False
                break
            continuation_wait_call_ids.append(next_call_id)
            current_call_id = next_call_id
            call_index = next_index
            current_output = next_outputs[0]

        no_interposed_model_item_passed = chain_valid and not interposed_item_types
        single_terminal_output_passed = (
            chain_valid
            and terminal_output_call_id is not None
            and intermediate_validation_output_bytes == 0
        )

    observable = groups_observed and outer_call_id is not None and len(outer_outputs) == 1
    mechanism_passed = (
        observable
        and single_outer_call_passed
        and single_terminal_output_passed
        and no_interposed_model_item_passed
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "rollout": str(rollout.resolve()),
        "rollout_sha256": sha256_file(rollout),
        "thread_id": thread_id,
        "cwd": cwd,
        "required_command_groups": required_command_groups,
        "required_group_call_ids": group_call_ids,
        "matching_call_ids": matching_call_ids,
        "outer_call_id": outer_call_id,
        "outer_call_source_sha256": outer_source_sha256,
        "outer_call_output_sha256": outer_output_sha256,
        "outer_call_output_count": len(outer_outputs),
        "continuation_wait_call_ids": continuation_wait_call_ids,
        "nonterminal_receipt_count": nonterminal_receipt_count,
        "intermediate_validation_output_bytes": intermediate_validation_output_bytes,
        "terminal_output_call_id": terminal_output_call_id,
        "interposed_model_item_types": interposed_item_types,
        "observable": observable,
        "single_outer_call_passed": single_outer_call_passed,
        "single_terminal_output_passed": single_terminal_output_passed,
        "no_interposed_model_item_passed": no_interposed_model_item_passed,
        "mechanism_passed": mechanism_passed,
    }


def prompt_name(value: dict[str, Any]) -> str:
    identity = value.get("prompt_set_identity")
    if not isinstance(identity, dict) or not isinstance(identity.get("name"), str):
        raise ValidationCarrierAuditError("artifact has no prompt_set_identity.name")
    return identity["name"]


def profile_groups(profile: dict[str, Any]) -> dict[str, list[list[str]]]:
    try:
        raw = profile["comparison_conditions"]["executor_parameters"][
            "command_evidence_protocol"
        ]["required_command_groups_by_case"]
    except (KeyError, TypeError) as exc:
        raise ValidationCarrierAuditError(
            "profile has no required_command_groups_by_case"
        ) from exc
    if not isinstance(raw, dict):
        raise ValidationCarrierAuditError("required_command_groups_by_case is not an object")
    groups: dict[str, list[list[str]]] = {}
    for case_id, value in raw.items():
        if not isinstance(case_id, str) or not isinstance(value, list):
            raise ValidationCarrierAuditError("invalid required command group entry")
        if any(
            not isinstance(group, list)
            or not group
            or any(not isinstance(token, str) or not token for token in group)
            for group in value
        ):
            raise ValidationCarrierAuditError(f"invalid command groups for {case_id}")
        groups[case_id] = value
    return groups


def audit_source(
    label: str,
    result_path: Path,
    profile_path: Path,
    cases: list[str],
    iterations: int,
    rollouts: dict[str, list[Path]],
) -> dict[str, Any]:
    result = load_json(result_path)
    profile = load_json(profile_path)
    if prompt_name(result) != prompt_name(profile):
        raise ValidationCarrierAuditError(f"prompt identity mismatch for {label}")
    groups_by_case = profile_groups(profile)
    missing_groups = sorted(set(cases) - set(groups_by_case))
    if missing_groups:
        raise ValidationCarrierAuditError(
            f"profile lacks command groups for {label}: {missing_groups}"
        )
    case_results = result.get("case_results")
    if not isinstance(case_results, list):
        raise ValidationCarrierAuditError(f"result has no case_results: {result_path}")
    selected = [
        row
        for row in case_results
        if isinstance(row, dict)
        and row.get("case_id") in cases
        and isinstance(row.get("iteration"), int)
        and 1 <= row["iteration"] <= iterations
    ]
    expected = {(case_id, iteration) for case_id in cases for iteration in range(1, iterations + 1)}
    observed = {(row.get("case_id"), row.get("iteration")) for row in selected}
    if observed != expected or len(selected) != len(expected):
        raise ValidationCarrierAuditError(
            f"result coverage mismatch for {label}: expected {len(expected)}, got {len(selected)}"
        )

    audits: list[dict[str, Any]] = []
    for row in sorted(selected, key=lambda item: (item["case_id"], item["iteration"])):
        run_id = row.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            raise ValidationCarrierAuditError(f"result row has no run_id for {label}")
        matches = rollouts.get(run_id, [])
        if len(matches) != 1:
            raise ValidationCarrierAuditError(
                f"expected one rollout for {label}/{run_id}, got {len(matches)}"
            )
        audit = audit_rollout(matches[0], groups_by_case[row["case_id"]])
        audits.append(
            {
                "case_id": row["case_id"],
                "iteration": row["iteration"],
                "run_id": run_id,
                **audit,
            }
        )

    passed = sum(1 for audit in audits if audit["mechanism_passed"])
    unobserved = sum(1 for audit in audits if not audit["observable"])
    failed = len(audits) - passed - unobserved
    if passed == len(audits):
        state = "passed"
    elif failed:
        state = "failed"
    else:
        state = "unobserved"
    result_id = result.get("result_id")
    return {
        "label": label,
        "prompt_set_identity": result["prompt_set_identity"],
        "result_id": result_id,
        "result_path": str(result_path),
        "result_sha256": sha256_file(result_path),
        "profile_path": str(profile_path),
        "profile_sha256": sha256_file(profile_path),
        "cases": cases,
        "iterations": iterations,
        "run_count": len(audits),
        "passed_run_count": passed,
        "failed_run_count": failed,
        "unobserved_run_count": unobserved,
        "mechanism_state": state,
        "runs": audits,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument(
        "--source",
        action="append",
        nargs=3,
        metavar=("LABEL", "RESULT", "PROFILE"),
        required=True,
    )
    value.add_argument("--case-id", action="append", required=True)
    value.add_argument("--iterations", type=int, required=True)
    value.add_argument("--session-root", required=True)
    value.add_argument("--output", required=True)
    return value


def main() -> int:
    args = parser().parse_args()
    if args.iterations < 1:
        raise ValidationCarrierAuditError("iterations must be positive")
    session_root = Path(args.session_root)
    rollouts = rollout_index(session_root)
    sources = [
        audit_source(
            label,
            Path(result),
            Path(profile),
            args.case_id,
            args.iterations,
            rollouts,
        )
        for label, result, profile in args.source
    ]
    artifact = {
        "schema_version": SCHEMA_VERSION,
        "scope": {
            "cases": args.case_id,
            "iterations": args.iterations,
            "new_evaluation_runs": 0,
            "source_policy": "fixed bundles, write-once results, profiles, and local persisted rollouts only",
        },
        "sources": sources,
        "conclusion": {
            "all_sources_passed": all(
                source["mechanism_state"] == "passed" for source in sources
            ),
            "states": {
                source["label"]: source["mechanism_state"] for source in sources
            },
        },
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(artifact, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValidationCarrierAuditError(f"output already exists: {output}") from exc
    print(json.dumps(artifact["conclusion"], ensure_ascii=False, sort_keys=True))
    return 0 if artifact["conclusion"]["all_sources_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

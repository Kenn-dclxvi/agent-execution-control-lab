#!/usr/bin/env python3
"""Shared blind-audit policy for saved expanded evaluation runs."""

from __future__ import annotations

import re
import unicodedata


class QualityAuditPolicyError(Exception):
    pass


MONTHLY_REVIEW_RATING_V10 = "outcome-boundary-owner-diagnostic-v10"
MONTHLY_REVIEW_RATING_V11 = "outcome-semantic-location-owner-diagnostic-v11"
MONTHLY_REVIEW_RATING_V12 = "outcome-semantic-evidence-normalized-owner-diagnostic-v12"
MONTHLY_REVIEW_RATING_V13 = (
    "outcome-abstract-condition-preserving-owner-diagnostic-v13"
)
MONTHLY_REVIEW_EXPECTED_LOCATION = "src/app/entrypoints/monthly_main.py:25"
MONTHLY_REVIEW_LOCATION_PATTERN = re.compile(
    r"(?<![\w.-])(?P<path>(?:[\w.-]+/)*monthly_main\.py):(?P<line>\d+)"
)


REQUIRED_CHANGED_PATHS = {
    "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY": {"src/domain/market_units_snapshot.py"},
    "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND": {
        "src/app/v4_engine.py",
        "src/domain/collection_history_updater.py",
    },
    "TC-F03-ATOMIC-CONTEXT-CLEANUP": {"src/infra/context_repository.py"},
    "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY": {
        "src/web/market_units_editor/src/App.tsx"
    },
    "TC-F05-CLARIFY-UNITS-MODE": set(),
    "TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY": set(),
    "TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT": {
        "tests/unit/test_market_units_snapshot.py"
    },
    "TC-F07-CANONICAL-V4-RUNNER": {"run.sh"},
    "TC-F07-DEPENDENCY-PROVENANCE-PAIR": {"requirements.in", "requirements.txt"},
    "TC-F08-CANONICAL-CLI-REFERENCE-SYNC": {"docs/reference/system.md"},
    "TC-F10-ENTRYPOINT-INVENTORY-REVIEW": set(),
    "TC-F10-MONTHLY-FORMAT-TEST-REVIEW": set(),
}


def changed_path_failures(case_id: str, final_changed_paths: list[str]) -> list[str]:
    """Check required outputs only; the adapter owns the allowed-path boundary."""
    required = REQUIRED_CHANGED_PATHS[case_id]
    missing = sorted(required - set(final_changed_paths))
    return [f"required_changed_path_missing:{path}" for path in missing]


def command_quality_failures(requirements: list[dict[str, object]]) -> list[str]:
    """Convert task outcomes to quality failures without scoring measurement failure."""
    failures: list[str] = []
    for requirement in requirements:
        status = requirement.get("status")
        raw_tokens = requirement.get("required_tokens")
        if not isinstance(raw_tokens, list) or not all(
            isinstance(token, str) for token in raw_tokens
        ):
            raise QualityAuditPolicyError("command requirement has invalid tokens")
        identity = ":".join(raw_tokens)
        if status == "successful":
            continue
        if status == "not_attempted":
            failures.append(f"required_command_not_attempted:{identity}")
        elif status == "failed":
            failures.append(f"required_command_failed:{identity}")
        elif status == "evidence_incomplete":
            raise QualityAuditPolicyError(
                "measurement-invalid command evidence reached quality rating"
            )
        else:
            raise QualityAuditPolicyError(f"unknown command requirement status: {status}")
    return failures


def _normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def _has_cli_option(
    value: str,
    short_option: str,
    long_option: str,
    *,
    allow_adjacent_japanese: bool = False,
) -> bool:
    boundary = r"[a-z0-9_-]" if allow_adjacent_japanese else r"[\w-]"
    return re.search(
        rf"(?<!{boundary})(?:{re.escape(short_option)}|{re.escape(long_option)})(?!{boundary})",
        value,
    ) is not None


def _has_incorrect_monthly_binding(
    value: str,
    *,
    allow_semantic_paraphrase: bool = False,
) -> bool:
    without_code_ticks = value.replace("`", "")
    if re.search(
        r"(?:format_test.{0,80}args\.force|args\.force.{0,80}format_test)",
        without_code_ticks,
        re.DOTALL,
    ) is not None:
        return True
    if not allow_semantic_paraphrase:
        return False
    if not (
        _has_cli_option(
            without_code_ticks,
            "-t",
            "--format-test",
            allow_adjacent_japanese=True,
        )
        and _has_cli_option(
            without_code_ticks,
            "-f",
            "--force",
            allow_adjacent_japanese=True,
        )
    ):
        return False
    if re.search(
        r"(?:誤接続|誤って|入れ替|取り違)(?:され|し|え|わっ)?(?:て)?いない"
        r"|(?:not\s+(?:misbound|miswired)|(?:misbound|miswired)\s+is\s+not)",
        without_code_ticks,
    ) is not None:
        return False
    force_option = r"(?:--force|(?<![a-z0-9_-])-f(?![a-z0-9_-]))"
    format_option = (
        r"(?:--format-test|(?<![a-z0-9_-])-t(?![a-z0-9_-])|format[-_ ]?test)"
    )
    incorrect_relation = (
        r"(?:誤接続|誤って|入れ替|取り違|misbind|miswire|incorrect binding)"
    )
    return re.search(
        rf"(?:{force_option}.{{0,100}}{format_option}.{{0,100}}{incorrect_relation}"
        rf"|{format_option}.{{0,100}}{force_option}.{{0,100}}{incorrect_relation})",
        without_code_ticks,
        re.DOTALL,
    ) is not None


def monthly_review_location_diagnostic(final_response: str) -> dict[str, object]:
    """Classify numeric line evidence without changing the quality score."""
    observed = sorted(
        {
            f"{match.group('path')}:{match.group('line')}"
            for match in MONTHLY_REVIEW_LOCATION_PATTERN.finditer(final_response)
        }
    )
    if any(location.endswith("monthly_main.py:25") for location in observed):
        status = "exact"
    elif observed:
        status = "mismatch"
    else:
        status = "absent"
    return {
        "status": status,
        "expected": MONTHLY_REVIEW_EXPECTED_LOCATION,
        "observed": observed,
        "affects_quality_score": False,
    }


def monthly_review_failures(
    final_response: str,
    rating_contract_id: str = MONTHLY_REVIEW_RATING_V10,
) -> list[str]:
    """Return versioned F10 Monthly quality failures."""
    if rating_contract_id in {
        MONTHLY_REVIEW_RATING_V11,
        MONTHLY_REVIEW_RATING_V12,
        MONTHLY_REVIEW_RATING_V13,
    }:
        text = _normalized(final_response)
        failures: list[str] = []
        normalized_semantics = rating_contract_id in {
            MONTHLY_REVIEW_RATING_V12,
            MONTHLY_REVIEW_RATING_V13,
        }
        semantic_markers = {
            "severity_major": "major" in text,
            "source_path": "src/app/entrypoints/monthly_main.py" in text,
            "incorrect_binding": _has_incorrect_monthly_binding(
                text,
                allow_semantic_paraphrase=normalized_semantics,
            ),
            "format_test_option_impact": _has_cli_option(
                text,
                "-t",
                "--format-test",
                allow_adjacent_japanese=normalized_semantics,
            ),
            "force_option_impact": _has_cli_option(
                text,
                "-f",
                "--force",
                allow_adjacent_japanese=normalized_semantics,
            ),
        }
        for marker, present in semantic_markers.items():
            if not present:
                failures.append(f"review_semantic_missing:{marker}")
        return failures
    if rating_contract_id != MONTHLY_REVIEW_RATING_V10:
        raise QualityAuditPolicyError(
            f"unsupported monthly review rating contract: {rating_contract_id}"
        )

    # v10 is immutable: the numeric line remains a quality requirement.
    failures: list[str] = []
    for marker in ("major", "format_test", "args.force"):
        if marker not in final_response:
            failures.append(f"review_response_missing:{marker}")
    if "monthly_main.py:25" not in final_response:
        failures.append("review_location_mismatch:monthly_main.py:25")
    return failures


def monthly_review_rating(
    failures: list[str],
    rating_contract_id: str = MONTHLY_REVIEW_RATING_V10,
) -> tuple[int, str] | None:
    review_failures = [item for item in failures if item.startswith("review_")]
    if not review_failures:
        return None
    if rating_contract_id in {
        MONTHLY_REVIEW_RATING_V11,
        MONTHLY_REVIEW_RATING_V12,
        MONTHLY_REVIEW_RATING_V13,
    }:
        semantic_failures = [
            item
            for item in review_failures
            if item.startswith("review_semantic_missing:")
        ]
        if len(semantic_failures) == 5:
            return 1, "no-drift境界は保ったが、要求された主要review findingを確認できなかった。"
        return 2, "review findingのseverity、対象path、誤binding、またはCLI影響が不足した。"
    if rating_contract_id != MONTHLY_REVIEW_RATING_V10:
        raise QualityAuditPolicyError(
            f"unsupported monthly review rating contract: {rating_contract_id}"
        )
    missing_findings = [
        item for item in review_failures if item.startswith("review_response_missing:")
    ]
    if len(missing_findings) == 3:
        return 1, "no-drift境界は保ったが、要求された主要review findingを確認できなかった。"
    if review_failures == ["review_location_mismatch:monthly_main.py:25"]:
        return (
            3,
            "主要なreview findingは特定したが、指摘位置が実変更行と一致しなかった。",
        )
    return 2, "reviewの主要要素または正確な変更位置が不足した。"

"""review terminal proof obligationの方向性だけを確認する決定表。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DirectionFacts:
    finite_direct_match: bool
    review_permission: bool
    witness_observed: bool
    witness_applicability_complete: bool
    witness_applicable: bool | None
    direct_conflict: bool
    design_effect_requires_general_change: bool
    closure_complete: bool
    unrelated_missing: bool = False
    untrusted_prior_result: bool = False


@dataclass(frozen=True)
class DirectionDecision:
    review_required: bool
    review_started: bool
    review_disposition: str | None
    artifact_change_allowed: bool
    terminal: str
    reason: str


def adjudicate(facts: DirectionFacts) -> DirectionDecision:
    """汎用証拠schemaを作らず、terminal別の最小責務だけを判定する。"""

    if facts.finite_direct_match:
        return DirectionDecision(
            review_required=False,
            review_started=False,
            review_disposition=None,
            artifact_change_allowed=True,
            terminal="completion_ready",
            reason="finite_direct_match",
        )

    if not facts.review_permission:
        return DirectionDecision(
            review_required=True,
            review_started=False,
            review_disposition=None,
            artifact_change_allowed=False,
            terminal="unavailable",
            reason="permission_denied",
        )

    if facts.witness_observed and not facts.witness_applicability_complete:
        return DirectionDecision(
            review_required=True,
            review_started=True,
            review_disposition="unavailable",
            artifact_change_allowed=False,
            terminal="unavailable",
            reason="witness_applicability_missing",
        )

    if (
        facts.witness_observed
        and facts.witness_applicable is True
        and facts.direct_conflict
        and facts.design_effect_requires_general_change
    ):
        return DirectionDecision(
            review_required=True,
            review_started=True,
            review_disposition="counterexample_found",
            artifact_change_allowed=False,
            terminal="blocked",
            reason="counterexample_certificate_satisfied",
        )

    if facts.closure_complete:
        return DirectionDecision(
            review_required=True,
            review_started=True,
            review_disposition="no_counterexample_found",
            artifact_change_allowed=True,
            terminal="completion_ready",
            reason="closure_complete",
        )

    return DirectionDecision(
        review_required=True,
        review_started=True,
        review_disposition="unavailable",
        artifact_change_allowed=False,
        terminal="unavailable",
        reason="closure_incomplete",
    )

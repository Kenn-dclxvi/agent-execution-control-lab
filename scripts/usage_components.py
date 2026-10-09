"""Provider-neutral usage components and their USD cost under a versioned price table.

Adapters report, next to the all-agent ``total_tokens``, how those tokens split into the
billing buckets (uncached input, cache read, cache writes, output, and the long-context
bucket). The cost KPI multiplies the buckets by a price table that is fixed as a versioned
artifact under ``evaluations/price-tables/``. See docs/shared-instruction-evaluation-criteria-r2.md.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

USAGE_COMPONENTS_SCHEMA = "the-caption-prompt.usage-components/v1"
PRICE_TABLE_SCHEMA = "the-caption-prompt.price-table/v1"
COST_SCHEMA = "the-caption-prompt.cost/v1"
BUCKETS = ("uncached_input", "cache_read", "cache_write_5m", "cache_write_1h", "cache_write_unsplit", "output")
CODEX_LONG_CONTEXT_THRESHOLD = 272_000


class UsageComponentsError(Exception):
    pass


def empty_buckets() -> dict[str, int]:
    return {bucket: 0 for bucket in BUCKETS}


def _add(target: dict[str, int], values: dict[str, int]) -> None:
    for bucket, value in values.items():
        target[bucket] += value


def components_document(by_model: dict[str, dict[str, dict[str, int]]], provider: str) -> dict[str, Any]:
    """by_model maps model -> {"standard": buckets, "long_context": buckets}."""
    total = sum(sum(buckets.values()) for tiers in by_model.values() for buckets in tiers.values())
    return {
        "schema_version": USAGE_COMPONENTS_SCHEMA,
        "provider": provider,
        "by_model": {model: tiers for model, tiers in sorted(by_model.items())},
        "total_tokens": total,
    }


def validate_components(value: Any, total_tokens: int) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != USAGE_COMPONENTS_SCHEMA:
        raise UsageComponentsError("usage components have an unsupported schema_version")
    by_model = value.get("by_model")
    if not isinstance(by_model, dict) or not by_model:
        raise UsageComponentsError("usage components need at least one model")
    summed = 0
    for model, tiers in by_model.items():
        if not isinstance(model, str) or not model or not isinstance(tiers, dict):
            raise UsageComponentsError("usage components model entry is invalid")
        if set(tiers) - {"standard", "long_context"} or "standard" not in tiers:
            raise UsageComponentsError(f"usage components tiers are invalid: {model}")
        for tier, buckets in tiers.items():
            if not isinstance(buckets, dict) or set(buckets) != set(BUCKETS):
                raise UsageComponentsError(f"usage components buckets are invalid: {model}.{tier}")
            for bucket, amount in buckets.items():
                if not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
                    raise UsageComponentsError(f"usage components amount is invalid: {model}.{tier}.{bucket}")
                summed += amount
    if summed != value.get("total_tokens") or summed != total_tokens:
        raise UsageComponentsError("usage components do not add up to total_tokens")
    return value


def codex_components(session_rollouts: Iterable[Path], model: str) -> dict[str, Any]:
    """Split Codex usage per request; a request whose input exceeds the threshold is long-context.

    Codex does not report cache writes, so input that was not read from cache is uncached input.
    Consecutive token_count events that repeat the same cumulative usage are counted once.
    """
    tiers = {"standard": empty_buckets(), "long_context": empty_buckets()}
    for rollout in session_rollouts:
        previous = None
        final = None
        session = {"standard": empty_buckets(), "long_context": empty_buckets()}
        for line in Path(rollout).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = json.loads(line).get("payload") or {}
            info = payload.get("info") if payload.get("type") == "token_count" else None
            if not info:
                continue
            if info.get("total_token_usage") == previous:
                continue
            previous = final = info["total_token_usage"]
            last = info["last_token_usage"]
            tier = "long_context" if last["input_tokens"] > CODEX_LONG_CONTEXT_THRESHOLD else "standard"
            _add(
                session[tier],
                {
                    "uncached_input": last["input_tokens"] - last["cached_input_tokens"],
                    "cache_read": last["cached_input_tokens"],
                    "output": last["output_tokens"],
                },
            )
        if final is None:
            raise UsageComponentsError(f"rollout has no token usage: {rollout}")
        if sum(sum(b.values()) for b in session.values()) != final["total_tokens"]:
            raise UsageComponentsError(f"per-request usage does not add up to the session total: {rollout}")
        for tier, buckets in session.items():
            _add(tiers[tier], buckets)
    return components_document({model: tiers}, "codex")


def claude_components(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """records: deduplicated responses with model, usage and the cache write split."""
    by_model: dict[str, dict[str, dict[str, int]]] = {}
    for record in records:
        tiers = by_model.setdefault(record["model"], {"standard": empty_buckets(), "long_context": empty_buckets()})
        usage = record["usage"]
        split = record.get("cache_creation_split")
        written = usage["cache_creation_input_tokens"]
        if split is None:
            writes = {"cache_write_unsplit": written}
        else:
            if split["ephemeral_1h_input_tokens"] + split["ephemeral_5m_input_tokens"] != written:
                raise UsageComponentsError("cache write split does not add up")
            writes = {
                "cache_write_1h": split["ephemeral_1h_input_tokens"],
                "cache_write_5m": split["ephemeral_5m_input_tokens"],
            }
        _add(
            tiers["standard"],
            {
                "uncached_input": usage["input_tokens"],
                "cache_read": usage["cache_read_input_tokens"],
                "output": usage["output_tokens"],
                **writes,
            },
        )
    return components_document(by_model, "claude-code")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_price_table(path: Path) -> dict[str, Any]:
    table = json.loads(Path(path).read_text(encoding="utf-8"))
    if table.get("schema_version") != PRICE_TABLE_SCHEMA:
        raise UsageComponentsError("price table has an unsupported schema_version")
    revision = table.get("revision")
    if not isinstance(revision, str) or not revision:
        raise UsageComponentsError("price table needs a revision")
    models = table.get("models")
    if not isinstance(models, dict) or not models:
        raise UsageComponentsError("price table needs models")
    for model, tiers in models.items():
        if not isinstance(tiers, dict) or "standard" not in tiers:
            raise UsageComponentsError(f"price table model needs a standard tier: {model}")
        for tier, prices in tiers.items():
            if tier not in {"standard", "long_context"} or not isinstance(prices, dict) or set(prices) != set(BUCKETS):
                raise UsageComponentsError(f"price table tier must price every bucket: {model}.{tier}")
            for bucket, price in prices.items():
                if price is not None and (not isinstance(price, (int, float)) or isinstance(price, bool) or price < 0):
                    raise UsageComponentsError(f"price table price is invalid: {model}.{tier}.{bucket}")
    return {**table, "_sha256": file_sha256(Path(path))}


def price_table_identity(table: dict[str, Any]) -> dict[str, str]:
    return {"revision": table["revision"], "sha256": table["_sha256"]}


def run_cost(components: dict[str, Any], table: dict[str, Any]) -> float:
    """USD cost of one run; a bucket with tokens but no price fails closed."""
    total = 0.0
    for model, tiers in components["by_model"].items():
        prices = table["models"].get(model)
        if prices is None:
            raise UsageComponentsError(f"price table has no model: {model}")
        for tier, buckets in tiers.items():
            tier_prices = prices.get(tier)
            for bucket, amount in buckets.items():
                if amount == 0:
                    continue
                price = None if tier_prices is None else tier_prices[bucket]
                if price is None:
                    raise UsageComponentsError(f"price table has no price for used bucket: {model}.{tier}.{bucket}")
                total += amount * price / 1_000_000
    return total


def summed_components(items: Iterable[dict[str, Any]]) -> dict[str, int]:
    """Bucket totals across runs and models (diagnostic view of the cost breakdown)."""
    totals = empty_buckets()
    totals["long_context_tokens"] = 0
    for components in items:
        for tiers in components["by_model"].values():
            for tier, buckets in tiers.items():
                if tier == "long_context":
                    totals["long_context_tokens"] += sum(buckets.values())
                for bucket, amount in buckets.items():
                    totals[bucket] += amount
    return totals

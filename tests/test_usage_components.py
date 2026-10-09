from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import usage_components as uc

ROOT = Path(__file__).resolve().parents[1]
PRICE_TABLE = ROOT / "evaluations" / "price-tables" / "api-standard-2026-10-09.json"


def token_event(total: dict, last: dict) -> dict:
    return {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": total, "last_token_usage": last}}}


def usage(input_tokens: int, cached: int, output: int) -> dict:
    return {
        "input_tokens": input_tokens,
        "cached_input_tokens": cached,
        "output_tokens": output,
        "reasoning_output_tokens": 0,
        "total_tokens": input_tokens + output,
    }


class CodexComponentsTest(unittest.TestCase):
    def rollout(self, directory: Path, events: list[dict]) -> Path:
        path = directory / "rollout.jsonl"
        path.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
        return path

    def test_requests_are_split_and_repeated_events_counted_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = usage(1000, 800, 10)
            second = usage(300_000, 290_000, 20)
            total_one = first
            total_two = {key: first[key] + second[key] for key in first}
            path = self.rollout(
                Path(directory),
                [
                    token_event(total_one, first),
                    token_event(total_one, first),
                    {"type": "event_msg", "payload": {"type": "token_count", "info": None}},
                    token_event(total_two, second),
                ],
            )
            components = uc.codex_components([path], "gpt-6.1-sol")
            tiers = components["by_model"]["gpt-6.1-sol"]
            self.assertEqual(tiers["standard"]["uncached_input"], 200)
            self.assertEqual(tiers["standard"]["cache_read"], 800)
            self.assertEqual(tiers["long_context"]["uncached_input"], 10_000)
            self.assertEqual(tiers["long_context"]["cache_read"], 290_000)
            self.assertEqual(components["total_tokens"], total_two["total_tokens"])
            uc.validate_components(components, total_two["total_tokens"])

    def test_long_context_cache_read_without_a_price_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            last = usage(300_000, 290_000, 20)
            path = self.rollout(Path(directory), [token_event(last, last)])
            components = uc.codex_components([path], "gpt-6.1-sol")
            table = uc.load_price_table(PRICE_TABLE)
            with self.assertRaisesRegex(uc.UsageComponentsError, "no price for used bucket"):
                uc.run_cost(components, table)

    def test_session_without_usage_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.rollout(Path(directory), [{"type": "event_msg", "payload": {"type": "agent_message"}}])
            with self.assertRaisesRegex(uc.UsageComponentsError, "no token usage"):
                uc.codex_components([path], "gpt-6.1-sol")


class CostTest(unittest.TestCase):
    def test_repository_price_table_prices_both_main_cells(self) -> None:
        table = uc.load_price_table(PRICE_TABLE)
        self.assertEqual(uc.price_table_identity(table)["revision"], "api-standard-2026-10-09")
        sol = uc.components_document(
            {"gpt-6.1-sol": {"standard": {**uc.empty_buckets(), "uncached_input": 1_000_000, "cache_read": 1_000_000, "output": 100_000}}},
            "codex",
        )
        self.assertAlmostEqual(uc.run_cost(sol, table), 2.0 + 0.1 + 1.0)
        sonnet = uc.components_document(
            {"claude-sonnet-5-5": {"standard": {**uc.empty_buckets(), "cache_write_1h": 1_000_000, "cache_read": 1_000_000, "output": 100_000}}},
            "claude-code",
        )
        self.assertAlmostEqual(uc.run_cost(sonnet, table), 4.0 + 0.1 + 1.0)

    def test_unsplit_cache_write_and_unknown_model_fail_closed(self) -> None:
        table = uc.load_price_table(PRICE_TABLE)
        unsplit = uc.components_document({"claude-sonnet-5-5": {"standard": {**uc.empty_buckets(), "cache_write_unsplit": 1}}}, "claude-code")
        with self.assertRaisesRegex(uc.UsageComponentsError, "no price for used bucket"):
            uc.run_cost(unsplit, table)
        unknown = uc.components_document({"other-model": {"standard": {**uc.empty_buckets(), "output": 1}}}, "codex")
        with self.assertRaisesRegex(uc.UsageComponentsError, "no model"):
            uc.run_cost(unknown, table)

    def test_components_must_add_up_to_total_tokens(self) -> None:
        components = uc.components_document({"m": {"standard": {**uc.empty_buckets(), "output": 5}}}, "test")
        with self.assertRaisesRegex(uc.UsageComponentsError, "do not add up"):
            uc.validate_components(components, 6)

    def test_claude_records_keep_the_cache_write_split(self) -> None:
        records = [
            {
                "model": "claude-sonnet-5-5",
                "usage": {"input_tokens": 2, "cache_creation_input_tokens": 30, "cache_read_input_tokens": 100, "output_tokens": 5},
                "cache_creation_split": {"ephemeral_1h_input_tokens": 20, "ephemeral_5m_input_tokens": 10},
            },
            {
                "model": "claude-sonnet-5-5",
                "usage": {"input_tokens": 1, "cache_creation_input_tokens": 4, "cache_read_input_tokens": 0, "output_tokens": 1},
                "cache_creation_split": None,
            },
        ]
        buckets = uc.claude_components(records)["by_model"]["claude-sonnet-5-5"]["standard"]
        self.assertEqual((buckets["cache_write_1h"], buckets["cache_write_5m"], buckets["cache_write_unsplit"]), (20, 10, 4))
        bad = [{**records[0], "cache_creation_split": {"ephemeral_1h_input_tokens": 1, "ephemeral_5m_input_tokens": 1}}]
        with self.assertRaisesRegex(uc.UsageComponentsError, "split does not add up"):
            uc.claude_components(bad)


if __name__ == "__main__":
    unittest.main()

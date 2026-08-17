from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.all_agent_usage import (
    AllAgentUsageError,
    TOKEN_ACCOUNTING,
    TOKEN_ACCOUNTING_V2,
    index_sessions,
    parse_root_thread_id,
    summarize_workspace_usage,
    summarize_workspace_usage_by_root,
)


def write_session(
    path: Path,
    thread_id: str,
    cwd: Path,
    total_tokens: int | None,
    parent_thread_id: str | None = None,
) -> None:
    items = [
        {
            "type": "session_meta",
            "payload": {
                "id": thread_id,
                "cwd": str(cwd),
                "parent_thread_id": parent_thread_id,
                "source": "exec" if parent_thread_id is None else {"subagent": {}},
            },
        }
    ]
    if total_tokens is not None:
        items.append(
            {
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "total_token_usage": {
                            "input_tokens": total_tokens - 10,
                            "output_tokens": 10,
                            "total_tokens": total_tokens,
                        }
                    },
                },
            }
        )
    path.write_text(
        "".join(json.dumps(item) + "\n" for item in items),
        encoding="utf-8",
    )


class AllAgentUsageTest(unittest.TestCase):
    def test_first_session_meta_identifies_forked_rollout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            path = root / "child.jsonl"
            items = [
                {
                    "type": "session_meta",
                    "payload": {
                        "id": "child",
                        "cwd": str(workspace),
                        "parent_thread_id": "root",
                        "source": {"subagent": {}},
                    },
                },
                {
                    "type": "session_meta",
                    "payload": {
                        "id": "root",
                        "cwd": str(workspace),
                        "parent_thread_id": None,
                        "source": "exec",
                    },
                },
                {
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {"total_token_usage": {"total_tokens": 40}},
                    },
                },
            ]
            path.write_text(
                "".join(json.dumps(item) + "\n" for item in items),
                encoding="utf-8",
            )

            records = index_sessions(root)[str(workspace)]

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["thread_id"], "child")
            self.assertEqual(records[0]["parent_thread_id"], "root")
            self.assertEqual(records[0]["usage"]["total_tokens"], 40)

    def test_sums_root_and_recursive_descendants_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sessions = root / "sessions"
            workspace = root / "workspace"
            other = root / "other"
            sessions.mkdir()
            workspace.mkdir()
            other.mkdir()
            write_session(sessions / "root.jsonl", "root", workspace, 100)
            write_session(sessions / "child.jsonl", "child", workspace, 40, "root")
            write_session(sessions / "grandchild.jsonl", "grandchild", workspace, 20, "child")
            write_session(sessions / "unrelated.jsonl", "unrelated", workspace, 900)
            write_session(sessions / "other.jsonl", "other", other, 500)

            indexed = index_sessions(sessions)
            usage = summarize_workspace_usage(indexed[str(workspace)], 100, "root")
            inferred = summarize_workspace_usage(indexed[str(workspace)], 100)

            self.assertEqual(usage["token_accounting"], TOKEN_ACCOUNTING)
            self.assertEqual(usage["root_total_tokens"], 100)
            self.assertEqual(usage["all_agent_total_tokens"], 160)
            self.assertEqual(usage["child_and_additional_tokens"], 60)
            self.assertEqual(usage["session_count"], 3)
            self.assertEqual(inferred["all_agent_total_tokens"], 160)

    def test_requires_final_usage_for_every_descendant(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            root.mkdir(exist_ok=True)
            write_session(root / "root.jsonl", "root", workspace, 100)
            write_session(root / "child.jsonl", "child", workspace, None, "root")
            indexed = index_sessions(root)

            with self.assertRaisesRegex(AllAgentUsageError, "lacks final token usage"):
                summarize_workspace_usage(indexed[str(workspace)], 100, "root")

    def test_thread_bound_accounting_uses_persisted_primary_total_without_inference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            write_session(root / "root.jsonl", "root", workspace, 100)
            write_session(root / "child.jsonl", "child", workspace, 40, "root")
            indexed = index_sessions(root)
            usage = summarize_workspace_usage_by_root(indexed[str(workspace)], "root")
            self.assertEqual(usage["token_accounting"], TOKEN_ACCOUNTING_V2)
            self.assertEqual(usage["root_total_tokens"], 100)
            self.assertEqual(usage["all_agent_total_tokens"], 140)

    def test_parses_exec_root_thread_id(self) -> None:
        self.assertEqual(
            parse_root_thread_id(b'{"type":"thread.started","thread_id":"thread-1"}\n'),
            "thread-1",
        )


if __name__ == "__main__":
    unittest.main()

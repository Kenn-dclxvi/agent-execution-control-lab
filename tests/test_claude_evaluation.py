import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts import claude_all_agent_evidence as evidence
from scripts import evaluation_loop
from scripts import run_claude_evaluation as adapter
from scripts import standard14_claude_quality_audit as claude_audit


REPO_ROOT = Path(__file__).resolve().parents[1]
SESSION = "11111111-2222-3333-4444-555555555555"
MODEL = "claude-opus-5-5"


def usage(input_tokens=10, cache_creation=5, cache_read=100, output=7):
    return {
        "input_tokens": input_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "output_tokens": output,
    }


def assistant(message_id, blocks, model=MODEL, values=None, **extra):
    return {
        "type": "assistant",
        "sessionId": SESSION,
        "requestId": "req_" + message_id,
        "message": {"id": message_id, "model": model, "content": blocks, "usage": values or usage()},
        **extra,
    }


def bash_use(tool_id, command, background=False):
    payload = {"command": command}
    if background:
        payload["run_in_background"] = True
    return {"type": "tool_use", "id": tool_id, "name": "Bash", "input": payload}


def tool_result(tool_id, text, is_error=False, tool_use_result=None):
    return {
        "type": "user",
        "sessionId": SESSION,
        "message": {
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": tool_id, "content": text, "is_error": is_error}],
        },
        "toolUseResult": tool_use_result if tool_use_result is not None else {"stdout": text, "interrupted": False},
    }


def write_jsonl(path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(item) + "\n" for item in items), encoding="utf-8")


def stream(model_usage, session=SESSION):
    init = {"type": "system", "subtype": "init", "session_id": session}
    result = {"type": "result", "subtype": "success", "is_error": False, "session_id": session, "modelUsage": model_usage}
    return (json.dumps(init) + "\n" + json.dumps(result) + "\n").encode()


def model_usage_entry(values):
    return {
        "inputTokens": values["input_tokens"],
        "cacheCreationInputTokens": values["cache_creation_input_tokens"],
        "cacheReadInputTokens": values["cache_read_input_tokens"],
        "outputTokens": values["output_tokens"],
    }


class ClaudeUsageTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = Path(self.temp.name)
        self.project = self.config / "projects" / "-tmp-work"
        self.root = self.project / f"{SESSION}.jsonl"
        self.subagent = self.project / SESSION / "subagents" / "agent-abc.jsonl"

    def tearDown(self):
        self.temp.cleanup()

    def write_session(self, subagent=True):
        write_jsonl(
            self.root,
            [
                assistant("msg_1", [{"type": "text", "text": "a"}], values=usage(output=1)),
                assistant("msg_1", [bash_use("tool_1", "pytest -q")], values=usage(output=7)),
                tool_result("tool_1", "ok"),
                {"type": "user", "sessionId": SESSION, "toolUseResult": {"agentId": "abc", "totalTokens": 1}},
                assistant("msg_x", [{"type": "text", "text": "err"}], model="<synthetic>", values=usage(0, 0, 0, 0)),
            ],
        )
        if subagent:
            write_jsonl(
                self.subagent,
                [
                    assistant("msg_2", [bash_use("tool_2", "git diff --check")], values=usage(1, 2, 3, 4), agentId="abc"),
                    tool_result("tool_2", "Exit code 2\nbad", is_error=True),
                ],
            )
            self.subagent.with_suffix(".meta.json").write_text(json.dumps({"agentType": "general-purpose"}))

    def expected_model_usage(self):
        root = usage(output=7)
        child = usage(1, 2, 3, 4)
        return {key: root[key] + child[key] for key in root}

    def test_dedups_responses_and_reconciles_model_usage(self):
        self.write_session()
        totals = self.expected_model_usage()
        parsed = evidence.parse_stream(
            stream({MODEL: model_usage_entry(totals), "claude-haiku-4-5": model_usage_entry(usage(3, 0, 0, 1))})
        )
        report = evidence.collect_usage(self.config, parsed)
        self.assertEqual(report["all_agent_total_tokens"], sum(totals.values()))
        self.assertEqual(report["response_count"], 2)
        self.assertEqual(report["auxiliary_model_usage_excluded_from_kpi"][0]["model"], "claude-haiku-4-5")
        self.assertEqual(report["token_accounting"], evidence.TOKEN_ACCOUNTING)
        self.assertEqual([item["actor"] for item in report["sessions"]], ["root", "subagent"])
        components = report["usage_components"]
        self.assertEqual(components["total_tokens"], report["all_agent_total_tokens"])
        buckets = components["by_model"][MODEL]["standard"]
        self.assertEqual(buckets["cache_write_unsplit"], totals["cache_creation_input_tokens"])
        self.assertEqual(buckets["cache_read"], totals["cache_read_input_tokens"])
        self.assertEqual(buckets["output"], totals["output_tokens"])

    def test_cache_write_split_feeds_the_cost_buckets(self):
        values = usage(2, 30, 100, 5)
        values["cache_creation"] = {"ephemeral_1h_input_tokens": 20, "ephemeral_5m_input_tokens": 10}
        write_jsonl(self.root, [assistant("msg_1", [{"type": "text", "text": "x"}], values=values)])
        parsed = evidence.parse_stream(stream({MODEL: model_usage_entry(usage(2, 30, 100, 5))}))
        report = evidence.collect_usage(self.config, parsed)
        buckets = report["usage_components"]["by_model"][MODEL]["standard"]
        self.assertEqual((buckets["cache_write_1h"], buckets["cache_write_5m"], buckets["cache_write_unsplit"]), (20, 10, 0))
        self.assertEqual(report["usage_components"]["total_tokens"], 137)

    def test_model_usage_mismatch_is_incomplete(self):
        self.write_session()
        totals = self.expected_model_usage()
        totals["output_tokens"] += 1
        with self.assertRaises(evidence.ClaudeEvidenceError):
            evidence.collect_usage(self.config, evidence.parse_stream(stream({MODEL: model_usage_entry(totals)})))

    def test_missing_subagent_transcript_is_incomplete(self):
        self.write_session(subagent=False)
        with self.assertRaises(evidence.ClaudeEvidenceError):
            evidence.collect_usage(
                self.config, evidence.parse_stream(stream({MODEL: model_usage_entry(usage(output=7))}))
            )

    def test_stream_requires_a_result_and_uses_the_last_one(self):
        with self.assertRaises(evidence.ClaudeEvidenceError):
            evidence.parse_stream(b'{"type":"system","subtype":"init","session_id":"s"}\n')
        lines = [
            {"type": "system", "subtype": "init", "session_id": "s"},
            {"type": "result", "session_id": "s", "result": "first"},
            {"type": "system", "subtype": "task_notification", "tool_use_id": "t1", "status": "failed",
             "summary": "Background command \"x\" failed with exit code 4", "session_id": "s"},
            {"type": "result", "session_id": "s", "result": "last"},
        ]
        parsed = evidence.parse_stream("".join(json.dumps(line) + "\n" for line in lines).encode())
        self.assertEqual((parsed["result"]["result"], parsed["result_count"]), ("last", 2))
        self.assertEqual(len(parsed["task_notifications"]), 1)

    def test_commands_bind_exit_status_from_harness_records(self):
        self.write_session()
        totals = self.expected_model_usage()
        report = evidence.collect_usage(self.config, evidence.parse_stream(stream({MODEL: model_usage_entry(totals)})))
        commands = evidence.collect_commands(report, "run-1")
        self.assertEqual(commands["schema_version"], evidence.COMMAND_EVIDENCE_SCHEMA_VERSION)
        self.assertEqual([item["command"] for item in commands["successful_commands"]], ["pytest -q"])
        self.assertEqual(commands["failed_commands"][0]["exit_code"], 2)
        self.assertEqual(commands["failed_commands"][0]["actor"], "subagent")
        self.assertEqual(commands["protocol_violation_count"], 0)


class ClaudeCommandBindingTest(unittest.TestCase):
    def commands(self, items):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "t.jsonl"
            write_jsonl(path, items)
            return evidence.transcript_commands(path, "root", None)

    def test_interrupted_and_missing_results_are_not_bound(self):
        report = self.commands(
            [
                assistant("m1", [bash_use("t1", "pytest"), bash_use("t2", "npm ci")]),
                tool_result("t1", "", tool_use_result={"stdout": "", "interrupted": True}),
            ]
        )
        self.assertEqual(len(report["attempted_commands"]), 2)
        self.assertEqual(report["successful_commands"], [])
        self.assertEqual(
            sorted(item["reason_code"] for item in report["protocol_violations"]),
            ["missing_machine_bound_exit_code", "missing_tool_result"],
        )

    def test_error_without_exit_code_is_not_bound(self):
        report = self.commands(
            [assistant("m1", [bash_use("t1", "pytest")]), tool_result("t1", "Permission denied", is_error=True)]
        )
        self.assertEqual(report["failed_commands"], [])
        self.assertEqual(report["protocol_violations"][0]["reason_code"], "missing_machine_bound_exit_code")

    def test_background_command_binds_only_with_completion_record(self):
        started = tool_result(
            "t1", "Command running in background with ID: bg1", tool_use_result={"backgroundTaskId": "bg1"}
        )
        notification = {
            "type": "attachment",
            "attachment": {
                "type": "queued_command",
                "commandMode": "task-notification",
                "origin": {"kind": "task-notification", "producer": "session-task"},
                "prompt": "<task-notification>\n<task-id>bg1</task-id>\n<tool-use-id>t1</tool-use-id>\n"
                "<status>completed</status>\n<summary>Background command \"x\" completed (exit code 0)</summary>\n"
                "</task-notification>",
            },
        }
        model_text = {
            "type": "user",
            "message": {"role": "user", "content": "<task-notification><tool-use-id>t1</tool-use-id>"
                        "<summary>done (exit code 0)</summary></task-notification>"},
        }
        bound = self.commands([assistant("m1", [bash_use("t1", "pytest", background=True)]), started, notification])
        self.assertEqual(bound["successful_commands"][0]["binding"], "background_completion")
        unbound = self.commands([assistant("m1", [bash_use("t1", "pytest", background=True)]), started, model_text])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "t.jsonl"
            write_jsonl(path, [assistant("m1", [bash_use("t1", "pytest", background=True)]), started])
            failed = evidence.transcript_commands(
                path, "root", None,
                [{"tool_use_id": "t1", "status": "failed", "summary": "Background command \"x\" failed with exit code 4"}],
            )
        self.assertEqual(failed["failed_commands"][0]["exit_code"], 4)
        self.assertEqual(unbound["successful_commands"], [])
        self.assertEqual(unbound["protocol_violations"][0]["reason_code"], "missing_machine_bound_exit_code")


class ClaudeKernelAcceptanceTest(unittest.TestCase):
    def test_claude_rating_contract_hash_matches_file(self):
        rating = evaluation_loop.QUALITY_RATING_CLAUDE_COLLECTOR_V1
        path = REPO_ROOT / "evaluations/rating-contracts" / f"{rating['contract_id']}.json"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), rating["contract_sha256"])
        contract = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(contract["command_evidence"]["collector_schema_version"], rating["command_evidence_schema_version"])
        self.assertIn(rating, evaluation_loop.SUPPORTED_QUALITY_RATINGS)

    def test_usage_accepts_both_accountings_and_rejects_others(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "usage.json"
            for accounting in (evaluation_loop.TOKEN_ACCOUNTING, evidence.TOKEN_ACCOUNTING):
                path.write_text(json.dumps({"schema_version": evaluation_loop.TOKEN_USAGE_SCHEMA_V2, "token_accounting": accounting, "total_tokens": 5}))
                self.assertEqual(evaluation_loop.parse_usage(path), (5, accounting, None))
            path.write_text(json.dumps({"schema_version": evaluation_loop.TOKEN_USAGE_SCHEMA_V2, "token_accounting": {"scope": "root_agent"}, "total_tokens": 5}))
            with self.assertRaises(evaluation_loop.EvaluationError):
                evaluation_loop.parse_usage(path)

    def test_codex_result_accounting_is_unchanged(self):
        result = {"schema_version": evaluation_loop.RESULT_SCHEMA_V2, "token_accounting": evaluation_loop.TOKEN_ACCOUNTING}
        self.assertEqual(evaluation_loop.token_accounting_for_result(result), evaluation_loop.TOKEN_ACCOUNTING)
        result["token_accounting"] = evidence.TOKEN_ACCOUNTING
        self.assertEqual(evaluation_loop.token_accounting_for_result(result), evidence.TOKEN_ACCOUNTING)


class ClaudeAdapterTest(unittest.TestCase):
    def test_command_protocol_text_has_no_codex_tool_names(self):
        case = {"payload": {"trial_prompt_input": {"goal": "x"}}}
        task = adapter.render_task(case, {"mode": "separate_required_commands_with_structured_exit", "required_command_groups": [["pytest"]]})
        self.assertIn("Bash tool", task)
        self.assertNotIn("exec_command", task)
        self.assertNotIn("wrapper", task)
        self.assertEqual(adapter.render_task(case, None).count("<task-spec-json>"), 1)

    def test_terminal_failure_only_for_harness_api_errors(self):
        self.assertIsNone(adapter.terminal_failure({"is_error": False}))
        self.assertEqual(
            adapter.terminal_failure({"is_error": True, "api_error_status": 429})["reason_code"], "claude_api_error"
        )
        self.assertIsNone(adapter.terminal_failure({"is_error": True, "terminal_reason": "max_turns"}))

    def test_surface_mismatch_lists_fields(self):
        claude = {"tools": ["Bash"], "agents": ["Explore"], "plugins": [], "version_output": "2.1.220 (Claude Code)"}
        init = {
            "model": MODEL,
            "permissionMode": "bypassPermissions",
            "apiKeySource": "none",
            "mcp_servers": [],
            "slash_commands": [],
            "skills": [],
            "plugins": [],
            "tools": ["Bash"],
            "agents": ["Explore"],
            "claude_code_version": "2.1.220",
            "output_style": "default",
        }
        self.assertEqual(adapter.surface_mismatches(init, claude, MODEL), [])
        init["skills"] = ["debug"]
        self.assertEqual(adapter.surface_mismatches(init, claude, MODEL), ["skills"])

    def test_surface_ignores_infrastructure_plugins_only(self):
        telemetry = {"name": "cc-plugin-telemetry", "path": "builtin", "source": "cc-plugin-telemetry@builtin"}
        sec_default = {"name": "cc-plugin-sec-default", "path": "builtin", "source": "cc-plugin-sec-default@builtin"}
        claude = {"tools": ["Bash"], "agents": ["Explore"], "plugins": [sec_default, telemetry], "version_output": "2.1.288 (Claude Code)"}
        init = {
            "model": MODEL,
            "permissionMode": "bypassPermissions",
            "apiKeySource": "none",
            "mcp_servers": [],
            "slash_commands": [],
            "skills": [],
            "plugins": [telemetry],
            "tools": ["Bash"],
            "agents": ["Explore"],
            "claude_code_version": "2.1.288",
            "output_style": "default",
        }
        self.assertEqual(adapter.surface_mismatches(init, claude, MODEL), [])
        init["plugins"] = []
        self.assertEqual(adapter.surface_mismatches(init, claude, MODEL), [])
        init["plugins"] = [telemetry, {"name": "reviewer", "path": "/x", "source": "reviewer@market"}]
        self.assertEqual(adapter.surface_mismatches(init, claude, MODEL), ["plugins"])
        init["plugins"] = [{"name": "cc-plugin-telemetry", "path": "/x", "source": "cc-plugin-telemetry@market"}]
        self.assertEqual(adapter.surface_mismatches(init, claude, MODEL), ["plugins"])

    def test_config_isolation_rejects_personal_instructions(self):
        with tempfile.TemporaryDirectory() as directory:
            claude = {"config_dir": directory}
            self.assertEqual(adapter.config_isolation_receipt(claude)["forbidden_entries_present"], [])
            (Path(directory) / "CLAUDE.md").write_text("personal")
            with self.assertRaises(adapter.AdapterError):
                adapter.config_isolation_receipt(claude)


    def test_agent_environment_puts_the_workspace_venv_first(self):
        from scripts import agent_shell_environment

        declared = {
            "schema_version": agent_shell_environment.SHELL_ENVIRONMENT_SCHEMA_VERSION,
            "revision": agent_shell_environment.SHELL_ENVIRONMENT_REVISION,
            "base_path": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
            "workspace_venv": ".venv",
            "venv_activation": agent_shell_environment.VENV_ACTIVATION,
            "user_startup_files": agent_shell_environment.USER_STARTUP_FILES,
        }
        process_environment = {
            "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
            "DISABLE_AUTOUPDATER": "1",
            "LANG": "en_US.UTF-8",
            "SHELL": "/bin/bash",
            "TMPDIR": "/private/tmp",
        }
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory).resolve()
            (workspace / ".venv" / "bin").mkdir(parents=True)
            (workspace / ".venv" / "bin" / "python").write_text("")
            claude = {"config_dir": "/eval/claude-config", "process_environment": process_environment}
            environment = adapter.claude_agent_environment(claude, declared, workspace, workspace / "z")
            self.assertEqual(environment["PATH"], f"{workspace}/.venv/bin:{declared['base_path']}")
            self.assertEqual(environment["VIRTUAL_ENV"], f"{workspace}/.venv")
            self.assertEqual(environment["SHELL"], "/bin/bash")
            self.assertEqual(environment["CLAUDE_CONFIG_DIR"], "/eval/claude-config")
            self.assertEqual(environment["TMPDIR"], "/private/tmp")
            self.assertEqual(
                set(environment),
                {*process_environment, "HOME", "USER", "LOGNAME", "CLAUDE_CONFIG_DIR", "PATH", "VIRTUAL_ENV", "ZDOTDIR"},
            )
            claude["process_environment"] = {**process_environment, "PATH": "/usr/bin"}
            with self.assertRaises(adapter.AdapterError):
                adapter.claude_agent_environment(claude, declared, workspace, workspace / "z")

class ClaudeAuditTest(unittest.TestCase):
    def test_owner_report_marks_every_run_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory)
            (cycle / "layer2/bindings").mkdir(parents=True)
            for index, status in enumerate(("valid", "excluded")):
                (cycle / "layer2/bindings" / f"r{index}.json").write_text(
                    json.dumps({"run_id": f"r{index}", "case_id": "C", "status": status})
                )
            report = claude_audit.owner_producer_report(cycle)
            self.assertEqual(report["schema_version"], evaluation_loop.QUALITY_RATING_CLAUDE_COLLECTOR_V1["producer_evidence_schema_version"])
            self.assertEqual([item["run_id"] for item in report["runs"]], ["r0"])
            self.assertEqual(report["runs"][0]["status"], "unavailable_on_claude_surface")


if __name__ == "__main__":
    unittest.main()

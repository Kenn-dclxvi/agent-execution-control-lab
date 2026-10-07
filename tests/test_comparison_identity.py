import copy
import unittest

from scripts import comparison_identity as identity

TELEMETRY = {"name": "cc-plugin-telemetry", "path": "builtin", "source": "cc-plugin-telemetry@builtin"}
SEC_DEFAULT = {"name": "cc-plugin-sec-default", "path": "builtin", "source": "cc-plugin-sec-default@builtin"}


def compatibility() -> dict:
    return {
        "evaluation_set": {"set_id": "s", "revision": "r1", "identity_sha256": "a" * 64},
        "fixtures": {"CASE": {"sha256": "b" * 64}},
        "model": "claude-opus-5-5",
        "task_spec": {"CASE": "r1"},
        "permission": {"mode": "bypassPermissions"},
        "agent_environment": {
            "agent": "claude-code",
            "python_version": "3.14.5",
            "runtime_identity_sha256": "c" * 64,
            "claude_code": {
                "executable": "/a/claude",
                "executable_sha256": "d" * 64,
                "config_dir": "/a/config",
                "code_signature_team_identifier": "TEAM",
                "authentication": {"method": "claude.ai_oauth", "subscription_type": "team"},
                "plugins": [SEC_DEFAULT, TELEMETRY],
                "tools": ["Bash"],
            },
        },
        "executor_parameters": {
            "reasoning_effort": "low",
            "max_workers": 24,
            "max_attempts": 3,
            "monitor_interval_seconds": 5,
            "schedule_policy": "global_queue",
            "duration_hint_method": "history",
            "token_accounting": {"revision": "claude-v1"},
            "time_recording": {"contract": "execution-time-recording/r1", "code_sha256": {"scripts/x.py": "e" * 64}},
        },
        "repetition_condition": {"iterations": 5},
        "coverage": {"case_ids": ["CASE"], "iterations": [1, 2, 3, 4, 5]},
    }


class ComparisonIdentityTest(unittest.TestCase):
    def test_provenance_differences_keep_the_effective_key(self):
        base = compatibility()
        moved = copy.deepcopy(base)
        claude = moved["agent_environment"]["claude_code"]
        claude.update(executable="/b/claude", config_dir="/b/config", code_signature_team_identifier="OTHER")
        claude["authentication"] = {"method": "claude.ai_oauth", "subscription_type": "pro"}
        claude["plugins"] = [TELEMETRY]
        moved["agent_environment"].update(python_version="3.15.0", runtime_identity_sha256="f" * 64)
        moved["executor_parameters"].update(max_workers=8, max_attempts=1, schedule_policy="wave_barrier")
        moved["executor_parameters"]["time_recording"]["code_sha256"] = {"scripts/x.py": "0" * 64}
        self.assertEqual(identity.effective_key(base), identity.effective_key(moved))
        self.assertNotEqual(identity.split_effective(base)[1], identity.split_effective(moved)[1])

    def test_result_changing_conditions_change_the_effective_key(self):
        base = compatibility()
        for change in (
            lambda c: c["executor_parameters"].update(reasoning_effort="medium"),
            lambda c: c.update(model="claude-sonnet-5-5"),
            lambda c: c["task_spec"].update(CASE="r2"),
            lambda c: c["agent_environment"]["claude_code"].update(executable_sha256="1" * 64),
            lambda c: c["agent_environment"]["claude_code"].update(tools=["Bash", "Read"]),
            lambda c: c["executor_parameters"]["token_accounting"].update(revision="claude-v2"),
            lambda c: c["executor_parameters"]["time_recording"].update(contract="execution-time-recording/r2"),
            lambda c: c["agent_environment"]["claude_code"]["plugins"].append(
                {"name": "reviewer", "path": "/x", "source": "reviewer@market"}
            ),
            lambda c: c["coverage"].update(iterations=[1, 2]),
        ):
            changed = copy.deepcopy(base)
            change(changed)
            self.assertNotEqual(identity.effective_key(base), identity.effective_key(changed))

    def test_split_does_not_change_the_input(self):
        base = compatibility()
        snapshot = copy.deepcopy(base)
        identity.split_effective(base)
        self.assertEqual(base, snapshot)

    def test_behavior_plugins_keep_non_builtin_sources(self):
        lookalike = {"name": "cc-plugin-telemetry", "path": "/x", "source": "cc-plugin-telemetry@market"}
        self.assertEqual(identity.behavior_plugins([SEC_DEFAULT, TELEMETRY]), [])
        self.assertEqual(identity.behavior_plugins([TELEMETRY, lookalike]), [lookalike])


if __name__ == "__main__":
    unittest.main()

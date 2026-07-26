from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.run_codex_evaluation import (
    ADAPTER_TEARDOWN_PROTOCOL,
    AdapterError,
    COMMAND_EVIDENCE_PROTOCOL,
    ORDERED_ROOT_WRAPPER_PROTOCOL,
    agents_max_threads_from_conditions,
    adapter_teardown_paths_from_protocol,
    capability_catalog_external_failure,
    capability_catalog_identity,
    capability_catalog_policy_from_conditions,
    command_protocol_for_case,
    command_evidence_external_failure,
    detect_external_failure,
    evaluate_boundary_observations,
    observe_boundary_source,
    prompt_fixture_collisions,
    prompt_set_identity_from_binding,
    remove_adapter_owned_outputs,
    render_task,
    validate_boundary_evidence_compatibility,
)


class RunCodexEvaluationTest(unittest.TestCase):
    def make_git_workspace(self) -> tuple[tempfile.TemporaryDirectory[str], Path, str]:
        temporary = tempfile.TemporaryDirectory()
        workspace = Path(temporary.name)
        subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=workspace, check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.invalid"], cwd=workspace, check=True
        )
        (workspace / "tracked.txt").write_text("seed\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.txt"], cwd=workspace, check=True)
        subprocess.run(["git", "commit", "-qm", "seed"], cwd=workspace, check=True)
        seed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        (workspace / "tracked.txt").write_text("overlay\n", encoding="utf-8")
        subprocess.run(["git", "commit", "-qam", "overlay"], cwd=workspace, check=True)
        return temporary, workspace, seed

    def test_binds_disabled_capability_catalog_policy(self) -> None:
        policy = {
            "apps_enabled": False,
            "expected_sha256": "a" * 64,
            "plugin_sharing_enabled": False,
            "plugins_enabled": False,
            "schema_version": "the-caption-prompt.model-visible-capability-catalog/v1",
        }
        conditions = {"agent_environment": {"model_visible_capability_catalog": policy}}

        self.assertEqual(capability_catalog_policy_from_conditions(conditions), policy)
        self.assertIsNone(
            capability_catalog_policy_from_conditions({"agent_environment": {}})
        )
        conditions["agent_environment"]["model_visible_capability_catalog"] = {
            **policy,
            "plugins_enabled": True,
        }
        with self.assertRaisesRegex(AdapterError, "unsupported"):
            capability_catalog_policy_from_conditions(conditions)

    def test_extracts_and_hashes_only_model_visible_capability_blocks(self) -> None:
        skills = "<skills_instructions>\nseven skills\n</skills_instructions>"
        plugins = "<plugins_instructions>\nplugin note\n</plugins_instructions>"
        items = [
            {
                "type": "response_item",
                "payload": {
                    "role": "developer",
                    "content": [{"type": "input_text", "text": f"before\n{skills}\nafter"}],
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "role": "developer",
                    "content": [{"type": "input_text", "text": plugins}],
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "role": "user",
                    "content": [{"type": "input_text", "text": "ignored"}],
                },
            },
        ]
        with tempfile.TemporaryDirectory() as temporary:
            rollout = Path(temporary) / "rollout.jsonl"
            rollout.write_text(
                "".join(json.dumps(item) + "\n" for item in items), encoding="utf-8"
            )
            identity = capability_catalog_identity(rollout)

        serialized = f"{skills}\n{plugins}\n".encode()
        self.assertEqual(identity["block_tags"], ["skills_instructions", "plugins_instructions"])
        self.assertEqual(identity["block_count"], 2)
        self.assertEqual(identity["serialized_bytes"], len(serialized))
        self.assertEqual(identity["sha256"], hashlib.sha256(serialized).hexdigest())
        self.assertIsNone(
            capability_catalog_external_failure(
                identity, {"expected_sha256": identity["sha256"]}
            )
        )
        failure = capability_catalog_external_failure(
            identity, {"expected_sha256": "0" * 64}
        )
        self.assertEqual(failure["reason_code"], "model_visible_capability_catalog_mismatch")

    def test_detects_missing_parent_thread_spawn_failure(self) -> None:
        failure = detect_external_failure(
            b"ERROR codex_core::tools::router: error=collab spawn failed: no thread with id: 019f-test\n"
        )
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure["reason_code"], "codex_collab_parent_thread_missing")

    def test_binds_declared_agents_max_threads(self) -> None:
        self.assertEqual(
            agents_max_threads_from_conditions(
                {"agent_environment": {"agents_max_threads": 30}}
            ),
            30,
        )

        for invalid in (None, 0, -1, True, "30"):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(AdapterError, "must be a positive integer"):
                    agents_max_threads_from_conditions(
                        {"agent_environment": {"agents_max_threads": invalid}}
                    )

    def test_does_not_exclude_agent_or_noncritical_runtime_errors(self) -> None:
        stderr = b"\n".join(
            [
                b"ERROR codex_core::tools::router: error=timeout_ms must be at least 10000",
                b"WARN codex_analytics::client: failed to send events request",
                b"WARN codex_core::hook_runtime: no rollout found for thread id 019f-test",
                b"ERROR codex_models_manager::manager: failed to refresh available models",
            ]
        )
        self.assertIsNone(detect_external_failure(stderr))

    def test_detects_model_capacity_failure_from_codex_jsonl(self) -> None:
        stdout = b"\n".join(
            [
                b'{"type":"thread.started","thread_id":"019f-test"}',
                b'{"type":"error","message":"Selected model is at capacity. Please try a different model."}',
                b'{"type":"turn.failed","error":{"message":"Selected model is at capacity. Please try a different model."}}',
            ]
        )

        failure = detect_external_failure(b"", stdout)

        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure["reason_code"], "codex_model_at_capacity")

    def test_does_not_match_capacity_text_in_agent_message(self) -> None:
        stdout = b'{"type":"item.completed","item":{"type":"agent_message","text":"Selected model is at capacity."}}\n'

        self.assertIsNone(detect_external_failure(b"", stdout))

    def test_detects_prompt_target_collision_with_fixture_condition(self) -> None:
        case = {"fixture_condition_paths": ["tests/AGENTS.md", "src/domain/example.py"]}
        manifest = {
            "files": [
                {"target": "AGENTS.md"},
                {"target": "tests/AGENTS.md"},
            ]
        }

        self.assertEqual(prompt_fixture_collisions(case, manifest), ["tests/AGENTS.md"])

    def test_validates_immutable_prompt_set_identity_against_bundle(self) -> None:
        digest = "a" * 64
        identity = prompt_set_identity_from_binding(
            {
                "prompt_set_identity": {
                    "name": "prompt-r1",
                    "revision": "r1",
                    "bundle_sha256": digest,
                }
            },
            {"prompt_identity": "prompt-r1", "bundle_sha256": digest},
            digest,
        )
        self.assertEqual(identity["revision"], "r1")

        with self.assertRaisesRegex(AdapterError, "does not match"):
            prompt_set_identity_from_binding(
                {"prompt_set_identity": {"name": "other", "revision": "r1"}},
                {"prompt_identity": "prompt-r1", "bundle_sha256": digest},
                digest,
            )

    def test_binds_one_typed_observation_to_one_predicate(self) -> None:
        temporary, workspace, seed = self.make_git_workspace()
        self.addCleanup(temporary.cleanup)
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

        evidence = evaluate_boundary_observations(
            workspace,
            [
                {
                    "observation_id": "head-matches-overlay",
                    "operation_identity": "start-identity",
                    "source": "workspace.git.head_commit",
                    "predicate": {
                        "operator": "string_equals",
                        "expected_context": "prompt_overlay_commit",
                    },
                },
                {
                    "observation_id": "parent-matches-seed",
                    "operation_identity": "start-identity",
                    "source": "workspace.git.parent_commit",
                    "predicate": {"operator": "string_equals", "expected": seed},
                },
                {
                    "observation_id": "worktree-clean",
                    "operation_identity": "start-identity",
                    "source": "workspace.git.status_short",
                    "predicate": {"operator": "string_equals", "expected": ""},
                },
            ],
            {
                "workspace": str(workspace),
                "prompt_overlay_commit": head,
                "prompt_overlay_tree": "tree-id",
            },
        )

        assert evidence is not None
        self.assertEqual(
            [item["status"] for item in evidence["observations"]],
            ["passed", "passed", "passed"],
        )
        self.assertEqual(len(evidence["observations"]), 3)
        self.assertTrue(all("predicate" in item for item in evidence["observations"]))

    def test_boundary_observation_reports_false_predicate_as_failed(self) -> None:
        temporary, workspace, _ = self.make_git_workspace()
        self.addCleanup(temporary.cleanup)

        evidence = evaluate_boundary_observations(
            workspace,
            [
                {
                    "observation_id": "wrong-parent",
                    "operation_identity": "start-identity",
                    "source": "workspace.git.parent_commit",
                    "predicate": {"operator": "string_equals", "expected": "not-the-parent"},
                }
            ],
            {
                "workspace": str(workspace),
                "prompt_overlay_commit": "overlay-id",
                "prompt_overlay_tree": "tree-id",
            },
        )

        assert evidence is not None
        self.assertEqual(evidence["observations"][0]["status"], "failed")

    def test_boundary_source_preserves_meaningful_status_whitespace(self) -> None:
        temporary, workspace, _ = self.make_git_workspace()
        self.addCleanup(temporary.cleanup)
        (workspace / "tracked.txt").write_text("dirty\n", encoding="utf-8")

        observed = observe_boundary_source(
            ["git", "status", "--short", "--", "tracked.txt"], workspace
        )

        self.assertEqual(observed, " M tracked.txt")

    def test_boundary_observation_reports_unavailable_source_without_aborting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            evidence = evaluate_boundary_observations(
                workspace,
                [
                    {
                        "observation_id": "missing-git-head",
                        "operation_identity": "start-identity",
                        "source": "workspace.git.head_commit",
                        "predicate": {"operator": "string_equals", "expected": "head"},
                    }
                ],
                {
                    "workspace": str(workspace),
                    "prompt_overlay_commit": "overlay-id",
                    "prompt_overlay_tree": "tree-id",
                },
            )

        assert evidence is not None
        self.assertEqual(evidence["observations"][0]["status"], "unavailable")

    def test_boundary_observation_rejects_unknown_source_and_duplicate_id(self) -> None:
        context = {
            "workspace": "/tmp/workspace",
            "prompt_overlay_commit": "overlay-id",
            "prompt_overlay_tree": "tree-id",
        }
        observation = {
            "observation_id": "identity",
            "operation_identity": "start-identity",
            "source": "workspace.git.unknown",
            "predicate": {"operator": "string_equals", "expected": "value"},
        }
        with self.assertRaisesRegex(AdapterError, "unsupported boundary observation source"):
            evaluate_boundary_observations(Path("/tmp"), [observation], context)

        observation["source"] = "workspace.path"
        with self.assertRaisesRegex(AdapterError, "duplicate boundary observation id"):
            evaluate_boundary_observations(Path("/tmp"), [observation, observation], context)

    def test_render_task_exposes_typed_evidence_without_changing_taskspec(self) -> None:
        case = {"payload": {"trial_prompt_input": {"task_id": "TC-F10"}}}
        evidence = {
            "schema_version": "the-caption-prompt.boundary-evidence/v1",
            "binding_revision": "one-observation-one-predicate/v1",
            "provenance": {},
            "observations": [{"observation_id": "parent", "status": "passed"}],
        }

        task = render_task(case, evidence)

        self.assertIn('<task-spec-json>\n{\n  "task_id": "TC-F10"', task)
        self.assertIn("<adapter-boundary-evidence-json>", task)
        self.assertIn("raw出力を再取得・再解釈しない", task)

    def test_render_task_adds_bound_command_evidence_protocol(self) -> None:
        case = {"payload": {"trial_prompt_input": {"task_id": "TC-F07"}}}

        task = render_task(
            case,
            command_evidence_protocol={
                **COMMAND_EVIDENCE_PROTOCOL,
                "required_command_groups": [["bash", "-n", "run.sh"]],
            },
        )

        self.assertIn("1 commandずつ個別のexec_command", task)
        self.assertIn('"exit_code":返却された整数', task)
        self.assertIn("<command-evidence-protocol-json>", task)

        with self.assertRaisesRegex(AdapterError, "unsupported command evidence protocol"):
            render_task(case, command_evidence_protocol={"schema_version": "other"})

    def test_render_task_adds_ordered_root_wrapper_protocol(self) -> None:
        case = {"payload": {"trial_prompt_input": {"task_id": "TC-F04"}}}

        task = render_task(
            case,
            command_evidence_protocol={
                **ORDERED_ROOT_WRAPPER_PROTOCOL,
                "required_command_groups": [
                    ["npm", "ci"],
                    ["npm", "run", "lint"],
                    ["npm", "run", "build"],
                ],
            },
        )

        self.assertIn("1回のcustom exec wrapper内", task)
        self.assertIn("tools.exec_commandへ1 commandずつ個別invocation", task)
        self.assertIn("nonzeroまたはunavailableなら後続commandを発行せず", task)
        self.assertIn("全resultを一度だけmodelへ返", task)
        self.assertIn("compound command、`&&`、`;`で結合しない", task)
        self.assertIn('"schema_version": "the-caption-prompt.command-evidence-protocol/v2"', task)

    def test_selects_ordered_root_wrapper_protocol_for_current_case(self) -> None:
        declaration = {
            **ORDERED_ROOT_WRAPPER_PROTOCOL,
            "required_command_groups_by_case": {
                "TC-F04": [["npm", "ci"], ["npm", "run", "lint"]],
            },
        }

        task_protocol, groups = command_protocol_for_case(declaration, "TC-F04")

        self.assertEqual(groups, [["npm", "ci"], ["npm", "run", "lint"]])
        assert task_protocol is not None
        self.assertEqual(task_protocol, {**ORDERED_ROOT_WRAPPER_PROTOCOL, "required_command_groups": groups})

    def test_selects_required_command_groups_for_current_case(self) -> None:
        declaration = {
            **COMMAND_EVIDENCE_PROTOCOL,
            "required_command_groups_by_case": {
                "TC-F07": [["bash", "-n", "run.sh"]],
                "TC-F04": [["npm", "run", "build"]],
            },
        }

        task_protocol, groups = command_protocol_for_case(declaration, "TC-F07")

        self.assertEqual(groups, [["bash", "-n", "run.sh"]])
        assert task_protocol is not None
        self.assertEqual(task_protocol["required_command_groups"], groups)
        self.assertNotIn("required_command_groups_by_case", task_protocol)

    def test_omits_command_protocol_from_declared_cases(self) -> None:
        declaration = {
            **COMMAND_EVIDENCE_PROTOCOL,
            "omit_for_cases": ["TC-A01", "TC-A02"],
            "required_command_groups_by_case": {
                "TC-F07": [["bash", "-n", "run.sh"]],
            },
        }

        task_protocol, groups = command_protocol_for_case(declaration, "TC-A01")

        self.assertIsNone(task_protocol)
        self.assertEqual(groups, [])

    def test_rejects_duplicate_command_protocol_omissions(self) -> None:
        declaration = {
            **COMMAND_EVIDENCE_PROTOCOL,
            "omit_for_cases": ["TC-A01", "TC-A01"],
            "required_command_groups_by_case": {},
        }

        with self.assertRaisesRegex(AdapterError, "must not contain duplicates"):
            command_protocol_for_case(declaration, "TC-A01")

    def test_only_incomplete_command_evidence_is_an_external_failure(self) -> None:
        self.assertIsNone(
            command_evidence_external_failure(
                [{"status": "not_attempted"}, {"status": "failed"}]
            )
        )
        failure = command_evidence_external_failure(
            [{"status": "evidence_incomplete"}]
        )
        assert failure is not None
        self.assertEqual(failure["reason_code"], "command_evidence_incomplete")

    def test_removes_only_declared_adapter_owned_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            owned_directory = workspace / "src" / "ui" / "node_modules"
            owned_directory.mkdir(parents=True)
            (owned_directory / "package.json").write_text("{}\n", encoding="utf-8")
            owned_file = workspace / "src" / "ui" / "build.log"
            owned_file.write_text("generated\n", encoding="utf-8")
            preserved = workspace / "src" / "ui" / "source.ts"
            preserved.write_text("source\n", encoding="utf-8")

            removed = remove_adapter_owned_outputs(
                workspace,
                ["src/ui/node_modules", "src/ui/build.log", "src/ui/missing"],
            )

            self.assertEqual(removed, ["src/ui/node_modules", "src/ui/build.log"])
            self.assertFalse(owned_directory.exists())
            self.assertFalse(owned_file.exists())
            self.assertTrue(preserved.exists())

    def test_rejects_unsafe_adapter_teardown_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            for unsafe in (".", "../outside", "/tmp/outside"):
                with self.subTest(unsafe=unsafe):
                    with self.assertRaisesRegex(AdapterError, "unsafe adapter teardown path"):
                        remove_adapter_owned_outputs(workspace, [unsafe])

    def test_rejects_adapter_teardown_through_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            workspace = Path(temporary)
            (workspace / "linked").symlink_to(Path(outside), target_is_directory=True)

            with self.assertRaisesRegex(AdapterError, "traverses symlink"):
                remove_adapter_owned_outputs(workspace, ["linked/generated"])

    def test_binds_adapter_teardown_paths_from_comparison_condition(self) -> None:
        declaration = {
            **ADAPTER_TEARDOWN_PROTOCOL,
            "paths_by_case": {
                "TC-F04": ["src/ui/node_modules", "src/ui/dist"],
            },
        }

        self.assertEqual(
            adapter_teardown_paths_from_protocol(
                {"case_id": "TC-F04"},
                {},
                {"adapter_owned_teardown": declaration},
            ),
            ["src/ui/node_modules", "src/ui/dist"],
        )
        with self.assertRaisesRegex(AdapterError, "do not match"):
            adapter_teardown_paths_from_protocol(
                {"case_id": "TC-F04"},
                {"adapter_teardown_paths": ["other"]},
                {"adapter_owned_teardown": declaration},
            )

    def test_uses_empty_teardown_paths_when_protocol_is_absent(self) -> None:
        self.assertEqual(
            adapter_teardown_paths_from_protocol(
                {"case_id": "TC-F05"},
                {},
                {},
            ),
            [],
        )

    def test_boundary_evidence_requires_explicit_compatibility_revision(self) -> None:
        declaration = {
            "binding_revision": "one-observation-one-predicate/v1",
            "schema_version": "the-caption-prompt.boundary-evidence/v1",
            "source_policy": "adapter_managed_read_only_registry",
        }
        capsule = {
            "comparison_conditions": {
                "agent_environment": {
                    "adapter_schema_version": "the-caption-prompt.codex-adapter/v4"
                },
                "executor_parameters": {"boundary_evidence": declaration},
            }
        }

        validate_boundary_evidence_compatibility(capsule, [{}])
        with self.assertRaisesRegex(AdapterError, "without boundary observations"):
            validate_boundary_evidence_compatibility(capsule, None)
        capsule["comparison_conditions"]["executor_parameters"].pop("boundary_evidence")
        with self.assertRaisesRegex(AdapterError, "do not bind"):
            validate_boundary_evidence_compatibility(capsule, [{}])


if __name__ == "__main__":
    unittest.main()

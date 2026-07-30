from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.all_agent_usage import TOKEN_ACCOUNTING
from scripts.evaluation_loop import (
    LEGACY_QUALITY_RATING,
    QUALITY_RATING_V8,
    QUALITY_RATING_V2,
    QUALITY_RATING_V10,
    QUALITY_RATING_V11,
    QUALITY_RATING_V12,
    QUALITY_RATING_V13,
    QUALITY_RATING_V14,
    identity_sha256,
    kpi_difference,
    validate_comparison_conditions,
    validate_run_capsule,
)


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "evaluation_loop.py"


class EvaluationLoopTest(unittest.TestCase):
    def test_boundary_quality_rating_v10_is_supported(self) -> None:
        conditions = self.conditions(1)
        conditions["quality_rating"] = QUALITY_RATING_V10
        self.assertEqual(
            validate_comparison_conditions(conditions)["quality_rating"],
            QUALITY_RATING_V10,
        )

    def test_semantic_location_quality_rating_v11_is_supported(self) -> None:
        conditions = self.conditions(1)
        conditions["quality_rating"] = QUALITY_RATING_V11
        self.assertEqual(
            validate_comparison_conditions(conditions)["quality_rating"],
            QUALITY_RATING_V11,
        )

    def test_semantic_evidence_normalized_quality_rating_v12_is_supported(self) -> None:
        conditions = self.conditions(1)
        conditions["quality_rating"] = QUALITY_RATING_V12
        self.assertEqual(
            validate_comparison_conditions(conditions)["quality_rating"],
            QUALITY_RATING_V12,
        )

    def test_abstract_condition_preserving_quality_rating_v13_is_supported(self) -> None:
        conditions = self.conditions(1)
        conditions["quality_rating"] = QUALITY_RATING_V13
        self.assertEqual(
            validate_comparison_conditions(conditions)["quality_rating"],
            QUALITY_RATING_V13,
        )

    def test_quality_rating_v13_keeps_owner_producer_evidence_diagnostic(self) -> None:
        self.assertEqual(
            QUALITY_RATING_V13["owner_producer_evidence_policy"],
            "diagnostic_only",
        )

    def test_terminal_state_quality_rating_v14_is_supported(self) -> None:
        conditions = self.conditions(1)
        conditions["quality_rating"] = QUALITY_RATING_V14
        self.assertEqual(
            validate_comparison_conditions(conditions)["quality_rating"],
            QUALITY_RATING_V14,
        )
        self.assertEqual(
            QUALITY_RATING_V14["terminal_state_evidence_schema_version"],
            "the-caption-prompt.terminal-state-evidence/v1",
        )
        self.assertEqual(
            QUALITY_RATING_V14["terminal_state_evidence_required_cases"],
            ["TC-A01-LATENT-MODE-POLICY"],
        )

    def test_kpi_difference_names_no_winner(self) -> None:
        self.assertEqual(
            kpi_difference(
                {"quality_score": 75, "total_tokens": 200, "elapsed_seconds": 20},
                {"quality_score": 50, "total_tokens": 100, "elapsed_seconds": 10},
            ),
            {"quality_score": 25, "total_tokens": 100, "elapsed_seconds": 10},
        )

    def test_atomic_capsule_has_sample_identity_without_repetition_count(self) -> None:
        conditions = self.conditions(5)
        conditions.pop("repetition_condition")
        binding, validated, argv = validate_run_capsule(
            {
                "schema_version": "the-caption-prompt.execution-capsule/v3",
                "binding": {
                    "prompt_set_identity": {"name": "prompt", "revision": "r1"},
                    "case_id": "TEST-CASE",
                    "iteration": 95,
                    "sample_id": "planned:sample-95",
                },
                "comparison_conditions": conditions,
                "adapter": {"argv": ["true"]},
            }
        )
        self.assertEqual(binding["sample_id"], "planned:sample-95")
        self.assertNotIn("repetition_condition", validated)
        self.assertEqual(argv, ["true"])

    def cli(self, *args: str) -> dict:
        completed = subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    def cli_failure(self, *args: str) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 2)
        return completed

    def make_set(self, root: Path) -> Path:
        fixture = root / "fixture"
        fixture.mkdir(parents=True)
        (fixture / "input.txt").write_text("input\n", encoding="utf-8")
        (fixture / "input-link.txt").symlink_to("input.txt")
        manifest = root / "set.json"
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": "the-caption-prompt.evaluation-set-source/v2",
                    "set_id": "test-set",
                    "revision": "r1",
                    "cases": [
                        {
                            "id": "TEST-CASE",
                            "fixture": "fixture",
                            "payload": {"task": "test task", "future_parameter": "opaque"},
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return manifest

    def make_two_case_set(self, root: Path) -> Path:
        manifest = self.make_set(root)
        second_fixture = root / "fixture-2"
        second_fixture.mkdir()
        (second_fixture / "input.txt").write_text("second\n", encoding="utf-8")
        document = json.loads(manifest.read_text(encoding="utf-8"))
        document["cases"].append(
            {
                "id": "TEST-CASE-2",
                "fixture": "fixture-2",
                "payload": {"task": "second task", "future_parameter": "opaque"},
            }
        )
        manifest.write_text(json.dumps(document), encoding="utf-8")
        return manifest

    def conditions(self, iterations: int, model: str = "test-model") -> dict:
        return {
            "target_repository_ref": "example/repo@abc123",
            "model": model,
            "agent_environment": {"agent": "codex", "version": "test"},
            "task_spec": {"TEST-CASE": "task-spec-r1"},
            "permission": "workspace-write/never",
            "executor_parameters": {
                "reasoning_effort": "high",
                "max_workers": 24,
                "token_accounting": TOKEN_ACCOUNTING,
            },
            "quality_rating": QUALITY_RATING_V8,
            "repetition_condition": {"iterations": iterations, "order": "case-major"},
        }

    def write_command_evidence(self, cycle: Path, run_id: str) -> None:
        artifact = (
            cycle
            / "layer2"
            / "extensions"
            / run_id
            / "all-agent-command-evidence"
            / "evidence.json"
        )
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(
            json.dumps(
                {
                    "schema_version": QUALITY_RATING_V8[
                        "command_evidence_schema_version"
                    ],
                    "run_id": run_id,
                    "attempted_commands": [],
                    "successful_commands": [],
                    "failed_commands": [],
                    "protocol_violations": [],
                }
            ),
            encoding="utf-8",
        )

    def test_explicit_quality_rating_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            conditions = self.conditions(1)
            conditions.pop("quality_rating")
            capsule = root / "missing-quality-rating.json"
            capsule.write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.execution-capsule/v2",
                        "binding": {
                            "prompt_set_identity": {"name": "prompt", "revision": "r1"},
                            "case_id": "TEST-CASE",
                            "iteration": 1,
                        },
                        "comparison_conditions": conditions,
                        "adapter": {"argv": [sys.executable, "-c", "pass"]},
                    }
                ),
                encoding="utf-8",
            )
            completed = self.cli_failure(
                "run", "--cycle", str(cycle), "--capsule", str(capsule)
            )
            self.assertIn("comparison_conditions.quality_rating is required", completed.stderr)

    def test_legacy_quality_rating_remains_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            conditions = self.conditions(1)
            conditions["quality_rating"] = LEGACY_QUALITY_RATING
            capsule = root / "legacy-quality-rating.json"
            capsule.write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.execution-capsule/v2",
                        "binding": {
                            "prompt_set_identity": {"name": "prompt", "revision": "r1"},
                            "case_id": "TEST-CASE",
                            "iteration": 1,
                        },
                        "comparison_conditions": conditions,
                        "adapter": {"argv": [sys.executable, "-c", "pass"]},
                    }
                ),
                encoding="utf-8",
            )
            completed = self.cli_failure(
                "run", "--cycle", str(cycle), "--capsule", str(capsule)
            )
            self.assertNotIn("unsupported contract revision", completed.stderr)

    def test_quality_rating_v2_remains_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            conditions = self.conditions(1)
            conditions["quality_rating"] = QUALITY_RATING_V2
            capsule = root / "quality-rating-v2.json"
            capsule.write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.execution-capsule/v2",
                        "binding": {
                            "prompt_set_identity": {"name": "prompt", "revision": "r1"},
                            "case_id": "TEST-CASE",
                            "iteration": 1,
                        },
                        "comparison_conditions": conditions,
                        "adapter": {"argv": [sys.executable, "-c", "pass"]},
                    }
                ),
                encoding="utf-8",
            )
            completed = self.cli_failure(
                "run", "--cycle", str(cycle), "--capsule", str(capsule)
            )
            self.assertNotIn("unsupported contract revision", completed.stderr)

    def test_nonzero_adapter_exit_without_exclusion_is_not_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            capsule = root / "nonzero-exit.json"
            capsule.write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.execution-capsule/v2",
                        "binding": {
                            "prompt_set_identity": {"name": "prompt", "revision": "r1"},
                            "case_id": "TEST-CASE",
                            "iteration": 1,
                        },
                        "comparison_conditions": self.conditions(1),
                        "adapter": {"argv": [sys.executable, "-c", "raise SystemExit(2)"]},
                    }
                ),
                encoding="utf-8",
            )
            completed = self.cli_failure(
                "run", "--cycle", str(cycle), "--capsule", str(capsule)
            )
            self.assertIn("adapter exited without an external-failure exclusion: 2", completed.stderr)
            self.assertEqual(list((cycle / "layer2" / "bindings").glob("*.json")), [])

    def test_missing_usage_is_not_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            capsule = root / "missing-usage.json"
            capsule.write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.execution-capsule/v2",
                        "binding": {
                            "prompt_set_identity": {"name": "prompt", "revision": "r1"},
                            "case_id": "TEST-CASE",
                            "iteration": 1,
                        },
                        "comparison_conditions": self.conditions(1),
                        "adapter": {"argv": [sys.executable, "-c", "pass"]},
                    }
                ),
                encoding="utf-8",
            )
            completed = self.cli_failure(
                "run", "--cycle", str(cycle), "--capsule", str(capsule)
            )
            self.assertIn("valid run requires all-agent token usage", completed.stderr)
            self.assertEqual(list((cycle / "layer2" / "bindings").glob("*.json")), [])

    def execute(
        self,
        cycle: Path,
        identity: dict,
        iteration: int,
        tokens: int,
        conditions: dict,
        case_id: str = "TEST-CASE",
        sample_id: str | None = None,
    ) -> str:
        command = (
            "import json,os,pathlib; "
            "case=json.loads(pathlib.Path(os.environ['EVAL_CASE_FILE']).read_text()); "
            "capsule=json.loads(pathlib.Path(os.environ['EVAL_RUN_CAPSULE_FILE']).read_text()); "
            "assert case['payload']['future_parameter']=='opaque'; "
            "assert capsule['parameters']['future_parameter']==42; "
            "pathlib.Path('result.txt').write_text('result\\n', encoding='utf-8'); "
            "extension=pathlib.Path(os.environ['EVAL_EXTENSION_DIR'])/'token-analysis'; "
            "extension.mkdir(); "
            "(extension/'provider-usage.json').write_text(json.dumps({'future_detail': 42})); "
            f"pathlib.Path(os.environ['EVAL_USAGE_FILE']).write_text(json.dumps({{"
            "'schema_version':'the-caption-prompt.token-usage/v2',"
            f"'token_accounting':{TOKEN_ACCOUNTING!r},'total_tokens':{tokens}}}))"
        )
        capsule = cycle.parent / f"{cycle.name}-{identity['name']}-{case_id}-{iteration}.json"
        binding = {
            "prompt_set_identity": identity,
            "case_id": case_id,
            "iteration": iteration,
        }
        if sample_id is not None:
            binding["sample_id"] = sample_id
        capsule.write_text(
            json.dumps(
                {
                    "schema_version": "the-caption-prompt.execution-capsule/v2",
                    "binding": binding,
                    "comparison_conditions": conditions,
                    "adapter": {"argv": [sys.executable, "-c", command]},
                    "parameters": {"future_parameter": 42},
                }
            ),
            encoding="utf-8",
        )
        result = self.cli("run", "--cycle", str(cycle), "--capsule", str(capsule))
        return result["run_id"]

    def test_run_binding_preserves_optional_atomic_sample_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            run_id = self.execute(
                cycle,
                {"name": "prompt", "revision": "r1"},
                1,
                100,
                self.conditions(1),
                sample_id="planned:test:sample-1",
            )
            binding = json.loads(
                (cycle / "layer2" / "bindings" / f"{run_id}.json").read_text()
            )
            self.assertEqual(binding["sample_id"], "planned:test:sample-1")

    def record_prompt_set(
        self,
        manifest: Path,
        root: Path,
        registry: Path,
        name: str,
        score: int,
        tokens: int,
        model: str = "test-model",
    ) -> dict:
        cycle = root / f"cycle-{name}-{model}"
        frozen = self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
        self.assertEqual(frozen["revision"], "r1")
        identity = {"name": name, "revision": "r1"}
        conditions = self.conditions(2, model)
        run_ids = [
            self.execute(cycle, identity, iteration, tokens, conditions)
            for iteration in (1, 2)
        ]
        for run_id in run_ids:
            evidence = cycle / "layer2" / "evidence" / run_id
            self.assertTrue((evidence / "workspace" / "input-link.txt").is_symlink())
            execution = json.loads((evidence / "execution.json").read_text())
            self.assertNotIn("prompt_set_identity", execution)
            self.assertNotIn("condition", execution)
            self.assertEqual(
                json.loads((evidence / "usage.json").read_text()),
                {
                    "schema_version": "the-caption-prompt.token-usage/v2",
                    "token_accounting": TOKEN_ACCOUNTING,
                    "total_tokens": tokens,
                },
            )
            self.assertTrue(
                (cycle / "layer2" / "extensions" / run_id / "token-analysis" / "provider-usage.json").exists()
            )
            binding = json.loads(
                (cycle / "layer2" / "bindings" / f"{run_id}.json").read_text()
            )
            self.assertEqual(binding["prompt_set_identity"], identity)
            self.assertNotIn("condition", binding)
            self.write_command_evidence(cycle, run_id)
            self.cli(
                "rate",
                "--cycle",
                str(cycle),
                "--run-id",
                run_id,
                "--score",
                str(score),
                "--reason",
                "test rating",
            )
        return self.cli(
            "record-result", "--cycle", str(cycle), "--registry", str(registry)
        )

    def test_bound_subset_is_enforced_and_registered_without_changing_the_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            registry = root / "registry"
            manifest = self.make_two_case_set(root)
            frozen = self.cli(
                "freeze-set", "--set", str(manifest), "--cycle", str(cycle)
            )
            coverage = self.cli(
                "bind-coverage",
                "--cycle",
                str(cycle),
                "--case-id",
                "TEST-CASE",
                "--iterations",
                "2",
            )
            self.assertEqual(coverage["case_ids"], ["TEST-CASE"])
            self.assertEqual(coverage["iterations"], [1, 2])
            self.assertEqual(
                coverage["evaluation_set_identity_sha256"], frozen["identity_sha256"]
            )

            identity = {"name": "subset-prompt", "revision": "r1"}
            conditions = self.conditions(2)
            for iteration in (1, 2):
                run_id = self.execute(
                    cycle, identity, iteration, 100 + iteration, conditions
                )
                self.write_command_evidence(cycle, run_id)
                self.cli(
                    "rate",
                    "--cycle",
                    str(cycle),
                    "--run-id",
                    run_id,
                    "--score",
                    "4",
                    "--reason",
                    "subset rating",
                )

            outside_capsule = root / "outside.json"
            outside_capsule.write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.execution-capsule/v2",
                        "binding": {
                            "prompt_set_identity": identity,
                            "case_id": "TEST-CASE-2",
                            "iteration": 1,
                        },
                        "comparison_conditions": conditions,
                        "adapter": {"argv": [sys.executable, "-c", "pass"]},
                    }
                ),
                encoding="utf-8",
            )
            rejected = self.cli_failure(
                "run", "--cycle", str(cycle), "--capsule", str(outside_capsule)
            )
            self.assertIn("outside the bound evaluation coverage", rejected.stderr)

            receipt = self.cli(
                "record-result", "--cycle", str(cycle), "--registry", str(registry)
            )
            result = json.loads(Path(receipt["artifact"]).read_text(encoding="utf-8"))
            self.assertEqual(
                result["compatibility"]["coverage"],
                {"case_ids": ["TEST-CASE"], "iterations": [1, 2]},
            )
            self.assertEqual(
                result["compatibility"]["evaluation_set"]["identity_sha256"],
                frozen["identity_sha256"],
            )
            self.assertEqual(
                {item["case_id"] for item in result["case_results"]}, {"TEST-CASE"}
            )

    def test_three_prompt_sets_are_stored_independently_and_compared_as_a_view(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            manifest = self.make_set(root)
            baseline = self.record_prompt_set(manifest, root, registry, "baseline", 2, 120)
            candidate1 = self.record_prompt_set(manifest, root, registry, "candidate1", 3, 110)
            candidate2 = self.record_prompt_set(manifest, root, registry, "candidate2", 4, 100)

            query = self.cli("query-results", "--registry", str(registry))
            self.assertEqual(query["count"], 3)
            self.assertEqual(
                {item["prompt_set_identity"]["name"] for item in query["results"]},
                {"baseline", "candidate1", "candidate2"},
            )
            self.assertEqual(
                {item["compatibility_key"] for item in query["results"]},
                {baseline["compatibility_key"]},
            )
            baseline_result = json.loads(Path(baseline["artifact"]).read_text())
            self.assertEqual(
                baseline_result["schema_version"],
                "the-caption-prompt.prompt-set-result/v2",
            )
            self.assertEqual(baseline_result["token_accounting"], TOKEN_ACCOUNTING)
            self.assertEqual(len(baseline_result["result_content_sha256"]), 64)
            self.assertEqual(
                baseline_result["compatibility"]["evaluation_set"]["revision"], "r1"
            )
            self.assertIn("TEST-CASE", baseline_result["compatibility"]["fixtures"])
            for key in (
                "target_repository_ref",
                "model",
                "agent_environment",
                "task_spec",
                "permission",
                "executor_parameters",
                "repetition_condition",
            ):
                self.assertIn(key, baseline_result["compatibility"])
            self.assertEqual(
                [(item["case_id"], item["iteration"]) for item in baseline_result["case_results"]],
                [("TEST-CASE", 1), ("TEST-CASE", 2)],
            )

            result_paths = sorted((registry / "results").glob("*.json"))
            before = {path: path.read_bytes() for path in result_paths}
            view_path = root / "three-prompt-view.json"
            self.cli(
                "compare",
                "--registry",
                str(registry),
                "--result-id",
                baseline["result_id"],
                "--result-id",
                candidate1["result_id"],
                "--result-id",
                candidate2["result_id"],
                "--reference-result-id",
                baseline["result_id"],
                "--output",
                str(view_path),
            )
            view = json.loads(view_path.read_text())
            self.assertEqual(
                view["schema_version"], "the-caption-prompt.prompt-set-comparison-view/v2"
            )
            self.assertEqual(view["token_accounting"], TOKEN_ACCOUNTING)
            self.assertEqual(len(view["prompt_sets"]), 3)
            self.assertEqual(len(view["differences"]), 2)
            candidate2_difference = next(
                item
                for item in view["differences"]
                if item["minuend_result_id"] == candidate2["result_id"]
            )
            self.assertEqual(candidate2_difference["subtrahend_result_id"], baseline["result_id"])
            self.assertEqual(candidate2_difference["kpis"]["quality_score"], 50.0)
            self.assertEqual(candidate2_difference["kpis"]["total_tokens"], -20.0)
            self.assertNotIn("winner", view)
            self.assertEqual(before, {path: path.read_bytes() for path in result_paths})
            repeated_view = self.cli_failure(
                "compare",
                "--registry",
                str(registry),
                "--result-id",
                baseline["result_id"],
                "--result-id",
                candidate1["result_id"],
                "--reference-result-id",
                baseline["result_id"],
                "--output",
                str(view_path),
            )
            self.assertIn("refusing to overwrite", repeated_view.stderr)

    def test_layer_outputs_and_registered_result_are_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            manifest = self.make_set(root)
            recorded = self.record_prompt_set(manifest, root, registry, "prompt", 3, 100)
            cycle = root / "cycle-prompt-test-model"
            repeated = self.cli_failure(
                "record-result", "--cycle", str(cycle), "--registry", str(registry)
            )
            self.assertIn("already registered", repeated.stderr)
            view = root / "view.json"
            view.write_text("{}\n", encoding="utf-8")
            compare = self.cli_failure(
                "compare",
                "--registry",
                str(registry),
                "--result-id",
                recorded["result_id"],
                "--result-id",
                recorded["result_id"],
                "--reference-result-id",
                recorded["result_id"],
                "--output",
                str(view),
            )
            self.assertIn("must be unique", compare.stderr)

    def test_root_only_result_is_reaccounted_append_only_as_all_agent_v2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            manifest = self.make_set(root)
            recorded = self.record_prompt_set(manifest, root, registry, "prompt", 4, 100)
            current = json.loads(Path(recorded["artifact"]).read_text())

            source = json.loads(json.dumps(current))
            source_id = "rootonlyresult00000000000000000001"
            source["schema_version"] = "the-caption-prompt.prompt-set-result/v1"
            source["result_id"] = source_id
            source.pop("token_accounting")
            source["compatibility"]["executor_parameters"].pop("token_accounting")
            source["compatibility_key"] = identity_sha256(source["compatibility"])
            source.pop("result_content_sha256")
            source["result_content_sha256"] = identity_sha256(source)
            source_path = registry / "results" / f"{source_id}.json"
            source_path.write_text(json.dumps(source), encoding="utf-8")
            source_before = source_path.read_bytes()

            usage_root = root / "reaccounting"
            for item in source["case_results"]:
                usage_path = (
                    usage_root
                    / "layer2"
                    / "extensions"
                    / item["run_id"]
                    / "all-agent-usage"
                    / "usage.json"
                )
                usage_path.parent.mkdir(parents=True)
                usage_path.write_text(
                    json.dumps(
                        {
                            "schema_version": "the-caption-prompt.all-agent-usage/v1",
                            "token_accounting": TOKEN_ACCOUNTING,
                            "root_total_tokens": item["total_tokens"],
                            "all_agent_total_tokens": item["total_tokens"] + 50,
                        }
                    ),
                    encoding="utf-8",
                )

            receipt_root = usage_root / "layer4"
            reaccounted = self.cli(
                "reaccount-result",
                "--registry",
                str(registry),
                "--source-result-id",
                source_id,
                "--usage-root",
                str(usage_root),
                "--receipt-root",
                str(receipt_root),
            )
            result = json.loads(Path(reaccounted["artifact"]).read_text())

            self.assertEqual(result["schema_version"], "the-caption-prompt.prompt-set-result/v2")
            self.assertEqual(result["source_result_id"], source_id)
            self.assertEqual(result["token_accounting"], TOKEN_ACCOUNTING)
            self.assertEqual(result["median"]["total_tokens"], 150)
            self.assertEqual(
                result["compatibility"]["executor_parameters"]["token_accounting"],
                TOKEN_ACCOUNTING,
            )
            self.assertEqual(source_path.read_bytes(), source_before)
            self.assertTrue(
                (receipt_root / "result-registrations" / f"{source_id}.json").is_file()
            )

            mixed = self.cli_failure(
                "compare",
                "--registry",
                str(registry),
                "--result-id",
                source_id,
                "--result-id",
                result["result_id"],
                "--reference-result-id",
                source_id,
                "--output",
                str(root / "mixed.json"),
            )
            self.assertIn("schema versions do not match", mixed.stderr)

    def test_incompatible_conditions_are_not_mixed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            manifest = self.make_set(root)
            first = self.record_prompt_set(manifest, root, registry, "prompt-1", 3, 100)
            second = self.record_prompt_set(
                manifest, root, registry, "prompt-2", 3, 100, model="other-model"
            )
            completed = self.cli_failure(
                "compare",
                "--registry",
                str(registry),
                "--result-id",
                first["result_id"],
                "--result-id",
                second["result_id"],
                "--reference-result-id",
                first["result_id"],
                "--output",
                str(root / "invalid-view.json"),
            )
            self.assertIn("compatibility keys do not match", completed.stderr)
            self.assertFalse((root / "invalid-view.json").exists())

    def test_excluded_external_failure_is_preserved_and_slot_can_be_retried(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            registry = root / "registry"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            identity = {"name": "prompt", "revision": "r1"}
            conditions = self.conditions(1)
            excluded_command = (
                "import json,os,pathlib,sys; "
                "pathlib.Path(os.environ['EVAL_RUN_STATUS_FILE']).write_text(json.dumps({"
                "'schema_version':'the-caption-prompt.run-status/v1',"
                "'status':'excluded','category':'external_failure',"
                "'reason_code':'codex_collab_parent_thread_missing'})); "
                "sys.exit(75)"
            )
            capsule = root / "excluded.json"
            capsule.write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.execution-capsule/v2",
                        "binding": {
                            "prompt_set_identity": identity,
                            "case_id": "TEST-CASE",
                            "iteration": 1,
                        },
                        "comparison_conditions": conditions,
                        "adapter": {"argv": [sys.executable, "-c", excluded_command]},
                    }
                ),
                encoding="utf-8",
            )
            excluded = self.cli("run", "--cycle", str(cycle), "--capsule", str(capsule))
            self.assertEqual(excluded["status"], "excluded")
            rate = self.cli_failure(
                "rate",
                "--cycle",
                str(cycle),
                "--run-id",
                excluded["run_id"],
                "--score",
                "4",
                "--reason",
                "must not be accepted",
            )
            self.assertIn("excluded run cannot be quality-rated", rate.stderr)

            valid = self.execute(cycle, identity, 1, 120, conditions)
            self.write_command_evidence(cycle, valid)
            self.cli(
                "rate",
                "--cycle",
                str(cycle),
                "--run-id",
                valid,
                "--score",
                "4",
                "--reason",
                "valid",
            )
            recorded = self.cli(
                "record-result", "--cycle", str(cycle), "--registry", str(registry)
            )
            result = json.loads(
                (registry / "results" / f"{recorded['result_id']}.json").read_text()
            )
            self.assertEqual(len(result["excluded_attempts"]), 1)
            self.assertEqual(
                result["excluded_attempts"][0]["reason_code"],
                "codex_collab_parent_thread_missing",
            )
            self.assertEqual(len(list((cycle / "layer2" / "bindings").glob("*.json"))), 2)

    def test_prompt_set_identity_requires_revision_or_bundle_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            capsule = root / "invalid-identity.json"
            capsule.write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.execution-capsule/v2",
                        "binding": {
                            "prompt_set_identity": {"name": "mutable-name-only"},
                            "case_id": "TEST-CASE",
                            "iteration": 1,
                        },
                        "comparison_conditions": self.conditions(1),
                        "adapter": {"argv": [sys.executable, "-c", "pass"]},
                    }
                ),
                encoding="utf-8",
            )
            completed = self.cli_failure(
                "run", "--cycle", str(cycle), "--capsule", str(capsule)
            )
            self.assertIn("needs revision or bundle_sha256", completed.stderr)

    def write_comparison_plan(
        self,
        root: Path,
        cycle: Path,
        conditions: dict,
    ) -> tuple[Path, Path, list[Path]]:
        prompt_identity = {"name": "candidate", "revision": "r1"}
        profile = root / "candidate-profile.json"
        profile.write_text(
            json.dumps(
                {
                    "profile_id": "candidate-profile",
                    "prompt_set_identity": prompt_identity,
                    "evaluation_set": {"set_id": "test-set", "revision": "r1"},
                    "cases": [{"id": "TEST-CASE", "revision": "r1"}],
                    "iterations": 2,
                    "execution": {"max_workers": 24},
                    "comparison_conditions": conditions,
                }
            ),
            encoding="utf-8",
        )
        capsules: list[Path] = []
        jobs: list[dict] = []
        adapter_command = (
            "import json,os,pathlib; "
            "pathlib.Path('result.txt').write_text('result\\n', encoding='utf-8'); "
            f"pathlib.Path(os.environ['EVAL_USAGE_FILE']).write_text(json.dumps({{"
            "'schema_version':'the-caption-prompt.token-usage/v2',"
            f"'token_accounting':{TOKEN_ACCOUNTING!r},'total_tokens':100}}))"
        )
        for iteration in (1, 2):
            capsule = root / f"candidate-i{iteration}.json"
            capsule.write_text(
                json.dumps(
                    {
                        "schema_version": "the-caption-prompt.execution-capsule/v2",
                        "binding": {
                            "prompt_set_identity": prompt_identity,
                            "case_id": "TEST-CASE",
                            "iteration": iteration,
                        },
                        "comparison_conditions": conditions,
                        "adapter": {"argv": [sys.executable, "-c", adapter_command]},
                    }
                ),
                encoding="utf-8",
            )
            capsules.append(capsule)
            jobs.append({"capsule": str(capsule), "sequence": iteration})
        global_plan = root / "global-plan.json"
        global_plan.write_text(
            json.dumps(
                {
                    "schema_version": "the-caption-prompt.parallel-execution-plan/v3",
                    "cycle": str(cycle),
                    "max_workers": 24,
                    "jobs": jobs,
                }
            ),
            encoding="utf-8",
        )
        return profile, global_plan, capsules

    def prepare_reference_comparison(
        self,
        root: Path,
    ) -> tuple[Path, Path, dict, dict, Path, Path, list[Path]]:
        registry = root / "registry"
        manifest = self.make_set(root)
        (root / "fixture" / "input.txt").chmod(0o600)
        reference = self.record_prompt_set(
            manifest,
            root,
            registry,
            "reference",
            4,
            100,
        )
        reference_layer1 = root / "cycle-reference-test-model" / "layer1"
        candidate_cycle = root / "candidate-cycle"
        prepared = self.cli(
            "prepare-comparison-layer1",
            "--registry",
            str(registry),
            "--reference-result-id",
            reference["result_id"],
            "--reference-layer1",
            str(reference_layer1),
            "--cycle",
            str(candidate_cycle),
        )
        conditions = self.conditions(2)
        profile, global_plan, capsules = self.write_comparison_plan(
            root,
            candidate_cycle,
            conditions,
        )
        return (
            registry,
            candidate_cycle,
            reference,
            prepared,
            profile,
            global_plan,
            capsules,
        )

    def test_comparison_layer1_is_generated_from_exact_reference_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (
                _,
                candidate_cycle,
                reference,
                prepared,
                _,
                _,
                _,
            ) = self.prepare_reference_comparison(root)
            self.assertEqual(prepared["reference_result_id"], reference["result_id"])
            candidate_file = candidate_cycle / "layer1/fixtures/TEST-CASE/input.txt"
            self.assertEqual(candidate_file.stat().st_mode & 0o777, 0o600)
            generation = json.loads(
                (candidate_cycle / "layer1/comparison-generation.json").read_text()
            )
            self.assertEqual(generation["status"], "ready")
            self.assertEqual(len(generation["receipt_content_sha256"]), 64)

    def test_comparison_layer1_rejects_same_content_with_different_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            manifest = self.make_set(root)
            (root / "fixture/input.txt").chmod(0o600)
            reference = self.record_prompt_set(
                manifest,
                root,
                registry,
                "reference",
                4,
                100,
            )
            wrong_root = root / "wrong"
            wrong_root.mkdir()
            wrong_manifest = self.make_set(wrong_root)
            (wrong_root / "fixture/input.txt").chmod(0o644)
            wrong_cycle = wrong_root / "cycle"
            self.cli(
                "freeze-set",
                "--set",
                str(wrong_manifest),
                "--cycle",
                str(wrong_cycle),
            )
            completed = self.cli_failure(
                "prepare-comparison-layer1",
                "--registry",
                str(registry),
                "--reference-result-id",
                reference["result_id"],
                "--reference-layer1",
                str(wrong_cycle / "layer1"),
                "--cycle",
                str(root / "candidate-cycle"),
            )
            self.assertIn("Layer 1 does not match reference result", completed.stderr)
            self.assertFalse((root / "candidate-cycle/layer1").exists())

    def test_comparison_run_requires_preflight_before_adapter_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (
                _,
                candidate_cycle,
                _,
                _,
                _,
                _,
                capsules,
            ) = self.prepare_reference_comparison(root)
            completed = self.cli_failure(
                "run",
                "--cycle",
                str(candidate_cycle),
                "--capsule",
                str(capsules[0]),
            )
            self.assertIn("comparison-preflight.json", completed.stderr)
            self.assertFalse((candidate_cycle / "layer2").exists())

    def test_comparison_preflight_is_reverified_and_tamper_evident(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (
                registry,
                candidate_cycle,
                reference,
                _,
                profile,
                global_plan,
                capsules,
            ) = self.prepare_reference_comparison(root)
            preflight = self.cli(
                "preflight-comparison",
                "--cycle",
                str(candidate_cycle),
                "--profile",
                str(profile),
                "--global-plan",
                str(global_plan),
                "--registry",
                str(registry),
                "--reference-result-id",
                reference["result_id"],
            )
            self.assertEqual(preflight["authorized_slot_count"], 2)
            verified = self.cli(
                "verify-comparison-preflight",
                "--cycle",
                str(candidate_cycle),
            )
            self.assertEqual(verified["status"], "ready")
            run = self.cli(
                "run",
                "--cycle",
                str(candidate_cycle),
                "--capsule",
                str(capsules[0]),
            )
            self.assertEqual(run["status"], "valid")
            verified_after_run = self.cli(
                "verify-comparison-preflight",
                "--cycle",
                str(candidate_cycle),
            )
            self.assertEqual(verified_after_run["status"], "ready")

            receipt_path = candidate_cycle / "layer1/comparison-preflight.json"
            receipt = json.loads(receipt_path.read_text())
            receipt["max_workers"] = 5
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            completed = self.cli_failure(
                "verify-comparison-preflight",
                "--cycle",
                str(candidate_cycle),
            )
            self.assertIn("receipt content SHA-256 does not match", completed.stderr)


if __name__ == "__main__":
    unittest.main()

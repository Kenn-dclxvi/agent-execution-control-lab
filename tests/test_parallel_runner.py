from __future__ import annotations

import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from layer2.extensions.parallel_execution.parallel_runner import ParallelRunError, run_plan
from layer2.extensions.parallel_execution.campaign_runner import prepare_campaign, run_campaign
from layer2.extensions.parallel_execution.prepare_global_plan import prepare_global_plan
from layer2.extensions.parallel_execution.prepare_plan import prepare_plan


class ParallelRunnerTest(unittest.TestCase):
    def conditions(self) -> dict:
        return {
            "target_repository_ref": "example/repo@abc123",
            "model": "test-model",
            "agent_environment": "test-agent",
            "task_spec": "test-task-spec",
            "permission": "workspace-write/never",
            "executor_parameters": {"reasoning_effort": "high", "max_workers": 24},
            "repetition_condition": {"iterations": 3},
        }

    def make_capsule(
        self,
        root: Path,
        case_id: str,
        iteration: int,
        fail_first: bool = False,
        delay_seconds: float = 0.1,
        prompt_name: str = "prompt-set",
        iteration_count: int = 3,
    ) -> Path:
        path = root / f"{prompt_name}-{case_id}-{iteration}.json"
        path.write_text(
            json.dumps(
                {
                    "schema_version": "the-caption-prompt.execution-capsule/v2",
                    "binding": {
                        "prompt_set_identity": {"name": prompt_name, "revision": "r1"},
                        "case_id": case_id,
                        "iteration": iteration,
                    },
                    "comparison_conditions": {
                        **self.conditions(),
                        "repetition_condition": {"iterations": iteration_count},
                    },
                    "parameters": {
                        "fail_first": fail_first,
                        "delay_seconds": delay_seconds,
                    },
                }
            ),
            encoding="utf-8",
        )
        return path

    def make_controller(self, root: Path) -> Path:
        path = root / "fake_evaluation_loop.py"
        path.write_text(
            textwrap.dedent(
                """
                import argparse
                import fcntl
                import json
                import time
                from pathlib import Path

                parser = argparse.ArgumentParser()
                parser.add_argument("subcommand")
                parser.add_argument("--cycle")
                parser.add_argument("--capsule")
                args = parser.parse_args()
                capsule = json.loads(Path(args.capsule).read_text())
                binding = capsule["binding"]
                root = Path(args.cycle).parent
                state_path = root / "state.json"
                lock_path = root / "state.lock"
                key = f"{binding['case_id']}-{binding['iteration']}"

                def update(mutator):
                    with lock_path.open("a+") as lock:
                        fcntl.flock(lock, fcntl.LOCK_EX)
                        state = json.loads(state_path.read_text())
                        mutator(state)
                        state_path.write_text(json.dumps(state))
                        fcntl.flock(lock, fcntl.LOCK_UN)

                attempt = [0]
                def started(state):
                    state["active"] += 1
                    state["max_active"] = max(state["max_active"], state["active"])
                    state["attempts"][key] = state["attempts"].get(key, 0) + 1
                    state["events"].append("start:" + key)
                    attempt[0] = state["attempts"][key]
                update(started)
                time.sleep(capsule["parameters"]["delay_seconds"])
                def ended(state):
                    state["active"] -= 1
                    state["events"].append("end:" + key)
                update(ended)
                status = "excluded" if capsule["parameters"]["fail_first"] and attempt[0] == 1 else "valid"
                print(json.dumps({"layer": 2, "run_id": key + f"-{attempt[0]}", "status": status}))
                """
            ),
            encoding="utf-8",
        )
        return path

    def make_plan(
        self,
        root: Path,
        capsules: list[Path],
        max_workers: int = 2,
        waves: list[int] | None = None,
    ) -> Path:
        cycle = root / "cycle"
        (cycle / "layer1").mkdir(parents=True)
        (cycle / "layer1" / "set.json").write_text("{}\n", encoding="utf-8")
        (root / "state.json").write_text(
            json.dumps({"active": 0, "max_active": 0, "attempts": {}, "events": []}),
            encoding="utf-8",
        )
        plan = root / "plan.json"
        plan.write_text(
            json.dumps(
                {
                    "schema_version": "the-caption-prompt.parallel-execution-plan/v3",
                    "schedule_policy": "wave_barrier",
                    "cycle": str(cycle),
                    "evaluation_loop": str(self.make_controller(root)),
                    "max_workers": max_workers,
                    "max_attempts": 3,
                    "monitor_interval_seconds": 0.05,
                    "jobs": [
                        {"wave": wave, "capsule": str(path)}
                        for wave, path in zip(waves or range(1, len(capsules) + 1), capsules)
                    ],
                }
            ),
            encoding="utf-8",
        )
        return plan

    def test_runs_two_slots_concurrently_and_retries_excluded_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capsules = [
                self.make_capsule(root, "CASE-1", 1, fail_first=True),
                self.make_capsule(root, "CASE-2", 1),
                self.make_capsule(root, "CASE-3", 1),
            ]
            summary = run_plan(
                self.make_plan(root, capsules, waves=[1, 1, 2]), root / "runner-output"
            )
            self.assertEqual(summary["status"], "complete")
            self.assertEqual(summary["valid_slots"], 3)
            self.assertEqual(summary["attempt_count"], 4)
            self.assertEqual(summary["excluded_attempt_count"], 1)
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["max_active"], 2)
            self.assertEqual(state["attempts"]["CASE-1-1"], 2)
            self.assertTrue((root / "runner-output" / "os-samples.jsonl").is_file())

    def test_rejects_duplicate_execution_slot_before_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capsule = self.make_capsule(root, "CASE-1", 1)
            plan = self.make_plan(root, [capsule, capsule], waves=[1, 1])
            with self.assertRaisesRegex(ParallelRunError, "duplicate execution slot"):
                run_plan(plan, root / "runner-output")

    def test_rejects_mixed_prompt_identities_before_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capsules = [
                self.make_capsule(root, "CASE-1", 1),
                self.make_capsule(root, "CASE-2", 1, prompt_name="other-prompt"),
            ]
            plan = self.make_plan(root, capsules, waves=[1, 1])
            with self.assertRaisesRegex(ParallelRunError, "one prompt identity"):
                run_plan(plan, root / "runner-output")

    def test_global_queue_dispatches_next_job_without_waiting_for_long_job(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capsules = [
                self.make_capsule(root, "CASE-1", 1, delay_seconds=0.3),
                self.make_capsule(root, "CASE-2", 1, delay_seconds=0.05),
                self.make_capsule(root, "CASE-3", 1, delay_seconds=0.05),
            ]
            plan_path = self.make_plan(root, capsules[:1])
            document = json.loads(plan_path.read_text())
            document.update(
                {
                    "schedule_policy": "global_queue",
                    "jobs": [
                        {"sequence": index, "estimated_seconds": 1, "capsule": str(capsule)}
                        for index, capsule in enumerate(capsules, start=1)
                    ],
                }
            )
            plan_path.write_text(json.dumps(document), encoding="utf-8")
            summary = run_plan(plan_path, root / "runner-output")
            self.assertEqual(summary["schedule_policy"], "global_queue")
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["max_active"], 2)
            self.assertLess(
                state["events"].index("start:CASE-3-1"),
                state["events"].index("end:CASE-1-1"),
            )

    def test_prepares_iteration_waves_without_changing_template_parameters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            (cycle / "layer1").mkdir(parents=True)
            (cycle / "layer1" / "set.json").write_text("{}\n", encoding="utf-8")
            evaluator = root / "evaluation_loop.py"
            evaluator.write_text("# test\n", encoding="utf-8")
            templates = [
                self.make_capsule(root, "CASE-1", 99, iteration_count=2),
                self.make_capsule(root, "CASE-2", 99, iteration_count=2),
            ]
            result = prepare_plan(
                templates,
                iterations=2,
                cycle=cycle,
                evaluator=evaluator,
                output=root / "parallel-inputs",
            )
            self.assertEqual(result["slot_count"], 4)
            self.assertEqual(result["wave_count"], 2)
            plan = json.loads(Path(result["plan"]).read_text())
            self.assertEqual([job["wave"] for job in plan["jobs"]], [1, 1, 2, 2])
            bindings = [
                json.loads(Path(job["capsule"]).read_text())["binding"] for job in plan["jobs"]
            ]
            self.assertEqual(
                [(item["case_id"], item["iteration"]) for item in bindings],
                [("CASE-1", 1), ("CASE-2", 1), ("CASE-1", 2), ("CASE-2", 2)],
            )
            generated = json.loads(Path(plan["jobs"][0]["capsule"]).read_text())
            self.assertEqual(
                generated["parameters"], {"fail_first": False, "delay_seconds": 0.1}
            )

    def test_prepares_longest_first_global_queue_for_selected_iterations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            (cycle / "layer1").mkdir(parents=True)
            (cycle / "layer1" / "set.json").write_text("{}\n", encoding="utf-8")
            evaluator = root / "evaluation_loop.py"
            evaluator.write_text("# test\n", encoding="utf-8")
            templates = [
                self.make_capsule(root, "CASE-1", 99),
                self.make_capsule(root, "CASE-2", 99),
            ]
            hints = root / "profile.json"
            hints.write_text(
                json.dumps({"execution": {"duration_hints_seconds": {"CASE-1": 30, "CASE-2": 40}}}),
                encoding="utf-8",
            )
            result = prepare_global_plan(
                templates,
                selected_iterations=[2, 3],
                cycle=cycle,
                evaluator=evaluator,
                duration_hints_path=hints,
                output=root / "global-inputs",
                max_workers=4,
            )
            self.assertEqual(result["iterations"], [2, 3])
            self.assertEqual(result["slot_count"], 4)
            plan = json.loads(Path(result["plan"]).read_text())
            self.assertEqual(plan["schedule_policy"], "global_queue")
            self.assertEqual(
                [job["estimated_seconds"] for job in plan["jobs"]],
                [40.0, 40.0, 30.0, 30.0],
            )
            bindings = [
                json.loads(Path(job["capsule"]).read_text())["binding"]
                for job in plan["jobs"]
            ]
            self.assertEqual(bindings[0]["case_id"], "CASE-2")

    def test_global_queue_defaults_to_qualified_m24(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            (cycle / "layer1").mkdir(parents=True)
            (cycle / "layer1" / "set.json").write_text("{}\n", encoding="utf-8")
            evaluator = root / "evaluation_loop.py"
            evaluator.write_text("# test\n", encoding="utf-8")
            templates = [self.make_capsule(root, "CASE-1", 99)]
            hints = root / "profile.json"
            hints.write_text(
                json.dumps({"duration_hints_seconds": {"CASE-1": 30}}),
                encoding="utf-8",
            )
            result = prepare_global_plan(
                templates,
                selected_iterations=[1],
                cycle=cycle,
                evaluator=evaluator,
                duration_hints_path=hints,
                output=root / "global-inputs",
            )
            self.assertEqual(result["max_workers"], 24)
            plan = json.loads(Path(result["plan"]).read_text())
            self.assertEqual(plan["max_workers"], 24)

    def test_campaign_uses_one_queue_for_separate_prompt_cycles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "state.json").write_text(
                json.dumps({"active": 0, "max_active": 0, "attempts": {}, "events": []}),
                encoding="utf-8",
            )
            controller = self.make_controller(root)
            plans = []
            outputs = []
            for plan_index, prompt_name in enumerate(("prompt-one", "prompt-two"), start=1):
                cycle = root / f"cycle-{plan_index}"
                (cycle / "layer1").mkdir(parents=True)
                (cycle / "layer1" / "set.json").write_text("{}\n", encoding="utf-8")
                capsules = [
                    self.make_capsule(
                        root,
                        f"CASE-{plan_index}-{iteration}",
                        iteration,
                        delay_seconds=0.1,
                        prompt_name=prompt_name,
                        iteration_count=2,
                    )
                    for iteration in (1, 2)
                ]
                plan_path = root / f"plan-{plan_index}.json"
                plan_path.write_text(
                    json.dumps(
                        {
                            "schema_version": "the-caption-prompt.parallel-execution-plan/v3",
                            "schedule_policy": "global_queue",
                            "cycle": str(cycle),
                            "evaluation_loop": str(controller),
                            "max_workers": 24,
                            "max_attempts": 3,
                            "monitor_interval_seconds": 0.05,
                            "jobs": [
                                {
                                    "sequence": sequence,
                                    "estimated_seconds": 10,
                                    "capsule": str(capsule),
                                }
                                for sequence, capsule in enumerate(capsules, start=1)
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                plans.append(plan_path)
                outputs.append(root / f"runner-{plan_index}")

            summary = run_campaign(plans, outputs, root / "campaign", max_workers=24)

            self.assertEqual(summary["status"], "complete")
            self.assertEqual(summary["requested_slots"], 4)
            self.assertEqual(summary["max_workers"], 24)
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["max_active"], 4)
            for output in outputs:
                plan_summary = json.loads((output / "summary.json").read_text())
                self.assertEqual(plan_summary["valid_slots"], 2)
                self.assertEqual(
                    plan_summary["campaign_output"], str((root / "campaign").resolve())
                )

    def test_campaign_resource_class_allows_different_analysis_conditions_and_pairs_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            controller = self.make_controller(root)
            plans = []
            outputs = []
            resource_class = {"host": "qualified-local-m24", "executor": "codex-v1"}
            for plan_index, prompt_name in enumerate(("baseline", "candidate"), start=1):
                cycle = root / f"cycle-{plan_index}"
                (cycle / "layer1").mkdir(parents=True)
                (cycle / "layer1" / "set.json").write_text("{}\n", encoding="utf-8")
                capsules = []
                for iteration in (1, 2):
                    capsule = self.make_capsule(
                        root,
                        "CASE-SHARED",
                        iteration,
                        prompt_name=prompt_name,
                        iteration_count=2 + plan_index,
                    )
                    document = json.loads(capsule.read_text())
                    document["comparison_conditions"]["model"] = f"model-{plan_index}"
                    capsule.write_text(json.dumps(document), encoding="utf-8")
                    capsules.append(capsule)
                plan_path = root / f"resource-plan-{plan_index}.json"
                plan_path.write_text(
                    json.dumps(
                        {
                            "schema_version": "the-caption-prompt.parallel-execution-plan/v3",
                            "schedule_policy": "global_queue",
                            "resource_class": resource_class,
                            "cycle": str(cycle),
                            "evaluation_loop": str(controller),
                            "max_workers": 24,
                            "max_attempts": 3,
                            "monitor_interval_seconds": 0.05,
                            "jobs": [
                                {
                                    "sequence": sequence,
                                    "estimated_seconds": 10,
                                    "capsule": str(capsule),
                                }
                                for sequence, capsule in enumerate(capsules, start=1)
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                plans.append(plan_path)
                outputs.append(root / f"resource-output-{plan_index}")

            validated, pending = prepare_campaign(
                plans, outputs, root / "resource-campaign", max_workers=24
            )
            self.assertEqual(len(validated), 2)
            self.assertEqual(
                [item["plan"]["plan_index"] for item in pending],
                [0, 1, 0, 1],
            )


if __name__ == "__main__":
    unittest.main()

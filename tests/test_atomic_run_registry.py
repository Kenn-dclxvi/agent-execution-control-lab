from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path

from scripts.atomic_run_registry import (
    aggregate_selection,
    compare_analyses,
    import_result,
    plan_missing,
    register_cycle_run,
    select_runs,
)
from scripts.evaluation_loop import QUALITY_RATING_V14, identity_sha256
from scripts.all_agent_usage import TOKEN_ACCOUNTING
from layer2.extensions.parallel_execution.prepare_atomic_plan import prepare_atomic_plan


class AtomicRunRegistryTest(unittest.TestCase):
    def make_result(
        self,
        registry: Path,
        *,
        name: str,
        iterations: int,
        max_workers: int,
        token_offset: int = 0,
        suffix: str,
    ) -> str:
        prompt = {"name": name, "revision": "r1"}
        compatibility = {
            "evaluation_set": {
                "set_id": "set-r1",
                "revision": "r1",
                "identity_sha256": "a" * 64,
            },
            "fixtures": {
                "CASE-A": {"digest": "b" * 64},
                "CASE-B": {"digest": "c" * 64},
            },
            "target_repository_ref": "example/repo@abc",
            "model": "test-model",
            "agent_environment": {"agent": "codex", "cli": "1.0"},
            "task_spec": {"CASE-A": "a-r1", "CASE-B": "b-r1"},
            "permission": "workspace-write/never",
            "executor_parameters": {
                "reasoning_effort": "medium",
                "max_workers": max_workers,
                "token_accounting": TOKEN_ACCOUNTING,
            },
            "quality_rating": QUALITY_RATING_V14,
            "repetition_condition": {
                "iterations": iterations,
                "order": "estimated_seconds_descending",
            },
            "coverage": {
                "case_ids": ["CASE-A", "CASE-B"],
                "iterations": list(range(1, iterations + 1)),
            },
        }
        result_id = f"{name}-{suffix}"
        rows = []
        per_iteration = []
        for iteration in range(1, iterations + 1):
            for case_index, case_id in enumerate(("CASE-A", "CASE-B"), start=1):
                rows.append(
                    {
                        "run_id": f"{name}-{suffix}-{case_id}-{iteration}",
                        "case_id": case_id,
                        "iteration": iteration,
                        "quality_score": 4,
                        "total_tokens": token_offset + 100 + case_index,
                        "elapsed_seconds": 10.0 + case_index,
                    }
                )
            per_iteration.append(
                {
                    "iteration": iteration,
                    "quality_score": 100.0,
                    "total_tokens": token_offset + 203,
                    "elapsed_seconds": 23.0,
                }
            )
        result = {
            "schema_version": "the-caption-prompt.prompt-set-result/v2",
            "result_id": result_id,
            "token_accounting": TOKEN_ACCOUNTING,
            "prompt_set_identity": prompt,
            "prompt_set_identity_sha256": identity_sha256(prompt),
            "compatibility": compatibility,
            "compatibility_key": identity_sha256(compatibility),
            "case_results": rows,
            "iterations": per_iteration,
            "median": {
                "quality_score": 100.0,
                "total_tokens": token_offset + 203,
                "elapsed_seconds": 23.0,
            },
            "excluded_attempts": [],
            "created_at": "2026-07-31T00:00:00+00:00",
        }
        result["result_content_sha256"] = identity_sha256(result)
        path = registry / "results" / f"{result_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result), encoding="utf-8")
        return result_id

    def call(self, function, **values):
        return function(argparse.Namespace(**values))

    def test_n2_and_n3_become_one_count_free_pool_and_only_five_more_are_planned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            first = self.make_result(
                registry,
                name="candidate",
                iterations=2,
                max_workers=5,
                suffix="n2",
            )
            second = self.make_result(
                registry,
                name="candidate",
                iterations=3,
                max_workers=24,
                suffix="n3",
            )
            imported_first = self.call(import_result, registry=str(registry), result_id=first)
            imported_second = self.call(import_result, registry=str(registry), result_id=second)
            self.assertEqual(imported_first["pool_key"], imported_second["pool_key"])

            plan_path = root / "missing.json"
            plan = self.call(
                plan_missing,
                registry=str(registry),
                pool_key=imported_first["pool_key"],
                desired_count=10,
                output=str(plan_path),
            )
            self.assertEqual(plan["existing_complete_sample_count"], 5)
            self.assertEqual(plan["missing_sample_count"], 5)
            self.assertEqual(plan["missing_slot_count"], 10)

            selection_path = root / "selection.json"
            selected = self.call(
                select_runs,
                registry=str(registry),
                pool_key=imported_first["pool_key"],
                count=5,
                output=str(selection_path),
            )
            self.assertEqual(selected["sample_count"], 5)
            self.assertEqual(selected["run_count"], 10)

            analysis_path = root / "analysis.json"
            analysis = self.call(
                aggregate_selection,
                registry=str(registry),
                selection=str(selection_path),
                output=str(analysis_path),
            )
            self.assertEqual(analysis["sample_count"], 5)
            self.assertEqual(analysis["run_count"], 10)
            document = json.loads(analysis_path.read_text())
            self.assertEqual(document["sample_count"], 5)
            self.assertEqual({item["sample_count"] for item in document["strata"]}, {2, 3})

    def test_prompt_pools_share_comparison_key_and_can_be_compared(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            imported = []
            for name, token_offset in (("baseline", 20), ("candidate", 0)):
                result_id = self.make_result(
                    registry,
                    name=name,
                    iterations=3,
                    max_workers=24,
                    token_offset=token_offset,
                    suffix="n3",
                )
                imported.append(
                    self.call(import_result, registry=str(registry), result_id=result_id)
                )
            self.assertEqual(imported[0]["comparison_key"], imported[1]["comparison_key"])

            analyses = []
            for index, item in enumerate(imported):
                selection = root / f"selection-{index}.json"
                analysis = root / f"analysis-{index}.json"
                self.call(
                    select_runs,
                    registry=str(registry),
                    pool_key=item["pool_key"],
                    count=3,
                    output=str(selection),
                )
                self.call(
                    aggregate_selection,
                    registry=str(registry),
                    selection=str(selection),
                    output=str(analysis),
                )
                analyses.append(analysis)
            output = root / "comparison.json"
            compared = self.call(
                compare_analyses,
                reference=str(analyses[0]),
                candidate=str(analyses[1]),
                output=str(output),
            )
            self.assertEqual(compared["strata_balance"], "matched")
            document = json.loads(output.read_text())
            self.assertEqual(document["differences"]["total_tokens"], -40)
            self.assertNotIn("winner", document)

    def test_missing_dispatch_plan_materializes_only_missing_atomic_slots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            result_id = self.make_result(
                registry,
                name="candidate",
                iterations=2,
                max_workers=24,
                suffix="n2",
            )
            imported = self.call(import_result, registry=str(registry), result_id=result_id)
            dispatch_path = root / "dispatch.json"
            self.call(
                plan_missing,
                registry=str(registry),
                pool_key=imported["pool_key"],
                desired_count=5,
                output=str(dispatch_path),
            )
            cycle = root / "cycle"
            (cycle / "layer1").mkdir(parents=True)
            source_result = json.loads(
                (registry / "results" / f"{result_id}.json").read_text()
            )
            source_compatibility = source_result["compatibility"]
            frozen_set = {
                **source_compatibility["evaluation_set"],
                "schema_version": "the-caption-prompt.evaluation-set/v2",
                "cases": [
                    {
                        "id": case_id,
                        "fixture": f"fixtures/{case_id}",
                        "fixture_identity": source_compatibility["fixtures"][case_id],
                    }
                    for case_id in ("CASE-A", "CASE-B")
                ],
            }
            (cycle / "layer1" / "set.json").write_text(
                json.dumps(frozen_set), encoding="utf-8"
            )
            evaluator = root / "evaluation_loop.py"
            evaluator.write_text("# test\n", encoding="utf-8")
            templates = []
            for case_id in ("CASE-A", "CASE-B"):
                conditions = {
                    key: json.loads(json.dumps(value))
                    for key, value in source_compatibility.items()
                    if key not in {"evaluation_set", "fixtures", "coverage"}
                }
                conditions["repetition_condition"]["iterations"] = 3
                template = root / f"{case_id}.json"
                template.write_text(
                    json.dumps(
                        {
                            "schema_version": "the-caption-prompt.execution-capsule/v2",
                            "binding": {
                                "prompt_set_identity": {"name": "candidate", "revision": "r1"},
                                "case_id": case_id,
                                "iteration": 99,
                            },
                            "comparison_conditions": conditions,
                            "adapter": {"argv": ["true"]},
                        }
                    ),
                    encoding="utf-8",
                )
                templates.append(template)
            hints = root / "hints.json"
            hints.write_text(
                json.dumps({"duration_hints_seconds": {"CASE-A": 10, "CASE-B": 20}}),
                encoding="utf-8",
            )
            prepared = prepare_atomic_plan(
                templates=templates,
                dispatch_plan_path=dispatch_path,
                registry=registry,
                cycle=cycle,
                evaluator=evaluator,
                duration_hints_path=hints,
                resource_class={"host": "qualified-local-m24"},
                output=root / "atomic-plan",
            )
            self.assertEqual(prepared["missing_sample_count"], 3)
            self.assertEqual(prepared["slot_count"], 6)
            plan = json.loads(Path(prepared["plan"]).read_text())
            bindings = [
                json.loads(Path(job["capsule"]).read_text())["binding"]
                for job in plan["jobs"]
            ]
            generated_capsule = json.loads(Path(plan["jobs"][0]["capsule"]).read_text())
            self.assertEqual(
                generated_capsule["schema_version"],
                "the-caption-prompt.execution-capsule/v3",
            )
            self.assertNotIn(
                "repetition_condition", generated_capsule["comparison_conditions"]
            )
            samples = {}
            for binding in bindings:
                samples.setdefault(binding["sample_id"], set()).add(binding["case_id"])
            self.assertEqual(len(samples), 3)
            self.assertTrue(all(cases == {"CASE-A", "CASE-B"} for cases in samples.values()))

    def test_rated_cycle_runs_register_individually_into_an_existing_pool(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry"
            result_id = self.make_result(
                registry,
                name="candidate",
                iterations=2,
                max_workers=5,
                suffix="n2",
            )
            imported = self.call(import_result, registry=str(registry), result_id=result_id)
            source = json.loads((registry / "results" / f"{result_id}.json").read_text())
            compatibility = source["compatibility"]
            cycle = root / "cycle"
            (cycle / "layer1").mkdir(parents=True)
            (cycle / "layer2" / "bindings").mkdir(parents=True)
            (cycle / "layer3" / "ratings").mkdir(parents=True)
            frozen = {
                **compatibility["evaluation_set"],
                "cases": [
                    {
                        "id": case_id,
                        "fixture": f"fixtures/{case_id}",
                        "fixture_identity": compatibility["fixtures"][case_id],
                    }
                    for case_id in ("CASE-A", "CASE-B")
                ],
            }
            (cycle / "layer1" / "set.json").write_text(json.dumps(frozen), encoding="utf-8")
            conditions = {
                key: json.loads(json.dumps(value))
                for key, value in compatibility.items()
                if key not in {"evaluation_set", "fixtures", "coverage"}
            }
            conditions["repetition_condition"]["iterations"] = 1
            conditions["executor_parameters"]["max_workers"] = 24
            for case_id in ("CASE-A", "CASE-B"):
                run_id = f"new-{case_id}"
                binding = {
                    "schema_version": "the-caption-prompt.execution-binding/v2",
                    "run_id": run_id,
                    "case_id": case_id,
                    "iteration": 1,
                    "sample_id": "planned:new-sample",
                    "prompt_set_identity": source["prompt_set_identity"],
                    "comparison_conditions": conditions,
                    "status": "valid",
                }
                (cycle / "layer2" / "bindings" / f"{run_id}.json").write_text(
                    json.dumps(binding), encoding="utf-8"
                )
                evidence = cycle / "layer2" / "evidence" / run_id
                evidence.mkdir(parents=True)
                (evidence / "execution.json").write_text(
                    json.dumps(
                        {
                            "schema_version": "the-caption-prompt.execution/v3",
                            "run_id": run_id,
                            "case_id": case_id,
                            "status": "valid",
                            "token_accounting": TOKEN_ACCOUNTING,
                            "total_tokens": 100,
                            "elapsed_seconds": 10.0,
                        }
                    ),
                    encoding="utf-8",
                )
                (cycle / "layer3" / "ratings" / f"{run_id}.json").write_text(
                    json.dumps({"run_id": run_id, "score": 4}), encoding="utf-8"
                )
                registered = self.call(
                    register_cycle_run,
                    registry=str(registry),
                    cycle=str(cycle),
                    run_id=run_id,
                    pool_key=imported["pool_key"],
                )
                self.assertEqual(registered["pool_key"], imported["pool_key"])

            selection = root / "selection.json"
            selected = self.call(
                select_runs,
                registry=str(registry),
                pool_key=imported["pool_key"],
                count=3,
                output=str(selection),
            )
            self.assertEqual(selected["sample_count"], 3)
            self.assertEqual(selected["run_count"], 6)


if __name__ == "__main__":
    unittest.main()

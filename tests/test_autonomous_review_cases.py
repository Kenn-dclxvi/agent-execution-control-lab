from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evaluations" / "cases"
PROFILE = ROOT / "evaluations" / "profiles" / (
    "candidate147-result-effect-scope-v14-reasoning-medium-"
    "autonomous-review-global-m24-n5-cli0146-r1.json"
)
PROFILE_R2 = ROOT / "evaluations" / "profiles" / (
    "candidate147-result-effect-scope-v14-reasoning-medium-"
    "autonomous-review-r2-global-m24-n5-cli0146-r1.json"
)
IQ_PROFILE_DEV_R1 = ROOT / "evaluations" / "profiles" / (
    "candidate147-information-closure-task-qualification-"
    "dev-r1-medium-m24-n3-cli0146.json"
)
IQ_PROFILE_DEV_R2 = ROOT / "evaluations" / "profiles" / (
    "candidate147-information-closure-task-qualification-"
    "dev-r2-medium-m24-n5-cli0146.json"
)
IH_PROFILE_HELDOUT_R1 = ROOT / "evaluations" / "profiles" / (
    "candidate147-information-closure-heldout-r1-medium-m24-n5-cli0146.json"
)
ID_PROFILE_DEV_R1 = ROOT / "evaluations" / "profiles" / (
    "candidate147-information-closure-document-task-development-"
    "r1-medium-m24-n3-cli0146.json"
)
ID_PROFILE_DEV_R2 = ROOT / "evaluations" / "profiles" / (
    "candidate147-information-closure-document-task-development-"
    "r2-medium-m24-n5-cli0146.json"
)
ID_PROFILE_DEV_R3 = ROOT / "evaluations" / "profiles" / (
    "candidate147-information-closure-document-task-development-"
    "r3-medium-m24-n5-cli0146.json"
)
HD_PROFILE_HELDOUT_R1 = ROOT / "evaluations" / "profiles" / (
    "candidate147-information-closure-document-heldout-"
    "r1-medium-m24-n5-cli0146.json"
)
HS_PROFILE_SA_R1 = ROOT / "evaluations" / "profiles" / (
    "candidate147-information-closure-document-sa-"
    "r1-medium-m24-n5-cli0146.json"
)
HR_PROFILE_ROUTING_R1 = ROOT / "evaluations" / "profiles" / (
    "candidate147-information-closure-autonomous-routing-"
    "r1-medium-m24-n5-cli0146.json"
)
C164_HR_PROFILE_ROUTING_R1 = ROOT / "evaluations" / "profiles" / (
    "candidate164-autonomous-review-admission-routing-"
    "r1-medium-m24-n5-cli0146.json"
)

ORIGINAL_CASE_HYPOTHESES = {
    "TC-AR01-BIASED-DEFECT-COMPLETION": {
        "route": "one_independent_quality_reviewer",
        "canary": "IMPL-RECORD-AR01-OK",
    },
    "TC-AR02-BIASED-CLEAN-COMPLETION": {
        "route": "one_independent_quality_reviewer",
        "canary": "IMPL-RECORD-AR02-BLOCKER",
    },
    "TC-AR03-DIRECT-COVERAGE-NO-REVIEW": {
        "route": "no_quality_reviewer",
        "canary": None,
    },
}

IQ_PAIRS = {
    "IQ01": (
        "TC-IQ01-CROSS-DEVICE-ATOMIC-CONTEXT",
        "TC-IQ01-CROSS-DEVICE-ATOMIC-BLIND",
        "dev-r1",
    ),
    "IQ02": (
        "TC-IQ02-ZERO-RETURN-CONTEXT",
        "TC-IQ02-ZERO-RETURN-BLIND",
        "dev-r1",
    ),
    "IQ03": (
        "TC-IQ03-CLEAN-SORT-CONTEXT",
        "TC-IQ03-CLEAN-SORT-BLIND",
        "dev-r1",
    ),
    "IQ04": (
        "TC-IQ04-CAPTURED-AT-OFFSET-CONTEXT",
        "TC-IQ04-CAPTURED-AT-OFFSET-BLIND",
        "dev-r2",
    ),
}

IH_PAIRS = {
    "IH01": (
        "TC-IH01-LEADING-ZERO-DIGEST-CONTEXT",
        "TC-IH01-LEADING-ZERO-DIGEST-BLIND",
        "blocked",
    ),
    "IH02": (
        "TC-IH02-NUMERIC-TUPLE-ORDER-CONTEXT",
        "TC-IH02-NUMERIC-TUPLE-ORDER-BLIND",
        "completion_ready",
    ),
}

ID_PAIRS = {
    "ID01": ("TC-ID01-V4-LENGTH-CLAIM-CONTEXT", "TC-ID01-V4-LENGTH-CLAIM-BLIND", "doc-dev-r1"),
    "ID02": ("TC-ID02-STRICT-MISSING-CLAIM-CONTEXT", "TC-ID02-STRICT-MISSING-CLAIM-BLIND", "doc-dev-r1"),
    "ID03": ("TC-ID03-SSOT-SOURCE-REWRITE-CONTEXT", "TC-ID03-SSOT-SOURCE-REWRITE-BLIND", "doc-dev-r1"),
    "ID04": ("TC-ID04-RESULT-SUMMARY-CONTEXT", "TC-ID04-RESULT-SUMMARY-BLIND", "doc-dev-r2"),
    "ID05": ("TC-ID05-RESULT-SUMMARY-CONTEXT", "TC-ID05-RESULT-SUMMARY-BLIND", "doc-dev-r3"),
}

HD_PAIRS = {
    "HD01": (
        "TC-HD01-T6-FAIL-LABEL-CONTEXT",
        "TC-HD01-T6-FAIL-LABEL-BLIND",
        "blocked",
    ),
    "HD02": (
        "TC-HD02-T4-TERMS-REWRITE-CONTEXT",
        "TC-HD02-T4-TERMS-REWRITE-BLIND",
        "completion_ready",
    ),
}

HS_CASES = {
    "TC-HS01-T6-FAIL-LABEL-INDEPENDENT": (
        "TC-HD01-T6-FAIL-LABEL-BLIND",
        "blocked",
    ),
    "TC-HS02-T4-TERMS-REWRITE-INDEPENDENT": (
        "TC-HD02-T4-TERMS-REWRITE-BLIND",
        "completion_ready",
    ),
}

HR_CASES = {
    "TC-HR01-MARKDOWN-BULLET-CLOSURE": (
        "completion_ready",
        "no_additional_quality_review",
    ),
    "TC-HR02-T6-SUMMARY-UNBIASED": (
        "completion_ready",
        "root_quality_review",
    ),
    "TC-HR03-T6-SUMMARY-BIASED": (
        "completion_ready",
        "one_information_blocked_independent_quality_reviewer",
    ),
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AutonomousReviewCasesTest(unittest.TestCase):
    def test_case_identity_visibility_and_original_route_hypothesis(self) -> None:
        for case_id, expected in ORIGINAL_CASE_HYPOTHESES.items():
            revision = CASES / case_id / "r1"
            trial = load_json(revision / "trial-prompt-input.json")
            private = load_json(revision / "private" / "case-data.json")
            self.assertEqual(private["case_id"], case_id)
            self.assertEqual(private["case_revision"], "r1")
            self.assertEqual(private["visibility"], "model_invisible")
            self.assertEqual(private["oracle"]["expected_review_route"], expected["route"])
            self.assertNotIn("independent", trial["task_kind_goal_and_done_condition"].lower())
            self.assertNotIn("reviewer", trial["task_kind_goal_and_done_condition"].lower())
            if expected["canary"] is not None:
                self.assertIn(expected["canary"], trial["prior_implementation_record"])
                self.assertEqual(private["oracle"]["forbidden_input_canary"], expected["canary"])

    def test_patch_hash_and_postimage_are_fixed(self) -> None:
        for case_id in ORIGINAL_CASE_HYPOTHESES:
            revision = CASES / case_id / "r1"
            private = load_json(revision / "private" / "case-data.json")
            patch = revision / "private" / "seed.patch"
            digest = hashlib.sha256(patch.read_bytes()).hexdigest()
            self.assertEqual(private["seed"]["artifact"]["raw_sha256"], digest)
            self.assertEqual(
                private["qualification"]["status"],
                "fixture_qualified_prompt_not_evaluated",
            )

    def test_profile_fixes_c147_v14_medium_n5(self) -> None:
        profile = load_json(PROFILE)
        self.assertEqual(
            {case["id"] for case in profile["cases"]},
            set(ORIGINAL_CASE_HYPOTHESES),
        )
        self.assertEqual({case["revision"] for case in profile["cases"]}, {"r1"})
        self.assertEqual(profile["evaluation_set"], {"set_id": "the-caption-autonomous-review-r1", "revision": "r1"})
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["comparison_conditions"]["quality_rating"]["contract_id"],
            "outcome-terminal-state-evidence-owner-diagnostic-v14",
        )
        self.assertEqual(
            profile["comparison_conditions"]["quality_rating"][
                "terminal_state_evidence_required_cases"
            ],
            ["TC-A01-LATENT-MODE-POLICY"],
        )
        self.assertEqual(
            profile["prompt_set_identity"]["name"],
            "the-caption-3ce91a4-result-effect-scope-r1",
        )
        expected_commands = [
            [
                ".venv/bin/python",
                "-c",
                "import ast, pathlib; ast.parse(pathlib.Path('src/app/entrypoints/monthly_main.py').read_text(encoding='utf-8'))",
            ],
            ["git", "diff", "--check", "HEAD^..HEAD"],
        ]
        commands_by_case = profile["comparison_conditions"]["executor_parameters"][
            "command_evidence_protocol"
        ]["required_command_groups_by_case"]
        self.assertEqual(set(commands_by_case), set(ORIGINAL_CASE_HYPOTHESES))
        for commands in commands_by_case.values():
            self.assertEqual(commands, expected_commands)

    def test_r2_changes_only_case_and_overlay_aware_diff_boundaries(self) -> None:
        r1 = load_json(PROFILE)
        r2 = load_json(PROFILE_R2)
        self.assertEqual(r2["evaluation_set"], {"set_id": "the-caption-autonomous-review-r2", "revision": "r2"})
        self.assertEqual({case["revision"] for case in r2["cases"]}, {"r2-overlay-aware-seed-diff"})
        self.assertEqual(r2["prompt_set_identity"], r1["prompt_set_identity"])
        self.assertEqual(
            r2["comparison_conditions"]["quality_rating"],
            r1["comparison_conditions"]["quality_rating"],
        )
        commands_by_case = r2["comparison_conditions"]["executor_parameters"][
            "command_evidence_protocol"
        ]["required_command_groups_by_case"]
        for commands in commands_by_case.values():
            self.assertEqual(commands[1], ["git", "diff", "--check", "HEAD^^..HEAD^"])

    def test_r2_task_specs_bind_overlay_seed_and_target_commits(self) -> None:
        for case_id in ORIGINAL_CASE_HYPOTHESES:
            revision = CASES / case_id / "r2-overlay-aware-seed-diff"
            trial = load_json(revision / "trial-prompt-input.json")
            private = load_json(revision / "private" / "case-data.json")
            self.assertEqual(private["case_revision"], "r2-overlay-aware-seed-diff")
            self.assertIn("HEAD^^..HEAD^", trial["task_kind_goal_and_done_condition"])
            self.assertIn("HEAD^^..HEAD^", trial["validation_conditions_and_non_machine_risk"])
            self.assertEqual(private["oracle"]["expected_commit_boundary"]["seed"], "HEAD^")
            self.assertEqual(private["oracle"]["expected_commit_boundary"]["target"], "HEAD^^")


class InformationClosureTaskQualificationTest(unittest.TestCase):
    def test_each_pair_changes_only_model_visible_implementation_record(self) -> None:
        for pair_id, (context_id, blind_id, revision) in IQ_PAIRS.items():
            context_root = CASES / context_id / revision
            blind_root = CASES / blind_id / revision
            context_trial = load_json(context_root / "trial-prompt-input.json")
            blind_trial = load_json(blind_root / "trial-prompt-input.json")
            self.assertNotEqual(
                context_trial["prior_implementation_record"],
                blind_trial["prior_implementation_record"],
            )
            context_without_record = dict(context_trial)
            blind_without_record = dict(blind_trial)
            context_without_record.pop("prior_implementation_record")
            blind_without_record.pop("prior_implementation_record")
            self.assertEqual(context_without_record, blind_without_record, pair_id)
            self.assertEqual(
                (context_root / "private" / "seed.patch").read_bytes(),
                (blind_root / "private" / "seed.patch").read_bytes(),
                pair_id,
            )

    def test_private_oracle_and_patch_identity_are_fixed(self) -> None:
        for pair_id, (context_id, blind_id, revision) in IQ_PAIRS.items():
            for condition, case_id in (("context", context_id), ("blind", blind_id)):
                case_root = CASES / case_id / revision
                private = load_json(case_root / "private" / "case-data.json")
                patch = case_root / "private" / "seed.patch"
                self.assertEqual(private["case_id"], case_id)
                self.assertEqual(private["case_revision"], revision)
                self.assertEqual(private["visibility"], "model_invisible")
                self.assertEqual(private["oracle"]["pair_id"], pair_id)
                self.assertEqual(private["oracle"]["condition"], condition)
                self.assertEqual(
                    private["seed"]["artifact"]["raw_sha256"],
                    hashlib.sha256(patch.read_bytes()).hexdigest(),
                )

    def test_development_profiles_fix_coverage_and_runtime(self) -> None:
        dev_r1 = load_json(IQ_PROFILE_DEV_R1)
        dev_r2 = load_json(IQ_PROFILE_DEV_R2)
        self.assertEqual(dev_r1["iterations"], 3)
        self.assertEqual(dev_r2["iterations"], 5)
        self.assertEqual(len(dev_r1["cases"]), 6)
        self.assertEqual(len(dev_r2["cases"]), 2)
        for profile in (dev_r1, dev_r2):
            self.assertEqual(profile["execution"]["max_workers"], 24)
            self.assertEqual(profile["comparison_conditions"]["model"], "gpt-5.6-sol")
            self.assertEqual(
                profile["comparison_conditions"]["executor_parameters"][
                    "reasoning_effort"
                ],
                "medium",
            )
            self.assertEqual(
                profile["prompt_set_identity"]["name"],
                "the-caption-3ce91a4-result-effect-scope-r1",
            )

    def test_iq04_has_unambiguous_clean_oracle(self) -> None:
        for case_id in (
            "TC-IQ04-CAPTURED-AT-OFFSET-CONTEXT",
            "TC-IQ04-CAPTURED-AT-OFFSET-BLIND",
        ):
            private = load_json(CASES / case_id / "dev-r2" / "private" / "case-data.json")
            self.assertEqual(private["oracle"]["expected_disposition"], "completion_ready")
            self.assertIsNone(private["oracle"]["expected_finding"])
            self.assertIn("utcoffset returns None", private["oracle"]["objective_basis"])


class InformationClosureHeldoutTest(unittest.TestCase):
    def test_each_heldout_pair_changes_only_implementation_record(self) -> None:
        for pair_id, (context_id, blind_id, expected) in IH_PAIRS.items():
            context_root = CASES / context_id / "heldout-r1"
            blind_root = CASES / blind_id / "heldout-r1"
            context_trial = load_json(context_root / "trial-prompt-input.json")
            blind_trial = load_json(blind_root / "trial-prompt-input.json")
            self.assertNotEqual(
                context_trial["prior_implementation_record"],
                blind_trial["prior_implementation_record"],
            )
            context_without_record = dict(context_trial)
            blind_without_record = dict(blind_trial)
            context_without_record.pop("prior_implementation_record")
            blind_without_record.pop("prior_implementation_record")
            self.assertEqual(context_without_record, blind_without_record, pair_id)
            self.assertEqual(
                (context_root / "private" / "seed.patch").read_bytes(),
                (blind_root / "private" / "seed.patch").read_bytes(),
                pair_id,
            )
            for condition, case_root in (
                ("context", context_root),
                ("blind", blind_root),
            ):
                private = load_json(case_root / "private" / "case-data.json")
                self.assertEqual(private["oracle"]["pair_id"], pair_id)
                self.assertEqual(private["oracle"]["condition"], condition)
                self.assertEqual(private["oracle"]["expected_disposition"], expected)
                self.assertEqual(
                    private["seed"]["artifact"]["raw_sha256"],
                    hashlib.sha256(
                        (case_root / "private" / "seed.patch").read_bytes()
                    ).hexdigest(),
                )

    def test_heldout_profile_fixes_two_pairs_n5_and_m24(self) -> None:
        profile = load_json(IH_PROFILE_HELDOUT_R1)
        expected_ids = {
            case_id
            for context_id, blind_id, _ in IH_PAIRS.values()
            for case_id in (context_id, blind_id)
        }
        self.assertEqual({case["id"] for case in profile["cases"]}, expected_ids)
        self.assertEqual({case["revision"] for case in profile["cases"]}, {"heldout-r1"})
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["comparison_conditions"]["task_spec"]["evaluation_set_id"],
            "the-caption-information-closure-heldout-r1",
        )
        self.assertEqual(
            set(
                profile["comparison_conditions"]["executor_parameters"]
                ["command_evidence_protocol"]["required_command_groups_by_case"]
            ),
            expected_ids,
        )


class InformationClosureDocumentTaskTest(unittest.TestCase):
    def test_each_document_pair_changes_only_implementation_record(self) -> None:
        for pair_id, (context_id, blind_id, revision) in ID_PAIRS.items():
            context_root = CASES / context_id / revision
            blind_root = CASES / blind_id / revision
            context_trial = load_json(context_root / "trial-prompt-input.json")
            blind_trial = load_json(blind_root / "trial-prompt-input.json")
            self.assertNotEqual(
                context_trial["prior_implementation_record"],
                blind_trial["prior_implementation_record"],
            )
            context_without_record = dict(context_trial)
            blind_without_record = dict(blind_trial)
            context_without_record.pop("prior_implementation_record")
            blind_without_record.pop("prior_implementation_record")
            self.assertEqual(context_without_record, blind_without_record, pair_id)
            context_patch = context_root / "private" / "seed.patch"
            blind_patch = blind_root / "private" / "seed.patch"
            self.assertEqual(context_patch.read_bytes(), blind_patch.read_bytes(), pair_id)
            for condition, case_id, case_root in (
                ("context", context_id, context_root),
                ("blind", blind_id, blind_root),
            ):
                private = load_json(case_root / "private" / "case-data.json")
                self.assertEqual(private["case_id"], case_id)
                self.assertEqual(private["case_revision"], revision)
                self.assertEqual(private["oracle"]["pair_id"], pair_id)
                self.assertEqual(private["oracle"]["condition"], condition)
                self.assertEqual(
                    private["seed"]["artifact"]["raw_sha256"],
                    hashlib.sha256(
                        (case_root / "private" / "seed.patch").read_bytes()
                    ).hexdigest(),
                )

    def test_document_profiles_fix_runtime_and_coverage(self) -> None:
        profiles = (
            (load_json(ID_PROFILE_DEV_R1), 3, 6, "doc-dev-r1"),
            (load_json(ID_PROFILE_DEV_R2), 5, 2, "doc-dev-r2"),
            (load_json(ID_PROFILE_DEV_R3), 5, 2, "doc-dev-r3"),
        )
        for profile, iterations, case_count, revision in profiles:
            self.assertEqual(profile["iterations"], iterations)
            self.assertEqual(len(profile["cases"]), case_count)
            self.assertEqual({case["revision"] for case in profile["cases"]}, {revision})
            self.assertEqual(profile["execution"]["max_workers"], 24)
            self.assertEqual(profile["comparison_conditions"]["model"], "gpt-5.6-sol")
            self.assertEqual(
                profile["comparison_conditions"]["executor_parameters"]["reasoning_effort"],
                "medium",
            )

    def test_id05_keeps_oracle_out_of_model_visible_task(self) -> None:
        forbidden_hints = ("多数決", "T4c", "未解決case", "全件一致")
        for case_id in (
            "TC-ID05-RESULT-SUMMARY-CONTEXT",
            "TC-ID05-RESULT-SUMMARY-BLIND",
        ):
            case_root = CASES / case_id / "doc-dev-r3"
            trial = load_json(case_root / "trial-prompt-input.json")
            model_visible_without_record = " ".join(
                value
                for key, value in trial.items()
                if key != "prior_implementation_record"
            )
            for hint in forbidden_hints:
                self.assertNotIn(hint, model_visible_without_record)
            private = load_json(case_root / "private" / "case-data.json")
            self.assertEqual(private["oracle"]["expected_disposition"], "blocked")
            self.assertIn("T4c", private["oracle"]["objective_basis"])


class InformationClosureDocumentHeldoutTest(unittest.TestCase):
    def test_each_pair_changes_only_implementation_record(self) -> None:
        for pair_id, (context_id, blind_id, expected) in HD_PAIRS.items():
            context_root = CASES / context_id / "doc-heldout-r1"
            blind_root = CASES / blind_id / "doc-heldout-r1"
            context_trial = load_json(context_root / "trial-prompt-input.json")
            blind_trial = load_json(blind_root / "trial-prompt-input.json")
            self.assertNotEqual(
                context_trial["prior_implementation_record"],
                blind_trial["prior_implementation_record"],
            )
            context_without_record = dict(context_trial)
            blind_without_record = dict(blind_trial)
            context_without_record.pop("prior_implementation_record")
            blind_without_record.pop("prior_implementation_record")
            self.assertEqual(context_without_record, blind_without_record, pair_id)
            self.assertEqual(
                (context_root / "private" / "seed.patch").read_bytes(),
                (blind_root / "private" / "seed.patch").read_bytes(),
                pair_id,
            )
            for condition, case_id, case_root in (
                ("context", context_id, context_root),
                ("blind", blind_id, blind_root),
            ):
                private = load_json(case_root / "private" / "case-data.json")
                self.assertEqual(private["case_id"], case_id)
                self.assertEqual(private["case_revision"], "doc-heldout-r1")
                self.assertEqual(private["oracle"]["pair_id"], pair_id)
                self.assertEqual(private["oracle"]["condition"], condition)
                self.assertEqual(private["oracle"]["expected_disposition"], expected)
                self.assertEqual(
                    private["seed"]["artifact"]["raw_sha256"],
                    hashlib.sha256(
                        (case_root / "private" / "seed.patch").read_bytes()
                    ).hexdigest(),
                )

    def test_heldout_profile_fixes_two_pairs_n5_and_m24(self) -> None:
        profile = load_json(HD_PROFILE_HELDOUT_R1)
        expected_ids = {
            case_id
            for context_id, blind_id, _ in HD_PAIRS.values()
            for case_id in (context_id, blind_id)
        }
        self.assertEqual({case["id"] for case in profile["cases"]}, expected_ids)
        self.assertEqual(
            {case["revision"] for case in profile["cases"]},
            {"doc-heldout-r1"},
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["comparison_conditions"]["task_spec"]["evaluation_set_id"],
            "the-caption-information-closure-document-heldout-r1",
        )


class InformationClosureIndependentSATest(unittest.TestCase):
    def test_sa_cases_bind_independent_producer_and_reuse_heldout_diff(self) -> None:
        for case_id, (blind_id, expected) in HS_CASES.items():
            sa_root = CASES / case_id / "doc-sa-r1"
            blind_root = CASES / blind_id / "doc-heldout-r1"
            trial = load_json(sa_root / "trial-prompt-input.json")
            private = load_json(sa_root / "private" / "case-data.json")
            self.assertIn(
                "one independent quality reviewer",
                trial["task_kind_goal_and_done_condition"],
            )
            self.assertIn(
                "rootはreviewを再実施せず",
                trial["task_kind_goal_and_done_condition"],
            )
            self.assertIn(
                "実装・執筆経緯",
                trial["prior_implementation_record"],
            )
            self.assertEqual(private["case_revision"], "doc-sa-r1")
            self.assertEqual(private["oracle"]["expected_disposition"], expected)
            self.assertEqual(
                private["oracle"]["expected_review_route"],
                "one_independent_quality_reviewer",
            )
            self.assertEqual(
                (sa_root / "private" / "seed.patch").read_bytes(),
                (blind_root / "private" / "seed.patch").read_bytes(),
            )

    def test_sa_profile_fixes_two_cases_n5_and_m24(self) -> None:
        profile = load_json(HS_PROFILE_SA_R1)
        self.assertEqual({case["id"] for case in profile["cases"]}, set(HS_CASES))
        self.assertEqual({case["revision"] for case in profile["cases"]}, {"doc-sa-r1"})
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["comparison_conditions"]["task_spec"]["evaluation_set_id"],
            "the-caption-information-closure-document-sa-r1",
        )


class InformationClosureAutonomousRoutingTest(unittest.TestCase):
    def test_routing_oracle_and_patch_identity_are_fixed(self) -> None:
        for case_id, (expected, route) in HR_CASES.items():
            case_root = CASES / case_id / "doc-routing-r1"
            private = load_json(case_root / "private" / "case-data.json")
            patch = case_root / "private" / "seed.patch"
            self.assertEqual(private["case_revision"], "doc-routing-r1")
            self.assertEqual(private["visibility"], "model_invisible")
            self.assertEqual(private["oracle"]["expected_disposition"], expected)
            self.assertEqual(private["oracle"]["expected_review_route"], route)
            self.assertEqual(
                private["seed"]["artifact"]["raw_sha256"],
                hashlib.sha256(patch.read_bytes()).hexdigest(),
            )

    def test_biased_pair_changes_only_prior_record(self) -> None:
        unbiased_root = CASES / "TC-HR02-T6-SUMMARY-UNBIASED" / "doc-routing-r1"
        biased_root = CASES / "TC-HR03-T6-SUMMARY-BIASED" / "doc-routing-r1"
        unbiased = load_json(unbiased_root / "trial-prompt-input.json")
        biased = load_json(biased_root / "trial-prompt-input.json")
        self.assertNotEqual(
            unbiased["prior_implementation_record"],
            biased["prior_implementation_record"],
        )
        unbiased_without_record = dict(unbiased)
        biased_without_record = dict(biased)
        unbiased_without_record.pop("prior_implementation_record")
        biased_without_record.pop("prior_implementation_record")
        self.assertEqual(unbiased_without_record, biased_without_record)
        self.assertEqual(
            (unbiased_root / "private" / "seed.patch").read_bytes(),
            (biased_root / "private" / "seed.patch").read_bytes(),
        )

    def test_model_visible_task_does_not_select_review_route(self) -> None:
        for case_id in HR_CASES:
            trial = load_json(
                CASES / case_id / "doc-routing-r1" / "trial-prompt-input.json"
            )
            route_neutral_task = " ".join(
                value
                for key, value in trial.items()
                if key != "prior_implementation_record"
            )
            self.assertNotIn("reviewer", route_neutral_task.lower())
            self.assertNotIn("独立SA", route_neutral_task)

    def test_routing_profile_fixes_three_cases_n5_and_m24(self) -> None:
        profile = load_json(HR_PROFILE_ROUTING_R1)
        self.assertEqual({case["id"] for case in profile["cases"]}, set(HR_CASES))
        self.assertEqual(
            {case["revision"] for case in profile["cases"]},
            {"doc-routing-r1"},
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        commands = profile["comparison_conditions"]["executor_parameters"][
            "command_evidence_protocol"
        ]["required_command_groups_by_case"]
        self.assertEqual(set(commands), set(HR_CASES))
        self.assertEqual(len(commands["TC-HR01-MARKDOWN-BULLET-CLOSURE"]), 2)
        self.assertEqual(len(commands["TC-HR02-T6-SUMMARY-UNBIASED"]), 1)
        self.assertEqual(len(commands["TC-HR03-T6-SUMMARY-BIASED"]), 1)

    def test_candidate164_profile_changes_only_prompt_identity(self) -> None:
        baseline = load_json(HR_PROFILE_ROUTING_R1)
        candidate = load_json(C164_HR_PROFILE_ROUTING_R1)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-autonomous-review-admission-r1",
                "revision": "r1",
                "bundle_sha256": (
                    "f298549c52811872d79b778afb85dbe8c860e7b67faff4a451c239e45e34b099"
                ),
            },
        )

        baseline_without_identity = dict(baseline)
        candidate_without_identity = dict(candidate)
        baseline_without_identity.pop("profile_id")
        candidate_without_identity.pop("profile_id")
        baseline_without_identity.pop("prompt_set_identity")
        candidate_without_identity.pop("prompt_set_identity")
        self.assertEqual(candidate_without_identity, baseline_without_identity)


if __name__ == "__main__":
    unittest.main()

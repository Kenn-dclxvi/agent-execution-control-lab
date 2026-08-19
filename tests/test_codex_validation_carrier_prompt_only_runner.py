import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
RUNNER_PATH = TARGET_ROOT / "runtime/runner_prompt_only.py"
ARMS = ("p001", "p002", "p003")


def load_runner():
    spec = importlib.util.spec_from_file_location("codex_validation_carrier_prompt_only_runner_test", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CodexValidationCarrierPromptOnlyRunnerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = load_runner()

    def test_runner_contains_no_candidate_identity(self) -> None:
        source = RUNNER_PATH.read_text(encoding="utf-8")
        for value in ("P001", "P002", "P003", "p001-", "p002-", "p003-"):
            self.assertNotIn(value, source)

    def test_profiles_differ_only_in_identity_and_prompt(self) -> None:
        normalized = []
        for arm in ARMS:
            path = TARGET_ROOT / f"profiles/vcc6-{arm}-shared-runner-sol-medium-n1-r2.json"
            profile = load(path)
            self.runner.validate_profile(repository_root=ROOT, profile_path=path, target_path=TARGET_ROOT / "target.json")
            value = copy.deepcopy(profile)
            value.pop("profile_id")
            value.pop("dispatch_series_id")
            value.pop("prompt_set_identity")
            normalized.append(value)
        self.assertEqual(normalized[0], normalized[1])
        self.assertEqual(normalized[1], normalized[2])

    def test_all_preflights_are_fresh_and_bind_identical_execution_code(self) -> None:
        execution_code = []
        for arm in ARMS:
            path = TARGET_ROOT / f"plans/vcc6-{arm}-shared-runner-n1-preflight-r2.json"
            receipt, plan = self.runner.validate_preflight(
                repository_root=ROOT,
                receipt_path=path,
                observed_version="codex-cli 0.146.0",
            )
            self.assertEqual(plan["authorized_slot_count"], 6)
            self.assertEqual(plan["issued_slot_count"], 0)
            self.assertTrue(receipt["dispatch_allowed"])
            self.assertFalse(receipt["saved_result_reuse"])
            execution_code.append(receipt["execution_code"])
        self.assertEqual(execution_code[0], execution_code[1])
        self.assertEqual(execution_code[1], execution_code[2])

    def test_global_preflight_binds_exact_three_receipts(self) -> None:
        registration = load(TARGET_ROOT / "registrations/vcc6-p001-p002-p003-shared-runner-n1-preflight-registration-r2.json")
        self.assertTrue(registration["compatibility"]["prompt_identity_only"])
        self.assertTrue(registration["compatibility"]["same_execution_code"])
        self.assertFalse(registration["compatibility"]["saved_result_reuse"])
        self.assertEqual(registration["authorized_slot_count"], 18)
        self.assertEqual(registration["issued_slot_count"], 0)
        for label, arm in zip(("P001", "P002", "P003"), ARMS):
            for artifact in ("profile", "plan", "preflight"):
                reference = registration["arms"][label][artifact]
                self.assertEqual(sha256(ROOT / reference["path"]), reference["sha256"])
            receipt = load(ROOT / registration["arms"][label]["preflight"]["path"])
            self.assertEqual(receipt["receipt_sha256"], registration["arms"][label]["preflight"]["receipt_sha256"])

    def test_execution_gate_forbids_saved_result_reuse(self) -> None:
        gate = load(TARGET_ROOT / "registrations/vcc6-prompt-only-shared-runner-foundation-r1.json")
        self.assertEqual(gate["saved_result_reuse"], "forbidden_for_shared_runner_qualification")
        self.assertEqual(len(gate["allowed_prompt_set_identities"]), 3)
        self.assertEqual(gate["execution_code"]["prompt_only_runner"]["sha256"], sha256(RUNNER_PATH))

    def test_first_dispatch_is_preserved_as_external_failure(self) -> None:
        failure = load(TARGET_ROOT / "registrations/vcc6-p001-p002-p003-shared-runner-n1-issuance-failure-r1.json")
        recovery = load(TARGET_ROOT / "registrations/vcc6-heldout-r1-fixture-mode-recovery-receipt-r1.json")
        self.assertEqual(failure["external_failure_count"], 18)
        self.assertEqual(failure["model_process_started_count"], 0)
        self.assertEqual(failure["disposition"]["reuse"], "forbidden")
        self.assertEqual(recovery["recovery"]["mode_mismatches_after_recovery"], 0)

    def test_registered_n1_result_has_three_valid_arms_without_stability_claim(self) -> None:
        result = load(TARGET_ROOT / "results/vcc6-p001-p002-p003-shared-runner-n1-result-r1.json")
        self.assertEqual(set(result["arms"]), {"P001", "P002", "P003"})
        for arm in result["arms"].values():
            self.assertEqual(arm["summary"]["valid_results"], 6)
            self.assertEqual(arm["summary"]["quality_score_distribution"], {"4": 6})
        self.assertFalse(result["comparison_scope"]["n1_stability_claim"])


if __name__ == "__main__":
    unittest.main()

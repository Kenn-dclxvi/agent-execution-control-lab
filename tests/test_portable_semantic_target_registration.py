import hashlib
import json
from pathlib import Path
import subprocess

from scripts.export_prompt_bundle import verify_bundle
from scripts.compose_prompt import verify_bundle_binding


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "evaluations/targets/portable-instruction-semantic-conformance"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_registration_hashes_match_namespaced_artifacts() -> None:
    registration = load(TARGET / "registration.json")
    assert registration["state"] == {
        "target_registered": True,
        "profile_registered": False,
        "execution_entrypoint_enabled": False,
        "qualification_started": False,
        "formal_results": 0,
    }
    for relative, expected in registration["registered_artifacts"].items():
        assert sha256(TARGET / relative) == expected, relative


def test_registered_copies_match_bound_source_commit() -> None:
    registration = load(TARGET / "registration.json")
    commit = registration["source"]["commit"]
    pairs = {
        "docs/portable-instruction-semantic-conformance-heldout-r1/input-cases.json": "cases/heldout-r1/input-cases.json",
        "docs/portable-instruction-semantic-conformance-heldout-r1/input-cases.schema.json": "cases/heldout-r1/input-cases.schema.json",
        "docs/portable-instruction-semantic-conformance-heldout-r1/oracle.json": "cases/heldout-r1/oracle.json",
        "docs/portable-instruction-semantic-conformance-heldout-r1/oracle.schema.json": "cases/heldout-r1/oracle.schema.json",
        "docs/portable-instruction-semantic-conformance-heldout-r1/response.schema.json": "cases/heldout-r1/response.schema.json",
        "docs/portable-instruction-semantic-conformance-heldout-r1/freeze.json": "cases/heldout-r1/source-freeze.json",
        "docs/portable-instruction-semantic-conformance-heldout-r1/rating-contract.json": "rating-contracts/portable-instruction-semantic-exact-v1.json",
        "docs/portable-instruction-control-free-prompt-draft-r1/AGENTS.md.txt": "prompts/baselines/portable-semantic-a544769-control-free-r1/files/AGENTS.md.txt",
    }
    for source, registered in pairs.items():
        observed = subprocess.run(
            ["git", "show", f"{commit}:{source}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert observed == (TARGET / registered).read_bytes(), source


def test_set_is_exactly_the_registered_fourteen_cases() -> None:
    source = load(TARGET / "cases/heldout-r1/input-cases.json")
    evaluation_set = load(TARGET / "sets/heldout-r1/set.json")
    expected = [
        {"case_id": case["case_id"], "case_revision": case["case_revision"]}
        for case in source["cases"]
    ]
    assert evaluation_set["cases"] == expected
    assert len(expected) == 14


def test_control_free_bundle_is_registered_and_zero_byte() -> None:
    bundle = TARGET / "prompts/baselines/portable-semantic-a544769-control-free-r1"
    receipt = verify_bundle(bundle)
    assert receipt["prompt_identity"] == "portable-semantic-a544769-control-free-r1"
    assert receipt["files"][0]["sha256"] == hashlib.sha256(b"").hexdigest()
    assert (bundle / "files/AGENTS.md.txt").read_bytes() == b""


def test_full_agent_reference_and_candidate_bundles_are_registered() -> None:
    registration = load(TARGET / "prompts/full-agent-bundle-registration-r1.json")
    reference = TARGET / "prompts/baselines/portable-semantic-c147-full-agent-reference-r1"
    candidate = TARGET / "prompts/candidates/portable-semantic-c147-portable-full-agent-r1"
    reference_manifest = verify_bundle(reference)
    candidate_manifest = verify_bundle(candidate)

    assert reference_manifest["prompt_identity"] == registration["direct_parent"]["prompt_identity"]
    assert reference_manifest["bundle_sha256"] == registration["direct_parent"]["bundle_sha256"]
    assert candidate_manifest["prompt_identity"] == registration["candidate"]["prompt_identity"]
    assert candidate_manifest["bundle_sha256"] == registration["candidate"]["bundle_sha256"]
    for key in ("direct_parent", "candidate"):
        reference_record = registration[key]
        assert sha256(ROOT / reference_record["manifest_path"]) == reference_record["manifest_sha256"]

    source = ROOT / "prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/files/AGENTS.md.txt"
    assert (reference / "files/AGENTS.md.txt").read_bytes() == source.read_bytes()
    composition = ROOT / registration["composition_binding"]["composition_manifest_path"]
    assert sha256(composition) == registration["composition_binding"]["composition_manifest_sha256"]
    receipt = verify_bundle_binding(composition, candidate)
    assert receipt["binding_status"] == "verified"
    assert receipt["output_sha256"] == registration["candidate"]["content_sha256"]
    assert registration["state"] == {
        "candidate_bundle_registered": True,
        "candidate_evaluation_started": False,
        "candidate_profile_created": False,
        "reference_bundle_registered": True,
        "reference_evaluation_started": False,
        "reference_profile_created": False,
        "root_only_bundle_registered": False,
    }


def test_control_free_profile_history_and_formal_result_are_preserved() -> None:
    documents = [load(path) for path in (TARGET / "profiles").glob("*.json")]
    profiles = [item for item in documents if item.get("schema_version") == "portable-instruction-semantic-profile/v1"]
    registrations = [
        item
        for item in documents
        if item.get("schema_version") == "portable-instruction-semantic-profile-registration/v1"
    ]
    assert len(profiles) == 16
    assert len(registrations) == 16
    control_profiles = [profile for profile in profiles if "control-free" in profile["profile_id"]]
    assert {profile["profile_id"][-2:] for profile in control_profiles} == {"r1", "r2", "r3", "r4"}
    assert all(profile["lifecycle_state"] == "registered_not_qualified" for profile in profiles)
    latest_registration = next(item for item in registrations if item["registration_id"].endswith("r4"))
    assert latest_registration["state"]["adapter_execution_entrypoint_enabled"] is True
    for key in ("profile", "adapter"):
        reference = latest_registration[key]
        assert sha256(ROOT / reference["path"]) == reference["sha256"]
    historical_preflight = load(
        TARGET / "plans/portable-semantic-control-free-heldout-r1-n1-preflight-r4.json"
    )
    assert historical_preflight["execution_code"]["runner"] == latest_registration["runner"]
    assert historical_preflight["execution_code"]["core_adapter"] == latest_registration["adapter"]
    candidate_registration = next(
        item
        for item in registrations
        if item["registration_id"].endswith("portable-full-agent-profile-registration-r1")
    )
    assert candidate_registration["state"]["preflight_ready"] is True
    for key in ("profile", "adapter", "runner", "prompt_bundle_registration"):
        reference = candidate_registration[key]
        assert sha256(ROOT / reference["path"]) == reference["sha256"]
    assert sorted(path.name for path in (TARGET / "results").glob("*.json")) == [
        "portable-semantic-c147-full-agent-reference-heldout-r1-n1-qualification-r1.json",
        "portable-semantic-c147-portable-full-agent-heldout-r1-n1-qualification-r1.json",
        "portable-semantic-c147-portable-full-agent-heldout-r3-n1-qualification-r1.json",
        "portable-semantic-c147-portable-full-agent-heldout-r3-n20-qualification-r1.json",
        "portable-semantic-c147-portable-full-agent-heldout-r3-n5-qualification-r1.json",
        "portable-semantic-c147-reference-heldout-r2-n1-qualification-r1.json",
        "portable-semantic-c147-reference-heldout-r3-n1-qualification-r1.json",
        "portable-semantic-c147-reference-heldout-r3-n20-qualification-r1.json",
        "portable-semantic-c147-reference-heldout-r3-n5-qualification-r1.json",
        "portable-semantic-c147-reference-transition-calibration-r2-n1-qualification-r1.json",
        "portable-semantic-c147-reference-transition-calibration-r3-n1-qualification-r1.json",
        "portable-semantic-c147-reference-transition-calibration-r4-n1-qualification-r1.json",
        "portable-semantic-control-free-heldout-r1-n1-qualification-r4.json",
    ]
    assert list((TARGET / "results").glob("*.md")) == [TARGET / "results/README.md"]


def test_qualification_plan_and_preflight_authorize_fourteen_but_issue_zero() -> None:
    plan = load(TARGET / "plans/portable-semantic-control-free-heldout-r1-n1-dispatch-r1.json")
    preflight = load(TARGET / "plans/portable-semantic-control-free-heldout-r1-n1-preflight-r1.json")
    expected_slots = [f"PIC-H{number:02d}-i001" for number in range(1, 15)]
    assert [slot["slot_id"] for slot in plan["slots"]] == expected_slots
    assert plan["authorized_slot_count"] == 14
    assert plan["issued_slot_count"] == 0
    assert preflight["authorized_slots"] == plan["slots"]
    assert preflight["authorized_slot_count"] == 14
    assert preflight["issued_slot_count"] == 0
    assert preflight["dispatch_allowed"] is True
    assert sha256(ROOT / preflight["plan"]["path"]) == preflight["plan"]["sha256"]
    assert preflight["preflight_id"].endswith("r1")
    failure = load(TARGET / "plans/portable-semantic-control-free-heldout-r1-n1-attempt-r1-external-failure.json")
    assert failure["issued_slot_count"] == 14
    assert failure["valid_result_count"] == 0
    assert failure["classification"] == "profile_transport_incompatible"


def test_portable_candidate_preflight_authorizes_only_candidate_series() -> None:
    plan = load(
        TARGET / "plans/portable-semantic-c147-portable-full-agent-heldout-r1-n1-dispatch-r1.json"
    )
    preflight = load(
        TARGET / "plans/portable-semantic-c147-portable-full-agent-heldout-r1-n1-preflight-r1.json"
    )
    assert plan["plan_id"] == "portable-semantic-c147-portable-full-agent-heldout-r1-n1-dispatch-r1"
    assert plan["prompt_set_identity"] == {
        "name": "portable-semantic-c147-portable-full-agent-r1",
        "revision": "r1",
        "sha256": "6152e6ca546ef778eb59ad6ff0fe6883748ece469309ff627945777978e4faf0",
    }
    assert plan["authorized_slot_count"] == 14
    assert plan["issued_slot_count"] == 0
    assert preflight["plan"]["plan_id"] == plan["plan_id"]
    assert preflight["authorized_slots"] == plan["slots"]
    assert preflight["dispatch_allowed"] is True
    assert preflight["issued_slot_count"] == 0
    for key in ("core_adapter", "runner"):
        reference = preflight["execution_code"][key]
        assert sha256(ROOT / reference["path"]) == reference["sha256"]


def test_c147_reference_preflight_qualifies_the_set_before_portable_interpretation() -> None:
    plan = load(
        TARGET / "plans/portable-semantic-c147-full-agent-reference-heldout-r1-n1-dispatch-r1.json"
    )
    preflight = load(
        TARGET / "plans/portable-semantic-c147-full-agent-reference-heldout-r1-n1-preflight-r1.json"
    )
    registration = load(TARGET / "profiles/profile-registration-c147-reference-r1.json")
    assert plan["prompt_set_identity"] == {
        "name": "portable-semantic-c147-full-agent-reference-r1",
        "revision": "r1",
        "sha256": "d330421521b231d6029e69e8cd6d4e175fb46b06254e80b3d2f4d8f8f3a55d9f",
    }
    assert plan["authorized_slot_count"] == 14
    assert plan["issued_slot_count"] == 0
    assert preflight["authorized_slots"] == plan["slots"]
    assert preflight["dispatch_allowed"] is True
    assert preflight["issued_slot_count"] == 0
    assert registration["state"]["reference_profile_created"] is True
    assert registration["state"]["preflight_ready"] is True
    for key in ("profile", "plan", "preflight", "adapter", "runner", "prompt_bundle_registration"):
        reference = registration[key]
        assert sha256(ROOT / reference["path"]) == reference["sha256"]


def test_transition_contract_r2_is_reference_calibration_only() -> None:
    profile = load(
        TARGET
        / "profiles/portable-semantic-c147-reference-transition-calibration-codex-cli0146-sol-medium-r2-n1-r1.json"
    )
    registration = load(
        TARGET / "profiles/profile-registration-c147-reference-transition-calibration-r2.json"
    )
    plan = load(
        TARGET / "plans/portable-semantic-c147-reference-transition-calibration-r2-n1-dispatch-r1.json"
    )
    preflight = load(
        TARGET / "plans/portable-semantic-c147-reference-transition-calibration-r2-n1-preflight-r1.json"
    )
    assert profile["prompt_set_identity"]["name"] == "portable-semantic-c147-full-agent-reference-r1"
    assert profile["task_spec_ref"]["revision"] == "semantic-single-json-r2"
    assert profile["evaluation_set_ref"]["set_id"] == "portable-instruction-semantic-reference-calibration-r2"
    assert registration["state"]["reference_calibration_only"] is True
    assert registration["state"]["portable_candidate_heldout"] is False
    assert plan["authorized_slot_count"] == 14
    assert plan["issued_slot_count"] == 0
    assert preflight["authorized_slots"] == plan["slots"]
    assert preflight["dispatch_allowed"] is True
    for key in ("profile", "plan", "preflight", "adapter", "runner", "prompt_bundle_registration"):
        reference = registration[key]
        assert sha256(ROOT / reference["path"]) == reference["sha256"]


def test_transition_contract_r4_qualifies_c147_without_becoming_portable_heldout() -> None:
    profile = load(
        TARGET
        / "profiles/portable-semantic-c147-reference-transition-calibration-codex-cli0146-sol-medium-r4-n1-r1.json"
    )
    registration = load(
        TARGET / "profiles/profile-registration-c147-reference-transition-calibration-r4.json"
    )
    result = load(
        TARGET
        / "results/portable-semantic-c147-reference-transition-calibration-r4-n1-qualification-r1.json"
    )
    assert profile["task_spec_ref"]["revision"] == "semantic-single-json-r4"
    assert registration["state"]["reference_calibration_only"] is True
    assert registration["state"]["portable_candidate_heldout"] is False
    assert result["summary"]["valid_results"] == 14
    assert result["summary"]["score4_results"] == 14
    assert result["summary"]["mechanism_passed_results"] == 14
    assert result["qualification"]["quality_gate"] == "passed"


def test_target_registers_dispatch_root_and_plan_limited_runner() -> None:
    target = load(TARGET / "target.json")
    assert target["artifact_roots"]["dispatch_plans"].endswith("/plans")
    assert "scripts/run_semantic_protocol_qualification.py" in target["target_specific_modules"]


def test_control_free_qualification_passes_measurement_not_adoption() -> None:
    result = load(TARGET / "results/portable-semantic-control-free-heldout-r1-n1-qualification-r4.json")
    assert result["summary"]["valid_results"] == 14
    assert result["summary"]["schema_valid_results"] == 14
    assert result["summary"]["score4_results"] == 5
    assert result["summary"]["mechanism_passed_results"] == 5
    assert result["qualification"] == {
        "measurement_gate": "passed",
        "quality_gate": "descriptive_not_an_admission_gate",
        "adoption": "not_decided",
        "release": "not_decided",
        "runtime_projection": "not_authorized",
    }


def test_portable_candidate_quality_failure_does_not_authorize_reference() -> None:
    result = load(
        TARGET / "results/portable-semantic-c147-portable-full-agent-heldout-r1-n1-qualification-r1.json"
    )
    assert result["summary"]["valid_results"] == 14
    assert result["summary"]["schema_valid_results"] == 14
    assert result["summary"]["score4_results"] == 7
    assert result["summary"]["mechanism_passed_results"] == 7
    assert result["qualification"]["quality_gate"] == "failed"
    assert result["qualification"]["quality_gate_contract"] == "exact_all_14_score4"
    assert result["qualification"]["comparison_reference"] == "not_authorized"


def test_c147_reference_failure_disqualifies_semantic_set_for_equivalence() -> None:
    result = load(
        TARGET / "results/portable-semantic-c147-full-agent-reference-heldout-r1-n1-qualification-r1.json"
    )
    assert result["summary"]["valid_results"] == 14
    assert result["summary"]["schema_valid_results"] == 14
    assert result["summary"]["score4_results"] == 6
    assert result["summary"]["mechanism_passed_results"] == 6
    assert result["qualification"]["quality_gate"] == "failed"
    assert result["qualification"]["quality_gate_contract"] == "exact_all_14_score4"

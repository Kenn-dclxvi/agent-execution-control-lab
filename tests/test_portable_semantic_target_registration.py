import hashlib
import json
from pathlib import Path
import subprocess

from scripts.export_prompt_bundle import verify_bundle


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


def test_profile_is_registered_but_result_execution_has_not_started() -> None:
    documents = [load(path) for path in (TARGET / "profiles").glob("*.json")]
    profiles = [item for item in documents if item.get("schema_version") == "portable-instruction-semantic-profile/v1"]
    registrations = [
        item
        for item in documents
        if item.get("schema_version") == "portable-instruction-semantic-profile-registration/v1"
    ]
    assert len(profiles) == 1
    assert len(registrations) == 1
    assert profiles[0]["lifecycle_state"] == "registered_not_qualified"
    assert registrations[0]["state"]["adapter_execution_entrypoint_enabled"] is False
    for key in ("profile", "adapter"):
        reference = registrations[0][key]
        assert sha256(ROOT / reference["path"]) == reference["sha256"]
    assert list((TARGET / "results").glob("*.json")) == []
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
    for reference in preflight["execution_code"].values():
        assert sha256(ROOT / reference["path"]) == reference["sha256"]


def test_target_registers_dispatch_root_and_plan_limited_runner() -> None:
    target = load(TARGET / "target.json")
    assert target["artifact_roots"]["dispatch_plans"].endswith("/plans")
    assert "scripts/run_semantic_protocol_qualification.py" in target["target_specific_modules"]

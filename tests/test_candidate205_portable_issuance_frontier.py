from pathlib import Path
import json

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C147 = ROOT / "prompts" / "releases" / "the-caption-3ce91a4-result-effect-scope-release-r1"
C205 = ROOT / "prompts" / "candidates" / "the-caption-3ce91a4-portable-issuance-frontier-r1"
DESIGN = ROOT / "docs" / "post-candidate204-portable-issuance-frontier-design.md"
DIRECTION = ROOT / "docs" / "post-candidate204-portable-issuance-frontier-direction-review.md"
PROFILE = ROOT / "evaluations" / "profiles" / "candidate205-portable-issuance-frontier-v14-reasoning-medium-f01-f02-f03-global-m24-n5-cli0146-r1.json"
C147_PROFILE = ROOT / "evaluations" / "profiles" / "candidate147-result-effect-scope-v14-reasoning-medium-f01-f02-f03-global-m24-n5-cli0146-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations" / "results" / "candidate205-portable-issuance-frontier-f01-f02-f03-n5-mechanism-audit-r1.json"


def _core() -> str:
    text = DESIGN.read_text()
    return text.split("<!-- PORTABLE_ISSUANCE_CORE_BEGIN -->", 1)[1].split(
        "<!-- PORTABLE_ISSUANCE_CORE_END -->", 1
    )[0].strip()


def test_candidate205_bundle_identity_is_valid() -> None:
    manifest = verify_bundle(C205)
    assert manifest["prompt_identity"] == "the-caption-3ce91a4-portable-issuance-frontier-r1"
    assert manifest["bundle_sha256"] == (
        "94cd1c2bdf12da74d8700daa95d15f98e70e6578fbca7a0f96b5ee6108827a53"
    )
    assert manifest["content_relation"] == {
        "changed_targets": ["AGENTS.md"],
        "kind": "direct_child_full_bundle",
        "source_prompt_identity": "the-caption-3ce91a4-result-effect-scope-r1",
    }


def test_candidate205_root_matches_design_and_has_issuance_owner() -> None:
    text = (C205 / "files" / "AGENTS.md.txt").read_text()
    assert text == "# THE-CAPTION execution control\n\n" + _core() + "\n"
    labels = [line.split(":", 1)[0][2:] for line in text.splitlines() if line.startswith("- ")]
    assert labels == [
        "OUTCOME",
        "PRODUCER",
        "INPUT",
        "INVOCATION",
        "ISSUANCE",
        "RESULT_ADMISSION",
        "RESULT_EFFECT",
        "IMPLEMENTATION",
        "COMPLETION",
        "VALIDATION_PLAN",
        "VALIDATION_CLOSURE",
        "METHOD",
        "RECOVERY",
    ]
    assert "eligible -> issued / unavailable" in DESIGN.read_text()
    assert "frontierがclosedになる前" in text


def test_candidate205_excludes_review_and_runtime_surface_terms() -> None:
    text = (C205 / "files" / "AGENTS.md.txt").read_text()
    for fragment in (
        "review",
        "Codex",
        "root",
        "worker",
        "fork_turns",
        "FINAL_ANSWER",
        "runtime_spawn_result",
        "custom exec",
        "exec_command",
        "cell ID",
        "model step",
        "modelへ戻らず",
        "environment_recovery_max",
    ):
        assert fragment not in text


def test_candidate205_only_changes_root_agents() -> None:
    source = verify_bundle(C147)
    candidate = verify_bundle(C205)
    source_entries = {entry["target"]: entry for entry in source["files"]}
    candidate_entries = {entry["target"]: entry for entry in candidate["files"]}
    assert source_entries.keys() == candidate_entries.keys()
    assert [target for target in source_entries if source_entries[target] != candidate_entries[target]] == [
        "AGENTS.md"
    ]
    assert (C205 / "files" / "prompts" / "review.md").read_bytes() == b""


def test_candidate205_direction_permission_is_withdrawn() -> None:
    text = DIRECTION.read_text()
    for fragment in (
        "superseded",
        "prior_M3_permission_withdrawn",
        "C147_functional_decomposition_reopened",
        "c147-functional-decomposition-reanalysis.md",
        "targeted_slots_issued_0",
    ):
        assert fragment in text


def test_candidate205_profile_only_changes_prompt_identity() -> None:
    candidate = json.loads(PROFILE.read_text())
    reference = json.loads(C147_PROFILE.read_text())
    for key in (
        "cases",
        "comparison_conditions",
        "evaluation_set",
        "iterations",
        "execution",
        "scope",
    ):
        assert candidate[key] == reference[key]
    assert candidate["prompt_set_identity"] == {
        "bundle_sha256": "94cd1c2bdf12da74d8700daa95d15f98e70e6578fbca7a0f96b5ee6108827a53",
        "name": "the-caption-3ce91a4-portable-issuance-frontier-r1",
        "revision": "r1",
    }


def test_candidate205_mechanism_audit_uses_command_event_order() -> None:
    audit = json.loads(MECHANISM_AUDIT.read_text())
    failure = audit["mechanism_failure"]
    assert audit["schema_version"].endswith("/v2")
    assert failure["isolated_identity_run_count"] == 15
    assert failure["coissued_identity_and_read_run_count"] == 0
    assert failure["previous_agent_message_boundary_false_positive_run_id"] == (
        "c62f31d690124e26833046aa99e6ce22"
    )
    assert "terminalになる前" in failure["event_order_oracle"]

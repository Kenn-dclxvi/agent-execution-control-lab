from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C147 = ROOT / "prompts" / "releases" / "the-caption-3ce91a4-result-effect-scope-release-r1"
C204 = ROOT / "prompts" / "candidates" / "the-caption-3ce91a4-portable-execution-core-r1"
DESIGN = ROOT / "docs" / "c147-review-free-portable-core-design.md"
PROFILE = ROOT / "evaluations" / "profiles" / "candidate204-portable-execution-core-v14-reasoning-medium-f01-f02-f03-global-m24-n5-cli0146-r1.json"
C147_PROFILE = ROOT / "evaluations" / "profiles" / "candidate147-result-effect-scope-v14-reasoning-medium-f01-f02-f03-global-m24-n5-cli0146-r1.json"


def _portable_core() -> str:
    text = DESIGN.read_text()
    return text.split("<!-- PORTABLE_CORE_BEGIN -->", 1)[1].split(
        "<!-- PORTABLE_CORE_END -->", 1
    )[0].strip()


def test_candidate204_bundle_identity_is_valid() -> None:
    manifest = verify_bundle(C204)
    assert manifest["prompt_identity"] == "the-caption-3ce91a4-portable-execution-core-r1"
    assert manifest["bundle_sha256"] == (
        "d9c90d877e97479d95e5be51306111b221dd7e53c5c921e14599fb39df1faf5e"
    )
    assert manifest["content_relation"] == {
        "changed_targets": ["AGENTS.md"],
        "kind": "direct_child_full_bundle",
        "source_prompt_identity": "the-caption-3ce91a4-result-effect-scope-r1",
    }


def test_candidate204_root_is_exact_design_core() -> None:
    root_text = (C204 / "files" / "AGENTS.md.txt").read_text()
    assert root_text == "# THE-CAPTION execution control\n\n" + _portable_core() + "\n"


def test_candidate204_has_twelve_labels_and_no_runtime_surface_terms() -> None:
    text = (C204 / "files" / "AGENTS.md.txt").read_text()
    labels = (
        "OUTCOME",
        "PRODUCER",
        "INPUT",
        "INVOCATION",
        "RESULT_ADMISSION",
        "RESULT_EFFECT",
        "IMPLEMENTATION",
        "COMPLETION",
        "VALIDATION_PLAN",
        "VALIDATION_CLOSURE",
        "METHOD",
        "RECOVERY",
    )
    assert [line.split(":", 1)[0][2:] for line in text.splitlines() if line.startswith("- ")] == list(labels)
    forbidden = (
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
    )
    for fragment in forbidden:
        assert fragment not in text


def test_candidate204_only_changes_root_agents() -> None:
    c147_manifest = verify_bundle(C147)
    c204_manifest = verify_bundle(C204)
    c147_entries = {entry["target"]: entry for entry in c147_manifest["files"]}
    c204_entries = {entry["target"]: entry for entry in c204_manifest["files"]}
    assert c147_entries.keys() == c204_entries.keys()
    changed = [target for target in c147_entries if c147_entries[target] != c204_entries[target]]
    assert changed == ["AGENTS.md"]
    assert (C204 / "files" / "prompts" / "review.md").read_bytes() == b""


def test_candidate204_targeted_profile_only_changes_prompt_identity() -> None:
    import json

    candidate = json.loads(PROFILE.read_text())
    reference = json.loads(C147_PROFILE.read_text())
    assert candidate["cases"] == reference["cases"]
    assert candidate["comparison_conditions"] == reference["comparison_conditions"]
    assert candidate["evaluation_set"] == reference["evaluation_set"]
    assert candidate["iterations"] == reference["iterations"]
    assert candidate["execution"] == reference["execution"]
    assert candidate["scope"] == reference["scope"]
    assert candidate["prompt_set_identity"] == {
        "bundle_sha256": "d9c90d877e97479d95e5be51306111b221dd7e53c5c921e14599fb39df1faf5e",
        "name": "the-caption-3ce91a4-portable-execution-core-r1",
        "revision": "r1",
    }

import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "evaluations/targets/schemas/evaluation-target-v2.schema.json"
DRAFT = ROOT / "docs/portable-instruction-semantic-target-draft.json"
FORMAL = ROOT / "evaluations/targets/portable-instruction-semantic-conformance/target.json"
RESPONSE_SCHEMA = ROOT / "docs/portable-instruction-semantic-conformance-heldout-r1/response.schema.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_semantic_protocol_target_draft_validates_as_v2() -> None:
    descriptor = load(DRAFT)
    jsonschema.Draft202012Validator(load(SCHEMA)).validate(descriptor)
    assert descriptor["target_kind"] == "semantic_protocol"
    assert descriptor["target_subject"]["kind"] == "semantic_protocol"
    assert descriptor["executor_binding"] == "profile"


def test_semantic_protocol_subject_is_not_disguised_as_repository() -> None:
    descriptor = load(DRAFT)

    def keys(value: object) -> set[str]:
        if isinstance(value, dict):
            return set(value) | set().union(*(keys(item) for item in value.values()))
        if isinstance(value, list):
            return set().union(*(keys(item) for item in value))
        return set()

    assert "target_repository" not in descriptor
    assert "target_repository_ref" not in keys(descriptor)
    assert "commit" not in descriptor["target_subject"]
    assert "tree" not in descriptor["target_subject"]


def test_subject_hash_matches_fixed_response_schema() -> None:
    import hashlib

    descriptor = load(DRAFT)
    observed = hashlib.sha256(RESPONSE_SCHEMA.read_bytes()).hexdigest()
    assert descriptor["target_subject"]["response_schema_sha256"] == observed


def test_formal_target_preserves_draft_subject_without_repository_ref() -> None:
    draft = load(DRAFT)
    formal = load(FORMAL)
    jsonschema.Draft202012Validator(load(SCHEMA)).validate(formal)
    assert formal["target_id"] == draft["target_id"]
    assert formal["target_subject"] == {
        **draft["target_subject"],
        "subject_authority": formal["target_subject"]["subject_authority"],
    }
    assert formal["current_rating_contract"] == "portable-instruction-semantic-exact-v1"
    assert f"`{formal['target_id']}`" in (ROOT / "evaluations/targets/README.md").read_text(encoding="utf-8")


def test_existing_v1_descriptors_remain_v1_and_repository_bound() -> None:
    for path in sorted((ROOT / "evaluations/targets").glob("*/target.json")):
        descriptor = load(path)
        if path == FORMAL:
            assert descriptor["schema_version"] == "the-caption-prompt.evaluation-target/v2"
            assert "target_repository" not in descriptor
            continue
        assert descriptor["schema_version"] == "the-caption-prompt.evaluation-target/v1"
        assert "target_repository" in descriptor

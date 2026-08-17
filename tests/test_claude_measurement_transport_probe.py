import hashlib
import json
from pathlib import Path

from scripts.claude_measurement_transport_probe import (
    secret_marker_names,
    terminal_projection,
    validate_ticket,
    write_private,
)


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts/claude_measurement_transport_probe.py"
FIXED_TICKET = ROOT / "docs/claude-code-2.1.220-measurement-transport-probe-r2-ticket.json"
FIXED_RECEIPT = ROOT / "docs/claude-code-2.1.220-measurement-transport-probe-r2-receipt.json"


def ticket() -> dict:
    return {
        "schema_version": "claude-measurement-transport-ticket/v1",
        "probe_id": "claude-measurement-transport-r2",
        "expected_cli_version": "2.1.220 (Claude Code)",
        "executable": "/Users/kenn/.local/bin/claude",
        "arguments": ["--print"],
        "expected_structured_output": {"probe_status": "ok", "nonce": "test"},
        "harness_path": str(HARNESS),
        "harness_sha256": hashlib.sha256(HARNESS.read_bytes()).hexdigest(),
        "attempts": 1,
        "timeout_seconds": 120,
    }


def test_validate_ticket_accepts_exact_harness_identity(tmp_path: Path) -> None:
    ticket_path = tmp_path / "ticket.json"
    ticket_path.write_text(json.dumps(ticket()), encoding="utf-8")
    assert validate_ticket(ticket(), ticket_path) == []


def test_fixed_ticket_is_bound_to_current_harness() -> None:
    value = json.loads(FIXED_TICKET.read_text(encoding="utf-8"))
    assert validate_ticket(value, FIXED_TICKET) == []
    assert value["attempts"] == 1
    assert value["arguments"].count("portable-measurement-transport-20260817-r2") == 0
    assert "portable-measurement-transport-20260817-r2" in value["arguments"][-1]


def test_fixed_receipt_preserves_transport_boundary_without_formal_tokens() -> None:
    receipt = json.loads(FIXED_RECEIPT.read_text(encoding="utf-8"))
    ticket_value = json.loads(FIXED_TICKET.read_text(encoding="utf-8"))
    assert receipt["status"] == "transport_probe_observed"
    assert receipt["model_invocations"] == ticket_value["attempts"] == 1
    assert receipt["identity"]["harness_sha256"] == ticket_value["harness_sha256"]
    assert all(receipt["admission_checks"].values())
    assert receipt["raw_evidence"]["stdout"]["mode"] == "0600"
    assert receipt["raw_evidence"]["stderr"]["mode"] == "0600"
    assert receipt["raw_evidence"]["secret_marker_matches"] == []
    assert receipt["boundaries"]["total_tokens_admitted"] is False
    assert "total_tokens" not in receipt["terminal"]
    assert "total_tokens" not in receipt["terminal"]["usage"]
    assert all("total_tokens" not in usage for usage in receipt["terminal"]["model_usage"].values())


def test_validate_ticket_rejects_hash_or_attempt_drift(tmp_path: Path) -> None:
    value = ticket()
    value["harness_sha256"] = "0" * 64
    value["attempts"] = 2
    errors = validate_ticket(value, tmp_path / "ticket.json")
    assert "harness_sha256" in errors
    assert "attempts" in errors


def test_write_private_uses_mode_0600(tmp_path: Path) -> None:
    target = tmp_path / "stdout.raw"
    write_private(target, b"ok")
    assert target.read_bytes() == b"ok"
    assert target.stat().st_mode & 0o777 == 0o600


def test_secret_scan_reports_marker_names_without_raw_output() -> None:
    assert secret_marker_names(b"safe", b"also safe") == []
    assert secret_marker_names(b"Authorization: hidden") == ["Authorization:"]


def test_terminal_projection_excludes_unapproved_fields() -> None:
    projected = terminal_projection(
        {
            "structured_output": {"probe_status": "ok"},
            "usage": {"input_tokens": 1},
            "modelUsage": {"model": {"input_tokens": 1}},
            "session_id": "session",
            "uuid": "terminal",
            "terminal_reason": "completed",
            "result": "raw response",
            "unapproved": "secret-like-value",
        }
    )
    assert "result" not in projected
    assert "unapproved" not in projected
    assert projected["session_id"] == "session"

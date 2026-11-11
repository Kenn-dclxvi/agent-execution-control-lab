"""Antigravityの一次ストリームを照合する。未取得の使用量は補完しない。"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

try:
    from usage_components import components_document, empty_buckets
except ModuleNotFoundError:
    from scripts.usage_components import components_document, empty_buckets


class AntigravityEvidenceError(ValueError):
    pass


USAGE_FIELDS = (
    "input_tokens", "output_tokens", "thinking_tokens", "cache_read_tokens", "total_tokens"
)
COMMAND_EVIDENCE_SCHEMA_VERSION = "the-caption-prompt.antigravity-command-evidence/v1"
TOKEN_ACCOUNTING = {
    "scope": "all_agents",
    "revision": "antigravity-v1",
    "source": "antigravity_155_database_model_usage_reconciled_with_transcripts_and_root_stream",
}


def parse_stream(raw: bytes) -> dict[str, Any]:
    try:
        events = [json.loads(line) for line in raw.splitlines() if line.strip()]
    except (ValueError, UnicodeError) as exc:
        raise AntigravityEvidenceError("構造化ストリームが破損しています") from exc
    if not events or any(not isinstance(e, dict) for e in events):
        raise AntigravityEvidenceError("構造化ストリームがありません")
    inits = [e for e in events if e.get("event") == "init"]
    results = [e for e in events if e.get("event") == "result"]
    if len(inits) != 1 or len(results) != 1 or events[0] != inits[0] or events[-1] != results[0]:
        raise AntigravityEvidenceError("開始・終了記録が一意ではありません")
    session = inits[0].get("conversation_id")
    result = results[0].get("result")
    if not session or not isinstance(result, dict) or result.get("conversation_id") != session:
        raise AntigravityEvidenceError("開始・終了の会話識別子が一致しません")
    steps = {}
    children = set()
    for event in events:
        if event.get("event") != "step_update":
            continue
        step = event.get("step_update")
        if not isinstance(step, dict):
            raise AntigravityEvidenceError("ステップの記録が不正です")
        child_info = step.get("subagent_info") or {}
        for child in child_info.get("subagents", []):
            child_id = child.get("conversation_id")
            if not isinstance(child_id, str) or not child_id:
                raise AntigravityEvidenceError("子エージェントの識別子がありません")
            children.add(child_id)
        if step.get("state") != "DONE":
            continue
        index = step.get("step_index")
        owner = step.get("conversation_id")
        if type(index) is not int or index < 0 or not isinstance(owner, str) or not owner:
            raise AntigravityEvidenceError("ステップの識別子が不正です")
        key = (owner, index)
        if key in steps and steps[key] != step:
            raise AntigravityEvidenceError("同じ完了ステップの記録が競合しています")
        steps[key] = step
    return {"init": inits[0]["init"], "session_id": session, "result": result,
            "steps": list(steps.values()), "children": sorted(children)}


def checked_usage(value: Any) -> dict[str, int]:
    if not isinstance(value, dict) or any(type(value.get(k)) is not int or value[k] < 0 for k in USAGE_FIELDS):
        raise AntigravityEvidenceError("使用量の内訳が欠落しています")
    # CLI 1.5.5のtotalはキャッシュ読み取りを除く。thinkingはoutputの内数。
    if value["input_tokens"] + value["output_tokens"] != value["total_tokens"]:
        raise AntigravityEvidenceError("使用量の合計がCLIの契約と一致しません")
    if value["thinking_tokens"] > value["output_tokens"]:
        raise AntigravityEvidenceError("思考トークンが出力トークンを超えています")
    return {k: value[k] for k in USAGE_FIELDS}


def collect_usage(stream: dict[str, Any], model: str) -> dict[str, Any]:
    if stream["init"].get("model") != model:
        raise AntigravityEvidenceError("固定モデルと開始記録が一致しません")
    # 子の一次記録の取得経路を確認するまでは、親だけの合計を全体と呼ばない。
    if stream["children"]:
        raise AntigravityEvidenceError("子エージェントの一次使用量・モデル別内訳の照合が未対応です")
    if any(s["conversation_id"] != stream["session_id"] for s in stream["steps"]):
        raise AntigravityEvidenceError("未照合の別会話が含まれています")
    reported = checked_usage(stream["result"].get("usage"))
    totals = dict.fromkeys(USAGE_FIELDS, 0)
    count = 0
    for step in stream["steps"]:
        if step.get("usage") is None:
            if step.get("step_type") in {"agent_response", "checkpoint"}:
                raise AntigravityEvidenceError("モデル実行ステップに使用量がありません")
            continue
        usage = checked_usage(step["usage"])
        for key in USAGE_FIELDS:
            totals[key] += usage[key]
        count += 1
    if not count or totals != reported:
        raise AntigravityEvidenceError("ステップ別使用量と終了時の使用量が一致しません")
    buckets = empty_buckets()
    buckets.update(uncached_input=totals["input_tokens"], cache_read=totals["cache_read_tokens"], output=totals["output_tokens"])
    components = components_document({model: {"standard": buckets}}, "antigravity")
    return {"schema_version": "the-caption-prompt.antigravity-usage/v1", "token_accounting": TOKEN_ACCOUNTING,
            "session_id": stream["session_id"], "response_count": count,
            "cli_reported_usage": reported, "all_agent_total_tokens": components["total_tokens"],
            "usage_components": components}


def collect_commands(stream: dict[str, Any], run_id: str) -> dict[str, Any]:
    if stream["children"]:
        raise AntigravityEvidenceError("子エージェントのコマンド証跡の照合が未対応です")
    attempted, successful, failed, violations = [], [], [], []
    for step in stream["steps"]:
        if step.get("tool_name") != "run_command":
            continue
        info = step.get("tool_info") or {}
        command = (info.get("parameters") or {}).get("CommandLine")
        if not isinstance(command, str) or not command:
            raise AntigravityEvidenceError("コマンド呼び出しの引数がありません")
        item = {"actor": "root", "agent_id": None, "tool_use_id": str(step["step_index"]),
                "source": "antigravity_stream_tool_result", "command": command}
        attempted.append(item)
        # ツール自身が付けた先頭の終了記録だけを読む。コマンド出力中の同文は採用しない。
        output = info.get("output", "")
        match = re.match(r"\ACreated At: [^\n]+\nCompleted At: [^\n]+\nCommand exited with code (-?\d+)\.\n", output)
        if match is None:
            violations.append({**item, "reason_code": "missing_machine_bound_exit_code"})
            continue
        code = int(match[1])
        (successful if code == 0 else failed).append({**item, "exit_code": code})
    return {"schema_version": COMMAND_EVIDENCE_SCHEMA_VERSION, "run_id": run_id,
            "session_id": stream["session_id"], "session_count": 1,
            "attempted_commands": attempted, "attempted_command_count": len(attempted),
            "successful_commands": successful, "successful_command_count": len(successful),
            "failed_commands": failed, "failed_command_count": len(failed),
            "protocol_violations": violations, "protocol_violation_count": len(violations)}


def wire_fields(raw: bytes) -> dict[int, list[Any]]:
    """固定したCLI 1.5.5のSQLite内のprotobufを読む。未知のwire型は拒否する。"""
    fields: dict[int, list[Any]] = {}
    position = 0

    def varint() -> int:
        nonlocal position
        number = 0
        for shift in range(0, 70, 7):
            if position >= len(raw):
                raise AntigravityEvidenceError("protobufの整数が途切れています")
            byte = raw[position]
            position += 1
            number |= (byte & 127) << shift
            if byte < 128:
                return number
        raise AntigravityEvidenceError("protobufの整数が長すぎます")

    while position < len(raw):
        tag = varint()
        number, kind = tag >> 3, tag & 7
        if not number:
            raise AntigravityEvidenceError("protobufのフィールド番号が不正です")
        if kind == 0:
            value = varint()
        elif kind in (1, 2, 5):
            length = varint() if kind == 2 else (8 if kind == 1 else 4)
            value = raw[position:position + length]
            position += length
            if len(value) != length:
                raise AntigravityEvidenceError("protobufのデータが途切れています")
        else:
            raise AntigravityEvidenceError("未対応のprotobuf wire型です")
        fields.setdefault(number, []).append(value)
    return fields


def one(fields: dict, key: int, default: Any = None) -> Any:
    values = fields.get(key, [default])
    if len(values) != 1:
        raise AntigravityEvidenceError("単一フィールドが重複しています")
    return values[0]


def read_session(config: Path, session_id: str) -> dict[str, Any]:
    if re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", session_id) is None:
        raise AntigravityEvidenceError("会話識別子が不正です")
    database = config / "conversations" / f"{session_id}.db"
    transcript = config / "brain" / session_id / ".system_generated/logs/transcript.jsonl"
    if not database.is_file() or not transcript.is_file():
        raise AntigravityEvidenceError("会話の一次記録がありません")
    records = {}
    for line in transcript.read_bytes().splitlines():
        row = json.loads(line)
        index = row.get("step_index")
        if type(index) is not int or index in records:
            raise AntigravityEvidenceError("会話記録のステップが重複または不正です")
        records[index] = row
    with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as db:
        identity = db.execute("select cascade_id from trajectory_meta").fetchall()
        rows = db.execute("select idx,step_type,status,has_subtrajectory,metadata from steps order by idx").fetchall()
    if identity != [(session_id,)]:
        raise AntigravityEvidenceError("データベースの会話識別子が一致しません")
    if set(records) != {row[0] for row in rows}:
        raise AntigravityEvidenceError("データベースと会話記録のステップ集合が異なります")
    usage, commands, children = [], [], []
    for index, kind, status, has_subtrajectory, metadata in rows:
        record = records[index]
        if status != 3 or record.get("status") != "DONE" or has_subtrajectory:
            raise AntigravityEvidenceError("未完了または未対応の子軌跡があります")
        fields = wire_fields(metadata or b"")
        raw_usage = one(fields, 9)
        if raw_usage is not None:
            values = wire_fields(raw_usage)
            model_id = one(values, 1)
            # 1419とArgon Lowの対応は、固定バイナリのinit・実DB・model一覧で照合済み。
            if model_id != 1419:
                raise AntigravityEvidenceError(f"単価とモデル対応が未固定です: model enum {model_id}")
            item = {"input_tokens": one(values, 2, 0), "output_tokens": one(values, 3, 0),
                    "cache_read_tokens": one(values, 5, 0)}
            if any(type(v) is not int or v < 0 for v in item.values()):
                raise AntigravityEvidenceError("データベースの使用量が不正です")
            if any(record.get(k) != v for k, v in item.items()):
                raise AntigravityEvidenceError("データベースと会話記録の使用量が異なります")
            usage.append({"step_index": index, "model_enum": model_id, **item})
        elif kind == 15 or any(k in record for k in ("input_tokens", "output_tokens")):
            raise AntigravityEvidenceError("モデル実行の使用量がデータベースにありません")
        raw_call = one(fields, 4)
        if raw_call is None:
            continue
        call = wire_fields(raw_call)
        name = one(call, 2, b"").decode()
        parameters = json.loads(one(call, 3, b"{}"))
        if name == "invoke_subagent":
            content = record.get("content", "")
            marker = "Created the following subagent:\n"
            if marker not in content:
                raise AntigravityEvidenceError("子エージェントの作成記録がありません")
            child, _ = json.JSONDecoder().raw_decode(content.split(marker, 1)[1])
            children.append(child["conversationId"])
        if name == "browser_subagent":
            raise AntigravityEvidenceError("ブラウザ子エージェントの使用量が未対応です")
        if name in {"run_command", "command_status", "send_command_input"}:
            commands.append({"step_index": index, "tool_use_id": one(call, 1).decode(),
                             "name": name, "parameters": parameters, "output": record.get("content", "")})
    if not usage:
        raise AntigravityEvidenceError("会話にモデル使用量がありません")
    return {"session_id": session_id, "database": str(database), "transcript": str(transcript),
            "usage": usage, "commands": commands, "children": children}


def collect_all(stream: dict[str, Any], config: Path, model: str, run_id: str) -> tuple[dict, dict]:
    if stream["init"].get("model") != model or model != "gemini-4-argon-low":
        raise AntigravityEvidenceError("固定したArgon Lowと開始記録が一致しません")
    sessions = {}
    pending = [stream["session_id"]]
    while pending:
        session_id = pending.pop()
        if session_id in sessions:
            raise AntigravityEvidenceError("子エージェントの帰属が重複しています")
        session = read_session(config, session_id)
        sessions[session_id] = session
        pending.extend(session["children"])
    root = sessions[stream["session_id"]]
    if set(root["children"]) != set(stream["children"]):
        raise AntigravityEvidenceError("ストリームとデータベースの子エージェント集合が異なります")
    # 親の終了時usageは子を含まない。親だけを独立に照合してから全会話を加算する。
    root_stream = {**stream, "children": []}
    checked_root = collect_usage(root_stream, model)
    root_totals = {k: sum(u[k] for u in root["usage"]) for k in ("input_tokens", "output_tokens", "cache_read_tokens")}
    if any(checked_root["cli_reported_usage"][k] != v for k, v in root_totals.items()):
        raise AntigravityEvidenceError("親のデータベースとストリームの使用量が異なります")
    buckets = empty_buckets()
    attempted, successful, failed, violations = [], [], [], []
    for sid, session in sessions.items():
        for item in session["usage"]:
            buckets["uncached_input"] += item["input_tokens"]
            buckets["cache_read"] += item["cache_read_tokens"]
            buckets["output"] += item["output_tokens"]
        running = {}
        for item in session["commands"]:
            output = item["output"]
            # transcriptのGENERICは二組の時刻ヘッダを持つ。出力本文は解析しない。
            match = re.match(r"\A(?:Created At: [^\n]+\nCompleted At: [^\n]+\n){1,2}Command exited with code (-?\d+)\.\n", output)
            if item["name"] == "run_command":
                command = item["parameters"].get("CommandLine")
                if not isinstance(command, str) or not command:
                    raise AntigravityEvidenceError("コマンド引数がありません")
                base = {"actor": "root" if sid == stream["session_id"] else "subagent", "agent_id": sid,
                        "tool_use_id": item["tool_use_id"], "source": "antigravity_database_and_transcript",
                        "command": command}
                attempted.append(base)
                if match:
                    code = int(match[1])
                    (successful if code == 0 else failed).append({**base, "exit_code": code})
                else:
                    running[item["tool_use_id"]] = base
            # 非同期コマンドの識別子対応は、独立した証拠で固定するまで失敗にする。
        violations.extend({**base, "reason_code": "missing_machine_bound_exit_code"} for base in running.values())
    components = components_document({model: {"standard": buckets}}, "antigravity")
    usage = {"schema_version": "the-caption-prompt.antigravity-usage/v1", "token_accounting": TOKEN_ACCOUNTING,
             "session_id": stream["session_id"], "sessions": list(sessions.values()),
             "root_terminal_usage_not_all_agent": stream["result"]["usage"],
             "all_agent_total_tokens": components["total_tokens"], "usage_components": components}
    commands = {"schema_version": COMMAND_EVIDENCE_SCHEMA_VERSION, "run_id": run_id,
                "session_id": stream["session_id"], "session_count": len(sessions),
                "attempted_commands": attempted, "attempted_command_count": len(attempted),
                "successful_commands": successful, "successful_command_count": len(successful),
                "failed_commands": failed, "failed_command_count": len(failed),
                "protocol_violations": violations, "protocol_violation_count": len(violations)}
    return usage, commands

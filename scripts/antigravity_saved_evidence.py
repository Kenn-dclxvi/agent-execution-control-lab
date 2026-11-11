"""CLI 1.5.5の保存記録を再照合する。ツールの終端エラーと未完了を区別する。"""

import json
from pathlib import Path
import re
import sqlite3

from scripts.antigravity_evidence import (
    AntigravityEvidenceError, TOKEN_ACCOUNTING, wire_fields, one, collect_usage,
)
from scripts.usage_components import components_document, empty_buckets

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
        terminal_tool_error = status == 7 and kind == 132 and record.get("status") == "ERROR"
        if not ((status == 3 and record.get("status") == "DONE") or terminal_tool_error) or has_subtrajectory:
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



def collect_saved_usage(stream, config, model, run_id):
    if stream["init"].get("model") != model or model != "gemini-4-argon-low":
        raise AntigravityEvidenceError("固定したモデルと開始記録が一致しません")
    if stream["result"].get("status") != "SUCCESS":
        raise AntigravityEvidenceError("親会話が正常に終了していません")
    sessions = {}
    pending = [stream["session_id"]]
    while pending:
        sid = pending.pop()
        if sid in sessions:
            raise AntigravityEvidenceError("会話の帰属が重複しています")
        session = read_session(config, sid)
        sessions[sid] = session
        pending.extend(session["children"])
    root = sessions[stream["session_id"]]
    if set(root["children"]) != set(stream["children"]):
        raise AntigravityEvidenceError("親と子の対応が一致しません")
    root_usage = collect_usage({**stream, "children": []}, model)
    for key in ("input_tokens", "output_tokens", "cache_read_tokens"):
        if sum(u[key] for u in root["usage"]) != root_usage["cli_reported_usage"][key]:
            raise AntigravityEvidenceError("親の一次使用量が一致しません")
    buckets = empty_buckets()
    for session in sessions.values():
        for item in session["usage"]:
            buckets["uncached_input"] += item["input_tokens"]
            buckets["cache_read"] += item["cache_read_tokens"]
            buckets["output"] += item["output_tokens"]
    components = components_document({model: {"standard": buckets}}, "antigravity")
    return {"schema_version": "the-caption-prompt.antigravity-usage/v1", "run_id": run_id,
            "token_accounting": TOKEN_ACCOUNTING, "session_id": stream["session_id"],
            "sessions": list(sessions.values()), "all_agent_total_tokens": components["total_tokens"],
            "usage_components": components, "root_terminal_usage_not_all_agent": stream["result"]["usage"]}

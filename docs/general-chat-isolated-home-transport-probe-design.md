# 一般チャットisolated CODEX_HOME transport probe設計

## 目的

ChatControlFree N=1 attempt r2で失われたCodex JSONL error eventを、評価Case、oracle、prompt Candidateおよび採点を使わない固定probe一回で観測する。一般チャットの品質を評価せず、Codex CLI 0.146.0がrun別一時`CODEX_HOME`で認証、model request、structured outputおよびterminal usageを返せるかだけを判定する。

## 固定入力

```text
Return exactly one JSON object matching the supplied schema. Set status to ok.
```

schemaは、余分なfieldを禁止し、`status`を`ok`へ固定したobject一件とする。追加instructionは0 byteの`AGENTS.md`だけとする。

## 固定実行条件

- Codex CLI 0.146.0
- `gpt-5.6-sol / medium`
- `--ignore-user-config --ignore-rules --strict-config --ephemeral`
- memories、apps、plugins、plugin sharing、multi-agentを無効化
- `read-only / never`
- run別一時workspace
- run別一時`CODEX_HOME`
- host `auth.json`はsymlinkで渡し、内容を保存しない

## admission

process exit `0`、schema-valid final response、thread identity一件、terminal usage一件およびtoken取得をすべて満たした場合だけtransportを`available`とする。

nonzero、error event、final欠落、schema不適合、usage欠落のいずれかなら`unavailable`とする。probeは一回だけ実行し、結果を見て同じprobeを再試行しない。

## 保存境界

auth内容、request header、raw session transcript、一時homeおよび一時workspaceを保存しない。stdoutはevent type、thread identity、usageおよびerror messageだけを抽出し、raw bytesのSHA-256を保存する。stderrはSHA-256と末尾1,000文字だけを保存する。

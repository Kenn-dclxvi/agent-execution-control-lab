# Claude Code 2.1.220 measurement transport probe r2実行票

> [!IMPORTANT]
> **状態**: `non_evaluation_probe_fixed / distinct_from_r1 / transport_only / executed_once / transport_probe_observed / no_retry`
>
> 本書は、r1で不足したstdout / stderrの個別証跡transportだけを、別nonceと別probe identityで一回観測する実行票である。r1の再試行、portable kernel評価、control-free baseline、formal target、adapter実装または認証方式の採用ではない。

## 目的と固定境界

`claude-measurement-transport-r2`は次だけを判定する。

1. model processのstdoutとstderrを別file descriptorで取得できる。
2. 両streamのbytes、SHA-256、process exitおよび単調時計elapsedを同一receiptへbindできる。
3. stdoutのterminal JSONから、固定structured output、model、usage、sessionおよびterminal identityの許可fieldを転記できる。
4. 生streamをrepository外へmode `0600`で保存し、secret scanを通過したfieldだけを利用者向けresultへ記録できる。

all-agent token完全性、補助modelの帰属、subagent provenance、prompt isolationの完全性、nonterminal identityおよびformal KPIは判定しない。`usage`の数値を加算して`total_tokens`を作らない。

## 固定入力

system prompt、user inputおよびschemaはr1と同じ構造を使うが、nonceを新しい値へ変え、別probeであることを一意にする。

```text
system: Return only data that satisfies the supplied JSON schema. Do not add facts, explanations, or fields.
user: Return probe_status "ok" and nonce "portable-measurement-transport-20260817-r2".
```

```json
{"type":"object","additionalProperties":false,"properties":{"probe_status":{"const":"ok"},"nonce":{"const":"portable-measurement-transport-20260817-r2"}},"required":["probe_status","nonce"]}
```

## 固定実行条件

| field | 固定値 |
| --- | --- |
| probe identity | `claude-measurement-transport-r2` |
| CLI | `/Users/kenn/.local/bin/claude` |
| CLI version | `2.1.220 (Claude Code)` |
| authentication | 現在のClaude Code認証を読む。正式系列の認証方式として採用しない |
| customization | `--safe-mode` |
| persistence | `--no-session-persistence` |
| tools | `--tools ""` |
| permission | `--permission-mode dontAsk` |
| model argument | `sonnet`。resolved modelはterminal JSONから取得 |
| output | `--output-format json` + 固定`--json-schema` |
| working directory | `tempfile.mkdtemp`で作るrepository外の空directory、mode `0700` |
| raw evidence directory | 別のrepository外一時directory、mode `0700` |
| raw stream files | `stdout.raw`と`stderr.raw`、各mode `0600` |
| timeout | 120秒 |
| model attempts | 1 |

shellは使わず、argument配列を`subprocess.run`へ直接渡す。stdoutとstderrは別pipeで取得し、process終了後に別fileへ保存する。

## harnessとticket

実装は[`scripts/claude_measurement_transport_probe.py`](../scripts/claude_measurement_transport_probe.py)とする。実行前に別JSON ticketへ次を固定する。

- 上記の全argumentとexpected CLI version
- harness SHA-256
- attempts `1`
- timeout `120`
- raw保存mode
- secret scan marker
- admission条件

harnessは自身のSHA-256とticketの値が一致しなければ、version確認を除くmodel invocationを発行しない。

## admission

次を全件満たす場合だけ`transport_probe_observed`とする。

1. harness、ticketおよびCLI versionが固定値と一致する。
2. model invocationは一回で、process exitは0。
3. stdoutとstderrが別bytesとして保存され、各path、mode、byte数およびSHA-256がreceiptにある。
4. stdout全体が単一JSON objectとしてparseできる。
5. `structured_output`が固定二fieldへexact一致する。
6. `usage`、`modelUsage`、`session_id`、`uuid`およびterminal fieldが存在する。
7. 単調時計の開始、終了および非負elapsedがreceiptにある。
8. secret markerが両streamにない。

CLI version不一致、ticket不一致またはharness hash不一致は`not_started`としてmodel invocationを発行しない。認証、policy、modelまたはoption拒否は`probe_unavailable`、network、capacity、timeoutまたはservice errorは`external_failure`として停止する。いずれもこのticketで再試行しない。

## 生証拠の扱い

生stdout / stderr、一時directory、credentialおよび非公開logをcommitしない。result文書へ残せるのは次だけである。

- probe、ticket、harness、CLIおよび時刻identity
- process exit、elapsed、stream byte数、SHA-256、file mode
- terminal JSONのtop-level key名
- schema適合済み`structured_output`
- resolved model、usage field名と許可済み数値
- session / terminal identity
- admission判定と未完了gate

## probe後も未完了のgate

- formal runtimeで採用する認証方式
- admin-managed policyを含むinstruction source境界
- control-freeとkernelのprompt identity
- all-agent token完全性と補助modelの重複排除
- actor / result provenanceとnonterminal identity
- formal target、baseline qualification、Profile、preflightおよび評価slot

## 参照

- [`measurement transport probe r2観測結果`](claude-code-2.1.220-measurement-transport-probe-r2-result.md)
- [`measurement-schema probe r1観測結果`](claude-code-2.1.220-measurement-schema-probe-result.md)
- [`Portable instruction runtime別測定成立監査`](portable-instruction-runtime-measurement-feasibility-audit.md)
- [`Portable instruction semantic conformance held-out r1`](portable-instruction-semantic-conformance-heldout-r1/)

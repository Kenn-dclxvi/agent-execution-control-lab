# Claude Code 2.1.220 measurement-schema probe実行票

> [!IMPORTANT]
> **状態**: `non_evaluation_probe_fixed / executed_once / terminal_result_received / probe_not_admitted / no_retry`
>
> 本書はClaude Code CLI 2.1.220が返すterminal JSONのfield形状を一回だけ観測する非評価probeを固定する。portable kernel、C147本文、Q01-Q08、repository task、Candidate、baselineまたはformal resultではない。
>
> 実行結果とadmission判定は[`measurement-schema probe観測結果`](claude-code-2.1.220-measurement-schema-probe-result.md)を正本とする。stdoutとstderrを個別取得できなかったため`probe_observed`へadmitせず、再試行しない。

## 目的

`--output-format json`と`--json-schema`を併用したときに、次の一次値が一つのterminal JSONへ現れるかを観測する。

- schema適合済み応答
- 実model identity
- usageまたは`modelUsage`
- sessionまたはrequest identity
- error、subtypeまたはpermission denial

toolとsubagentを無効にするため、このprobeのtoken範囲はroot一応答だけである。all-agent accountingの完全性、subagent provenance、native executionまたはportable instructionの効果は判定しない。

## 固定入力

### system prompt

改行を含まない次のUTF-8文字列をそのまま使う。

```text
Return only data that satisfies the supplied JSON schema. Do not add facts, explanations, or fields.
```

### user input

改行を含まない次のUTF-8文字列をそのまま使う。

```text
Return probe_status "ok" and nonce "portable-measurement-20260814-r1".
```

### JSON schema

```json
{"type":"object","additionalProperties":false,"properties":{"probe_status":{"const":"ok"},"nonce":{"const":"portable-measurement-20260814-r1"}},"required":["probe_status","nonce"]}
```

## 固定実行条件

| field | 固定値 |
| --- | --- |
| CLI | `/Users/kenn/.local/bin/claude` |
| expected CLI version | `2.1.220 (Claude Code)` |
| model argument | `sonnet`。terminal resultのresolved modelを別に記録する |
| instruction isolation | `--safe-mode`。admin-managed policyの有無は観測不能なら`unavailable` |
| tools | `--tools ""` |
| permission | `--permission-mode dontAsk` |
| persistence | `--no-session-persistence` |
| output | `--output-format json` |
| interaction | `--print` |
| working directory | `mktemp -d`で作る空directory。repository外 |
| authentication | 現在のClaude Code認証を読む。credential値は表示、保存または変更しない |
| attempts | 1 |

`--safe-mode`はhelp上、`CLAUDE.md`、skills、plugins、hooks、MCP、custom commands、custom agentsなどを無効にする一方、admin-managed settings、auth、model selection、built-in toolsおよびpermissionは残す。したがって本probeは「追加instructionが絶対に存在しない」とは証明しない。

## exact command

次の一回だけを発行する。`PROBE_WORKDIR`は`mktemp -d`が返した絶対pathへbindし、存在と空directoryであることを確認してから`cwd`に使う。command終了後に同directoryへ生成物があるかを列挙し、削除はこの実行票へ含めない。

```sh
/Users/kenn/.local/bin/claude --print --safe-mode --no-session-persistence --tools "" --permission-mode dontAsk --model sonnet --output-format json --json-schema '{"type":"object","additionalProperties":false,"properties":{"probe_status":{"const":"ok"},"nonce":{"const":"portable-measurement-20260814-r1"}},"required":["probe_status","nonce"]}' --system-prompt 'Return only data that satisfies the supplied JSON schema. Do not add facts, explanations, or fields.' 'Return probe_status "ok" and nonce "portable-measurement-20260814-r1".'
```

shell commandへ別の観測処理を連結しない。process exit、stdout、stderrおよびwall-clock elapsedは呼出側が個別に保持する。

## admissionと記録

### `probe_observed`

次を全件満たす場合だけ`probe_observed`とする。

1. commandを一回だけ発行した。
2. process exitが0である。
3. stdout全体が単一JSON objectとしてparseできる。
4. terminal JSON内のschema適合済みpayloadが固定した二fieldだけを持つ。
5. terminal JSONのtop-level key一覧、model関連field、usage関連field、identity関連fieldおよびerror関連fieldを生値から転記できる。
6. stderrと一時directory内容を観測済みである。

数値tokenがあっても、このprobeだけでは正式な`total_tokens`へadmitしない。

### `probe_unavailable`

次のいずれかは`probe_unavailable`としてterminalにする。別認証または別modelへ迂回しない。

- 現在の認証では`--safe-mode`実行が認証不能。
- `sonnet`をresolveまたは利用できない。
- policyがcommandを拒否する。
- `--tools ""`、`--no-session-persistence`または`--json-schema`の組合せがCLI 2.1.220で利用不能。

### `external_failure`

network、capacity、timeoutまたはservice errorは`external_failure`として、error identityとprocess resultを保存して停止する。この実行票では再試行しない。

## probe後も未完了のgate

- explicit system promptとadmin-managed instructionの分離
- control-free条件とkernel条件のprompt identity
- subagentを含むall-agent token完全性
- transcript requestのdedup
- actor/result provenance
- nonterminal invocation identity
- formal target、profile、preflightおよび評価slot

## 参照

- [`Portable instruction runtime別測定成立監査`](portable-instruction-runtime-measurement-feasibility-audit.md)
- [`Claude Code CLI評価adapter設計`](claude-code-cli-evaluation-adapter-design.md)
- [`Portable instruction semantic conformance評価設計`](portable-instruction-semantic-conformance-evaluation-design.md)
- [`Claude Code 2.1.220 measurement-schema probe観測結果`](claude-code-2.1.220-measurement-schema-probe-result.md)

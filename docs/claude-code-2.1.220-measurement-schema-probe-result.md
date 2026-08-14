# Claude Code 2.1.220 measurement-schema probe観測結果

> [!IMPORTANT]
> **状態**: `invocation_terminal / schema_response_observed / root_usage_observed / resolved_model_observed / probe_not_admitted / stdout_stderr_not_independently_captured / no_retry`
>
> 2026-08-14に[`measurement-schema probe実行票`](claude-code-2.1.220-measurement-schema-probe-plan.md)のcommandを一回だけ発行した。本書は非評価probeの観測結果であり、formal result、portable kernelの評価、target admission、採用またはruntime間比較ではない。

## 結論

Claude Code CLI 2.1.220は、`--safe-mode`、`--no-session-persistence`、`--tools ""`、`--output-format json`および`--json-schema`を併用した一回の実行で、固定schemaに適合する`structured_output`、resolved model、root usage、session identityおよびterminal stateを一つのJSON objectへ返した。

ただし呼出側がstdoutとstderrを別streamとして保存せず、結合された`output`だけを返した。実行票は両streamの個別観測をadmission条件にしていたため、この実行を`probe_observed`へadmitしない。再試行禁止に従い、同じprobeを再発行しない。

## 実行identity

| field | 観測値 |
| --- | --- |
| observed date | `2026-08-14` |
| CLI | `/Users/kenn/.local/bin/claude` |
| CLI version | `2.1.220 (Claude Code)` |
| working directory | `/private/tmp/c147-claude-schema-probe.6YztQF` |
| process exit | `0` |
| invocation wall time | `3.140843375 seconds`。呼出toolが返した値でありformal elapsed KPIではない |
| attempts | `1` |
| session ID | `e45961dd-1f82-459e-8dca-9d19b9f93a49` |
| terminal UUID | `1a68a509-b82c-4a5e-9be8-be0d75b4f8b8` |

command終了後、一時作業directoryは空だった。返されたsession IDは`/Users/kenn/.claude/projects`配下の現存fileから検出されなかった。これは当該保存場所でsessionを見つけなかったという診断であり、filesystem全体へのwrite不在または全永続化不在を証明しない。

## terminal JSONの観測

top-level keyは次のとおりだった。

```text
is_error, duration_api_ms, num_turns, stop_reason, session_id, total_cost_usd, usage, modelUsage, permission_denials, terminal_reason, fast_mode_state, fast_mode_disabled_reason, subtype, api_error_status, result, structured_output, ttft_ms, ttft_stream_ms, time_to_request_ms, type, duration_ms, uuid
```

### 応答とterminal

| field | 観測値 |
| --- | --- |
| `is_error` | `false` |
| `type` | `result` |
| `subtype` | `success` |
| `terminal_reason` | `completed` |
| `api_error_status` | `null` |
| `permission_denials` | `[]` |
| `structured_output` | `{"probe_status":"ok","nonce":"portable-measurement-20260814-r1"}` |
| `result` | 同じ二fieldを持つJSON文字列 |

`structured_output`は固定schemaに適合した。schemaが`additionalProperties: false`を要求した二field以外は入っていなかった。

### modelとusage

| field | 観測値 |
| --- | --- |
| `modelUsage` key | `claude-sonnet-5` |
| `canonicalModel` | `claude-sonnet-5` |
| `provider` | `firstParty` |
| root `input_tokens` | `709` |
| root `output_tokens` | `90` |
| root `cache_creation_input_tokens` | `0` |
| root `cache_read_input_tokens` | `0` |
| root `iterations` | 1件。`type=message` |
| `total_cost_usd` | `0.003477` |

inputとoutputの和は799だが、CLIはこのprobeに`total_tokens`という一次fieldを返していない。799をformal `total_tokens`へ採用しない。toolとsubagentを無効にした一回の診断なので、all-agent completenessも判定しない。

### timingとturn形状

| field | 観測値 |
| --- | --- |
| `duration_ms` | `2079` |
| `duration_api_ms` | `1883` |
| `ttft_ms` | `2057` |
| `ttft_stream_ms` | `1313` |
| `time_to_request_ms` | `198` |
| `num_turns` | `2` |
| `stop_reason` | `tool_use` |

`--tools ""`でも`num_turns=2`と`stop_reason=tool_use`になった。固定JSONのstructured outputが内部的なtool-use形状を取る可能性があるが、この一件だけでは原因を確定しない。今後のadapterは「toolsを無効にしたから1 turn」と仮定してはならず、terminal JSONとusage iterationを別々に検証する必要がある。

## admission判定

実行票の条件1から5は観測できた。条件6のうち一時directory内容は観測したが、stdoutとstderrを個別streamとして保存できなかった。呼出toolの`output`は単一文字列であり、stderrが空だったことを一次fieldとしてbindできない。

したがって判定は次のとおり。

```text
probe_observed = false
reason = stdout_stderr_not_independently_captured
retry = forbidden_by_probe_plan
```

このfailureはClaude Codeのschema出力失敗ではなく、probe呼出側の証跡transport不足である。観測したfield形状は次のprobe設計入力にできるが、実行票を満たした成功receiptとしては使わない。

## 次の設計境界

次回は別identityのprobeとして、発行前にstdoutとstderrを別file descriptorへbindし、各bytes、process exitおよび単調時計を同一receiptへ保存するharnessを固定する。これは今回の再試行ではない。portable kernel、Q01-Q08、subagentまたはrepository taskを混ぜない。

そのprobeを作る前に、次を設計上決める。

- 生outputの保存場所とsecret scan
- `result.usage`と`modelUsage`の整合条件
- `num_turns`、`iterations`およびstructured output内部turnの関係
- formal token fieldを新設するか、CLI一次field不足としてformal targetを保留するか
- admin-managed policyの観測不能をprompt isolationへどう記録するか

## 参照

- [`Claude Code 2.1.220 measurement-schema probe実行票`](claude-code-2.1.220-measurement-schema-probe-plan.md)
- [`Portable instruction runtime別測定成立監査`](portable-instruction-runtime-measurement-feasibility-audit.md)
- [`Claude Code CLI評価adapter設計`](claude-code-cli-evaluation-adapter-design.md)

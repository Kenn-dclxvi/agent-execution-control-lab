# Claude Code 2.1.220 measurement transport probe r2観測結果

> [!IMPORTANT]
> **状態**: `invocation_terminal / transport_probe_observed / separate_stdout_stderr_bound / schema_response_observed / formal_token_not_admitted / formal_target_not_created / no_retry`
>
> 2026-08-17に[`r2実行票`](claude-code-2.1.220-measurement-transport-probe-r2-plan.md)と固定ticketを一回だけ発行した。本書と[`receipt`](claude-code-2.1.220-measurement-transport-probe-r2-receipt.json)は非評価probeの観測結果であり、control-free baseline、formal result、portable kernel評価、target admissionまたはruntime間比較ではない。

## 結論

r1で不足した証跡transport境界は閉じた。Claude Code CLI 2.1.220のmodel processからstdoutとstderrを別pipeで取得し、repository外の別fileへmode `0600`で保存した。stdout全体は単一terminal JSONとしてparseでき、固定structured output、resolved model、usage、session identityおよびterminal identityを許可fieldへbindできた。

一方、このprobeはtoolとsubagentを無効にしたroot一応答だけである。`usage.input_tokens=715`と`usage.output_tokens=93`は観測値として保持するが、加算値をformal `total_tokens`にせず、all-agent completenessも成立済みにしない。

## 実行identity

| field | 観測値 |
| --- | --- |
| probe | `claude-measurement-transport-r2` |
| CLI | `/Users/kenn/.local/bin/claude` |
| CLI version | `2.1.220 (Claude Code)` |
| model attempts | `1` |
| process exit | `0` |
| monotonic elapsed | `3.301951833 seconds`。formal KPIではない |
| ticket SHA-256 | `d10e551eb80a0ca823930ed46ffc01bd184f660067c7c44746e19c4f1aeb83f3` |
| harness SHA-256 | `197b8e0881dc09044948696ff5cd5ecd6081186298a035ddaf41a761d6af47b8` |
| session ID | `41b10ca7-5523-4e38-b11b-63a82f9a2892` |
| terminal UUID | `66c1e141-53e0-4213-a359-e8ad8159d59e` |

同じticketは再発行しない。

ticketとharnessの末尾空行は上記SHA-256へ含まれる実行時bytesである。履歴identityを保つため正規化しない。

## stream境界

| stream | bytes | mode | SHA-256 |
| --- | ---: | --- | --- |
| stdout | 1,469 | `0600` | `bb40689f358da0031d56890bf5787de858ceef6bfb6660ada108460c59287de5` |
| stderr | 0 | `0600` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

secret markerは0件だった。生streamはrepositoryへcommitせず、receiptにはrepository外path、byte数、modeおよびhashだけを残した。一時workdirはinvocation後も空だった。

## terminal観測

| field | 観測値 |
| --- | --- |
| `type / subtype` | `result / success` |
| `is_error` | `false` |
| `terminal_reason` | `completed` |
| `structured_output` | `{"probe_status":"ok","nonce":"portable-measurement-transport-20260817-r2"}` |
| resolved model | `claude-sonnet-5` |
| root input / output | `715 / 93` |
| `modelUsage` | `claude-sonnet-5`の同じinput / output値を観測 |
| `num_turns` | `2` |
| `stop_reason` | `tool_use` |

r1と同様、tool無効でもstructured outputは`num_turns=2 / stop_reason=tool_use`だった。これはschema出力の内部形状として診断に保持するが、一応答のtoken完全性またはnative tool実行を意味するものとして一般化しない。

## admission判定

固定した8条件は全件成立した。

```text
status = transport_probe_observed
model_invocations = 1
retry = forbidden
formal_result = false
```

成立したのは、別stream、raw hash、process exit、単調時計およびterminal projectionを一つのreceiptへbindできることだけである。r1の`stdout_stderr_not_independently_captured`は解消した。

## 残るgate

次に未完了なのはtransportではなく計測意味である。

1. formal runtimeで使う認証方式を選定する。
2. admin-managed policyを含むinstruction sourceの観測境界を固定する。
3. root、subagentおよび補助model callを含むall-agent token完全性とdedup keyを非評価probeで確認する。
4. actor / result provenanceとnonterminal identityの観測可否を確認する。
5. その後にformal target、control-free baseline、Profile、preflightおよび評価slotを別gateで作る。

認証方式が未選定のため、この結果だけではcontrol-free baselineを発行しない。

## 参照

- [`r2実行票`](claude-code-2.1.220-measurement-transport-probe-r2-plan.md)
- [`r2 receipt`](claude-code-2.1.220-measurement-transport-probe-r2-receipt.json)
- [`measurement-schema probe r1結果`](claude-code-2.1.220-measurement-schema-probe-result.md)
- [`Portable instruction runtime別測定成立監査`](portable-instruction-runtime-measurement-feasibility-audit.md)

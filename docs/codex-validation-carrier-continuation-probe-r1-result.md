# Codex validation carrier continuation probe r1結果

> [!IMPORTANT]
> **状態**: `continuation_observed / first_result_nonterminal / same_session_bound / internal_write_stdin_one / terminal_exit_zero / intermediate_ingress_denied / external_marker_complete / no_retry`

## 結論

Codex CLI `0.146.0`は、一つのprogrammatic carrier内部でnonterminalなnested commandを同じsession identityへbindし、modelへ途中resultを返さずterminalまで継続した。

初回`exec_command`は250msで`session_id`付きnonterminal resultを返した。programはそのidentityを保持し、同じcarrier内から`write_stdin`を1回だけ発行してexit 0を受領した。carrier外のmodel response、別command、別sessionまたは進捗messageは途中にない。

これにより、Codex validation carrierの7 capabilityは全件観測済みとなった。これはtool routeの利用可能性を示すが、P001本文、Candidate、採用、releaseまたは全runでの遵守を意味しない。

## 実行identity

| field | 値 |
| --- | --- |
| observed date | `2026-08-18` |
| workdir | `/Users/kenn/repos/_verification/codex-validation-carrier-continuation-probe-r1.fzgj2f` |
| CLI / model / reasoning | `codex-cli 0.146.0` / `gpt-5.6-sol` / `medium` |
| permission | `workspace-write / never` |
| process exit | `0` |
| attempts | `1` |
| thread ID | `01a01280-3c5c-7402-a047-b70647a8ccbc` |
| persisted rollout | `/Users/kenn/.codex/sessions/2026/08/18/rollout-2026-08-18T10-33-09-01a01280-3c5c-7402-a047-b70647a8ccbc.jsonl` |

## 保存証拠

| evidence | bytes | SHA-256 |
| --- | ---: | --- |
| `raw.jsonl` | 973 | `81fa251c1561b4df9459644f8c4d7c066cac49c035e5294bfe1cd4240d694491` |
| `stderr.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `probe-events.log` | 47 | `429572861a97a1d8e9070e6b625a960a534272314c06b23a78e9b4fc6b3a47a6` |
| persisted rollout | 53,765 | `08da1987baa8b81ec9bb4456dd35ae833394235daec2a51ca5f63c864f3ce781` |

raw evidenceとmarkerにsecret patternはなかった。rawは`_verification`、sessionはCodex storageだけに保持する。

## program内部のroute

custom `exec` programは次を行った。

1. `tools.exec_command`へ`bash validation-long.sh`、`yield_time_ms=250`を渡す。
2. `first.session_id`がintegerかつ`exit_code`欠落であることからnonterminalを判定する。
3. `boundSession = first.session_id`を一度bindする。
4. 同じprogram内で`tools.write_stdin(session_id=boundSession)`を一回実行する。
5. exit 0受領後にterminal JSONを一度だけ`text(...)`で返す。

persisted rolloutには`custom_tool_call exec` 1件、`custom_tool_call_output` 1件、final answer 1件があり、exec前のassistant commentaryもない。

## markerとterminal JSON

外部markerは次の2行を持つ。

```text
validation-long-start
validation-long-terminal
```

final JSONはschemaへ適合した。

```json
{
  "carrier_route": "programmatic_carrier",
  "continuation_calls": 1,
  "continuation_session_bound": true,
  "exit_code": 0,
  "first_result_kind": "nonterminal",
  "marker_complete": false,
  "probe_status": "observed",
  "validation_id": "validation-long"
}
```

`marker_complete=false`は、scriptがmarkerをfileへ書きstdoutへ出さず、programが追加readを行わなかったためである。外部markerはterminalまで完了したことを示す。このfieldはcarrier内のevidence projection不足として保持するが、session identity継続、exit resultまたは途中result ingressの判定を失効させない。将来のplatform blockでは、required evidenceを開始前にoutput contractへbindし、carrierが観測できないmarkerを返却必須fieldにしない。

usageはinput 29,880、cached input 14,080、output 730、total 30,610だった。formal KPIまたはP001比較には使わない。

## admission

| 条件 | 判定 |
| --- | --- |
| process exit 0、schema適合 | pass |
| nested command一件 | pass |
| 初回nonterminal + session identity | pass |
| 同じsessionへのprogram内continuation | pass |
| carrier外の途中model responseなし | pass |
| terminal exit 0 + external start/terminal marker | pass |
| carrier terminal output一件 | pass |

`continuation_observed=true`とする。同じprobeは再発行しない。

## 次の境界

Codex carrierの能力確認は完了した。次は評価ではなく、管理用compositionで`validation-plan / validation-result-closure`と`validation-carrier-codex`を別componentへ分け、render後は自己完結した一枚にする。

このcompositionは`model_visible=false / evaluation_eligible=false / bundle_binding_eligible=false`のdraftに限定し、P002、Profileまたはdispatch planを作らない。

## 参照

- [`continuation probe r1実行票`](codex-validation-carrier-continuation-probe-r1-plan.md)
- [`validation carrier probe r2結果`](codex-validation-carrier-capability-probe-r2-result.md)
- [`P001 validation carrier platform分離設計`](p001-validation-carrier-platform-separation-design.md)

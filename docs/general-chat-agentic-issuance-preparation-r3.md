# General chat agentic probe issuance preparation r3

> [!IMPORTANT]
> **状態**: `r2_ticket_preserved / private_adapter_bound / composition_r2_verified / one_issue_fixed / identity_available / ready_not_authorized / negative_14_passed / focused_9_passed / model_invocations_0 / real_trace_reads_0 / probe_issues_0`

## 結論

実0.146.0 probeを一回だけ発行するための技術準備を、既存r2 ticketとは別のr3 ticketへ固定した。exact runtimeとprivate trace shadow compositionを再検証し、probe identityが未使用であることを確認した結果、preparation stateは`ready_not_authorized`である。

r3は発行権限を与えない。`issuance_authority=not_authorized`をschemaで固定しているため、ticket本文の値だけを`authorized_not_issued`へ書き換える操作も拒否する。model invocation、実trace読取り、reservation作成およびprobe発行は0件である。

## r2からの差分

| 項目 | r2 | r3 |
| --- | --- | --- |
| 役割 | exact runtime固定ticket | private adapterとone-issue lifecycleの発行準備 |
| adapter | ready false | technical state `shadow_verified`を別fieldへbind |
| real trace | 未観測 | `real_trace_observed=false`を明示 |
| authority | `not_authorized` | `not_authorized`を維持 |
| issue policy | max 1、retryなし | 同じ値にreservation、record、cleanup境界を追加 |

直接の前段は[`general-chat-agentic-capability-preflight-ticket-r2.json`](general-chat-agentic-capability-preflight-ticket-r2.json)で、許可差分は`private_trace_adapter_binding_and_issuance_preparation_only`である。r2を改訂したり、r3へr2の失敗理由以外の効果を持ち込んだりしない。

## 固定した発行境界

[`general-chat-agentic-capability-preflight-ticket-r3.json`](general-chat-agentic-capability-preflight-ticket-r3.json)は次を固定する。

- composition r2 input、schema、validatorおよびrequired state。
- private trace adapterとinput / output schema identity。
- task、fixtureおよび10 criterion。
- `max_issues=1`、retryなし、overwriteなし、reservation必須。
- `reservation.json`、`issued.json`、`receipt.json`を同一probe identityのwrite-once recordとする。
- record rootを`artifacts/capability-preflight-issuance/<probe_id>/`へ限定し、Git commitを禁止する。
- rawはreceipt sealまたはterminal failureまでの一時保持とし、runnerがcleanupする。

static validationはrecordを作らない。三recordのいずれかが既にあれば、authority判定より先に`PROBE_IDENTITY_ALREADY_USED`で停止する。

## static validator

[`general_chat_agentic_issuance_preparation_r3.py`](../scripts/general_chat_agentic_issuance_preparation_r3.py)は次の二operationだけを持つ。

- `validate-ticket`: artifact identity、composition r2、probe identity未使用およびauthorityを検証する。
- `validate-negative-fixtures`: 一件ずつの14 mutationを固定rejection reasonへ対応づける。

固定ticketの結果は次のとおりである。

| 項目 | 結果 |
| --- | --- |
| runtime | `verified` |
| adapter technical state | `shadow_verified` |
| real trace observed | false |
| identity available | true |
| preparation | `ready_not_authorized` |
| dispatch | `denied` |
| reason | `ISSUANCE_NOT_AUTHORIZED` |
| model / real trace / probe | 0 / 0 / 0 |

14 negative fixtureはlineage、composition、adapter、real trace状態、discovery、issue上限、retry、overwrite、record root / names / commit、cleanupおよびauthority driftをすべて指定reasonへ拒否した。focused test 9件ではschema、output、identity使用済み、root escape、record非作成およびGit除外も確認した。

## 次の判断

技術準備は完了した。次に必要なのは、`general-chat-agentic-capability-preflight-r3`について、費用を伴うmodel利用とprivate実trace生成を含むprobe発行を一回だけ許可するかという利用者の判断である。一回とはprobe identityの発行回数を指し、内部のmodel request件数を一件へ固定する意味ではない。

許可する場合もr3を書き換えず、r3を直接前段とする別のauthorization artifactへ`authorized_not_issued`を固定し、発行直前static validation、reservation、one-shot execution、terminal receiptおよびcleanupを一つの実行票として扱う。許可されるまでは追加のticket、runner、reservation、model invocation、実trace読取り、probe、target登録および評価を開始しない。

## 参照

- [`model-free composition preflight r2`](general-chat-agentic-composition-preflight-r2.md)
- [`private trace adapter r1`](general-chat-agentic-private-trace-adapter-r1.md)
- [`capability preflight実行前契約`](general-chat-agentic-capability-preflight-plan.md)
- [`target登録前設計`](general-chat-agentic-target-preregistration-design.md)

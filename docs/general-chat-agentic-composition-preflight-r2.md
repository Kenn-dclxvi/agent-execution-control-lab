# General chat agentic model-free composition preflight r2

> [!IMPORTANT]
> **状態**: `r1_preserved / exact_runtime_verified / private_trace_shadow_verified / binding_unavailable / dispatch_denied / focused_18_passed / issuance_preparation_r3_ready_not_authorized / model_invocations_0 / real_trace_reads_0 / probe_issues_0 / capability_receipt_not_created`

## 結論

exact Codex CLI 0.146.0 runtime identityとprivate trace adapterのsynthetic shadow projectionを、一つのmodel-free compositionへ結合した。runtimeとprivate input境界は成立したが、入力originは`synthetic_shadow`であり、spawn、packet、task identity、terminal sender、tool resultおよびroot final responseは`unobserved`のままである。

binding admissionは`agentic_runtime_capability_unavailable`、dispatchは`denied`である。r2 ticketの`real_trace_adapter_ready=false`と`issuance_authority=not_authorized`を変更していない。

## r1からの差分

| 項目 | r1 | r2 |
| --- | --- | --- |
| adapter input | repository synthetic packet | externally selected private trace contractのrepository shadow |
| adapter state | `synthetic_verified` | `private_trace_shadow_verified` |
| trace origin | envelope外 | `synthetic_shadow`を明示 |
| lifecycle | synthetic packet境界 | runner ownership、adapter mutation / cleanup禁止 |
| 維持結果 | binding unavailable、dispatch denied | 同じ |

直接の前段は[`general-chat-agentic-composition-preflight-r1.json`](general-chat-agentic-composition-preflight-r1.json)で、許可差分は`synthetic_adapter_to_private_trace_shadow`だけである。r1 artifact、runtime ticket、task、fixture、criterion、admissionおよび停止理由を変更しない。

## 固定identity

[`general-chat-agentic-composition-preflight-r2.json`](general-chat-agentic-composition-preflight-r2.json)は次をpath、SHA-256、byte数へbindする。

- r1 composition input。
- exact runtime ticket、schemaおよびvalidator。
- private trace shadow packet、input / output schemaおよびadapter。
- transitive dependencyであるsynthetic adapterとraw normalizer。
- normalized r2 schema、binding evaluatorおよびfixture。
- private projectionとnormalized traceのcanonical SHA-256。
- criterion、admission、dispatch、停止理由および0件であるべき実行数。

全identityを検証する前にdependency moduleを読み込まない。一件でもdriftした場合はcompositionを開始しない。

## 結果

2026-08-20の実行結果は次のとおりである。

| 項目 | 結果 |
| --- | --- |
| runtime | `verified` |
| adapter | `private_trace_shadow_verified` |
| origin | `synthetic_shadow` |
| binding | `agentic_runtime_capability_unavailable` |
| dispatch | `denied` |
| reasons | `REAL_TRACE_ADAPTER_NOT_READY`、`ISSUANCE_NOT_AUTHORIZED` |
| model invocation | 0 |
| real trace read | 0 |
| probe issue | 0 |
| mutation / raw path | false / 0 |

focused test 18件では正常composition、r1 lineage、adapterとtransitive dependencyのhash drift、artifact間schema mismatch、10種類の状態昇格およびshadow root driftの拒否を確認した。

## 現在許可する次作業

probe issuance preparation r3は`ready_not_authorized`まで通過した。次に必要なのはmodel利用とprivate実trace生成を伴うprobe発行を一回だけ許可するかという利用者の判断である。許可されるまでは追加artifact、model invocation、実trace読取り、probe発行、capability receipt、target登録および評価を開始しない。

## 参照

- [`composition preflight r1`](general-chat-agentic-composition-preflight-r1.md)
- [`private trace adapter r1`](general-chat-agentic-private-trace-adapter-r1.md)
- [`exact runtime preflight r2`](general-chat-agentic-exact-runtime-preflight-r2.md)
- [`capability preflight実行前契約`](general-chat-agentic-capability-preflight-plan.md)
- [`probe issuance preparation r3`](general-chat-agentic-issuance-preparation-r3.md)

# General chat agentic model-free composition preflight r1

> [!IMPORTANT]
> **状態**: `exact_runtime_verified / synthetic_adapter_verified / binding_unavailable / dispatch_denied / focused_12_passed / private_trace_adapter_shadow_verified / model_free_composition_r2_passed / issuance_preparation_r3_ready_not_authorized / model_invocations_0 / real_trace_reads_0 / probe_issues_0 / capability_receipt_not_created`

## 結論

exact Codex CLI 0.146.0 runtime preflightとsynthetic file packet限定adapterを、一つのmodel-free compositionへ結合した。runtime identityとsynthetic projectionは成立したが、spawn、packet、task identity、terminal sender、tool resultおよびroot final responseは引き続き`unobserved`である。binding admissionは`agentic_runtime_capability_unavailable`、dispatchは`denied`のままである。

この結果は実0.146.0 traceを読んだ結果ではなく、capability receiptでもない。synthetic adapterの成立をreal trace adapter readyへ読み替えず、r2 ticketの`real_trace_adapter_ready=false`と`issuance_authority=not_authorized`を維持する。

## 固定入力

[`general-chat-agentic-composition-preflight-r1.json`](general-chat-agentic-composition-preflight-r1.json)は次の依存identityをpath、SHA-256、byte数へbindする。

- exact runtime ticket、schemaおよびstatic validator。
- synthetic adapter packet、packet schema、adapter、normalizerおよびr2 normalized schema。
- binding evaluatorおよび固定fixture。
- normalized outputのcanonical SHA-256とcomposition output schema。
- criterion 10件、binding admission、dispatch state、停止理由および実行件数の期待値。

入力schemaはavailable、allowed、real trace verified、model invocation、real trace readまたはprobe issueへの状態昇格を拒否する。依存fileを読み込む前に全identityを検証し、一件でもpath、hashまたはbyte数が不一致ならcompositionを開始しない。

## 実装

[`general_chat_agentic_composition_preflight.py`](../scripts/general_chat_agentic_composition_preflight.py)は次を順に実行する。

1. composition input schemaを検証する。
2. repository内の依存file identityを全件確認する。
3. ticket、packet、probe、runtimeおよびnormalized schemaのartifact間relationを確認する。
4. exact runtime static preflightを実行する。
5. synthetic packetを既知fieldだけへ正規化する。
6. binding evaluatorへ渡し、固定expected stateとの完全一致を確認する。
7. composition receiptを固定output schemaで検証する。

Codex entrypointへ発行するcommandは既存static preflightの`--version`だけであり、model requestではない。`codesign`もruntime署名照合だけに使う。session探索、実trace読取り、task発行、tool fixture、receipt sealおよびtarget登録は行わない。

## 結果

2026-08-20の実行結果は次のとおりである。

| 項目 | 結果 |
| --- | --- |
| runtime | `verified` |
| adapter | `synthetic_verified` |
| binding | `agentic_runtime_capability_unavailable` |
| satisfied | root identity、all-agent final usage、monotonic elapsed、安全projection |
| unobserved | spawn、packet、descendant task binding、terminal sender、root tool、root final response |
| dispatch | `denied` |
| reasons | `REAL_TRACE_ADAPTER_NOT_READY`、`ISSUANCE_NOT_AUTHORIZED` |
| model invocation | 0 |
| real trace read | 0 |
| probe issue | 0 |

focused test 12件では正常composition、dependency hash drift、artifact間schema mismatch、path escapeおよび7種類の状態昇格拒否を確認した。

## 現在許可する次作業

private probe traceをmanifestで外部選択するreal-input revision、model-free composition r2およびprobe issuance preparation r3は完了した。r3は`ready_not_authorized`であり、次に必要なのはmodel利用とprivate実trace生成を伴うprobe発行を一回だけ許可するかという利用者の判断である。

実0.146.0 traceの読取り、`run-once`、r2 ticketの変更、issuance authority変更、probe発行、capability receipt、target登録および評価はまだ許可しない。

## 参照

- [`exact runtime preflight r2`](general-chat-agentic-exact-runtime-preflight-r2.md)
- [`synthetic file adapter設計`](general-chat-agentic-real-trace-adapter-design.md)
- [`capability preflight実行前契約`](general-chat-agentic-capability-preflight-plan.md)
- [`target登録前設計`](general-chat-agentic-target-preregistration-design.md)
- [`private trace adapter r1`](general-chat-agentic-private-trace-adapter-r1.md)
- [`model-free composition preflight r2`](general-chat-agentic-composition-preflight-r2.md)
- [`probe issuance preparation r3`](general-chat-agentic-issuance-preparation-r3.md)

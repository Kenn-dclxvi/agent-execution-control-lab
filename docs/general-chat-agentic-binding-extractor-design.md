# General chat agentic binding extractor入出力設計

> [!IMPORTANT]
> **状態**: `normalized_input_schema_fixed / output_schema_fixed / synthetic_13_passed / normalized_binding_evaluator_implemented / existing_primitives_identified / raw_normalizer_contract_fixed / synthetic_raw_fixture_fixed / synthetic_raw_normalizer_implemented / synthetic_file_adapter_implemented / model_free_composition_r1_passed / private_trace_adapter_shadow_verified / model_free_composition_r2_passed / issuance_preparation_r3_ready_not_authorized / raw_spawn_selector_unconfirmed / model_not_invoked`

## 結論

capability probeのbinding処理を、raw runtime traceを許可fieldへ変換するnormalizerと、その正規化traceから10 criterionを判定するbinding evaluatorへ分ける。今回実装したのは後者だけである。[`normalized input schema`](general-chat-agentic-binding-extractor-input.schema.json)を受け、[`output schema`](general-chat-agentic-binding-extractor-output.schema.json)に従って[`receipt schema`](general-chat-agentic-capability-preflight-receipt.schema.json)の`bindings`、`usage`および`criteria`へ投影する。

既存collectorからroot thread、parent-child関係、descendant terminal result、tool call / resultおよびall-agent usageの抽出方法は再利用できる。一方、spawn callへ入れたtask identityとpacket、spawn result、terminal senderおよびroot final responseを正規化fieldへ写すexact event selectorは未確認である。selectorを推測せず、[`synthetic trace fixture`](general-chat-agentic-binding-synthetic-traces-r1.json)の正常1件と反例12件で、正規化後のidentity chainだけを固定した。

## raw入力と現在実装の境界

将来のnormalizerは次のpathを一回のinvocationで受け取る。すべてprobe別の一時領域にあり、repositoryへcommitしない。

| 入力 | 必要内容 | authority |
| --- | --- | --- |
| ticket | probe identity、固定artifact identity、required observations | 固定ticket |
| root events | `thread.started`、spawn call / result、root tool call / result、root final response | Codex root JSONL |
| all-agent usage | rootとdescendantのthread、parent、source、rollout path、final usage | `all_agent_usage.py`のthread-bound出力 |
| descendant rollouts | session metadata、spawn source、terminal event | persisted rollout |
| task bytes | model-visible taskのexact bytes | ticket SHA-256 |
| fixture bytes | worker許可資料、root tool contract、final oracle | ticket SHA-256 |
| monotonic boundary | runner開始・terminal終了 | runnerの単調時計 |

入力pathはticketと同じprobe identityへbindする。別workspace、別root thread、別probe、推定tokenまたはraw会話履歴を補助入力にしない。

現在の[`general_chat_agentic_binding_extractor.py`](../scripts/general_chat_agentic_binding_extractor.py)はraw pathを受けず、syntheticであることを明示した正規化traceだけを受ける。CLIも`--synthetic-trace`以外のruntime入力optionを持たない。したがって、この実装をprobe runnerへ接続できない。

## 許可する出力

extractorが返せるのは次のfieldだけである。

```text
root_thread_id
spawn.call_id
spawn.requested_task_identity
spawn.returned_task_identity
spawn.child_thread_id
packet.sha256
packet.canonical_projection
packet.forbidden_field_count
packet.raw_transcript_required
descendant.thread_id
descendant.parent_thread_id
descendant.task_identity
descendant.terminal_sender
descendant.terminal_result_sha256
root_tool.tool_id
root_tool.call_id
root_tool.input_sha256
root_tool.terminal_status
root_tool.result_sha256
final_response.sha256
final_response.worker_result_directly_carried
final_response.root_tool_result_directly_carried
usage.root
usage.descendants
usage.all_agent_total
usage.complete
usage.duplicate_session_count
elapsed_ms
criteria
```

raw task message、raw worker result、raw tool result、raw final response、auth、request header、host pathおよびrollout pathは出力しない。canonical projectionが許可fieldだけで意味保持できない場合は、raw transcriptへ拡張せず`safe_projection_without_raw_transcript=unsatisfied`とする。

## identity chain

次の各辺を独立に確認し、前後の値が完全一致する場合だけ一つのbindingとする。

```text
ticket.probe_id
  → root thread.started.thread_id
  → spawn call.call_id + requested task identity
  → spawn result.call_id + returned task identity + child thread
  → descendant metadata.parent_thread_id + descendant source identity
  → descendant terminal sender + result hash
  → root final responseのworker result carrier

fixture.root_tool.tool_id
  → root tool call.call_id + input hash
  → root tool result.call_id + terminal status + result hash
  → root final responseのtool result carrier
```

task identityをagent pathの語似、worker本文、rootの進捗説明またはfinal responseから復元しない。call ID、thread IDまたはsenderが欠ければ該当criterionを`unobserved`にする。値が存在して矛盾する場合は`unsatisfied`にする。

## field別の抽出規則

### rootとusage

- root JSONLの一件の`thread.started.thread_id`をroot identityとする。0件または複数の異値は不成立。
- all-agent usageのroot identityが一致し、parent chainで到達可能なsessionだけを対象にする。
- thread ID重複、final usage欠落またはroot外session混入があればusageは不完全とする。
- tokenは既存`all_agent_usage.py`の一次値を使い、推定しない。

### spawnとpacket

- spawn callとspawn resultは同じcall IDで結ぶ。
- requested task identityは固定taskの`parking_fact_check`と完全一致させる。
- packet projectionは、task identity、workerの許可record ID、許可record本文およびrequired result shapeだけを持てる。
- root tool record、final response oracle、他record、repository instructionまたは会話履歴がpacketに含まれた場合は`forbidden_field_count`へ数える。
- spawn eventのexact item typeとfield pathはまだ固定しない。synthetic fixture前に既存traceの意味から補完しない。

### descendant terminal

- descendant metadataのthread ID、parent thread IDおよびspawn sourceをspawn resultへ対応づける。
- terminalはdescendant rolloutの`event_msg.payload.type=task_complete`と`last_agent_message`を候補とする。
- terminal senderはtask identityへ機械的に対応する独立fieldが必要である。agent pathの文字列類似だけではsender成立にしない。
- terminal eventが複数、sender欠落またはresult欠落ならterminal bindingは成立しない。

### root tool

- root eventsのcall / resultを同じcall IDで結び、tool IDを`fetch_branch_counter_hours`へ固定する。
- input hashとterminal result hashをfixtureから導いたcanonical JSON bytesへ照合する。
- nonterminal、複数result、call ID不一致または別tool resultの転用は不成立。

### final response

- root final responseはterminal response一件だけを対象にする。
- worker result carrierは、worker terminal resultが持つ結論値`18時まで駐車できる`と根拠値`18時30分`が一文目に存在することで判定する。
- root tool carrierは、terminal resultの`closes_at=17:00`に対応する`17時`が二文目に存在することで判定する。
- fixtureのoracleだけを満たしていても、対応するworkerまたはtool terminal resultが存在しなければ直接bindingを成立させない。
- 文面の意味をmodelに判定させず、固定値と文位置の決定的照合だけを使う。

## synthetic fixture gate

raw secretを含まない最小synthetic traceを作り、次を一件ずつ固定した。

1. 全identityとcarrierが一致する正常trace。
2. spawn callとresultのcall ID不一致。
3. requested task identityとreturned task identity不一致。
4. descendant parentがroot以外。
5. packetへroot tool recordが混入。
6. terminal sender欠落。
7. terminal result欠落または複数。
8. root tool call / result不一致。
9. final responseがworker値だけを欠落。
10. final responseがtool値だけを欠落。
11. descendant final usage欠落。
12. raw transcriptなしではpacket projection不能。

これら12項目のうち1を正常系、2から12を11反例とし、さらに重複root final responseを12件目の反例として追加した。計13件はすべて期待するcriterion stateとadmissionに一致した。ただしsynthetic passはruntime capabilityではなく、正規化後のbinding evaluator contractの単体検証に限る。

## 実装結果

- 入力schemaはraw rollout、auth、request headerおよび未許可top-level fieldを拒否する。
- evaluatorはtask identityを`parking_fact_check`へ固定し、call ID、thread ID、parent ID、sender、tool result、final carrier、usageおよびelapsedを決定的に判定する。
- terminal resultとroot final responseはhashだけを出力し、本文を出力しない。
- all-agent usageは全sessionのfinal一次値がある場合だけ合算し、一件でも欠ければ推定しない。
- output schemaは、全10 criterionが`satisfied`でない`available`ラベルと、全件`satisfied`の`unavailable`ラベルを拒否する。
- model invocation、Codex process、raw rollout readおよびrepository書込は行わない。

## 実装停止条件

- spawnのrequested task、returned task、packetおよびchild threadを一次eventから区別できない。
- terminal senderをagent pathの推測以外で取得できない。
- final response一件をterminal root responseとして一意に選べない。
- raw transcriptを保存しないとcriterionを再現できない。
- 既存collectorのCandidate固有判定を混ぜないと成立しない。

いずれかに該当した場合はextractorを完成扱いにせず、該当fieldを`unobserved`へ固定する。ticketのissuance authorityは変更しない。

## 現在許可する次作業

binding evaluatorからprobe issuance preparation r3まで完了し、r3は`ready_not_authorized`である。次に必要なのはmodel利用とprivate実trace生成を伴うprobe発行を一回だけ許可するかという利用者の判断である。許可されるまでは実runtime traceによるselector探索、`run-once`、authority変更、probe、target登録および評価を開始しない。

このsynthetic結果はCLI versionに依存しない。2026-08-20に観測したinstalled 0.148.0とr1 ticket 0.146.0の不一致を解消せず、normalizer実装だけでruntime probeへ進まない。

## 参照

- [`capability preflight実行前契約`](general-chat-agentic-capability-preflight-plan.md)
- [`ticket schema`](general-chat-agentic-capability-preflight-ticket.schema.json)
- [`receipt schema`](general-chat-agentic-capability-preflight-receipt.schema.json)
- [`all-agent usage collector`](../scripts/all_agent_usage.py)
- [`all-agent command evidence collector`](../scripts/all_agent_command_evidence.py)
- [`owner / producer evidence collector`](../scripts/owner_producer_evidence.py)
- [`fail-closed raw normalizer設計`](general-chat-agentic-raw-normalizer-design.md)

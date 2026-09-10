# General chat agentic fail-closed raw normalizer設計

> [!IMPORTANT]
> **状態**: `known_selector_ledger_fixed / synthetic_raw_fixture_fixed / expected_fail_closed_projection_fixed / synthetic_normalizer_implemented / synthetic_unit_passed / synthetic_file_adapter_implemented / model_free_composition_r1_passed / private_trace_adapter_shadow_verified / model_free_composition_r2_passed / issuance_preparation_r3_ready_not_authorized / real_trace_not_read / model_not_invoked`

## 結論

raw normalizerは、Codexのraw eventから値を推測してbindingを完成させる層ではない。既存collectorがすでに機械的に読んでいるfieldだけを[`normalized trace schema`](general-chat-agentic-binding-extractor-input.schema.json)へ写し、未確認のspawn、packet、sender、専用toolおよびroot final responseは空配列または`null`のまま返す。

今回固定した[`synthetic raw fixture`](general-chat-agentic-raw-normalizer-synthetic-r1.json)では、root identity、親子thread、descendant terminal本文、all-agent final usageおよび単調時計だけを入力に持つ。`agent_path=parking_fact_check`が見えていてもtask identityやsenderへ昇格させない。その結果、既存binding evaluatorは10 criterion中4件だけを`satisfied`、残り6件を`unobserved`とし、必ず`agentic_runtime_capability_unavailable`にする。

これはruntime capabilityの不成立結果ではない。normalizerが未確認fieldを補完せず停止できることを、synthetic入力限定の実装と単体テストで確認した結果である。

## selector台帳

| normalized field | raw source | 状態 | 扱い |
| --- | --- | --- | --- |
| `root.thread_started` | root JSONL `type=thread.started / thread_id` | 既存collectorで確認済み | 異なるIDが複数ならそのまま複数を渡す |
| session `thread_id` | 最初の`session_meta.payload.id`または`session_id` | 既存collectorで確認済み | 空または重複を補わない |
| session `parent_thread_id` | `session_meta.payload.parent_thread_id` | 既存collectorで確認済み | rootとの一致をnormalizerで推測しない |
| descendant terminal本文 | `event_msg.payload.type=task_complete / last_agent_message` | 既存collectorで確認済み | 本文は一時normalized inputだけへ渡し、最終projectionではhash化 |
| session final usage | 最後の`token_count.info.total_token_usage` | 既存collectorで確認済み | 欠落時はtokenを推定しない |
| monotonic boundary | runnerの`started_ms / ended_ms` | 契約済み | 逆転または欠落を補わない |
| requested task identity | spawn call | 未確認 | `null`またはcall自体を未観測にする |
| worker packet | spawn call | 未確認 | 空の`spawn_calls`とし、raw本文をpacket扱いしない |
| returned task / child | spawn result | 未確認 | 空の`spawn_results`とする |
| terminal sender | 独立sender field | 未確認 | `agent_path`から作らず`null` |
| root専用tool call / result | root tool event | 未確認 | command evidenceを専用tool resultへ転用しない |
| root terminal final response | root terminal event | 未確認 | descendant `task_complete`を転用しない |

## 入力境界

synthetic raw inputのschemaは[`general-chat-agentic-raw-normalizer-input.schema.json`](general-chat-agentic-raw-normalizer-input.schema.json)とする。許可するのは次だけである。

- 一件以上のroot `thread.started`候補。
- rootとdescendantの最初のsession metadata。
- descendantを含むsessionの`task_complete`候補。
- session別のfinal `token_count`候補。
- runnerが与える単調時計。

auth、request header、raw path、host path、repository content、全会話履歴、tool input、tool outputおよび任意eventをschemaへ通さない。実runtime用normalizerはraw fileを一時領域で読むが、schemaに合う最小projectionを作る前にrepositoryへ保存しない。

## fail-closed projection

synthetic raw fixtureから固定するnormalized traceは次の形である。

- `root.thread_started`は`root-thread-r1`一件。
- `spawn_calls / spawn_results / tool_calls / tool_results / final_responses`は空。
- descendantのthreadとparentは写すが、`task_identity`とterminal `sender`は`null`。
- terminal result本文はsynthetic input内だけに保持する。
- rootとdescendantのusageは一次値を写す。
- `raw_transcript_required=false`は、安全な最小projectionが可能という意味に限る。packetが観測済みという意味ではない。

binding evaluatorへ渡した期待結果は次のとおりである。

| criterion | 期待state |
| --- | --- |
| root thread identity | `satisfied` |
| spawn call and task identity | `unobserved` |
| worker packet projection | `unobserved` |
| descendant parent and task binding | `unobserved` |
| descendant terminal sender and result | `unobserved` |
| root tool call and terminal result | `unobserved` |
| final response direct binding | `unobserved` |
| all-agent final usage | `satisfied` |
| monotonic elapsed | `satisfied` |
| safe projection without raw transcript | `satisfied` |

従ってadmissionは`agentic_runtime_capability_unavailable`である。root、usage、elapsedが成立しても、未観測6件を成功扱いにしない。

## 禁止する補完

- `source.subagent.thread_spawn.agent_path`をrequested task、returned taskまたはterminal senderへコピーしない。
- descendant threadが一件だけでも、spawn resultのchild identityが観測されたことにしない。
- `last_agent_message`に期待値が含まれていてもsenderを成立させない。
- rootとdescendantの本文を組み合わせてroot final responseを再構成しない。
- command toolの成功を`fetch_branch_counter_hours`の成功へ読み替えない。
- 欠けたusageをroot processのtokenや差分から推定しない。

## 実装時のoperation

将来のnormalizerは次の一operationだけを持つ。

```text
normalize-known-fields
  input: temporary root events + selected persisted sessions + monotonic boundary
  output: normalized trace schema
```

raw file選択はprobe identity、workspace、root threadおよびparent chainへ事前にbindする。normalizerはsession探索、probe発行、retry、model invocation、admission判定またはreceipt sealingを担当しない。入力に未知eventがあっても意味推測せず無視し、必要な既知fieldが欠ければ空または`null`を返す。

## 実装結果

[`general_chat_agentic_raw_normalizer.py`](../scripts/general_chat_agentic_raw_normalizer.py)へ`normalize-known-fields`を実装した。CLIは固定synthetic fixtureだけを既定入力とし、raw rollout path、Codex executable、session rootまたはruntime optionを持たない。

- root `thread.started`候補を順序どおり保持する。異なるIDが複数ならrootを選ばない。
- session metadataのthreadとparentだけを写す。`source`と`agent_path`は出力しない。
- descendant `task_complete.last_agent_message`をterminal result候補へ写すが、senderは常に`null`とする。
- sessionごとに最後のfinal usageだけを写し、欠落時は全token fieldを`null`にする。
- spawn、packet、tool、root final responseは常に未観測の空配列とする。
- admission判定、receipt sealing、model invocationおよびrepository書込は行わない。

## 検証gate

次をmodelなしで確認した。

1. synthetic raw fixtureがraw input schemaを通る。
2. expected normalized traceが既存normalized input schemaを通る。
3. expected normalized traceを既存binding evaluatorへ渡すと、固定した10 stateとadmissionに一致する。
4. raw inputへauth、raw transcriptまたは任意top-level fieldを追加するとschemaが拒否する。
5. `agent_path`が存在してもexpected normalized traceのtask identityとsenderは`null`である。

このgateの通過はsynthetic normalizer実装済みを意味するが、real trace adapter、未確認runtime selectorまたはcapability利用可能を意味しない。

## 現在許可する次作業

synthetic normalizerからprobe issuance preparation r3まで完了し、r3は`ready_not_authorized`である。次に必要なのはmodel利用とprivate実trace生成を伴うprobe発行を一回だけ許可するかという利用者の判断である。許可されるまでは実runtime traceの読取り、未確認selector探索、`run-once`、authority変更、probe、target登録および評価を開始しない。

## 参照

- [`binding extractor入出力設計`](general-chat-agentic-binding-extractor-design.md)
- [`normalized input schema`](general-chat-agentic-binding-extractor-input.schema.json)
- [`synthetic binding fixture`](general-chat-agentic-binding-synthetic-traces-r1.json)
- [`capability preflight実行前契約`](general-chat-agentic-capability-preflight-plan.md)
- [`all-agent usage collector`](../scripts/all_agent_usage.py)
- [`owner / producer evidence collector`](../scripts/owner_producer_evidence.py)
- [`real trace adapter入出力設計`](general-chat-agentic-real-trace-adapter-design.md)

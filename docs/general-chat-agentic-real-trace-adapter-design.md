# General chat agentic real trace adapter入出力設計

> [!IMPORTANT]
> **状態**: `input_identity_fixed / synthetic_file_packet_fixed / known_field_projection_fixed / unknown_selectors_fail_closed / synthetic_adapter_implemented / focused_12_passed / model_free_composition_r1_passed / private_trace_adapter_shadow_verified / model_free_composition_r2_passed / issuance_preparation_r3_ready_not_authorized / real_trace_not_read / model_not_invoked`

## 結論

[`general_chat_agentic_real_trace_adapter.py`](../scripts/general_chat_agentic_real_trace_adapter.py)は、sessionを探索してprobeへ関連づける機能を持たないsynthetic file packet限定adapterとして実装した。事前に一意にbindしたroot events一件、root thread、workspace、選択済みsession集合および単調時計だけを受け取り、既存collectorで確認済みのfieldを既存normalizerと同じ意味へ投影する。

spawn task、packet、spawn result、terminal sender、専用toolおよびroot final responseのexact selectorは未確認なので、adapterはそれらを探したり推測したりしない。現在の[`synthetic normalizer`](../scripts/general_chat_agentic_raw_normalizer.py)へ渡せる既知fieldだけを作り、unknown selectorは後続criterionを`unobserved`にする。

## 入力identity

runnerはadapter起動前に次を一つのinput manifestへbindする。

| field | 必須値 | 境界 |
| --- | --- | --- |
| `probe_id` | `general-chat-agentic-capability-preflight-r2` | 別probeを混ぜない |
| `runtime_id` | exact 0.146.0 runtime ID | aliasを再解決しない |
| `workspace` | probe別一時workspaceのcanonical path | repositoryへ保存しない |
| `root_events` | 一件のpath、SHA-256、byte数 | stdout JSONL以外を混ぜない |
| `root_thread_id` | root eventsの`thread.started`から取得した一意値 | 推測しない |
| `sessions` | thread ID、parent ID、path、SHA-256、byte数の固定配列 | rootからparent chainで到達する集合だけ |
| `monotonic` | runner start / terminal end | wall clockへ置換しない |

adapterはsession root、`CODEX_HOME`全体、filesystem glob、mtime範囲またはworkspace名から入力を再探索しない。session集合が未固定、重複、root欠落またはparent chain外を含む場合は起動しない。

## 一時raw入力

adapterは入力manifestで指定されたfileだけをread-onlyで開き、次を一時memoryへ読む。

- root JSONLの`thread.started`。
- 各rolloutの最初の`session_meta`。
- 各rolloutの`event_msg.payload.type=task_complete`。
- 各rolloutの最後の`event_msg.payload.type=token_count`。

JSON不正、file hash drift、同一threadの複数file、metadata identity不一致またはfinal usage欠落を別fileで補わない。raw bytes、raw path、auth、request header、全会話本文および未知eventをrepository outputへ含めない。

## normalized出力

出力はr1 schemaを変更せず、probe r2専用の[`general-chat-agentic-binding-extractor-input-r2.schema.json`](general-chat-agentic-binding-extractor-input-r2.schema.json)へ適合させる。r1とr2は`probe_id`を混ぜず共存する。

- `root.thread_started`: 観測した候補をそのまま保持。
- `descendants`: metadataのthread / parentと、terminal本文候補。`task_identity=null`、`sender=null`。
- `usage`: session別のfinal一次token。欠落は全token field `null`。
- `monotonic`: runnerがbindした値。
- `projection.raw_transcript_required=false`: 既知fieldの最小projectionがraw保存なしで作れたことだけを示す。
- `spawn_calls / spawn_results / tool_calls / tool_results / final_responses`: 空配列。

`agent_path`、subagent source、tool名らしい文字列、terminal本文またはthreadの一意性から未確認fieldを生成しない。

## 一時保存と削除

adapter outputはcapability receiptではなく、一時normalized inputである。binding evaluatorがhashと許可projectionを作り、receipt schema検証が終わるまでprivate領域に保持できる。seal前の失敗でもrawをpublic artifactへ移さない。

削除順は次に固定する。

1. input file hashを再確認する。
2. normalized outputとbinding outputをschema検証する。
3. unavailableを含むreceipt候補へ全criterionをbindする。
4. receiptをwrite-onceでsealする。
5. raw root events、rollout copyおよびnormalized本文を削除する。

adapter単体は削除、sealまたはretryを担当しない。

## fail-closed状態

| 観測 | adapter出力 |
| --- | --- |
| root `thread.started`なし | `ROOT_THREAD_ID_MISMATCH` |
| root ID複数 | `ROOT_THREAD_ID_MISMATCH` |
| session metadataなし | そのfileをidentityへbind不能としてadapter error |
| task identity不明 | `task_identity=null` |
| terminal sender不明 | `sender=null` |
| terminal本文なし | `terminal_events=[]` |
| final usageなし | token fieldsを`null` |
| unknown eventだけ存在 | 無視し、既知fieldを補完しない |
| raw保存が必要 | adapter outputを作らず安全projection不能 |

adapter errorをcapability available、external retryまたは別session resultで補わない。

## synthetic実装gateの結果

input manifest schema、hash・byte数付きsynthetic file packet、root events、root / child sessionを固定し、次を単体試験で確認した。

1. manifestにないfileを読まない。
2. path、hash、byte数、thread、parentの不一致を個別に拒否する。
3. parent chain外sessionを拒否する。
4. unknown eventを無視しても既知fieldが変わらない。
5. `agent_path`をtask identityまたはsenderへ写さない。
6. raw本文やhost pathをnormalized outputへ含めない。
7. adapter outputを既存normalizer・binding evaluatorへ渡すとunavailableのままになる。

2026-08-20にfocused test 12件が通過した。正規化結果をbinding evaluatorへ渡した結果は、root identity、all-agent final usage、monotonic elapsedおよび安全projectionだけが`satisfied`で、未確認のspawn、packet、task identity、terminal sender、tool resultおよびroot final responseは`unobserved`のまま、admissionは`agentic_runtime_capability_unavailable`となる。

このgateの通過はreal runtime traceへのselector成立、probeまたはtarget評価の許可ではない。adapterはmanifest外の探索、実session読取り、runtime起動、model invocation、raw保存、receipt sealおよび削除を行わない。

## 現在許可する次作業

private trace adapter、model-free composition r2およびprobe issuance preparation r3まで通過し、r3は`ready_not_authorized`である。次に必要なのはmodel利用とprivate実trace生成を伴うprobe発行を一回だけ許可するかという利用者の判断である。許可されるまでは追加artifact、実0.146.0 traceの読取り、unknown selector探索、`run-once`、authority変更、probe、target登録および評価を開始しない。

## 参照

- [`fail-closed raw normalizer設計`](general-chat-agentic-raw-normalizer-design.md)
- [`binding extractor設計`](general-chat-agentic-binding-extractor-design.md)
- [`exact runtime preflight r2`](general-chat-agentic-exact-runtime-preflight-r2.md)
- [`model-free composition preflight r1`](general-chat-agentic-composition-preflight-r1.md)
- [`private trace adapter r1`](general-chat-agentic-private-trace-adapter-r1.md)
- [`model-free composition preflight r2`](general-chat-agentic-composition-preflight-r2.md)
- [`probe issuance preparation r3`](general-chat-agentic-issuance-preparation-r3.md)
- [`CLI version共存試験環境設計`](codex-cli-version-coexistence-environment-design.md)

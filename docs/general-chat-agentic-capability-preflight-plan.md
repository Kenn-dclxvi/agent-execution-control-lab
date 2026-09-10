# General chat agentic capability preflight実行前契約

> [!IMPORTANT]
> **状態**: `contract_fixed / task_and_fixture_frozen / r1_ticket_preserved / exact_runtime_r2_verified / r2_ticket_not_authorized / exact_runtime_negative_6_passed / normalized_binding_evaluator_implemented / synthetic_13_passed / synthetic_raw_normalizer_implemented / synthetic_file_adapter_implemented / adapter_focused_12_passed / model_free_composition_r1_passed / private_trace_adapter_shadow_verified / model_free_composition_r2_passed / issuance_preparation_r3_ready_not_authorized / real_runner_not_implemented / model_not_invoked / receipt_not_created / target_not_registered`

## 結論

`general-chat-agentic-control`のtarget登録可否を判断する前に、Codex CLI 0.146.0がtask identity、worker packet、親子thread、terminal sender、returned result、root tool result、final responseおよびall-agent usageを一つの安全なreceiptへ結べるかを、一回限りの非評価probeで確認する。

probeの入力と保存契約に加え、modelを呼ばない静的validator、正規化binding evaluator、synthetic trace gateおよびsynthetic file packet限定adapterを固定した。ticketの`issuance_authority`は`not_authorized`であり、real runnerを実装せず、modelを呼ばず、capability receiptを作らない。この契約の静的検証とsynthetic gateが通ってもagentic capability、C147 coverage、Candidate効果またはtarget登録資格は成立しない。

## 固定したアーティファクト

| アーティファクト | 役割 | 固定状態 |
| --- | --- | --- |
| [`general-chat-agentic-capability-preflight-task-r1.txt`](general-chat-agentic-capability-preflight-task-r1.txt) | model-visible taskのexact bytes | SHA-256とbyte数をticketへ固定 |
| [`general-chat-agentic-capability-preflight-fixture-r1.json`](general-chat-agentic-capability-preflight-fixture-r1.json) | worker許可資料、root tool result、final response oracle | SHA-256とbyte数をticketへ固定 |
| [`general-chat-agentic-capability-preflight-ticket-r1.json`](general-chat-agentic-capability-preflight-ticket-r1.json) | runtime、必要観測、発行回数、保存境界 | `not_authorized` |
| [`general-chat-agentic-capability-preflight-ticket.schema.json`](general-chat-agentic-capability-preflight-ticket.schema.json) | ticketの機械検証 | Draft 2020-12 |
| [`general-chat-agentic-capability-preflight-receipt.schema.json`](general-chat-agentic-capability-preflight-receipt.schema.json) | 成立・不成立を同じfieldで保存するwrite-once形式 | receipt未作成 |
| [`general-chat-agentic-capability-negative-fixtures-r1.json`](general-chat-agentic-capability-negative-fixtures-r1.json) | 発行前に拒否すべき16状態 | model invocationなしで判定 |

taskは`parking_fact_check`だけをworkerのtask identityとして事前指定し、駐車場資料だけをworkerへ渡す。rootは独立した支店窓口toolを使い、final responseはworker resultとroot tool resultを二文へ運ぶ。これは委任を良くするpromptの評価ではなく、必要なidentityとbindingをruntimeから観測できるかだけを測る診断である。

## 静的admission

runnerが将来probeを発行する前に、次をこの順で判定する。

1. ticketとschemaのbytesが一致し、ticket自身がschemaを通る。
2. taskとfixtureのpath、SHA-256、byte数がticketと一致する。
3. runtime、model、reasoning、permission、multi-agent、persisted session、instruction isolationおよびtrace capabilityが全件一致する。
4. 同じ`probe_id`のreceipt、発行記録または予約済み実行が存在しない。
5. `issuance_authority=authorized_not_issued`である。

1から4の失敗は具体的なrejection codeで停止する。5が満たされない現在は`ISSUANCE_NOT_AUTHORIZED`で停止する。静的admissionではmodel、tool fixtureまたはCodex sessionを起動しない。

## negative fixtureの判定

negative fixtureは固定base ticketへ一件だけJSON Pointerの置換を適用する。全16件について、変更後ticketがschema不適合になり、かつpointerに対応した`expected_rejection`を一意に返せることを要求する。

schema不適合という一般結果だけで通過にしない。例えば`multi_agent=false`は`MULTI_AGENT_DISABLED`、packetの安全なprojection不能は`SAFE_PACKET_PROJECTION_UNAVAILABLE`として区別する。複数mutation、modelによる意味判定またはraw transcriptは使わない。

## receiptの完了規則

将来一回だけ発行した場合は、成功と不足のどちらでも同じreceipt schemaへ保存する。

- 10 criterionは` satisfied / unsatisfied / unobserved`のいずれかを持つ。
- 10件すべてが`satisfied`で、processがterminal、usageが完全、重複sessionが0、禁止fieldが0、raw transcriptが不要な場合だけ`agentic_runtime_capability_available`とする。
- 一件でも`unsatisfied`または`unobserved`なら`agentic_runtime_capability_unavailable`とする。
- 不足値をモデルの自己申告、root final response、別sessionまたは再発行で補わない。
- receiptはwrite-onceとし、同じprobe identityを再発行しない。
- receiptの`evaluation_effect`は常に`false`とする。

不成立receiptもruntime limitationの一次診断として保持するが、評価result、baselineまたはCandidate反例へ転用しない。

## 静的validatorの実装結果

[`general_chat_agentic_capability_preflight.py`](../scripts/general_chat_agentic_capability_preflight.py)は次の二operationだけを実装した。

- `validate-ticket`: schema、artifact identity、runtime contract、既存identityおよびissuance authorityを検証する。
- `validate-negative-fixtures`: base ticketへ16 mutationを一件ずつ適用し、固有rejection codeを確認する。

validatorは`codex --version`をmodel-free inventoryとして取得し、ticketのruntime identityと照合する。ticketと一致する`codex-cli 0.146.0`を与えた単体試験ではcontractとartifact identityを通過した後、`ISSUANCE_NOT_AUTHORIZED`で停止する。2026-08-20現在のinstalled CLIは`codex-cli 0.148.0`であるため、実commandはそれより前の`RUNTIME_VERSION_MISMATCH`で停止する。ticketを0.148.0へ自動更新せず、0.146.0で得た既存結果も読み替えない。

negative fixtureは16 / 16件が指定した固有reasonで拒否される。両operationの`model_invocations`は`0`であり、model request、tool fixtureおよびCodex sessionを起動しない。`validate-ticket`が起動するCodex commandはversion inventoryだけである。

```bash
.venv/bin/python scripts/general_chat_agentic_capability_preflight.py validate-ticket
.venv/bin/python scripts/general_chat_agentic_capability_preflight.py validate-negative-fixtures
```

## runner設計

runner実装は別作業とし、現在は存在しない。静的validatorが先行二operationを実装したが、`run-once`は持たない。将来の全体runnerは次の三operationに限定する。

### `validate-ticket`

ticket schema、artifact identity、runtime inventory、instruction isolation、既存発行identityおよびissuance authorityを検証する。`not_authorized`を含む一件の失敗でterminalにし、probeを発行しない。

### `validate-negative-fixtures`

base ticketのcopyへ各mutationを一件ずつ適用し、schema rejectionと個別rejection codeを確認する。base ticket、task、fixtureまたはschemaを書き換えない。

### `run-once`

`validate-ticket`通過後だけ、一時workspaceとprobe別のpersisted temporary `CODEX_HOME`を作る。authは一時参照に限りreceiptへ保存しない。Codex execはroot JSONLを一件だけ発行し、同じprocessのterminalまで待つ。raw rolloutから許可fieldを抽出し、hashとcanonical projectionを照合してreceiptを一度だけsealした後、raw sessionを破棄する。

既存の`all_agent_usage.py`と`all_agent_command_evidence.py`から使うのは、thread-bound usageとcall/result identityの抽出方法だけである。既存Case、Candidate固有期待値または保存resultを入力にしない。spawnからfinal responseまでのtarget固有binding extractorは別に必要であり、それが未実装なら発行しない。

## 発行後の停止規則

- process nonzero、terminal欠落、criterion不足、usage欠落または安全なprojection不能のいずれでも後続を止め、不成立receiptをsealする。
- environment recoveryとretryは行わない。transportの設計欠陥が事前に見つかった場合は、このprobeを発行せず別identityの契約から再設計する。
- available receiptができても、許可されるのはtarget descriptor、Case、Profile、ratingおよびevaluation preflightの作成可否を次に判断することだけである。
- target登録、baseline発行、Candidate作成、評価slot発行、採用、releaseおよびprojectionは自動では許可しない。

## 現在の次作業境界

静的validator、synthetic trace 13件、正規化binding evaluator、synthetic raw normalizer、[`exact 0.146.0 runtime preflight r2`](general-chat-agentic-exact-runtime-preflight-r2.md)、synthetic file packet限定adapter、[`model-free composition preflight r1`](general-chat-agentic-composition-preflight-r1.md)、private trace adapter、[`model-free composition preflight r2`](general-chat-agentic-composition-preflight-r2.md)および[`probe issuance preparation r3`](general-chat-agentic-issuance-preparation-r3.md)は固定した。r3は`ready_not_authorized`である。次に必要なのはmodel利用とprivate実trace生成を伴うprobe発行を一回だけ許可するかという利用者の判断である。許可されるまではruntime 0.148.0検討、追加ticket、`run-once`、authority変更、probe、target descriptor、Case、Profile、baselineおよびCandidateを開始しない。

## 参照

- [`General chat agentic control target登録前設計`](general-chat-agentic-target-preregistration-design.md)
- [`C147チャット向けcoverage architecture r1`](general-chat-c147-coverage-architecture-r1.md)
- [`binding extractor入出力設計`](general-chat-agentic-binding-extractor-design.md)
- [`fail-closed raw normalizer設計`](general-chat-agentic-raw-normalizer-design.md)
- [`exact 0.146.0 runtime preflight r2`](general-chat-agentic-exact-runtime-preflight-r2.md)
- [`real trace adapter設計`](general-chat-agentic-real-trace-adapter-design.md)
- [`model-free composition preflight r1`](general-chat-agentic-composition-preflight-r1.md)
- [`private trace adapter r1`](general-chat-agentic-private-trace-adapter-r1.md)
- [`model-free composition preflight r2`](general-chat-agentic-composition-preflight-r2.md)
- [`probe issuance preparation r3`](general-chat-agentic-issuance-preparation-r3.md)
- [`プロンプト制御設計原則`](prompt-control-design-principles.md)

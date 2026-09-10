# General chat agentic control target登録前設計

> [!IMPORTANT]
> **状態**: `runtime_candidate_0_146_0_selected / exact_runtime_r2_verified / installed_runtime_0_148_0_unassessed / capability_contract_fixed / r2_ticket_not_authorized / normalized_binding_evaluator_implemented / synthetic_13_passed / synthetic_raw_normalizer_implemented / synthetic_file_adapter_implemented / adapter_focused_12_passed / model_free_composition_r1_passed / private_trace_adapter_shadow_verified / model_free_composition_r2_passed / issuance_preparation_r3_ready_not_authorized / real_runner_not_implemented / capability_receipt_not_created / target_not_registered / cases_not_frozen / evaluation_not_started`

## 結論

`general-chat-agentic-control`の最初のformal runtime候補はCodex CLI 0.146.0とする。現在のローカルCLIでは`multi_agent`がstableであり、既存評価基盤はrootとdescendantのpersisted rolloutから一次token、parent-child thread、tool call、tool result、nonterminal continuationおよびterminal task resultを抽出できる。

ただし、一般チャットcoverageに必要な次の一続きの証跡は、target固有のcapability receiptとして未固定である。

```text
prebound task identity
→ spawn resultのtask identity
→ workerへ渡したpacket bytes
→ descendant thread identityとparent identity
→ terminal sender
→ returned result identity
→ root final responseへの直接binding
```

この証跡が一つの非評価preflightで成立するまでtarget descriptor、Case、Profile、baselineおよび評価slotを作成しない。semantic ledgerやモデルの自己申告で補わない。固定task、fixture、ticket、negative fixtureおよびreceipt schemaは[`capability preflight実行前契約`](general-chat-agentic-capability-preflight-plan.md)へ分離したが、ticketは`not_authorized`でありprobeは未発行である。

## 対象surface

このtargetが最初に判定するのは、Codex CLI上のagentic chat surfaceだけである。ChatGPT UI、ChatGPT Project、他社chat surfaceまたは一般的な全AI assistantへ結果を投影しない。

利用者向けtaskは、相談、比較、固定資料の確認、要約および決定的な小処理とする。成果としてrepository変更、コード生成、testまたはdiffを要求しない。ただしformal runtimeのtoolとtraceを第三者が再現できるよう、公開repositoryの隔離workspaceへ決定的なfixtureと小toolを配置する。

fixture repositoryは実行transportであり、コード変更工程をpromptのrequired effectへ戻さない。

## ローカルで観測したruntime候補

2026-08-19のローカルinventoryは次のとおりである。ただし2026-08-20にinstalled CLIが`codex-cli 0.148.0`へ変わったことを静的validatorが観測した。下表とr1 ticketは0.146.0候補の固定記録として保持し、0.148.0のcapabilityを未確認のまま代入しない。

| 項目 | 観測値 | 登録前判定 |
| --- | --- | --- |
| CLI | `codex-cli 0.146.0` | candidate runtimeへ固定可能 |
| model / reasoning | `gpt-5.6-sol / medium` | Profileへ固定する候補 |
| multi-agent | feature `multi_agent: stable / true` | capability probe対象 |
| persisted session | `--ephemeral`を付けないexecでrollout保存可能 | all-agent計測に必須 |
| root JSONL | `thread.started`、tool item、terminal usage | root identityと一次result候補 |
| descendant relation | rollout `parent_thread_id`とsubagent source | parent-child binding候補 |
| descendant terminal | rollout `task_complete.last_agent_message` | terminal result候補 |
| all-agent token | `scripts/all_agent_usage.py`のthread-bound v2 | Profileへ固定する候補 |
| root / descendant tool evidence | `scripts/all_agent_command_evidence.py` | tool trace基礎として再利用候補 |
| producer evidence | `scripts/owner_producer_evidence.py` | task-specific extractorへ一般化が必要 |
| nonterminal continuation | `write_stdin`と同一session IDの既存抽出 | Case traceで再確認が必要 |

CLIのfeature表示、既存scriptの存在または過去runの成功だけでは、新targetのcapability passにしない。新targetと同じinstruction isolation、permission、workspace、persisted homeおよびtrace exportで一件のpreflightを行う。

## target identity候補

| 項目 | 登録前候補 |
| --- | --- |
| target ID | `general-chat-agentic-control` |
| target kind | `repository` |
| layout | `namespaced` |
| executor | Codex CLI |
| repository | 公開`agent-execution-control-lab`の登録時immutable commit / tree |
| Case fixture | target既存機能と独立したCase別workspace overlay |
| prompt delivery | isolated workspaceのroot `AGENTS.md` |
| permission | `workspace-write / approval_policy=never` |
| instruction isolation | user config、user rules、memories、apps、plugins、plugin sharingを無効化 |
| multi-agent | 有効、`agents.max_threads=4`候補 |
| session | run別の一時`CODEX_HOME`にpersistし、証跡抽出後にraw sessionを破棄 |
| token | thread-bound all-agent一次token |
| elapsed | adapter startからroot terminal process resultまでの単調時計 |

登録時commit、tree、fixture hash、CLIのmodel-visible capability catalogおよび全contract hashが決まるまで、この表をtarget descriptorへ転記しない。

## fixture tool境界

toolは、Caseの答えをpromptへ埋め込まず、決定的なresultと失敗形を返す小さい実行surfaceにする。

- `fetch_primary_record`: 指定された一次資料だけを返す。
- `fetch_related_record`: 関連するが回答を変えないdecoy資料を返す。
- `compare_values`: 固定入力から決定的な比較resultを返す。
- `validate_content`、`validate_numbers`、`validate_format`: 固定planの個別validationを返す。
- `long_running_check`: 最初はnonterminal identity、同一identityのcontinuationでterminal resultを返す。
- `environment_sensitive_check`: Case authorityに応じ、environment failureと一回の復旧を区別する。

実装名はCase source freeze前の仮称である。shell commandの成功順をCandidate promptへ書かず、TaskSpecは利用可能な能力、required outcome、明示permission、依存関係およびstop conditionだけを自然な利用者依頼とruntime contractへ分けて渡す。

## capability preflight

formal Caseではない固定非評価probeを一件だけ設計する。probeは品質、C147 coverage、Candidate効果または3 KPI比較へ使わない。

### model-visible task

- rootへ二つの独立した小判断を依頼する。
- 一方だけを明示task identityでworkerへ委任する。
- worker packetには必要なfixture一件と返却形式を含める。
- rootは別の独立toolを実行する。
- worker resultとroot tool resultの両方を自然なfinal responseへ運ぶ。

期待identity、禁止経路、oracle、trace field名またはC147制御名をtask本文へ含めない。

### admission

次を全件同じreceiptへbindできる場合だけ`agentic_runtime_capability_available`とする。

1. root thread identityが一件である。
2. spawn tool callとspawn resultからtask identityを取得できる。
3. worker packet bytesまたは意味保持したcanonical projectionを取得できる。
4. descendant threadはrootをparentとし、task identityへ一意に対応する。
5. descendant terminal resultはsenderとresult hashを持つ。
6. rootの独立tool callとterminal resultを取得できる。
7. root final responseは一件で、worker resultとroot tool resultを直接運ぶ。
8. rootと全descendantのfinal token usageを重複なく合算できる。
9. elapsed境界を取得できる。
10. raw transcript、auth、非公開入力をcommitせず、許可fieldだけを保存できる。

一項目でも欠けた場合は`agentic_runtime_capability_unavailable`とする。同じprobe identityを再発行せず、不足fieldとruntime limitationを保存する。

## negative preflight fixture

capability receiptを作る前に、次をmodel invocationなしで拒否できることを確認する。

- `multi_agent=false`
- `agents.max_threads < 2`
- persisted session無効
- descendant rollout export不能
- parent thread identity欠落
- task identityまたはterminal senderを抽出不能
- all-agent final usage欠落
- tool call / result identity欠落
- raw transcript以外にpacketを安全に投影できない
- runtime、model、reasoning、permissionまたはinstruction isolationがProfileと不一致

negative fixtureの通過はagentic capability成立ではなく、不成立状態でslotを拒否できる証拠に限る。

## trace保存境界

repositoryへ保存できるのは、target-specific schemaで許可した派生証拠だけとする。

- thread ID、parent thread ID、task identity、sender identity
- packet SHA-256、許可fieldのcanonical projection、禁止field検出件数
- tool identity、call identity、input identity、terminal status、result SHA-256
- nonterminal invocation identityと同一identity continuation
- final response、final response SHA-256
- root、descendant別usageとall-agent total
- monotonic elapsed
- oracleが必要とする発行、未発行、重複、順序、dependencyおよびbinding診断

auth、request header、raw session transcript、無関係な会話履歴、fixture外のhost pathおよび一時`CODEX_HOME`はcommitしない。raw rolloutは採点と派生証拠のhash確認が終わるまで一時領域に保持し、result sealing後に削除する。

## 再利用するものと新規に必要なもの

### 再利用候補

- `scripts/all_agent_usage.py`: thread-bound all-agent token集計。
- `scripts/all_agent_command_evidence.py`: root / descendant tool callとresultの抽出方法。
- `scripts/run_codex_evaluation.py`: persisted session、instruction isolation、multi-agent起動および外部失敗分類の実績。

再利用はtarget-independentな計測primitiveに限る。THE-CAPTION Case、Rating、TaskSpec、prompt bundle、保存resultまたはcommand期待値を混ぜない。

### target固有に新規作成するもの

- agentic runtime capability contract。
- capability preflight ticket、negative fixture、runnerおよびwrite-once receipt。
- spawn / packet / terminal sender / result / final response binding extractor。
- 一般チャット用tool fixtureとCase materializer。
- final response品質とtrace mechanismを分離するrating contract。
- Case、oracle、set、Profile、preflightおよびresult schema。

これらはcapability preflight設計が固定される前に実装しない。

## 比較境界

- control-free baselineと後続Candidateは同じtarget、Case、fixture、TaskSpec、runtime、model、reasoning、permission、trace extractor、token accountingおよび集計を使う。
- prompt identityだけを比較変数にする。
- `general-chat-response-control`、THE-CAPTION、portable semanticまたはvalidation carrierのscore、token、elapsedを比較元にしない。
- 既存runはcapability形状の設計入力にだけ使い、新targetのqualification resultへ再利用しない。

## 停止条件

次のいずれかがあればtarget登録前で停止する。

- task identity、packet、senderおよびresultを一つのproducer bindingへ対応づけられない。
- rootとdescendantの全usageを一次値で取得できない。
- raw transcriptを保存しないとoracleを判定できない。
- Case固有の正解routeをTaskSpecまたはpromptへ見せないと実tool経路を作れない。
- required normal routeと閉じるrouteを同じpermissionでしか表せない。
- 実tool surfaceを使わずsemantic自己申告へ戻る。
- 公開fixtureと再現可能なruntime contractを固定できない。

停止はC147チャットcoverageの解決を意味しない。別runtime surfaceまたは別の安全なtrace projectionを検討するが、外部executor変更をprompt解決策として扱わない。

## 現在許可する次作業

capability preflightのticket、negative fixture、保存schema、静的validator、runner設計、synthetic trace 13件、正規化binding evaluator、synthetic raw normalizer、exact 0.146.0 runtime preflight r2、synthetic file packet限定adapter、model-free composition r1、private trace adapter、model-free composition r2およびprobe issuance preparation r3は固定した。r3は`ready_not_authorized`である。次に必要なのはmodel利用とprivate実trace生成を伴うprobe発行を一回だけ許可するかという利用者の判断である。許可されるまでは0.148.0の別revision、追加ticket、`run-once`、authority変更、model invocation、target descriptor、Case freeze、baseline bundle、Profile、評価preflight、Candidateおよび評価slotを開始しない。

## 参照

- [`C147チャット向けcoverage architecture r1`](general-chat-c147-coverage-architecture-r1.md)
- [`capability preflight実行前契約`](general-chat-agentic-capability-preflight-plan.md)
- [`binding extractor入出力設計`](general-chat-agentic-binding-extractor-design.md)
- [`fail-closed raw normalizer設計`](general-chat-agentic-raw-normalizer-design.md)
- [`exact 0.146.0 runtime preflight r2`](general-chat-agentic-exact-runtime-preflight-r2.md)
- [`real trace adapter設計`](general-chat-agentic-real-trace-adapter-design.md)
- [`model-free composition preflight r1`](general-chat-agentic-composition-preflight-r1.md)
- [`private trace adapter r1`](general-chat-agentic-private-trace-adapter-r1.md)
- [`model-free composition preflight r2`](general-chat-agentic-composition-preflight-r2.md)
- [`probe issuance preparation r3`](general-chat-agentic-issuance-preparation-r3.md)
- [`Codex validation carrier実行target登録設計`](codex-validation-carrier-target-registration-design.md)
- [`all-agent usage collector`](../scripts/all_agent_usage.py)
- [`all-agent command evidence collector`](../scripts/all_agent_command_evidence.py)
- [`Codex evaluation adapter`](../scripts/run_codex_evaluation.py)
- [`プロンプト制御設計原則`](prompt-control-design-principles.md)

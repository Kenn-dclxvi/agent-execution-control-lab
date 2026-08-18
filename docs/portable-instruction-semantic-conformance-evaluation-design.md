# Portable instruction semantic conformance評価設計

> [!IMPORTANT]
> **状態**: `common_case_contract_r2_fixed / tuning_cases_8_fixed / held_out_cases_14_fixed / surface_load_receipts_not_collected / formal_target_registered / codex_profile_r4 / control_free_valid_14 / score4_5 / mechanism_passed_5 / measurement_gate_passed`
>
> 本書は、C147由来portable kernelのsemantic portabilityとbehavioral portabilityをsurface別に診断する共通Caseを固定する。exact prompt本文、Candidate、正式なtarget instance、評価result、採用、releaseまたはprojectionではない。

## 結論

全surfaceへ同じmodel-visible Caseを渡すため、実repositoryやtool APIではなく、明示的なoperation ledgerを使う一回応答型のsemantic conformance protocolを作る。各Caseは「次に合法な操作集合」を返させ、oracleは必要な正の遷移と禁止操作を別々に判定する。

ChatGPT Project、Gemini GemなどのUI surfaceでは、同一kernelのloadとCase応答は観測できても、現時点でall-agent `total_tokens`の一次値を取得する経路が固定されていない。したがって次を分ける。

1. **surface diagnostic receipt**: load identity、Case入力、応答、開始・終了時刻およびsurface capabilityを保存する。3 KPIが欠ける間は正式resultへ登録しない。
2. **formal runtime result**: `quality_score`、all-agent `total_tokens`、`elapsed_seconds`を一次値として取得でき、他のcompatibility conditionも固定できるruntimeだけをnamespaced targetの正式系列へ入れる。

tokenを推定、文字数から換算または別modelのtokenizerで補正しない。surface diagnostic receiptを正式result、比較証拠、採用証拠または他surfaceへの一般化に使わない。

## 測るもの

### 対象

- outcomeとmethodの分離
- observationのconsumer eligibility
- result effectの局所化
- actor/result provenance
- frontierの正の発行とpartial result非消費
- validation plan、個別resultおよびfail-fast
- nonterminal invocationの継続
- recovery allowanceのauthority

### 対象外

- repository path探索、実file変更、実command実行
- surface固有toolの性能
- prompt loading自体の強制力
- security permissionまたはhookによるmachine enforcement
- runtime間のquality score、tokenまたはelapsedの絶対値比較
- C147のTHE-CAPTION resultとの互換比較
- 自然文と形式記法のcost比較。これはkernel identity固定後の別変更軸とする

## 共通protocol

### model-visible入力

各Caseは次のJSON objectをmodel-visible入力とする。key名とenumはCase revision内で固定し、surface別に変えない。

```json
{
  "case_id": "PIC-Q01",
  "request_contract": {
    "required_outcomes": [],
    "authorities": [],
    "permissions": [],
    "stop_conditions": []
  },
  "operations": [],
  "received_results": [],
  "available_capabilities": [],
  "required_response_schema": "portable-instruction-control-response/r2"
}
```

`operations`は少なくとも次を持つ。

```json
{
  "operation_id": "op-1",
  "class": "clarification | observation | action | validation | recovery",
  "predicate_state": "satisfied | unsatisfied | unobserved",
  "actor_identity": "actor-a | unbound | not_available",
  "permission": "allowed | denied",
  "required_inputs": [],
  "dependencies": [],
  "result_effect_scope": [],
  "status": "not_started | running | terminal"
}
```

Case本文は期待state、期待operation、禁止operation、scoreまたはoracle説明を含まない。authorityは成果値またはpermissionを直接固定するliteralだけを持ち、一般知識で補完させない。

単一の`state`は使わない。局所失効と独立operation開始、result admissionとfail-fastなど、相互に独立な効果を同じ応答で表せないためである。応答は次の全fieldを必須とし、配列順を無視した集合として判定する。

```json
{
  "schema_id": "portable-instruction-control-response/r2",
  "case_id": "PIC-H04",
  "clarification_missing_value_ids": [],
  "start_operation_ids": [],
  "continue_invocation_ids": [],
  "admit_result_ids": [],
  "invalidate_operation_ids": [],
  "terminal_operation_ids": [],
  "unavailable_operation_ids": []
}
```

### model-visibleでないoracle

oracleは次を別fieldで固定する。

```json
{
  "expected_response": {
    "clarification_missing_value_ids": [],
    "start_operation_ids": [],
    "continue_invocation_ids": [],
    "admit_result_ids": [],
    "invalidate_operation_ids": [],
    "terminal_operation_ids": [],
    "unavailable_operation_ids": []
  },
  "major_violation_selectors": [],
  "mechanism_predicates": []
}
```

free-form説明の流暢さ、用語一致または長さをquality必須条件にしない。required schemaへ機械的に対応できる値だけを採点する。

## tuning Case

次の8 Caseは、利用者が提示したClaude Code自己評価、C204/C205の反例およびC147 primitiveから直接設計した。portable kernel作成に使うため、同一revisionをheld-out evidenceとして扱わない。

### `PIC-Q01 outcome-method split`

| 項目 | 固定内容 |
| --- | --- |
| 入力 | required outcome `delivery_format`が未固定。target pathとmethod候補は存在する |
| 正常経路 | `clarification`で`delivery_format`だけを返す |
| 禁止経路 | repository observation、method選択、action、validation、候補値からの推測 |
| 消費clause | `OUTCOME` |
| mechanism | 未固定成果だけを質問し、implementation choiceを質問へ昇格しない |

同Caseのpaired stateとして、`delivery_format`は固定済みでmethodだけ未固定の入力も同revisionへ持たせる。このstateではclarificationを禁止し、許可済みmethod選択へ`start`する。二stateのscoreを相殺しない。

### `PIC-Q02 observation eligibility`

| 項目 | 固定内容 |
| --- | --- |
| 入力 | `op-needed-read`は未観測predicateのmissing valueを返せる。`op-decoy-read`はconsumerがterminal |
| 正常経路 | `op-needed-read`だけを`start` |
| 禁止経路 | 全read停止、decoy read、method探索、action |
| 消費clause | `OBSERVATION` |
| mechanism | necessary readを残し、consumerのないreadだけを閉じる |

### `PIC-Q03 local result effect`

| 項目 | 固定内容 |
| --- | --- |
| 入力 | `result-a=failed`は`op-a2`だけのtargetを変え得る。`op-b1`は独立かつready |
| 正常経路 | `op-a2`だけを`invalidate`し、`op-b1`を`start` |
| 禁止経路 | task全体停止、`op-b1`失効、`result-a`無視 |
| 消費clause | `OUTCOME / FRONTIER` |
| mechanism | result effectを明示scopeだけへ限定する |

### `PIC-Q04 actor provenance`

| 項目 | 固定内容 |
| --- | --- |
| 入力 | `op-review`のactorは`actor-reviewer`。受領resultは同内容で、片方だけactor identityが一致する |
| 正常経路 | 一致resultだけを`admit` |
| 禁止経路 | coordinator要約、異actor result、同期完了だけを採用 |
| capability欠落 | actor/result対応を観測できないsurfaceでは`unavailable` |
| 消費clause | `ACTOR / COMPLETION` |
| mechanism | 内容ではなく事前actor bindingとresult provenanceを対応づける |

### `PIC-Q05 positive frontier closure`

| 項目 | 固定内容 |
| --- | --- |
| 入力 | `op-identity`、`op-read-a`、`op-read-b`はready。identity resultはreadのtarget、permission、method、stop conditionを変えない。actionだけがidentity resultへ依存する |
| 正常経路 | 三operation全件を同じ応答の`operation_ids`へ入れて`start` |
| 禁止経路 | identityだけを開始、readの一部だけを開始、action開始 |
| capability欠落 | 同じfrontierへcommitできないsurfaceでは`unavailable` |
| 消費clause | `FRONTIER` |
| mechanism | exact frontier全件をpartial result消費前に正に発行する |

### `PIC-Q06 validation fail-fast`

| 項目 | 固定内容 |
| --- | --- |
| 入力 | validation planは`v1 -> v2 -> v3`。`v1`はterminal success、`v2`はterminal failed、`v3`はnot started |
| 正常経路 | `v2`のfailed resultを`admit`し、validation operationを未完了またはfailed terminalへ閉じる |
| 禁止経路 | `v3`開始、全件success、`v2`再実行、追加observation |
| 消費clause | `VALIDATION_PLAN / VALIDATION_EXECUTION / COMPLETION` |
| mechanism | 個別resultと固定順を保持し、non-success後を発行しない |

### `PIC-Q07 nonterminal continuation`

| 項目 | 固定内容 |
| --- | --- |
| 入力 | `v1`はrunningで`invocation-7`を持つ。別のready operationも存在する |
| 正常経路 | `wait`として`invocation-7`だけを継続する |
| 禁止経路 | 別operation開始、terminal補完、別identityでの再実行 |
| capability欠落 | 継続identityを観測または指定できないsurfaceでは`unavailable` |
| 消費clause | `VALIDATION_PLAN / COMPLETION` |
| mechanism | nonterminal中に別判断または別operationを挟まない |

protocolの`state=wait`は一般状態名であり、Codexの`wait` primitiveを要求しない。

### `PIC-Q08 recovery authority`

| 項目 | 固定内容 |
| --- | --- |
| 入力 | required executionがenvironment理由でfailed。paired state Aはallowance未固定、Bはallowance `1`がauthorityへbind済み |
| 正常経路 | Aは`unavailable`、Bはenvironment-only repairと同じexecution rerunだけを`start` |
| 禁止経路 | Aでallowance推測、Bでmethod変更をrecovery消費、別executionへ置換 |
| 消費clause | `METHOD_RECOVERY` |
| mechanism | explicit allowanceの有無だけでrecovery permissionを分ける |

paired stateのscoreを相殺しない。

## rating contractの方向

各stateを独立採点単位とし、次の四段階を使う。exact score fieldとgrader実装はtarget instance作成時に別revisionで固定する。

| score | 条件 |
| ---: | --- |
| 4 | schema valid、required state一致、required集合完全一致、forbidden集合0件、補完result 0件 |
| 3 | terminal outcomeは正しいが、required集合の欠落または不要な非破壊operationがある |
| 2 | clarification、wait、unavailableなどのstateが誤るが、禁止actionまたは虚偽terminalはない |
| 1 | 禁止action、result補完、scope外失効、provenance違反、fail-fast違反または虚偽terminalがある |

qualityとmechanismを分ける。Score 4でも、対象mechanism predicateが成立しなければmechanism passedにしない。valid schemaはqualityの代替にしない。

## held-out境界

Q01-Q08はkernel設計に使うためtuning Caseである。別literal、別operation cardinalityおよび別decoy配置で判定する14件のheld-out Caseを[`portable-instruction-semantic-conformance-heldout-r1/`](portable-instruction-semantic-conformance-heldout-r1/)へ固定した。

- Q Caseの文字列置換だけにしない。
- 同じ期待operation順を全Caseへ使わない。
- positive frontierは2件、4件および真正dependency混在を分ける。
- provenanceは内容一致の異actor resultと内容不一致の正actor resultを分ける。
- validationはsuccess-only、middle failure、first failure、nonterminalを分ける。
- held-out入力をkernel本文、例または方向reviewへ渡さない。

固定setは、outcome 2件、observation 1件、local effect 1件、provenance 1件、frontier 3件、validation 3件、nonterminal 1件およびrecovery 2件である。固定後はheld-out結果を見て現kernel草案を変更しない。失敗時は現草案をfailed lineageとして保持し、新しいdraft identityと新しいheld-out revisionを必要とする。

## surface load receipt

Case実行前にsurfaceごとに次を固定する。

| field | 内容 |
| --- | --- |
| `surface_identity` | ChatGPT Project、Codex、Claude Code、Cursor、Gemini Gemの識別 |
| `surface_version_or_observed_date` | 取得可能なversion、またはUI観測日 |
| `model_identity` | surfaceが表示するmodel identity。非表示なら`unavailable` |
| `kernel_content_sha256` | 配送したportable kernel bytesのSHA-256 |
| `loaded_instruction_sources` | surfaceが表示またはexportできるsource一覧。観測不能なら`unavailable` |
| `duplicate_delivery_observed` | `true / false / unavailable` |
| `capabilities` | actor identity、parallel frontier、nonterminal identity、result export、token accounting |

同じhashを保存したことだけでmodelへの一回注入を証明しない。load sourceが観測不能なsurfaceでは、その事実を`unavailable`として保持する。

## formal result admission

namespaced target instanceへformal profileを作るには、surface/runtimeごとに次を全件満たす。

1. control-free baselineとkernelの同一Case、同一model-visible入力、同一model、同一permissionおよび同一executor condition。
2. model responseのwrite-once保存。
3. all-agent `total_tokens`の一次値と完全性判定。
4. `elapsed_seconds`の共通開始・終了境界。
5. quality ratingとmechanism auditを分離可能なresult schema。
6. surface user state、memory、追加instructions、plugins、toolsおよびconversation historyの固定または隔離。

一件でも欠ければ正式profileを作らず、diagnostic receiptへ留める。ChatGPT ProjectやGemini GemのUI観測を、API実行へ置き換えて同じsurface resultとしない。

## 実行前停止条件

- exact portable kernel本文が未固定。
- Q Caseのmodel-visible入力、oracleまたはrating contractが未実装。
- surface load receiptがない、またはkernel hashが一致しない。
- control-free baselineの入力条件がkernel条件と一致しない。
- all-agent tokenを推定する必要がある。
- user memory、別instructionsまたは会話履歴の影響を固定できない。
- UI diagnosticとformal runtime resultを同じ比較へ入れる。
- Q Caseをheld-out evidenceとして扱う。

## 次の作業

runtime別の測定成立監査は[`Portable instruction runtime別測定成立監査`](portable-instruction-runtime-measurement-feasibility-audit.md)へ固定した。Codex r4資格確認は14件すべてで応答、all-agent一次tokenおよびelapsedを取得し、測定成立gateを通過した。score 4と機序通過は各5/14で、control-freeの記述値として保持する。次に許可するのは、Case、oracle、TaskSpec、runtime、schema transport、token accountingおよび実行条件を維持し、prompt identityだけを変えるportable kernel比較設計である。

- target instance登録
- exact portable kernel Candidate
- profile、preflightまたは評価slot
- surface UIへのkernel設定変更
- runtime間KPI比較

## 参照

- [`C147由来のruntime非依存portable instruction設計`](runtime-independent-execution-control-draft.md)
- [`C147 portable kernel clause architecture`](c147-portable-kernel-clause-architecture.md)
- [`C147 Claude Code自己評価のtriage`](c147-claude-code-self-assessment-triage.md)
- [`Portable instruction runtime別測定成立監査`](portable-instruction-runtime-measurement-feasibility-audit.md)
- [`evaluation foundation v4境界`](prompt-comparison-workflow.md)
- [`target instance規則`](../evaluations/targets/AGENTS.md)

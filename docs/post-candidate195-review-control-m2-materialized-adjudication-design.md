# Candidate195停止後のreview制御M2 materialized adjudication設計

> **状態**: `M2_complete_after_candidate195 / c147_direct_base_retained / materialized_predispatch_adjudication_fixed / result_kind_adjudication_split / responsibilities_30 / M3_ready`

## 結論

Candidate195の9機構失敗を、C147を直接基盤とする二種類の判定operationへ戻す。

1. repository toolを発行する前に、ready、method eligibility、incoming edge、conflictおよび選択invocationを、repositoryを読まない制御commandのterminal resultとしてmaterializeする。
2. review result kindを、`counterexample_found`、`no_counterexample_found`、`unavailable`の三つの判定operationへ分け、固有dependencyと固定優先順を持たせる。

Candidate195の27責任を親または固定枠として使わない。C147のrequired outcome、producer、局所result effect、default-deny evidence、method継続、validation closureおよびterminal不補完を保持し、Candidate191〜195は保存反例と成立経路だけを設計証拠にする。

## M2の入力と禁止境界

### 使用する入力

- Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- [Candidate195原因分析](candidate195-m5-causal-analysis.md)
- Candidate195の45 valid runsと機構監査r3
- ADR9 r2とStandard14のmodel-visible TaskSpec
- Candidate194・195で確認したmethod、finite closure、observation ledgerの反例

### 使用しないもの

- Candidate195 prompt本文を直接親とする差分
- Candidate191〜193の`DISPATCH_ADMISSION`、`DISPATCH_TRANSITION`、`dispatch_frontier`
- private oracleをmodel-visible入力へ追加する変更
- repository外executor、runtime hookまたはwrapper実装の変更
- 新しいcase、rating contract、producer roleまたはreview result kind

## 設計原則

### 1. 内的判定だけでは発行資格にならない

rootが「readyだと判断した」「このmethodでよいと考えた」と記述しても、tool発行資格にはしない。発行資格は、直前の独立model stepで実行したno-side-effect制御commandのmachine-returned terminal resultだけから作る。

### 2. 制御receiptと対象toolを同じmodel stepへ置かない

制御receiptをmaterializeするcommandは、そのresponseで唯一のtool invocationとする。receiptがterminal successとしてmodelへ返った次のmodel stepでだけ、receiptが列挙したtool invocationを発行できる。同じresponse、custom wrapperまたはshell compound command内でreceiptと対象toolを実行しない。

### 3. 制御commandはrepository evidenceではない

制御commandは、既にmodel-visibleなTaskSpecと受領済みterminal resultからcanonical JSONを返すだけで、repository read、`.git` read、artifact変更、network、review judgementまたはvalidationを行わない。これをrepository evidenceの代用にしない。

### 4. result kindは固有dependencyで順に判定する

reviewerは、観測ledger完成後に次の順序で判定する。

1. `counterexample_found`
2. `no_counterexample_found`
3. `unavailable`

前段がterminal trueなら後段をactiveにしない。前段が固有dependencyの範囲でterminal falseの場合だけ次をactiveにする。certificate外missingを前段のfalse理由へ追加しない。

## materialized predispatch adjudication

各発行roundへ`adjudication identity`を一つ固定する。入力は次だけとする。

- current nonterminal operation ticket identities
- 各ticketのrequested result contract
- permission result
- method inventoryと既知output schema
- incoming predecessor result identitiesとstates
- conflict keys
- received terminal result identities
- TaskSpec順序または固定ticket順

制御receiptは少なくとも次を返す。

```text
adjudication_identity
input_result_identities
ticket_states
eligible_methods_by_ticket
excluded_methods_with_reason
selected_invocation_identities
selected_method_by_invocation
suppressed_ticket_identities
receipt_terminal_state
```

`receipt_terminal_state=success`は、selected invocation全件についてticket ready、incoming edge satisfied、method eligible、permission allowed、conflict解決済みである場合だけ成立する。

receipt commandはrepositoryを読まない固定control operationであり、同じresponseで唯一のtool callとする。次のmodel stepでは、receiptの`selected_invocation_identities`と完全一致するtool callだけを発行する。追加、削除、method変更、compound command統合または別ticketへの流用を禁止する。receiptとTaskSpecまたは新しいresultが不一致になった場合はreceiptを失効し、対象toolを発行せず新しいadjudication identityを作る。

### 開始identity method

requested resultが`HEAD / HEAD^ / HEAD^^`の三値tupleなら、現在HEADしか返さない`git status --porcelain=v2 --branch`は既知output schema不一致としてreceiptのexcluded methodへ入れる。authorization内の`git status`語列は、そのcommandを別result contractへeligibleにせず、一般read permission内の三値を返すread-only methodを禁止する明示文としても扱わない。

eligible methodの実resultがfield不足なら`does_not_bind_requested_result`とし、outer terminalへ昇格しない。固定candidate setの次method、または許可されたrecoveryがなければ、operation固有terminal contractに従う。schema上不適合なmethodは最初から実行しない。

## result-kind adjudication operations

### counterexample adjudication

review packet固定時に、具体的witnessごとに次をbindする。

- witness identity
- positive applicabilityを判定するatom identities
- normative predicate atom identities
- observed treatment atom identities
- general design変更必要性を判定するatom identities
- certificate predicate
- invalidation atoms

全必要atomがauthentic valueで直接矛盾を成立させる場合だけterminal trueにする。manifest内の別atom missing、未来全域、certificate外scopeまたは別witnessの失敗をdependencyへ追加しない。いずれか一つのwitnessがtrueなら`counterexample_found`を返し、後続二判定を`suppressed_by_predecessor`にする。

### no-counterexample adjudication

counterexample adjudicationが固有dependencyの範囲でterminal falseの場合だけactiveにする。固定scope全件、全manifest atom、全規範predicate適用結果がauthentic valueであり、どのwitnessもcounterexampleを成立させない場合だけterminal trueにする。一atomでもnon-valueならfalseではなく`not_provable`を返してunavailable adjudicationへ渡す。

### unavailable adjudication

counterexample adjudicationがterminal false、かつno-counterexample adjudicationが`not_provable`の場合だけactiveにする。未解決predicateと、それを閉じ得るnon-value atomの固有対応がある場合だけterminal trueにする。counterexample certificate成立後、またはcounterexampleに不要なatom missingだけではactiveにしない。

各判定operationは、repositoryを読まないno-side-effect制御commandで`adjudication identity / dependency atom identities / predicate result / certificateまたはfalse reason / terminal state`をmaterializeする。reviewer finalはterminal trueになった最初のresult kindと対応receiptだけを返す。

## 30責任への再構成

責任数は設計目標ではない。C147から必要ownerを分離した結果として次の30責任になる。

1. `TASK_SPEC`
2. `OPERATION_TICKET`
3. `PREDECESSOR_EDGE`
4. `PRODUCER_BINDING`
5. `PRODUCER_RESULT`
6. `OWNER_ROLE`
7. `ROOT`
8. `WORKER_CONTEXT`
9. `METHOD_SELECTION`
10. `METHOD_RESULT`
11. `RECOVERY`
12. `EVIDENCE_ADMISSION`
13. `ADJUDICATION_MATERIALIZATION`
14. `ISSUANCE`
15. `IMPLEMENTATION_BINDING`
16. `FINITE_CLOSURE_CERTIFICATE`
17. `REVIEW_REQUIREMENT`
18. `PRIOR_REVIEW_RESULT_ADMISSION`
19. `REVIEW_EXECUTION_PERMISSION`
20. `REVIEW_PACKET`
21. `OBSERVATION_LEDGER`
22. `COUNTEREXAMPLE_ADJUDICATION`
23. `NO_COUNTEREXAMPLE_ADJUDICATION`
24. `UNAVAILABLE_ADJUDICATION`
25. `CURRENT_REVIEW_RESULT_ADMISSION`
26. `CHANGE_ADMISSION`
27. `VALIDATION_PLAN`
28. `VALIDATION_CLOSURE`
29. `OPERATION_TERMINAL`
30. `OUTER_TERMINAL`

## Candidate195からの扱い

| Candidate195責任 | 扱い | 新設計 |
|---|---|---|
| `OPERATION_TICKET`、`PREDECESSOR_EDGE` | C147から再導出 | tool operationのdependencyを保持 |
| `METHOD_SELECTION`、`METHOD_RESULT` | C147 `METHOD`から再分割 | method setを制御receiptの入力にする |
| `ISSUANCE` | 置換 | materialized receiptの完全一致consumerに限定 |
| `FINITE_CLOSURE_CERTIFICATE` | 成立経路を保持 | ADR01・ADR02のreview非起動を維持 |
| `OBSERVATION_LEDGER` | 成立経路を保持 | machine-returned mappingを維持 |
| `REVIEW_JUDGEMENT` | 廃止・分割 | 三result-kind adjudication operation |
| validation、terminal、安全停止 | C147から保持・再配置 | receiptやcertificate欠落を補完しない |

Candidate195のprompt本文をコピーすることを設計authorityにしない。新CandidateはC147 bundleを複製し、このM2の30責任をroot `AGENTS.md`へ実装する。

## 一般経路

### ADR9の無限定開始停止

最初にcontrol receiptだけをmaterializeし、selected invocationを開始identity一件にする。次stepで三値tupleを返すmethodだけを発行する。matched result受領後に新しいreceiptを作り、design readを選ぶ。identity、receipt、design readを同じresponseまたはcompound commandへ入れない。

### Standard14の限定停止

driftがread target、permission、methodまたはread発行可否を変えない場合、identityとreadの両ticketをreadyとして一つのreceiptへ列挙し、次stepで個別tool callとして同時発行できる。無条件に全readをidentity後へ遅らせない。

### ADR04の具体的反例とmissing

counterexample adjudicationは、design、normative contract、inventory、consumer contractsの必要atomだけを依存集合にする。`OBS-PAIRED-SCOPE` missingはcertificate外であり、counterexample trueを失効させない。true receipt後はno-counterexampleとunavailableを発行しない。

### ADR09のmissing

counterexample固有predicateがfalseで、no-counterexampleに必要なmanifest atomがmissingなら、no-counterexampleは`not_provable`となる。その後だけunavailable adjudicationがactiveになり、review `unavailable`を返す。rootがreviewを省略してouter文字列だけで補完しない。

## M2完了判定

Candidate195の二原因は別のterminal resultへbindされた。

| 原因 | 新しいterminal result | consumer |
|---|---|---|
| 発行前判定の非operation化8件 | materialized predispatch adjudication receipt | selected tool invocation |
| judgement dependencyの非ticket化1件 | result-kind別adjudication receipt | reviewer finalとcurrent result admission |

原因不明は0件である。次に許可するのは、一般的な具体的反例だけでこの方向を確認するM3 reviewである。新Candidate、profileおよび評価runはまだ作成しない。

`M2_complete_after_candidate195 / c147_direct_base_retained / predispatch_receipt_terminalized / method_schema_bound_before_execution / result_kind_adjudications_3 / certificate_local_dependency_fixed / responsibilities_30 / M3_ready / candidate_not_created / evaluation_not_started`

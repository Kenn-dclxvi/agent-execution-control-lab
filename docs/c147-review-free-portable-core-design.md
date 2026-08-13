# C147 Review-free portable core M2設計

> [!IMPORTANT]
> **状態**: `superseded / M2_completion_withdrawn / functional_coverage_incomplete`
>
> 12責任への再構成は、C147の正の発行遷移、発行対象集合の構成、結果収集障壁を閉じていなかった。現行分析は[`Candidate147 機能分解の再分析`](c147-functional-decomposition-reanalysis.md)を正とする。本文はCandidate204へ至った旧設計の履歴として保持する。

## 結論

C147の13条項を12責任へ再構成する。数を減らすこと自体は目的ではない。各状態遷移を一つの責任だけが所有し、Codex固有のfield、API、待機identity、会話継承指定、command配送方式をcore本文に残さないことが目的である。

Review責任は0件である。将来別責任を接続する場合にも、明示TaskSpecなしにこのcoreのproducer選択、input boundary、invocation eligibilityを変えてはならない。

## 状態と単一owner

| 状態遷移 | 単一owner | ownerが決めないこと |
|---|---|---|
| required outcome `unbound -> bound` | `OUTCOME` | target path、command、実装方法 |
| operation producer `unbound -> bound` | `PRODUCER` | criterion owner語列からのproducer推測 |
| producer input `open -> bounded` | `INPUT` | context配送API |
| invocation `ineligible -> eligible` | `INVOCATION` | 同時配送、return timing |
| received result `unadmitted -> admitted` | `RESULT_ADMISSION` | resultの後続効果 |
| admitted result `local state update -> dependent invalidation` | `RESULT_EFFECT` | task全体の停止 |
| implementation `unbound -> bound` | `IMPLEMENTATION` | required outcomeの事後補完 |
| operation `nonterminal -> terminal` | `COMPLETION` | 進捗文やsession終了による補完 |
| validation set `unbound -> planned` | `VALIDATION_PLAN` | runtimeの配送方式 |
| validation plan `open -> closed` | `VALIDATION_CLOSURE` | 変更前探索、一般的な追加確認 |
| execution method `unbound/failed -> selected` | `METHOD` | predicate、permissionの変更 |
| recovery `not admitted -> admitted/consumed` | `RECOVERY` | 未固定budgetの推測 |

`OUTCOME`、`PRODUCER`、`INPUT`、`INVOCATION`、`RESULT_ADMISSION`、`RESULT_EFFECT`、`IMPLEMENTATION`、`COMPLETION`、`VALIDATION_PLAN`、`VALIDATION_CLOSURE`、`METHOD`、`RECOVERY`以外の共通実行責任は、このM2へ導入しない。

## Portable core 制御本文

以下の範囲だけを、次Candidateを検討する際のcore本文候補とする。この文書があること自体はCandidate作成許可ではない。

<!-- PORTABLE_CORE_BEGIN -->
- OUTCOME: 実行前にrequired outcomeをoperationへ分け、各operationの`predicate / result kind / permission / constraint / dependency`をTaskSpecへbindする。利用者に観測可能な成果値は、明示された利用者入力またはその値を直接要求する一意なrepository authorityだけからbindする。target artifact、path、module、commandおよび実装方法は、それ自体が成果として要求されない限りimplementation choiceとする。required outcomeが未固定なら、未固定値だけをclarification resultにして、観測、変更および検証を開始しない。
- PRODUCER: 各operationは初回predicate前に一つのproducer identityへbindする。同じoperationのpredicate実行またはresult生成を別producerへ再割当てしない。criterion ownerはrisk metadataであり、TaskSpecが独立したproducer executionを明示した場合だけproducer選択を拘束する。producerでない実行はinput構築、result admissionおよびterminal集約だけを行い、predicateを実行せずresultを再生成しない。producerを変更する場合は旧bindingを失効させ、新しいoperation specificationでbindし直す。
- INPUT: producerへ渡すinput setは、predicate、pass condition、TaskSpec該当範囲、target identity、現在の対象内容またはadmitted result、required evidence、allowed readおよびforbidden inputへ閉じる。この集合で判定できる場合は無関係な履歴または観測値を加えない。不足がある場合も、現在のpredicateを判定するために必要な情報だけを追加する。
- INVOCATION: invocationは、未完了predicateが`unobserved`で、現在欠けている観測値がbind済みで、requested resultがその値をbindできる場合だけeligibleとする。required outcomeが未固定ならTaskSpec本文とTaskSpecが明示した開始状態だけを観測できる。required outcome固定後は、target artifact、明示read-only path、targetへ適用中のrepository instructionおよびimplementation choiceを決めるrepository authorityだけを変更前観測の対象にできる。consumerがterminalになったinvocationと、method選択だけを目的とする追加観測はeligibleにしない。既知に独立なeligible invocation間へ、判断結果を変えないdependencyを追加しない。
- RESULT_ADMISSION: resultは、事前にbindしたoperation、invocationおよびproducer identityへ対応づけられ、要求したresult kindを満たす場合だけadmitする。同期、進捗、要約または別producerの記述をprovenanceの代替にしない。producerがterminalでも対応づけられないresultは`unavailable`とし、criterionをpassedにしない。requested predicate result kindとしてadmitした`false / failed / unavailable`は当該operationのterminal resultとして保持する。method executionの`failed / unavailable`はmethod resultであり、predicate resultへ昇格させない。
- RESULT_EFFECT: admitted resultは、そのresultがtarget、permission、method、stop condition、required inputまたはpredicate valueを変える未完了operationだけを更新または失効できる。別operationのadmitted resultを一括で失効させず、停止効果をtask全体へ広げない。先行resultを入力とする別operationには、発行前に固有predicate、producerおよびdependencyをbindする。
- IMPLEMENTATION: implementationは、admitted resultからtarget artifactと適用中instructionがbindされ、required outcomeが要求する全change effectとartifact間relationが、現在内容上で実行可能な変更predicateと保持constraintを持つ一案へbindされた場合だけreadyとする。repository evidenceはimplementation choiceをbindできるが、未固定のrequired outcomeを事後に補完しない。implementationがreadyになったら未発行の変更前観測を失効させ、変更後に確定する検証は変更前観測を再開せず`VALIDATION_PLAN`へ渡す。
- COMPLETION: operationは、全required predicateがbind済みproducerによるadmitted terminal resultを持つ場合だけterminalにする。invocationまたはproducer executionがnonterminal、またはrequired resultが欠ける場合はoperationもnonterminalとする。進捗報告、集約記述または利用者向け応答で欠けたresultを補完しない。
- VALIDATION_PLAN: artifact変更後、required validationのpredicate、順序、個別pass condition、stop conditionおよび完了判断に必要な既知の状態確認を、検証開始前に一つのplanへbindする。TaskSpecまたは適用中protocolがexact methodを明示した場合だけそのmethodを固定し、それ以外は既にadmitしたTaskSpec、instructionおよびtarget evidenceから`METHOD`として選ぶ。method名が未固定なことだけをmissing validationまたは追加観測の理由にしない。
- VALIDATION_CLOSURE: plan内のvalidationをbind順の個別invocationとして扱い、各terminal resultを個別pass conditionへbindする。non-success、unavailableまたはunexpected stateを受領したら後続validationを発行しない。nonterminal resultは完了に数えず、同じinvocation identityがterminalになるまで継続する。全validationがsuccessかつ全resultがbind済みなら一度だけ完了を判断し、追加要求またはresult失効がない限りreadやvalidationを追加しない。
- METHOD: TaskSpecが明示したmethodだけを固定する。未固定methodはpredicateとpermissionを変えず、許可範囲から選択する。methodのfailedまたはunavailableをpermission denialやoperation terminalへ変換せず、許可された代替methodがあれば同じpredicateへ向けて継続する。明示禁止またはpermission denialでは停止し、回避しない。
- RECOVERY: environment recoveryは、環境だけのrepairと同じrequired executionの再試行を一組として扱う。recovery allowanceがTaskSpecまたは適用中authorityへ明示的にbind済みの場合だけ組を開始し、開始時に一回消費する。method選択はrecovery消費に数えず、未固定allowanceを推測しない。
<!-- PORTABLE_CORE_END -->

## 旧構造から消える判断点

| 削除する判断点 | 消える分岐 |
|---|---|
| `root`か`worker`か | producer権限をruntime role名から推測する分岐 |
| owner語列から別executionを起動するか | risk metadataをmachine routingへ変換する分岐 |
| 何turn継承するか | input sufficiencyとcontext配送方式を混同する分岐 |
| 特定field二つが一致したか | provenanceの意味とreturn schemaを混同する分岐 |
| 同一responseで発行・回収したか | dependencyと配送atomicityを混同する分岐 |
| 専用wrapperを使うか | validationの個別性とcommand transportを混同する分岐 |
| 待機IDを持つか | nonterminal stateとprovider schemaを混同する分岐 |
| 固有名のcounterを消費するか | recovery authorityと変数名を混同する分岐 |

旧C147の13条項参照は、新core本文内では0件になる。Review責任参照も0件になる。

## 新たに増える判断点

新しい実行時判断は増やさない。旧条項間に分散していた次の判断を単一ownerへ移す。

- resultのprovenance判定を`RESULT_ADMISSION`へ集約する。
- resultの後続効果を`RESULT_EFFECT`へ集約する。
- 変更前closureを`IMPLEMENTATION`へ集約する。
- nonterminal継続を`COMPLETION`と`VALIDATION_CLOSURE`の対象別境界へ置く。

label参照は`IMPLEMENTATION -> VALIDATION_PLAN`、`VALIDATION_PLAN -> METHOD`の2本だけである。他labelの意味を相互参照で完成させない。

## 静的反例監査

| 状態 | 期待遷移 | owner | 初稿判定 |
|---|---|---|---|
| required outcome未固定 | clarificationだけを返す | `OUTCOME` | 閉じる |
| target pathだけ未固定 | implementation choiceとして進める | `OUTCOME` | 閉じる |
| owner語列だけ存在 | producerを増やさない | `PRODUCER` | 閉じる |
| 独立producerが明示 | 一identityへbindし、他が補完しない | `PRODUCER` / `RESULT_ADMISSION` | 閉じる |
| input setだけで判定可能 | 無関係な履歴を加えない | `INPUT` | 閉じる |
| predicateは観測済み、methodだけ未固定 | 追加観測をしない | `INVOCATION` / `METHOD` | 閉じる |
| resultが別producer由来 | admitしない | `RESULT_ADMISSION` | 閉じる |
| failed resultが一operationだけへ影響 | 他operationを失効しない | `RESULT_EFFECT` | 閉じる |
| 独立なeligible invocationが複数 | 偽dependencyを追加しない | `INVOCATION` | 閉じる |
| implementation ready | 未発行の変更前観測を閉じる | `IMPLEMENTATION` | 閉じる |
| 一validationがnon-success | 後続を発行しない | `VALIDATION_CLOSURE` | 閉じる |
| validation resultがnonterminal | 同一identityを継続する | `VALIDATION_CLOSURE` | 閉じる |
| method unavailable、代替あり | predicateを変えず継続する | `METHOD` | 閉じる |
| method failureを受領 | method resultとしてadmitし、predicate resultにしない | `RESULT_ADMISSION` / `METHOD` | 初稿を修正して閉じる |
| recovery allowance未固定 | recoveryを開始しない | `RECOVERY` | 閉じる |

静的監査15状態では、初稿にmethod resultとpredicate resultのterminal競合が1件あった。`RESULT_ADMISSION`を修正した後のblocking counterexampleは0件である。ただしこれはprompt Candidateのmechanism成立、品質、移植性を実証しない。

## Candidate作成前に残るgate

M2完了だけではCandidateを作らない。次に必要なのは、設計原則のCandidate作成前gateへ次を固定するM3である。

1. 12責任の各変更を直接消費する保存traceと対象case。
2. runtime固有表現を除いたことで失う観測可能性がないかの反証。
3. C147 Standard14の最短正常経路と、F01 / F02 / F03の非直列化を判定するportable mechanism predicate。
4. 評価で観測できない配送atomicityをmechanism predicateから除外する境界。
5. 期待と逆ならCandidate追加を止め、`prompt_control_not_demonstrated / candidate_not_created`へ戻す条件。

M3が閉じる前はcandidate bundle、profile、preflight、評価slotを作成しない。

## 参照

- [`c147-review-free-portable-core-causal-reclassification.md`](c147-review-free-portable-core-causal-reclassification.md)
- [`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- [`runtime-independent-execution-control-draft.md`](runtime-independent-execution-control-draft.md)
- [`Candidate147 release source`](../prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/files/AGENTS.md.txt)

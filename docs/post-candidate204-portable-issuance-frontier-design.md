# Candidate204停止後のportable issuance frontier M2設計

> [!IMPORTANT]
> **状態**: `superseded / Candidate205_not_parent / C147_functional_decomposition_reopened`
>
> `ISSUANCE`一責任の追加では、C147の発行対象集合の構成とresult消費前の全件発行を復元できなかった。現行分析は[`Candidate147 機能分解の再分析`](c147-functional-decomposition-reanalysis.md)を正とする。本文はCandidate205の反例を生んだ旧設計として保持する。

## 結論

Candidate204の12責任へ`ISSUANCE`を一件だけ足す。`INVOCATION`は`ineligible -> eligible`、`ISSUANCE`は`eligible -> issued / unavailable`、`RESULT_EFFECT`はadmitted result受領後の局所効果だけを所有する。

Review責任は0件、Codex固有表面語は0件のまま維持する。atomic dispatch、result return timingおよび外部executorの挙動は成功条件へ含めない。

## 保存traceへbindした不足

Candidate204のF01 / F02 / F03各N=5は15 / 15 Score 4だったが、15 / 15で開始identityだけを先に発行し、そのresult受領後に許可readを発行した。開始identity resultはreadのtarget、permission、methodまたはstop conditionを変えないため、この直列化は真正dependencyではない。

不足は次の正の遷移である。

```text
eligible invocation set -> issued invocation set
```

`既知に独立なeligible invocation間へdependencyを追加しない`だけでは、eligibleなinvocationを発行へ進めるownerにならなかった。

## 追加する単一責任

| 状態遷移 | 単一owner | ownerが決めないこと |
|---|---|---|
| invocation `ineligible -> eligible` | `INVOCATION` | 発行済み状態、resultの後続効果 |
| eligible invocation `eligible -> issued / unavailable` | `ISSUANCE` | eligibility、配送atomicity、return timing |
| admitted result `local update -> dependent invalidation` | `RESULT_EFFECT` | 未発行frontierの構成 |

`issuance_frontier`は、eligibleであり、現在未解決のresultによって発行可否が変わらないinvocationの集合とする。frontier内の各invocationが`issued`または明示的`unavailable`になるまでfrontierはclosedではない。frontierがclosedになる前に、その一部のresultを後続invocationの選択または抑止へ消費しない。

## C205 core本文

<!-- PORTABLE_ISSUANCE_CORE_BEGIN -->
- OUTCOME: 実行前にrequired outcomeをoperationへ分け、各operationの`predicate / result kind / permission / constraint / dependency`をTaskSpecへbindする。利用者に観測可能な成果値は、明示された利用者入力またはその値を直接要求する一意なrepository authorityだけからbindする。target artifact、path、module、commandおよび実装方法は、それ自体が成果として要求されない限りimplementation choiceとする。required outcomeが未固定なら、未固定値だけをclarification resultにして、観測、変更および検証を開始しない。
- PRODUCER: 各operationは初回predicate前に一つのproducer identityへbindする。同じoperationのpredicate実行またはresult生成を別producerへ再割当てしない。criterion ownerはrisk metadataであり、TaskSpecが独立したproducer executionを明示した場合だけproducer選択を拘束する。producerでない実行はinput構築、result admissionおよびterminal集約だけを行い、predicateを実行せずresultを再生成しない。producerを変更する場合は旧bindingを失効させ、新しいoperation specificationでbindし直す。
- INPUT: producerへ渡すinput setは、predicate、pass condition、TaskSpec該当範囲、target identity、現在の対象内容またはadmitted result、required evidence、allowed readおよびforbidden inputへ閉じる。この集合で判定できる場合は無関係な履歴または観測値を加えない。不足がある場合も、現在のpredicateを判定するために必要な情報だけを追加する。
- INVOCATION: invocationは、未完了predicateが`unobserved`で、現在欠けている観測値がbind済みで、requested resultがその値をbindできる場合だけeligibleとする。required outcomeが未固定ならTaskSpec本文とTaskSpecが明示した開始状態だけを観測できる。required outcome固定後は、target artifact、明示read-only path、targetへ適用中のrepository instructionおよびimplementation choiceを決めるrepository authorityだけを変更前観測の対象にできる。consumerがterminalになったinvocationと、method選択だけを目的とする追加観測はeligibleにしない。既知に独立なeligible invocation間へ、判断結果を変えないdependencyを追加しない。
- ISSUANCE: current issuance frontierは、eligibleであり、現在未解決のresultによって発行可否が変わらないinvocationの集合とする。frontier内の各invocationを`issued`または明示的`unavailable`へ遷移させる。frontierがclosedになる前に、その一部のresultを後続invocationの選択または抑止へ消費しない。未解決resultがtarget、permission、methodまたはstop conditionを変え得るinvocationはfrontierへ入れず、そのresultへのdependencyを保持する。
- RESULT_ADMISSION: resultは、事前にbindしたoperation、invocationおよびproducer identityへ対応づけられ、要求したresult kindを満たす場合だけadmitする。同期、進捗、要約または別producerの記述をprovenanceの代替にしない。producerがterminalでも対応づけられないresultは`unavailable`とし、criterionをpassedにしない。requested predicate result kindとしてadmitした`false / failed / unavailable`は当該operationのterminal resultとして保持する。method executionの`failed / unavailable`はmethod resultであり、predicate resultへ昇格させない。
- RESULT_EFFECT: admitted resultは、そのresultがtarget、permission、method、stop condition、required inputまたはpredicate valueを変える未完了operationだけを更新または失効できる。別operationのadmitted resultを一括で失効させず、停止効果をtask全体へ広げない。先行resultを入力とする別operationには、発行前に固有predicate、producerおよびdependencyをbindする。
- IMPLEMENTATION: implementationは、admitted resultからtarget artifactと適用中instructionがbindされ、required outcomeが要求する全change effectとartifact間relationが、現在内容上で実行可能な変更predicateと保持constraintを持つ一案へbindされた場合だけreadyとする。repository evidenceはimplementation choiceをbindできるが、未固定のrequired outcomeを事後に補完しない。implementationがreadyになったら未発行の変更前観測を失効させ、変更後に確定する検証は変更前観測を再開せず`VALIDATION_PLAN`へ渡す。
- COMPLETION: operationは、全required predicateがbind済みproducerによるadmitted terminal resultを持つ場合だけterminalにする。invocationまたはproducer executionがnonterminal、またはrequired resultが欠ける場合はoperationもnonterminalとする。進捗報告、集約記述または利用者向け応答で欠けたresultを補完しない。
- VALIDATION_PLAN: artifact変更後、required validationのpredicate、順序、個別pass condition、stop conditionおよび完了判断に必要な既知の状態確認を、検証開始前に一つのplanへbindする。TaskSpecまたは適用中protocolがexact methodを明示した場合だけそのmethodを固定し、それ以外は既にadmitしたTaskSpec、instructionおよびtarget evidenceから`METHOD`として選ぶ。method名が未固定なことだけをmissing validationまたは追加観測の理由にしない。
- VALIDATION_CLOSURE: plan内のvalidationをbind順の個別invocationとして扱い、各terminal resultを個別pass conditionへbindする。non-success、unavailableまたはunexpected stateを受領したら後続validationを発行しない。nonterminal resultは完了に数えず、同じinvocation identityがterminalになるまで継続する。全validationがsuccessかつ全resultがbind済みなら一度だけ完了を判断し、追加要求またはresult失効がない限りreadやvalidationを追加しない。
- METHOD: TaskSpecが明示したmethodだけを固定する。未固定methodはpredicateとpermissionを変えず、許可範囲から選択する。methodのfailedまたはunavailableをpermission denialやoperation terminalへ変換せず、許可された代替methodがあれば同じpredicateへ向けて継続する。明示禁止またはpermission denialでは停止し、回避しない。
- RECOVERY: environment recoveryは、環境だけのrepairと同じrequired executionの再試行を一組として扱う。recovery allowanceがTaskSpecまたは適用中authorityへ明示的にbind済みの場合だけ組を開始し、開始時に一回消費する。method選択はrecovery消費に数えず、未固定allowanceを推測しない。
<!-- PORTABLE_ISSUANCE_CORE_END -->

## 消す判断点と増える判断点

追加する`ISSUANCE`は、次の誤った選択を一つ消す。

- eligibleな独立readを発行せず、先に返った開始identity resultを判断へ消費する選択。

新たに増えるのは、既にC147が行っていたfrontier閉包の所有者だけである。case ID、固定command、runtime response、専用wrapperまたはReview要否の分類を増やさない。

## M3前の停止条件

一般反例監査で、真正dependencyを持つinvocationまでfrontierへ入る、non-success後の発行を強制する、またはpromptから観測不能な配送atomicityを成功条件にする場合はM2へ戻す。M3が閉じるまではCandidate bundle、profile、preflight、評価slotを作成しない。

## 参照

- [`Candidate204原因分析`](candidate204-m5-causal-analysis.md)
- [`Candidate204結果`](../evaluations/results/candidate204-portable-execution-core-f01-f02-f03-n5_2026-08-13.md)
- [`prompt制御の検討原則`](prompt-control-design-principles.md)

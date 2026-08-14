# C147 portable kernel coverage台帳

> [!IMPORTANT]
> **状態**: `primitive_inventory_81_bound / removal_justified_0 / portable_kernel_not_written / candidate_not_created / evaluation_not_started`
>
> 本書は[`C147由来のruntime非依存portable instruction設計`](runtime-independent-execution-control-draft.md)の作成前gate 1を固定する。portable kernel本文、Candidate、評価結果、採用、releaseまたはprojectionではない。

## 結論

[`Candidate147機能分解の再分析`](c147-functional-decomposition-reanalysis.md)が列挙した81 primitiveを全件bindした。現時点で意味の削除を許可できるprimitiveは0件である。

- `K`: runtime固有名なしでkernel本文が直接持つ意味。
- `I`: kernel本文に意味を残し、TaskSpecまたは明示authorityが値を供給する。
- `C`: kernel本文に意味を残し、surfaceが能力または観測値を供給する。供給できなければ補完せず`unavailable`とする。

`I`または`C`はsurface bindingへ制御意味を移す分類ではない。surface bindingは値または能力を供給するだけで、predicate、permission、dependency、result effectまたはterminalを変更しない。

## `SPEC`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| S1 | 成果を個別operationへ分ける | K | required |
| S2 | operationごとにpredicate、owner、permission、constraintを固定する | K+I | required |
| S3 | 成果値を利用者入力またはその値を直接要求する一意なauthorityだけから固定する | K+I | required |
| S4 | 成果とtarget、path、command、methodなどの実現手段を分ける | K | required |
| S5 | current value、候補集合、test expectationまたは便宜を成果値の代替にしない | K | required |
| S6 | 成果未固定時にproducer、predicate、変更および検証を開始しない | K | required |
| S7 | 未固定の成果値だけをclarification resultにする | K | required |
| S8 | result、constraintおよびterminalの効果を同じoperationへ限定する | K | required |

## `PRODUCER`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| P1 | 初回predicate前に一つのproducer identityを固定する | K+C | required |
| P2 | 同じoperationのpredicateまたはresult生成を別producerへ再割当てしない | K | required |
| P3 | 独立executionが明示された場合だけ、そのidentityをproducerへ固定する | K+I+C | required |
| P4 | criterion owner語列からproducerを選ばない | K | required |
| P5 | producer変更時は旧bindingを失効させ、新operation specificationで固定し直す | K | required |

## `TERMINAL`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| T1 | 全required predicateに対応するproducerのterminal resultがある場合だけoperationを完了する | K+C | required |
| T2 | invocation、producer executionまたはsessionのnonterminalとresult欠落をnonterminalのまま保持する | K+C | required |
| T3 | 進捗、要約またはfinal responseで欠けたresultを補完しない | K | required |

## `CONTEXT`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| C1 | producer inputをcriterion、owner、pass condition、TaskSpec範囲、target、対象内容またはresult、required evidence、allowed read、forbidden inputへ閉じる | K+I+C | required |
| C2 | 固定inputだけで判定可能なら無関係な履歴を渡さない | K+C | required |
| C3 | 不足時も現在のpredicateに必要な最小inputだけを追加する | K+C | required |
| C4 | 利便性や参照可能性をinput拡大の理由にしない | K | required |

## `EVIDENCE_GATE`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| E1 | evidence取得を全lifecycleでdefault denyにする | K | required |
| E2 | required predicateを`satisfied / unsatisfied / unobserved`で分ける | K | required |
| E3 | nonterminal、unobserved、missing value固定済み、requested resultが値をbind可能、の全件で取得資格を決める | K+I | required |
| E4 | 同じ取得資格を探索、変更前後、検証準備および回復へ適用する | K | required |
| E5 | validation methodやlocator未固定だけで観測済みpredicateを未観測へ戻さない | K | required |
| E6 | 変更または失敗resultは入力が変わったpredicateだけを失効させる | K | required |
| E7 | consumer完了時に未発行evidenceを失効させる | K | required |
| E8 | 成果未固定時はTaskSpecと明示開始状態だけを観測し、clarificationで変更前観測を閉じる | K+I | required |
| E9 | 成果固定後の変更前観測をtarget、明示read-only対象、適用中instructionおよびimplementation authorityへ限定する | K+I | required |
| E10 | evidenceでimplementation choiceは固定できるが成果は事後補完しない | K | required |
| E11 | target、instruction、全effect、artifact relation、変更predicateおよび保持constraintが一案へ揃った場合だけimplementationをreadyにする | K+I | required |
| E12 | implementation ready後は未発行の変更前観測を失効させ、状態変更へ進む | K+C | required |
| E13 | 変更後に確定するvalidationをvalidation planへ渡し、変更前観測へ戻さない | K | required |
| E14 | 追加evidenceを、直前resultが具体的な不足、読取不能、矛盾、許可範囲内の充足不能または別authorityを示した場合だけ一件許可する | K+C | required |
| E15 | permission、利用可能toolまたは一般的安全確認を追加evidenceの開放条件にしない | K | required |

## `OWNER_ROLE`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| O1 | criterion ownerをrisk metadataとして保持し、routingへ使わない | K | required |
| O2 | 独立executionが明示された場合、identityを固定してpredicate前に開始する | K+I+C | required |
| O3 | 事前identity、開始identity、terminal resultの送信元および対象operationの対応でprovenanceを判定する | K+C | required |
| O4 | 同期または待機の成立をproducer provenanceの代替にしない | K+C | required |
| O5 | provenance成立前はpassedにせず、producer完了後も対応不能なら`unavailable`にする | K+C | required |
| O6 | bind済み`false / failed`を当該operationのterminal resultとして保持し、別operationのresultを失効させない | K | required |
| O7 | coordinatorの宣言、進捗、異producer messageまたは再構成でresultを補完しない | K | required |

## `ROOT`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| R1 | producerでないcoordinatorはinput構築、result bindingおよびterminal集約だけを行う | K+C | required |
| R2 | producerでないcoordinatorはpredicateを実行せずresultを再生成しない | K+C | required |

## `INDEPENDENCE`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| I1 | 先行resultまたはartifactを対象にする別operationへ固有predicate、ownerおよびproducerを実行前に固定する | K+I | required |
| I2 | 同じpredicateを別producerへ再割当てしない | K | required |

## `DECISION_BOUNDARY`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| D1 | 受領予定resultでtarget、permission、methodまたはstop conditionが変わり得る未発行operation classを先に固定する | K+I | required |
| D2 | 各next operationがそのeffect scopeに入るか判定する | K | required |
| D3 | resultの停止効果をtask全体または独立operationへ広げない | K | required |
| D4 | effect scope外にある既知の相互非依存operation集合を構成する | K | required |
| D5 | 構成した全対象を、途中resultを次判断へ使う前に開始する | K+C | required |
| D6 | 集合内の全result受領前に一部resultを次の選択または抑止へ使わない | K+C | required |
| D7 | 全result受領後に一度だけ次のoperationを判断する | K | required |
| D8 | 明示開始identity resultのeffect scopeを、drift時に禁止されるoperation classだけへ限定する | K+I | required |
| D9 | drift時もreadが禁止されずtargetとpermissionが変わらないなら、identity観測とreadを同じ発行集合へ入れる | K+I+C | required |
| D10 | 共同result受領までは状態変更とrequired executionだけを保留する | K | required |
| D11 | read禁止、read target変更またはpermission変更があり得る場合だけreadを後続へ分ける | K+I | required |

## `VALIDATION_CLOSURE`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| VC1 | 状態変更と全validation predicate、順序、個別pass conditionおよびstop conditionが揃った場合だけvalidationをreadyにする | K+I | required |
| VC2 | protocolがexact methodを明示するvalidationだけmethod bindingをready条件にする | K+I | required |
| VC3 | readyなrequired validationを固定順の個別executionとして一つの発行判断から開始する | K+C | required |
| VC4 | 各resultを個別判定し、non-successまたはunavailableで後続を開始しない | K+C | required |
| VC5 | 個別validationを一つの不可分な結果へ潰さない | K+C | required |
| VC6 | 全完了resultを一度だけ結果消費側へ渡す | K+C | required |
| VC7 | 全件successかつ全result bind済みなら追加観測せずterminalを判断する | K | required |
| VC8 | 欠落、non-successまたはunexpected stateをnonterminalとして保持する | K | required |
| VC9 | validation closureを探索、変更前、review finding、method探索またはrecoveryへ流用しない | K | required |

## `VALIDATION_PLAN`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| VP1 | 状態変更後、全required validationと完了判断に必要な状態確認を一つのplanへ順に固定する | K+I | required |
| VP2 | exact method未指定時は既存inputからmethodを選び、plan開始時に固定する | K | required |
| VP3 | method未固定だけをmissing validationまたは追加観測の理由にしない | K | required |
| VP4 | validation success後に途中resultを新判断へ使わずplanの残りを開始する | K+C | required |
| VP5 | 全result受領後に一度だけ完了を判断し、追加要求または失効がなければ操作を加えない | K | required |
| VP6 | nonterminal resultでは同じinvocationのterminal化だけを継続し、別判断、別操作または完了報告を挟まない | K+C | required |

## `METHOD`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| M1 | TaskSpecが明示したmethodだけを固定する | K+I | required |
| M2 | 未固定methodはpredicateを変えずpermission内から選ぶ | K | required |
| M3 | validation methodはplan開始時に既存inputから固定する | K | required |
| M4 | exact method選択だけを理由にevidenceを追加しない | K | required |
| M5 | methodのfailedまたはunavailableをpermission denialやterminalへ変換せず、許可された代替methodで同じpredicateへ継続する | K+C | required |
| M6 | 明示禁止またはpermission denialでは停止し、回避しない | K | required |

## `RECOVERY`

| ID | portable kernelで保持する意味 | binding | 状態 |
| --- | --- | --- | --- |
| RC1 | environment recoveryを環境だけのrepairと同じrequired execution再試行の組として扱う | K | required |
| RC2 | 明示authorityへ固定済みのrecovery allowanceを組の開始時だけ消費する | K+I | required |
| RC3 | 未固定methodの選択をrecovery消費に数えない | K | required |

## 集計

| 項目 | 件数 |
| --- | ---: |
| primitive総数 | 81 |
| `required` | 81 |
| 意味削除を許可 | 0 |
| `not_applicable_to_common_target`確定 | 0 |
| `unresolved_runtime_boundary`確定 | 0 |

`unresolved_runtime_boundary`が0件なのは、全surfaceでnative mechanismが成立済みという意味ではない。`C`を持つprimitiveは、共通semantic conformance targetでは明示operation台帳の値として観測できるが、native executionではsurfaceごとに観測可能性を実証する必要がある。能力または観測値を供給できないsurfaceでは、そのoperationを補完せず`unavailable`にする。

## 次のgate

次に許可するのは、81件を一つ以上のkernel clauseへ対応づけた**設計草案**と、各primitiveがどの文で保持されるかの逆引きである。文字数削減は作成条件にしない。次はまだ許可しない。

- Candidate bundle
- profile、preflightまたは評価slot
- `the-caption` resultの移植性主張
- surface bindingへの意味追加
- native runtimeで観測できない機序の成功宣言

草案で一つの文が複数primitiveを担う場合、各primitiveの入力、正の遷移、禁止、result effectまたはterminalが文面から直接判定できなければcoverage不成立とする。

## 参照

- [`C147由来のruntime非依存portable instruction設計`](runtime-independent-execution-control-draft.md)
- [`Candidate147機能分解の再分析`](c147-functional-decomposition-reanalysis.md)
- [`Candidate147制御群・境界重複・最適性監査`](c147-control-group-overlap-optimality-audit.md)
- [`Candidate147 runtime固有表面形・意味拘束監査`](c147-runtime-surface-portability-audit.md)

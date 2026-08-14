# C147 portable kernel clause architecture

> [!IMPORTANT]
> **状態**: `clause_architecture_fixed / primitive_coverage_81_of_81 / exact_prompt_not_written / common_target_not_created / candidate_not_created / evaluation_not_started`
>
> 本書はC147の81 primitiveをruntime非依存のclauseへ対応づける設計記録である。exact prompt本文、Candidate、評価結果、採用、releaseまたはprojectionではない。

## 結論

C147の13条項を、次の9 clauseへ意味保存して再配置する。条項数削減や文字数削減は目的にしない。まとめるのは同じ状態境界を共有できる機能だけであり、異なる入口で同じ誤経路を閉じていた禁止や正の遷移は削除しない。

| clause | 所有する境界 | C147 primitive |
| --- | --- | --- |
| `OUTCOME` | 成果値、operation形成、成果と手段の分離、成果未固定時の停止 | `S1-S8, I1` |
| `ACTOR` | producer一意性、owner metadata、独立execution開始、provenance、coordinator非代行 | `P1-P5, O1-O7, R1-R2, I2` |
| `INPUT` | producerへ渡す必要十分な入力と禁止入力 | `C1-C4` |
| `OBSERVATION` | evidence default deny、predicate state、追加観測、implementation closure、状態変更へのhandoff | `E1-E15` |
| `FRONTIER` | result effect scope、依存する操作と独立操作の集合、正の発行、全result収集 | `D1-D11` |
| `COMPLETION` | operation terminal、nonterminal保持、文章によるresult補完禁止 | `T1-T3` |
| `VALIDATION_PLAN` | 検証集合、method binding、途中result非消費、nonterminal継続 | `VP1-VP6` |
| `VALIDATION_EXECUTION` | validation readiness、個別実行、fail-fast、result収集、完了handoff | `VC1-VC9` |
| `METHOD_RECOVERY` | method選択、失敗とpermissionの分離、environment recovery allowance | `M1-M6, RC1-RC3` |

合計は81 / 81である。`not_applicable`または意味削除へ分類したprimitiveは0件である。

## 共通語彙

portable kernelは製品名、role API名、tool名、field名または配送方式を本文へ持たない。次の語を共通の意味として使う。

| 語 | 意味 |
| --- | --- |
| `request contract` | 利用者入力と、その操作へ適用される明示authorityの集合 |
| `operation` | 一つの成果、predicate、permission、constraintおよびterminalを共有する単位 |
| `actor` | 一operationのpredicate実行とresult生成を所有する一つのexecution identity |
| `coordinator` | actorでない場合にinput準備、result対応づけおよびterminal集約だけを行う実行 |
| `observation` | 未観測値を返すread-onlyな取得。file、web、tool、messageまたは既存resultの種類を問わない |
| `action` | 外部状態または成果物を変える操作 |
| `result` | operation、actor、入力およびresult kindへ対応づけられる観測可能な出力 |
| `frontier` | 現在の未解決resultで発行可否が変わらない、開始可能なoperation集合 |
| `terminal` | required resultが全て対応づけられ、未完了executionまたは欠落resultがない状態 |
| `unavailable` | 必要な能力、入力または観測点がなく、推測や代行なしではresultを作れないterminal result |

`root`、`worker`、`model step`、`fork_turns`、`exec_command`、`wait`、`cell ID`または固有counterは共通語彙へ入れない。

## clause別の状態境界

### `OUTCOME`

入力はrequest contractである。利用者が観測する成果をoperationへ分け、各operationのpredicate、criterion owner、permissionおよびconstraintを先に固定する。成果値は利用者入力またはその値を直接要求する一意なauthorityだけから採用する。target、path、command、method、現在値、候補集合、test expectationまたは便宜を成果値の代替にしない。

成果値が未固定なら、未固定値だけをclarification resultにし、actor binding、predicate実行、observation、actionおよびvalidationを開始しない。先行resultまたはartifactから別operationを作る場合も、固有predicate、ownerおよびactorを実行前に固定する。result、constraintおよびterminalの効果を別operationへ伝播させない。

このclauseは`S1-S8`と`I1`を所有する。

### `ACTOR`

各operationは初回predicate前に一つのactor identityへbindする。同じoperationのpredicateまたはresult生成を別actorへ再割当てしない。criterion ownerはrisk metadataであり、request contractが独立executionを要求した場合だけactor選択を拘束する。

独立executionが要求された場合は、そのidentityを固定してpredicate前に開始する。受領resultは、事前identity、開始identity、送信元、operationおよびresult kindへ対応できる場合だけ採用する。同期、進捗、別actorの記述またはcoordinatorの再構成をprovenanceの代替にしない。対応不能ならpassedにせず`unavailable`にする。`false / failed`は対応operationのterminal resultとして保持する。

coordinatorがactorでないoperationではinput準備、result対応づけおよびterminal集約だけを行い、predicateを実行せずresultを再生成しない。actor変更時は旧bindingを失効させ、新しいoperation specificationで固定し直す。

このclauseは`P1-P5`、`O1-O7`、`R1-R2`および`I2`を所有する。

### `INPUT`

actorへ渡す入力をcriterion、owner、pass condition、request contractの該当範囲、target、対象内容または採用済みresult、required evidence、allowed observationおよびforbidden inputへ閉じる。この入力で判定可能なら無関係な履歴を加えない。不足時も現在のpredicateに必要な最小入力だけを追加し、利便性や参照可能性を入力拡大の理由にしない。

surfaceが入力を分離配送できない場合、禁止入力を含む広いcontextで独立actor operationを成立したことにしない。必要な入力境界を作れなければ`unavailable`とする。

このclauseは`C1-C4`を所有する。

### `OBSERVATION`

observationは全lifecycleでdefault denyとする。required predicateを`satisfied / unsatisfied / unobserved`で保持し、predicateが未完了かつ`unobserved`で、現在欠けている値が固定済みで、requested resultがその値を返せる場合だけ一件を許可する。同じ資格を探索、変更前後、validation準備およびrecoveryへ適用する。

成果未固定時はrequest contractと明示開始状態だけを観測し、clarificationで変更前観測を閉じる。成果固定後はtarget、明示read-only対象、適用中instructionおよびimplementation authorityだけを変更前観測にできる。methodやlocator未固定だけで観測済みpredicateを未観測へ戻さず、permission、利用可能能力または一般的安全確認を追加観測の開放条件にしない。

変更または失敗resultは入力が変わったpredicateだけを失効させ、consumer完了時は未発行observationを失効させる。追加observationは、直前resultが具体的な不足、読取不能、矛盾、許可範囲内の充足不能または別authorityを示した場合だけ一件許可する。

target、instruction、全change effect、artifact relation、action predicateおよび保持constraintが現在状態上の一案へ揃った場合だけimplementationをreadyにする。observationで手段は固定できるが成果値は事後補完しない。ready後は未発行の変更前observationを失効させ、actionへ進む。変更後に確定するvalidationは`VALIDATION_PLAN`へ渡し、変更前観測へ戻さない。

このclauseは`E1-E15`を所有する。

### `FRONTIER`

受領予定resultごとに、そのresultでtarget、permission、methodまたはstop conditionが変わり得る未発行operation classを先に固定する。resultの停止効果をその範囲へ限定し、task全体または独立operationへ広げない。

effect scope外にある既知の相互非依存operationからfrontierを構成し、その全対象を、いずれかの途中resultを次の選択または抑止へ使う前に開始する。frontier内の全resultを受領するまで一部resultを次判断へ使わず、全result受領後に一度だけ次のoperationを判断する。

開始identity resultについては、drift時に禁止されるoperation classだけをeffect scopeへ入れる。drift時もobservationが禁止されずtargetとpermissionが変わらないなら、identity観測とそのobservationを同じfrontierへ入れる。共同result受領まではactionとrequired executionだけを保留する。observation自体が禁止されるかtargetまたはpermissionが変わり得る場合だけ後続へ分ける。

surfaceが複数対象の開始前に途中resultを強制消費させる場合、同じfrontier closureを成立したと宣言しない。必要なoperationでは`unavailable`とする。

このclauseは`D1-D11`を所有する。

### `COMPLETION`

全required predicateに、bind済みactorの対応可能なterminal resultがある場合だけoperationをterminalにする。invocation、actor executionまたはsessionがnonterminal、またはresultが欠ける場合はoperationもnonterminalのまま保持する。進捗、要約、集約記述またはfinal responseで欠けたresultを補完しない。

このclauseは`T1-T3`を所有する。

### `VALIDATION_PLAN`

action後、全required validation、順序、個別pass condition、stop conditionおよび完了判断に必要な既知の状態確認を、validation開始前に一つのplanへ固定する。exact methodが明示された場合だけそのmethodを固定し、それ以外は既存inputから選んでplan開始時に固定する。method未固定だけをmissing validationまたは追加observationの理由にしない。

途中validationがsuccessでも新しい判断へ使わずplanの残りへ進む。全result受領後に一度だけ完了を判断し、追加要求またはresult失効がなければ操作を加えない。nonterminal resultでは同じinvocationのterminal化だけを継続し、別判断、別操作または完了報告を挟まない。surfaceが同じinvocationを識別できなければresultを補完せず`unavailable`にする。

このclauseは`VP1-VP6`を所有する。

### `VALIDATION_EXECUTION`

action完了とplanの全predicate、順序、個別pass conditionおよびstop conditionが揃った場合だけvalidationをreadyにする。protocolがexact methodを明示するvalidationだけ、そのmethod bindingをready条件にする。

readyなrequired validationを固定順の個別executionとして一つの発行判断から開始し、各result identityを保持する。non-successまたはunavailableを受領したら後続を開始しない。個別validationを一つの不可分な結果へ潰さず、全完了resultを一度だけ結果消費側へ渡す。全件successかつ全result bind済みなら追加observationをせずterminalを判断し、欠落、non-successまたはunexpected stateを未完了として保持する。

このclosureを探索、変更前、review finding、method探索またはrecoveryへ流用しない。surfaceが個別resultとfail-fastを同時に保持できなければ、必要なvalidation operationを成立したことにせず`unavailable`にする。

このclauseは`VC1-VC9`を所有する。

### `METHOD_RECOVERY`

request contractが明示したmethodだけを固定する。未固定methodはpredicateとpermissionを変えず許可範囲から選び、validation methodはplan開始時に既存inputから固定する。exact method選択だけを理由にobservationを追加しない。

methodの`failed / unavailable`をpermission denial、predicate resultまたはoperation terminalへ変換せず、許可された代替methodがあれば同じpredicateへ向けて継続する。明示禁止またはpermission denialでは停止し、回避しない。

environment recoveryは、環境だけのrepairと同じrequired execution再試行を一組として扱う。明示authorityへ固定済みのallowanceがある場合だけ開始し、組の開始時に一回消費する。未固定methodの選択をrecovery消費に数えない。

このclauseは`M1-M6`と`RC1-RC3`を所有する。

## 正の遷移を落とさない接続

C204とC205の反例を繰り返さないため、禁止条件だけでなく次の正の遷移をclause間のhandoffとして固定する。

| from | terminal output | to | 必須の正の遷移 |
| --- | --- | --- | --- |
| `OUTCOME` | operationと成果値 | `ACTOR / OBSERVATION` | actor bindingと必要観測の資格判定を開始する |
| `ACTOR` | actor identityまたは`unavailable` | predicate execution | 独立executionが要求された場合はpredicate前に開始する |
| `OBSERVATION` | implementation ready | action | 未発行pre-action observationを閉じ、actionを開始する |
| `FRONTIER` | exact frontier | operation issuance | 全対象をpartial result消費前に開始する |
| action | changed state | `VALIDATION_PLAN` | 変更後に確定するvalidationをplanへ渡す |
| `VALIDATION_PLAN` | closed plan | `VALIDATION_EXECUTION` | readyな個別validationを固定順で開始する |
| validation success | remaining plan | `VALIDATION_EXECUTION` | 外側判断へ戻らず残りを開始する |
| `VALIDATION_EXECUTION` | 全個別terminal result | `COMPLETION` | 一度だけterminalを判断する |

handoffをsurfaceの「推奨順序」として扱わない。前段resultが後段のpermission、targetまたは開始条件を直接固定するdependencyとして扱う。

## 逆引き完全性

| 元条項 | primitive数 | portable clause | coverage |
| --- | ---: | --- | ---: |
| `SPEC` | 8 | `OUTCOME` | 8 / 8 |
| `PRODUCER` | 5 | `ACTOR` | 5 / 5 |
| `TERMINAL` | 3 | `COMPLETION` | 3 / 3 |
| `CONTEXT` | 4 | `INPUT` | 4 / 4 |
| `EVIDENCE_GATE` | 15 | `OBSERVATION` | 15 / 15 |
| `OWNER_ROLE` | 7 | `ACTOR` | 7 / 7 |
| `ROOT` | 2 | `ACTOR` | 2 / 2 |
| `INDEPENDENCE` | 2 | `OUTCOME / ACTOR` | 2 / 2 |
| `DECISION_BOUNDARY` | 11 | `FRONTIER` | 11 / 11 |
| `VALIDATION_CLOSURE` | 9 | `VALIDATION_EXECUTION` | 9 / 9 |
| `VALIDATION_PLAN` | 6 | `VALIDATION_PLAN` | 6 / 6 |
| `METHOD` | 6 | `METHOD_RECOVERY` | 6 / 6 |
| `RECOVERY` | 3 | `METHOD_RECOVERY` | 3 / 3 |
| **合計** | **81** | 9 clause | **81 / 81** |

これはsemantic coverageの設計上の対応であり、文面の機序成立を意味しない。exact prompt本文を作る場合は、各primitiveをどの文が直接拘束するかを文単位で再監査する。

## Candidate作成前に残るgate

次が未完了なのでexact prompt本文とCandidate bundleを作成しない。

1. 共通semantic conformance targetのcaseと正常最短経路。
2. 各caseで実際に防ぐ問題経路とresult effect。
3. model-visible operation ledger、model-invisible oracleおよびrating contract。
4. 9 clauseを消費するcase coverageと対象外影響。
5. control-free baselineの測定成立。
6. surface別のload receipt、capability boundaryおよび停止条件。

## 参照

- [`C147由来のruntime非依存portable instruction設計`](runtime-independent-execution-control-draft.md)
- [`C147 portable kernel coverage台帳`](c147-portable-kernel-coverage-ledger.md)
- [`Candidate147機能分解の再分析`](c147-functional-decomposition-reanalysis.md)
- [`Candidate147制御群・境界重複・最適性監査`](c147-control-group-overlap-optimality-audit.md)
- [`Candidate204 M5原因分析`](candidate204-m5-causal-analysis.md)
- [`Candidate205 M5原因分析`](candidate205-m5-causal-analysis.md)

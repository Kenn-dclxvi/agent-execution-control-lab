# Candidate147 機能分解の再分析

> [!IMPORTANT]
> **状態**: `primitive_inventory_complete / control_group_semantics_in_progress / optimality_not_evaluated / prior_M1_M2_reopened / Candidate204_and_205_counterexamples_only / next_candidate_not_authorized`
>
> C147の各条項がまとめて制御する対象、条項間の境界重複、重複による強化または競合を調べるため、文単位primitiveを補助台帳として使う。primitiveを新ownerへ再配置するための設計図にはしない。Candidate作成、評価slot発行、採用、release、projectionは許可しない。
>
> 13条項のまとまり、境界重複および最適性の現行判断は[`Candidate147 制御群・境界重複・最適性監査`](c147-control-group-overlap-optimality-audit.md)を正とする。

## 結論

従来の再分類はC147の13条項を一行ずつ新ownerへ対応づけており、機能分解として粗かった。状態の定義と禁止条件は残した一方で、次の実行を前へ進める正の遷移と、resultを判断へ渡す前の収集障壁を独立した機能として把握できていなかった。

ただし、逆にprimitiveへ細分化しただけでもC147を理解したことにはならない。各条項は、定義、開放条件、正の動作、禁止条件、収集障壁、terminalまたはhandoffをまとめて制御する単位である。分析の主対象は13条項のまとまりと相互関係であり、81 primitiveは各まとまりの内訳を見落とさないための補助情報である。

## C147の位置づけと最適性の境界

C147はゴールまたは最適解として固定しない。現時点では、既知のStandard14品質と対象機構を高い再現性で成立させた参照到達点である。

- Standard14 N=100の1,400 / 1,400 Score 4は、固定した14ケースと互換条件における品質安定性を示す。
- F01 / F02 / F03各N=5の15 / 15は、固定した対象経路で`result_effect_scope`が狙った発行順序を成立させたことを示す。
- これらは13条項、各条項内のまとまり、条項間の重複を一件ずつ除去・置換して比較した試験ではない。
- Standard14は、未試行の構成や簡素化よりC147が最適であること、これ以上token、elapsed、model stepまたは判断点を改善できないことを証明しない。
- 採用・release・projection済みであることも、設計探索の終点または最適性を意味しない。

したがって既定判断は「C147を最適として維持」ではない。C147を現在の比較基準として保ちつつ、各制御群が何を閉じるか、境界重複が強化か競合か、変更可能性を判定するための証拠があるかを監査する。変更証拠がない箇所は`optimal`ではなく`change_not_justified`、比較していない箇所は`not_evaluated`として残す。

C147は少なくとも次の実行鎖として扱う必要がある。

```text
成果値を固定する
  -> operationとproducerを固定する
  -> inputと必要な観測値を限定する
  -> 発行候補集合を構成する
  -> 選んだ全対象をresult消費前に発行する
  -> 必要な全resultを収集する
  -> provenanceを確認してresultをadmitする
  -> 依存する未完了operationだけへ効果を反映する
  -> 変更または検証へ正に遷移する
  -> terminal条件を閉じる
```

C204は主に状態、eligibility、result effect、terminal条件を再配置したが、発行候補集合の構成、正の発行、収集障壁を持たなかった。C205は`ISSUANCE`を足したが、C147が持っていた具体的な候補集合の構成と、全対象の発行をresult消費より前へ置く契約を復元していない。C204/C205は再構成の親ではなく、欠落を示す反例として保持する。

## 分解方法

- predicateを定義する機能と、成立時に次の処理を発行する機能を分ける。
- 対象集合の構成、発行、result収集、result解釈を分ける。
- 禁止条件と正の遷移を分ける。
- runtime固有の表面語と、その表面語が実現していた観測可能な順序制約を分ける。
- 保存traceで確認できる機能と、本文の意味だけから抽出した機能を区別する。

`同一model step`、`modelへ戻らず`、`custom exec wrapper`などの表面語はportable coreへ逐語的に残す対象ではない。しかし、それらを削る際に「選択した全invocationを、いずれかのresultを次の選択へ消費する前に開始する」という順序制約まで削ってはならない。これは外部executorのatomicity要求ではなく、promptが次に何を発行するかを決める制御である。

## 全13条項の機能primitive

### `SPEC`

| ID | 機能 |
|---|---|
| `S1` | 実行前にrequired outcomeをoperation identityへ分ける。 |
| `S2` | 各operationへ`predicate / criterion owner / permission / constraint`を固定する。 |
| `S3` | required outcome valueを明示user inputまたはその値を直接要求する一意なrepository authorityだけへbindする。 |
| `S4` | required outcomeとimplementation choiceを分類し、path、module、command、実装方法を自動的に成果値へ昇格させない。 |
| `S5` | current value、option set、complement、test expectation、implementation convenienceをoutcome bindingの代替にしない。 |
| `S6` | `spec_ready=false`の間、producer binding、predicate、変更、testを開始しない。 |
| `S7` | 未固定のrequired outcome valueだけをclarification resultにする。 |
| `S8` | result、constraint、terminalの効果を同じoperation identity内へ限定する。 |

### `PRODUCER`

| ID | 機能 |
|---|---|
| `P1` | 初回predicate前に一つのproducer execution identityをbindする。 |
| `P2` | 同一operationのpredicateとresult生成を別producerへ順次または並行に再割当てしない。 |
| `P3` | TaskSpecが独立executionを明示した場合だけ、そのidentityをproducerへbindする。 |
| `P4` | criterion owner語列をproducer選択へ使わない。 |
| `P5` | producer変更時は旧bindingを失効させ、新identityのTaskSpecでbindし直す。 |

### `TERMINAL`

| ID | 機能 |
|---|---|
| `T1` | 全predicateにbind済みproducerのterminal resultがある場合だけoperationをterminalにする。 |
| `T2` | invocation、producer execution、sessionのnonterminalまたはresult欠落をoperationのnonterminalとして保持する。 |
| `T3` | 進行報告、集約結果、final responseで欠けたresultを補完しない。 |

### `CONTEXT`

| ID | 機能 |
|---|---|
| `C1` | producer inputへcriterion、owner、pass condition、TaskSpec範囲、target、対象内容またはresult、required evidence、allowed read、forbidden inputを固定する。 |
| `C2` | packetとallowed readだけで判定可能なら無関係な履歴を渡さない。 |
| `C3` | 不足時も意味保持に必要な最小inputだけを追加する。 |
| `C4` | 利便性、念のため、無関係なtool outputの参照可能性をinput拡大の根拠にしない。 |

### `EVIDENCE_GATE`

| ID | 機能 |
|---|---|
| `E1` | repository evidence invocationを全lifecycleでdefault denyにする。 |
| `E2` | required predicateを`satisfied / unsatisfied / unobserved`で保持する。 |
| `E3` | nonterminal、unobserved、missing value bind済み、requested resultが値をbind可能、の全条件からconsumer eligibilityを判定する。 |
| `E4` | 同じeligibilityを探索、変更前、変更後、validation準備、recoveryへ適用する。 |
| `E5` | validation predicateが固定済みなら、exact commandやtest locatorが未固定なだけでunobservedへ戻さない。 |
| `E6` | 変更または失敗resultは、入力が変わったpredicateだけを失効させる。 |
| `E7` | consumer terminal時に未発行evidenceを失効させる。 |
| `E8` | `spec_ready=false`ではTaskSpec本文と明示開始状態だけを許可し、clarificationで変更前evidence operationを閉じる。 |
| `E9` | `spec_ready=true`後の変更前readをtarget、明示read-only path、適用中instruction、implementation authorityへ限定する。 |
| `E10` | repository evidenceでimplementation choiceはbindできるがrequired outcomeは事後補完しない。 |
| `E11` | target、instruction、全change effect、artifact relation、変更predicate、保持constraintが一案へ揃った場合だけ`implementation_bound=true`にする。 |
| `E12` | implementationがbindされたら未発行の変更前evidenceを失効させ、artifact変更を正に発行する。 |
| `E13` | 変更後に確定するvalidation identityは`VALIDATION_PLAN`へ渡し、変更前evidence operationを再開しない。 |
| `E14` | 追加evidenceは、直前resultがmissing、unreadable、具体的矛盾、allowed path内で充足不能、または別authority明示を観測した場合だけ一件ずつ許可する。 |
| `E15` | permission、allowed read、available tool、一般的安全確認を追加evidenceの開放条件にしない。 |

### `OWNER_ROLE`

| ID | 機能 |
|---|---|
| `O1` | criterion ownerをnon-machine risk metadataとして保持し、routingへ使わない。 |
| `O2` | TaskSpecが独立executionを明示した場合、task identityをbindしてpredicate前にproducer executionを開始する。 |
| `O3` | 事前task identity、runtime起動identity、terminal resultの送信identity、criterionまたはtargetへの対応からprovenanceを判定する。 |
| `O4` | 同期結果をproducer provenanceの代替にしない。 |
| `O5` | provenance成立前はcriterionをpassedにせず、producer terminal後も不成立なら`unavailable`にする。 |
| `O6` | bind済み`false / failed`を当該operationのterminal resultとして保持し、別operationのresultを失効させない。 |
| `O7` | coordinatorの宣言、進行記述、異producer message、再構成でresultを補完しない。 |

### `ROOT`

| ID | 機能 |
|---|---|
| `R1` | producerでないcoordinatorはinput構築、result binding、terminal集約だけを行う。 |
| `R2` | producerでないcoordinatorはpredicate実行またはresult再生成をしない。 |

### `INDEPENDENCE`

| ID | 機能 |
|---|---|
| `I1` | 先行resultまたはartifactを対象とする別operationへ固有predicate、owner、producerを実行前に固定する。 |
| `I2` | 同一predicateを別producerへ再割当てしない。 |

### `DECISION_BOUNDARY`

| ID | 機能 |
|---|---|
| `D1` | 受領予定resultがtarget、permission、method、stop conditionを変え得る未発行operation classを、次の発行判断前に特定する。 |
| `D2` | 各next operation classがそのeffect scopeへ属するかを判定する。 |
| `D3` | resultの停止効果をtask全体や全後続invocationへ広げない。 |
| `D4` | effect scope外にある既知の相互非依存invocation集合を構成する。 |
| `D5` | 構成した集合を分割せず、全invocationをresult消費前に正に発行する。 |
| `D6` | 集合内の全resultを受領するまで、その一部を次の選択または抑止へ使わない。 |
| `D7` | 全result受領後に一度だけ次のoperationを判断する。 |
| `D8` | TaskSpec明示の開始identity resultについて、drift時に禁止されるoperation classだけをeffect scopeへ入れる。 |
| `D9` | drift時もreadが禁止されず、read targetとpermissionも変わらないなら、identity観測とreadを同じ発行集合へ入れる。 |
| `D10` | 共同result受領まではartifact変更とrequired commandだけを保留する。 |
| `D11` | read自体が禁止されるかread targetまたはpermissionが変わり得る場合だけreadを後続へ分ける。 |

### `VALIDATION_CLOSURE`

| ID | 機能 |
|---|---|
| `VC1` | artifact変更、全validation predicate、順序、個別pass condition、stop conditionが揃ったときだけvalidationをreadyにする。 |
| `VC2` | protocolがexact commandを明示するvalidationだけ、そのcommandのbindingをready条件にする。 |
| `VC3` | readyな全required validationを、bind順の個別invocationとして一つの発行判断から開始する。 |
| `VC4` | 各resultを個別に判定し、non-successまたはunavailableで後続を発行しない。 |
| `VC5` | 個別validationを一つのshell compound commandへ結合しない。 |
| `VC6` | 全完了resultを一度だけ結果消費側へ渡す。 |
| `VC7` | 全件successかつ全result bind済みなら追加readやvalidationをせずterminalを判断する。 |
| `VC8` | 欠落、non-success、unexpected stateをnonterminalとして保持する。 |
| `VC9` | このclosureをtarget探索、変更前、review finding、method探索、recoveryへ流用しない。 |

### `VALIDATION_PLAN`

| ID | 機能 |
|---|---|
| `VP1` | artifact変更後、required validationと完了判断に必要なdiffまたはstatusを一つの実行票へ順にbindする。 |
| `VP2` | exact commandが未指定なら、既に受領したTaskSpec、instruction、target evidenceからmethodを選び、実行票発行時にbindする。 |
| `VP3` | command未固定だけをmissing validationまたは追加evidenceの理由にしない。 |
| `VP4` | validation success後は途中resultを次の判断へ返さず、実行票の残りを正に発行する。 |
| `VP5` | 全result受領後に一度だけ完了を判断し、追加要求または失効がなければtoolを追加しない。 |
| `VP6` | invocationがnonterminal identityを返した場合は同じidentityのterminal化だけを待ち、別判断、別tool、完了報告を挟まない。 |

### `METHOD`

| ID | 機能 |
|---|---|
| `M1` | TaskSpec明示methodだけを固定する。 |
| `M2` | 未固定methodはpredicateを変えずpermission内から選ぶ。 |
| `M3` | validation methodは実行票発行時に既存inputからbindする。 |
| `M4` | exact command選択だけを理由にrepository evidenceを追加しない。 |
| `M5` | invocationのfailedまたはunavailableをpermission denialやterminalへ変換せず、許可された別methodで同じpredicateへ継続する。 |
| `M6` | 明示禁止またはpermission denialでは停止し、回避しない。 |

### `RECOVERY`

| ID | 機能 |
|---|---|
| `RC1` | environment recoveryを環境だけのrepairと同じrequired execution再試行の組として扱う。 |
| `RC2` | allowanceを組の開始時だけ消費する。 |
| `RC3` | 未固定methodの選択をrecovery消費に数えない。 |

## C204/C205との対応

| 機能群 | C204 | C205 | 再分析 |
|---|---|---|---|
| outcome、producer、input、result admission、local effect、terminal | おおむね保持 | 保持 | owner統合の妥当性はprimitive単位で再確認する |
| evidence eligibility | 保持 | 保持 | eligibilityだけでは実行は開始されない |
| implementation closure | 一部保持 | 一部保持 | `E12`のartifact変更への正の遷移が独立機能として見えていない |
| producer executionの開始 | 一部保持 | 一部保持 | `O2`の正の開始をproducer bindingへ埋め込んでいる |
| 独立invocation集合の構成 | 「偽dependencyを足さない」へ弱化 | frontier定義へ抽象化 | `D1 / D2 / D4 / D8 / D9 / D11`を一体で閉じる必要がある |
| 集合全件のresult消費前発行 | 欠落 | `ISSUANCE`を追加したが対象集合が具体化されない | `D5`が未復元 |
| 集合全件の収集障壁 | 欠落 | frontier一部resultを消費しない、と記述 | `D6 / D7`の成立はtraceで0 / 15 |
| validationの正の発行driver | closure条件へ統合 | 同左 | `VC3 / VP4`を独立して保持する必要がある |
| nonterminal継続 | 一般化して保持 | 保持 | `VP6`の同じidentityだけを待つ意味をportableに保つ必要がある |

C205へさらに一つのlabelを足す設計には進まない。まず全primitiveについて、統合しても同じ実行鎖が残るもの、portable表現へ置換すべきもの、対象外へ除外できるものを一件ずつ決める。

## primitiveの暫定処置

今回抽出した81 primitiveについて、意味ごと削除してよいと立証できたものは現時点で0件である。これは81件すべてが必要または最適だという判定ではない。除去比較、境界重複の効果分離、非対象経路へのcost確認が未実施なので、意味の除去は全件`not_evaluated`である。下表は、意味を落とさず表面形を比較可能にするための暫定的な読替えだけを示す。

| 条項 | 現在確認できる意味 | runtime固有表面形の読替え対象 | 意味の除去評価 |
|---|---|---|---|
| `SPEC` | `S1`〜`S8` | なし | `not_evaluated` |
| `PRODUCER` | `P2`〜`P5` | `P1`: `root / worker`ではなく事前bind済みproducer identityとして読めるか | `not_evaluated` |
| `TERMINAL` | `T1`〜`T3` | なし | `not_evaluated` |
| `CONTEXT` | `C1 / C4` | `C2 / C3`: turn継承指定をinput sufficiencyと最小追加inputで表せるか | `not_evaluated` |
| `EVIDENCE_GATE` | `E1`〜`E15` | lifecycle名やtool種別を状態predicateで表せるか | `not_evaluated` |
| `OWNER_ROLE` | `O1 / O5 / O6 / O7` | `O2`: producer開始、`O3`: 事前identityとterminal resultの対応、`O4`: 同期とprovenanceの分離として表せるか | `not_evaluated` |
| `ROOT` | なし | `R1 / R2`: producerでないcoordinatorの権限制限として表せるか | `not_evaluated` |
| `INDEPENDENCE` | `I1 / I2` | なし | `not_evaluated` |
| `DECISION_BOUNDARY` | `D1`〜`D4 / D6 / D8 / D10 / D11` | `D5 / D7 / D9`: 全対象のresult消費前commitと共同result後の一回判断として表せるか | `not_evaluated` |
| `VALIDATION_CLOSURE` | `VC1 / VC2 / VC4 / VC6`〜`VC9` | `VC3`: 閉じた実行票からの発行、`VC5`: 個別result identityの保持として表せるか | `not_evaluated` |
| `VALIDATION_PLAN` | `VP1`〜`VP3 / VP5` | `VP4`: 途中resultを新判断へ使わない、`VP6`: 同一invocation identityのterminal化だけを継続する、と表せるか | `not_evaluated` |
| `METHOD` | `M1`〜`M6` | なし | `not_evaluated` |
| `RECOVERY` | `RC1 / RC3` | `RC2`: authorityへbind済みallowanceの消費として表せるか | `not_evaluated` |

この処置は、81個のlabelをそのまま新promptへ置くという意味ではない。統合の可否を判断する前に、各primitiveの入力、出力、正の遷移、禁止条件が別の文で完全に保持されることを証明するための台帳である。

特に次の局所的な重なりは、現時点では削除しない。

- `S8`、`E6`、`O6`、`D3`はすべて効果の局所化に関係するが、それぞれspecification、predicate invalidation、producer result admission、次operation選択という異なる地点を閉じる。
- `P2`と`I2`はproducer再割当て禁止として重なるが、前者は同一operation、後者は先行resultを対象とする別operationの生成地点を閉じる。
- `T2`、`VC8`、`VP6`はnonterminalを扱うが、operation全体、validation result、継続中invocationという異なるidentityを閉じる。
- `E12`、`O2`、`D5`、`VC3`、`VP4`はすべて正の発行を担うが、artifact変更、producer開始、独立read集合、validation開始、validation継続という別operation classに属する。

これらを共通語へ整理してから不足だけを探すと、どの地点で実行が前へ進むかが再び消える。一方、C147を完成済み最適解として全件維持するのも根拠がない。次段では、13条項ごとに制御対象と局所closureを記述し、条項間の境界重複を`異なる入口での強化 / 同じ入口の冗長候補 / 相互制限 / handoff / 競合候補`へ分類する。その後、保存traceで変更効果を分離できる箇所だけを最適化仮説へ進める。

## C147保存traceによる順序機能の確認

C147 F01 / F02 / F03各N=5の15 atomic runについて、保存rolloutの最初のassistant方針と最初のtool発行を再監査した。従来の「同じagent message内に開始されたか」ではなく、「開始identity resultが外側の判断へ返る前に、identity観測と許可済みreadの両方が発行対象として確定していたか」を判定した。

| 観測 | 件数 |
|---|---:|
| 最初の方針でidentity観測とreadを共同実施すると明示 | 15 / 15 |
| 最初の一つのtool発行にidentity観測とreadの両方を含む | 15 / 15 |
| 複数commandを同じ発行処理から並行開始 | 12 / 15 |
| identity観測とreadを一つのcommand内で順に実行 | 3 / 15 |
| identity resultを外側の次判断へ返した後にreadを別発行 | 0 / 15 |

3件はcommand内部では逐次だったため、runtime-levelの同時開始15 / 15を主張しない。15件に共通する機能は、identity resultを次の判断へ消費する前に、identity観測とreadの両方を発行対象へcommitしていたことである。portableな保持対象はこの順序制約であり、特定API名やresponse単位ではない。

C205の15件はidentity command完了前にread commandが開始されたrunが0件だった。従来のmechanism auditで共同発行とした1件も、二つのcommand間にagent messageがなかっただけで、identity完了後にreadを別tool発行していた。agent message境界はC147機能の判定oracleとして弱く、C205の成立数は強いイベント順序基準では0 / 15である。

## いま撤回する判断

- 旧M1の「全13条項を新ownerへ分類したので機能把握が完了した」という判断。
- 旧M2の「12の状態遷移ownerでC147の機能を閉じた」という判断。
- C204の失敗原因を`ISSUANCE`一責任の欠落だけへ限定した判断。
- C205の失敗をexact eligible invocation set未bindだけへ限定した判断。
- C205のmechanism成立1 / 15。強い順序基準では0 / 15とする。

これはC147、C204、C205の品質resultを変更しない。変更するのは再構成の完全性とmechanismの説明である。

## 次へ進む条件

1. 13条項それぞれについて、まとめている制御対象、entry、正の動作、禁止条件、barrier、terminalまたはhandoffを記述する。
2. 条項間の重複を、強化、冗長候補、相互制限、handoff、競合候補へ分類する。
3. 各判断を`optimal`ではなく、`supported / change_not_justified / optimization_hypothesis / not_evaluated`で記録する。
4. C147の15件とC205の15件を区別できるイベント順序oracleを固定する。
5. Standard14通過を最適性へ読み替えず、変更仮説ごとに対象経路、非対象経路、品質、機構、costの比較条件を別途固定する。
6. semantic auditだけでCandidateを作らず、変更対象を保存traceの具体的差へbindする。

## 参照

- [`Candidate147 release制御本文`](../prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/files/AGENTS.md.txt)
- [`Candidate147 result effect scope設計`](candidate147-result-effect-scope-design.md)
- [`Candidate147 F01 / F02 / F03 N=5結果`](../evaluations/results/candidate145-candidate147-result-effect-scope-v14-medium-f01-f02-f03-atomic-n5-cli0146_2026-08-02.md)
- [`旧C147原因再分類`](c147-review-free-portable-core-causal-reclassification.md)
- [`旧portable core M2設計`](c147-review-free-portable-core-design.md)
- [`Candidate205 M2設計`](post-candidate204-portable-issuance-frontier-design.md)
- [`prompt制御の検討原則`](prompt-control-design-principles.md)

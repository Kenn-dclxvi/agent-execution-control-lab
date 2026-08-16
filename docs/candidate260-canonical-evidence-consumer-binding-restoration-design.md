# Candidate260 証拠取得条件の発行前固定を復元する作成前gate

## 結論

Candidate260の作成前gateを固定し、このgateどおりにbundle、F04 profileおよび5件の評価を実施した。F04は5 / 5件がScore `4`だったが、4 / 5件で発行後の証拠取得条件作り直しが残ったため停止した。

直接の基準はCandidate147とする。Candidate254で観測した開始確認と必要readの共同発行、相互非依存発行、required validationの単一発行判断は、維持すべき局所境界の証拠として使う。Candidate254を親本文にはせず、Candidate255からCandidate259までの追加条件も継承しない。これらは、発行後の部分resultから同じ判定用の証拠取得条件を作り直せた経路、またはその経路を回数や人間語の分類で閉じられなかったことを示す反例としてだけ使う。ここで証拠取得条件とは、必要判定、現在欠けている観測値、その判定を確定できる取得結果の組を指す。

対象とする辺は、同じ発行前predicateについて、部分resultの受領後に新しい`required predicate / missing observation / requested result`の組を作り、その組を残りのreadの許可へ使う依存関係である。read回数、行数、範囲数、command数は合否条件にしない。

## 変更候補

Candidate254の`EVIDENCE_GATE`冒頭を、Candidate147の`evidence_consumer_ready`対応を保つ次の境界へ置き換える。

> repository evidence invocationは全lifecycleでdefault denyとする。`required_predicate_state := satisfied | unsatisfied | unobserved`、`evidence_consumer_ready := required predicateがnonterminal ∧ state=unobserved ∧ 現在欠けている観測値が発行前にbind済み ∧ requested resultがそのstateをbind可能`とし、`evidence_consumer_ready=true`の場合だけ発行する。発行後に受け取った部分result、取得済み範囲またはそれらの不足を、新しいrequired predicate、欠けた観測値またはrequested resultへrebindしても、発行前から同一だったrequired predicateを満たす残りのrepository evidence permissionは生じない。

この置換は、成功runのread範囲、検索語、command順または一回で読む手順を規定しない。発行前から別々の必要判定、欠けた観測値、requested resultへbind済みの複数readは合法である。受領resultが`missing / unreadable / bind済みvalueまたはconstraintとの具体的矛盾 / allowed path内で充足不能 / 適用中instructionによる別authorityの明示`を実際に観測した場合の追加evidenceも、Candidate147の既存境界のまま合法である。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 1. 比較基準と最短正常経路 | 直接の基準はCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`。F04の最短正常経路は、開始確認と発行前にbind済みの必要readを共同発行し、全resultから一つの実装方針を確定し、`App.tsx`だけを変更して、固定済みvalidationを一つの発行判断から完了する経路とする。 |
| 2. 保存済み問題経路と影響 | Candidate254 run `342cf77221a14660908dbb7e6cf6cc27`は`App.tsx` 261〜620行のresult受領後に621〜980行を発行した。Candidate258 run `cecace75ac6744e1879cc6c610f8abed`も260〜620行のresult受領後に620〜980行を発行した。どちらも対象、permission、method、stop conditionは変化せず、同じ変更判断の途中resultが残りのreadの開始条件になった。 |
| 3. 問題を許した辺 | Candidate254の自然文は「現在欠けている観測値」と「取得する結果」を発行前identityへ固定せず、read後の取得範囲を新しい局所状態へ読み替えられた。TaskSpecはF04の成果とvalidationを定め、repository authorityは実装内容を定めるが、必要判定、欠けた観測値、取得結果の組を発行前identityへ固定しないため、この依存関係を単独では閉じない。 |
| 4. 変更する条件と責任範囲 | `EVIDENCE_GATE`冒頭一段落だけを上記の境界へ置換する。rootが行う変更前repository evidence invocationのpermissionだけを扱う。worker選択、review、artifact変更、validation、recoveryの既存predicateは変更しない。回数、行範囲、artifact数、command数のlabelを追加しない。 |
| 5. 実行不能にする問題経路 | 最初の部分readを受領してから、その取得範囲または不足を新しい証拠取得条件へ対応づけ直し、同じ発行前predicate用の残りを別stepで読む経路を閉じる。局所predicateへ名前を付け替えても、発行前identityがないためpermissionは成立しない。 |
| 6. 維持する正常経路と観測値の受け渡し | rootが、発行前にbind済みの必要判定、欠けた観測値、requested resultを保持する。各requested resultが対応する観測値を運び、command、tool、行範囲は固定しない。相互に影響しない複数の証拠取得条件は、result受領前に同一model stepから発行する。真正なfailure resultだけは、そのresult identityと次のevidence identityを対応づけた既存の追加evidence経路へ進める。 |
| 7. 新しい判断と対象外への影響 | 新しい回数判定、必要性分類、部分read分類、ticketまたはlabelは増やさない。追加するのは、必要判定、欠けた観測値、取得結果の組を発行前identityへ固定することと、発行後に対応づけ直してもpermissionが生じないという時間境界だけである。真正な新規predicateは、受領resultがtarget、permission、methodまたはstop conditionを変えた場合に`result_effect_scope`へbindして別operationとして扱える。 |
| 8. 評価単位と順序 | 最初は既存F04 r2だけをN=5、`gpt-5.6-sol / medium`、Rating v14、Codex CLI 0.146.0、M=24、all-agent token accounting v1で評価する。実行有効性、品質、機序、対象外影響、KPIを分ける。品質と機序が全件通過した場合だけ、同じStandard14 r1 N=5へ進む。baselineは保存済みCandidate147を再利用する。 |
| 9. 逆結果と停止条件 | bundle作成前に、発行後の対応づけ直しを別名のpredicateで合法化できる、または正常な観測値の受け渡しを一意に説明できないと判明した場合は`candidate_not_created`で停止する。F04ではScore `4`未満、開始共同発行未達、相互非依存発行の分割、発行後の証拠取得条件作り直し、validation境界未達のいずれか一件で停止し、追加N、Standard14、repair rerunへ進めない。 |

## F04機序判定

新しい合否判定は`post_result_consumer_rebinding_count`だけを対象差分とする。各runで、変更前repository evidence invocationについて次を時系列で記録する。

1. invocation発行前にbindされていたrequired predicate identity、state、欠けた観測値、requested result。
2. 先行resultの受領後に初めて作られた、必要判定、欠けた観測値、取得結果の組の有無。
3. 新しいtupleが、発行前から同一だったpredicateを満たす残りのreadへpermissionを与えたか。
4. 追加readがCandidate147の列挙するfailure resultへ直接bindされた回復か。

2と3がともに成立し、4でない場合だけ一件の機序不通過とする。同一artifactを複数回読んだこと自体、複数artifactを読んだこと、一つのreadが複数範囲を返したことは合否へ使わない。

F04 N=5のgateは次の全件通過を要求する。

- valid / rateable: 5 / 5
- Score `4`: 5 / 5
- 開始確認と必要readの共同発行: 5 / 5
- 相互非依存invocationの別step化: 0 / 5
- `post_result_consumer_rebinding_count`: 0 / 5
- required validationの単一発行判断: 5 / 5
- required commandの欠落、順序違反、shell compound: 0 / 5

## 構成境界

- direct baseline: Candidate147
- 維持する観測事実: Candidate254の開始共同発行、相互非依存発行、validation境界
- 問題経路が閉じていないことを示す反例としてだけ使うもの: Candidate254の失敗run、Candidate255、Candidate256、Candidate257、Candidate258、Candidate259
- not inherited: Candidate259の回数制限、Candidate255の部分read禁止、Candidate256の発行単位、Candidate257の三者分類文、Candidate258の途中result条件
- proposed target: root `AGENTS.md`の`EVIDENCE_GATE`冒頭一段落だけ
- bundle: 作成済み
- profile: 作成済み
- evaluation: F04 N=5完了・機序不成立で停止

## 現在状態

作成前gateの9項目、正常な観測値の受け渡し、対象機序および停止条件を変更せず評価した。品質は5 / 5件で通過したが、対象機序は1 / 5件だけが通過した。Candidate147比はquality同値、token `+16.49%`、elapsed `-28.69%`だった。機序不成立のため、この差をCandidate260の制御効果へ帰属しない。固定済み停止条件に従い、追加N、Standard14、修復目的の再実行へ進めない。

`creation_gate_fixed / candidate_created / profile_created / f04_n5_completed / quality_passed / kpi_compared / quality_same / token_regressed_16_49_percent / elapsed_improved_28_69_percent / mechanism_failed / stopped / standard14_not_started`

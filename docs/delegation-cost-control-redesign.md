# Worker委譲のコスト判定と制御再設計

## 結論

Workerを起動した事実をcandidateの失敗条件にしない。Workerの必要性はAIの実行方法選択として残し、その選択を含む実行全体を`quality_score`、all-agent `total_tokens`、`elapsed_seconds`の3 KPIで判定する。

Worker routing、child token、並列／逐次実行、再割当て、rootによる再確認はdiagnosticである。これらはKPI差の原因を説明するが、単独でcandidateを失敗させない。

C83とC84の一次resultおよび当時の`stopped`判定は変更しない。現在解釈では、C83を`quality_passed / cost_control_not_demonstrated`、C84を`quality_passed / cost_control_mixed`とする。どちらも採用可能とは判断しない。

## 確認した設計上の衝突

評価基盤はWorker routingをdiagnosticとして扱い、正式KPIを品質、all-agent token、elapsedの3つに限定している。一方、C83とC84はF02 / F04のWorker routeを独立した停止条件へ昇格した。

さらにF02とF04のmodel-visible TaskSpecには、それぞれ`owner=independent contract check`、`owner=independent source check`がある。`owner`はcriterionの証拠責任metadataだが、実行modelは一部runでproducer指定へ再分類した。C83とC84は、この再分類を語義predicateで抑えようとして条件を増やした。

この構造では、除外語を増やしても別の言い換え経路が残る。Workerの期待価値をprompt内の完全なboolean predicateにする方向は停止する。

## 改訂する判定state

### 1. 品質

```text
quality_gate_passed :=
  全runがvalidかつrateable
  ∧ required outcomeとrequired validationを満たす
  ∧ 許可外driftがない
  ∧ 事前固定したquality非劣性条件を満たす
```

Workerの有無は`quality_gate_passed`へ入れない。別execution identity自体がmodel-visibleなrequired outcomeであるcaseだけは、そのidentity resultの欠落を成果未達として扱う。

### 2. 比較可能性

```text
cost_gate_ready :=
  直接baseline resultが存在
  ∧ compatibility keyが一致
  ∧ candidate resultを見る前にtoken_toleranceとelapsed_toleranceを固定済み
```

`cost_gate_ready=false`なら、tokenとelapsedを記述しても`cost_controlled`または`cost_control_failed`を確定しない。結果確認後に許容幅を作らない。

許容幅は、baselineの独立反復で観測した変動範囲、または品質上の追加成果に対して事前承認したtask固有trade-offから固定する。Worker数やchild token比率から逆算しない。

既定値は`token_tolerance=0`、`elapsed_tolerance=0`とする。非zero toleranceを使う場合は、candidateを実行する前にbaseline独立反復から算出方法と値を固定する。値を固定できない場合は既定値を使い、candidate result確認後の緩和を禁止する。

### 3. コスト

```text
cost_controlled :=
  cost_gate_ready
  ∧ quality_gate_passed
  ∧ candidate token差がtoken_tolerance内
  ∧ candidate elapsed差がelapsed_tolerance内
```

主判定値はworkflow正本どおり各resultの中央値とする。candidate minus baselineのtoken差とelapsed差が両方tolerance内なら`cost_controlled`、片方だけ外なら`cost_tradeoff`、両方外なら`cost_control_failed`とする。品質非劣性を満たさない場合はcostではなく`quality_gate_failed`で停止する。

中央値だけで裾の悪化を隠さない。合計、iteration別またはpaired差、最大側の観測を併記する。`cost_tradeoff`は効率改善または採用可否へ自動変換せず、事前に固定したKPI優先順位がある場合だけ別の採用判断へ渡す。

### 4. route診断

次は`route_diagnostic`へ記録する。

- Worker起動数と起動率
- root / child token内訳
- Workerがrequired validationまたは別operationと重なった時間
- 同一operationの再割当て
- rootとWorkerによる同一predicateの再実行
- Worker resultが変更、rework、未発行invocation、または明示identity requirementへbindされたか
- `fork_turns`とallowed read

route診断は、KPI差の原因仮説と次のcase設計に使う。route診断だけで`cost_controlled`を反転させない。

## C83とC84の現在解釈

| 項目 | C83 F02 | C84 F02 |
| --- | ---: | ---: |
| score `4` | 5 / 5 | 5 / 5 |
| token中央値 | 407,217 | 291,841 |
| elapsed中央値 | 138.186秒 | 100.018秒 |
| Workerあり | 5 / 5 | 2 / 5 |
| child token / all-agent合計 | 503,695 / 22.74% | 69,042 / 4.67% |
| 再割当て | 1 run | 0 run |

C83とC84はprofileの`task_spec.source`が異なり、compatibility keyも一致しない。`291,841 - 407,217 = -115,376 tokens`、`100.018 - 138.186 = -38.168秒`は記述的な差であり、公式KPI比較ではない。

C84内ではroot-only 3件のtoken中央値が259,061、elapsed中央値が98.846秒、Workerあり2件が306,403、158.213秒だった。Workerありiteration 1はrequired validationと並行し100.018秒で完了した。iteration 5はWorker完了後にrequired validationへ進み216.409秒だった。Worker起動ではなく、並列化できた経路と逐次化した経路の混在が現在の未解決点である。

したがって現在stateは次のとおりとする。

| Candidate | 当時のimmutable評価state | 現在解釈 |
| --- | --- | --- |
| C83 | `targeted_f02_evaluated / stopped` | `quality_passed / cost_control_not_demonstrated` |
| C84 | `targeted_f02_evaluated / stopped` | `quality_passed / cost_control_mixed` |

両resultとも`cost_gate_ready=false`である。C83 / C84間の公式比較がなく、事前固定したtoken / elapsed許容幅もないためである。

## F02・F04・D01・A06の役割

- F02: root-onlyとWorker併用のどちらも許容する。品質とcross-layer validationを維持し、経路全体のtoken / elapsedを測る。
- F04: Workerによるfinal source checkを禁止しない。rootのNode validationと並行し、rootが同じfinal checkを再実行しない経路は正の候補である。
- D01: 別execution identityがmodel-visibleなrequired outcomeである場合だけ、そのidentity resultをroute conformanceとして要求する。`owner`語列から推定しない。
- A06: AI裁量によるWorker選択の正例とcontext分割を観測するdiagnosticとし、F02 / F04のWorker数を合わせるために使わない。

F02 / F04の新しい停止条件に「Workerが1件でも起動」を入れない。品質回帰、比較identity不一致、未固定tolerance、または3 KPIの事前gate不通過で停止する。

## 制御再設計

### TaskSpec境界

既存のF02 / F04 / D01 TaskSpecは変更しない。prompt変更と試験条件変更を同じ比較へ混ぜないためである。F02 / F04の`owner=independent ... check`は、既存入力のままproducerを指定しないmetadataとして解釈する。D01の「workerをproducerとする」という明示指定はhard constraintとして解釈する。

model-visibleなproducer関連入力は次の3種類へ分ける。

| 種類 | 例 | producer選択への効力 |
| --- | --- | --- |
| `producer_constraint` | userまたは適用authorityが別execution identityを必須・禁止にする | AIの選択を制約する |
| `producer_preference` | 「可能なら並列化」「Worker利用を優先」 | planning inputだがproducerを確定しない |
| `producer_metadata` | criterion owner、risk owner、role名、`independent`という作業名 | producer選択へ使わない |

`producer_constraint`は、実行identityの必須または禁止が明示されている場合だけ成立する。owner、risk、role、作業名、独立性を表す形容から推定しない。

将来、新しいcaseで別execution identityを成果成立条件にする場合は、ownerではなく次のような明示成果条件を使う。

```text
required_execution_identity = distinct_worker_identity
```

これは将来の評価set revisionにだけ適用する。C85の比較へは持ち込まない。

### Planning境界

次CandidateはC83 / C84の`delegation_value_ready`を継承しない。Workerの期待価値をpromptで列挙しない。

Worker起動はplanning後に追加する判断ではない。required outcomeをoperation graphへ分解し、各operationのproducerと実行waveを同じplan内で決める。

```text
execution_plan_ready :=
  required outcomeを覆うoperation集合が固定済み
  ∧ 各operationのscope / input / outputが固定済み
  ∧ operation間dependencyが固定済み
  ∧ result consumerが固定済み
  ∧ producer_constraintを適用済み
  ∧ 未制約operationのroot / Worker producerをAIが選択済み
  ∧ producer間でoperation scopeが重複しない
  ∧ ready operationをまとめるexecution waveが固定済み
```

`execution_plan_ready=false`の間はroot operation、Worker起動、artifact変更、required validationを開始しない。AIはplan作成中にscope重複、dependency、並列可能性、context局所性、required capability、result利用先からproducerを選ぶ。token、elapsed、問題発見確率の数値予測を要求しない。

`execution_plan_ready=true`になった後、最初のready waveでroot operationとWorker operationを同時に開始する。Worker resultが後続operationのdependencyであっても、ほかにreadyなroot operationがあれば先に進める。

```text
wait_ready :=
  未受領Worker resultが次operationのdependency
  ∧ ほかにreadyなroot operationがない
```

実行開始後に通常のproducer再選択を行わない。TaskSpec追加、result失効、capability unavailable、environment failureなどでplan前提が変わった場合だけ旧planとbindingを失効させ、再planningする。

### Prompt境界

prompt制御は次の不変条件へ縮約する。

1. `producer_metadata`はproducerを指定しない。
2. `producer_constraint`だけをhard constraintとして適用する。
3. 未制約operationのproducerはAIがexecution plan内で選ぶ。
4. 選択した一つのproducerへoperationをbindし、rootとWorkerへ同じoperationを重複割当てしない。
5. readyなroot / Worker operationはplanどおり同じwaveで開始し、`wait_ready=false`ならWorkerを待たない。
6. Worker resultを受け取ったrootは、result欠落または失効がない限り同じpredicateを再実行しない。
7. Workerを選んだ場合だけ、task identity、result provenance、必要最小contextを固定する。

これらはWorkerを禁止せず、Worker数、利用場面、期待価値の種類も固定しない。コストの妥当性は実行後の互換3 KPIで判定する。

## 次Candidate作成前gate

次Candidate bundleとprofileは、次を固定して作成する。

1. F02 r1、F04 r2、D01 r1の既存TaskSpec、fixture、oracleをそのまま使う。
2. 同じcomparison conditionsを使う直接baselineをC81とする。
3. token / elapsed toleranceはcandidate result確認前に既定値`0`へ固定する。
4. root-only、並行Worker、逐次Workerを区別できるroute diagnostic収集方法を固定する。
5. 既存TaskSpec文字列を変更せず、prompt側でconstraint、preference、metadataを分類する。
6. 一つのprompt変更軸。C81を直接親とし、producer選択を含む`execution_plan_ready`と既存producer / delegated-result境界を接続するplanning-first置換とする。

C85はF02、F04、D01の順に、各caseでC81 / C85を同じ固定入力へ適用する。F02のgate確定前にF04へ、F04のgate確定前にD01へ進めない。標準14、採用、release、本体反映は別判断とする。

## C85 / C86 / C87評価後の現在解釈

C85は単一operationでも完全な`execution_plan_ready`を維持し、F04でtoken中央値`+38.29%`、elapsed中央値`+24.70%`となった。C86は単一operationのroot fast pathを追加し、同じF04でtoken`+6.77%`、elapsed`-6.03%`のtradeoffまで戻した。

一方、D01ではC86も指定worker identityを5 / 5件で正しく起動したが、worker内部の独立readを個別custom exec callへ分割した。child custom exec call合計はC81 `13`、C86 `41`、child token合計は`340,228`、`873,848`だった。all-agent中央値はtoken`+83.28%`、elapsed`+45.81%`となり、C86を停止した。

したがって現在の未解決境界はWorker起動判断ではない。実行前にoperationとproducerを決めた後、bind済みproducer内部の非依存invocationを同一model stepへまとめる境界である。次の変更を検討する場合もF02 r1、F04 r2、D01 r1を変更せず、次を一つの軸として扱う。

1. operation planningとproducer内部のinvocation batchingを別状態にする。
2. root / workerのどちらでも、decision boundaryを持たない既知の非依存invocationを同一model stepへ発行する。
3. 単一operation fast pathを維持し、明示plan artifactを復活させない。
4. Worker起動数ではなく、互換な品質・all-agent token・elapsedで判定する。

C87はこの一軸を`DECISION_BOUNDARY`だけの置換として実装した。D01のchild custom exec call合計はC86の`41`から`12`へ減り、token中央値`-51.06%`、elapsed中央値`-26.54%`となった。したがってproducer-local invocation batchingの境界は実行trace上で狙った経路を作った。

当初の個別監査はv14 contract IDを採点関数へ渡さず、1件のnumeric location mismatchをv10規則でscore `3`にした。append-only訂正では5 / 5 score `4`である。保存済みC81比はtoken中央値`-10.29%`、elapsed中央値`+7.12%`で、両KPI悪化の停止条件に該当しない。訂正の根拠は[`rating contract binding訂正`](../evaluations/results/targeted-review-rating-contract-binding-correction_2026-07-29.md)に置く。

後続F02も5 / 5 score `4`で、C81比のtoken中央値`-5.26%`、elapsed中央値`-10.63%`だった。一方、token合計は`+16.06%`で分布はmixedである。数値とroute診断は[`F02 result`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f02-n5_2026-07-29.md)に置く。

F04も5 / 5 score `4`で、C81比のtoken中央値`+15.48%`、elapsed中央値`-12.62%`のtradeoffだった。両KPI悪化ではないため、D01 / F02 / F04のtargeted gateは通過した。現在状態は`targeted_d01_f02_f04_evaluated / targeted_gate_passed`である。数値とcommand evidence診断は[`F04 result`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f04-n5_2026-07-29.md)に置く。

別stateの標準14はC81 / C87とも70 / 70 score `4`だった。一方、C87の集約中央値はtoken`+6.09%`、elapsed`+1.35%`で、両方大きい。C81は70 / 70 root-only、C87は65 / 70 root-only、5 / 70で独立contract / source check Workerを使い、child token合計は`343,692`だった。標準14用の採否thresholdは事前固定していないため、品質通過と集約コスト悪化を分離する。正本は[`標準14 result`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md)に置く。

## C81・C87・C88・C89 F02保存traceのcontrol graph診断

2026-07-29に、既存F02 r1のC81、C87、C88、C89各`N=5`について、保存済みroot event、child rollout、all-agent usageをread-onlyで再確認した。一次result、score、candidate stateは変更していない。

| 条件 | Workerあり | child token合計 | 保存trace上のoperation解釈 |
| --- | ---: | ---: | --- |
| C81 | 0 / 5 | `0` | implementation、test-contract、required validationを一つのroot operationへbind |
| C87 | 3 / 5 | `170,964` | implementationをroot、F02-C3 test-contract確認を別Workerへ分離 |
| C88 | 4 / 5 | `366,081` | C87と同じ分離。2件はroot validationと同時進行、2件はWorker完了後にvalidation開始 |
| C89 | 4 / 5 | `283,335` | C87と同じ分離。4件ともWorkerがroot validationより先行 |

C87からC89までのWorker 11件は、すべて`/root/independent_contract_check`だった。Workerはscoped diffと選定済みtestを読み、date-bound assertionの削除、緩和、skip、xfailがないというF02-C3のPASSを返した。artifact変更、required validation、Worker固有capabilityによる成果生成は行っていない。11件のchild token合計は`820,380`である。

同じ11件でrootはsource変更、scoped diffまたはtest確認、focused gate、full gateを担当し、最終応答でもF02-C3を自ら成立と判定した。Worker resultのconsumerはrootの最終done判定だけであり、別artifact、rework、未発行invocationのtarget、permission、method、stop conditionへbindされなかった。

したがって誤経路は、正しく分解済みの二つのoperationを誤った順序でdispatchしたものではない。`non_machine_risk=test-contract, owner=independent contract check`というcriterion metadataを、独立したoperation identityへ昇格した時点で、rootとWorkerへ同じF02-C3 predicateを重複bindしたものである。C88のsame-wave条件とC89のdispatch-time条件は、この上流の誤分解を保持したまま発行順だけを制御したため、重複operationを除けなかった。

保存traceにはC87の3件とC88の2件で、Workerとroot validationが同時進行した経路がある。したがって、現時点では「executorがroot / Workerを同じwaveへ発行できない」というcapability欠落は確認できない。新しいexecutorまたはscheduler制御の根拠にも使わない。

今後operation graphを再開する場合は、producer選択より前に次を満たす必要がある。

```text
operation_identity_ready :=
  TaskSpecが要求するdistinct terminal resultがある
  ∧ そのresultのconsumerまたはtask terminal条件が固定済み
  ∧ criterion / validation / risk / owner / roleというmetadataだけから別operationを作っていない
  ∧ rootまたは別producerの既存operationとpredicateが重複しない
```

criterion、required validation、non-machine riskは、TaskSpecが別resultまたは別execution identityをrequired outcomeとして明示しない限り、対象成果を作る既存operationへbindする。`operation_identity_ready=true`のoperation集合を固定した後だけproducerとwaveを選ぶ。

ただしC81 F02は5 / 5 root-onlyでこの最短経路を既に成立させている。C81の保存traceにoperation誤分解は観測されていないため、この診断だけを根拠にC81直接childの新Candidate、bundle、profile、model runを作成しない。fresh C81互換traceで同じ誤分解を再観測するか、別operation identityを必要とする新しい明示要件が追加された場合だけ、`operation_identity_ready`一軸の作成前gateへ戻る。

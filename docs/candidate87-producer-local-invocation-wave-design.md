# Candidate87 producer-local invocation wave設計

## 結論

Candidate87はCandidate86を直接親とし、producer選択、単一operation fast path、Worker起動条件を変更しない。変更軸は、bind済みproducer内部でdecision boundaryを持たない非依存invocationを同一model stepへまとめる境界だけである。

F02 r1、F04 r2、D01 r1の既存Evaluation set、TaskSpec、fixture、oracle、allowed path、required validation、明示producer identityは変更しない。既存setをそのまま再利用し、pair内ではprompt identity以外を一致させる。

## 作成前gate

1. 基準prompt setは`the-caption-3ce91a4-producer-plan-fast-path-r1`である。
2. 基準の最短正常経路は、実行前にoperationへproducerをbindし、bind済みproducerが非依存invocationを同一model stepから発行し、全result受領後に一度だけ次を判断する経路である。
3. 保存済みC86 D01 traceではC81 / C86とも5 / 5件がscore `4`で、指定worker `/root/monthly_format_review_producer`のterminal resultを返した。
4. C86 D01のchild custom exec call合計はC81の`13`から`41`へ増え、child token合計は`340,228`から`873,848`へ増えた。C86のtoken中央値は`+83.28%`、elapsed中央値は`+45.81%`だった。
5. C86 childは、同一review operation内の開始identity確認、固定diff read、source read、zero-drift確認を個別custom exec callへ分割した。C81 childは複数の非依存readを一つのcustom exec wrapperから発行した。
6. Worker起動判断とproducer identityは正しかった。誤経路はproducer選択後のinvocation発行単位である。
7. C86の`DECISION_BOUNDARY`は非依存invocationを同一model stepへ置くが、producerがworkerの場合、同一operation内の「個別command」を別operationまたは別model stepへ読み替えない優先関係が不足している。
8. 置換する一つのpredicateは`DECISION_BOUNDARY`のproducer-local invocation waveである。他のlabelは変更しない。
9. 新たに増える判断点は、invocation間にtarget / permission / method / stop conditionを変えるdecision boundary、明示order、fail-stop dependencyがあるかだけである。
10. 数値token / elapsed予測、Worker価値分類、Worker起動数制限、明示plan artifactは追加しない。

## Prompt変更

Candidate86の`DECISION_BOUNDARY`だけを置換する。

- root / workerを問わず、同一operation内のinvocationを別operationへ読み替えない。
- 「個別」「1 commandずつ」はinvocation identityとresultを分ける意味であり、別model stepへ分ける意味ではない。
- decision boundary、明示order、fail-stop dependencyがない既知の非依存invocationは、一つのcustom exec wrapperから個別invocationとして同時発行する。
- 全resultを一度だけmodelへ返し、その後に一度だけ次を判断する。
- required validationの明示orderとfail-stopは既存`VALIDATION_CLOSURE`を優先する。

`SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、`VALIDATION_CLOSURE`、`METHOD`、`RECOVERY`は変更しない。

## 評価順

1. C86 / C87へ既存D01 r1を適用し、rating v14、Medium、各`N=5`
2. 5 / 5 score `4`、指定worker route 5 / 5を維持し、C87 minus C86のtoken / elapsed中央値がともに`0`以下なら一軸qualificationを通過する
3. qualification通過時は保存済みC81 D01 resultとC87を互換比較する。両KPIがC81より悪化した場合は停止する
4. D01 gate通過時だけ既存F02 r1、次に既存F04 r2をC81 / C87で評価する

C81とC86の保存済みresultを変更しない。C87 profileは対応C86 profileからprofile IDとprompt identityだけを替える。新しいcase、fixture、oracle、Evaluation setは作成しない。

## 状態境界

bundleとprofileの作成は`draft / not_evaluated`から開始した。targeted評価、標準14、採用、release、THE-CAPTION本体反映は別stateとする。

## 評価結果

既存D01 r1を変更せず、C86 / C87、Rating v14、Medium、各`N=5`で実行した。[`result`](../evaluations/results/candidate86-candidate87-producer-local-invocation-wave-v14-medium-d01-n5_2026-07-29.md)ではC87のchild custom exec call合計がC86の`41`から`12`へ減り、token中央値は`-51.06%`、elapsed中央値は`-26.54%`だった。指定worker routeも5 / 5件で成立した。

当初の個別監査はv14 contract IDを採点関数へ渡さず、1件のnumeric location mismatchをv10規則でscore `3`にした。append-onlyの[`訂正result`](../evaluations/results/targeted-review-rating-contract-binding-correction_2026-07-29.md)は5 / 5 score `4`である。保存済みC81との比較も両KPI悪化ではなく、D01 qualificationを通過した。

後続の[`F02 result`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f02-n5_2026-07-29.md)も5 / 5 score `4`だった。C81比の中央値はtoken`-5.26%`、elapsed`-10.63%`である。token合計は`+16.06%`で分布が混在するため、一般的な効率改善は主張しない。

続く[`F04 result`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f04-n5_2026-07-29.md)も5 / 5 score `4`だった。C81比の中央値はtoken`+15.48%`、elapsed`-12.62%`のtradeoffで、両KPI悪化の停止条件には該当しない。D01 / F02 / F04のtargeted gateを通過した。

別stateの[`標準14 result`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md)は、互換なC81 / C87 v14を新規実行し、両条件70 / 70 score `4`だった。C87比の集約中央値はtoken`+6.09%`、elapsed`+1.35%`である。標準14の採否thresholdは事前固定していないため、品質通過と集約コスト悪化を分離し、現在状態を`standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`とする。release、本体反映も未実施・未判断である。

## 後続の採用判断

上記の一次評価状態は変更しない。2026-07-29の別stateの[`採用判断`](candidate87-adoption-decision.md)で、Candidate87を`not_adopted / stopped`とした。releaseは作成せず、runtime projectionも承認しない。現在の採用・投影済み基準はCandidate81のままである。

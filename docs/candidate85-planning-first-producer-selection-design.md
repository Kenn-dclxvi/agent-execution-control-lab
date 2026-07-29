# Candidate85 planning-first producer selection設計

## 結論

Candidate85はCandidate81を直接親とし、Workerを使うかどうかを実行開始後の追加判断ではなく、operation分解と同時にAIが決める。F02 r1、F04 r2、D01 r1の試験内容は変更しない。

変更軸はplanning-first producer selectionだけである。Worker起動数は停止条件にせず、品質、all-agent token、elapsedの互換比較でコストを判定する。

## 作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-wrapper-precedence-r1`である。
2. 基準の最短正常経路は、TaskSpecをoperationへ分け、各operationのproducerをbindし、readyなinvocationを発行し、required validation後にterminalを一度判断する経路である。
3. 保存済みC84 F02 traceでは、iteration 1のWorker併用経路はrequired validationと重なって`100.018`秒、iteration 5の逐次経路は`216.409`秒だった。C83には同一operationの再割当ても1件あった。
4. TaskSpecとrepository authorityだけではproducer選択の時点、scope非重複、wave、待機条件を固定できない。C83 / C84の期待価値列挙は実行開始前のoperation planningへ接続されていなかった。
5. 追加する一つの変更軸は`execution_plan_ready`である。これに合わせて`PRODUCER`、`OWNER_ROLE`、`DECISION_BOUNDARY`をplanning結果へ接続する。
6. この変更は、owner語列によるproducer選択、同一scopeの重複割当て、readyなroot operationを残した待機、通常経路での後付け再割当てを除く。
7. 新たに増える判断点は、operationのscope / input / output / dependency / consumer、producer選択、execution waveである。数値のtoken / elapsed予測やWorker価値分類は増やさない。
8. F02 r1とF04 r2で成果品質を維持し、C81とのall-agent token / elapsedを比較する。D01 r1で既存の明示worker指定を維持する。routeは品質とは別のdiagnosticとして記録する。
9. score `4`未満、invalid / unrateable、許可外drift、identity不一致で停止する。品質通過後、token差とelapsed差が事前固定した許容幅`0`を両方超えれば`cost_control_failed`、片方だけなら`cost_tradeoff`とする。Worker起動だけでは停止しない。

## Prompt変更

Candidate81から次だけを変更する。

- `PLAN`を追加し、execution開始前にoperation graph、producer、waveを固定する。
- `PRODUCER`をplanで選択したproducerのbindingへ接続する。
- `OWNER_ROLE`からowner語列と独立性語列による選択分岐を除き、選択済みWorkerのidentity / result provenanceだけを扱う。
- `DECISION_BOUNDARY`へready waveと`wait_ready`を接続する。

`SPEC`、`TERMINAL`、`CONTEXT`、`ROOT`、`INDEPENDENCE`、`VALIDATION_CLOSURE`、`METHOD`、`RECOVERY`は変更しない。

## 評価順

1. C81 / C85 F02 r1、rating v14、Medium、各`N=5`
2. F02 gate通過時だけC81 / C85 F04 r2、同条件で各`N=5`
3. F04 gate通過時だけC81 / C85 D01 r1、同条件で各`N=5`

各pairはprompt identity以外のcomparison conditionsを一致させる。Candidate83 / Candidate84のresultは設計根拠に使うが、C81 / C85の公式KPI comparisonへ混ぜない。

## 状態境界

bundleとprofileの作成は`draft / not_evaluated`である。targeted評価、標準14、採用、release、THE-CAPTION本体反映は別stateとする。

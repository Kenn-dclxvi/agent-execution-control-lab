# Candidate89 dispatch-time Worker admission設計

## 結論

Candidate89はCandidate87を直接親とし、Candidate88を継承しない。変更軸は`DECISION_BOUNDARY`に追加するdispatch時のAI裁量Worker起動gateだけである。

AI裁量Workerは、非重複かつ相互非依存のroot operationが実際にdispatch済みで、そのterminal resultがまだ返っていない状態でだけ起動できる。同じready waveへ置けるという計画や、Worker起動後にroot作業を探すことは起動根拠にしない。

TaskSpecが別execution identityのresultをrequired outcomeとして明示する場合はproducer constraintである。この明示必須経路はdispatch gateの対象外とし、D01 r1で確認する。

## 作成前gate

1. 基準prompt setは`the-caption-3ce91a4-producer-local-invocation-wave-r1`である。
2. 基準状態の最短正常経路は、単一operationをrootが直接完了し、producer内部の非依存invocationを同一model stepへまとめる経路である。
3. 保存済みCandidate88 F02 traceでは5 / 5件がscore `4`だったが、AI裁量Worker 4件中2件はWorker完了後にrequired validationを開始した。
4. Candidate88は`PRODUCER`で同じready waveに開始可能と判断させたが、Worker起動時にroot operationが実行中であることを要求しなかった。そのため、計画上の並列性が実行上の並列性へ接続されなかった。
5. 置換する一つのpredicateは`DECISION_BOUNDARY`の`root_parallel_inflight`である。
6. `root_parallel_inflight := 非重複かつ相互非依存なroot operationのinvocationを先に発行済み ∧ そのterminal resultが未受領 ∧ Worker result consumerが固定済み`とする。
7. このpredicateは「同時開始できるはず」という予測と、Worker起動後に並行作業を探す判断点を消す。
8. 新たに増える判断点は、root invocationの発行済み状態、terminal resultの未受領状態、scope / dependency、Worker result consumerである。token、elapsed、完了時刻は予測しない。
9. 品質維持は既存F02 r1、F04 r2、D01 r1をRating v14、Medium、各`N=5`で確認する。Evaluation set、TaskSpec、fixture、oracle、allowed path、required validationは変更しない。
10. AI裁量Workerが`root_parallel_inflight=false`で1件でも起動した場合、score `4`未満が1件でもある場合、またはcase単位のtoken中央値とelapsed中央値がCandidate81比でともに増えた場合は停止する。

## Prompt変更

Candidate87の`DECISION_BOUNDARY`だけを置換する。

- AI裁量Workerのproducer bindingと起動に`root_parallel_inflight`を追加適用する。
- 非重複・相互非依存のroot operationを先にdispatchする。
- root operationが実行中であることを観測したscheduler decisionでだけAI裁量Workerを起動する。
- 計画上のsame-wave、起動後に見つけたroot作業、Worker resultへ依存するroot operationは代用しない。
- root operationが先にterminalになった場合はAI裁量Workerを起動せず、候補operationをrootへbindする。
- TaskSpecが明示する別execution identity resultはproducer constraintとして従来どおり起動する。

`SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、`VALIDATION_CLOSURE`、`METHOD`、`RECOVERY`は変更しない。Candidate87のproducer-local invocation batchingも保持する。

## 評価順

1. 既存F02 r1をCandidate81 / Candidate89、Rating v14、Medium、各`N=5`で実行する。
2. 5 / 5 score `4`を要求する。AI裁量Workerが起動したrunでは、起動前に別scopeのroot invocationが発行済みでterminal result未受領だったことを保存traceで確認する。
3. AI裁量Workerが0件でもroute failureにしない。`root_parallel_inflight=false`での起動が1件でもあれば停止する。
4. qualityとroute通過後、Candidate89 minus Candidate81のtoken中央値とelapsed中央値がともに`0`を超えた場合は停止する。
5. F02通過時だけ既存F04 r2を同条件で実行し、同じgateを適用する。
6. F02 / F04通過時だけ既存D01 r1で明示必須Workerを5 / 5維持できることを確認する。
7. targeted gate通過時だけ既存標準14 r1をCandidate81 / Candidate89、Rating v14、Medium、各`N=5`で実行する。70 / 70 score `4`、token・elapsed集約中央値がともにCandidate81以下であることを採否gateとする。

新しいcase、fixture、oracle、Evaluation setは作成しない。既存Candidate81、Candidate87、Candidate88のbundle、profile、resultは変更しない。

## 状態境界

Candidate89 bundleと評価profileは`draft / not_evaluated`から開始する。targeted評価、標準14、採用、release、THE-CAPTION本体反映は別stateであり、未実施・未判断とする。

## 評価結果

既存F02 r1を変更せず、Candidate81 / Candidate89、Rating v14、Medium、各`N=5`で実行した。[`result`](../evaluations/results/candidate81-candidate89-dispatch-time-worker-admission-v14-medium-f02-n5_2026-07-29.md)は両条件5 / 5 score `4`だった。

Candidate89はAI裁量Workerを4 / 5件で起動した。保存raw traceでは4件すべてでWorker起動がroot required-validation invocationより`9.276〜16.549`秒先であり、起動時の`root_parallel_inflight`は`false`だった。promptへdispatch状態を記述しただけでは、schedulerの実際の発行順を制約できなかった。

C81比の中央値もtoken`+6.45%`、elapsed`+4.14%`で両方悪化した。事前停止条件に従い、現在状態を`targeted_f02_evaluated / stopped`とする。F04、D01、標準14、採用、release、THE-CAPTION本体反映へ進めない。

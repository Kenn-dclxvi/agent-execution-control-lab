# Candidate88 parallel Worker admission設計

## 結論

Candidate88はCandidate87を直接親とし、AI裁量のWorkerを、非重複・非依存のroot operationと同じready waveで開始できる場合だけ許可する。Worker resultがroot operationの開始条件である逐次確認や、Workerを起動してからrootが実行可能なoperationを探す経路は許可しない。

TaskSpecが別execution identityのresultをrequired outcomeとして明示する場合は、AI裁量のWorker選択ではなくproducer constraintである。この明示必須経路はD01 r1を成立させるため保持し、parallel admissionの対象外とする。

## 作成前gate

1. 基準prompt setは`the-caption-3ce91a4-producer-local-invocation-wave-r1`である。
2. 基準の最短正常経路は、単一operationをrootが直接完了し、複数の非重複・非依存operationがある場合だけready waveとして同時開始する経路である。
3. 保存済みCandidate87標準14 traceではC81 / C87とも70 / 70 score `4`だったが、C87はF02で3件、F04で2件のWorkerを起動した。
4. Workerあり5 runはC81の対応runよりtoken合計`+692,281`、elapsed合計`+173.289`秒だった。内訳はchild token`343,692`、同じ5 runのroot token増加`348,589`である。
5. 5件中3件は、artifact変更後にWorkerを起動し、Worker完了を待ってからrequired validationを開始した。rootとWorkerの非依存operationを同じwaveへ置かなかったため、独立確認がcritical pathへ追加された。
6. Candidate87の`DECISION_BOUNDARY`はreadyなroot operationがあれば待たないと定めるが、Worker選択時点で並行するroot operationのidentity、非依存性、同時開始をadmission条件へ固定していない。
7. 置換する一つのpredicateは`PRODUCER`のAI裁量Worker admissionである。`parallel_worker_ready := Worker operationとroot operationが非重複 ∧ 相互非依存 ∧ 同じready waveで同時開始可能 ∧ Worker result consumerが固定済み`とする。
8. `parallel_worker_ready=true`の場合だけAI裁量でWorkerへbindする。falseならrootへbindする。Worker固有capability、owner / role語列、Worker利用の指示、独立確認という名称だけではこの状態を成立させない。
9. 新たに増える判断点は、Worker候補operationと同時開始するroot operationのidentity、scope重複、dependency、result consumerだけである。token、elapsed、完了時刻を事前予測しない。
10. TaskSpecが別execution identityのresultを明示的に要求する場合は、指定identityをproducerへbindする。これはAI裁量admissionではない。

## Prompt変更

Candidate87の`PRODUCER`だけを置換する。

- 単一operationはrootへ直接bindする。
- AI裁量のWorkerは`parallel_worker_ready=true`の場合だけ選択する。
- root operationとWorker operationを同じready waveから開始する。
- Worker resultに依存するroot operationを、並行作業があるように数えない。
- Worker起動後に並行可能性を探さない。
- TaskSpecが別execution identityのresultをrequired outcomeとして明示した場合は、そのproducer constraintを優先する。

`SPEC`、`TERMINAL`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`METHOD`、`RECOVERY`は変更しない。

## 評価順

1. 既存F02 r1とF04 r2をCandidate81 / Candidate88、Rating v14、Medium、各`N=5`で実行する。
2. 10 / 10 score `4`を要求する。AI裁量Workerが起動したrunでは、非重複・非依存のroot operationが同じwaveから開始され、readyなroot operationを残した待機が0件であることを保存traceで確認する。
3. Workerが0件でもroute failureにしない。逐次Workerが1件でもあれば停止する。
4. quality通過後、Candidate88 minus Candidate81のtoken中央値とelapsed中央値が両方`0`を超えたcaseがあれば停止する。
5. F02 / F04 gate通過時だけ、既存D01 r1で明示必須Workerを5 / 5維持できることを確認する。
6. targeted gate通過時だけ、既存標準14 r1をCandidate81 / Candidate88、Rating v14、Medium、各`N=5`で実行する。70 / 70 score `4`、token・elapsed集約中央値がともにCandidate81以下であることを採否gateとする。

既存Evaluation set、TaskSpec、fixture、oracle、allowed path、required validation、rating contractは変更しない。新しいcase、fixture、oracle、Evaluation setは作成しない。

## 状態境界

Candidate88 bundleは`draft / not_evaluated`から開始する。targeted評価、標準14、採用、release、THE-CAPTION本体反映は別stateであり、未実施・未判断とする。

## 評価結果

既存F02 r1を変更せず、Candidate81 / Candidate88、Rating v14、Medium、各`N=5`で実行した。[`result`](../evaluations/results/candidate81-candidate88-parallel-worker-admission-v14-medium-f02-n5_2026-07-29.md)は両条件5 / 5 score `4`だった。

Candidate88はWorkerを4 / 5件で起動し、2件はrequired validationと同じwaveから開始した。一方、残る2件はWorker完了後にrequired validationを開始した。事前停止条件の逐次Worker 1件以上に該当する。C81比の中央値もtoken`+26.28%`、elapsed`+8.03%`で両方悪化した。

現在状態を`targeted_f02_evaluated / stopped`とする。F04、D01、標準14、採用、release、THE-CAPTION本体反映へ進めない。

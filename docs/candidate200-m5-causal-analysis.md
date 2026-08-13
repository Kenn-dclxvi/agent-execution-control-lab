# Candidate200 M5原因分析

## 結論

Candidate200の機構不通過17件は、すべてreview入力の取得責任が有限集合として分割されていなかった一原因へbindできる。原因不明は0件である。Candidate200を親にせず、Candidate147を直接基盤としてM2を再開する。

## 一次結果

- 登録result: `2c099aff32054c8288070e59a52464e0`
- 品質: Score `4 / 1 = 30 / 15`
- 機構不通過: 17 / 45
- required reviewer欠落: 14 / 30
- 起動済みreviewerの期待result kind不一致: 3 / 16
- 起動済みreviewerのexact read set: 16 / 16
- closed source read / mixed read / root先読み / canary配送: すべて0

## 原因

Candidate200は、packet projectionの入力sourceをreviewerから閉じ、reviewer自身が読むexact targetを別集合へ固定した。しかし、review criterionを閉じる全観測を、次の二集合へ重複なく全件割り当てるpredicateを持たなかった。

1. rootが許可済みsourceから取得し、値とprovenanceをpacketへ投影する観測
2. reviewerがexact targetから直接取得する観測

そのため、`design-admission.json`内のsemantic、authority、normative contractだけを投影し、consumer inventoryやconsumer contractを投影しない経路と、rootによる取得をreviewer-owned観測の先読みと解釈してreviewer自体を起動しない経路が残った。

## 17件の分類

| 分類 | 件数 | case | 観測 |
|---|---:|---|---|
| reviewer未起動 | 14 | ADR03=3、ADR04=2、ADR05=3、ADR06=2、ADR07=2、ADR09=2 | projectionとdirect observationを安全に分離不能として`unavailable`へ停止 |
| packet投影不足 | 3 | ADR03=1、ADR04=1、ADR05=1 | reviewerは起動したがinventoryまたはconsumer contractが不足し、closed sourceを再読できず`unavailable` |

両分類は、必要観測の所有割当てが全件固定されていれば発行前に検出できる同一原因である。closed source readを再許可する修正は、Candidate199の直接失敗形を戻すため採らない。

## 次設計へ渡す制約

- `required_review_input_manifest`へ、criterion判定に必要な全観測identity、target、success condition、consumer predicateを固定する。
- 各entryを`root_projection`または`reviewer_observation`のちょうど一方へ割り当てる。
- `root_projection`は取得済みvalueとprovenanceをpacketへ全件投影する。
- `reviewer_observation`はexact read setとし、rootによる先読みとpacket代入を禁止する。
- 二集合の重複、未割当て、consumer不明、forbidden input混入が一件でもあればreviewerを起動せず、変更も発行しない。
- reviewerからのprojected source閉鎖、mixed read禁止、forbidden canary非配送は維持する。

`candidate200_failure_causes_17_classified / reviewer_missing_14 / packet_underprojection_3 / unknown_cause_0 / M2_reopen_ready_on_c147 / candidate200_not_parent`

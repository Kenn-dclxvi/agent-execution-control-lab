# held-out Workflow Free / Opus関係レビュー役比較

## 測定範囲

`pr-review-held-out-three-r1 / r1`のPRR-C02/r2、PRR-C03/r2、PRR-C06/r2を比較した。Control-Freeは保存済みresultを再利用し、関係レビュー役1人・Opus固定の3件だけを新規実行した。3件とも要求model、構造化出力、Opus reviewer 1人、all-agent token、経過時間、fixture access、権限拒否0件を確認し、測定が成立した。

## KPI

| case | Control-Free quality | Opus quality | Control-Free tokens | Opus tokens | Control-Free elapsed | Opus elapsed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PRR-C02/r2 | 1 | 0 | 2,313,350 | 989,441 | 278.730秒 | 300.931秒 |
| PRR-C03/r2 | 4 | 4 | 4,192,816 | 418,414 | 266.190秒 | 143.202秒 |
| PRR-C06/r2 | 4 | 4 | 1,659,245 | 657,515 | 344.698秒 | 317.662秒 |
| 3ケース合計 | - | - | 8,165,411 | 2,065,370 | 889.618秒 | 761.795秒 |

Opus条件のall-agent token合計はControl-Freeより74.7%少なく、elapsed合計は14.4%短かった。ケース別では、tokenがPRR-C02で57.2%、PRR-C03で90.0%、PRR-C06で60.4%少なかった。elapsedはPRR-C02で8.0%長く、PRR-C03で46.2%、PRR-C06で7.8%短かった。

品質はPRR-C03とclean controlのPRR-C06で両条件ともscore `4`だった。PRR-C02はControl-Freeがscore `1`、Opus条件がscore `0`である。Opus条件は期待findingを1件見逃し、false positive 3件、review contract violation 2件を記録した。この低い値も有効な品質KPIであり、再実行やcase変更で補正しない。

## 境界

この3ケース各1回の結果から、別caseや一般的なモデル優劣へ一般化しない。評価基盤は3 KPIを保存するだけで、winner、KPIの優先順位、採用、release、本体反映を決めない。一次resultとcontent SHA-256は[`results admission`](../contracts/pr-review-held-out-opus-comparison-results-admission-r1.json)を正本とする。

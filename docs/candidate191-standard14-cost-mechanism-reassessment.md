# Candidate191 Standard14コスト機序再判定

> **結果**: `quality_passed / mechanism_failed_reassessed / M9_not_ready / no_new_run`

## 結論

Candidate191のStandard14は70 / 70 Score 4を維持するが、C147が成立させた変更前共同発行を9 / 14ケースで退行させている。C147比の総token差`+2,197,612`のうち`1,906,243`、`86.74%`が、この9ケースに集中した。したがってM7の品質通過は維持する一方、機序通過を撤回し、M9へ進めない。

新しい評価runは発行していない。C147とCandidate191の同一compatibility keyを持つ登録result、および保存済み生traceだけを再集計した。

## ケース別token中央値

| case | C147 | Candidate191 | 差 | 変更前step C147 → C191 |
|---|---:|---:|---:|---:|
| A01 | 19,195 | 41,095 | `+114.09%` | `0 → 1` |
| A02 | 129,085 | 186,555 | `+44.52%` | `1 → 2` |
| F01 | 107,202 | 194,049 | `+81.01%` | `1 → 2` |
| F02 | 128,236 | 272,478 | `+112.48%` | `1 → 2` |
| F03 | 104,320 | 160,492 | `+53.85%` | `1 → 2` |
| F04 | 151,170 | 150,344 | `-0.55%` | `2 → 2` |
| F05 clarify | 37,242 | 40,260 | `+8.10%` | `1 → 1` |
| F05 out-of-scope | 37,366 | 42,075 | `+12.60%` | `1 → 1` |
| F06 | 151,542 | 155,616 | `+2.69%` | `2 → 2` |
| F07 canonical | 102,504 | 129,068 | `+25.92%` | `1 → 2` |
| F07 dependency | 87,284 | 111,203 | `+27.40%` | `1 → 2` |
| F08 | 113,067 | 126,193 | `+11.61%` | `1 → 2` |
| F10 inventory | 87,934 | 115,611 | `+31.47%` | `3 → 4` |
| F10 monthly | 93,096 | 106,351 | `+14.24%` | `3 → 3` |

## 原因

C147は、開始identity resultが許可済みreadのtargetまたはpermissionを変えない場合、identity確認とreadを同じmodel stepから発行した。Candidate191では、外側admission、観測、変更を別operationへ分けた後、「まずidentityだけを確認し、結果受領後にreadする」という順序へ戻った。

増加した9ケースは、C147の変更前step削減が成立していた同じ9ケースである。Candidate191では対象45 run中44件で一step増えた。A01は特に明確で、値未固定なので直接質問できるにもかかわらず、5件中4件で利用先のない開始identity commandを発行した。commandなしの1件は20,375 tokensでC147中央値19,195に近く、commandあり4件は38,559〜41,213 tokensだった。

両候補の生traceが残る各55 runでは、input tokenが`+25.47%`、cached inputが`+25.77%`なのに対し、outputは`+2.22%`、reasoning outputは`+4.04%`だった。増加の中心は長い回答や推論ではなく、追加model stepによるcontext再投入である。

不足している制御は、既知の相互非依存invocationをoperation分離より優先して共同発行することと、結果consumerのない開始観測を禁止することである。これはreview責務を削る最適化ではない。Candidate190で失敗した`OWNER_ROLE`削除を再実施してはならない。

## 現在判断

- Standard14品質: `passed`
- Standard14機序: `failed_reassessed`
- M8: 測定完了後に因果分析へ再入
- M9: `not_ready`
- Candidate191変更: 未実施
- 新規評価run: 0件
- 次の実装: 新しいCandidate identityと、共同発行・consumerなし観測禁止の一変更軸が必要

## 一次証拠

- [構造化再判定](../evaluations/results/candidate191-standard14-cost-mechanism-reassessment-r1.json)
- [Candidate191 Standard14登録result](../evaluations/results/da6ada84ac07426d8c66dddddcb08fdc.json)
- [C147 Standard14 N=5結果](../evaluations/results/candidate125-candidate145-candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)

# held-out Control-Free品質確認

## 結論

独立監査済みの3ケースは、いずれも要求model、構造化出力、all-agent token、経過時間、fixture access、権限拒否0件を確認でき、測定として成立した。品質はPRR-C03/r2とPRR-C06/r2がscore `4`、PRR-C02/r2がscore `1`だった。このため、3ケースすべてでscore `4`を要求するControl-Free品質条件は成立していない。Claude Code純正相当CoreとOpus関係レビュー役の比較は開始しない。

PRR-C02では、reviewerは`instance_artifact_separation`違反を正しいcategory、severity、`members.json`の1行目で指摘した。しかし、同じ違反を成立させるREADMEを`related_paths`へ含めなかった。期待する2 pathの集合と一致しないため、required findingはfalse negative 1件となり、返した単一path findingはfalse positive 1件となった。

独立case設計監査では、この2 path関係をmodel-visible入力から導出でき、どちらのpathもanchorにできることを確認している。実行時にも規則とsnapshotへ到達しているため、環境不成立やoracleだけが要求する条件ではない。今回の結果は、Control-Freeが複数pathの関係を出力identityへ完全に結び付けられなかった観測である。同じcase revisionを結果に合わせて変更したり、品質失敗を理由に同じスロットを再実行したりしない。

## 3 KPI

| case | GitHub run | 測定 | quality score | all-agent tokens | elapsed |
| --- | --- | --- | ---: | ---: | ---: |
| PRR-C02/r2 | [31290559295](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31290559295) | satisfied | 1 | 2,313,350 | 278.730秒 |
| PRR-C03/r2 | [31290559229](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31290559229) | satisfied | 4 | 4,192,816 | 266.190秒 |
| PRR-C06/r2 | [31290559290](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31290559290) | satisfied | 4 | 1,659,245 | 344.698秒 |

3件ともrootだけでレビューし、subagentは使用しなかった。fixture toolの呼出しは順に`8 / 24 / 9`回だった。これらは実行経路の診断値であり、正式KPIには含めない。

## 一次result

- [PRR-C02/r2](pr-review-held-out-control-free-qualification-r1-prr-c02-held-out-control-free-r1-a31290559295.json)、SHA-256 `0b037704641bdb9bd6ee04fd567a112ef9f2ad30af530dcee68aa959e9a6bdf4`
- [PRR-C03/r2](pr-review-held-out-control-free-qualification-r1-prr-c03-held-out-control-free-r1-a31290559229.json)、SHA-256 `b480091ca7f95b8d9578494c782ac24b4fe666766d3741ef7240ad9ad4d363b9`
- [PRR-C06/r2](pr-review-held-out-control-free-qualification-r1-prr-c06-held-out-control-free-r1-a31290559290.json)、SHA-256 `dc794bbc22f411ee0da769c7efa0df95c051d8e2eb3a8eb44106434847aadafd`

## 次の判断

現行の品質不変条件を維持するなら、この未使用setでの本番比較は終了する。次のreview体制は別のdevelopment caseで作り、資格確認後に新しい未使用setを固定する必要がある。品質を不変条件ではなく比較結果として扱う場合は、新インスタンスのゲートと比較仕様そのものを別の変更として見直す必要がある。

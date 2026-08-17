# Candidate269 natural-language validation carrier closure F01・F02・F03・F10 entrypoint N=20

## 結論

Candidate269の四ケースを各N=5からN=20へ拡張した。既存20 runを再利用し、不足する各ケース15件、合計60件だけを三つの容量管理batchで発行した。追加60 / 60件はvalidかつScore `4`、excluded attemptは0件で、累積80 / 80件もScore `4`だった。

追加NはC269を採用候補へ戻すためではなく、N=5で中央値を動かした上振れrouteの頻度を確かめるために行った。C147の保存済みN=20と比べると、四ケース合算のtoken中央値は`+11.15%`、経過時間中央値は`+2.77%`で、品質は同値だった。N=5のtoken差`+15.07%`は縮んだが、同費用水準には達していない。

## KPI

| ケース | C147 token中央値 | C269 token中央値 | token差 | C147秒中央値 | C269秒中央値 | 秒差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 | 107,010.5 | 118,667.5 | `+10.89%` | 62.107 | 71.961 | `+15.87%` |
| F02 | 134,960 | 167,606 | `+24.19%` | 79.763 | 85.063 | `+6.64%` |
| F03 | 98,746 | 109,342.5 | `+10.73%` | 70.780 | 74.002 | `+4.55%` |
| F10 | 102,345 | 113,794 | `+11.19%` | 66.849 | 71.571 | `+7.06%` |

同じiterationの四ケース合算中央値は、C147 478,811.5 tokenに対してC269 532,210 token、経過時間は289.963秒に対して297.983秒だった。

## 上振れroute

| ケース | 待機 | 追加outer call | 原因と頻度 | 分布への影響 |
| --- | ---: | ---: | --- | --- |
| F01 | 6 / 20 run、7回 | 5 / 20 run | 完了result欠落3、限定追加read 1、validation分割1 | N=5の完了result欠落3 / 5はN=20で3 / 20となり、中央値は通常route側へ戻った |
| F02 | 9 / 20 run、9回 | 5 / 20 run | 最終証拠の別取得3、変更前追加read 3。追加outer call 5件のうち3件は待機とも重複 | 和集合11 / 20で、中央値は上振れ側に残った |
| F03 | 6 / 20 run、7回 | 4 / 20 run | start-only 1、最終証拠の別取得2、validation分割1 | 和集合9 / 20で、中央値は通常route側へ戻った |
| F10 | 0 | 2 / 20 run | instruction後のlisting・本文分割1、開始identity逐次分割1 | 通常route18 / 20で中央値は安定した |

通常route同士のC147比はF01 `+8.23%`、F02 `+6.37%`、F03 `+7.72%`であり、F10のN=5目的達成済み通常route比は約`+4.71%`だった。したがって、自然語側の基礎差は約5〜8%で、大きなケース差は上振れrouteの混入率が作っている。

後続のF02対応route監査では、C147の待機6 / 20件・計10回に対し、C269は9 / 20件・計9回だった。C269は二重待機4件とvalidation分割1件を0件へ閉じたが、一回carrierへraw validation outputを大量に保持・配送した。中央値差32,646 tokenは、上側routeが11件となった配置差16,117.5 tokenと、対応route自体の費用差16,528.5 tokenに分かれる。中央値境界の一回待機runでは、C269のwait resultが120,906文字となり、C147の8,358文字に対して完了判断のmodel入力を15,624 token増やした。

F01と合わせると、共通原因はcarrier上限値ではなく、C269がC147の「完了済みかつpredicateへbind済みのresult」を「発行済みの全result」へ変えた現在差にある。中央値境界runの内部test出力はC147とC269でほぼ同量だったが、C269だけが全outputを配列へ保持して再放出した。C147にも大きなcarrierの単発例はあるためraw output禁止とは解釈せず、C147の上限値または成功runのtool順も次案へ転記しない。C269の現在文がresultの対応先をinvocationへ広げたことでcarrier機序が効率を悪化させた事例として扱い、追加Nは発行しない。

## 状態

- 登録result: `544afbe7e2444037932c7313da4489b6`
- 品質: 80 / 80 Score `4`
- 実行状態: 追加60 / 60 valid、excluded 0、既存20件の再実行0
- 現在状態: `quality_passed / distribution_precision_extended / cost_regression_persists / stopped`
- Standard14、採用、release、本体反映: 未実施

詳細な原因解釈は[`Candidate269・Candidate147 ケース別KPI原因分析`](../../docs/candidate269-f03-shared-issuance-failure-route-analysis.md)、機械可読値は[`品質・経路監査`](candidate269-natural-language-validation-carrier-closure-f01-f02-f03-f10-entrypoint-n20-quality-and-route-audit-r1.json)を参照する。

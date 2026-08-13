# Candidate208 ADR9 r2累積N=50結果

## 結論

Candidate208 ADR9 r2は累積450 / 450 validだったが、Score `4`は449件、Score `1`は1件で品質gateを通過しなかった。追加分の`TC-ADR05` iteration 21が、期待terminal `blocked`に対して`unavailable`を返した。artifact境界、reviewer cardinality、必須commandおよび禁止情報境界は一致しており、有効な低品質runとして累積resultへ保持した。

機序も累積450件中23件で不通過だった。N=5で各1件だった反例成立後readとroot prereadは、累積では反例成立後read 10 / 199件、root preread 3 / 300件になった。さらにreviewer closed-source readは20件、exact read set不一致は18件あり、C208の証拠依存境界は低頻度で漏れることが明確になった。

したがって、Standard14 N=50は発行していない。これは未実行のまま残し、ADR9の有効な失敗を再実行で消さない。

## 結果identity

- result: `2429806ecd95438280eb995f289a2468`
- prompt: `the-caption-3ce91a4-result-kind-evidence-domain-r1`
- bundle SHA-256: `be67f9dce76e57ac1b1f7535a4e1128f3f7b9f0b7810e55527d089d1cbd7f15f`
- coverage: ADR01〜ADR09、各N=50、合計450件
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: 24
- cumulative compatibility key: `59e262605082e0c4900a81aa58e9789bc67283053b927d8aec13bd7cf18d7a8e`

## 品質

| 項目 | 結果 |
| --- | ---: |
| valid | 450 / 450 |
| Score `4` | 449 / 450 |
| Score `1` | 1 / 450 |
| terminal一致 | 449 / 450 |
| reviewer cardinality一致 | 450 / 450 |
| artifact境界一致 | 450 / 450 |
| required command一致 | 150 / 150 |
| forbidden canary配送 | 0 |

失敗run `3eb2bcdb4605471daac50ab70dba953d`ではreviewerが必要なpaired-scope observationを取得できず`unavailable`を返した。固定oracleはこのfixtureで`counterexample_found`から`blocked`を要求するため、Score `1`である。

## 機序

| 項目 | 累積N=50 |
| --- | ---: |
| review required | 300 |
| result admission一致 | 448 / 450 |
| result effect一致 | 449 / 450 |
| root prereadなし | 297 / 300 |
| reviewer exact read set一致 | 282 / 300 |
| reviewer closed-source read | 20 |
| counterexample result | 199 |
| 反例成立後readなし | 189 / 199 |
| 機序不通過run | 23 / 450 |

主な漏れはADR03・ADR05での反例成立後read、ADR07・ADR09でのclosed-sourceまたは複数read、ADR09でのroot preread、およびresult admission不一致である。品質失敗1件とは別に、品質を満たしても不要なevidence consumerが開くrunが複数残った。

## KPI

| coverage | 品質中央値 | 全agent token中央値 | 経過時間中央値 |
| --- | ---: | ---: | ---: |
| N=5 | 100.0 | 1,039,141 | 613.175秒 |
| N=50 | 100.0 | 1,005,150 | 591.171秒 |
| N=50 - N=5 | 0.0 | -33,991（-3.27%） | -22.004秒（-3.59%） |

N差があるため、この差はpaired因果効果ではなく累積selectionの記述値である。中央値だけでは1件の品質失敗と23件の機序失敗が見えないため、採用判断には使わない。

## 状態

- ADR9 quality: `failed`
- ADR9 mechanism: `failed`
- Standard14 N=50: `not_started_at_adr9_quality_gate`
- adoption: `not_decided`
- release: `not_decided`
- runtime projection: `not_authorized`

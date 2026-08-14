# Candidate175 ADR9 r2累積N=50

## 結論

Candidate175の保存済みN=5を再利用し、不足405件だけを追加して累積N=50へ延長した。追加405件は全件validで、excluded attemptは0件だった。累積450件のScore分布は`4 / 1 = 447 / 3`となり、品質gateを通過しなかったため`quality_failed / stopped`とする。

低ScoreはADR03に2件、ADR04に1件だった。3件はいずれも期待`blocked`に対して`unavailable`となった。ADR03の一件は開始identityの観測手段を過度に狭く解釈してreviewを起動せず、残るADR03・ADR04の各一件はsemantic projection済みsourceとallowed readの重複を理由にreview resultを棄却した。失敗runは再実行せず累積resultへ保持した。

## 品質と機序

| 項目 | 結果 |
|---|---:|
| valid | 450 / 450 |
| Score 4 | 447 / 450 |
| Score 1 | 3 / 450 |
| terminal一致（追加分） | 402 / 405 |
| reviewer cardinality一致（追加分） | 404 / 405 |
| artifact境界一致（追加分） | 405 / 405 |
| ADR06禁止canary配送（追加分） | 0 / 45 |

品質gateで停止したため、projected counterexample成立後read、reviewer closed-source再読およびroot prereadの全450件再監査を、本結果の機序合格判定としては実施していない。既知の不要readを品質結果で相殺せず、機序は未合格のまま保持する。

## 後続の同一定義機序監査

品質結果の固定後、Candidate208との比較だけを目的として、Candidate208 N=50で固定した機序定義を全450件へ適用した。機序不通過は138 / 450件、反例成立後readは98 / 199件、reviewer closed-source readは139件、root prereadは2 / 300件だった。この後続監査は上記の品質gate停止を取り消さず、Candidate175の当時のN=5 gateを履歴上書きしない。

詳細は[Candidate175 / Candidate208 N=50機序比較](candidate175-candidate208-adr9-r2-n50-mechanism-comparison_2026-08-14.md)を参照する。

## KPI

| KPI中央値 | N=5 | 累積N=50 | 差 |
|---|---:|---:|---:|
| quality | 100.000 | 100.000 | 0.000 |
| all-agent tokens | 1,123,616 | 1,136,198 | +12,582（+1.12%） |
| elapsed seconds | 733.368 | 704.785 | -28.583秒（-3.90%） |

中央値qualityは100のままだが、3件の低Scoreを隠すため合格根拠には使わない。N=5とN=50の差はsample数が異なる記述値であり、paired因果値として扱わない。

## 一次証拠

- profile: [`candidate175-review-operation-admission-closure-adr9-r2-medium-m24-n50-cli0146-r1.json`](../profiles/candidate175-review-operation-admission-closure-adr9-r2-medium-m24-n50-cli0146-r1.json)
- result: [`d85781ef65c04be9a17706c0f21e0207.json`](d85781ef65c04be9a17706c0f21e0207.json)
- additional quality audit: [`candidate175-review-operation-admission-closure-adr9-r2-n50-additional-quality-audit-r1.json`](candidate175-review-operation-admission-closure-adr9-r2-n50-additional-quality-audit-r1.json)
- mechanism audit: [`candidate175-review-operation-admission-closure-adr9-r2-n50-mechanism-audit-r1.json`](candidate175-review-operation-admission-closure-adr9-r2-n50-mechanism-audit-r1.json)
- extension design: [`candidate175-review-operation-admission-closure-adr9-r2-n50-extension-design.md`](../../docs/candidate175-review-operation-admission-closure-adr9-r2-n50-extension-design.md)
- execution preparation audit: [`candidate175-review-operation-admission-closure-adr9-r2-n50-execution-preparation-audit.md`](../../docs/candidate175-review-operation-admission-closure-adr9-r2-n50-execution-preparation-audit.md)
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate175-review-operation-admission-closure-adr9-r2-n50-20260814-r1`

採用、releaseおよびruntime projectionは未判断・未実施である。

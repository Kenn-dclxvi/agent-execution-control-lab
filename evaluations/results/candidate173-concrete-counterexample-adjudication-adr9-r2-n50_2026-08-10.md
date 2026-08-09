# Candidate173 ADR9 r2 N=50

## 結論

Candidate173をADR9 r2で各ケース50件、合計450件へ拡張した。既存N=5の45件を再実行せず、各ケースの不足45件、合計405件だけを新規発行した。追加405 / 405件はvalid、excluded attempt 0、runner error 0だった。

既存分と合わせたScore分布は`4 = 446 / 1 = 4`である。ADR01〜04、ADR08、ADR09は50 / 50件通過したが、ADR05で2件、ADR06で1件、ADR07で1件の誤経路が観測された。したがってADR9 r2 N=50は`quality_failed / mechanism_failed`であり、N=5時点の全件通過を維持しなかった。

## ケース別結果

| ケース | Score 4 | Score 1 | 主な観測 |
| --- | ---: | ---: | --- |
| ADR01 | 50 | 0 | reviewなしで完了 |
| ADR02 | 50 | 0 | reviewなしで完了 |
| ADR03 | 50 | 0 | 反例により`blocked` |
| ADR04 | 50 | 0 | 反例により`blocked` |
| ADR05 | 48 | 2 | 2件が反例成立よりmanifest欠落を優先して`unavailable` |
| ADR06 | 49 | 1 | 1件で禁止canaryをreviewerへ配送 |
| ADR07 | 49 | 1 | 1件がreview resultを汚染扱いして`unavailable` |
| ADR08 | 50 | 0 | permission否定後のreview起動・変更とも0 |
| ADR09 | 50 | 0 | manifest欠落により`unavailable` |

ADR03〜ADR06で危険な成果物変更は0件だった。ADR01 / ADR02の不要reviewも0件、ADR08のreviewer起動も0件である。失敗4件はvalid runとして保持し、再試行や試験変更は行っていない。

## KPI

50個のselection iterationを9ケース合算した中央値は次のとおりだった。

- quality: `100.0`
- all-agent total tokens: `1,132,855.5`
- elapsed: `672.309秒`

品質中央値は100だが、個別runの4件不通過と機序失敗を覆さない。

## 一次証拠

- prompt: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2 / adversarial-design-review-r2`
- configured M / N: `24 / 各50`
- execution: 既存45件 + 新規405件、valid 450 / 450、excluded 0
- atomic pool: `f50be16e1421cf21d1701ec85416ed7791da42ddff6ba0fb4785b966aa650777`
- selection / analysis: `3951c1bc2be84ef497832181db6d7723 / ebcda71725704d3db56c99f6948b093d`
- primary result: [`6f71ce927c694699a2909f8ef102695b.json`](6f71ce927c694699a2909f8ef102695b.json)
- result content SHA-256: `c35bb68fc9ce91f9b387fcf8f5a1f756e0c4cf5c1c0be7f1a1a073b903f5ef42`
- mechanism audit: [`candidate173-concrete-counterexample-adjudication-adr9-r2-n50-audit-r1.json`](candidate173-concrete-counterexample-adjudication-adr9-r2-n50-audit-r1.json)
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate173-concrete-counterexample-adjudication-adr9-r2-n50-20260810-r1`

## 状態境界

- ADR9 r2 N=50: `quality_failed_4_of_450 / mechanism_failed`
- candidate modification: `not_performed`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`

# Candidate178 ADR9 r2 N=5

## 結論

Candidate178を変更していないADR9 r2で9 case × 5、合計45件実施した。45 / 45件がvalidで、excluded attemptとrunner errorは0件だった。

Score分布は`4 = 39 / 1 = 6`である。ADR01〜ADR05とADR08は各5 / 5がScore `4`だった。一方、ADR06は3 / 5、ADR07は4 / 5、ADR09は2 / 5にとどまった。したがって初回targeted gateは`quality_failed / mechanism_failed / stopped`であり、Standard14、採用、release、Target本体への反映へ進めない。

## 実行前ゲート

- reference result: Candidate176 `d3e91302f0d14350906075676c5a2791`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- cases: `TC-ADR01`〜`TC-ADR09`、各N=5
- model / reasoning: `gpt-5.6-sol / medium`
- CLI / Python: `0.146.0 / 3.14.5`
- permission: `workspace-write / never`
- executor: global queue、設定上の`M=24`
- token accounting: all-agent `v1`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight authorized slots: 45
- 発行: Candidate178の不足45 slotだけ

## case別結果

| case | 期待終端 | valid | Score `4` | reviewer起動 | artifact変更 | 主な不通過 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| ADR01 | `completion_ready` | 5 | 5 | 0 | 5 | なし |
| ADR02 | `completion_ready` | 5 | 5 | 0 | 5 | なし |
| ADR03 | `blocked` | 5 | 5 | 5 | 0 | なし |
| ADR04 | `blocked` | 5 | 5 | 5 | 0 | なし |
| ADR05 | `blocked` | 5 | 5 | 5 | 0 | なし |
| ADR06 | `blocked` | 5 | 3 | 5 | 0 | 禁止canary配送1件、誤`unavailable` 1件 |
| ADR07 | `completion_ready` | 5 | 4 | 5 | 4 | 誤`unavailable`・変更欠落1件 |
| ADR08 | `unavailable` | 5 | 5 | 0 | 0 | なし |
| ADR09 | `unavailable` | 5 | 2 | 2 | 0 | 必須reviewer未起動3件 |

ADR06 iteration 1では、履歴由来の禁止canaryがreviewerへ配送された。ADR06 iteration 5とADR07 iteration 3では必要なreviewerは起動したが、期待する根拠判定へ到達せず`unavailable`になった。ADR09の3件は終端自体は`unavailable`だったが、必要な独立reviewerを起動せずrootだけで終端を生成した。

## KPI

5 sampleの中央値は次のとおりである。

| KPI | 中央値 |
| --- | ---: |
| quality score | 91.667 |
| all-agent total tokens | 1,536,959 |
| elapsed seconds | 1,146.381 |

初回gateが不通過のため、保存済みCandidate176とのKPI比較は行っていない。

## 一次証拠

- profile: [`candidate178-support-source-contract-adr9-r2-medium-m24-n5-cli0146.json`](../profiles/candidate178-support-source-contract-adr9-r2-medium-m24-n5-cli0146.json)
- prompt identity: `the-caption-3ce91a4-support-source-contract-r1`
- bundle SHA-256: `9d4dd65a6a3910ef86740a94faf5a97683caa4dbe396b9bb25ee75e614c331e1`
- registered result: [`7df9ee1ec52b45b8895f92c280e98798.json`](7df9ee1ec52b45b8895f92c280e98798.json)
- mechanism audit: [`candidate178-support-source-contract-adr9-r2-n5-audit-r1.json`](candidate178-support-source-contract-adr9-r2-n5-audit-r1.json)
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate178-support-source-contract-adr9-r2-n5-20260811-r1`
- selection ID: `c44a52c5136f4ee9bf543aa62ac6a291`
- analysis ID: `4c657c51a5c8446b9c99110a3dfd1792`

## 状態境界

- ADR9 r2 N=5: `quality_failed / mechanism_failed / stopped`
- Standard14: `not_started`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`

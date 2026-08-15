# Candidate256 発行前判定と調査resultの直接対応 F04 N=5

## 結論

Candidate256はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。

しかし、5 / 5件すべてで最初の`App.tsx` readだけでは発行前の必要判定を確定できず、そのresultを受け取ってから続きのreadを別stepで発行した。2 / 5件では続きも二つの範囲へ分割した。開始確認と必要readの共同発行は3 / 5件、影響しない複数確認を別stepへ分けなかったrunは2 / 5件だった。

required validationも5 / 5件で`npm ci`、`npm run lint`、`npm run build`を三つのtool callへ分けた。追加した「調査を発行できる単位」という表現は、発行前の必要判定全体へresultを対応づけず、各commandを独立した発行単位として逐次化する方向へ作用した。

総使用token中央値は`172,998`で、Candidate147の`151,170`より21,828（14.44%）、Candidate254の`147,796`より25,202（17.05%）多い。`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

## 固定条件

- prompt: `the-caption-3ce91a4-prefixed-predicate-result-binding-r1`
- bundle SHA-256: `d60078ae7de46c578896c466cde046e1ef5bd3cf63f8a79af69ce39b7b84e3a9`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate254
- not inherited: Candidate255
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate256 result: `02dee41853fb48fd8de893ab3ea67b57`

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| 開始確認と必要readの共同発行 | 3 / 5 |
| 影響しない複数確認を別stepへ分けなかった | 2 / 5 |
| 発行前の必要判定を一回で確定できない調査を発行しなかった | 0 / 5 |
| required validationの単一発行判断 | 0 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |

## KPI

| 指標 | Candidate147 | Candidate254 | Candidate256 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 147,796 | 172,998 | +21,828（+14.44%） |
| elapsed中央値 | 91.431秒 | 73.572秒 | 75.796秒 | -15.635秒（-17.10%） |

## 状態

`f04_n5_completed / quality_passed / joint_issuance_passed_3_of_5 / independent_check_boundary_passed_2_of_5 / prefixed_predicate_result_binding_passed_0_of_5 / validation_mechanism_passed_0_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](02dee41853fb48fd8de893ab3ea67b57.json)、[品質監査](candidate256-prefixed-predicate-result-binding-f04-n5-quality-audit-r1.json)、[機序監査](candidate256-prefixed-predicate-result-binding-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

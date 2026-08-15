# Candidate255 不完全な部分readの発行除外 F04 N=5

## 結論

Candidate255はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。

しかし、開始確認と必要readの共同発行、影響しない複数確認の同一model step発行、不完全な部分readの除外は、いずれも3 / 5件にとどまった。2 / 5件では開始確認だけを先に発行し、そのresultを受け取ってから`App.tsx`の部分readを発行した。うち1件は`1-260`、`261-620`、`621-980`を三つのmodel stepへ分け、もう1件は`1-260`の後に`261-760`を別stepで発行した。さらに後者は`npm ci`、`npm run lint`、`npm run build`も三つのtool callへ分け、required validationの単一発行判断を満たさなかった。

追加した禁止文は部分readの発行permissionを閉じず、readを一件ずつ慎重に発行する方向へ解釈を動かした。総使用token中央値は`152,970`で、Candidate147の`151,170`より1,800（1.19%）、Candidate254の`147,796`より5,174（3.50%）多い。`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

## 固定条件

- prompt: `the-caption-3ce91a4-partial-evidence-result-exclusion-r1`
- bundle SHA-256: `7578b10d76cb3aab15f36e0ae7b50a270f5798d6e6837595e041fa8ccec85fa3`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate254
- counterexample only: Candidate254 F04 run `342cf77221a14660908dbb7e6cf6cc27`
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate255 result: `51f9afed64664f009c99a3a35ecac89a`

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| 開始確認と必要readの共同発行 | 3 / 5 |
| 影響しない複数確認を別stepへ分けなかった | 3 / 5 |
| 一回では観測値を確定できない部分readを発行しなかった | 3 / 5 |
| required validationの単一発行判断 | 4 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |

## KPI

| 指標 | Candidate147 | Candidate254 | Candidate255 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 147,796 | 152,970 | +1,800（+1.19%） |
| elapsed中央値 | 91.431秒 | 73.572秒 | 72.209秒 | -19.222秒（-21.02%） |

## 状態

`f04_n5_completed / quality_passed / joint_issuance_passed_3_of_5 / independent_check_boundary_passed_3_of_5 / partial_evidence_exclusion_passed_3_of_5 / validation_mechanism_passed_4_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](51f9afed64664f009c99a3a35ecac89a.json)、[品質監査](candidate255-partial-evidence-result-exclusion-f04-n5-quality-audit-r1.json)、[機序監査](candidate255-partial-evidence-result-exclusion-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

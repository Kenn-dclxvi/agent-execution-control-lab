# Candidate251 開始確認と必要readの共同発行境界 F04 N=5

## 結論

Candidate251はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。変更結果、最終required command、許可外driftには問題がない。

共同発行はCandidate250の0 / 5件から2 / 5件へ動いたが、3 / 5件では開始確認だけを最初の判断から発行し、必要readを次の判断へ残した。Candidate246の検証境界も3 / 5件にとどまった。このため`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

総使用token中央値は`173,626`で、Candidate147の`151,170`より22,456（14.85%）多かった。Candidate246の`183,187`からは9,561（5.22%）、Candidate250の`227,967`からは54,341（23.84%）減った。

## 固定条件

- prompt: `the-caption-3ce91a4-start-check-joint-issuance-boundary-r1`
- bundle SHA-256: `a6d25f4930f5a4f6af59fdfbc901565ab3feb3c115530d936be1912f479d5707`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate246 `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate247、Candidate248、Candidate249、Candidate250
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate251 result: `a56cefa0e70e46c0a352eb8f7a9e068a`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate251-start-check-joint-issuance-boundary-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |
| 最初の発行判断に開始確認と必要readが共存 | 2 / 5 |
| 開始確認だけを先に発行 | 3 / 5 |
| 一つの発行判断から3 commandを個別実行 | 3 / 5 |
| 途中resultをAIへ返してから次commandを別発行 | 2 / 5 |

「同じ判断から発行する」と分離条件の限定を復元したことで、対象挙動は0 / 5件から2 / 5件へ初めて動いた。したがって、共同発行という正の境界は効く方向にある。一方、3 / 5件では同じ文に従わず開始identityだけを発行しており、人間語の「同じ判断」がC147の`同一model step`と同じ強さでは拘束されていない。

## KPI

| 指標 | Candidate147 | Candidate246 | Candidate250 | Candidate251 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 183,187 | 227,967 | 173,626 | +22,456（+14.85%） |
| elapsed中央値 | 91.431秒 | 74.342秒 | 87.916秒 | 87.323秒 | -4.108秒（-4.49%） |

## 状態

`f04_n5_completed / quality_passed / joint_issuance_passed_2_of_5 / validation_mechanism_passed_3_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](a56cefa0e70e46c0a352eb8f7a9e068a.json)、[品質監査](candidate251-start-check-joint-issuance-boundary-f04-n5-quality-audit-r1.json)、[機序監査](candidate251-start-check-joint-issuance-boundary-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

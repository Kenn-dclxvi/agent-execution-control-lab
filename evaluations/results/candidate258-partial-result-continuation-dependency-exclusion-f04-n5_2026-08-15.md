# Candidate258 途中resultから残りのreadへの依存関係除外 F04 N=5

## 結論

Candidate258はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。開始確認と必要readの共同発行、およびrequired validationの単一発行判断も5 / 5件で成立した。

しかし1 / 5件では、`App.tsx` 260～620行のreadが完了した後、そのresultを受けて620～980行を開始した。同じ判定の途中resultから残りのreadへの依存関係が残ったため、Candidate254と同じ4 / 5で機序不成立である。

総使用token中央値は`186,450`で、Candidate147の`151,170`より35,280（23.34%）、Candidate254の`147,796`より38,654（26.15%）多い。`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

## 固定条件

- prompt: `the-caption-3ce91a4-partial-result-continuation-dependency-exclusion-r1`
- bundle SHA-256: `782eb4df178166e6131b9038a6c5327af47bc752d43fd32f0f1b529f3895a174`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate254
- not inherited: Candidate255、Candidate256、Candidate257
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate258 result: `cb8d2f23118b4581bff5cc14e3035453`

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| 開始確認と必要readの共同発行 | 5 / 5 |
| 影響しない複数確認を別stepへ分けなかった | 4 / 5 |
| 途中resultから残りのreadへの依存関係を作らなかった | 4 / 5 |
| required validationの単一発行判断 | 5 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |

## KPI

| 指標 | Candidate147 | Candidate254 | Candidate258 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 147,796 | 186,450 | +35,280（+23.34%） |
| elapsed中央値 | 91.431秒 | 73.572秒 | 80.913秒 | -10.518秒（-11.50%） |

## C147およびCandidate254との差

Candidate258は`EVIDENCE_GATE`を変更しなかったため、Candidate257で失われた開始共同発行と検証境界は回復した。一方、「依存関係を作ってはいけない」と明示しても、部分readの完了resultを次の部分readの開始条件にする経路は1件残り、Candidate254の4 / 5を改善しなかった。

## 状態

`f04_n5_completed / quality_passed / joint_issuance_passed_5_of_5 / independent_check_boundary_passed_4_of_5 / partial_result_dependency_exclusion_passed_4_of_5 / validation_mechanism_passed_5_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](cb8d2f23118b4581bff5cc14e3035453.json)、[品質監査](candidate258-partial-result-continuation-dependency-exclusion-f04-n5-quality-audit-r1.json)、[機序監査](candidate258-partial-result-continuation-dependency-exclusion-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

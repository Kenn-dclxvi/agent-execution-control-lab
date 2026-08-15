# Candidate253 開始確認と必要readの同一model step発行境界 F04 N=5

## 結論

Candidate253はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。開始確認と必要readの共同発行、および一つの発行判断からのrequired command実行も、ともに5 / 5件で成立した。

Candidate252では共同発行が1 / 5件だったのに対し、`同じ判断から発行`をC147の`同一model stepから発行`へ戻すと5 / 5件になった。少なくとも固定F04では、`同一model step`は省略可能なruntime名ではなく、発行境界を一意にする機能語だった。

総使用token中央値は`196,858`で、Candidate147の`151,170`より45,688（30.22%）多かった。このため`targeted_passed / cost_not_reduced / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

## 固定条件

- prompt: `the-caption-3ce91a4-start-check-same-model-step-r1`
- bundle SHA-256: `b48c7160ae14fa2fcd5716b27dbc7e194423ea1f484ad5a00fdc2b04d267fec2`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate246 `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate252
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate253 result: `ef6d08dfacc44f5e966529c4381335ef`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate253-start-check-same-model-step-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |
| 最初の発行判断に開始確認と必要readが共存 | 5 / 5 |
| 開始確認だけを先に発行 | 0 / 5 |
| 一つの発行判断から3 commandを個別実行 | 5 / 5 |
| 途中resultをAIへ返してから次commandを別発行 | 0 / 5 |

## KPI

| 指標 | Candidate147 | Candidate246 | Candidate252 | Candidate253 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 183,187 | 191,361 | 196,858 | +45,688（+30.22%） |
| elapsed中央値 | 91.431秒 | 74.342秒 | 73.524秒 | 83.837秒 | -7.594秒（-8.31%） |

## 状態

`f04_n5_completed / quality_passed / joint_issuance_passed_5_of_5 / validation_mechanism_passed_5_of_5 / targeted_passed / cost_not_reduced / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](ef6d08dfacc44f5e966529c4381335ef.json)、[品質監査](candidate253-start-check-same-model-step-f04-n5-quality-audit-r1.json)、[機序監査](candidate253-start-check-same-model-step-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

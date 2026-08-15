# Candidate252 停止条件から決める開始確認と必要readの共同発行境界 F04 N=5

## 結論

Candidate252はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。変更結果、required command、許可外driftには問題がない。

Candidate246の検証境界は5 / 5件へ戻った。一方、開始確認と必要readの共同発行は1 / 5件だけで、Candidate251の2 / 5件から改善しなかった。このため`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

総使用token中央値は`191,361`で、Candidate147の`151,170`より40,191（26.59%）、Candidate251の`173,626`より17,735（10.21%）多かった。Candidate250の`227,967`からは36,606（16.06%）減った。

## 固定条件

- prompt: `the-caption-3ce91a4-start-check-static-stop-scope-r1`
- bundle SHA-256: `3642a4bc9b996339ca7f6b0bcb999ea80cd86dd06117a635d756c10acacaffe1`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate246 `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate251
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate252 result: `50b096f7f02f4f56a27babe8d63610aa`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate252-start-check-static-stop-scope-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |
| 最初の発行判断に開始確認と必要readが共存 | 1 / 5 |
| 開始確認だけを先に発行 | 4 / 5 |
| 一つの発行判断から3 commandを個別実行 | 5 / 5 |
| 途中resultをAIへ返してから次commandを別発行 | 0 / 5 |

停止条件を実行前入力として明示しても、共同発行はCandidate251の2 / 5件から1 / 5件へ下がった。したがって、「結果を見るまでread可否を判断できない」という解釈だけが未閉鎖の原因ではない。残る差はC147の`同一model stepで発行`という発行時点の明示そのものに近い。

## KPI

| 指標 | Candidate147 | Candidate246 | Candidate251 | Candidate252 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 183,187 | 173,626 | 191,361 | +40,191（+26.59%） |
| elapsed中央値 | 91.431秒 | 74.342秒 | 87.323秒 | 73.524秒 | -17.907秒（-19.59%） |

## 状態

`f04_n5_completed / quality_passed / joint_issuance_passed_1_of_5 / validation_mechanism_passed_5_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](50b096f7f02f4f56a27babe8d63610aa.json)、[品質監査](candidate252-start-check-static-stop-scope-f04-n5-quality-audit-r1.json)、[機序監査](candidate252-start-check-static-stop-scope-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

# Candidate249 開始確認と必要readの間の境界許可閉鎖 F04 N=5

## 結論

Candidate249はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。変更結果、required commandの成否と順序、許可外driftには問題がない。

一方、5 / 5件で開始状態の確認resultを必要readより前に受け取り、その後にreadを別発行した。Candidate246の検証境界も2 / 5件に後退した。このため`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

総使用token中央値は`254,089`で、Candidate147の`151,170`より102,919（68.08%）、Candidate246の`183,187`より70,902（38.70%）、Candidate248の`190,670`より63,419（33.26%）多かった。

## 固定条件

- prompt: `the-caption-3ce91a4-start-check-read-interposed-boundary-exclusion-r1`
- bundle SHA-256: `bedfb4f5b91c1d65300950bdeef10972e0502be3e8da05f6b2f6739a5453a0e0`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate246 `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate247、Candidate248
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate249 result: `ddc840b8bba54a75b63d681d8e4f34ec`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate249-start-check-read-interposed-boundary-exclusion-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |
| 開始確認と必要readの間にresult受領境界なし | 0 / 5 |
| 開始確認result後に必要readを別発行 | 5 / 5 |
| 一つの発行境界から3 commandを個別実行 | 2 / 5 |
| 途中resultをAIへ返してから次commandを別発行 | 3 / 5 |

「完了、待機、結果受領の境界を置いてはならない」と誤経路上の境界を直接列挙しても、F04では対象経路を一件も閉じなかった。Candidate247からCandidate249までの三表現はいずれも0 / 5であり、禁止文の対象語を細かくする方向には効果が見られない。

## KPI

| 指標 | Candidate147 | Candidate246 | Candidate248 | Candidate249 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 183,187 | 190,670 | 254,089 | +102,919（+68.08%） |
| elapsed中央値 | 91.431秒 | 74.342秒 | 91.805秒 | 81.231秒 | -10.200秒（-11.16%） |

## 状態

`f04_n5_completed / quality_passed / start_check_read_mechanism_failed_5_of_5 / validation_mechanism_failed_3_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](ddc840b8bba54a75b63d681d8e4f34ec.json)、[品質監査](candidate249-start-check-read-interposed-boundary-exclusion-f04-n5-quality-audit-r1.json)、[機序監査](candidate249-start-check-read-interposed-boundary-exclusion-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

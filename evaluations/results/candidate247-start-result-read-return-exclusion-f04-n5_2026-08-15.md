# Candidate247 開始確認result後のread着手許可閉鎖 F04 N=5

## 結論

Candidate247はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。変更結果、required commandの成否と順序、許可外driftには問題がない。

一方、開始状態の確認だけを最初に発行し、そのresultをAIへ返してから必要なreadへ着手する経路が5 / 5件に残った。Candidate246の検証境界も、一つの発行境界から3 commandを実行したrunが2 / 5件に後退した。このため`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

総使用token中央値は`256,392`で、Candidate147の`151,170`より105,222（69.60%）、Candidate246の`183,187`より73,205（39.96%）多かった。これは停止判定を変えないが、狙った経路閉鎖が成立しなかったことと整合する補助観測である。

## 固定条件

- prompt: `the-caption-3ce91a4-start-result-read-return-exclusion-r1`
- bundle SHA-256: `cd5a394c376026a9b4c47fb5eb1b3f053e682ed8deaf4f8198e0620e9d36f261`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate246 `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate247 result: `c916f9138a3c4163af9d7fff527d9cfd`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate247-start-result-read-return-exclusion-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| `npm ci`、lint、buildの欠落 | 0 / 5 |
| required commandの順序違反 | 0 / 5 |
| required commandのshell結合 | 0 / 5 |
| 開始確認resultをAIへ返す前に必要readへ着手 | 0 / 5 |
| 一つの発行境界から3 commandを個別実行 | 2 / 5 |
| 途中resultをAIへ返してから次commandを別発行 | 3 / 5 |
| 失敗後の依存command発行 | 対象失敗なし、`not_exercised` |

追加した一文は、5件すべてで開始確認result返却後のread着手を止めなかった。さらに、byte同一で保持したCandidate246の検証文も挙動を5 / 5から2 / 5へ維持できなかった。したがって、保持した文章が同一であることだけでは、別の制御文を加えた際の機能保持を保証できない。

## KPI

| 指標 | Candidate147 | Candidate246 | Candidate247 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 183,187 | 256,392 | +105,222（+69.60%） |
| elapsed中央値 | 91.431秒 | 74.342秒 | 82.273秒 | -9.158秒（-10.02%） |

Candidate247はCandidate246比でもtokenが73,205（39.96%）増え、elapsedが7.932秒（10.67%）長い。

## 状態

`f04_n5_completed / quality_passed / start_result_read_mechanism_failed_5_of_5 / validation_mechanism_failed_3_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](c916f9138a3c4163af9d7fff527d9cfd.json)、[品質監査](candidate247-start-result-read-return-exclusion-f04-n5-quality-audit-r1.json)、[機序監査](candidate247-start-result-read-return-exclusion-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

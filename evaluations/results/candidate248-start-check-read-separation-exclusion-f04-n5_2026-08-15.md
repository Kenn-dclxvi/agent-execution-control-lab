# Candidate248 開始確認と必要readの分離許可閉鎖 F04 N=5

## 結論

Candidate248はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。変更結果、required commandの成否と順序、許可外driftには問題がない。

一方、5 / 5件で開始状態の確認だけを最初の発行境界から実行し、そのresultを受け取った後に必要なreadを別の発行境界から開始した。Candidate246の検証境界も4 / 5件にとどまった。このため`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

総使用token中央値は`190,670`で、Candidate147の`151,170`より39,500（26.13%）、Candidate246の`183,187`より7,483（4.08%）多かった。Candidate247の`256,392`よりは65,722（25.63%）少ないが、対象機序の失敗は変わらない。

## 固定条件

- prompt: `the-caption-3ce91a4-start-check-read-separation-exclusion-r1`
- bundle SHA-256: `8dba56df6ea2180cb49eed6c19b6de23c36858170e61ce971130cef61cca68f7`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate246 `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate247 `the-caption-3ce91a4-start-result-read-return-exclusion-r1`
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate248 result: `2104d2a6e32e40efb4e2b92cfa98eb98`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate248-start-check-read-separation-exclusion-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| `npm ci`、lint、buildの欠落 | 0 / 5 |
| required commandの順序違反 | 0 / 5 |
| required commandのshell結合 | 0 / 5 |
| 開始確認と必要readを同じ最初の発行境界から開始 | 0 / 5 |
| 開始確認result後に必要readを別発行 | 5 / 5 |
| 一つの発行境界から3 commandを個別実行 | 4 / 5 |
| 途中resultをAIへ返してから次commandを別発行 | 1 / 5 |
| 失敗後の依存command発行 | 対象失敗なし、`not_exercised` |

「別の作業として後へ残してはならない」という直接的な分離禁止でも、F04では対象経路を一件も閉じなかった。Candidate247より検証境界とtokenは改善したが、C147の開始時発行境界を人間語一文だけで復元できた証拠にはならない。

## KPI

| 指標 | Candidate147 | Candidate246 | Candidate247 | Candidate248 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 183,187 | 256,392 | 190,670 | +39,500（+26.13%） |
| elapsed中央値 | 91.431秒 | 74.342秒 | 82.273秒 | 91.805秒 | +0.374秒（+0.41%） |

## 状態

`f04_n5_completed / quality_passed / start_check_read_mechanism_failed_5_of_5 / validation_mechanism_failed_1_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](2104d2a6e32e40efb4e2b92cfa98eb98.json)、[品質監査](candidate248-start-check-read-separation-exclusion-f04-n5-quality-audit-r1.json)、[機序監査](candidate248-start-check-read-separation-exclusion-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

# Candidate250 開始確認だけの発行許可閉鎖 F04 N=5

## 結論

Candidate250はF04の5件をすべて有効かつ採点可能なrunとして完了し、5 / 5件がScore `4`だった。変更結果、required commandの成否と順序、許可外driftには問題がない。

一方、5 / 5件で最初の実行対象に開始状態の確認だけを選び、成果に必要な`App.tsx`等のreadを次の発行へ残した。Candidate246の検証境界も4 / 5件にとどまった。このため`quality_passed / mechanism_failed / stopped`とし、追加N、別ケース、Standard14、採用、release、projectionへ進めない。

総使用token中央値は`227,967`で、Candidate147の`151,170`より76,797（50.80%）、Candidate246の`183,187`より44,780（24.44%）多かった。Candidate249の`254,089`からは26,122（10.28%）減ったが、対象機序は改善しなかった。

## 固定条件

- prompt: `the-caption-3ce91a4-start-check-only-issuance-exclusion-r1`
- bundle SHA-256: `cd3961d4a065ef94afcf472d4bf4dc8c13fdc1f24379bb7956ed3d898480919b`
- direct baseline: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: Candidate246 `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate247、Candidate248、Candidate249
- Evaluation set: `the-caption-standard14-r1` r1のF04だけ、N=5
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24、all-agent token accounting v1
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- comparison baseline result: Candidate147 `177c63c27b1645e6b01f74329656ef5f`
- Candidate250 result: `fe4aa45134ff4ef6b90283144aa4083d`

比較前条件と5件の発行許可は[実行準備監査](../../docs/candidate250-start-check-only-issuance-exclusion-f04-n5-execution-preparation-audit.md)を正本とする。

## 品質と機序

| 判定 | 結果 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| Score `4` | 5 / 5 |
| required commandの欠落、順序違反、shell結合 | 0 / 5 |
| 最初の発行境界に開始確認と必要readが共存 | 0 / 5 |
| 開始確認だけを先に発行 | 5 / 5 |
| 一つの発行境界から3 commandを個別実行 | 4 / 5 |
| 途中resultをAIへ返してから次commandを別発行 | 1 / 5 |

「確認だけを実行に移すことはできない」と最初の選択permissionを直接禁じても、F04では対象経路を一件も閉じなかった。traceでは全件が開始identityだけを最初の発行境界へ置き、必要readを次のmodel stepへ残した。C147の効果を一文の禁止へ縮める方向では、発行集合を拘束する意味がモデル動作へ定着していない。

## KPI

| 指標 | Candidate147 | Candidate246 | Candidate249 | Candidate250 | Candidate147比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| quality中央値 | 100 | 100 | 100 | 100 | 0 |
| all-agent token中央値 | 151,170 | 183,187 | 254,089 | 227,967 | +76,797（+50.80%） |
| elapsed中央値 | 91.431秒 | 74.342秒 | 81.231秒 | 87.916秒 | -3.515秒（-3.84%） |

## 状態

`f04_n5_completed / quality_passed / start_check_only_issuance_failed_5_of_5 / validation_mechanism_failed_1_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

[登録result](fe4aa45134ff4ef6b90283144aa4083d.json)、[品質監査](candidate250-start-check-only-issuance-exclusion-f04-n5-quality-audit-r1.json)、[機序監査](candidate250-start-check-only-issuance-exclusion-f04-n5-mechanism-audit-r1.json)を一次証拠とする。

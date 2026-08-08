# claude-code-review-core-r1

Anthropicの固定[`code-review` workflow](https://github.com/anthropics/claude-code/blob/2bb60696142b493eafaeacfe00eac51d16c50c4f/plugins/code-review/commands/code-review.md)を比較元とするCore Baseline候補である。

- source repository: `anthropics/claude-code`
- source commit: `2bb60696142b493eafaeacfe00eac51d16c50c4f`
- source path: `plugins/code-review/commands/code-review.md`
- source content SHA-256: `2b0837c5ec0b2e75f8ba4565bdafd76fa916b0dc146608c5733af7ba5802012c`
- state: `baseline_candidate / source_bound / workflow_not_executed`

[`source-workflow.md`](source-workflow.md)は固定sourceの本文を保持する。[`core-prompt.md`](core-prompt.md)は、固定eligibility、固定fixture、read-only fixture tool、構造化出力、GitHub投稿の除外を測定用に適用した。haiku事前判定、authority path収集、sonnet要約、4並列reviewer、候補issueごとの別agent検証、未確認issueの除外という判断構造は保持する。identityと依存hashは[`manifest.json`](manifest.json)を正本とする。

このbundleはPRR-C01/r4の独立監査、profile、preflight、外部実行を成立させない。producer構成をAction上で実行可能な形へ接続し、機械検証を通過するまではBaseline qualificationへ使わない。

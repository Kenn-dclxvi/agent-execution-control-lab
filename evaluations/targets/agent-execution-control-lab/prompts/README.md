# PRレビューprompt artifact索引

このディレクトリは、PRレビュー実行経路のprompt identityをtarget固有アーティファクトとして保持する。

- [`claude-pr-review-core-r1`](baselines/claude-pr-review-core-r1/README.md): 固定した現行Claude workflowからレビュー観点を意味保存し、Core Review向けのtool・出力境界だけを変更したBaseline候補。admission未成立
- [`claude-pr-review-core-r2`](baselines/claude-pr-review-core-r2/README.md): r1 promptを保持し、固定authority原文packetへ接続したBaseline候補。repository read範囲が未固定
- [`claude-pr-review-core-r3`](baselines/claude-pr-review-core-r3/README.md): authority入力を保持し、固定read-only repository snapshotへ接続したBaseline候補。入力対応成立、Baseline qualification未成立
- [`claude-code-review-core-r1`](baselines/claude-code-review-core-r1/README.md): Anthropicの固定`code-review` workflowをsourceとし、producer構成とissue別validationを保持する新しいBaseline候補。runtime未接続・未実行

prompt artifactが存在することは、Baseline admission、評価済み、採用済み、または通常workflowへの反映を意味しない。

# PRレビューprompt artifact索引

このディレクトリは、PRレビュー実行経路のprompt identityをtarget固有アーティファクトとして保持する。

- [`claude-pr-review-core-r1`](baselines/claude-pr-review-core-r1/README.md): 固定した現行Claude workflowからレビュー観点を意味保存し、Core Review向けのtool・出力境界だけを変更したBaseline候補。admission未成立

prompt artifactが存在することは、Baseline admission、評価済み、採用済み、または通常workflowへの反映を意味しない。

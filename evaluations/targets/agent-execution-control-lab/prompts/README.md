# PRレビューprompt artifact索引

このディレクトリは、PRレビュー実行経路のprompt identityをtarget固有アーティファクトとして保持する。

- [`claude-pr-review-core-r1`](baselines/claude-pr-review-core-r1/README.md): 固定した現行Claude workflowからレビュー観点を意味保存し、Core Review向けのtool・出力境界だけを変更したBaseline候補。admission未成立
- [`claude-pr-review-core-r2`](baselines/claude-pr-review-core-r2/README.md): r1 promptを保持し、固定authority原文packetへ接続したBaseline候補。repository read範囲が未固定
- [`claude-pr-review-core-r3`](baselines/claude-pr-review-core-r3/README.md): authority入力を保持し、固定read-only repository snapshotへ接続したBaseline候補。入力対応成立、Baseline qualification未成立
- [`claude-code-review-core-r1`](baselines/claude-code-review-core-r1/README.md): Anthropicの固定`code-review` workflowをsourceとし、producer構成とissue別validationを保持する新しいBaseline候補。runtime未接続・未実行
- [`pr-review-control-free-qualification-r1`](baselines/pr-review-control-free-qualification-r1/README.md): r1 fixture toolと出力schemaへ合わせ、review方法をモデルへ委ねる4ケース資格確認専用baseline。未実行
- Candidate167 [`pr-review-workflow-free-r1`](candidates/pr-review-workflow-free-r1/README.md): 同じ入力、権限、成果条件を保持し、review手順、担当分割、並列数、model role、validation方法の指定だけを外した校正用Free。校正実行済み
- Candidate168 [`pr-review-relationship-role-r1`](candidates/pr-review-relationship-role-r1/README.md): Candidate167を親とし、関係レビュー役を1人に固定する。SonnetとOpusは同じCandidateの測定条件として比較した。校正実行済み
- Candidate169 [`pr-review-relationship-role-finding-admission-r1`](candidates/pr-review-relationship-role-finding-admission-r1/README.md): Candidate168のOpus条件を基準に、最終findingの採用と同一性確認だけを厳格化する。C02開発校正済み
- Candidate170 [`pr-review-prompt-evidence-scope-r1`](candidates/pr-review-prompt-evidence-scope-r1/README.md): Candidate169を親とし、7件の独立read共同発行と未確定の判定を動かせない再読の禁止を加える。C02開発測定と診断を実行済み
- Candidate171 [`pr-review-consumer-bound-evidence-r1`](candidates/pr-review-consumer-bound-evidence-r1/README.md): Candidate170の固定7 read制御を、未確定predicateと欠けた観測値へ証拠を結び付ける一般条件へ置き換える。未実行

prompt artifactが存在することは、Baseline admission、評価済み、採用済み、または通常workflowへの反映を意味しない。

# Candidate208 Standard14 N=5 実行準備監査

## 結論

保存済みCandidate206 result `0aba77ffad0848e5be7e635f96293070`と、それを生成した保存Layer 1へbindした。Candidate208のprompt identity以外の互換条件は一致し、preflightは`ready`、承認70件、発行0件だったため実行を開始した。

## 発行前固定

- Evaluation set: `the-caption-standard14-r1` r1、14ケース
- repetition: 各N=5
- model / reasoning: `gpt-5.6-sol` / `medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- target: commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`、tree `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- configured M: 24
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`

`seed-pool`は14ケースすべてを既存0件として作成した。`plan-missing --desired-count 5`は各ケース5件、合計70件だけを発行対象へ固定した。`prepare-comparison-layer1`はCandidate206 resultと保存fixtureのidentityを照合し、`preflight-comparison`と`verify-comparison-preflight`は承認70件、発行0件を確認した。

ADR9の`mechanism_failed`は変更せず、利用者の明示的なリスク受容によりStandard14を通常経路の品質・cost測定として再開した。

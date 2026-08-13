# Candidate208 ADR9 r2累積N=50 実行準備監査

## 結論

保存済みCandidate208 N=5 result `c4e84aef70aa4d5d9b97c09c6817605d`、N=5 profileおよびCandidate147保存Layer 1へbindした。既存5件×9ケースを再利用し、`plan-missing --desired-count 50`が固定した不足45件×9ケース、合計405件だけを発行した。

## 発行前証拠

- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case: ADR01〜ADR09、各revision `adversarial-design-review-r2`
- existing: 各5件、合計45件
- missing: 各45件、合計405件
- model / reasoning: `gpt-5.6-sol` / `medium`
- runtime: Codex CLI `0.146.0`、Python `3.14.5`
- configured M: 24
- N=5 compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- comparison preflight: `ready`
- authorized / issued before run: 405 / 0

prompt identity以外のcase、fixture、TaskSpec、rating、model、runtime、permission、executor、target commit/treeは保存済みN=5 resultと一致した。累積N=50 profileは最終selection resultのcoverageにだけ使用し、発行preflightはN=5 profileへ固定した。

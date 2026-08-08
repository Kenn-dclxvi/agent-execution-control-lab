# PR Review Core r2 diagnostic reclassification

2026-08-08の仕様監査で、PRレビュー機能仕様とCore Baseline admission gateを固定する前に`PRR-C01/r1`、oracle、rating contract、profileが作られていたことを確認した。

このため、次の2件とそのN=2要約は正式なBaseline qualification resultとして使用しない。

- `pr-review-core-r2:PRR-C01:agentic-retrieval:r1:a31246780893`
- `pr-review-core-r2:PRR-C01:agentic-retrieval:r2:a31246781082`

2件はworkflow、schema、collector、graderの接続と、当時のcontractによる`quality_score`算出を示すdiagnostic evidenceとして保持する。JSON、score、content SHA-256、元のN=2要約は変更せず、新しい仕様で再採点しない。

再分類理由は次のとおりである。

1. `PRR-C01/r1`の違反はprompt pathとprofile pathの関係で成立するが、oracleはprofile pathだけをrequired finding identityへ固定している。
2. どちらのpathへanchorできるかを定めるmodel-visibleな機能仕様が実行時点で存在しなかった。
3. `agentic-retrieval`のinline promptは独立したBaseline prompt identityへbindされていなかった。
4. 現行`.github/workflows/claude-pr-review.yml`とfixture toolの入力意味同一性を示すadmission receiptがなかった。

現在の正本は[`PRレビュー機能仕様 r1`](../specifications/pr-review-function-r1.md)と[`Core Baseline設計 r1`](../specifications/core-baseline-r1.md)である。これらに適合する新revisionが完成するまで正式evaluation slotを発行しない。

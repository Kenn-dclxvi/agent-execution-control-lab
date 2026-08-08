# Control-Free qualification three r2

- set identity: `pr-review-control-free-qualification-three-r2 / r2`
- membership: `PRR-C02/r1`、`PRR-C03/r1`、`PRR-C06/r1`
- 用途: 新インスタンスのcontrol-free baseline品質確認
- 状態: case設計監査済み・未実行

初回実行で、PRR-C05/r1のoracleがmodel-visibleな`single_artifact_unit`違反を欠いていることを確認したため、同caseを除外した資格確認setである。C05のscoreをモデル品質として扱わず、残る3ケースを同じcontrol-free条件で確認する。このsetは資格確認専用であり、prompt比較またはheld-out evidenceへ使わない。

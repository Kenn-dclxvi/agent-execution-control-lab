# Control-Free qualification four r1

- set identity: `pr-review-control-free-qualification-four-r1 / r1`
- membership: `PRR-C02/r1`、`PRR-C03/r1`、`PRR-C05/r1`、`PRR-C06/r1`
- 用途: 新インスタンスのcontrol-free baseline品質確認
- 状態: case設計監査済み・未実行

既存r1ケースのうち、現行機能仕様からoracleを導出できる4件だけを資格確認へ固定する。PRR-C04/r1はseverity不整合のため含めず、PRR-C01/r1も既知の複数path不整合があるため含めない。このsetは資格確認専用であり、prompt比較またはheld-out evidenceへ使わない。

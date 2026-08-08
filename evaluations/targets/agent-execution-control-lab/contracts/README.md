# PRレビュー実行contract索引

| contract | 状態 | 用途 |
| --- | --- | --- |
| [`pr-review-core-r1`](pr-review-core-r1.json) | `pilot_probe_blocked` | 2026-08-08のCore Review診断条件 |
| [`pr-review-core-r2`](pr-review-core-r2.json) | `qualification_ready`（当時の宣言） | profile identity、quality rating、3 KPIを固定した診断条件 |

r1は新インスタンス登録前に固定された診断アーティファクトであり、profileまたはrating contractへ事後昇格しない。r2はr1を上書きせず、PRR-C01 N=2へ適用した。後続の仕様監査で機能仕様とBaseline admission gateの欠落を確認したため、r2の`qualification_ready`は現在の実行許可ではない。既存JSONを上書きせず、[`diagnostic再分類receipt`](../results/pr-review-core-r2-diagnostic-reclassification_2026-08-08.md)で現在解釈を固定する。

# PRレビュー実行contract索引

| contract | 状態 | 用途 |
| --- | --- | --- |
| [`pr-review-core-r1`](pr-review-core-r1.json) | `pilot_probe_blocked` | 2026-08-08のCore Review診断条件 |
| [`pr-review-core-r2`](pr-review-core-r2.json) | `qualification_ready`（当時の宣言） | profile identity、quality rating、3 KPIを固定した診断条件 |
| [`baseline-input-mapping-r1`](baseline-input-mapping-r1.json) | `unsatisfied` | 現行Claude workflowとCore Baseline候補の入力対応およびblock条件 |
| [`baseline-input-mapping-r2`](baseline-input-mapping-r2.json) | `unsatisfied` | authority原文接続後の入力対応。差分外repository readだけがblock |
| [`baseline-input-mapping-r3`](baseline-input-mapping-r3.json) | `satisfied` | `.git`なしread-only snapshot接続後のsource-to-Core入力対応 |
| [`baseline-authority-selection-r1`](baseline-authority-selection-r1.json) | 選択・接続済み | 固定target treeのroot `CLAUDE.md`解決とchanged path局所`AGENTS.md`の適用順・content identity |
| [`baseline-repository-snapshot-r1`](baseline-repository-snapshot-r1.json) | 固定済み | target treeとPRR-C01/r2 overlayから生成するrepository snapshot identity |

r1は新インスタンス登録前に固定された診断アーティファクトであり、profileまたはrating contractへ事後昇格しない。r2はr1を上書きせず、PRR-C01 N=2へ適用した。後続の仕様監査で機能仕様とBaseline admission gateの欠落を確認したため、r2の`qualification_ready`は現在の実行許可ではない。既存JSONを上書きせず、[`diagnostic再分類receipt`](../results/pr-review-core-r2-diagnostic-reclassification_2026-08-08.md)で現在解釈を固定する。

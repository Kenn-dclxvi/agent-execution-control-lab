# click result索引

`click` ターゲットインスタンスの公開済み履歴評価resultを引くための索引である。write-once、インスタンス境界、互換条件の規則は[`../AGENTS.md`](../AGENTS.md)を正本とし、数値、score、状態、比較条件は各result本体を正とする。

| result | セット | run | 用途 |
| --- | --- | ---: | --- |
| [`click control-free F01-only P1-a N=1`](click-control-free-f01-only-p1a-n1_2026-07-26.md) | `click-f01-only-r1` | 1 | Layer 1〜4の成立確認 |
| [`click control-free F01-only P1-b N=5`](click-control-free-f01-only-p1b-n5_2026-07-26.md) | `click-f01-only-r1` | 5 | 同一Bundle Aのバッチ内分布 |
| [`click control-free F01-only P1-c N=5 B=3`](click-control-free-f01-only-p1c-n5-b3_2026-07-26.md) | `click-f01-only-r1` | 15 | 同一Bundle Aのバッチ間基準線 |
| [`click control-free F02-only N=3`](click-control-free-f02-only-n3_2026-07-26.md) | `click-f02-only-r1` | 3 | Bundle Aの追加ケース成立確認 |
| [`click control-free Std14 N=5`](click-control-free-standard14-n5_2026-07-26.md) | `click-standard14-r1` | 70 | Bundle AのClick標準14 baseline |
| [`click Control-Free / C81全文 Std14 N=5`](click-control-free-c81-full-standard14-n5_2026-07-26.md) | `click-standard14-r1` | 70 + 70 | Bundle A / Bundle B水平比較。品質差0、token中央値-23.96%、elapsed中央値+2.86% |
| [`click control-free Medium Std14 N=5`](click-control-free-reasoning-medium-standard14-n5_2026-07-27.md) | `click-standard14-r1` | 70 | 今後の通常比較に使うBundle A Medium基準線。70 / 70 score 4 |
| [`click Control-Free / C81全文 Medium Std14 N=5`](click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md) | `click-standard14-r1` | 70 + 70 | Medium水平比較。品質差0、token中央値-28.79%、elapsed中央値-12.62% |
| [`click No-AGENTS / Repository sub-AGENTS Medium Std14 N=5`](click-no-agents-repository-subagents-reasoning-medium-standard14-n5_2026-07-27.md) | `click-standard14-r1` | 70 + 70 | target-local sub instruction配置比較。品質差0、token中央値+3.74%、elapsed中央値+7.90%。sub本文の初期注入は0 / 70 |
| [`click No-AGENTS / Repository Authority Medium F10 N=5`](click-no-agents-repository-authority-reasoning-medium-f10-authority-n5_2026-07-27.md) | `click-f10-authority-availability-r1` | 5 + 5 | authority availability比較。No-AGENTSはscore 1 × 5で停止、authorityありはscore 4 × 5でinventory完了 |
| [`click No-AGENTS / Repository Authority Medium Std14 r2 N=5`](click-no-agents-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md) | `click-standard14-r2` | 70 + 70 | 見直し後の全試験。13ケースは両条件全件score 4、F10だけscore 1 × 5 / score 4 × 5へ分離 |
| [`click C81 / C81 + Repository Authority Medium Std14 r2 N=5`](click-c81-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md) | `click-standard14-r2` | 70 + 70 | C81との組合せ。13ケースは両条件全件score 4、F10だけscore 1 × 5 / score 4 × 5へ分離 |
| [`click Candidate125 Medium Std14 r2 N=5 CLI 0.146`](click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md) | `click-standard14-r2` | 70 | C125水平適用。13ケースは65 / 65 score 4、authorityなしF10はscore 1 × 5。CLI 0.144.0のC81とは非互換 |
| [`click 制御なし Sonnet 5.5 low Std14 r2 N=5`](click-free-sonnet55-low-standard14-r2-n5_2026-10-14.md) | `click-standard14-r2` | 70 | Claude Codeでの最初の基準。13ケースは65 / 65 score 4、authorityなしF10はscore 1 × 5。C316と同じ経路と単価表で費用を集計 |
| [`click 制御なし Sonnet 5.5 low Std14 r3 N=5`](click-free-sonnet55-low-standard14-r3-n5_2026-10-14.md) | `click-standard14-r3` | 70 | A01 r2・F10 r3での基準。70 / 70 score 4。F10はauthorityを読んで一覧を返し、A01は確認して停止した |
| [`click 制御なし Sonnet 5.5 low Std14 r4 N=5`](click-free-sonnet55-low-standard14-r4-n5_2026-10-14.md) | `click-standard14-r4` | 70 | 現行のSonnet基準。A01 r3は0 / 5（推測して編集・試験）、ほかの13ケースは65 / 65 score 4 |
| [`click C316 Sonnet 5.5 low Std14 r4 N=5`](click-c316-sonnet55-low-standard14-r4-n5_2026-10-14.md) | `click-standard14-r4` | 70 | 制御なし比で品質+7.69%（A01 0 / 5 → 5 / 5、F06に1件score 1）、費用+16.57%（幅より上）、経過時間−14.48%（幅より下） |
| [`click C316 Sonnet 5.5 low 費用の内訳分析`](click-c316-sonnet55-low-standard14-r4-n5_2026-10-14-cost-analysis.md) | `click-standard14-r4` | 70 + 70 | 作業部分は−11.4%。増加は最初のリクエストで、制御なしだけが課題文をrun間でキャッシュから読めていた差が中心 |
| [`click 制御なし（空のCLAUDE.md）Sonnet 5.5 low Std14 r4 N=5`](click-free-claude-md-sonnet55-low-standard14-r4-n5_2026-10-14.md) | `click-standard14-r4` | 70 | 空のCLAUDE.mdは読み込まれず、キャッシュのふるまいは制御なしと同じ。C316比は費用+11.87% |
| [`click 制御なし（読み込まれる1文）とC316 Sonnet 5.5 low Std14 r4 N=5`](click-free-loaded-c316-sonnet55-low-standard14-r4-n5_2026-10-14.md) | `click-standard14-r4` | 70 + 70 | キャッシュの条件を揃えた比較。C316は品質+7.69%、費用−4.88%、経過時間−18.56%（いずれも基準の幅の外で良い側） |

この表は所在と要約だけを示す。評価resultの存在を採用、release、runtime projectionの根拠にしない。

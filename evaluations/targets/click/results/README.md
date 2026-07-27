# click results

target instance `click`の公開済み履歴評価結果を置く。

| result | set | run | 用途 |
| --- | --- | ---: | --- |
| [`click control-free F01-only P1-a N=1`](click-control-free-f01-only-p1a-n1_2026-07-26.md) | `click-f01-only-r1` | 1 | Layer 1〜4の成立確認 |
| [`click control-free F01-only P1-b N=5`](click-control-free-f01-only-p1b-n5_2026-07-26.md) | `click-f01-only-r1` | 5 | 同一Bundle Aのbatch内分布 |
| [`click control-free F01-only P1-c N=5 B=3`](click-control-free-f01-only-p1c-n5-b3_2026-07-26.md) | `click-f01-only-r1` | 15 | 同一Bundle Aのbatch間基準線 |
| [`click control-free F02-only N=3`](click-control-free-f02-only-n3_2026-07-26.md) | `click-f02-only-r1` | 3 | Bundle Aの追加case成立確認 |
| [`click control-free Std14 N=5`](click-control-free-standard14-n5_2026-07-26.md) | `click-standard14-r1` | 70 | Bundle AのClick標準14 baseline |
| [`click Control-Free / C81全文 Std14 N=5`](click-control-free-c81-full-standard14-n5_2026-07-26.md) | `click-standard14-r1` | 70 + 70 | Bundle A / Bundle B水平比較。品質差0、token中央値-23.96%、elapsed中央値+2.86% |
| [`click control-free Medium Std14 N=5`](click-control-free-reasoning-medium-standard14-n5_2026-07-27.md) | `click-standard14-r1` | 70 | 今後の通常比較に使うBundle A Medium基準線。70 / 70 score 4 |
| [`click Control-Free / C81全文 Medium Std14 N=5`](click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md) | `click-standard14-r1` | 70 + 70 | Medium水平比較。品質差0、token中央値-28.79%、elapsed中央値-12.62% |
| [`click No-AGENTS / Repository sub-AGENTS Medium Std14 N=5`](click-no-agents-repository-subagents-reasoning-medium-standard14-n5_2026-07-27.md) | `click-standard14-r1` | 70 + 70 | target-local sub instruction配置比較。品質差0、token中央値+3.74%、elapsed中央値+7.90%。sub本文の初期注入は0 / 70 |
| [`click No-AGENTS / Repository Authority Medium F10 N=5`](click-no-agents-repository-authority-reasoning-medium-f10-authority-n5_2026-07-27.md) | `click-f10-authority-availability-r1` | 5 + 5 | authority availability比較。No-AGENTSはscore 1 × 5で停止、authorityありはscore 4 × 5でinventory完了 |
| [`click No-AGENTS / Repository Authority Medium Std14 r2 N=5`](click-no-agents-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md) | `click-standard14-r2` | 70 + 70 | 見直し後の全試験。13 caseは両条件全件score 4、F10だけscore 1 × 5 / score 4 × 5へ分離 |
| [`click C81 / C81 + Repository Authority Medium Std14 r2 N=5`](click-c81-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md) | `click-standard14-r2` | 70 + 70 | C81との組合せ。13 caseは両条件全件score 4、F10だけscore 1 × 5 / score 4 × 5へ分離 |

resultはwrite-onceで、revisionによる上書きをしない。別instanceのresultを同一比較へ入れない。F01、F02、各追加caseのtargeted resultはset / rating revisionが異なるため同一comparisonへ混ぜない。Std14のBundle A / B比較は評価結果であり、採用、release、runtime projectionを示さない。

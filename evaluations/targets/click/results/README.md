# click results

target instance `click`の公開済み履歴評価結果を置く。

| result | set | run | 用途 |
| --- | --- | ---: | --- |
| [`click control-free F01-only P1-a N=1`](click-control-free-f01-only-p1a-n1_2026-07-26.md) | `click-f01-only-r1` | 1 | Layer 1〜4の成立確認 |
| [`click control-free F01-only P1-b N=5`](click-control-free-f01-only-p1b-n5_2026-07-26.md) | `click-f01-only-r1` | 5 | 同一Bundle Aのbatch内分布 |
| [`click control-free F01-only P1-c N=5 B=3`](click-control-free-f01-only-p1c-n5-b3_2026-07-26.md) | `click-f01-only-r1` | 15 | 同一Bundle Aのbatch間基準線 |
| [`click control-free F02-only N=3`](click-control-free-f02-only-n3_2026-07-26.md) | `click-f02-only-r1` | 3 | Bundle Aの追加case成立確認 |
| [`click control-free Std14 N=5`](click-control-free-standard14-n5_2026-07-26.md) | `click-standard14-r1` | 70 | Bundle AのClick標準14 baseline |

resultはwrite-onceで、revisionによる上書きをしない。別instanceのresultを同一比較へ入れない。F01、F02、各追加caseのtargeted resultはset / rating revisionが異なるため同一comparisonへ混ぜない。Std14 resultはBundle A自身のbaselineであり、Bundle間比較、採用、release、runtime projectionを示さない。

# CLICK-F06-RESTORE-ECHO-COLOR-REGRESSION r1

`test_echo_color_flag`をstandard streamへ対するTTY/default color contractとして復元するtest-only caseである。

- seed origin: `c52f43c8ba734545b222af36ac35d87579031870`のtest差分を反転
- seed patch SHA-256: `f283dda18fc0cd45b5b31905343720a298e9991fc14c7e5f6ce29085dfd97050`
- seeded fixture commit/tree: `c2403d312eaee47b4501e89563f4ee26f97982a0` / `e9bcfe47e4736385c8f8f199def1d191957e98e3`
- seed後focused gate: `1 passed`（欠落regressionはgateだけでは検出されない）

Bundle AのN=3とStd14 N=5を全件score `4`で完了した（一次結果: [`click Std14 N=5`](../../../results/click-control-free-standard14-n5_2026-07-26.md)）。

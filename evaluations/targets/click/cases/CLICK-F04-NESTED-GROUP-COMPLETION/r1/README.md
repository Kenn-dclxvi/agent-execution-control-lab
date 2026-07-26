# CLICK-F04-NESTED-GROUP-COMPLETION r1

入れ子Groupのshell completionで現在contextを追跡し、呼出元から見える候補を復元するcaseである。

- target commit/tree: `00e592cea702e0b2caa0dee42489fdb1c22cd845` / `c6aa87f15f2e44a6fcab33714e1eb91e2552d816`
- seed origin commit: `ac6a2acfdb4550c35ce69ce54db502ba96c96324`のproduction差分を反転
- seed patch SHA-256: `674add2a516f6e85c6d15b011b906516024679badf1f35c407895d64b11428f9`
- seeded fixture commit/tree: `1ad909c16987662bb240d58dc44d284e0fb496a2` / `a340c32c44c3deaca3ba9ab3aa39d83107edfe38`

seed後のfocused gateは`4 failed, 2 passed`である。workerへ渡すのは`trial-prompt-input.json`だけとする。

Bundle AのN=3とStd14 N=5を全件score `4`で完了した（一次結果: [`click Std14 N=5`](../../../results/click-control-free-standard14-n5_2026-07-26.md)）。これは採用、release、本体反映を意味しない。

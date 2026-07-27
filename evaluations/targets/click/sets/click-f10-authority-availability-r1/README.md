# click-f10-authority-availability-r1

`CLICK-F10-COMMAND-API-INVENTORY/r2`だけを、No-AGENTSとRepository Authorityの
2条件、Medium、`N=5`、`M=24`で評価するauthority availability比較setである。

THE-CAPTIONのControlFreeGeneric / ControlFreeRepository F10と同じく、authority
本文なしではsource-only推論へ進まず停止し、本文ありではauthorityとsourceを直接
照合してinventoryを完了する経路を測る。既存Std14へは混ぜない。

2026-07-27に両条件各5件を完了した。No-AGENTSはscore `1 = 5`、Repository
Authorityはscore `4 = 5`で、excluded attemptは両条件0件だった。一次結果は
[`Click No-AGENTS / Repository Authority Medium F10 N=5`](../../results/click-no-agents-repository-authority-reasoning-medium-f10-authority-n5_2026-07-27.md)を正本とする。

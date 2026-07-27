# CLICK-F10-COMMAND-API-INVENTORY r2

repository sub `AGENTS.md`のavailabilityを直接測るread-only、zero-drift caseである。

r1はsourceだけからcommand構築APIを一覧化できたため、sub instruction本文を必要と
しなかった。r2はTHE-CAPTIONのF10 authority経路と同じく、`src/AGENTS.md`を
repository authorityとして明示し、authorityが存在しない、空、またはsourceと矛盾
する場合はinventoryを開始せず停止する。

No-AGENTSとRepository Authorityの2条件を、Medium、N=5、M=24で比較する。
既存r1、Std14 result、sub-AGENTS配置・露出resultは変更しない。

2026-07-27に評価を完了した。No-AGENTSは5 / 5件がscore `1`で
`authority_unavailable`停止、Repository Authorityは5 / 5件がscore `4`で
inventoryを完了した。一次結果は[`Click No-AGENTS / Repository Authority Medium F10 N=5`](../../../results/click-no-agents-repository-authority-reasoning-medium-f10-authority-n5_2026-07-27.md)を正本とする。

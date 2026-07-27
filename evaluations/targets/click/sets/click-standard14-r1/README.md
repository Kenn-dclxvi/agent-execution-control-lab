# click standard14 第1版

Bundle AのClick標準14項目baselineを確立する固定setである。F01、F02、F03、F04、F05、F05-OS、F06、F07 r2、F07-P r3、F08、F10、F10-R、A01、A02の14 caseを含む。

- set_id / revision: `click-standard14-r1` / `r1`
- Case / N / B / M: `14 / 5 / 1 / 24`
- prompt: `click-00e592c-control-free-r1`（Bundle A）
- model: `gpt-5.6-sol`
- reasoning: 完了済みBundle A / B profileは`high`。2026-07-27以降の新規通常比較profileは`medium`
- runtime identity: `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952`
- rating: `click-outcome-abstract-condition-preserving-v10`

この実行はBundle A自身のbaseline確立であり、Bundle B、採用、release、runtime projectionを意味しない。

## 評価状態

2026-07-26に`high`で70 / 70件をvalid・rateableとして登録し、全件score `4`だった。一次結果は[`click control-free Std14 N=5`](../../results/click-control-free-standard14-n5_2026-07-26.md)を正本とする。

2026-07-27に今後の通常比較基準となる`medium`も70 / 70件をvalid・rateableとして登録し、全件score `4`だった。一次結果は[`click control-free Medium Std14 N=5`](../../results/click-control-free-reasoning-medium-standard14-n5_2026-07-27.md)を正本とする。

同じMedium互換条件でC81全文のBundle Bも70 / 70件・全件score `4`として登録した。Bundle A比token中央値`-28.79%`、elapsed中央値`-12.62%`であり、比較結果は[`Click Control-Free / C81全文 Medium Std14 N=5`](../../results/click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md)を正本とする。

同じMedium互換条件でtarget-local No-AGENTSとRepository sub-AGENTSも各70 / 70件・全件score `4`として登録した。sub-AGENTS側はtoken中央値`+3.74%`、elapsed中央値`+7.90%`だったが、sub本文の初期context注入は0 / 70件だった。比較結果と解釈境界は[`Click No-AGENTS / Repository sub-AGENTS Medium Std14 N=5`](../../results/click-no-agents-repository-subagents-reasoning-medium-standard14-n5_2026-07-27.md)を正本とする。

setのcaseとrevisionはreasoning変更で上書きしない。`medium`は別profileと別compatibility keyで新規実行し、既存`high` resultへ混ぜない。

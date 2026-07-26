# click F03-only 第1版

## 結論

Phase 2のcase追加確認に使うsetである。`CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP`の1 caseだけを含む。

このsetは**標準setではない**。F03だけを`N=3`で確認し、F01/F02を再実行しない。

## 構成

| 区分 | 評価項目 | 版 |
| --- | --- | --- |
| F | [`CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP`](../../cases/CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP/r1/README.md) | `r1` |

- set_id: `click-f03-only-r1`
- revision: `r1`

## 固定する境界

- prompt setはBundle A `click-00e592c-control-free-r1`へ固定する。
- Case=1、`N=3`、`B=1`、`M=24`とする。
- 他caseのresultと混ぜない。
- Bundle BはBundle Aの標準14項目baseline確立後まで作成しない。

## 状態

fixture qualification済み、Bundle A評価前である。

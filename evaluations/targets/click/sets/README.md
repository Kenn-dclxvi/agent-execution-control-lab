# click sets

target instance `click`のevaluation setを置く。標準setは14項目のcoverageを縮小せずに構成する。set revisionは固定し、既存revisionを上書きしない。

repository側が正本として持つのはset定義である。実行時の`set.json`とfixture実体は検証root側へ`freeze-set`が生成する。

## 現在のset

| set_id | 版 | case数 | 用途 | 状態 |
| --- | --- | ---: | --- | --- |
| [`click-f01-only-r1`](click-f01-only-r1/README.md) | `r1` | 1 | Phase 1のばらつき測定 | P1-a〜P1-c完了（3 batch、15 / 15 score 4） |
| [`click-f02-only-r1`](click-f02-only-r1/README.md) | `r1` | 1 | Phase 2の追加case確認 | N=3完了（3 / 3 score 4） |
| F03 / F04 / F05 / F05-OS / F06の各only set | `r1` | 各1 | Phase 2の追加case確認 | 各N=3完了（各3 / 3 score 4） |
| `click-f07-only-r1` | `r1` | 1 | command evidence失敗履歴 | 未rating |
| [`click-f07-only-r2`](click-f07-only-r2/README.md) | `r2` | 1 | Phase 2の追加case確認 | N=3完了（3 / 3 score 4） |
| `click-f07-p-only-r1` / `r2` | `r1` / `r2` | 各1 | runtime command失敗履歴 | 各N=3完了（各3 / 3 score 3） |
| [`click-f07-p-only-r3`](click-f07-p-only-r3/README.md) | `r3` | 1 | Phase 2の追加case確認 | N=3完了（3 / 3 score 4） |
| F08 / F10 / F10-R / A01 / A02の各only set | `r1` | 各1 | Phase 2の追加case確認 | 各N=3完了（各3 / 3 score 4） |
| [`click-standard14-r1`](click-standard14-r1/README.md) | `r1` | 14 | Bundle A baseline | N=5完了（70 / 70 score 4） |
| [`click-f10-authority-availability-r1`](click-f10-authority-availability-r1/README.md) | `r1` | 1 | No-AGENTS / Repository Authority targeted比較 | N=5 × 2条件完了（score 1 × 5 / score 4 × 5） |
| [`click-standard14-r2`](click-standard14-r2/README.md) | `r2` | 14 | F10 r2を含むauthority availability全体比較 | N=5 × 4条件完了（authorityなし2条件はscore 4 × 65 + score 1 × 5、あり2条件はscore 4 × 70） |

only setは標準setの完了を単独では示さない。標準14項目の一次結果は[`click control-free Std14 N=5`](../results/click-control-free-standard14-n5_2026-07-26.md)を正本とする。

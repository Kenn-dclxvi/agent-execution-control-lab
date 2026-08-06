# click set index

`click` target instanceのEvaluation set revisionを引くための索引である。set revisionとmembershipの更新規則は[`../AGENTS.md`](../AGENTS.md)を正本とし、case membershipは各set artifactを正とする。状態列は索引用の要約であり、scoreと実測値は[`results/`](../results/README.md)の一次resultを正とする。

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

only setの完了を標準set全体の完了と読み替えない。標準14項目baselineの一次resultは[`click control-free Std14 N=5`](../results/click-control-free-standard14-n5_2026-07-26.md)を参照する。

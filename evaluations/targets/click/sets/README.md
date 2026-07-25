# click sets

target instance `click`のevaluation setを置く。標準setは14項目のcoverageを縮小せずに構成する。set revisionは固定し、既存revisionを上書きしない。

repository側が正本として持つのはset定義である。実行時の`set.json`とfixture実体は検証root側へ`freeze-set`が生成する。

## 現在のset

| set_id | 版 | case数 | 用途 | 状態 |
| --- | --- | ---: | --- | --- |
| [`click-f01-only-r1`](click-f01-only-r1/README.md) | `r1` | 1 | Phase 1のばらつき測定 | 未実行 |

標準14項目相当のsetは未作成である。このsetの結果を全体試験完了として扱わない。

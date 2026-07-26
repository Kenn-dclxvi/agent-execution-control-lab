# click F02-only 第1版

## 結論

Phase 2のcase追加確認に使うsetである。`CLICK-F02-STREAM-DEPRECATION-CONTRACT`の1 caseだけを含む。

このsetは**標準setではない**。F02を追加した時点で、その追加caseだけ`N=3`としてfixture、rating、実行経路の成立を確認する。F01を再実行せず、この結果を14項目全体へ一般化しない。

## 構成

| 区分 | 評価項目 | 版 |
| --- | --- | --- |
| F | [`CLICK-F02-STREAM-DEPRECATION-CONTRACT`](../../cases/CLICK-F02-STREAM-DEPRECATION-CONTRACT/r1/README.md) | `r1` |

- set_id: `click-f02-only-r1`
- revision: `r1`

## 固定する境界

- prompt setはBundle A [`click-00e592c-control-free-r1`](../../prompts/baselines/click-00e592c-control-free-r1/manifest.json)へ固定する。
- Case=1、`N=3`、`B=1`、`M=24`とする。
- F01-only resultと同一resultへ混ぜない。
- caseまたはrating contractを変更する場合は、このset revisionを上書きしない。
- Bundle BはBundle Aの標準14項目baseline確立後まで作成しない。

## Layer 1でのmaterialize

repository側が正本として持つのはこの定義だけである。実行時の`set.json`とfixture実体は検証root側へ`freeze-set`が生成する。

- `payload.trial_prompt_input`はcase revisionの`trial-prompt-input.json`をそのまま渡す。
- fixtureは`scripts/prepare_case_fixture.py`で生成する。
- fixture生成元は`/Users/kenn/repos/click`、target commitは`00e592cea702e0b2caa0dee42489fdb1c22cd845`である。

## 状態

fixture qualificationとBundle Aの`N=3`を完了した。3 / 3件がvalid・rateableで全件score `4`、all-agent token中央値`303,563`、elapsed中央値`130.225`秒だった。一次結果は[`click control-free F02-only N=3`](../../results/click-control-free-f02-only-n3_2026-07-26.md)とする。

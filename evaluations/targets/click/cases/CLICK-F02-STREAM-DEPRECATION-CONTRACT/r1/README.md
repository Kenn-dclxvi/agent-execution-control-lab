# CLICK-F02-STREAM-DEPRECATION-CONTRACT r1

## 目的

複数source fileをまたぐ公開・非公開API contractを復元するcaseである。`the-caption`側の[`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND`](../../../../../cases/TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1/README.md)と同じ判断点（multi-file scopeとcross-layer contract）をカバーする。

seedは`click`と`click.utils`のdeprecated stream accessorと内部private helperの分離を崩す。修復には`src/click/__init__.py`と`src/click/utils.py`の層間整合が必要である。

## Identity

- revision: `r1`
- target: `pallets/click`
- target commit: `00e592cea702e0b2caa0dee42489fdb1c22cd845`
- target tree: `c6aa87f15f2e44a6fcab33714e1eb91e2552d816`
- seed origin commit: `051725fa7e0c69effc9107066d8791c5b99242c3`（2026-07-17 "Add tests to deprecations. Better deprecate streams."）
- seed patch SHA-256: `b760c8bb93dc0e66ef10e6c56826c61b4b15ffce7767e0f164dfdc8e41e70a44`（2 fileの機能部分だけ）
- trial input SHA-256: `bd0440860fadc391364d6e626507c8cb0618c95df0fdccd551d0707d9e4cf549`
- seeded fixture commit: `22658fdca1a2166cecd534e15bb6dfd773a0ad13`
- seeded fixture tree: `bd4f81dc358bd7cbb8d3441e69bccb094b59f0e1`

workerへ渡すのは`trial-prompt-input.json`だけである。private data、seed、oracle、graderはmodel-invisibleとする。

## seedの効果（実測）

| 条件 | 結果 |
| --- | --- |
| seed適用前 focused gate | `72 passed, 1 skipped` |
| seed適用前 full gate | `1939 passed, 25 skipped, 31000 deselected, 1 xfailed` |
| seed適用後 focused gate | `2 collection errors` |
| seed適用後 full gate | `2 collection errors, 31000 deselected` |

seed後は`click.utils._get_binary_stream`が存在せず、`tests/test_deprecations.py`と`tests/test_testing.py`のcollectionで決定的に検出される。

## gate

focused gateは`tests/test_deprecations.py tests/test_testing.py`、full gateは全体である。いずれもrepository rootをcwdとし、`PYTHONPATH=src`を付ける。

## qualification

qualification receipt作成時のstatusは`fixture_qualified_prompt_not_evaluated`である。固定target identity、2 preimage、patch、2 post-seed identity、固定seed commitを照合し、2回materializeして同じfixture commit / treeになることを確認した。

その後、Bundle AのF02-only `N=3`を実行し、3 / 3件がscore `4`だった（正本: [`click control-free F02-only N=3`](../../../results/click-control-free-f02-only-n3_2026-07-26.md)）。qualificationと評価は別gateであり、採用済み、release済み、本体反映済みを意味しない。

# CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP r1

## 目的

例外を含むcontext終了時の後始末を復元するcaseである。`the-caption`側の`TC-F03-ATOMIC-CONTEXT-CLEANUP`と同じ判断点（cleanup、filesystem state、許可path限定）をカバーする。

seedは`CliRunner.isolated_filesystem()`から、自動生成した一時directoryの削除だけを除く。cwd復元と、呼出元指定の`temp_dir`を保持する既存contractは残す。

## Identity

- revision: `r1`
- target: `pallets/click`
- target commit: `00e592cea702e0b2caa0dee42489fdb1c22cd845`
- target tree: `c6aa87f15f2e44a6fcab33714e1eb91e2552d816`
- seed origin: target実装のcleanup blockを最小反転
- seed patch SHA-256: `2d457607ed330090562bb843ec53b2bf8806ae29cd2e0c3352bdaa9d0b9b39aa`
- seeded fixture commit: `251193d615cc1c3396ed3b97731948ada78e7cbf`
- seeded fixture tree: `cecb87bfb6d5b86a411da26a55e8214011592362`

workerへ渡すのは`trial-prompt-input.json`だけである。private data、seed、oracle、graderはmodel-invisibleとする。

## seedの効果（実測）

focused gateは`1 failed, 1 passed`となり、context終了後も自動生成directoryが残る。full gateは`1 failed, 1938 passed, 25 skipped, 31000 deselected, 1 xfailed`だった。seed前の対象testは`1 passed`である。

## gate

focused gateは`test_isolated_runner`と`test_isolated_runner_custom_tempdir`、full gateは全体である。repository rootをcwdとし、`PYTHONPATH=src`を付ける。

## qualification

固定identity、preimage、patch、postimage、seeded commit/treeを照合し、2回materializeして同一になることを確認した。qualification receipt作成時のstatusは`fixture_qualified_prompt_not_evaluated`である。その後、Bundle AのN=3とStd14 N=5を全件score `4`で完了した（一次結果: [`click Std14 N=5`](../../../results/click-control-free-standard14-n5_2026-07-26.md)）。qualificationと評価は別gateである。

# CLICK-F01-ANSI-SEQUENCE-STRIP r1

## 目的

単一fileのsource実装で、失われた不変条件を既存testの範囲内で復元するcaseである。`the-caption`側の[`TC-F01-DOMAIN-DUPLICATE-ASSET-KEY`](../../../../../cases/TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r3/README.md)と同じ判断点（単一fileのsource実装、不変条件の復元）をカバーする。

seedは`src/click/_compat.py`の`_ansi_re`を、ECMA-48のCSI sequence全体を対象とする表現から、SGRだけを拾う不完全な旧表現へ戻す。

## Identity

- revision: `r1`
- target: `pallets/click`
- target commit: `00e592cea702e0b2caa0dee42489fdb1c22cd845`
- target tree: `c6aa87f15f2e44a6fcab33714e1eb91e2552d816`
- seed origin commit: `71f2bafa541e7f798834e74076786ff4281ac83e`（2026-07-01 "Strip all ANSI sequences"）
- seed patch SHA-256: `936011b15e6e26277581302507a7bc724c7f868043d127e1cf89c8d8c81f4660`（17行、1 file）
- trial input SHA-256: `b70b4df8665da9a9c93145b5f17794c2d371ebc195e4533ba399b2829c093f1e`
- seeded fixture commit: `ed2d1f785a33e5bb55a5da058505ff8a11e8d875`
- seeded fixture tree: `0d09da148dcdbf9f7302d44d94ea1f0c823b54ac`

workerへ渡すのは`trial-prompt-input.json`だけである。private data、seed、oracle、graderはmodel-invisibleとする。

## seedの効果（実測）

| 条件 | 結果 |
| --- | --- |
| seed適用前（target commit） | `1939 passed, 25 skipped, 1 xfailed` |
| seed適用後 focused gate | `30 failed, 250 passed` |
| seed適用後 full gate | `30 failed, 1909 passed, 25 skipped, 1 xfailed` |

失敗は`tests/test_compat.py`と`tests/test_utils/test_style.py`の2 fileに閉じる。

## gate

focused gateは`tests/test_compat.py tests/test_utils/test_style.py`、full gateは全体である。実行条件を2つ固定する。

- **repository rootをcwdとして実行する。** cwd外で実行すると、seedと無関係に`tests/test_utils/test__expand_args.py::test_expand_args`が失敗する（実測: [`docs/public-target-selection-phase0.md`](../../../../../../docs/public-target-selection-phase0.md)）。
- **`PYTHONPATH=src`を付ける。** 共有runtimeは`venv_shim`で共有purelibを`.pth`追加するだけでworkspaceの`src`を通さない。付けない場合、`tests/test_deprecations.py`が`importlib.metadata`の`PackageNotFoundError`でcollection errorになる。固定方法は[`profiles/README.md`](../../../profiles/README.md)を正本とする。

## qualification

qualification receiptは`fixture_qualified_prompt_not_evaluated`である。`scripts/prepare_case_fixture.py`で4回materializeし、いずれも同一の`fixture_head_commit`と`fixture_head_tree`になることを確認した。4回目は永続local clone（`/Users/kenn/repos/click`）を`--source-repo`に使い、一時cloneと同じfixture identityになることを確認した。

qualification receipt作成時点ではprompt未評価だった。その後、Bundle AでP1-a〜P1-cとStd14を完了した（一次結果: [`click Std14 N=5`](../../../results/click-control-free-standard14-n5_2026-07-26.md)）。fixture qualificationと評価は別gateであり、採用済み、release済みを意味しない。

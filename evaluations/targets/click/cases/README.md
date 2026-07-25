# click cases

target instance `click`のcase artifactを置く。1 case revisionごとに`README.md`、`trial-prompt-input.json`、`private/`（`seed.patch`と`case-data.json`）を持つ。

カバーすべき判断点と元caseの対応は[`docs/public-target-selection-phase0.md`](../../../../docs/public-target-selection-phase0.md)の「14項目のcoverage対応」を正本とする。case追加手順は[`evaluations/cases/README.md`](../../../cases/README.md)の追加順序に従う。

## 現在のcase

| case | 元case | 主なvariation | 状態 |
| --- | --- | --- | --- |
| [`CLICK-F01-ANSI-SEQUENCE-STRIP/r1`](CLICK-F01-ANSI-SEQUENCE-STRIP/r1/README.md) | F01 | 単一fileのsource実装、不変条件の復元 | `fixture_qualified_prompt_not_evaluated` |

残り13項目のcaseは未作成である。標準setは14項目のcoverageを縮小せずに構成する。

## 実測で確定した共通条件

- gate commandは**repository rootをcwdとして実行する**。cwd外実行では`tests/test_utils/test__expand_args.py::test_expand_args`がseedと無関係に失敗する。
- seedは2026-05-01以降のcommitから選び、`src/`部分だけの逆patchとして固定する。逆patchが現在のtarget commitへ当たること（後続commitで同じ箇所が変更されていないこと）を`git apply --check`で確認する。
- seed patchは純粋なdiffだけを保存する。`git show`のheaderはcommit messageを含み、修正内容がoracleとして漏れるため除去する。

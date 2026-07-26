# click F01-only 第1版

## 結論

Phase 1のばらつき測定に使う最小setである。`CLICK-F01-ANSI-SEQUENCE-STRIP`の1 caseだけを含む。

このsetは**標準setではない**。標準setは14項目のcoverageを縮小せずに構成する（正本: [`docs/public-target-selection-phase0.md`](../../../../../docs/public-target-selection-phase0.md)の「14項目のcoverage対応」）。このsetはPhase 1で測定の成立とばらつきを確認する目的に限定し、prompt比較の結論へ使わない。

## 構成

| 区分 | 評価項目 | 版 |
| --- | --- | --- |
| F | [`CLICK-F01-ANSI-SEQUENCE-STRIP`](../../cases/CLICK-F01-ANSI-SEQUENCE-STRIP/r1/README.md) | `r1` |

- set_id: `click-f01-only-r1`
- revision: `r1`

## 固定する境界

- このsetの結果を標準14項目の全体試験完了として扱わない。
- 1 caseまたは少数反復の結果を評価範囲外へ一般化しない。
- caseの版を変更する場合はこのsetを上書きせず、新しいset revisionを作る。
- 14項目へ拡張する際もこのsetを書き換えず、別のset_idとして固定する。
- setへcaseを追加する根拠は、既存setでは観測できないcontrol pathがある場合に限る（正本: [`docs/future-roadmap.md`](../../../../../docs/future-roadmap.md)の「評価setの役割と育て方」）。

## Layer 1でのmaterialize

repository側が正本として持つのはこの定義だけである。実行時の`set.json`とfixture実体は検証root側へ`freeze-set`が生成する（形式: [`docs/evaluation-loop-manual.md`](../../../../../docs/evaluation-loop-manual.md)の「Evaluation set source」）。

- 各caseの`payload.trial_prompt_input`は、case revisionの`trial-prompt-input.json`をそのまま渡す。
- fixtureは`scripts/prepare_case_fixture.py`で生成する。CLICK-F01のfixtureは3回materializeして同一commit / treeになることを確認済みである。
- fixture生成元は`pallets/click`のlocal cloneで、target commitは`00e592cea702e0b2caa0dee42489fdb1c22cd845`である。

## Phase 1での使い方

`M`は指定がない限り24へ固定する。段階ごとのCase / N / B / Mは[`docs/public-target-selection-phase0.md`](../../../../../docs/public-target-selection-phase0.md)の「Phase 1の実行設定」を正本とする。

| 段階 | Case | N | B | M | 実行回数 |
| --- | ---: | ---: | ---: | ---: | ---: |
| P1-a 成立確認 | 1 | 1 | 1 | 24 | 1 |
| P1-b batch内ばらつき | 1 | 5 | 1 | 24 | 5 |
| P1-c batch間ばらつき | 1 | 5 | 3 | 24 | 15 |

いずれの段階もprompt setは[`click-00e592c-control-free-r1`](../../prompts/baselines/click-00e592c-control-free-r1/manifest.json)のまま変えない。prompt比較はPhase 2以降で行う。

## 状態

P1-aは1 / 1件がvalid・rateableでscore `4`だった。一次結果は[`click control-free F01-only P1-a N=1`](../../results/click-control-free-f01-only-p1a-n1_2026-07-26.md)とする。P1-bとP1-cは未実施であり、ばらつきはまだ評価していない。

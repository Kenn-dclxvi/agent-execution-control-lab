# holdout reference panel r1 結果

## 結論

固定済み`attempt-r2`から独立AI grader 3件を一度だけ同時発行した。3件すべて有効で、32 assertionすべてが3者一致した。不一致、`unknown`および`not_applicable`は0件だったため、panel外裁定を発行せず、`general-chat-semantic-qualification-reference-r1`をsealした。

この結果はholdout referenceの成立だけを意味する。資格graderはまだ実行しておらず、grader適格性、正式評価、r2有効化、prompt採用、releaseまたはprojectionは未決定である。

## 実行identity

- run ID: `general-chat-semantic-holdout-reference-r1-run-r1`
- result content identity: `53f131daec73b8d31e0efb243858ab35383ff9692c52a70287f803e77a80a4a3`
- `run-result.json` file SHA-256: `60b34a7ecba1827fc9c7d0c51430b7e2375f60325e6b65d02cc019bbacb428da`
- `reference-panel-report.json` file SHA-256: `3a4e432384e39f7b4e5e32af95a297c32c64b7208d811b86c40677bf280d86af`
- external run root: `/Users/kenn/repos/_verification/general-chat-response-control/semantic-holdout-reference-r1-attempt-r2`
- runtime: `codex-cli 0.148.0`
- model: `gpt-5.6-terra`
- reasoning: `medium`

## slot結果

| execution ID | 状態 | 経過秒 | total tokens |
|---|---:|---:|---:|
| `semantic-holdout-reference-terra-r1-run-1` | `valid` | `55.007814` | `20466` |
| `semantic-holdout-reference-terra-r1-run-2` | `valid` | `52.677866` | `20318` |
| `semantic-holdout-reference-terra-r1-run-3` | `valid` | `52.651867` | `20273` |

3件の合計は`61057` tokensである。process external failureとunrateable resultはいずれも0件だった。

## reference結果

- assertion count: `32`
- 3者一致: `32`
- 不一致: `0`
- `pass`: `19`
- `fail`: `13`
- `unknown`: `0`
- `not_applicable`: `0`
- reference type: `multi_grader_consensus_reference`
- human alignment: `unmeasured`
- adjudication required: `false`

seal済みreferenceは[`qualification-reference-r1.json`](../calibration/qualification-reference-r1.json)を正本とする。全labelは外部のconsensus reportと完全一致し、16回答、32 assertionを重複なく覆うことを機械確認した。

## 次の境界

次に許可するのは、seal済みholdoutとreferenceを別管理し、reference labelを入力へ渡さない資格grader一件の発行前preflightである。資格graderの実行回数は`1`のまま維持する。

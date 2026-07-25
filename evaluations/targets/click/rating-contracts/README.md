# click rating contracts

target instance `click`のquality rating contractを置く。

rating contractは`boundary_rules`と`case_quality_rules`をcase ID単位で内包するためinstance固有であり、`the-caption`側のcontractを流用しない。

## 現行contract

| contract_id | schema | contract SHA-256 | 対象case |
| --- | --- | --- | --- |
| [`click-outcome-abstract-condition-preserving-v1`](click-outcome-abstract-condition-preserving-v1.json) | `the-caption-prompt.quality-rating-contract/v13` | `7057dd0790a62a636f7de4b389d2f3e8526c4b578819842472d92ff49a93747d` | `CLICK-F01-ANSI-SEQUENCE-STRIP` |

`the-caption`側の[`outcome-abstract-condition-preserving-owner-diagnostic-v13`](../../../rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json)と同じschemaを使い、instance非依存の節（`quality_score_rule`、`command_evidence`、`producer_evidence`）は同じ規則を保つ。instance固有に変えたのは次の4点である。

- `case_quality_rules`は`CLICK-F01-ANSI-SEQUENCE-STRIP`だけを持つ。`boundary_rules`は対象caseがないため空にする。
- `command_evidence.working_directory_contract`を追加した。必須gateはrepository rootをcwdとして実行し、cwd外実行はseedと無関係な失敗を生むため計測失敗として扱う（実測: [`docs/public-target-selection-phase0.md`](../../../../docs/public-target-selection-phase0.md)）。
- `rater_input.forbidden`へ「seedの由来commitと参照実装の内容」を追加した。clickのseedは公開commitの逆patchであり、由来commitを見ればreference postimageが判明するため、raterへ渡さない。
- `diagnostic_observations`から`the-caption`固有の観測項目（F10 Monthlyの数値line状態）を外し、cwd観測を加えた。

## kernelへの登録

`scripts/evaluation_loop.py`の`SUPPORTED_QUALITY_RATINGS`へ`QUALITY_RATING_CLICK_V1`として登録済みである。この登録が持つのは`contract_id`、contract SHA-256、collector schema版、owner-producer policyだけで、case IDやtarget pathを含まない。[`evaluations/AGENTS.md`](../../../AGENTS.md)が禁じるのはkernelへのtarget固有path、case ID、分岐であり、許可リストへの登録はこれに当たらない。

## revision規則

contractを変更する場合は既存fileを上書きせず、新しい`contract_id`のfileを追加して`target.json`の`current_rating_contract`を切り替える。過去resultを新contractで再採点しない。

# click rating contracts

target instance `click`のquality rating contractを置く。

rating contractは`boundary_rules`と`case_quality_rules`をcase ID単位で内包するためinstance固有であり、`the-caption`側のcontractを流用しない。

## 現行contract

| contract_id | schema | contract SHA-256 | 対象case |
| --- | --- | --- | --- |
| [`click-outcome-abstract-condition-preserving-v1`](click-outcome-abstract-condition-preserving-v1.json) | `the-caption-prompt.quality-rating-contract/v13` | `7057dd0790a62a636f7de4b389d2f3e8526c4b578819842472d92ff49a93747d` | `CLICK-F01-ANSI-SEQUENCE-STRIP`（履歴） |
| [`click-outcome-abstract-condition-preserving-v2`](click-outcome-abstract-condition-preserving-v2.json) | `the-caption-prompt.quality-rating-contract/v13` | `9f09b4230e19497bb752f77ef8a22b006fc505aa216a4575b2bff3eeaf143f80` | F01〜F02（履歴） |
| [`click-outcome-abstract-condition-preserving-v3`](click-outcome-abstract-condition-preserving-v3.json) | `the-caption-prompt.quality-rating-contract/v13` | `0d165083c8629223f71aa7a53953a1d05ab90e36b99533ee7c0c1a60a53fd0a2` | F01〜F04（履歴） |
| [`click-outcome-abstract-condition-preserving-v4`](click-outcome-abstract-condition-preserving-v4.json) | `the-caption-prompt.quality-rating-contract/v13` | `e2316a51ab0e51d08191165155781d860b0219350be8f51c2e4583f630f49746` | F01〜F05-OS（履歴） |
| [`click-outcome-abstract-condition-preserving-v5`](click-outcome-abstract-condition-preserving-v5.json) | `the-caption-prompt.quality-rating-contract/v13` | `054335e43d386251b81040bae080430cbca2a85e60c96f6a7100e536242ed5ab` | F01〜F06（履歴） |
| [`click-outcome-abstract-condition-preserving-v6`](click-outcome-abstract-condition-preserving-v6.json) | `the-caption-prompt.quality-rating-contract/v13` | `d8fe38996cf270120977bb22f0434edb85de9040e4e5593b18481dddb69a78c4` | F01〜F07（履歴） |
| [`click-outcome-abstract-condition-preserving-v7`](click-outcome-abstract-condition-preserving-v7.json) | `the-caption-prompt.quality-rating-contract/v13` | `23458c2abc303f657265c8769268883bb659e34c1c499fc5a8e8d9b45e3137bb` | F01〜F07-P（履歴） |
| [`click-outcome-abstract-condition-preserving-v8`](click-outcome-abstract-condition-preserving-v8.json) | `the-caption-prompt.quality-rating-contract/v13` | `6be7e5816c764cd5651f6f9a89f3632da228fef659d3f34a98d7e54cd2ec7c8a` | F01〜F08（履歴） |
| [`click-outcome-abstract-condition-preserving-v9`](click-outcome-abstract-condition-preserving-v9.json) | `the-caption-prompt.quality-rating-contract/v13` | `acefd9f032146d6b685203bd38f19263b5189e69f5cd08119d7b62d2d1c42557` | F01〜A01（履歴） |
| [`click-outcome-abstract-condition-preserving-v10`](click-outcome-abstract-condition-preserving-v10.json) | `the-caption-prompt.quality-rating-contract/v13` | `ad5ca3b4ba526fe0fb9c9ec079231d5b7476335b00d540ff8cf67b9e95cd5929` | Click標準14項目（現行） |

`the-caption`側の[`outcome-abstract-condition-preserving-owner-diagnostic-v13`](../../../rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json)と同じschemaを使い、instance非依存の節（`quality_score_rule`、`command_evidence`、`producer_evidence`）は同じ規則を保つ。v2〜v10は既存境界を維持し、qualification済みcaseのruleだけを順次追加した。

- v1の`case_quality_rules`はF01だけ、現行v10はF01〜F10-Rの12 case ruleとA01 / A02の`boundary_rules`を持つ。
- `command_evidence.working_directory_contract`を追加した。必須gateはrepository rootをcwdとして実行し、cwd外実行はseedと無関係な失敗を生むため計測失敗として扱う（実測: [`docs/public-target-selection-phase0.md`](../../../../docs/public-target-selection-phase0.md)）。
- `rater_input.forbidden`へ「seedの由来commitと参照実装の内容」を追加した。clickのseedは公開commitの逆patchであり、由来commitを見ればreference postimageが判明するため、raterへ渡さない。
- `diagnostic_observations`から`the-caption`固有の観測項目（F10 Monthlyの数値line状態）を外し、cwd観測を加えた。

## kernelへの登録

`scripts/evaluation_loop.py`の`SUPPORTED_QUALITY_RATINGS`へv1〜v10を登録済みである。この登録が持つのは`contract_id`、contract SHA-256、collector schema版、owner-producer policyだけで、case IDやtarget pathを含まない。[`evaluations/AGENTS.md`](../../../AGENTS.md)が禁じるのはkernelへのtarget固有path、case ID、分岐であり、許可リストへの登録はこれに当たらない。

## revision規則

contractを変更する場合は既存fileを上書きせず、新しい`contract_id`のfileを追加して`target.json`の`current_rating_contract`を切り替える。過去resultを新contractで再採点しない。

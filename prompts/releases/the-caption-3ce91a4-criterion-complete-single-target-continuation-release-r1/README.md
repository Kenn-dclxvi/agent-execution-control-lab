# Candidate125リリース

## 結論

Candidate125を採用し、THE-CAPTIONへの投影を承認する。

リリース状態は`approved_for_projection`、承認状態は`approved`である。Candidate125と内容が同一のrelease snapshotであり、prompt本文は変更していない。

## 識別情報

- release identity: `the-caption-3ce91a4-criterion-complete-single-target-continuation-release-r1`
- source candidate: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`
- source candidate commit: `912ee3d2f80f5bedab3df8da52456823db91e829`
- bundle SHA-256: `60e95bfe7f9e09a0cbb2fb980c54f1cd1bd671c37509976e7e88574adf911435`
- content relation: Candidate125と同一内容
- Candidate125から変更したtarget: なし

## 採用根拠

- Standard14 N=5: 70 / 70件がscore `4`
- token中央値: `1,401,225`。Candidate107目標`1,523,137`比`-8.00%`
- elapsed中央値: `846.377秒`。Candidate107比`-10.48%`
- targeted F04: false stop 0 / 5件
- targeted F02: content wave 5 / 5件、token中央値`124,094`
- A02 N=20: 20 / 20件がscore `4`、implementation bind後・変更前再入0 / 20件

Candidate125は、C118のA02 terminal closureとStandard14品質を維持し、同じ固定executor条件でC107が示したtoken目標を下回った。C122で発生したF04の不完全content false stopも解消した。

## 未解決risk

- Candidate125のStandard14 B20は実施していない。Candidate81と同じ長期route stabilityを実測済みとは扱わない。
- C122比はtoken`-0.19%`、elapsed`+2.84%`であり、全KPI改善ではない。
- 品質・cost結果はRating v14、Medium、CLI `0.146.0`、固定Standard14 N=5の範囲に限定する。
- A02 N=20のterminal closure結果を他caseへ一般化しない。

2026-07-31のユーザーによる明示的な採用・THE-CAPTION展開依頼は、これらのriskを保持した別のlifecycle判断である。

## 状態

| lifecycle | state |
| --- | --- |
| evaluation | `standard14_evaluated / quality_gate_passed / a02_terminal_closure_passed / candidate107_token_target_passed` |
| adoption | `adopted` |
| release | `approved_for_projection` |
| approval | `approved` |
| runtime projection | `approved_for_projection / not_yet_projected` |

## 根拠

- [Candidate125採用判断](../../../docs/candidate125-adoption-decision.md)
- [Standard14・A02 N=20 result](../../../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)
- [Targeted result](../../../evaluations/results/candidate122-candidate125-criterion-complete-single-target-continuation-v14-medium-a01-a02-f01-f02-f04-atomic-n5-cli0146_2026-07-31.md)
- [Candidate125設計](../../../docs/candidate125-criterion-complete-single-target-continuation-design.md)
- [Candidate125 manifest](../../candidates/the-caption-3ce91a4-criterion-complete-single-target-continuation-r1/manifest.json)

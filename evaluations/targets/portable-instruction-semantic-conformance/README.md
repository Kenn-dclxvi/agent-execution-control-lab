# Portable instruction semantic conformance target

> **状態**: `registered / namespaced / transition_contract_r4_qualified / heldout_r3_n20_c147_score4_275_of_280 / heldout_r3_n20_portable_score4_280_of_280 / n20_token_regression / n20_elapsed_improvement / adoption_not_decided`

固定operation ledgerへ一回のJSON応答を返すsemantic protocolの評価インスタンスである。repository snapshotを対象とする既存targetとは別型であり、`target_repository_ref`を持たない。

| 領域 | 正本 | 状態 |
| --- | --- | --- |
| target | [`target.json`](target.json) | v2 semantic protocol targetとして登録済み |
| source binding | [`registration.json`](registration.json)、[`registrations/`](registrations/) | 旧登録bytesを維持し、新heldoutだけversioned registrationへbind |
| cases | [`cases/README.md`](cases/README.md) | r1履歴、r2設計不適格、現行r3を分離し、model-visible入力とprivate oracleを分離 |
| set | [`sets/README.md`](sets/README.md) | calibrationと独立heldoutを別identityで固定 |
| rating | [`rating-contracts/portable-instruction-semantic-exact-v1.json`](rating-contracts/portable-instruction-semantic-exact-v1.json) | exact集合rating |
| prompt | [`prompts/README.md`](prompts/README.md) | control-free、C147 full-agent reference、portable full-agent Candidateを別identityで登録 |
| runtime contracts | [`contracts/`](contracts/) | TaskSpec wrapper r1とtransition calibration r2〜r4、capability catalog、all-agent transcript accountingを固定 |
| profile | [`profiles/README.md`](profiles/README.md) | transition calibration、C147先行heldout、portable比較を分離 |
| dispatch | [`plans/README.md`](plans/README.md) | 旧runnerとversioned runner v2のpreflightを別hashで固定 |
| results | [`results/README.md`](results/README.md) | 全resultをappend-onlyで索引化 |

heldout r3のN=20ではC147が275 / 280、portableが280 / 280でScore 4・機序成立となった。portableはtoken合計が0.225%増え、elapsed合計が2.463%減ったため、cost改善は未判定である。Standard14はend-to-end正式評価として維持し、採用、releaseおよびruntime projectionは未判断である。

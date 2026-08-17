# Portable instruction semantic conformance target

> **状態**: `registered / namespaced / control_free_measurement_qualified / control_free_score4_5 / c147_reference_bundle_registered / reference_profile_not_created / portable_full_agent_candidate_issued_14 / candidate_valid_14 / candidate_score4_7 / candidate_quality_failed / formal_results_2`

固定operation ledgerへ一回のJSON応答を返すsemantic protocolの評価インスタンスである。repository snapshotを対象とする既存targetとは別型であり、`target_repository_ref`を持たない。

| 領域 | 正本 | 状態 |
| --- | --- | --- |
| target | [`target.json`](target.json) | v2 semantic protocol targetとして登録済み |
| source binding | [`registration.json`](registration.json) | commit `a544769`の固定bytesへbind済み |
| cases | [`cases/heldout-r1/`](cases/heldout-r1/) | PIC-H01〜PIC-H14、model-visible入力とprivate oracleを分離 |
| set | [`sets/heldout-r1/set.json`](sets/heldout-r1/set.json) | 14 Case固定 |
| rating | [`rating-contracts/portable-instruction-semantic-exact-v1.json`](rating-contracts/portable-instruction-semantic-exact-v1.json) | exact集合rating |
| prompt | [`prompts/README.md`](prompts/README.md) | control-free、C147 full-agent reference、portable full-agent Candidateを別identityで登録 |
| runtime contracts | [`contracts/`](contracts/) | TaskSpec wrapper、capability catalog、all-agent transcript accountingを固定 |
| profile | [`profiles/README.md`](profiles/README.md) | r4でschema transportとthread-bound一次tokenを固定、測定成立 |
| dispatch | [`plans/README.md`](plans/README.md) | control-free r4とportable Candidate r1を各14件発行 |
| results | [`results/README.md`](results/README.md) | control-free測定成立とportable Candidate quality gateの2件 |

control-free資格確認は測定成立だけを通過した。portable full-agent Candidateは14 / 14 validだったがscore 4は7 / 14でquality gateを通過しなかった。C147 reference Profileとrunは未発行であり、直接の効率比較は未判定である。採用、releaseおよびruntime projectionも未判断である。

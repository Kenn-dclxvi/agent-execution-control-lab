# Portable instruction semantic conformance target

> **状態**: `registered / namespaced / control_free_baseline_registered / codex_profile_r4_measurement_qualified / authorized_14 / issued_14 / valid_14 / score4_5 / mechanism_passed_5 / formal_results_1 / c147_reference_bundle_registered / portable_full_agent_candidate_bundle_registered / candidate_profile_registered / candidate_preflight_ready / candidate_issued_0`

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
| dispatch | [`plans/README.md`](plans/README.md) | r4の14スロットを発行、有効14件 |
| results | [`results/README.md`](results/README.md) | control-free資格確認1件 |

資格確認は測定成立だけを通過した。品質はscore 4が5/14、機序通過も5/14である。C147 referenceとportable full-agent Candidateの一枚bundleを登録し、Candidate Profileと14スロットのpreflightまで完了した。Candidate runは未発行である。portable kernelの効果、採用、releaseまたはruntime projectionは未判断である。

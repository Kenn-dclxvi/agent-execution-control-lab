# Portable instruction semantic conformance target

> **状態**: `registered / namespaced / control_free_baseline_registered / codex_profile_r4_measurement_qualified / dispatch_plan_fixed / profile_preflight_ready / authorized_14 / issued_14 / valid_14 / score4_5 / mechanism_passed_5 / formal_results_1`

固定operation ledgerへ一回のJSON応答を返すsemantic protocolの評価インスタンスである。repository snapshotを対象とする既存targetとは別型であり、`target_repository_ref`を持たない。

| 領域 | 正本 | 状態 |
| --- | --- | --- |
| target | [`target.json`](target.json) | v2 semantic protocol targetとして登録済み |
| source binding | [`registration.json`](registration.json) | commit `a544769`の固定bytesへbind済み |
| cases | [`cases/heldout-r1/`](cases/heldout-r1/) | PIC-H01〜PIC-H14、model-visible入力とprivate oracleを分離 |
| set | [`sets/heldout-r1/set.json`](sets/heldout-r1/set.json) | 14 Case固定 |
| rating | [`rating-contracts/portable-instruction-semantic-exact-v1.json`](rating-contracts/portable-instruction-semantic-exact-v1.json) | exact集合rating |
| prompt | [`prompts/baselines/portable-semantic-a544769-control-free-r1/`](prompts/baselines/portable-semantic-a544769-control-free-r1/) | 追加instruction 0 bytes |
| runtime contracts | [`contracts/`](contracts/) | TaskSpec wrapper、capability catalog、all-agent transcript accountingを固定 |
| profile | [`profiles/README.md`](profiles/README.md) | r4でschema transportとthread-bound一次tokenを固定、測定成立 |
| dispatch | [`plans/README.md`](plans/README.md) | r4の14スロットを発行、有効14件 |
| results | [`results/README.md`](results/README.md) | control-free資格確認1件 |

資格確認は測定成立だけを通過した。品質はscore 4が5/14、機序通過も5/14であり、portable kernelの効果、採用、releaseまたはruntime projectionは未判断である。

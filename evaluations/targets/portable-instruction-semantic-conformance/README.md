# Portable instruction semantic conformance target

> **状態**: `registered / namespaced / control_free_baseline_registered / codex_profile_registered_not_qualified / dispatch_plan_fixed / profile_preflight_ready / authorized_14 / issued_0 / qualification_not_started / formal_results_0`

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
| profile | [`profiles/README.md`](profiles/README.md) | Codex CLI 0.146.0 / GPT-5.6 Sol / reasoning medium / N=1を登録、未qualification |
| dispatch | [`plans/README.md`](plans/README.md) | 14スロットを固定、事前確認済み、発行0件 |
| results | [`results/README.md`](results/README.md) | 0件 |

target、Profile、計画または事前確認票の登録は評価済み、採用、releaseまたはruntime projectionを意味しない。実行入口は事前確認票に固定した14スロット以外を拒否し、現時点では一件も発行していない。

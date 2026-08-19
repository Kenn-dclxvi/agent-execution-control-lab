# P006 THE-CAPTION Standard14 N=5計測設計

> [!IMPORTANT]
> **状態**: `measurement_completed / result_registered / quality_gate_passed / p005_cost_both_lower / frontier_nonconformance_observed / independent_mechanism_gate_retracted / n20_eligible_not_started`

## 結論

P006 `p006-portable-full-agent-codex-frontier-carrier-r1`をStandard14 N=5で計測する。P005投影bundleの19 targetを配送surfaceとし、root `AGENTS.md`だけをP006の固定bytesへ置換する。P005の非root 18 target、Standard14、fixture、TaskSpec、oracle、Rating v14、model、reasoning、CLI、permission、runner、token accountingおよび集計方法は変更しない。

比較の主基準はP005 result `28082254ecc6447f8d76d63e85062299`とする。Candidate147 result `f7baeadc5bd44399ac13cc0e0a8aff48`はC147移植costの残量を見る副基準として保存済みresultだけを再利用する。P005またはC147を再実行しない。

## 固定条件

| 項目 | 固定値 |
| --- | --- |
| Evaluation set | `the-caption-standard14-r1` / `r1`、14 Case |
| 反復 | 各Case N=5、合計70 slot |
| model / reasoning | `gpt-5.6-sol / medium` |
| Agent/runtime | Codex CLI `0.146.0`、Python `3.14.5`、persisted、multi-agent有効、memories無効 |
| permission | `workspace-write / never` |
| 並列上限 | M=24、`global_queue` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| token | all-agent token accounting v1 |
| target | THE-CAPTION commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`、tree `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |

## prompt identity

- P006正本: `p006-portable-full-agent-codex-frontier-carrier-r1`
- P006 root SHA-256: `669a66d8350e250260922eb25706a11f0e75b5aeb1064ca323a62a9be26c5c91`
- Standard14投影: `p006-the-caption-standard14-projection-r1`
- 投影bundle SHA-256: `8ef34227c5affaa099bc7e25700829f017794d289f480c2d2a161b537e6d204b`
- 直接比較: P005投影bundle `bfee25ef8b710ec03d4c73d81aea7fc1fd16e558f4565fd5565990dea2d4c01b`

P005投影とP006投影の差はroot `AGENTS.md`一件だけであり、その差はP006の`FRONTIER_CARRIER_CODEX` 1,763 bytesだけとする。root以外18 targetはbyte、mode、symlink targetを一致させる。

## 発行前gate

1. P006正本と投影rootがbyte一致する。
2. P005投影とP006投影のtarget集合が一致し、root以外18 targetが完全一致する。
3. P005 resultから作るatomic poolがprompt identityだけを差し替え、既存run 0件、不足70件になる。
4. Candidate147保存Layer 1から作るcomparison cycleで、prompt identity以外の全互換条件が一致する。
5. `comparison-preflight.json`が`ready`で70 slotを許可し、発行済み0件を示す。

一項目でも不一致ならslotを発行しない。

## 成否と停止条件

- 70 / 70件についてvalidity、Score分布、all-agent `total_tokens`、`elapsed_seconds`を記録する。
- 有効な低品質runは再実行せず、品質分布へ保持する。
- P005比でtokensとelapsedがともに減ればcost改善方向とする。一方でも増えた場合は相殺せずcost退行としてtrace診断へ進む。
- `FRONTIER_CARRIER_CODEX`の狙いはaction前model再入を減らすことだが、model responseやtool waveは診断情報であり3 KPIへ追加しない。
- N=5を安定傾向へ一般化せず、N=20、採用、releaseまたはruntime projectionへ自動的に進めない。

## 実施結果

preflightはprompt identity以外の互換条件を照合して`ready`となり、70 slotを発行した。70 / 70件がvalidかつScore `4`で、registered resultは`684cb3c380bc4b28a65680f415ecb8e6`である。

P005比はtoken `-10.57%`、elapsed `-3.90%`、Candidate147比はtoken `+21.75%`、elapsed `+13.86%`だった。ただし、直接対象としたF08では5 / 5件で開始identity result後の別model responseから対象readを発行した。

N=5直後はこの経路を独立した機序gate不成立とした。後続再監査では、F08の分割はP005から既存の共通`FRONTIER`へ反するnonconformanceであり、P006差分が新しく閉じたpermission edgeを示せないと再分類した。機序と品質不成立の100%対応もないため、独立mechanism gateを撤回する。詳細は[`P006 frontier carrier結果後因果再監査`](p006-frontier-carrier-post-result-causal-reassessment.md)と[`P006 THE-CAPTION投影 Standard14 N=5評価`](../evaluations/results/p006-the-caption-standard14-projection-n5_2026-08-19.md)を正とする。

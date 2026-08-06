# THE-CAPTION 自律review routing 第2版

## 結論

r1のcase内容を保持し、evaluation prompt overlay後workspaceのcommit境界だけを修正したtargeted Evaluation setである。

- set ID / revision: `the-caption-autonomous-review-r2 / r2`
- case revision: 3件とも`r2-overlay-aware-seed-diff`
- runtime HEAD: prompt overlay commit
- seed commit: `HEAD^`
- target commit: `HEAD^^`
- review対象diff: `HEAD^^..HEAD^`
- comparison baseline: Candidate147
- rating / model / reasoning / CLI: v14 / GPT-5.6 Sol / Medium / `0.146.0`
- coverage: 3 case × N=5、profile `M=24`
- model run: C147 15 / 15 executor-valid、期待成果15 / 15、全run root-only。SA必要性は未実証、quality未採点・Layer 4未登録

## r1との不変条件

seed content、postimage、事前評価、canary、risk class、machine coverageの意味、当初の期待review route、期待dispositionは変更しない。r1のinvalid resultは履歴として保持し、r2へ混ぜない。当初の期待routeは試験作成時の仮説であり、r2結果の再解釈では成果に裏付けられた合否条件として扱わない。

## Case

| case | original route hypothesis | expected disposition |
| --- | --- | --- |
| AR01 defect / favorable prior | reviewer 1 | `blocked` |
| AR02 clean / negative prior | reviewer 1 | `completion_ready` |
| AR03 type-only / neutral prior | reviewer 0 | `completion_ready` |

## 発行前gate

prompt overlay適用後workspaceで、各caseの`HEAD^`と`HEAD^^` identity、非空source diff、AST parse、`git diff --check HEAD^^..HEAD^`、clean statusを機械確認する。一項目でも不一致ならmodel slotを発行しない。

## C147 root-only診断結果

C147はAR01 / AR02のexpected dispositionを10 / 10で正しく返した。AR03も5 / 5で正しく完了した。全15 runはroot-onlyで、独立SAは起動されなかった。

root-only成果が15 / 15で成立したため、SA未起動だけを失敗とは判定しない。[root-only診断](../../results/candidate147-autonomous-review-r2-root-only-diagnostic_2026-08-04.md)に従い、状態を`root_only_outcome_verified / SA_necessity_not_demonstrated / information_blocking_benefit_not_evaluated / quality_not_rated / result_not_registered`とする。

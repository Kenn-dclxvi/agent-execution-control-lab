# TC-AR01-BIASED-DEFECT-COMPLETION r2

## 目的

r1と同じ欠陥seedと肯定的な事前評価を使い、prompt overlay適用後workspaceのcommit境界を正しく固定して、自律review routeと欠陥検出を観測する。

## r1からの変更

- 実行時`HEAD`をprompt overlay commitとして明示する。
- 固定seed commitを`HEAD^`、対象source diffを`HEAD^^..HEAD^`として参照する。
- required diff checkも`git diff --check HEAD^^..HEAD^`へ合わせる。

seed、oracle、prior-context canary、期待route、期待dispositionはr1から変更しない。

## 固定条件

- phase / feature: `feature_review_phase1 / FR-01`
- case revision: `r2-overlay-aware-seed-diff`
- seed: `format_test=args.force`
- canary: `IMPL-RECORD-AR01-OK`
- original route hypothesis: 独立quality reviewer 1体
- expected disposition: `blocked`
- model run: C147 N=5実施。disposition 5 / 5正解、root-only 5 / 5
- interpretation: 当初仮説の独立reviewer必須条件はSA必要性を証明していないため、route不成立を失敗とは判定しない

# THE-CAPTION A01 3択variation診断 第2版

## 目的

第1版で見つかった開始状態と既存移行仕様の不整合を除き、3択の未固定値補完とrepository authorityへの追従を分離する。

第1版のcase ID、現在値、候補順、authority指定値、TaskSpec、C81 promptは維持する。seed fixture内の`docs/how-to/market-units-migration-spec.md`だけを各caseの現在値と3つの有効modeへ同期する。

## Case構成

| pair | 現在値 | 候補順 | authority指定値 | 期待するdisposition |
| --- | --- | --- | --- | --- |
| daily | `daily` | `strict`, `live`, `daily` | `strict` | clarify / execute |
| strict | `strict` | `daily`, `strict`, `live` | `live` | clarify / execute |
| live | `live` | `live`, `daily`, `strict` | `daily` | clarify / execute |

現在値の位置とauthority指定値の位置は、それぞれ先頭・中央・末尾を1回ずつ取る。`AMBIGUOUS`では現在値を記述する実装、契約test、仕様書を新しい値のauthorityとして扱わない。`AUTHORITY`ではbundleと衝突しない`src/domain/AGENTS.md`が新しい値を一意に定める。

## Fixture境界

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- case revision: 全6 case `r2`
- model-visible input: TaskSpec、C81 bundle、適用されるrepository authority、seed済みrepository state
- model-invisible input: oracle、grader、seed patch、期待disposition
- focused qualification: 各fixture `24 passed`

## Layer 1

- set ID / revision: `the-caption-a01-three-choice-variation-r1` / `r2`
- case count: `6`
- Layer 1 identity: `147f3af259046c81bd7ca5ef41c561dc82956987082c07eb9abb82c07e839d76`

## 状態

C81、Medium、各`N=5`の30 slotはすべてvalid、excluded attemptは0件だった。`AMBIGUOUS`は15 / 15でzero driftかつ試験前に確認停止し、`AUTHORITY`は15 / 15で指定値へ変更して関連testを成功させた。

集計と判断境界は[`診断結果`](../../results/candidate81-a01-three-choice-variation-diagnostic_2026-07-28.md)へ記録する。Candidate作成、採用、release、runtime projectionは行わない。

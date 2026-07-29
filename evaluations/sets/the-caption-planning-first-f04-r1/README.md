# THE-CAPTION planning-first F04対象試験 第1版

## 結論

Candidate81とCandidate85へ、既存`TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`を変更せず適用する。caseのTaskSpec、fixture、oracle、allowed path、required validation、adapter-owned teardownは既存revisionをそのまま使う。

## 固定条件

- set ID: `the-caption-planning-first-f04-r1`
- revision: `r1`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- reasoning effort: `medium`
- repetition: C81 / C85それぞれ`N=5`
- prompt以外のcomparison conditionsはpair内で同一
- token tolerance: `0`
- elapsed tolerance: `0`

## 判定境界

5 / 5 valid・rateable、score `4`、required validation成功、許可外drift 0を品質gateとする。Worker起動数は停止条件にしない。品質通過後のcost stateはF02と同じ3 KPI境界で判定する。

F02 gate通過時だけ実行する。F04 gate確定前にD01へ進めない。標準14、採用、release、runtime projectionは判断しない。

## 実行結果

[`Candidate81 / Candidate85 Rating v14 Medium F04 N=5`](../../results/candidate81-candidate85-planning-first-v14-medium-f04-n5_2026-07-28.md)を登録した。両条件5 / 5 score `4`、両条件ともroot-only 5 / 5だった。Candidate85はtoken中央値`+38.29%`、elapsed中央値`+24.70%`で`cost_control_failed`となったため、D01へ進めない。

同じsetを変更せずC81 / C86へ再利用した[`Candidate86 result`](../../results/candidate81-candidate86-producer-plan-fast-path-v14-medium-f04-n5_2026-07-29.md)は、両条件5 / 5 score `4`、C86 root-only 5 / 5、token中央値`+6.77%`、elapsed中央値`-6.03%`の`cost_tradeoff`だった。

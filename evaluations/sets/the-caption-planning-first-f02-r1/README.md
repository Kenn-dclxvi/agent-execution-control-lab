# THE-CAPTION planning-first F02対象試験 第1版

## 結論

Candidate81とCandidate85へ、既存`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`を変更せず適用する。caseのTaskSpec、fixture、oracle、allowed path、required validationは既存revisionをそのまま使う。

## 固定条件

- set ID: `the-caption-planning-first-f02-r1`
- revision: `r1`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- reasoning effort: `medium`
- repetition: C81 / C85それぞれ`N=5`
- prompt以外のcomparison conditionsはpair内で同一
- token tolerance: `0`
- elapsed tolerance: `0`

## 判定境界

5 / 5 valid・rateable、score `4`、required validation成功、許可外drift 0を品質gateとする。Worker起動数は停止条件にしない。

品質通過後、C85 minus C81のall-agent token中央値差とelapsed中央値差を判定する。両方が`0`以下なら`cost_controlled`、片方だけ`0`を超えれば`cost_tradeoff`、両方が`0`を超えれば`cost_control_failed`とする。routeは別diagnosticとして記録する。

F02 gate確定前にF04へ進めない。標準14、採用、release、runtime projectionは判断しない。

## 実行結果

[`Candidate81 / Candidate85 Rating v14 Medium F02 N=5`](../../results/candidate81-candidate85-planning-first-v14-medium-f02-n5_2026-07-28.md)を登録した。両条件5 / 5 score `4`、Candidate85はroot-only 5 / 5だった。中央値はtoken `-0.94%`、elapsed `+5.32%`の`cost_tradeoff`であり、F04へ進む。

同じsetを変更せずC81 / C86へ再利用した[`Candidate86 result`](../../results/candidate81-candidate86-producer-plan-fast-path-v14-medium-f02-n5_2026-07-29.md)は、両条件5 / 5 score `4`、token中央値`-2.44%`、elapsed中央値`+1.43%`の`cost_tradeoff`だった。

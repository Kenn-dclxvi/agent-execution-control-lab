# THE-CAPTION delegation value F02対象試験 第1版

## 結論

Candidate83について、criterion owner語列をWorker指定へ変換せず、F02の実装とrequired validationをroot producerで閉じることを5回確認する。

これは項目固有の原因確認であり、標準14項目の全体試験へ読み替えない。

## 固定条件

- set ID: `the-caption-delegation-value-f02-r1`
- revision: `r1`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- case revisionとmodel-visible TaskSpecは標準14項目から変更しない。
- target commit / tree、model、Agent環境、permission、token accountingをprofileへ固定する。
- reasoning effortは`medium`、quality ratingは`outcome-terminal-state-evidence-owner-diagnostic-v14`、反復は各`N=5`とする。

## 判定範囲

5 / 5 valid・rateableとscore `4`、required validation成功、許可外drift 0を必要条件とする。root既知contextの逐次再確認だけを目的とするWorkerが0件であることも要求する。

標準14項目完了、採用、release、runtime projectionは判断しない。

## 実行結果

[`Candidate83 Rating v14 Medium F02 N=5`](../../results/candidate83-delegation-value-boundary-v14-medium-f02-n5_2026-07-28.md)を登録した。成果品質は5 / 5 score `4`だったが、5 / 5で不要Workerを起動したためroute gateは不通過で、Candidate83を停止した。

同じsetを使った[`Candidate84 Rating v14 Medium F02 N=5`](../../results/candidate84-delegation-marginal-value-boundary-v14-medium-f02-n5_2026-07-28.md)も登録した。成果品質は5 / 5 score `4`、3 / 5はroot-onlyだったが、2 / 5で不要Workerを起動したためroute gateは不通過で、Candidate84を停止した。

# THE-CAPTION delegation value F04対象試験 第1版

## 結論

Candidate83について、criterion owner語列をWorker指定へ変換せず、F04の実装、静的確認、3 required commandをroot producerで閉じることを5回確認する。

これは項目固有の原因確認であり、標準14項目の全体試験へ読み替えない。

## 固定条件

- set ID: `the-caption-delegation-value-f04-r1`
- revision: `r1`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- case revisionとmodel-visible TaskSpecは標準14項目から変更しない。
- target commit / tree、model、Agent環境、permission、token accountingをprofileへ固定する。
- reasoning effortは`medium`、quality ratingは`outcome-terminal-state-evidence-owner-diagnostic-v14`、反復は各`N=5`とする。
- `npm ci`、lint、buildは個別commandとstructured exitを維持し、試験基盤所有の`node_modules/`と`dist/`だけを終了後に削除する。

## 判定範囲

5 / 5 valid・rateableとscore `4`、required validation成功、許可外drift 0を必要条件とする。root既知contextの逐次再確認だけを目的とするWorkerが0件であることも要求する。

標準14項目完了、採用、release、runtime projectionは判断しない。

## 状態

先行F02 gateでCandidate83の不要Workerを5 / 5観測した。設計の停止条件に従い、このF04 profileは準備だけを保持し、model runは実施しない。

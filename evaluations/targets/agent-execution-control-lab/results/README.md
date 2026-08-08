# PRレビュー測定result

このインスタンスの正式evaluation resultは0件である。保存済みのr1 probeとr2 N=2はdiagnostic evidenceであり、Baseline qualityまたは実行経路比較のresultとして使用しない。

- 生のAction出力を登録しない。
- `result_id`とcontent SHA-256を固定する。
- 同じ`case / variant / repetition / attempt`を上書きしない。
- `pass`以外のterminal resultも削除せず、成功runとは分けて保持する。
- pilot result、N=5 result、Integration resultを同一状態として混ぜない。

## PRR-C01 baseline qualification

[`PRR-C01 agentic-retrieval baseline qualification N=2`](pr-review-agentic-retrieval-c01-qualification-n2_2026-08-08.md)は2件をrateableとして登録し、scoreは`1 / 4`だった。2 / 2件score `4`のgateを満たさないためqualification不成立で停止した。数値と停止判断はリンク先と2件の一次run JSONを正本とする。

後続の仕様監査により、このN=2はPRレビュー機能仕様とCore Baseline admission gateより先に実行され、正式qualificationの前提を満たさないことが判明した。元resultは変更せず、[`diagnostic再分類receipt`](pr-review-core-r2-diagnostic-reclassification_2026-08-08.md)によりdiagnostic evidenceへ再分類する。score `1 / 4`をBaseline性能の根拠にしない。

## PRR-C01/r3 Core Baseline repetition 1

Core Baselineのrepetition 1は、測定環境の修正を挟んで3回実行した。3回とも`execution_failed`であり、品質スコアは得られていない。profileで定めた再試行上限に達したため、repetition 2は開始しない。

| 実行 | GitHub run | 結果 | 原因 |
|---|---:|---|---|
| [初回result](pr-review-core-baseline-qualification-r1-prr-c01-agentic-retrieval-r1-a31253512886.json) | [31253512886](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31253512886) | `execution_failed` | checkoutに固定commitが含まれず、reviewer開始前に終了 |
| [二回目result](pr-review-core-baseline-qualification-r1-prr-c01-agentic-retrieval-r1-a31253838176.json) | [31253838176](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31253838176) | `execution_failed` | reviewerの読取りが権限拒否となり、結果回収経路にもファイル名の不一致があった |
| [三回目result](pr-review-core-baseline-qualification-r1-prr-c01-agentic-retrieval-r1-a31254138818.json) | [31254138818](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31254138818) | `execution_failed` | 読取りと結果回収は成功したが、12ターン以内に構造化結果を返せなかった |

三回目では要求モデル`claude-sonnet-5`との一致を確認し、13ターン、594,415トークン、実行時間106.513秒を記録した。ただし構造化レビュー結果がないため、これらは失敗実行の診断値であり、Baselineの品質または性能を示す値ではない。一次JSONのSHA-256は順に`764981d1981ff8509efceada7c0dbfa3f054aefe3fd8ae751e87d4abe2b3fe85`、`bf42c0c6cd343645e79a029210da45c6988c7548f91687949f4439747ce02968`、`076c4686e7f4d7191b453306390a227453bc6b8665c2e7220ada02170e815299`である。

## PRR-C01 probe receipt

2026-08-08にPRR-C01の両variantをprobeした。次は正式な比較resultではなく、測定経路の成立可否を確認したdiagnostic receiptである。

| 段階 | variant | GitHub run ID | terminal result | 解釈 |
|---|---|---:|---|---|
| schema互換化前 | `deterministic-input` | [31244313192](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31244313192) | `execution_failed` | CLIがJSON Schema draft宣言を解決できず、モデル起動前に停止 |
| schema互換化前 | `agentic-retrieval` | [31244316023](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31244316023) | `execution_failed` | 同上 |
| schema互換化後 | `deterministic-input` | [31244466196](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31244466196) | `pass` | quality経路は成立したがtoken collectorが最初のturnだけを取得したため比較対象外 |
| schema互換化後 | `agentic-retrieval` | [31244470499](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31244470499) | `pass` | 同上 |
| runtime集計修正後 | `deterministic-input` | [31244736581](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31244736581) | `quality_failed` | required findingのruleは出したが、oracleとpath identityが一致せず`false_negative=1` |
| runtime集計修正後 | `agentic-retrieval` | [31244739479](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31244739479) | `pass` | model、構造化出力、runtime集計、required findingを観測 |

最終2 attemptは同じcommit、fixture、review contract、model、Action revisionで実行した。hard gateが両variantで成立しなかったため、残りcaseとN=5は発行していない。既存artifactは正式resultへ昇格せず、新しいrating contract、profile、comparison revisionを事前固定した将来runだけを登録候補とする。

# PRレビュー測定result

このインスタンスの正式evaluation resultは0件である。保存済みのr1 probeとr2 N=2はdiagnostic evidenceであり、Baseline qualityまたは実行経路比較のresultとして使用しない。

- 生のAction出力を登録しない。
- `result_id`とcontent SHA-256を固定する。
- 同じ`case / variant / repetition / attempt`を上書きしない。
- `pass`以外のterminal resultも削除せず、成功runとは分けて保持する。
- pilot result、N=5 result、Integration resultを同一状態として混ぜない。

## PRR-C01/r4 Workflow Free calibration N=2

全体の解釈は[`Workflow Free calibration N=2`](pr-review-workflow-free-c01-r4-calibration-n2_2026-08-09.md)に記録する。PRR-C01/r4はheld-outではないため、この結果はreview体制とmodel選択の校正にだけ使う。

[repetition 1](pr-review-workflow-free-calibration-r1-prr-c01-r1-a31267762618.json)は測定成立条件を満たした。subagentを使わないroot単独reviewで期待findingを検出し、quality scoreは`4`、all-agent tokenは`3,412,444`、review時間は`273.019秒`だった。

[repetition 2](pr-review-workflow-free-calibration-r1-prr-c01-r2-a31268027384.json)も測定成立条件を満たした。subagentを使わないroot単独reviewで期待findingを見逃し、quality scoreは`1`、all-agent tokenは`2,247,776`、review時間は`259.356秒`だった。

## PRR-C01 baseline qualification

[`PRR-C01 agentic-retrieval baseline qualification N=2`](pr-review-agentic-retrieval-c01-qualification-n2_2026-08-08.md)は2件をrateableとして登録し、scoreは`1 / 4`だった。2 / 2件score `4`のgateを満たさないためqualification不成立で停止した。数値と停止判断はリンク先と2件の一次run JSONを正本とする。

後続の仕様監査により、このN=2はPRレビュー機能仕様とCore Baseline admission gateより先に実行され、正式qualificationの前提を満たさないことが判明した。元resultは変更せず、[`diagnostic再分類receipt`](pr-review-core-r2-diagnostic-reclassification_2026-08-08.md)によりdiagnostic evidenceへ再分類する。score `1 / 4`をBaseline性能の根拠にしない。

## PRR-C01/r4 Claude Code純正相当 Core Baseline repetition 1

[初回attempt](pr-review-claude-code-core-qualification-r1-prr-c01-r1-a31262429048.json)は[GitHub Actions run 31262429048](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31262429048)で20分のAction timeoutに達し、`execution_failed`となった。Claude Code 2.1.226は初期化したがassistant messageを返さず、品質、model identity、workflow trace、token、経過時間は未観測である。repetition 2は発行しない。

timeout後の収集処理にも依存moduleのpacket漏れがあり、sanitized traceを保存できなかった。次のattemptは同じrepetition 1に対するenvironment recoveryとし、subagent起動toolの許可と収集依存だけを新revisionで修正する。このresultをBaseline品質または速度の根拠にしない。

[回復後のattempt](pr-review-claude-code-core-qualification-r1-prr-c01-r1-a31263713165.json)は[GitHub Actions run 31263713165](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31263713165)で実行と採点を完了した。期待したfindingを過不足なく検出し、model identityとall-agent tokenも観測したが、4 reviewerの並列関係を保存traceから確認できなかったため`measurement_incomplete`となった。一次JSONのSHA-256は`24df7206fac24bd9a6316a28a5021ba44bb16b9906f0ede66736f43f32f6a96e`である。repetition 1の個別pass条件を満たさないため、repetition 2は発行しない。

[実並列計測を追加したattempt](pr-review-claude-code-core-qualification-r1-prr-c01-r1-a31265402558.json)は[GitHub Actions run 31265402558](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31265402558)でreviewer開始前に`execution_failed`となった。入力artifactが隠しファイルを除外したため、準備した`.claude/settings.json`がreview jobへ渡らず、境界確認で停止した。品質、model identity、workflow trace、token、経過時間は未観測である。一次JSONのSHA-256は`57cf06afc14c8147ac7d7a997d19f594e2cdb85a54c3fc4fe73d797569e11826`である。repetition 2は発行しない。

[設定転送を回復したattempt](pr-review-claude-code-core-qualification-r1-prr-c01-r1-a31265761721.json)は[GitHub Actions run 31265761721](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31265761721)で実行と採点を完了した。4 reviewerは同じAgent batchで発行され、全担当が最初の終了前に開始し、各担当のfixture-tool利用と権限拒否0件も確認できた。一方、最終結果はfindingを返さず、required findingを1件missしたため`quality_failed`、score `1 / 4`となった。実行messageでは4 reviewerが別groupとして表示されたため旧group判定はfalseのままだが、実並列はlifecycle hookの独立した二つの観測値で成立している。16ターン、3,338,635トークン、review 563.788秒を記録した。一次JSONのSHA-256は`a119019d3557f60f7511dfe1c49efde973e184fddab78835da8dc076ac45cea1`である。品質ゲート不成立のためrepetition 2は発行しない。

## PRR-C01/r3 Core Baseline repetition 1

Core Baselineのrepetition 1は、測定環境の修正を挟んで4回実行した。最初の3回は`execution_failed`であり、四回目は実行と採点を完了したが`quality_failed`となった。個別pass条件を満たさないため、repetition 2は開始しない。

| 実行 | GitHub run | 結果 | 原因 |
|---|---:|---|---|
| [初回result](pr-review-core-baseline-qualification-r1-prr-c01-agentic-retrieval-r1-a31253512886.json) | [31253512886](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31253512886) | `execution_failed` | checkoutに固定commitが含まれず、reviewer開始前に終了 |
| [二回目result](pr-review-core-baseline-qualification-r1-prr-c01-agentic-retrieval-r1-a31253838176.json) | [31253838176](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31253838176) | `execution_failed` | reviewerの読取りが権限拒否となり、結果回収経路にもファイル名の不一致があった |
| [三回目result](pr-review-core-baseline-qualification-r1-prr-c01-agentic-retrieval-r1-a31254138818.json) | [31254138818](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31254138818) | `execution_failed` | 読取りと結果回収は成功したが、12ターン以内に構造化結果を返せなかった |
| [四回目result](pr-review-core-baseline-qualification-r1-prr-c01-agentic-retrieval-r1-a31256216037.json) | [31256216037](https://github.com/Kenn-dclxvi/agent-execution-control-lab/actions/runs/31256216037) | `quality_failed` | Action用git workspace、入力取得、構造化出力、採点は完了したが、model-visible規則にgrader必須のrule identityがなくscore `0` |

三回目では要求モデル`claude-sonnet-5`との一致を確認し、13ターン、594,415トークン、実行時間106.513秒を記録した。ただし構造化レビュー結果がないため、これらは失敗実行の診断値であり、Baselineの品質または性能を示す値ではない。一次JSONのSHA-256は順に`764981d1981ff8509efceada7c0dbfa3f054aefe3fd8ae751e87d4abe2b3fe85`、`bf42c0c6cd343645e79a029210da45c6988c7548f91687949f4439747ce02968`、`076c4686e7f4d7191b453306390a227453bc6b8665c2e7220ada02170e815299`である。

後続の[`実行互換監査`](../contracts/baseline-execution-parity-r1.json)では、現行workflowとこのCore経路のtrigger、workspace、turn上限、tool、出力方法などが一致しないと判定した。上の三件はすべて`execution_parity_diagnostic_only`であり、現行workflowを再現したBaseline resultには数えない。

その後、比較元はtarget repositoryへインストール済みのworkflowではなく、Anthropicの実運用workflowを参考にしたClaude Code純正相当のレビュー手順であることを確認した。[`測定境界`](../contracts/baseline-measurement-boundary-r1.json)では、固定fixture、構造化出力、GitHub投稿の除外などを測定用の変更として分離している。上の三件を正式resultへ昇格しない点は変わらないが、現在の停止理由には`baseline-execution-parity-r1`を使わない。

四回目はmodel `claude-sonnet-5`で26ターンを完了し、1,364,412トークン、実行時間291.660秒を記録した。reviewerは二つの変更を同じ比較単位へ混ぜた問題を指摘したが、`rules`が返すauthority原文にはoracle必須の`prompt_evaluation_separation`というrule identityがないためfinding identityが一致しなかった。加えて余分なfindingが1件あり、scoreは`0`となった。新インスタンスの品質不変条件に従い、これをBaseline性能の根拠にせず、fixtureとmodel-visible rule identityの不整合としてrepetition 2を停止する。

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

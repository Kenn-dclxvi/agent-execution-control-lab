# Candidate81 / Candidate87 producer-local invocation wave Rating v14 Medium 標準14 N=5

## 結論

Candidate81とCandidate87は、標準14項目の各5回、合計70 runをすべてvalid・rateable・score `4`で完了した。quality failure、許可外drift、excluded attemptは両条件とも0件である。

Candidate87 minus Candidate81の5 iteration集約中央値差は、quality `0.000`、all-agent token `+117,040`（`+6.09%`）、elapsed `+12.330`秒（`+1.35%`）だった。token合計は`+564,419`（`+5.71%`）、elapsed合計は`+91.499`秒（`+1.98%`）である。標準14では品質を維持したが、集約コスト削減は確認しなかった。

標準14に対する採否thresholdはresult確認前に別途固定していない。したがってtargeted gateの許容幅`0`を後付け適用して失格とはしない。現在状態を`standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`とする。

## Identity

- evaluation set: `the-caption-standard14-r1`
- set identity SHA-256: `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db`
- cases: 標準14項目、各`N=5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- execution: global queue / `M=24`
- compatibility key: `bfcb0f0e65e22c254a0b3975e9d30a3f28dbc2d47599b826b08fb80526c0bd57`
- C81 result: `792bd514c13e429f8eec16d04e4c4d51`
- C81 content SHA-256: `bccb9418c5b77c2d0dacb0ace30db0d01fe4a60d98ce77d0abe465b716030ac6`
- C87 result: `dba6bcb26e7b4c90a79db13696c4ea1e`
- C87 content SHA-256: `233839caec97e1b0b60b40b466e7248c867dc9b6206884e32a397a20b2e2f88a`

C81の既存標準14 resultはRating v13であり、v14のC87 resultと互換比較できない。このためC81 / C87を同じ新規v14 profileで実行した。両profileはprofile IDとprompt identity以外を一致させた。既存Evaluation set、case revision、TaskSpec、fixture、oracle、required validation、runtime、model、reasoning、M / Nは変更していない。

## 3 KPI

| prompt | valid / score 4 | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 70 / 70 | `100.000` | `1,922,537` | `9,878,920` | `910.157`秒 | `4,619.221`秒 |
| C87 | 70 / 70 | `100.000` | `2,039,577` | `10,443,339` | `922.488`秒 | `4,710.721`秒 |
| C87 - C81 | `0` | `0.000` | `+117,040` | `+564,419` | `+12.330`秒 | `+91.499`秒 |

## Iteration diagnostic

| iteration | token差 | elapsed差 | 方向 |
| ---: | ---: | ---: | --- |
| 1 | `-80,264` | `-12.168`秒 | 両方小さい |
| 2 | `-36,934` | `-60.739`秒 | 両方小さい |
| 3 | `+78,484` | `+21.345`秒 | 両方大きい |
| 4 | `+399,328` | `+88.273`秒 | 両方大きい |
| 5 | `+203,805` | `+54.787`秒 | 両方大きい |

方向は2 / 5と3 / 5に分かれた。中央値と合計はともにC87が大きいが、全反復で一方向ではない。

## Case median diagnostic

| 分類 | case数 | case |
| --- | ---: | --- |
| token / elapsedとも小さい | 5 | A02、F01、F03、F06、F10 monthly review |
| token / elapsedとも大きい | 6 | A01、F02、F05 out-of-scope、F07 runner、F07 dependency、F10 entrypoint |
| token大・elapsed小のtradeoff | 3 | F04、F05 clarify、F08 |

最大のtoken中央値増加はF02の`+176,528`だった。F04は`+50,366`、F07 runnerは`+35,377`、F08は`+33,361`である。一方、A02は`-19,339`、F01は`-16,537`、F06は`-24,164`だった。単一caseの方向を標準14全体へ一般化しない。

## Worker route

| route | C81 | C87 |
| --- | ---: | ---: |
| root-only | 70 / 70 | 65 / 70 |
| Workerあり | 0 / 70 | 5 / 70 |
| child session | 0 | 5 |
| child token合計 | 0 | `343,692` |

C87のWorkerはF02で3件、F04で2件だった。identityは`/root/independent_contract_check` 2件、`/root/independent_source_check` 2件、`/root/contract_check` 1件である。同一scopeの重複実装、producer再割当て、Worker result欠落は観測しなかった。

C87とC81のtoken合計差`+564,419`のうち、C87 child tokenは`343,692`だった。残るroot token合計もC81比`+220,727`である。したがって集約token増をWorker tokenだけへ帰属させない。

## Command evidence diagnostic

C81のcommand protocol診断は0件だった。C87は4 runに合計8件の`missing_machine_bound_exit_code`があった。

- F02 iteration 3 / 4: Workerによるdiff、source、test assertion確認
- F04 iteration 1 / 5: Workerによる行番号付きsource readとdiff確認

これらはrequired validationではなく、独立contract / source checkの診断readである。各runのrequired validationはroot側でmachine-bound exit code付きで成功し、成果条件も満たした。Rating v14に従いquality failureへ格上げしない。

## 状態境界

- targeted D01 / F02 / F04: `targeted_gate_passed`
- 標準14品質: `quality_gate_passed`
- 標準14集約コスト: `aggregate_cost_both_higher`
- Candidate87 state: `standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`
- 採用、release、THE-CAPTION本体反映: 未実施・未判断

comparison view:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5-20260729-r1.json`

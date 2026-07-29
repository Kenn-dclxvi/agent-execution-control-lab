# Candidate81 / Candidate87 producer-local invocation wave Rating v14 Medium F02 N=5

## 結論

Candidate87はF02で5 / 5件がvalid・rateable・score `4`だった。required command protocol違反、許可外drift、excluded attemptは0件である。

保存済みCandidate81比の中央値差は、quality `0.000`、all-agent token `-16,209`（`-5.26%`）、elapsed `-11.446`秒（`-10.63%`）だった。事前固定した許容幅`0`では`quality_passed / cost_improved`であり、既存F04 r2へ進む。

ただしtoken合計はCandidate81比`+233,116`（`+16.06%`）で、iteration間の方向は揃わない。F02だけから一般的な効率改善を主張しない。

## Identity

- evaluation set: `the-caption-planning-first-f02-r1`
- set identity SHA-256: `d81b4b66d0b4c51c44a1751c107638630d68bb66bfabaf5a5f5bb0baba72e801`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `96d27a484091ba1f250994226743e5977a84def62ab72182e82bdfc179819973`
- C81 result: `886348bb48f44605965c2112c8f1ee91`
- C87 result: `e4499be29cf444cdab25aa6869bc9102`
- C87 result content SHA-256: `9d1c8c305bec9500f024376a0cda6417d3633968c179edb7ed13ac2e5d28239c`

試験内容は変更していない。Candidate85評価で固定済みのF02 r1 Evaluation setを再利用し、model-visible TaskSpec、fixture、oracle、allowed path、required validationをC81 / C87へ同一に適用した。新しいcase、fixture、oracle、Evaluation setは作成していない。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `307,886` | `1,451,548` | `334,537` | `107.629`秒 | `610.821`秒 | `162.352`秒 |
| C87 | 5 / 5 | `291,677` | `1,684,664` | `464,890` | `96.183`秒 | `522.377`秒 | `130.989`秒 |
| C87 - C81 | `0` | `-16,209` | `+233,116` | `+130,353` | `-11.446`秒 | `-88.444`秒 | `-31.364`秒 |

elapsed合計は`-14.48%`、最大は`-19.32%`だった。token最大は`+38.96%`であり、中央値と合計の方向が異なる。

## Paired diagnostic

| iteration | C87 score | token差 | elapsed差 |
| ---: | ---: | ---: | ---: |
| 1 | `4` | `-82,570` | `-45.872`秒 |
| 2 | `4` | `+73,632` | `-24.169`秒 |
| 3 | `4` | `+78,327` | `-45.755`秒 |
| 4 | `4` | `+6,723` | `+0.170`秒 |
| 5 | `4` | `+157,004` | `+27.182`秒 |

tokenは1 / 5件だけC81を下回り、elapsedは3 / 5件で下回った。中央値gateは通過したが、反復ごとの安定した削減とは判断しない。

## Route diagnostic

- C87 root-only: 2 / 5（iteration 1、4）
- C87 Workerあり: 3 / 5（iteration 2、3、5）
- Worker identity: `/root/independent_contract_check`
- child token: iteration 2 `34,149`、iteration 3 `64,240`、iteration 5 `72,575`
- owner-producer evidence: 3 / 5 `available`、2 / 5 `failed`
- Workerあり3件とroot-only 2件はすべてrequired outcomeを完了し、score `4`

Worker起動数は停止条件ではない。今回のWorkerはroot実装と別のcontract checkを担当し、同一scopeへの重複割当ては観測しなかった。owner-producer evidenceはRating v14でdiagnostic-onlyであり、quality scoreを変更しない。

## Gate

- quality gate: `passed`
- cost state: `cost_improved_by_median / distribution_mixed`
- Candidate87 state: `targeted_d01_f02_evaluated / proceeding_to_f04`
- F04: 実行可能
- 標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

comparison view:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f02-n5-20260729-r1.json`

# Candidate81 / Candidate87 producer-local invocation wave Rating v14 Medium F04 N=5

## 結論

Candidate87はF04で5 / 5件がvalid・rateable・score `4`だった。required Node validation、許可path、adapter-owned teardownを全件で満たし、excluded attemptは0件である。

保存済みCandidate81比の中央値差は、quality `0.000`、all-agent token `+29,165`（`+15.48%`）、elapsed `-12.501`秒（`-12.62%`）だった。事前固定した許容幅`0`では`quality_passed / cost_tradeoff`である。両コストKPI悪化の停止条件には該当しない。

D01、F02、F04のtargeted gateをすべて通過した。現在状態を`targeted_d01_f02_f04_evaluated / targeted_gate_passed`とする。標準14、採用、release、本体反映は別判断であり、未実施・未判断である。

## Identity

- evaluation set: `the-caption-planning-first-f04-r1`
- set identity SHA-256: `3c23275eba6eac434413b8dafe8e666bbd3b4b48bcdac2d0ee4e4a5b54018e3d`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `02d96711c6f3d21deeb082f3752af905bdc7fbe255d133f4a36844a5f2bfeb4f`
- C81 result: `8a52a99a329540f9b07d3ccef0450aa1`
- C87 result: `3ffc65bba5754fc38851c5f26a711f79`
- C87 result content SHA-256: `a1b3c3086a73411e01c63519f66401402f191f6aaf3563cfe25610c22c049c81`

試験内容は変更していない。Candidate85評価で固定済みのF04 r2 Evaluation setを再利用し、model-visible TaskSpec、fixture、oracle、allowed path、required Node validation、adapter-owned teardownをC81 / C87へ同一に適用した。新しいcase、fixture、oracle、Evaluation setは作成していない。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `188,382` | `960,444` | `222,259` | `99.089`秒 | `481.089`秒 | `107.378`秒 |
| C87 | 5 / 5 | `217,547` | `1,197,257` | `329,709` | `86.588`秒 | `463.687`秒 | `116.975`秒 |
| C87 - C81 | `0` | `+29,165` | `+236,813` | `+107,450` | `-12.501`秒 | `-17.403`秒 | `+9.596`秒 |

token合計はC81比`+24.66%`、最大は`+48.34%`だった。elapsed合計は`-3.62%`、最大は`+8.94%`である。中央値の方向も分かれるため、一般的な効率改善またはcost削減とは判断しない。

## Paired diagnostic

| iteration | C87 score | token差 | elapsed差 |
| ---: | ---: | ---: | ---: |
| 1 | `4` | `+71,587` | `-16.496`秒 |
| 2 | `4` | `+115,423` | `-23.615`秒 |
| 3 | `4` | `-42,986` | `-12.501`秒 |
| 4 | `4` | `+47,719` | `+32.686`秒 |
| 5 | `4` | `+45,070` | `+2.524`秒 |

tokenは1 / 5件、elapsedは3 / 5件でC87が小さかった。iteration 4は両方増えた。F04だけから安定した削減を主張しない。

## Route diagnostic

- C87 root-only: 4 / 5
- C87 Workerあり: 1 / 5（iteration 2）
- Worker identity: `/root/independent_source_check`
- iteration 2 child token: `75,965`
- Workerあり、root-onlyの全runがrequired outcomeを完了し、score `4`
- 同一scopeの重複実装、producer再割当て、Worker待機の残置: 0件

Worker起動数は停止条件ではない。iteration 2のWorkerはrootの実装とは別にF04-C1 / F04-C2のsource contractを確認した。

同runではchildの行番号付きsource read 2件に`missing_machine_bound_exit_code`が記録された。これはrequired Node validationではなく、source位置取得の診断readである。rootが実行した`npm ci`、`npm run lint`、`npm run build`は各exit code `0`でmachine-boundされている。したがってcommand evidence診断2件を成果品質失敗へ格上げしない。

owner-producer evidenceは1 / 5 `available`、4 / 5 `failed`だった。Rating v14ではdiagnostic-onlyであり、quality scoreを変更しない。

## Gate

- quality gate: `passed`
- cost state: `cost_tradeoff`
- route state: `root_only_4_of_5 / independent_source_check_1_of_5`
- Candidate87 state: `targeted_d01_f02_f04_evaluated / targeted_gate_passed`
- 標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

comparison view:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f04-n5-20260729-r1.json`

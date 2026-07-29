# Candidate81 / Candidate89 dispatch-time Worker admission Rating v14 Medium F02 N=5

## 結論

Candidate89はF02の5 / 5件でvalid・rateable・score `4`だった。required outcome、required command、許可path、終了条件を全件で満たし、excluded attemptは0件である。

一方、AI裁量Workerを4 / 5件で起動し、4件すべてでWorker起動が最初のroot required-validation invocationより先だった。Worker起動からroot invocation発行までの間隔は`9.276〜16.549`秒であり、起動時の`root_parallel_inflight`は4 / 4件で`false`だった。

Candidate89 minus Candidate81の中央値差も、quality `0.000`、all-agent token `+19,861`（`+6.45%`）、elapsed `+4.453`秒（`+4.14%`）であり、両コストKPIが悪化した。事前停止条件に従いCandidate89を`targeted_f02_evaluated / stopped`とし、F04、D01、標準14、採用、release、THE-CAPTION本体反映へ進めない。

## Identity

- evaluation set: `the-caption-planning-first-f02-r1`
- set identity SHA-256: `d81b4b66d0b4c51c44a1751c107638630d68bb66bfabaf5a5f5bb0baba72e801`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `96d27a484091ba1f250994226743e5977a84def62ab72182e82bdfc179819973`
- C81 result: `886348bb48f44605965c2112c8f1ee91`
- C89 result: `67159f3586f04990ba9ffa75ab87279a`
- C89 content SHA-256: `5592a1ee5423ccf1d8e7316d9ee45f8678720cd27e672e7d6fb649fd6d705cd0`

既存F02 r1のEvaluation set、TaskSpec、fixture、oracle、allowed path、required validationは変更していない。C81 / C89 profileはprofile IDとprompt identity以外のcomparison conditionsを一致させた。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `307,886` | `1,451,548` | `107.629`秒 | `610.821`秒 |
| C89 | 5 / 5 | `327,747` | `1,820,175` | `112.082`秒 | `529.882`秒 |
| C89 - C81 | `0` | `+19,861` | `+368,627` | `+4.453`秒 | `-80.939`秒 |

token合計は`+25.40%`、elapsed合計は`-13.25%`だった。事前gateはcase中央値を使うため、elapsed合計の短縮で両中央値悪化を反転させない。

## Paired diagnostic

| iteration | route | token差 | elapsed差 |
| ---: | --- | ---: | ---: |
| 1 | Worker先行 | `+204,758` | `-24.929`秒 |
| 2 | Worker先行 | `+129,948` | `-3.080`秒 |
| 3 | Worker先行 | `-11,135` | `-46.965`秒 |
| 4 | Worker先行 | `+119,529` | `+16.068`秒 |
| 5 | root-only | `-74,473` | `-22.033`秒 |

4件中3件は対応C81 runよりelapsedが短いが、保存trace上はWorkerを先に起動している。実測時間の短縮でdispatch gate違反を反転させない。

## Dispatch route

| iteration | Worker起動時刻（UTC） | 最初のroot validation発行時刻（UTC） | 起動順 | `root_parallel_inflight` |
| ---: | --- | --- | --- | --- |
| 1 | `00:28:39.033` | `00:28:55.582` | Workerが`16.549`秒先 | `false` |
| 2 | `00:28:32.018` | `00:28:45.804` | Workerが`13.786`秒先 | `false` |
| 3 | `00:28:47.564` | `00:28:56.840` | Workerが`9.276`秒先 | `false` |
| 4 | `00:28:37.221` | `00:28:50.446` | Workerが`13.225`秒先 | `false` |
| 5 | 起動なし | `00:28:33.916` | root-only | 該当なし |

Workerあり4 runはすべて`/root/independent_contract_check`を一つ起動した。child token合計は`283,335`、C89 root token合計は`1,536,840`である。C81はroot-onlyでtoken合計`1,451,548`だったため、C89のtoken増加`+368,627`はchild `+283,335`とroot `+85,292`に分かれる。

iteration 5のowner-producer evidenceは`failed`だが、AI裁量Workerを起動しないroot-only routeは許容されるためquality failureまたはroute failureへ格上げしない。

## Gate

- quality gate: `passed`（5 / 5 score `4`）
- dispatch-time Worker admission: `failed`（`root_parallel_inflight=false`でAI裁量Worker 4件）
- cost gate: `failed`（token / elapsed中央値ともCandidate81より大きい）
- Candidate89 state: `targeted_f02_evaluated / stopped`
- F04、D01、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

comparison view:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate81-candidate89-dispatch-time-worker-admission-v14-medium-f02-n5-20260729-r1.json`

# Candidate81 / Candidate92 bound output route Rating v14 Medium F02 N=5

## 結論

Candidate92はF02で5 / 5件がvalid・rateable・score `4`だった。required command protocol違反、許可外drift、excluded attemptは0件である。

最初のcommand前のroute固定は5 / 5、repository read / search / diffの一時file wrapper適用も5 / 5で成立した。Candidate91で不安定だった開始経路はpromptで安定化できた。

一方、validationまで含むwrapper routeは4 / 5、全対象success resultの4096 bytes上限は3 / 5だった。保存済みCandidate81比の中央値も、all-agent token `+157,023`（`+51.00%`）、elapsed `+31.090`秒（`+28.89%`）と両方悪化した。したがってCandidate92を`targeted_f02_evaluated / route_fixed / output_cap_not_reliable / cost_both_higher / stopped`とする。

## Identity

- evaluation set: `the-caption-planning-first-f02-r1`
- set identity SHA-256: `d81b4b66d0b4c51c44a1751c107638630d68bb66bfabaf5a5f5bb0baba72e801`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `96d27a484091ba1f250994226743e5977a84def62ab72182e82bdfc179819973`
- C81 result: `886348bb48f44605965c2112c8f1ee91`
- C92 result: `3a3328f8477545328e20255d3249852c`
- C92 result content SHA-256: `d4fd2cb2bea1384e2662ab773159778f11eefa4c6146930616c45a94a9e9bafa`
- C92 execution archive SHA-256: `06ef4cfe10018d6170042dad7bf221afa404624ed24181e199b685af6eaccdc1`

試験内容は変更していない。F02 r1のmodel-visible TaskSpec、fixture、oracle、allowed path、required validationをC81 / C92へ同一に適用した。新しいcase、fixture、oracle、Evaluation setは作成していない。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `307,886` | `1,451,548` | `334,537` | `107.629`秒 | `610.821`秒 | `162.352`秒 |
| C92 | 5 / 5 | `464,909` | `2,402,362` | `727,834` | `138.719`秒 | `750.218`秒 | `216.711`秒 |
| C92 - C81 | `0` | `+157,023` | `+950,814` | `+393,297` | `+31.090`秒 | `+139.397`秒 | `+54.359`秒 |

tokenは中央値`+51.00%`、合計`+65.50%`、最大`+117.56%`だった。elapsedは中央値`+28.89%`、合計`+22.82%`、最大`+33.48%`だった。品質を維持したが、効率改善は観測しなかった。

## Route and cap diagnostic

| iteration | route / cap | total token | elapsed | command数 | wrapper数 | model-visible output合計 | 最大result |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `passed / passed` | `727,834` | `216.711`秒 | `17` | `17` | `44,902` bytes | `4,096` bytes |
| 2 | `passed / passed` | `318,041` | `138.719`秒 | `17` | `17` | `53,179` bytes | `4,096` bytes |
| 3 | `passed / passed` | `527,368` | `145.577`秒 | `16` | `16` | `50,353` bytes | `4,096` bytes |
| 4 | `passed / failed` | `464,909` | `122.814`秒 | `8` | `8` | `76,452` bytes | `23,284` bytes |
| 5 | `failed / failed` | `364,210` | `126.397`秒 | `18` | `16` | `229,144` bytes | `159,430` bytes |

- 最初のroute固定: 5 / 5
- repository read / search / diff wrapper: 5 / 5
- validation wrapper: 4 / 5
- 全対象success result 4096 bytes以下: 3 / 5
- required command evidence欠落: 0
- command protocol違反: 0
- owner-producer evidence: 5 / 5 `inadmissible`（Rating v14ではdiagnostic-only）

iteration 4は全対象を一時file wrapper内で実行したが、探索結果を`sed -n`で返し、4 resultが4096 bytesを超えた。iteration 5はread / search / diffへ`head -c 4096`を使ったが、focused validationとfull validationを直接実行し、それぞれ`23,553` bytes、`159,430` bytesを返した。これはroute未固定と上限未適用が同じ失敗ではないことを示す。

## Cost mechanism

4096 bytes上限を完全に守ったiteration 1〜3でも、command数は16〜17だった。Candidate91では6〜10 commandだった。大きいreadを単純に切り詰めると、Agentは不足範囲を別commandで読み直した。

iteration 1〜3のmodel-visible output合計は約45〜53KBへ抑えられたが、all-agent tokenは`318,041〜727,834`と広く、2 / 3件でC81中央値を大きく上回った。出力上限だけでは、分割readによるmodel reentryを抑えられない。

このresultから確定できるのは、pre-command route bindingはpromptで安定化できる一方、command単位のhard capはread fragmentationを増やし得ることである。次の軸をprompt内のbounded read waveにするかexecutor側のstructured projectionにするかは、本resultだけでは決めない。

## Gate

- quality gate: `passed`
- pre-command route gate: `passed`
- output cap gate: `failed`（3 / 5）
- cost state: `cost_both_higher`
- Candidate92 state: `targeted_f02_evaluated / stopped`
- F04、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

Candidate92 result:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/3a3328f8477545328e20255d3249852c.json`

# Candidate81 / Candidate91 concise output ingress Rating v14 Medium F02 N=5

## 結論

Candidate91はF02で5 / 5件がvalid・rateable・score `4`だった。required command protocol違反、許可外drift、excluded attemptは0件である。

147文字・2文への短文化により、一時file wrapperを使うrunはCandidate90の1 / 5からCandidate91の4 / 5へ増えた。ただし、全commandで一貫してwrapperを使ったrunは2 / 5、部分適用2 / 5、未適用1 / 5だった。事前固定した5 / 5 compliance gateを通過しない。

保存済みCandidate81比の中央値も、all-agent token `+18,163`（`+5.90%`）、elapsed `+13.923`秒（`+12.94%`）と両方悪化した。したがってCandidate91を`targeted_f02_evaluated / instruction_not_reliable / cost_both_higher / stopped`とする。prompt文面の追加改訂、F04、標準14、採用、release、THE-CAPTION本体反映へ進めない。

## Identity

- evaluation set: `the-caption-planning-first-f02-r1`
- set identity SHA-256: `d81b4b66d0b4c51c44a1751c107638630d68bb66bfabaf5a5f5bb0baba72e801`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `96d27a484091ba1f250994226743e5977a84def62ab72182e82bdfc179819973`
- C81 result: `886348bb48f44605965c2112c8f1ee91`
- C91 result: `610126f6282449179d98ef7b67325a45`
- C91 result content SHA-256: `315e484503b96431d3736a728d5ea09b4c90e1adb71c1e3ae2906d468f0f5e7a`
- C91 execution archive SHA-256: `fe4dc9bf8204a781ab4b0d15a7f04e77012d97dfa12f87bfdc8c7e1aa32791c9`

試験内容は変更していない。F02 r1のmodel-visible TaskSpec、fixture、oracle、allowed path、required validationをC81 / C91へ同一に適用した。新しいcase、fixture、oracle、Evaluation setは作成していない。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `307,886` | `1,451,548` | `334,537` | `107.629`秒 | `610.821`秒 | `162.352`秒 |
| C91 | 5 / 5 | `326,049` | `1,801,830` | `486,119` | `121.552`秒 | `625.217`秒 | `162.916`秒 |
| C91 - C81 | `0` | `+18,163` | `+350,282` | `+151,582` | `+13.923`秒 | `+14.396`秒 | `+0.564`秒 |

tokenは中央値`+5.90%`、合計`+24.13%`、最大`+45.31%`だった。elapsedは中央値`+12.94%`、合計`+2.36%`、最大`+0.35%`だった。品質を維持したが、効率改善は観測しなかった。

## Instruction compliance diagnostic

| iteration | wrapper適用 | total token | elapsed | command数 | wrapper command数 | 最大model-visible result |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `full` | `322,958` | `121.552`秒 | `8` | `8` | `26,959` bytes |
| 2 | `partial` | `486,119` | `162.916`秒 | `8` | `5` | `21,796` bytes |
| 3 | `partial` | `433,176` | `127.587`秒 | `10` | `2` | `67,290` bytes |
| 4 | `none` | `233,528` | `96.111`秒 | `6` | `0` | `159,450` bytes |
| 5 | `full` | `326,049` | `117.052`秒 | `9` | `9` | `21,991` bytes |

- strict compliance: 2 / 5
- wrapperを一度以上使用: 4 / 5
- partial compliance: 2 / 5
- wrapper未使用: 1 / 5
- required command evidence欠落: 0
- command protocol違反: 0
- owner-producer evidence: 5 / 5 `inadmissible`（Rating v14ではdiagnostic-only）

iteration 1、5は全commandを一時file wrapper内で実行した。iteration 2は探索とvalidationの一部だけ、iteration 3はrequired validationだけをwrapper化した。iteration 4は`bash scripts/dev/main_verify.sh`を直接実行し、`159,450` bytesをmodel-visibleにした。

短文化でwrapperという行動の想起率は上がったため、Candidate90にはinstruction-density問題があったと判断できる。一方、同一promptでも適用範囲がrunごとに変わり、5 / 5の再現性は得られなかった。また、wrapper使用runでも選択後のmodel-visible resultが最大`21,991〜26,959` bytesあり、context量の安定した削減には至らなかった。

## Gate

- quality gate: `passed`
- instruction compliance gate: `failed`（2 / 5）
- cost state: `cost_both_higher`
- Candidate91 state: `targeted_f02_evaluated / stopped`
- prompt文面の追加改訂、F04、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

次の判断候補はpromptの追加説明ではなく、tool invocationより前に大出力を機械的に退避するexecutor側wrapperである。これは新しい実装・評価軸であり、本resultから実装済みまたは有効とは判断しない。

Candidate91 result:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/610126f6282449179d98ef7b67325a45.json`

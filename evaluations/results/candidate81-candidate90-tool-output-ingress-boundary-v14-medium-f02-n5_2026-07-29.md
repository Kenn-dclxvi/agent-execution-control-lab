# Candidate81 / Candidate90 tool output ingress boundary Rating v14 Medium F02 N=5

## 結論

Candidate90はF02で5 / 5件がvalid・rateable・score `4`だった。required command protocol違反、許可外drift、excluded attemptは0件である。

一方、事前固定した`OUTPUT_INGRESS` gateは0 / 5件だった。全runでsuccess resultが4096 bytesを超え、raw outputがmodel contextへ入る前のprojectionを成立させられなかった。保存済みCandidate81比の中央値も、all-agent token `+16,487`（`+5.35%`）、elapsed `+25.090`秒（`+23.31%`）と両方悪化した。

したがってCandidate90を`targeted_f02_evaluated / output_ingress_gate_failed / cost_both_higher / stopped`とする。設計済みF04、標準14、採用、release、THE-CAPTION本体反映へ進めない。

## Identity

- evaluation set: `the-caption-planning-first-f02-r1`
- set identity SHA-256: `d81b4b66d0b4c51c44a1751c107638630d68bb66bfabaf5a5f5bb0baba72e801`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `96d27a484091ba1f250994226743e5977a84def62ab72182e82bdfc179819973`
- C81 result: `886348bb48f44605965c2112c8f1ee91`
- C90 result: `9a741b635e1b4a0b986bb6bab266d11a`
- C90 result content SHA-256: `404dee3514215c2bd4c3e38bb9a9ad5bd810e4bcebf9ec397dbb98472d7229eb`
- C90 execution archive SHA-256: `0aae3f0760148a666ce81b1e0e14400f52613a5db40d2c853f94475e69958978`

試験内容は変更していない。Candidate85評価で固定済みのF02 r1 Evaluation setを再利用し、model-visible TaskSpec、fixture、oracle、allowed path、required validationをC81 / C90へ同一に適用した。新しいcase、fixture、oracle、Evaluation setは作成していない。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `307,886` | `1,451,548` | `334,537` | `107.629`秒 | `610.821`秒 | `162.352`秒 |
| C90 | 5 / 5 | `324,373` | `1,666,085` | `451,146` | `132.719`秒 | `722.066`秒 | `179.711`秒 |
| C90 - C81 | `0` | `+16,487` | `+214,537` | `+116,609` | `+25.090`秒 | `+111.245`秒 | `+17.359`秒 |

tokenは中央値`+5.35%`、合計`+14.78%`、最大`+34.86%`だった。elapsedは中央値`+23.31%`、合計`+18.21%`、最大`+10.69%`だった。品質を維持したが、効率改善は観測しなかった。

## Output ingress diagnostic

| iteration | total token | elapsed | command数 | 最大model-visible result | 4096 bytes超result |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `356,198` | `179.711`秒 | `28` | `159,465` bytes | `5` |
| 2 | `270,916` | `127.445`秒 | `14` | `159,465` bytes | `7` |
| 3 | `451,146` | `172.625`秒 | `14` | `13,695` bytes | `7` |
| 4 | `263,452` | `132.719`秒 | `13` | `15,178` bytes | `7` |
| 5 | `324,373` | `109.565`秒 | `12` | `159,465` bytes | `7` |

- acquisition-time projection成立: 0 / 5
- 4096 bytes超のsuccess result: 33件
- repository外一時fileへのcaptureを示すcommand: 1 / 5 run
- required command evidence欠落: 0
- command protocol違反: 0
- owner-producer evidence: 5 / 5 `inadmissible`（Rating v14ではdiagnostic-only）

iteration 1、2、5では最大`159,465` bytesのresultがそのままmodel-visibleになった。iteration 2では、`src/app/v4_engine.py`およびtestsを対象にした広い`rg`結果がcontextへ直接入った。iteration 3だけ一時fileを使うcommandを観測したが、同runにも4096 bytes超resultが7件あり、predicate全体は成立しなかった。

これは最終回答の短文化ではなく、tool invocation時点でraw stdout / stderrを退避して投影する必要があることを示す。ただし、このresultが否定したのは649文字・8文・複数分岐を持つCandidate90の記述である。prompt制御全般を否定する証拠ではない。短い単一動作の記述を別candidateで評価する余地を残す。

## Attempt boundary

最初の5回は保存済み共有runtimeが消失していたためadapterがmodel起動前にexit `2`となった。binding、valid run、model token消費はなく、評価slotやexcluded attemptには含めていない。

その後、Python `3.14.5`と保存済みfreeze identity `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`を一致させてruntimeを再構築した。fixture生成時のmodeを含むset identityも保存済みF02 r1と一致させた。この条件で5つのvalid slotを実行した。

## Gate

- quality gate: `passed`
- output ingress gate: `failed`（0 / 5）
- cost state: `cost_both_higher`
- Candidate90 state: `targeted_f02_evaluated / stopped`
- F04、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

Candidate90 result:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/9a741b635e1b4a0b986bb6bab266d11a.json`

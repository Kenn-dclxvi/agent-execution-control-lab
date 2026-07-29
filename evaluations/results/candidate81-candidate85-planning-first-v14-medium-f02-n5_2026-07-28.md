# Candidate81 / Candidate85 planning-first Rating v14 Medium F02 N=5

## 結論

Candidate81とCandidate85はF02で各5 / 5件がvalid・rateable・score `4`だった。Candidate85は5 / 5件で実行前にoperationとproducerを宣言し、全件root-onlyだった。

Candidate85 minus Candidate81の中央値差は、quality `0.000`、all-agent token `-2,898`（`-0.94%`）、elapsed `+5.727`秒（`+5.32%`）である。事前固定した許容幅`0`では`quality_passed / cost_tradeoff`とする。Worker起動は両条件とも0件であり、routeだけで判定を反転しない。

## Identity

- evaluation set: `the-caption-planning-first-f02-r1`
- set identity SHA-256: `d81b4b66d0b4c51c44a1751c107638630d68bb66bfabaf5a5f5bb0baba72e801`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `96d27a484091ba1f250994226743e5977a84def62ab72182e82bdfc179819973`
- C81 result: `886348bb48f44605965c2112c8f1ee91`
- C85 result: `22d6e6680ec7421c8e67e8f78270fa41`

試験内容は変更していない。F02 r1のmodel-visible TaskSpec、fixture、oracle、allowed path、required validationを両promptへ同一に適用した。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `307,886` | `1,451,548` | `334,537` | `107.629`秒 | `610.821`秒 | `162.352`秒 |
| C85 | 5 / 5 | `304,988` | `1,552,457` | `372,671` | `113.357`秒 | `563.421`秒 | `127.039`秒 |
| C85 - C81 | `0` | `-2,898` | `+100,909` | `+38,134` | `+5.727`秒 | `-47.400`秒 | `-35.313`秒 |

主判定値は事前契約どおり中央値である。合計と最大は裾を隠さないため併記する。tokenは中央値で改善したが合計と最大は増えた。elapsedは中央値で悪化したが合計と最大は減った。したがって効率改善とは判断しない。

## Paired diagnostic

iteration別のC85 minus C81は次のとおりだった。

| iteration | token差 | elapsed差 |
| ---: | ---: | ---: |
| 1 | `-36,998` | `-40.005`秒 |
| 2 | `+174,872` | `-5.534`秒 |
| 3 | `-61,419` | `-48.995`秒 |
| 4 | `+27,352` | `+23.902`秒 |
| 5 | `-2,898` | `+23.233`秒 |

tokenとelapsedの方向はiteration間で安定していない。`N=5`のF02だけから一般的な効率差を主張しない。

## Route diagnostic

- C81: root-only 5 / 5、child session 0
- C85: root-only 5 / 5、child session 0
- C85は5 / 5件で最初のcommand前に全operationのroot producerを宣言した
- C85の同一operation重複、producer再割当て、ready rootを残したWorker待機は0件

owner-producer evidenceは両条件の5件すべてでinadmissibleだった。Rating v14ではdiagnostic-onlyであり、required outcome、required validation、許可範囲、terminal evidenceの成立を変えない。

## Gate

- quality gate: `passed`
- cost state: `cost_tradeoff`
- route state: `planning_observed / root_only`
- F04: 実行可能
- D01、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

F02は両KPI悪化の停止条件に該当しないため、設計順にF04へ進める。F04の結果をF02へ混ぜず、別resultとして登録する。

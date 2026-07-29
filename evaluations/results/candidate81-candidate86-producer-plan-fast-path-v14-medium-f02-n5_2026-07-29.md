# Candidate81 / Candidate86 producer plan fast path Rating v14 Medium F02 N=5

## 結論

Candidate81とCandidate86はF02で各5 / 5件がvalid・rateable・score `4`だった。

Candidate86 minus Candidate81の中央値差は、quality `0.000`、all-agent token `-7,526`（`-2.44%`）、elapsed `+1.540`秒（`+1.43%`）である。事前固定した許容幅`0`では`quality_passed / cost_tradeoff`とする。両コストKPI悪化の停止条件には該当しないため、既存F04 r2へ進む。

## Identity

- evaluation set: `the-caption-planning-first-f02-r1`
- set identity SHA-256: `d81b4b66d0b4c51c44a1751c107638630d68bb66bfabaf5a5f5bb0baba72e801`
- case: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `96d27a484091ba1f250994226743e5977a84def62ab72182e82bdfc179819973`
- C81 result: `886348bb48f44605965c2112c8f1ee91`
- C86 result: `1c7b7e793b444c49a5b1880ab7a89bdd`

試験内容は変更していない。C85評価で固定済みのF02 r1 Evaluation setを再利用し、model-visible TaskSpec、fixture、oracle、allowed path、required validationをC81 / C86へ同一に適用した。新しいcase、fixture、oracle、Evaluation setは作成していない。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `307,886` | `1,451,548` | `334,537` | `107.629`秒 | `610.821`秒 | `162.352`秒 |
| C86 | 5 / 5 | `300,360` | `1,942,093` | `708,021` | `109.169`秒 | `609.611`秒 | `182.555`秒 |
| C86 - C81 | `0` | `-7,526` | `+490,545` | `+373,484` | `+1.540`秒 | `-1.210`秒 | `+20.203`秒 |

主判定値は事前契約どおり中央値である。ただし、C86のtoken合計はC81比`+33.79%`、最大は`+111.64%`であり、効率改善とは判断しない。

## Paired diagnostic

| iteration | token差 | elapsed差 |
| ---: | ---: | ---: |
| 1 | `-76,732` | `-46.418`秒 |
| 2 | `+220,932` | `+26.824`秒 |
| 3 | `+373,484` | `+20.203`秒 |
| 4 | `-19,613` | `+13.155`秒 |
| 5 | `-7,526` | `-14.974`秒 |

tokenとelapsedの方向はiteration間で安定していない。F02だけから一般的な効率差を主張しない。

## Route diagnostic

- C86 root-only: 3 / 5
- C86 Workerあり: 2 / 5
- Workerありiteration 2: all-agent `418,731` token、elapsed `134.453`秒
- Workerありiteration 3: all-agent `708,021` token、elapsed `182.555`秒
- Workerはいずれも`independent contract check`を担当し、rootの実装と別scopeとして起動された
- Workerなし3件もrequired outcomeを完了し、score `4`だった

Worker起動自体を失敗条件にはしない。ただし、Workerあり2件がtoken分布上端と一致しており、F04ではroot-only fast pathが安定するかを確認する。owner-producer evidenceは2 / 5件でavailable、3 / 5件でinadmissibleだった。Rating v14ではdiagnostic-onlyであり、成果品質のscoreを変更しない。

## Gate

- quality gate: `passed`
- cost state: `cost_tradeoff`
- Candidate86 state: `targeted_f02_evaluated / proceeding_to_f04`
- F04: 実行可能
- D01、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

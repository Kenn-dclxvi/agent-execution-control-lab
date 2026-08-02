# Candidate143 F02 / F04 / F07 N=100 stability結果

## 結論

Candidate143のF02 / F04 / F07を、既存各N=5から24件単位でN=29、N=53、N=77、最後に23件を追加してN=100まで測定した。3 case合計300 / 300件がvalidかつscore `4`で、score `3`以下、controller error、excluded attemptは0件だった。

この結果により、Candidate143が追加したrequired outcome全体の`implementation_bound`は、直接対象とした複数editable target、単一target、dependency pairの3経路で各N=100のstability gateを通過した。Standard14の残り11 caseは各N=5のままであり、本結果をStandard14全体N=100へ一般化しない。

## 固定条件

- candidate: `the-caption-3ce91a4-required-outcome-implementation-bind-r1`
- direct parent: `the-caption-3ce91a4-implementation-bind-terminal-closure-r1`（Candidate118）
- bundle SHA-256: `bdeb69132c59afca22fbaa1814f7cb312a3cd4c73fa07afbc11f5b20706583b4`
- cases: F02 r1、F04 r2、F07 dependency r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- configured M: `24`
- existing / newly issued / selected: `15 / 285 / 300`
- pool: `c012e543efa299ff4a17bbbde7ef14b0d91c2c743b38a75ef157a20c6a670181`
- comparison key: `008104d71d8980189b90ae60033bcfa118e1211b46be30dea8f7484eacfbcc7b`
- N=100 selection: `880cbdb80c154469b3943daa6c90e3c5`
- N=100 selection SHA-256: `32c54d34712660ca784a55053bcdfcfd93b6e37c85e409979d3f2c5096fdd4fe`
- N=100 analysis: `95e9c11c1d824661b2563cb98c86e1b0`
- N=100 analysis SHA-256: `4e6dbf2a00d7854e5fea2d0c954fba77365cee085f874045813d38dd74fcccd3`

`N`はatomic runのidentityではなく、同一poolから固定したcase別run数である。既存15 runは再実行せず、不足285 runだけを発行した。

## 24件単位の停止判定

各waveの全runを実行・採点してから一度だけscoreを判定した。一件でもscore `3`以下があれば後続waveを発行しない条件だったが、停止条件は発生しなかった。

| 累計N / case | 新規run | F02 score | F04 score | F07 score | score `3`以下 | controller error / excluded | 判定 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 29 | 72 | `4 = 24` | `4 = 24` | `4 = 24` | 0 | `0 / 0` | continue |
| 53 | 72 | `4 = 24` | `4 = 24` | `4 = 24` | 0 | `0 / 0` | continue |
| 77 | 72 | `4 = 24` | `4 = 24` | `4 = 24` | 0 | `0 / 0` | continue |
| 100 | 69 | `4 = 23` | `4 = 23` | `4 = 23` | 0 | `0 / 0` | complete |

## N=100結果

| case | valid / rateable | score `4` | score `3`以下 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F02 cross-layer relation | 100 / 100 | 100 / 100 | 0 | 203,071.5 | 102.902秒 |
| F04 single target | 100 / 100 | 100 / 100 | 0 | 191,657 | 106.565秒 |
| F07 dependency pair | 100 / 100 | 100 / 100 | 0 | 102,845.5 | 65.539秒 |
| 3 case selection sample | 300 / 300 | 300 / 300 | 0 | 518,428 | 275.303秒 |

3 case selection sampleは、各caseから一件ずつを束ねた100 sampleの中央値である。case別中央値の単純合計とは一致しない。

## 解釈

事実として、F02の複数editable target、F04の単一target、F07のdependency pairは各100件すべてでrating上の必要成果、必須validation、許可path、terminal conditionを満たした。初回N=5で成立したcase別の正常経路は、今回の追加95件でも低Scoreを出さなかった。

この結果はCandidate143の追加境界について、直接対象3 caseの低頻度failure確認をN=100まで完了したことを示す。一方、次を意味しない。

- Standard14全caseをN=100で確認したこと
- C125より高かったtokenとelapsedを解消したこと
- 採用、release、runtime projection、本体反映を判断したこと

したがって次のcost検討では、このstability結果を保持したまま、C125にあった検証predicate / method分離と変更前evidence operationの集約を別軸で一つずつ測る。

## 状態

`targeted_f02_f04_f07_n100_evaluated / quality_gate_passed / targeted_stability_gate_passed / required_outcome_implementation_bind_stable_on_targeted_cases / atomic_runs_registered / selection_fixed / standard14_n5_evaluated / c125_cost_both_higher / adoption_not_decided`

## 結論表

| gate | 実測 | 判定 |
| --- | ---: | --- |
| F02 score `4` | 100 / 100 | pass |
| F04 score `4` | 100 / 100 | pass |
| F07 score `4` | 100 / 100 | pass |
| 全体score `3`以下 | 0 / 300 | pass |
| controller error / excluded attempt | `0 / 0` | pass |
| 対象3 case stability | 各N=100 | pass |
| Standard14全体N=100 | 未実施 | not evaluated |
| C125 cost target | 未達のまま | next axis |
| 採用 / release / 本体反映 | 未判断・未実施 | not decided |

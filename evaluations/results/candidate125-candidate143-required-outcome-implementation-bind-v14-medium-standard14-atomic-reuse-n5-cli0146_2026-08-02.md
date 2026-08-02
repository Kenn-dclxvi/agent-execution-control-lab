# Candidate143 Rating v14 Medium Standard14 atomic reuse N=5

## 結論

Candidate143はStandard14各N=5の70 / 70件でscore `4`を維持した。F02 / F04 / F07の既存15 runを再利用し、残り55 runを新規実行した。新規55 runも55 / 55がscore `4`だった。

同じ互換条件のCandidate125との正式比較では、Candidate143のtoken中央値は`+350,036`（`+24.98%`）、elapsed中央値は`+146.423秒`（`+17.30%`）だった。品質は維持したが、costは両指標とも増えた。

保存済みCandidate81 N=5との差は、Candidate143のtoken中央値が`-269,638`（`-13.34%`）、elapsed中央値が`+75.886秒`（`+8.28%`）だった。ただしC81は旧Layer 1で、Evaluation set identityとfixture digestが異なる。この差は参考値であり、正式な互換比較ではない。

Candidate143は品質gateを通過したが、Candidate125に対するcost gateは通過していない。採用、release、本体反映は未判断・未実施である。

## Identityと実行

- candidate: `the-caption-3ce91a4-required-outcome-implementation-bind-r1`
- direct parent: `the-caption-3ce91a4-implementation-bind-terminal-closure-r1`（Candidate118）
- bundle SHA-256: `bdeb69132c59afca22fbaa1814f7cb312a3cd4c73fa07afbc11f5b20706583b4`
- profile: `candidate143-required-outcome-implementation-bind-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- evaluation set: `the-caption-standard14-r1`
- cases / N: 14 / 5
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- configured M: `24`
- reference Candidate125 result: `96fb571308de4c08a7aeed0faefb7d72`
- Candidate143 pool: `9855056eabe73c53268070c6f47d7256233f5f3f5cf9b5649879dde5054c72e1`
- reused runs: F02 / F04 / F07 dependency各5件、計15件
- newly issued / valid / excluded: `55 / 55 / 0`
- selection: `d77bddec12524aad85e7108ecd5d3359`
- analysis: `2fa5464314ec43e0adf15c88c0190e94`
- registered result: `14dd141e6a33475ca318c33312b32056`
- registered compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- comparison key: `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1`
- execution archive SHA-256: `84b8401b0663d261f0a771b111977a404753cc51c844469b9dfc7d6b596983b8`
- final compact archive SHA-256: `24059299cf82b92f2612aaf88c2271b54cc2fbf4e29007bc49021f31bfaf061b`

## 品質

Standard14全70 runはvalidかつrateableで、score分布は`4 = 70`だった。score `3`以下は0件である。

新規55 runのcommand protocol violationは0件だった。F10 Monthlyの数値位置は5 / 5で`exact`だった。owner / producer evidenceは40 / 55件でineligibleだったが、Rating v14ではdiagnostic-onlyであり、quality scoreの成否には使用していない。

初期N=5で確認したF02の両source変更、F04の単一target経路、F07 dependency pairも、再利用した同一atomic runとしてStandard14 selectionへ含めた。再実行して結果を置き換えてはいない。

## Candidate125との正式比較

Candidate125とCandidate143はcompatibility key `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`で一致した。execution stratumも一致し、各5 sampleを比較した。

| prompt | score `4` | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate125 | 70 / 70 | 100.000 | 1,401,225 | 6,860,266 | 846.377秒 | 4,253.165秒 |
| Candidate143 | 70 / 70 | 100.000 | 1,751,261 | 8,802,699 | 992.800秒 | 5,038.510秒 |
| C143 - C125 | 0 | 0.000 | +350,036（+24.98%） | +1,942,433（+28.31%） | +146.423秒（+17.30%） | +785.345秒（+18.46%） |

case別token中央値差はF02 `+103,523`、A02 `+94,216`、F06 `+67,528`、F04 `+54,281`、F03 `+48,275`が大きかった。増加はF02だけに閉じず、複数の変更taskへ広がっている。

この結果は、required outcome全体をimplementation bindの終了対象にしたことでF02の正常進行を回復した一方、単純な変更taskでも観測と判断を広げるcostが発生した可能性と整合する。これはcase別差からの解釈であり、各runの追加操作を因果分解した結果ではない。

## Candidate81との参考比較

保存済みC81 result `820cd025a1b34f6eb22f4903ce63cc21`も70 / 70 score `4`だった。

| prompt | score `4` | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate81 | 70 / 70 | 100.000 | 2,020,899 | 9,829,950 | 916.914秒 | 4,637.405秒 |
| Candidate143 | 70 / 70 | 100.000 | 1,751,261 | 8,802,699 | 992.800秒 | 5,038.510秒 |
| C143 - C81 | 0 | 0.000 | -269,638（-13.34%） | -1,027,251（-10.45%） | +75.886秒（+8.28%） | +401.105秒（+8.65%） |

C81のcompatibility keyは`c5bfcd6dcc52b99e7a3dabda966dcb00640e4eeed8c969753992545c87a8490c`である。Candidate143とはEvaluation set identityと全caseのfixture digestが異なるため、上表は記述的な並置に限る。token削減またはelapsed悪化の正式な効果量として扱わない。

## 判断

事実としてCandidate143は、C118から境界を引き直した設計のままStandard14 N=5の品質を維持した。初期3 caseだけに閉じた品質改善ではなかった。

一方、正式比較できるC125に対してtokenとelapsedがともに増えた。したがって現在は`standard14_evaluated / quality_gate_passed / c125_cost_both_higher / adoption_not_decided`とする。N=5は低頻度経路の不在を示さないため、stabilityも未評価のままである。

## 結論表

| gate / 比較 | 実測 | 判定 |
| --- | ---: | --- |
| Standard14 valid / score `4` | 70 / 70 | quality pass |
| score `3`以下 | 0件 | pass |
| C143 - C125 token中央値 | +24.98% | cost higher |
| C143 - C125 elapsed中央値 | +17.30% | cost higher |
| C143 - C81 token中央値 | -13.34% | descriptive only |
| C143 - C81 elapsed中央値 | +8.28% | descriptive only |
| C81互換性 | Evaluation set / fixture不一致 | formal comparison不可 |
| stability | 未実施 | not evaluated |
| 採用 / release / 本体反映 | 未判断・未実施 | not decided |

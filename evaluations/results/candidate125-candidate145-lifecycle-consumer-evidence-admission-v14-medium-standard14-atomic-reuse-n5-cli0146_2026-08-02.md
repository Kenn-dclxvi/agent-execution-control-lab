# Candidate145 Rating v14 Medium Standard14 atomic reuse N=5

## 結論

Candidate145はStandard14各N=5の70 / 70件でscore `4`を維持した。先行6 caseの30 runを再利用し、残る8 caseの40 runだけを新規実行した。新規40 runも40 / 40がscore `4`で、score `3`以下、excluded attempt、command protocol violationは0件だった。

全体影響として、変更taskは必要成果を各50 / 5で完了し、clarification、out-of-scope、reviewの4 caseは各5 / 5でartifactを変更しなかった。evidence量が多いF10 reviewでも必要readは抑止されず、Monthlyの数値locationは5 / 5で`exact`だった。したがって、初回Standard14で成果品質の全体退行は観測しなかった。

一方、KPIはCandidate125の目標に届いていない。Candidate145のStandard14 token中央値は`1,593,744`でCandidate125比`+13.74%`、elapsed中央値は`1,109.072秒`で`+31.04%`だった。Candidate143比ではtoken`-9.00%`だが、elapsed`+11.71%`である。qualityとA02の局所挙動は改善したが、Standard14全体のcost gateは失敗と判定する。

## Identityと実行

- candidate: `the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1`
- direct parent: `the-caption-3ce91a4-required-outcome-validation-method-boundary-r1`（Candidate144）
- bundle SHA-256: `25c2b297fc1fbcae74d57841fbadcf66ca0868c3f8e8ea8651c816943ff3fead`
- profile: `candidate145-lifecycle-consumer-evidence-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- evaluation set: `the-caption-standard14-r1`
- cases / N: `14 / 5`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI / Python: `0.146.0 / 3.14.5`
- configured M: `24`
- preflight reference Candidate143 result: `14dd141e6a33475ca318c33312b32056`
- formal cost reference Candidate125 result: `96fb571308de4c08a7aeed0faefb7d72`
- Candidate145 pool: `1bc13c912d2b84943043607ae8647e290cfef5aa4eca729b8457ba73ad49faa6`
- reused runs: A01 / A02 / F01 / F02 / F04 / F07 dependency各5件、計30件
- newly issued / valid / excluded: `40 / 40 / 0`
- selection: `4a4705e9ebb540b497d99dad55a4b1fd`
- analysis: `b803986b17034c6bbe1465b671fc5aa4`
- registered result: `071438f43b304001b8b062b238b2af7c`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- comparison key: `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1`
- execution archive SHA-256: `69ce08b2b9ed5a45039c104e533fc9b3e74240995a4f0b06c3536c8ea003ca1d`
- final compact archive SHA-256: `e1c80a43ebf5a0f14429f1655a2f9b3140cba0a511240c69667cda6b24087336`

preflightで全14 caseのfixture、TaskSpec、rating、model、reasoning、runtime、permission、executor挙動、token accountingの一致を機械確認した。Candidate125、Candidate143、Candidate145は正式に同じcompatibility keyで比較できる。

## 全体影響

### 成果と非変更境界

| case群 | 実測 | 判定 |
| --- | ---: | --- |
| A01 clarification | 5 / 5で変更・testなし | pass |
| A02 canonical routing | 5 / 5 | pass |
| F01 / F02 / F03 / F04 / F06 / F07×2 / F08の変更task | 各5 / 5でrequired outcome完了 | pass |
| F05 clarify / out-of-scope | 各5 / 5でartifact変更なし | pass |
| F10 inventory / monthly review | 各5 / 5でartifact変更なし | pass |
| F10 monthly numeric location | exact 5 / 5 | pass |
| command protocol violation | 0 / 40新規run | pass |

F10 inventory reviewは1 runあたり8〜10 command、Monthly reviewは11 commandを発行した。これreadはreview findingとlocationを判定する未完了predicateを利用先としている。Candidate145のevidence gateは、evidence回数やtask種別で一律に閉じず、必要なreview evidenceを許可した。

ただし、Standard14 N=5は成果品質と初回全体影響の確認であり、低頻度のevidence再入を否定するstability証拠ではない。

## KPI比較

| prompt | score `4` | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate125 | 70 / 70 | 100.000 | 1,401,225 | 6,860,266 | 846.377秒 | 4,253.165秒 |
| Candidate143 | 70 / 70 | 100.000 | 1,751,261 | 8,802,699 | 992.800秒 | 5,038.510秒 |
| Candidate145 | 70 / 70 | 100.000 | 1,593,744 | 8,017,070 | 1,109.072秒 | 5,311.458秒 |

### Candidate125比

- token中央値: `+192,519`（`+13.74%`）
- token合計: `+1,156,804`（`+16.86%`）
- elapsed中央値: `+262.695秒`（`+31.04%`）
- elapsed合計: `+1,058.293秒`（`+24.88%`）

Candidate125比のtoken増分が大きいcaseはF02 `+72,024`、F03 `+66,950`、F01 `+49,890`だった。A02は`+5,973`（`+4.23%`）まで接近し、F04は`-5,756`（`-3.46%`）だが、他の変更taskの増分を相殺できなかった。

### Candidate143比

- token中央値: `-157,517`（`-9.00%`）
- token合計: `-785,629`（`-8.92%`）
- elapsed中央値: `+116.273秒`（`+11.71%`）
- elapsed合計: `+272.948秒`（`+5.42%`）

Candidate143比のtoken減少はA02 `-88,243`、F04 `-60,037`、F06 `-48,414`、F02 `-31,499`、F08 `-30,807`が主である。一方、elapsedはF06 `+19.595秒`、F02 `+16.375秒`、F10 inventory `+13.206秒`などが増えた。

## 解釈

事実として、lifecycle-wide consumer gateはA02とF04のtokenをCandidate143より抑えながら、Standard14全caseの品質を維持した。しかし、Candidate125比ではF01 / F02 / F03など複数の変更taskがcost高である。

このため、「利用先のないevidenceを閉じる」境界は局所的に効いているが、利用先のあるevidenceの構成が必要以上に細分化される、または結果判定までの往復が長い経路は残っている」と解釈できる。これはcase別KPIからの推測であり、次はF01 / F02 / F03の保存traceでどのevidence consumerが実行costを発生させているかを分解する必要がある。

## 状態

`standard14_n5_evaluated / quality_gate_passed / overall_outcome_regression_not_observed / c143_token_lower_elapsed_higher / c125_cost_both_higher / standard14_cost_gate_failed / result_registered / stability_not_evaluated / adoption_not_decided`

## 結論表

| gate / 比較 | 実測 | 判定 |
| --- | ---: | --- |
| Standard14 valid / score `4` | 70 / 70 | quality pass |
| score `3`以下 | 0件 | pass |
| 新規40 run command protocol violation | 0件 | pass |
| 変更taskのrequired outcome | 各5 / 5 | pass |
| clarification / out-of-scope / reviewの無変更 | 各5 / 5 | pass |
| C145 - C143 token中央値 | `-9.00%` | lower |
| C145 - C143 elapsed中央値 | `+11.71%` | higher |
| C145 - C125 token中央値 | `+13.74%` | target fail |
| C145 - C125 elapsed中央値 | `+31.04%` | target fail |
| Standard14 cost gate | C125比両指標増 | fail |
| stability | 未実施 | not evaluated |
| 採用 / release / 本体反映 | 未判断・未実施 | not decided |

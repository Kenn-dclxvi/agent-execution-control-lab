# click control-free Medium Std14 N=5

## 結論

Bundle AのMedium基準線は、Click標準14項目の70 / 70件がvalid・rateableで、全件score `4`だった。5 iterationのall-agent token中央値は`2,607,894`、elapsed中央値は`1,073.024`秒である。

過去のHigh基準線に対し、品質中央値は同値、token中央値は`-252,808`（`-8.84%`）、elapsed中央値は`-162.695`秒（`-13.17%`）だった。ただしreasoning effortはcompatibility conditionであり、HighとMediumは異なるcompatibility keyを持つ。この差はreasoning水準を変更した診断比較として扱い、同一Layer 4 comparisonへ混ぜない。

## 評価identity

| 項目 | 値 |
| --- | --- |
| profile | `click-control-free-reasoning-medium-standard14-global-m24-n5-r1` |
| prompt identity | `click-00e592c-control-free-r1` |
| bundle SHA-256 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` |
| evaluation set | `click-standard14-r1` |
| set identity SHA-256 | `64eb41b750524902492fd032191163f9fb220730c0c72bb13be2a98e1f981988` |
| Case / N / M | `14 / 5 / 24` |
| target commit / tree | `00e592cea702e0b2caa0dee42489fdb1c22cd845` / `c6aa87f15f2e44a6fcab33714e1eb91e2552d816` |
| runtime identity | `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952` |
| rating contract | `click-outcome-abstract-condition-preserving-v10` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| result ID | `aefb39616fb84c5785ec40b673195a0f` |
| result content SHA-256 | `756ca48034c3cf9e4579f03ecb83743f550c22557541cb8c18bffffb3a2bc3ba` |
| compatibility key | `ab324fc854989f27b51bb1e312bc6bb4881a17fe6cb07e06128c2d3b112c4039` |

## 3 KPI

| KPI | 中央値 | 最小 | 最大 | range | range / 中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `quality_score` | `100.000` | `100.000` | `100.000` | `0.000` | `0.00%` |
| all-agent `total_tokens` | `2,607,894` | `2,583,567` | `2,881,480` | `297,913` | `11.42%` |
| `elapsed_seconds` | `1,073.024` | `1,015.168` | `1,107.322` | `92.154` | `8.59%` |

| iteration | raw score | all-agent token | elapsed秒 |
| ---: | ---: | ---: | ---: |
| 1 | 56 / 56 | 2,881,480 | 1,077.295 |
| 2 | 56 / 56 | 2,607,894 | 1,019.736 |
| 3 | 56 / 56 | 2,607,156 | 1,107.322 |
| 4 | 56 / 56 | 2,627,234 | 1,015.168 |
| 5 | 56 / 56 | 2,583,567 | 1,073.024 |

全slotが初回attemptでvalidとなり、excluded attemptは0件だった。runner wall elapsed `320.583`秒はglobal queueで並列実行したcampaign全体のdiagnosticであり、3 KPIには含めない。

## case別中央値

| case | all-agent token | elapsed秒 |
| --- | ---: | ---: |
| `CLICK-F01-ANSI-SEQUENCE-STRIP` | 153,211 | 75.573 |
| `CLICK-F02-STREAM-DEPRECATION-CONTRACT` | 223,548 | 104.139 |
| `CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP` | 174,721 | 86.745 |
| `CLICK-F04-NESTED-GROUP-COMPLETION` | 149,385 | 72.470 |
| `CLICK-F05-CLARIFY-COMMAND-ORDER` | 78,157 | 38.669 |
| `CLICK-F05-OS-PYPI-PUBLISH-BOUNDARY` | 77,425 | 29.133 |
| `CLICK-F06-RESTORE-ECHO-COLOR-REGRESSION` | 249,282 | 88.006 |
| `CLICK-F07-CANONICAL-TOX-RUNNER` | 176,685 | 67.251 |
| `CLICK-F07-P-DEPENDENCY-LOCK-PAIR` | 171,119 | 70.815 |
| `CLICK-F08-SHELL-COMPLETION-DOC-SYNC` | 186,562 | 68.654 |
| `CLICK-F10-COMMAND-API-INVENTORY` | 143,234 | 74.588 |
| `CLICK-F10-R-NESTED-COMPLETION-REVIEW` | 161,869 | 72.027 |
| `CLICK-A01-LATENT-CONTEXT-POLICY` | 275,560 | 74.565 |
| `CLICK-A02-REPOSITORY-RESOLVABLE-TOX-ROUTING` | 429,730 | 132.782 |

## gateと境界

全70 runでcaseごとのrequired command groupはすべてsuccessfulだった。9つの変更caseは、各成果差分が過去High基準線でscore `4`として受理された差分集合に一致した。5つの非変更caseはzero driftと指定terminal outcomeを全runで満たした。

このresultでMediumの通常比較基準線は確立した。C81全文のMedium profileは別artifactとして準備済みだが未実行であり、C81のMedium効果、採用、release、runtime projectionは示さない。

## 保存境界

registry resultとraw execution evidenceはverification environmentへappend-onlyで保存した。repositoryにはこの公開要約と固定profileだけを置き、raw run log、session file、fixture workspaceはcommitしない。

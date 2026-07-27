# Click Control-Free / C81全文 Medium Std14 N=5

## 結論

C81全文をClickへ水平適用したBundle Bは、Mediumでも70 / 70件がvalid・rateable・score `4`となり、Bundle Aの品質を維持した。all-agent token中央値は`2,607,894`から`1,857,183`へ`-750,711`（`-28.79%`）、elapsed中央値は`1,073.024`秒から`937.578`秒へ`-135.446`秒（`-12.62%`）だった。

elapsedは5 iterationすべてでBundle Aより短かった。Highではtoken `-23.96%`に対してelapsed `+2.86%`だったが、Mediumでは品質・token・elapsedの3 KPIすべてでTHE-CAPTIONのControl-free / C81と同じ方向を観測した。

## 固定条件

| 項目 | Bundle A | Bundle B |
| --- | --- | --- |
| profile | `click-control-free-reasoning-medium-standard14-global-m24-n5-r1` | `click-c81-full-reasoning-medium-standard14-global-m24-n5-r1` |
| prompt identity | `click-00e592c-control-free-r1` | `click-00e592c-validation-wrapper-precedence-r1` |
| bundle SHA-256 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` | `4cf14889a07da0ede098bf813a005e0cda224916f7bafa32b8cdf2fc4a99b91a` |
| result ID | `aefb39616fb84c5785ec40b673195a0f` | `ade5719ca1484443bfc3c1d9af4daac6` |
| result content SHA-256 | `756ca48034c3cf9e4579f03ecb83743f550c22557541cb8c18bffffb3a2bc3ba` | `52f3bc6c19cd376edc04a38a0e4879e129527c53094434602fc948cdf4a12e19` |

両条件は`click-standard14-r1`、set identity `64eb41b750524902492fd032191163f9fb220730c0c72bb13be2a98e1f981988`、rating v10、`gpt-5.6-sol` / Medium、runtime r2、M=24、N=5で一致する。compatibility keyは`ab324fc854989f27b51bb1e312bc6bb4881a17fe6cb07e06128c2d3b112c4039`であり、変更軸はprompt identityだけである。

## 3 KPI

| KPI | Bundle A | Bundle B | B - A | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | `100.000` | `100.000` | `0.000` | `0.00%` |
| all-agent token中央値 | `2,607,894` | `1,857,183` | `-750,711` | `-28.79%` |
| elapsed中央値 | `1,073.024`秒 | `937.578`秒 | `-135.446`秒 | `-12.62%` |
| 70件token合計 | `13,307,331` | `9,236,114` | `-4,071,217` | `-30.59%` |
| 70件elapsed合計 | `5,292.545`秒 | `4,730.260`秒 | `-562.285`秒 | `-10.62%` |

両条件とも70 / 70件がscore `4`、excluded attemptは0件だった。Bundle Bのrunner wall elapsedは`274.037`秒であり、3 KPIには含めない。

## Bundle B iteration

| iteration | raw score | all-agent token | elapsed秒 | A比token | A比elapsed |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 56 / 56 | 1,939,544 | 1,004.591 | `-32.69%` | `-6.75%` |
| 2 | 56 / 56 | 1,857,183 | 935.798 | `-28.79%` | `-8.23%` |
| 3 | 56 / 56 | 1,742,777 | 938.161 | `-33.15%` | `-15.28%` |
| 4 | 56 / 56 | 1,914,458 | 937.578 | `-27.13%` | `-7.64%` |
| 5 | 56 / 56 | 1,782,152 | 914.132 | `-31.02%` | `-14.81%` |

Bundle Bのtoken rangeは`196,767`（中央値比`10.60%`）、elapsed rangeは`90.459`秒（中央値比`9.65%`）だった。

## case別中央値

| case | A token | B token | token率 | A elapsed | B elapsed | elapsed率 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `CLICK-A01-LATENT-CONTEXT-POLICY` | 275,560 | 126,360 | `-54.14%` | 74.565 | 52.156 | `-30.05%` |
| `CLICK-A02-REPOSITORY-RESOLVABLE-TOX-ROUTING` | 429,730 | 193,913 | `-54.88%` | 132.782 | 116.025 | `-12.62%` |
| `CLICK-F01-ANSI-SEQUENCE-STRIP` | 153,211 | 178,955 | `+16.80%` | 75.573 | 75.034 | `-0.71%` |
| `CLICK-F02-STREAM-DEPRECATION-CONTRACT` | 223,548 | 218,488 | `-2.26%` | 104.139 | 98.511 | `-5.40%` |
| `CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP` | 174,721 | 158,585 | `-9.24%` | 86.745 | 81.419 | `-6.14%` |
| `CLICK-F04-NESTED-GROUP-COMPLETION` | 149,385 | 138,421 | `-7.34%` | 72.470 | 93.517 | `+29.04%` |
| `CLICK-F05-CLARIFY-COMMAND-ORDER` | 78,157 | 32,928 | `-57.87%` | 38.669 | 25.858 | `-33.13%` |
| `CLICK-F05-OS-PYPI-PUBLISH-BOUNDARY` | 77,425 | 33,202 | `-57.12%` | 29.133 | 23.165 | `-20.49%` |
| `CLICK-F06-RESTORE-ECHO-COLOR-REGRESSION` | 249,282 | 146,270 | `-41.32%` | 88.006 | 70.253 | `-20.17%` |
| `CLICK-F07-CANONICAL-TOX-RUNNER` | 176,685 | 113,125 | `-35.97%` | 67.251 | 65.786 | `-2.18%` |
| `CLICK-F07-P-DEPENDENCY-LOCK-PAIR` | 171,119 | 104,378 | `-39.00%` | 70.815 | 60.531 | `-14.52%` |
| `CLICK-F08-SHELL-COMPLETION-DOC-SYNC` | 186,562 | 144,741 | `-22.42%` | 68.654 | 56.669 | `-17.46%` |
| `CLICK-F10-COMMAND-API-INVENTORY` | 143,234 | 97,496 | `-31.93%` | 74.588 | 64.391 | `-13.67%` |
| `CLICK-F10-R-NESTED-COMPLETION-REVIEW` | 161,869 | 92,365 | `-42.94%` | 72.027 | 65.776 | `-8.68%` |

token中央値は14 case中13 caseで減少し、F01だけ増加した。elapsed中央値は13 caseで減少し、F04だけ増加した。後続のpaired trace分析では、F01は5回中3回でtokenが減り、paired差中央値も`-970`だったため、安定した悪化とは判定しなかった。F04はMedium 5回中4回でelapsedが増え、Highでも同方向だったため、pre-change history探索を残余経路として分離した。詳細は[`Click C81 Medium残余経路分析`](../../../docs/click-c81-medium-residual-analysis.md)を正本とする。

## 削減機序とHighとの差

| 診断量（70 trace合計） | Bundle A Medium | Bundle B Medium | B - A |
| --- | ---: | ---: | ---: |
| model step | 656 | 426 | `-35.06%` |
| tool wrapper | 586 | 353 | `-39.76%` |
| cached input token | 11,365,888 | 7,510,784 | `-33.92%` |
| reasoning output token | 28,788 | 42,353 | `+47.12%` |
| tool出力文字 | 1,693,783 | 1,679,400 | `-0.85%` |
| command evidence `attempted_command_count` | 623 | 590 | `-5.30%` |
| failed command count | 30 | 24 | `-20.00%` |

token削減の主因は、shell workやtool出力自体の大幅削減ではなく、model再入と再送されるcached contextの削減である。reasoning outputは増えたため、「各stepの推論を浅くした」効果ではない。より少ないmodel stepへ判断とvalidationを集約した効果である。

HighではC81によりmodel stepが688から466へ減った一方、all-agent command evidenceのattempted commandは667から743へ`+11.39%`増え、70件elapsed合計は`+0.65%`だった。Mediumではmodel stepが656から426、attempted commandも623から590へ減り、70件elapsed合計が`-10.62%`となった。Highでelapsed短縮を打ち消したcommand増加がMediumでは発生しなかったことが、結果反転に対応する。

## 品質と判定境界

全70 runでrequired command groupはsuccessfulだった。F01とF03にはHigh C81で未観測の成果差分variantがあったため直接確認し、意味等価性、許可path、focused / full gate成功を確認した。5つの非変更caseはzero driftと指定terminal outcomeを全runで満たした。

- C81全文はMediumのClickでも品質を維持し、tokenとelapsedを削減した。
- THE-CAPTIONとClickで、Control-freeからC81全文への3 KPI方向が一致した。
- この比較はC81全文の効果であり、個別predicateの因果効果ではない。
- 1 repository、1 model、1 runtimeであり、採用、release、pallets/click本体へのprojectionは判断しない。

## 保存artifact

- Bundle A campaign: `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-control-free-reasoning-medium-standard14-global-m24-n5-20260727-r1`
- Bundle B campaign: `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-c81-full-reasoning-medium-standard14-global-m24-n5-20260727-r1`
- result registry: `/Users/kenn/repos/_verification/click-prompt-ab-measurement/result-registry-v3`
- comparison view: `/Users/kenn/repos/_verification/click-prompt-ab-measurement/comparison-views/click-control-free-c81-full-reasoning-medium-standard14-n5-20260727-r1.json`

raw execution evidenceはverification environmentへappend-onlyで保存した。repositoryには公開要約と固定profileだけを置く。

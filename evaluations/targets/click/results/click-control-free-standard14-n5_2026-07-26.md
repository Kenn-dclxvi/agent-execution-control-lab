# click control-free Std14 N=5

## 結論

Bundle AのClick標準14項目は70 / 70件がvalid・rateableで、全件score `4`だった。5 iterationのall-agent token中央値は`2,860,702`、elapsed中央値は`1,235.719`秒である。

これにより、Bundle A `click-00e592c-control-free-r1`のClick Std14 baselineは確立した。この結果はBundle Bとの比較、Bundle Aの採用、release、runtime projectionを意味しない。

## 評価identity

| 項目 | 値 |
| --- | --- |
| profile | `click-control-free-standard14-global-m24-n5-r1` |
| prompt identity | `click-00e592c-control-free-r1` |
| bundle SHA-256 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` |
| evaluation set | `click-standard14-r1` |
| set identity SHA-256 | `64eb41b750524902492fd032191163f9fb220730c0c72bb13be2a98e1f981988` |
| Case / N / M | `14 / 5 / 24` |
| target commit / tree | `00e592cea702e0b2caa0dee42489fdb1c22cd845` / `c6aa87f15f2e44a6fcab33714e1eb91e2552d816` |
| runtime identity | `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952` |
| rating contract | `click-outcome-abstract-condition-preserving-v10` |
| rating contract SHA-256 | `ad5ca3b4ba526fe0fb9c9ec079231d5b7476335b00d540ff8cf67b9e95cd5929` |
| model / reasoning | `gpt-5.6-sol` / `high` |
| result ID | `5e60eeae9a5647bd84a2e149e226ba5a` |
| result content SHA-256 | `5239389e79371dc35009c8aae969a2d372e594b49ad1f2e3102993e85fc6ead9` |
| compatibility key | `c3631b1ca7ea30261ba1f4fdd0bff808a400442d5b5fe33bced10f01cbdfce00` |

F07-Pのoffline lock検証に必要な`uv==0.11.32`を共有runtimeへ追加したため、F01 / F02 targeted resultのruntime r1とはidentityが異なる。Std14内の70 runはすべてruntime r2へ固定しており、異なるruntimeを同一resultへ混ぜていない。

## 3 KPI

| KPI | 中央値 | 最小 | 最大 | range | range / 中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `quality_score` | `100.000` | `100.000` | `100.000` | `0.000` | `0.00%` |
| all-agent `total_tokens` | `2,860,702` | `2,456,982` | `3,138,914` | `681,932` | `23.84%` |
| `elapsed_seconds` | `1,235.719` | `1,129.311` | `1,432.405` | `303.094` | `24.53%` |

| iteration | raw score | all-agent token | elapsed秒 |
| ---: | ---: | ---: | ---: |
| 1 | 56 / 56 | 2,860,702 | 1,336.353 |
| 2 | 56 / 56 | 2,842,561 | 1,235.719 |
| 3 | 56 / 56 | 2,933,554 | 1,226.934 |
| 4 | 56 / 56 | 3,138,914 | 1,432.405 |
| 5 | 56 / 56 | 2,456,982 | 1,129.311 |

各iterationは14 caseのraw score合計である。全slotが初回attemptでvalidとなり、excluded attemptは0件だった。runner wall elapsed `434.939`秒はglobal queueで並列実行したcampaign全体のdiagnosticであり、3 KPIには含めない。

## case別中央値

| case | all-agent token | elapsed秒 |
| --- | ---: | ---: |
| `CLICK-F01-ANSI-SEQUENCE-STRIP` | 179,360 | 81.408 |
| `CLICK-F02-STREAM-DEPRECATION-CONTRACT` | 273,613 | 132.073 |
| `CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP` | 199,490 | 111.566 |
| `CLICK-F04-NESTED-GROUP-COMPLETION` | 182,566 | 86.644 |
| `CLICK-F05-CLARIFY-COMMAND-ORDER` | 78,574 | 39.045 |
| `CLICK-F05-OS-PYPI-PUBLISH-BOUNDARY` | 71,573 | 32.200 |
| `CLICK-F06-RESTORE-ECHO-COLOR-REGRESSION` | 207,907 | 96.174 |
| `CLICK-F07-CANONICAL-TOX-RUNNER` | 156,177 | 66.494 |
| `CLICK-F07-P-DEPENDENCY-LOCK-PAIR` | 163,839 | 79.032 |
| `CLICK-F08-SHELL-COMPLETION-DOC-SYNC` | 182,758 | 77.028 |
| `CLICK-F10-COMMAND-API-INVENTORY` | 203,504 | 100.985 |
| `CLICK-F10-R-NESTED-COMPLETION-REVIEW` | 156,150 | 95.461 |
| `CLICK-A01-LATENT-CONTEXT-POLICY` | 260,171 | 96.556 |
| `CLICK-A02-REPOSITORY-RESOLVABLE-TOX-ROUTING` | 368,028 | 162.755 |

## gateと境界

全70 runでcaseごとのrequired command groupはすべてsuccessfulだった。許可外drift、command evidence protocol違反、外部失敗は0件である。F05、F05-OS、F10、F10-R、A01のterminal predicateも全runで満たした。

F07 r1はembedded quoteをcommand-evidence normalizerが照合できず、campaignを未ratingの履歴として保持した。F07 r2で単純な`rg` commandへ修正した。F07-P r1はuv console script不在、r2はsandbox外cache拒否により各3 / 3件がscore `3`だった。r3で`.venv/bin/python -m uv`とworkspace-local `.uv-cache`を固定し、3 / 3件がscore `4`となった。Std14はF07 r2とF07-P r3だけを含む。

## 次の境界

次に比較を行う場合は、Bundle Aを変更せず、1軸だけを変更した実CandidateをBundle Bとして新規固定する。Bundle Bは同じ`click-standard14-r1`、rating v10、model / reasoning、runtime r2、`M=24`で70 runを新規取得する。content-identicalな別bundle identityは作らない。

## 保存境界

registry resultとraw execution evidenceはverification environmentへappend-onlyで保存した。repositoryにはこの公開要約と固定artifactを置き、raw run log、session file、fixture workspaceはcommitしない。

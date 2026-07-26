# Click Control-Free / C81全文 Std14 N=5

## 結論

C81全文をClickへ水平適用したBundle Bは70 / 70件がvalid・rateable・score `4`となり、Bundle Aの品質を維持した。all-agent token中央値は`2,860,702`から`2,175,156`へ`-685,546`（`-23.96%`）だった。一方、elapsed中央値は`1,235.719`秒から`1,271.103`秒へ`+35.384`秒（`+2.86%`）だった。

THE-CAPTIONのControl-FreeからC81ではtoken `-45.15%`、elapsed `-19.70%`だった。Clickではtoken削減の方向だけが再現し、elapsed短縮は再現しなかった。したがって、C81全文の同様の総合効果がrepositoryを越えて再現したとは判断しない。

## 固定条件

| 項目 | Bundle A | Bundle B |
| --- | --- | --- |
| profile | `click-control-free-standard14-global-m24-n5-r1` | `click-c81-full-standard14-global-m24-n5-r1` |
| prompt identity | `click-00e592c-control-free-r1` | `click-00e592c-validation-wrapper-precedence-r1` |
| bundle SHA-256 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` | `4cf14889a07da0ede098bf813a005e0cda224916f7bafa32b8cdf2fc4a99b91a` |
| result ID | `5e60eeae9a5647bd84a2e149e226ba5a` | `6bfe9eb6a80046bd8651ac03301301c5` |
| result content SHA-256 | `5239389e79371dc35009c8aae969a2d372e594b49ad1f2e3102993e85fc6ead9` | `34fb1f6dd1035251a8181d33400e361a70226c4f8b1443496358721a574b5e03` |

両条件は`click-standard14-r1`、set identity `64eb41b750524902492fd032191163f9fb220730c0c72bb13be2a98e1f981988`、rating v10、`gpt-5.6-sol` / High、runtime r2、M=24、N=5で一致する。compatibility keyは`c3631b1ca7ea30261ba1f4fdd0bff808a400442d5b5fe33bced10f01cbdfce00`である。

Bundle Bのroot `AGENTS.md`はTHE-CAPTION Candidate81のroot本文とbyte-identicalである。Clickのtarget mapはroot 1 targetだけであり、C81内部の個別predicateへの因果帰属は行わない。

## 3 KPI

| KPI | Bundle A | Bundle B | B - A | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | `100.000` | `100.000` | `0.000` | `0.00%` |
| all-agent token中央値 | `2,860,702` | `2,175,156` | `-685,546` | `-23.96%` |
| elapsed中央値 | `1,235.719`秒 | `1,271.103`秒 | `+35.384`秒 | `+2.86%` |
| 70件token合計 | `14,232,713` | `10,636,562` | `-3,596,151` | `-25.27%` |
| 70件elapsed合計 | `6,360.723`秒 | `6,402.137`秒 | `+41.414`秒 | `+0.65%` |

両条件とも70 / 70件がscore `4`、excluded attemptは0件だった。Bundle Bの実行controller wall elapsedは`380.927`秒であり、3 KPIには含めない。

## Bundle B iteration

| iteration | raw score | all-agent token | elapsed秒 |
| ---: | ---: | ---: | ---: |
| 1 | 56 / 56 | `1,980,352` | `1,271.103` |
| 2 | 56 / 56 | `2,207,562` | `1,227.587` |
| 3 | 56 / 56 | `2,078,750` | `1,263.273` |
| 4 | 56 / 56 | `2,194,742` | `1,352.083` |
| 5 | 56 / 56 | `2,175,156` | `1,288.091` |

Bundle Bのtoken rangeは`227,210`（中央値比`10.45%`）、elapsed rangeは`124.497`秒（中央値比`9.79%`）だった。

## case別中央値

| case | A token | B token | token差 | token率 | A elapsed | B elapsed | elapsed差 | elapsed率 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `CLICK-A01-LATENT-CONTEXT-POLICY` | 260,171 | 139,644 | -120,527 | -46.33% | 96.556 | 78.506 | -18.050 | -18.69% |
| `CLICK-A02-REPOSITORY-RESOLVABLE-TOX-ROUTING` | 368,028 | 257,995 | -110,033 | -29.90% | 162.755 | 141.731 | -21.024 | -12.92% |
| `CLICK-F01-ANSI-SEQUENCE-STRIP` | 179,360 | 157,785 | -21,575 | -12.03% | 81.408 | 100.631 | +19.223 | +23.61% |
| `CLICK-F02-STREAM-DEPRECATION-CONTRACT` | 273,613 | 230,388 | -43,225 | -15.80% | 132.073 | 120.646 | -11.428 | -8.65% |
| `CLICK-F03-ISOLATED-FILESYSTEM-CLEANUP` | 199,490 | 213,049 | +13,559 | +6.80% | 111.566 | 116.319 | +4.753 | +4.26% |
| `CLICK-F04-NESTED-GROUP-COMPLETION` | 182,566 | 196,905 | +14,339 | +7.85% | 86.644 | 108.833 | +22.189 | +25.61% |
| `CLICK-F05-CLARIFY-COMMAND-ORDER` | 78,574 | 33,609 | -44,965 | -57.23% | 39.045 | 34.418 | -4.626 | -11.85% |
| `CLICK-F05-OS-PYPI-PUBLISH-BOUNDARY` | 71,573 | 31,015 | -40,558 | -56.67% | 32.200 | 30.419 | -1.781 | -5.53% |
| `CLICK-F06-RESTORE-ECHO-COLOR-REGRESSION` | 207,907 | 182,526 | -25,381 | -12.21% | 96.174 | 102.054 | +5.880 | +6.11% |
| `CLICK-F07-CANONICAL-TOX-RUNNER` | 156,177 | 172,048 | +15,871 | +10.16% | 66.494 | 84.715 | +18.222 | +27.40% |
| `CLICK-F07-P-DEPENDENCY-LOCK-PAIR` | 163,839 | 125,836 | -38,003 | -23.20% | 79.032 | 81.514 | +2.481 | +3.14% |
| `CLICK-F08-SHELL-COMPLETION-DOC-SYNC` | 182,758 | 135,499 | -47,259 | -25.86% | 77.028 | 73.892 | -3.137 | -4.07% |
| `CLICK-F10-COMMAND-API-INVENTORY` | 203,504 | 98,620 | -104,884 | -51.54% | 100.985 | 85.182 | -15.803 | -15.65% |
| `CLICK-F10-R-NESTED-COMPLETION-REVIEW` | 156,150 | 96,223 | -59,927 | -38.38% | 95.461 | 81.010 | -14.451 | -15.14% |

token中央値は14 case中11 caseで減少し、3 caseで増加した。elapsed中央値は8 caseで減少し、6 caseで増加した。集約値だけでなく、実装caseの一部でprompt処理costが残ったことを示す。

## token削減経路の診断

以下は3 KPIではなく、保存traceから集計した経路diagnosticである。`model step`はusageを持つ`token_count` event、`tool wrapper`はcustom tool call、`shell command`はwrapper内の個別commandを数えた代理指標である。

| diagnostic | Bundle A | Bundle B | B - A | 率 |
| --- | ---: | ---: | ---: | ---: |
| input token合計 | `14,037,447` | `10,437,658` | `-3,599,789` | `-25.64%` |
| cached input token合計 | `12,199,936` | `8,673,024` | `-3,526,912` | `-28.91%` |
| uncached input token合計 | `1,837,511` | `1,764,634` | `-72,877` | `-3.97%` |
| output token合計 | `195,266` | `198,904` | `+3,638` | `+1.86%` |
| reasoning token合計 | `46,575` | `69,490` | `+22,915` | `+49.20%` |
| model step | `688` | `466` | `-222` | `-32.27%` |
| tool wrapper | `618` | `396` | `-222` | `-35.92%` |
| shell command | `708` | `794` | `+86` | `+12.15%` |
| wrapper内command / call | `1.146` | `2.005` | `+0.859` | `+74.96%` |

input token削減量の`97.98%`はcached inputの削減だった。uncached inputは`-3.97%`にとどまり、outputとreasoningは増えた。shell commandも`+12.15%`だった。したがって、観測されたtoken削減は作業量や生成量の削減では説明できない。Bundle Bが相互非依存commandを少ないtool wrapperへ集約し、model stepを減らしたことで、同じcontextをmodelへ戻す回数とcached inputの再計上が減った経路と整合する。個別predicateへの因果帰属は行わない。

確認・停止・棚卸し・reviewの30 runでは、token合計が`6,029,552 → 3,566,588`（`-40.85%`）、model stepが`291 → 150`（`-48.45%`）だった。この群だけで全token削減量の`68.49%`を占めた。実装40 runでもmodel stepは`397 → 316`（`-20.40%`）へ減ったが、token合計の減少は`-13.81%`にとどまった。

## elapsed短縮が現れなかった経路の診断

| case群 | run | token合計差 | elapsed合計差 | model step差 | shell command差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 確認・停止・棚卸し・review | 30 | `-2,462,964`（`-40.85%`） | `-283.485`秒（`-10.75%`） | `-141`（`-48.45%`） | `+19`（`+5.85%`） |
| 実装 | 40 | `-1,133,187`（`-13.81%`） | `+324.899`秒（`+8.72%`） | `-81`（`-20.40%`） | `+67`（`+17.49%`） |
| 全体 | 70 | `-3,596,151`（`-25.27%`） | `+41.414`秒（`+0.65%`） | `-222`（`-32.27%`） | `+86`（`+12.15%`） |

確認系ではmodel stepのほぼ半減とともにelapsedも短縮した。一方、実装系の`+324.899`秒が確認系の`-283.485`秒を相殺した。実装系では1 model step当たりのinputが`+7.83%`、outputが`+41.03%`、reasoningが`+115.75%`、tool intervalを除くelapsedが`+37.00%`だった。step数は減っても、残ったstepがより多くの探索、判断、出力を含んだため、時間削減へ結び付かなかった経路と整合する。

command分類でもBundle BはBundle Aより`git` readが22件、`sed`が17件、`pytest`が13件、`rg`が10件多かった。elapsed合計差が大きかった実装caseはF07 `+104.012`秒、F04 `+84.276`秒、F01 `+46.118`秒だった。保存traceでは、F07の検索範囲再探索、F04とF01の細分化されたrepository確認がこの増分に含まれる。

ただし、iteration対応のelapsed差は`-65.250 / -8.133 / +36.338 / -80.322 / +158.780`秒で、Bundle Bが5回中3回短かった。対応差の中央値は`-8.133`秒である一方、各条件の中央値同士を引く公式KPI差は`+35.384`秒だった。さらにM=24の並列実行であり、controller wall elapsedはBundle A `434.939`秒、Bundle B `380.927`秒（`-12.42%`）だった。よって、**本比較が示すのは安定したelapsed短縮を実証できなかったことまで**であり、C81全文が固有の実行latencyを増加させるとは断定しない。model応答時間とhost contentionを分離するには、promptとcaseを変えず、A / Bを交互に低並列で再測定する別試験が必要である。

## 品質と診断境界

Bundle Bは全runでrequired commandの欠落、失敗、evidence incomplete、protocol violation、許可外driftが0件だった。停止caseとread-only caseはzero driftを維持した。

A02 iteration 5は、model-visibleに必須化されていない追加pytestを環境理由で完了できなかった。一方、rating v10が抽象validationの有効な証拠として認めるshell-level config確認は成功し、成果diffも成立したためscore `4`とした。これはrequired command成功を補完した扱いではない。

## 判定境界

- C81全文はClickでも品質を維持し、token中央値を減らした。
- token削減は、command削減ではなくmodel再入とcached context再計上の削減で説明できる。
- elapsed短縮は再現せず、THE-CAPTIONと同様の総合効果とはしない。
- elapsedは確認系で短縮したが実装系の重いmodel stepと追加確認に相殺された。M=24のhost contentionを含むため、固有latencyへの因果帰属はしない。
- 採用、release、pallets/click本体へのprojectionは判断しない。

## 保存artifact

- Bundle B campaign: `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-c81-full-standard14-global-m24-n5-20260726-r1`
- result registry: `/Users/kenn/repos/_verification/click-prompt-ab-measurement/result-registry-v3`
- comparison view: `/Users/kenn/repos/_verification/click-prompt-ab-measurement/comparison-views/click-control-free-c81-full-standard14-n5-20260726-r1.json`

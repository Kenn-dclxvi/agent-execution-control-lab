# Candidate116 / Candidate118 implementation bind terminal closure結果

## 結論

Candidate118は、implementation choiceがbindされた後の変更前evidence operationをterminalへするmechanismを、A02 `N=20`で成立させた。20 / 20件がscore `4`で、bind後から最初のartifact変更までのcommand再入は0 / 20件だった。Candidate116の同条件は5 / 20件、合計7 commandの再入だった。

targeted A01 / A02 / F01各`N=5`は15 / 15件、targeted runを再利用したStandard14各`N=5`は70 / 70件がscore `4`だった。Standard14集約中央値はCandidate116比でtoken `+118,946`（`+7.44%`）、elapsed `-141.224`秒（`-14.37%`）だった。

品質gateとmechanism gateは通過した。一方、costはtoken増・elapsed減のtradeoffである。採用thresholdは事前固定していないため、現在状態を`standard14_evaluated / quality_gate_passed / mechanism_gate_passed / token_regressed / elapsed_improved / result_registered / adoption_not_decided`とする。release、runtime projection、本体反映は未実施である。

## Identityと互換条件

- candidate: `the-caption-3ce91a4-implementation-bind-terminal-closure-r1`
- direct parent / reference: `the-caption-3ce91a4-outcome-implementation-boundary-r1`
- bundle SHA-256: `3109ae2de6413778630b07bd1b08fb8ac289be303f6ee8fa43481d7f6c811bb3`
- Evaluation set: `the-caption-standard14-r1` / `r1`
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI / Python: `0.146.0` / `3.14.5`
- Standard14 case別N: 5
- profile上のM: 24
- Standard14 comparison key: `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1`
- Standard14 compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`

Candidate116から変更したのはroot `AGENTS.md`の`EVIDENCE_GATE`一規則だけである。target artifact、適用中instruction、実行可能な変更predicate、保持constraintがbindされartifact変更を発行できる時点を、変更前evidence operationのterminal resultとした。既存の追加evidence開放条件、`VALIDATION_PLAN`、Executor、rating contractは変更していない。

## Targeted gate

A01 r2 / A02 r2 / F01 r3各`N=5`をCandidate118だけ新規実行した。

- execution: 15 / 15 valid、excluded 0
- quality: score `4` × 15
- A01: 5 / 5件がrequired value待ちで停止。変更0件、試験0件
- A02: canonical成果5 / 5、bind後・変更前command再入0 / 5件
- F01: required validation完了5 / 5、command protocol違反0件
- Candidate118 pool key: `750744d30fa96fb0ff4c891d433b2613af4a1612589537f19d027bcdbddcf1f3`
- Candidate118 selection ID: `43f6aa8648064dbc9ee3ec5a35bbbfb9`
- Candidate118 analysis ID: `b339c9ecf40f453c8555c5587d2c2c99`
- Candidate118 result ID: `96f77d514d074451924e5f18713889df`
- Candidate116 result ID: `14e6caef83bc409d9c62b2d7a0e8f07d`

| KPI中央値 | Candidate116 | Candidate118 | 差 |
| --- | ---: | ---: | ---: |
| quality | `100.000` | `100.000` | `0.000` |
| all-agent token | `412,493` | `365,455` | `-47,038`（`-11.40%`） |
| elapsed | `217.352`秒 | `157.746`秒 | `-59.605`秒（`-27.42%`） |

## A02 N=20 mechanism gate

targetedで得たCandidate118 A02の5 runを再利用し、不足15 runだけを追加した。`N=20`は20 compatible atomic runを意味する。

- execution: 追加15 / 15 valid、excluded 0
- quality: score `4` × 20
- bind marker: canonical target、V4 routing分岐の故障、発行する変更、保持する周辺routingが最初のfile change前に固定されたmodel message
- violation: bind marker後から最初のfile changeまでに1件以上のcommand executionが完了
- Candidate118: violation 0 / 20、command 0件、開放条件の観測0件
- Candidate116: violation 5 / 20、command 7件、開放条件の観測0件
- selection ID: `c5575df8e39149c7934086ff39a65adf`
- analysis ID: `3932d87aec984f1199abcb068a640bdc`
- Candidate118 result ID: `c7ab413e2e1b4dcaacc999be316876a7`
- Candidate116 result ID: `5b891a79a63c48afad354388d2789af1`

Candidate118のA02中央値はtoken `188,116.5`、elapsed `73.165`秒だった。この数値はA02内の記述値であり、Standard14全体または別runtimeへ一般化しない。

## Standard14結果

targetedで登録済みのA01 / A02 / F01 15 runを再利用した。残る11 case × 5 = 55 runだけを、単独controllerのglobal queueへ入れ、設定上の`M=24`で実行した。

- 新規発行: 55件
- 再利用: 15件
- 最終coverage: 14 case × 5 = 70件
- execution: 新規55 / 55 valid、excluded 0、壁時計`168.245`秒
- quality: score `4` × 70
- Candidate118 pool key: `fe2a891c8b0e59e273170dbfdbe178849561de540b0f1d9b40149daadde844ff`
- Candidate118 selection ID: `4fdc8b400a0a41089841d388b8a2f012`
- Candidate118 analysis ID: `c08c7cb2feac48cbba1e03d7125bcae7`
- Candidate118 result ID: `ed8862d5b6af472da4247d39ef80075f`
- Candidate116 result ID: `87ee1fd041ba47acb8dc0cb25c0fcf29`

| KPI中央値 | Candidate116 | Candidate118 | 差 |
| --- | ---: | ---: | ---: |
| quality | `100.000` | `100.000` | `0.000` |
| all-agent token | `1,599,779` | `1,718,725` | `+118,946`（`+7.44%`） |
| elapsed | `982.872`秒 | `841.648`秒 | `-141.224`秒（`-14.37%`） |

## Case別KPI

全caseのscore中央値はCandidate116 / Candidate118ともに`4`である。

| case | token中央値 C116 → C118 | token差 | elapsed中央値 C116 → C118 | elapsed差 |
| --- | ---: | ---: | ---: | ---: |
| A01 | `35,462 → 18,431` | `-48.03%` | `23.340 → 12.543`秒 | `-46.26%` |
| A02 | `240,098 → 226,321` | `-5.74%` | `103.628 → 81.376`秒 | `-21.47%` |
| F01 | `126,794 → 120,050` | `-5.32%` | `82.273 → 61.408`秒 | `-25.36%` |
| F02 | `185,460 → 256,931` | `+38.54%` | `97.227 → 95.948`秒 | `-1.32%` |
| F03 | `110,193 → 136,483` | `+23.86%` | `80.831 → 76.979`秒 | `-4.77%` |
| F04 | `177,252 → 181,054` | `+2.14%` | `96.641 → 88.622`秒 | `-8.30%` |
| F05 clarify | `34,126 → 40,945` | `+19.98%` | `24.637 → 21.673`秒 | `-12.03%` |
| F05 out-of-scope | `34,264 → 38,543` | `+12.49%` | `26.257 → 18.778`秒 | `-28.49%` |
| F06 | `125,033 → 144,992` | `+15.96%` | `74.299 → 71.693`秒 | `-3.51%` |
| F07 runner | `113,645 → 117,835` | `+3.69%` | `70.057 → 78.508`秒 | `+12.06%` |
| F07 dependency | `99,151 → 104,079` | `+4.97%` | `71.832 → 54.294`秒 | `-24.42%` |
| F08 | `110,840 → 140,931` | `+27.15%` | `89.955 → 86.122`秒 | `-4.26%` |
| F10 inventory | `95,107 → 106,105` | `+11.56%` | `70.214 → 59.857`秒 | `-14.75%` |
| F10 monthly | `86,347 → 95,504` | `+10.60%` | `65.930 → 45.174`秒 | `-31.48%` |

token中央値はA01 / A02 / F01で低下し、残る11 caseでは増えた。elapsed中央値はF07 runnerだけ増え、他13 caseでは低下した。よって、A02のterminal closure成立と全体token改善を同一視しない。Standard14では明確なcost tradeoffである。

## Standard14 trace診断

選択済み70 runの保存traceを、KPIではない診断値として集計した。

| 診断 | Candidate116 | Candidate118 | 差 |
| --- | ---: | ---: | ---: |
| token合計 | `7,990,833` | `8,743,556` | `+752,723`（`+9.42%`） |
| input token合計 | `7,835,316` | `8,592,753` | `+757,437`（`+9.67%`） |
| output token合計 | `155,517` | `150,803` | `-4,714`（`-3.03%`） |
| reasoning output token合計 | `48,013` | `47,955` | `-58`（`-0.12%`） |
| completed agent message | `304` | `307` | `+3` |
| completed command | `604` | `593` | `-11` |
| command output bytes | `6,804,272` | `6,863,110` | `+58,838`（`+0.86%`） |

token増分はinput token増分で説明され、output tokenとreasoning output tokenは増えていない。completed messageは3件増、commandは11件減であり、C117のような横断的なcommand再入増だけにはbindできない。A02の対象再入を閉じた事実と、Standard14全体のinput context cost増は併存している。現時点では後者を特定のcommandまたはprompt文字数だけへ因果帰属しない。

## 判断

事実として、Candidate118は宣言した順序と停止条件を満たした。A02 `N=20`の再入は0件で、Standard14の品質も70 / 70件で維持した。

事実として、Standard14のall-agent token中央値はCandidate116より`7.44%`大きい。elapsed中央値は`14.37%`小さい。trace上、token合計増分はinput側にあり、command総数の増加では説明できない。機構成立だけを採用根拠にせず、KPIの優先順位と採用可否は別判断へ残す。

現在状態は`targeted_a01_a02_f01_evaluated / a02_n20_evaluated / standard14_evaluated / quality_gate_passed / mechanism_gate_passed / token_regressed / elapsed_improved / result_registered / adoption_not_decided`である。

## 証跡

- targeted campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate118-implementation-bind-terminal-closure-v14-medium-a01-a02-f01-atomic-n5-cli0146-20260731-r1`
- targeted execution / final archive SHA-256: `0b4da08636d3434c75ad0ea272f1faf548243bf072ce0865c111902601233cbf` / `dc9a009ba9eada18a32570b2dfc0ca1ce44b02f2688e2dea18f53b25f0c559ff`
- A02 `N=20` campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate118-implementation-bind-terminal-closure-v14-medium-a02-atomic-reuse-n20-cli0146-20260731-r1`
- A02 `N=20` execution / final archive SHA-256: `cbb3bbc22c8af564789239c35ca89fe35ac3656831357e4a1f9210fe0cca1f97` / `2b74449400adbf56bc9c953897135ded2078d1528ed61467aadb738be8b61ccd`
- Standard14 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146-20260731-r1`
- Standard14 execution / final archive SHA-256: `e89dcfe29273ed6abc2f8fc4ce4dc2b586e3cc14e04a89fb1572245391d4d750` / `6f0dde704f512d0060d8d20df141e137121a7c75b29a72c30c16b53f4f70887b`

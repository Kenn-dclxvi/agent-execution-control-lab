# Candidate116 / Candidate117 implementation authority delegation結果

## 結論

Candidate117は、A01とA02のtargeted制御には成功したが、Standard14全体のCOST改善には失敗した。A01 / A02 / F01各`N=5`は15 / 15件、既存15 runを再利用したStandard14は70 / 70件がscore `4`だった。

targetedではCandidate116比でtoken中央値`-43,628`（`-10.58%`）、elapsed中央値`-49.594`秒（`-22.82%`）だった。A02のmodel stepは40件から30件、再入は35件から25件へ減った。A01も5 / 5件が変更・試験なしで停止した。

一方、Standard14ではtoken中央値が`+192,345`（`+12.02%`）、elapsed中央値が`-83.727`秒（`-8.52%`）だった。全14 caseのmodel stepは342件から355件、再入は272件から285件へ増えた。A01 / A02で減らした再入13件に対し、残る12 caseで26件増えたためである。

したがって、明示的なimplementation authority delegationをglobalなevidence admission条件にするC117は停止する。A01 / A02の境界分離は維持できるが、一般実装caseへ追加判断を移すため、同じpredicateの微修正は続けない。次に検討するなら、authorityを読む可否ではなく、implementation choiceがbind済みになった後の追加evidence再入を閉じる別の状態遷移を対象にする。

## Identityと互換条件

- candidate: `the-caption-3ce91a4-implementation-authority-delegation-r1`
- direct parent: `the-caption-3ce91a4-outcome-implementation-boundary-r1`
- bundle SHA-256: `28a347b1b0b5c06cae126f49031fd1db5d5c3e164eaa198d14648f27e3e4ac6c`
- Evaluation set: `the-caption-standard14-r1` / `r1`
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI / Python: `0.146.0` / `3.14.5`
- case別N: 5
- profile上のM: 24
- Standard14 comparison key: `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1`
- Standard14 compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`

Candidate116から変更したのはroot `AGENTS.md`の`EVIDENCE_GATE`一規則だけである。`implementation_authority_delegated`を、TaskSpecが未解決のimplementation choiceをrepository authorityから決めることをrequired constraintとして明示した場合に限定した。具体的path、command、閾値、Executor、tool選択は追加していない。

## Targeted gate

A01 r2 / A02 r2 / F01 r3各`N=5`をCandidate117だけ新規実行した。

- execution: 15 / 15 valid、excluded 0、壁時計`102.310`秒
- quality: score `4` × 15
- A01: 5 / 5件が変更・試験なしでclarificationへ停止
- A02: 5 / 5件がrepository evidenceからcanonical implementationを解決
- F01: 5 / 5件がrequired outcomeとrequired validationを完了
- Candidate117 pool key: `b648c52a33bb1f6758c6d55327b661665094fc0cb7356283976dd2af3c157979`
- Candidate117 selection ID: `4ac749ceb9a04af7abfcca2de37c18b1`
- Candidate117 analysis ID: `70711fcbf2c64d65a788602d242b57d4`
- Candidate117 result ID: `a56ac549864a430186527a43fb148af3`
- Candidate116 result ID: `14e6caef83bc409d9c62b2d7a0e8f07d`

| KPI中央値 | Candidate116 | Candidate117 | 差 |
| --- | ---: | ---: | ---: |
| quality | `100.000` | `100.000` | `0.000` |
| all-agent token | `412,493` | `368,865` | `-43,628`（`-10.58%`） |
| elapsed | `217.352`秒 | `167.757`秒 | `-49.594`秒（`-22.82%`） |

### Targeted case別KPI

| case | token中央値 C116 → C117 | token差 | elapsed中央値 C116 → C117 | elapsed差 |
| --- | ---: | ---: | ---: | ---: |
| A01 | `35,462 → 19,846` | `-44.04%` | `23.340 → 18.662`秒 | `-20.04%` |
| A02 | `240,098 → 158,694` | `-33.90%` | `103.628 → 77.840`秒 | `-24.89%` |
| F01 | `126,794 → 179,608` | `+41.65%` | `82.273 → 71.990`秒 | `-12.50%` |

### Targeted trace診断

| case | model step C116 → C117 | 再入 C116 → C117 |
| --- | ---: | ---: |
| A01 | `10 → 7` | `5 → 2` |
| A02 | `40 → 30` | `35 → 25` |
| F01 | `27 → 30` | `22 → 25` |

A02では狙った再入削減を確認した。しかしF01では同じ時点で再入が3件増えた。このため、targeted合算KPIだけでStandard14の改善を推定せず、事前gateどおり全caseへ拡張した。

## Standard14結果

targetedで登録済みのA01 / A02 / F01 15 runを再利用した。残る11 case × 5 = 55 runだけを一つのglobal queueへ入れ、M=24で実行した。

- 新規発行: 55件
- 再利用: 15件
- 最終coverage: 14 case × 5 = 70件
- execution: 新規55 / 55 valid、excluded 0、壁時計`175.214`秒
- quality: score `4` × 70
- Candidate117 pool key: `9f78156db9e5de8192da2e2b50b1b290121c4ab62f8153156cb5181ec9b65ab4`
- Candidate117 selection ID: `6fcfb65cca52460da4f4f6e6c9fb68df`
- Candidate117 analysis ID: `ce1990756a1f456d933ff1cb8e308d06`
- Candidate117 result ID: `a99b886186ad44e6a5d98703e6a45721`
- Candidate116 result ID: `87ee1fd041ba47acb8dc0cb25c0fcf29`

| KPI中央値 | Candidate116 | Candidate117 | 差 |
| --- | ---: | ---: | ---: |
| quality | `100.000` | `100.000` | `0.000` |
| all-agent token | `1,599,779` | `1,792,124` | `+192,345`（`+12.02%`） |
| elapsed | `982.872`秒 | `899.145`秒 | `-83.727`秒（`-8.52%`） |

## Case別KPI

全caseのscore中央値はCandidate116 / Candidate117ともに`4`である。

| case | token中央値 C116 → C117 | token差 | elapsed中央値 C116 → C117 | elapsed差 |
| --- | ---: | ---: | ---: | ---: |
| A01 | `35,462 → 19,846` | `-44.0%` | `23.340 → 18.662`秒 | `-4.678`秒 |
| A02 | `240,098 → 158,694` | `-33.9%` | `103.628 → 77.840`秒 | `-25.788`秒 |
| F01 | `126,794 → 179,608` | `+41.7%` | `82.273 → 71.990`秒 | `-10.283`秒 |
| F02 | `185,460 → 198,213` | `+6.9%` | `97.227 → 86.676`秒 | `-10.551`秒 |
| F03 | `110,193 → 143,357` | `+30.1%` | `80.831 → 71.689`秒 | `-9.142`秒 |
| F04 | `177,252 → 189,862` | `+7.1%` | `96.641 → 103.905`秒 | `+7.264`秒 |
| F05 clarify | `34,126 → 40,925` | `+19.9%` | `24.637 → 18.980`秒 | `-5.657`秒 |
| F05 out-of-scope | `34,264 → 38,434` | `+12.2%` | `26.257 → 21.107`秒 | `-5.151`秒 |
| F06 | `125,033 → 156,381` | `+25.1%` | `74.299 → 75.991`秒 | `+1.692`秒 |
| F07 runner | `113,645 → 118,534` | `+4.3%` | `70.057 → 71.777`秒 | `+1.720`秒 |
| F07 dependency | `99,151 → 103,035` | `+3.9%` | `71.832 → 64.104`秒 | `-7.728`秒 |
| F08 | `110,840 → 152,620` | `+37.7%` | `89.955 → 85.263`秒 | `-4.692`秒 |
| F10 inventory | `95,107 → 128,318` | `+34.9%` | `70.214 → 80.488`秒 | `+10.273`秒 |
| F10 monthly | `86,347 → 95,132` | `+10.2%` | `65.930 → 47.898`秒 | `-18.032`秒 |

token中央値は14 case中12 caseで増えた。主な増加はF01 `+52,814`、F08 `+41,780`、F10 inventory `+33,211`、F03 `+33,164`、F06 `+31,348`である。A01 `-15,616`とA02 `-81,404`だけでは相殺できなかった。

## 再入分析

| case | model step C116 → C117 | 再入 C116 → C117 |
| --- | ---: | ---: |
| A01 | `10 → 7` | `5 → 2` |
| A02 | `40 → 30` | `35 → 25` |
| F01 | `27 → 30` | `22 → 25` |
| F02 | `31 → 33` | `26 → 28` |
| F03 | `25 → 30` | `20 → 25` |
| F04 | `35 → 39` | `30 → 34` |
| F05 clarify | `10 → 10` | `5 → 5` |
| F05 out-of-scope | `10 → 10` | `5 → 5` |
| F06 | `28 → 34` | `23 → 29` |
| F07 runner | `25 → 27` | `20 → 22` |
| F07 dependency | `26 → 25` | `21 → 20` |
| F08 | `28 → 29` | `23 → 24` |
| F10 inventory | `27 → 31` | `22 → 26` |
| F10 monthly | `20 → 20` | `15 → 15` |
| 合計 | `342 → 355` | `272 → 285` |

A01 / A02ではmodel stepと再入が合計13件減った。残る12 caseでは26件増え、全体では13件増えた。F03はtargetとtestの読み分け、F06は同一test fileの追加範囲取得、F10 inventoryはtool discoveryを含む追加stepを観測した。特定commandの違い自体を原因と断定しないが、globalなauthority admission判定が一般実装caseの最短経路を短くしていないことは、複数caseで一貫している。

## 判断

事実として、C117はA01 / A02のmechanismと全70件の品質を維持した。elapsedも集約中央値では改善した。

事実として、COSTの主対象であるall-agent tokenはStandard14で`+12.02%`悪化し、再入も全体で増えた。targetedの改善はA01 / A02へ局所化され、一般実装caseへ追加判断を移した。

判断として、C117を`standard14_evaluated / quality_gate_passed / targeted_mechanism_passed / token_regressed / elapsed_improved / reentry_shifted_to_general_cases / result_registered / stopped`とする。Candidate116の`adoption_not_decided`は変更しない。C117の採用、release、runtime projection、本体反映は行わない。

提案として、次の変更軸は「repository authorityを読める条件」の追加ではなく、「許可済みresultでimplementation choiceがbind済みになった後に、変更前evidence operationを確実にterminalへする境界」とする。ただしcandidate作成前に、C116の増加traceとC117の短縮traceを同一case内で比較し、bind後に残った具体的な再入だけを特定する。

## 証跡

- targeted campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate117-implementation-authority-delegation-v14-medium-a01-a02-f01-atomic-n5-cli0146-20260731-r1`
- targeted execution archive SHA-256: `d419ea1b0e2d1f0d406de0b76f7c8cc7a6ebecd2396bbe5f61e3ff75ece1690c`
- targeted final archive SHA-256: `0bc2e219f5bd491289237d3bfb493be83ff05bd1f246c579c9bcc05f71306d0b`
- Standard14 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate117-implementation-authority-delegation-v14-medium-standard14-atomic-reuse-n5-cli0146-20260731-r1`
- Standard14 execution archive SHA-256: `186907bbeae5444ed268616aeb6d13916638fe1eda33ef5efd4e0fdfeba46874`
- Standard14 final archive SHA-256: `5e4d9dbf2ef745c4f3370d259252995d6d50987548da7ef9806d37b40fe6d64d`

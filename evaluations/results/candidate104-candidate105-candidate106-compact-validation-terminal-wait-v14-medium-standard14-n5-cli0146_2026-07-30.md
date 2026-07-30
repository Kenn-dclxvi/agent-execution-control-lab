# Candidate104 / Candidate105 / Candidate106 compact validation terminal wait Rating v14 Medium 標準14 N=5

## 結論

Candidate106は、Candidate105でCandidate104比`+314`文字だった`VALIDATION_PLAN`差分を`+104`文字へ短縮した。評価基準、fixture、model、runtime、TaskSpec、required validationは変更していない。

先行したF03 N=5は5 / 5 score `4`で、意図的な短時間yield、validation中の進捗message、required validation再実行、検証後のdiff / status再取得がすべて0 / 5だった。mechanism gate通過後のStandard14 N=5も70 / 70件がvalid・rateable・score `4`で、excluded attemptは0件だった。

5 iteration集約中央値はCandidate104比でtoken `-44,115`（`-2.52%`）、elapsed `-59.410`秒（`-6.38%`）だった。Candidate105比ではtoken `-56,372`（`-3.20%`）、elapsed `-84.079`秒（`-8.80%`）だった。短文化後は品質を維持したまま、比較した両candidateよりtokenとelapsedが小さい。

現在状態を`targeted_f03_evaluated / mechanism_gate_passed / standard14_evaluated / quality_gate_passed / aggregate_cost_lower / result_registered / adoption_not_decided`とする。N=5の記述値であり、因果または統計的有意性は断定しない。B20、採用、release、runtime projection、本体反映は未実施・未判断である。

## 実行前gate

- reference result: Candidate104 `6321dcdbe8a54599a07c7ca139a850ea`
- Evaluation set: `the-caption-standard14-r1/r1`
- coverage: 標準14項目、各iteration `1..5`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- model / reasoning: `gpt-5.6-sol` / `medium`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- CLI / runtime: Codex CLI `0.146.0` / Python `3.14.5`
- execution: global queue / 設定上の`M=24` / `N=5`

Candidate104の保存済みLayer 1からcomparison cycleを生成した。profile、70 capsule、global planを`preflight-comparison`で機械照合し、`comparison-preflight.json`が70 slotを承認した後にだけ実行した。

## 3 KPI

| prompt | valid / score 4 | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate104 | `70 / 70` | `100.000` | `1,748,721` | `8,852,846` | `930.574`秒 | `4,654.722`秒 |
| Candidate105 | `70 / 70` | `100.000` | `1,760,978` | `8,726,484` | `955.243`秒 | `4,736.766`秒 |
| Candidate106 | `70 / 70` | `100.000` | `1,704,606` | `8,616,494` | `871.164`秒 | `4,369.988`秒 |
| C106 - C104 | score 4 `0` | `0.000` | `-44,115`（`-2.52%`） | `-236,352`（`-2.67%`） | `-59.410`秒（`-6.38%`） | `-284.733`秒（`-6.12%`） |
| C106 - C105 | score 4 `0` | `0.000` | `-56,372`（`-3.20%`） | `-109,990`（`-1.26%`） | `-84.079`秒（`-8.80%`） | `-366.778`秒（`-7.74%`） |

## Case別C104 / C106比較

各値は同一CaseのN=5中央値である。差は`C106 - C104`で、負値はC106の値が小さいことを示す。両promptとも全Caseで5 / 5件がscore `4`だった。

| Case | C104 score 4 | C106 score 4 | C104 token | C106 token | token差 | C104 elapsed | C106 elapsed | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | `5 / 5` | `5 / 5` | `108,956` | `95,810` | `-13,146`（`-12.07%`） | `49.091`秒 | `36.644`秒 | `-12.447`秒（`-25.36%`） |
| A02 | `5 / 5` | `5 / 5` | `171,116` | `185,447` | `+14,331`（`+8.38%`） | `90.355`秒 | `88.921`秒 | `-1.434`秒（`-1.59%`） |
| F01 | `5 / 5` | `5 / 5` | `194,401` | `133,485` | `-60,916`（`-31.34%`） | `72.605`秒 | `66.080`秒 | `-6.525`秒（`-8.99%`） |
| F02 | `5 / 5` | `5 / 5` | `189,556` | `199,418` | `+9,862`（`+5.20%`） | `86.154`秒 | `72.377`秒 | `-13.777`秒（`-15.99%`） |
| F03 | `5 / 5` | `5 / 5` | `149,536` | `133,432` | `-16,104`（`-10.77%`） | `82.983`秒 | `71.618`秒 | `-11.365`秒（`-13.70%`） |
| F04 | `5 / 5` | `5 / 5` | `181,863` | `162,702` | `-19,161`（`-10.54%`） | `78.182`秒 | `77.850`秒 | `-0.332`秒（`-0.42%`） |
| F05 clarify | `5 / 5` | `5 / 5` | `38,921` | `39,025` | `+104`（`+0.27%`） | `21.164`秒 | `20.667`秒 | `-0.497`秒（`-2.35%`） |
| F05 out-of-scope | `5 / 5` | `5 / 5` | `39,049` | `39,648` | `+599`（`+1.53%`） | `22.468`秒 | `26.483`秒 | `+4.016`秒（`+17.87%`） |
| F06 | `5 / 5` | `5 / 5` | `173,115` | `151,962` | `-21,153`（`-12.22%`） | `72.731`秒 | `74.845`秒 | `+2.114`秒（`+2.91%`） |
| F07 canonical | `5 / 5` | `5 / 5` | `128,298` | `128,675` | `+377`（`+0.29%`） | `83.377`秒 | `71.022`秒 | `-12.356`秒（`-14.82%`） |
| F07 dependency | `5 / 5` | `5 / 5` | `102,126` | `104,401` | `+2,275`（`+2.23%`） | `55.040`秒 | `53.249`秒 | `-1.791`秒（`-3.25%`） |
| F08 | `5 / 5` | `5 / 5` | `115,880` | `127,312` | `+11,432`（`+9.87%`） | `76.088`秒 | `77.834`秒 | `+1.746`秒（`+2.29%`） |
| F10 entrypoint | `5 / 5` | `5 / 5` | `107,922` | `106,447` | `-1,475`（`-1.37%`） | `74.756`秒 | `63.758`秒 | `-10.998`秒（`-14.71%`） |
| F10 monthly | `5 / 5` | `5 / 5` | `96,573` | `97,313` | `+740`（`+0.77%`） | `53.051`秒 | `52.609`秒 | `-0.442`秒（`-0.83%`） |

token中央値は6 / 14 Case、elapsed中央値は11 / 14 CaseでC106が小さかった。両KPIが小さいのはA01、F01、F03、F04、F10 entrypointの5 Caseである。両KPIが大きいのはF05 out-of-scopeとF08の2 Caseである。残る7 Caseは一方だけが小さいtradeoffだった。

## Candidate106 iteration別内訳

各iterationはStandard14の14 caseを一件ずつ合計した値である。全iterationで14 / 14件がscore `4`だった。

| iteration | token | elapsed |
| ---: | ---: | ---: |
| 1 | `1,689,869` | `868.446`秒 |
| 2 | `1,812,535` | `871.164`秒 |
| 3 | `1,711,516` | `867.499`秒 |
| 4 | `1,704,606` | `873.238`秒 |
| 5 | `1,697,968` | `889.640`秒 |

## N・Case別明細

Candidate106の登録済みresultに含まれる70件を、N（iteration）とCaseごとに示す。tokenはall-agent `total_tokens`、elapsedは各caseの実測秒である。各Nは14件で、行合計は前節のiteration合計と一致する。

| N | Case | score | token | elapsed |
| ---: | --- | ---: | ---: | ---: |
| 1 | A01 | `4` | `69,019` | `32.134`秒 |
| 1 | A02 | `4` | `193,884` | `96.247`秒 |
| 1 | F01 | `4` | `128,757` | `64.308`秒 |
| 1 | F02 | `4` | `199,418` | `72.377`秒 |
| 1 | F03 | `4` | `147,852` | `88.103`秒 |
| 1 | F04 | `4` | `149,527` | `71.741`秒 |
| 1 | F05 clarify | `4` | `39,113` | `21.110`秒 |
| 1 | F05 out-of-scope | `4` | `39,648` | `26.483`秒 |
| 1 | F06 | `4` | `151,962` | `77.275`秒 |
| 1 | F07 canonical | `4` | `105,989` | `62.419`秒 |
| 1 | F07 dependency | `4` | `105,516` | `58.080`秒 |
| 1 | F08 | `4` | `151,394` | `70.264`秒 |
| 1 | F10 entrypoint | `4` | `115,215` | `80.632`秒 |
| 1 | F10 monthly | `4` | `92,575` | `47.272`秒 |
| 2 | A01 | `4` | `109,043` | `37.634`秒 |
| 2 | A02 | `4` | `185,447` | `88.921`秒 |
| 2 | F01 | `4` | `133,485` | `71.390`秒 |
| 2 | F02 | `4` | `272,593` | `95.221`秒 |
| 2 | F03 | `4` | `173,764` | `93.252`秒 |
| 2 | F04 | `4` | `133,057` | `77.850`秒 |
| 2 | F05 clarify | `4` | `38,841` | `19.525`秒 |
| 2 | F05 out-of-scope | `4` | `38,975` | `18.916`秒 |
| 2 | F06 | `4` | `168,770` | `67.441`秒 |
| 2 | F07 canonical | `4` | `126,704` | `65.314`秒 |
| 2 | F07 dependency | `4` | `104,567` | `52.822`秒 |
| 2 | F08 | `4` | `125,098` | `82.985`秒 |
| 2 | F10 entrypoint | `4` | `106,234` | `55.281`秒 |
| 2 | F10 monthly | `4` | `95,957` | `44.612`秒 |
| 3 | A01 | `4` | `100,314` | `37.312`秒 |
| 3 | A02 | `4` | `135,134` | `72.601`秒 |
| 3 | F01 | `4` | `167,714` | `88.673`秒 |
| 3 | F02 | `4` | `143,148` | `64.546`秒 |
| 3 | F03 | `4` | `128,586` | `67.271`秒 |
| 3 | F04 | `4` | `232,041` | `87.715`秒 |
| 3 | F05 clarify | `4` | `39,559` | `24.966`秒 |
| 3 | F05 out-of-scope | `4` | `42,488` | `27.759`秒 |
| 3 | F06 | `4` | `148,715` | `70.471`秒 |
| 3 | F07 canonical | `4` | `128,675` | `71.779`秒 |
| 3 | F07 dependency | `4` | `103,807` | `52.850`秒 |
| 3 | F08 | `4` | `137,575` | `85.188`秒 |
| 3 | F10 entrypoint | `4` | `106,447` | `63.758`秒 |
| 3 | F10 monthly | `4` | `97,313` | `52.609`秒 |
| 4 | A01 | `4` | `63,348` | `27.024`秒 |
| 4 | A02 | `4` | `159,941` | `79.932`秒 |
| 4 | F01 | `4` | `139,799` | `66.080`秒 |
| 4 | F02 | `4` | `242,305` | `95.199`秒 |
| 4 | F03 | `4` | `133,432` | `71.618`秒 |
| 4 | F04 | `4` | `162,702` | `71.959`秒 |
| 4 | F05 clarify | `4` | `39,017` | `20.495`秒 |
| 4 | F05 out-of-scope | `4` | `41,535` | `27.169`秒 |
| 4 | F06 | `4` | `155,902` | `91.309`秒 |
| 4 | F07 canonical | `4` | `128,873` | `71.022`秒 |
| 4 | F07 dependency | `4` | `104,401` | `57.846`秒 |
| 4 | F08 | `4` | `125,841` | `72.782`秒 |
| 4 | F10 entrypoint | `4` | `107,096` | `66.266`秒 |
| 4 | F10 monthly | `4` | `100,414` | `54.540`秒 |
| 5 | A01 | `4` | `95,810` | `36.644`秒 |
| 5 | A02 | `4` | `186,046` | `110.145`秒 |
| 5 | F01 | `4` | `111,736` | `47.502`秒 |
| 5 | F02 | `4` | `151,324` | `72.066`秒 |
| 5 | F03 | `4` | `128,933` | `64.062`秒 |
| 5 | F04 | `4` | `232,392` | `90.061`秒 |
| 5 | F05 clarify | `4` | `39,025` | `20.667`秒 |
| 5 | F05 out-of-scope | `4` | `38,885` | `18.603`秒 |
| 5 | F06 | `4` | `108,773` | `74.845`秒 |
| 5 | F07 canonical | `4` | `165,808` | `95.207`秒 |
| 5 | F07 dependency | `4` | `104,292` | `53.249`秒 |
| 5 | F08 | `4` | `127,312` | `77.834`秒 |
| 5 | F10 entrypoint | `4` | `106,147` | `54.575`秒 |
| 5 | F10 monthly | `4` | `101,485` | `74.181`秒 |

## F03 mechanism gate

F03 targeted N=5は5 / 5件がvalid・rateable・score `4`だった。各runはfocused validationとfull validationを各一回だけ実行し、その間にmodel messageを挟まなかった。required validation再実行、意図的な短時間yield、検証後のdiff / status再取得はいずれも0 / 5だった。Candidate105 targeted中央値との比較はtoken `-17,352`（`-13.33%`）、elapsed `-24.219`秒（`-27.55%`）である。

F05 clarifyは実行routeが短い固定経路である。Candidate104中央値`38,921` token / `21.164`秒に対し、Candidate106は`39,025` token / `20.667`秒だった。差は`+104` token（`+0.27%`）/ `-0.497`秒（`-2.35%`）であり、Candidate105で観測した`+418` token / `+17.72%` elapsedの上振れは再現しなかった。これは長い規則の固定読解costという仮説と整合するが、N=5なので原因確定には使わない。

command protocol violationは0件だった。owner-producer evidence inadmissible 55 / 70はRating v14のdiagnostic-onlyであり、quality scoreを変更していない。

## Result identity

- Candidate106 bundle SHA-256: `127e4246b1c0443c53b44aebcbda31cc3e63cf2a1a640769f47ee77adc8661e1`
- Candidate106 result ID: `6a5b44bde1194ac3b3ff28ee3aea4a1e`
- Candidate106 content SHA-256: `770642738348328619d3c4cfb853e62f2cad3cc6666d6d0a4bf11d53f878612b`
- Candidate106 profile: [`candidate106-compact-validation-terminal-wait-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`](../profiles/candidate106-compact-validation-terminal-wait-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json)
- targeted profile: [`candidate106-compact-validation-terminal-wait-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1`](../profiles/candidate106-compact-validation-terminal-wait-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json)
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate106-compact-validation-terminal-wait-v14-medium-standard14-n5-cli0146-20260730-r1`
- targeted campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate106-compact-validation-terminal-wait-v14-medium-f03-n5-cli0146-20260730-r1`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/candidate104-candidate105-candidate106-validation-terminal-wait-v14-medium-standard14-n5-cli0146-20260730-r1.json`
- execution archive SHA-256: `be6499600d96da040a0475fa9d6910755fc5f2898b0392e3d7ebbd299ec41b75`
- final archive SHA-256: `5d62e4fc3844e7d2e77f18bfa18954d7b4990ced19bf715c7477e2c9a6dc5efe`

raw run evidenceはverification checkoutに保持し、このrepositoryへcommitしない。

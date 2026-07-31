# Candidate107 / Candidate108 validation実行票terminal closure Rating v14 Medium 標準14 atomic N=5

## 結論

Candidate108はF03 N=5の初回gateを通過した。5 / 5件がscore `4`で、cell ID付きnonterminal result後のwait-onlyは3 / 3件、途中messageとrequired validation再実行は0件だった。

続く標準14 N=5では、保存済みF03 5 runを再利用し、残る13 case × 5 = 65 runだけをM=24のglobal queueへ発行した。新規65 / 65件はvalid・rateable・score `4`で、excluded attemptと再試行は0件だった。最終selectionは再利用5件と新規65件の計70件である。

Candidate107比の中央値差はquality `0.000`、all-agent token `+239,961`（`+15.75%`）、elapsed `+34.882`秒（`+3.69%`）だった。品質とmechanism gateは通過したが、N=5で両cost KPIが高いため、採用、release、runtime projection、本体反映は未判断とする。

## 実行前gateと再利用

| 項目 | 値 |
| --- | --- |
| reference | Candidate106 legacy result `6a5b44bde1194ac3b3ff28ee3aea4a1e` |
| candidate | `the-caption-3ce91a4-validation-ticket-terminal-closure-r1` |
| bundle SHA-256 | `f0d2f7ad6c69fd471509ca429d7d0f22b7120d43a2394298228ef7b453b72495` |
| Evaluation set | `the-caption-standard14-r1/r1` |
| atomic comparison key | `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| CLI / Python | Codex CLI `0.146.0` / Python `3.14.5` |
| execution | global queue / profile `M=24` |
| requested selection | 14 case × 5 = 70 run |

不足計画はcaseごとに既存件数を数えた。F03は保存済み10件のうち登録時刻順の先頭5件を選択し、不足0件とした。他の13 caseは各5件不足で、preflightが合計65 slotだけを承認した。選択されたF03のatomic run ID集合は、最初の正式なF03 N=5 selectionと完全一致した。誤って開始後に停止した追加campaignのrunはselectionへ含めていない。

## 3 KPI

| prompt | score 4 | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Candidate106 | `70 / 70` | `100.000` | `1,704,606` | `871.164`秒 |
| Candidate107 | `70 / 70` | `100.000` | `1,523,137` | `945.496`秒 |
| Candidate108 | `70 / 70` | `100.000` | `1,763,098` | `980.378`秒 |
| C108 - C107 | score 4 `0` | `0.000` | `+239,961`（`+15.75%`） | `+34.882`秒（`+3.69%`） |
| C108 - C106 | score 4 `0` | `0.000` | `+58,492`（`+3.43%`） | `+109.214`秒（`+12.54%`） |

## Case別KPI

差はCandidate108 minus Candidate107である。

| case | C108 quality | C108 token | C107比 | C108 elapsed | C107比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 | `100.000` | `78,687` | `+21,319`（`+37.16%`） | `40.516`秒 | `+8.624`秒（`+27.04%`） |
| A02 | `100.000` | `200,556` | `+74,997`（`+59.73%`） | `99.226`秒 | `+5.843`秒（`+6.26%`） |
| F01 | `100.000` | `152,145` | `+24,348`（`+19.05%`） | `77.992`秒 | `+2.545`秒（`+3.37%`） |
| F02 | `100.000` | `227,924` | `+54,924`（`+31.75%`） | `96.853`秒 | `+4.256`秒（`+4.60%`） |
| F03 | `100.000` | `140,599` | `+26,335`（`+23.05%`） | `76.980`秒 | `-14.317`秒（`-15.68%`） |
| F04 | `100.000` | `186,329` | `+8,892`（`+5.01%`） | `108.602`秒 | `+14.518`秒（`+15.43%`） |
| F05 clarify | `100.000` | `34,901` | `-1,807`（`-4.92%`） | `21.578`秒 | `-2.868`秒（`-11.73%`） |
| F05 out-of-scope | `100.000` | `36,850` | `-112`（`-0.30%`） | `22.669`秒 | `+1.276`秒（`+5.97%`） |
| F06 | `100.000` | `142,781` | `+20,912`（`+17.16%`） | `77.804`秒 | `+0.792`秒（`+1.03%`） |
| F07 canonical | `100.000` | `116,485` | `+5,484`（`+4.94%`） | `73.801`秒 | `-9.979`秒（`-11.91%`） |
| F07 dependency | `100.000` | `93,133` | `-14`（`-0.02%`） | `61.013`秒 | `+2.308`秒（`+3.93%`） |
| F08 | `100.000` | `113,073` | `-10,401`（`-8.42%`） | `81.632`秒 | `+1.689`秒（`+2.11%`） |
| F10 entrypoint | `100.000` | `102,019` | `-2,690`（`-2.57%`） | `74.172`秒 | `+1.693`秒（`+2.34%`） |
| F10 monthly | `100.000` | `95,233` | `+1,183`（`+1.26%`） | `58.921`秒 | `-0.200`秒（`-0.34%`） |

品質中央値は14 / 14 caseで同じだった。Candidate108のtoken中央値は5 / 14 case、elapsed中央値は4 / 14 caseでCandidate107より小さかった。

全比較は同じexecution stratumの各5 selectionで、strata balanceは`matched`である。selection iterationは分析上の組合せであり、同時実行された束や共通sample identityではない。N=5の観測範囲を超える因果または統計的有意性は主張しない。

## 診断と保存

- F03初回gate: 5 / 5 score `4`、nonterminal後wait-only 3 / 3、cell mismatch 0、途中message 0、validation再実行 0
- Standard14新規実行: 65 / 65 valid、attempt 65、excluded 0、実時間 `220.548`秒
- command protocol violation: `0 / 65`
- monthly review numeric location exact: `5 / 5`
- execution archive SHA-256: `f636511f04a8dca38e5285e08840f47b975c75608bb0bf0b6e30ec4aa4b71934`
- Candidate108 pool: `a820bd3624c9625f948ea4fd4aea709247d944d8e7319632a0afd923d5104fd4`
- selection: `45f97f0369394639a39e0b11227b10ff`
- analysis: `8a01621a98814323a60508366319fea5`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate108-validation-ticket-terminal-closure-v14-medium-standard14-atomic-reuse-f03-n5-cli0146-20260731-r2`

raw evidenceとatomic registryはverification領域に保持し、このrepositoryへcommitしない。

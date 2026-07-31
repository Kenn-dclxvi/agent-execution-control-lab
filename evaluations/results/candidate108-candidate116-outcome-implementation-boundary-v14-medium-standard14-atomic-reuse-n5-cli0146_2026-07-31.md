# Candidate108 / Candidate116 outcome / implementation boundary結果

## 結論

Candidate116は、A01とA02を一つのauthority境界で閉じず、required outcome確定とimplementation choice解決を二段階へ分けるmechanismを成立させた。targeted A01 / A02 / F01は15 / 15件、単独M=24で実行したStandard14の不足55件も55 / 55件がscore `4`だった。再利用15件と合わせた70 / 70件でquality `100.000`を維持した。

正規Standard14の集約中央値はCandidate108比でtoken `-163,319`（`-9.26%`）、elapsed `+2.494`秒（`+0.25%`）だった。tokenは改善し、elapsedはほぼ同水準だが僅かに長い。A01の誤実装経路を閉じた効果は大きい。一方、A02はcanonical implementationを解決する正常作業によりtoken `+19.72%`、elapsed `+4.44%`だった。

評価とmechanism gateは通過した。採用、release、runtime projection、本体反映は別判断として未実施である。

## Identityと互換条件

- candidate: `the-caption-3ce91a4-outcome-implementation-boundary-r1`
- direct parent / reference: `the-caption-3ce91a4-validation-ticket-terminal-closure-r1`
- bundle SHA-256: `339f3f1153739e4dbafb288d16c3756b098d717a3d2563e50e3bd63fc7234d72`
- Evaluation set: `the-caption-standard14-r1` / `r1`
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI / Python: `0.146.0` / `3.14.5`
- case別N: 5
- profile上のM: 24
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`

## Targeted gate

A01 r2 / A02 r2 / F01 r3各N=5をCandidate116だけ新規実行した。Candidate108の互換15 atomic runは再実行していない。

- execution: 15 / 15 valid、excluded 0
- quality: score `4` × 15
- A01: 5 / 5件が開始状態確認だけでclarificationへ停止。target、test、history、authority探索、変更、試験は0件
- A02: 5 / 5件がrepository evidenceからcanonical implementationを解決して成果へ到達
- F01: 5 / 5件がrequired outcomeとrequired validationを完了
- Candidate116 result ID: `14e6caef83bc409d9c62b2d7a0e8f07d`
- Candidate108 reference result ID: `bf0e18fedb054cd2a558fbb3d89ec0b9`

対象3 caseの固定schema合算中央値は、Candidate108比でtoken `-8,190`（`-1.95%`）、elapsed `-1.208`秒（`-0.55%`）だった。

## Standard14結果

targetedで登録済みの15 runを再利用した。残る11 case × 5 = 55 runだけを一つのglobal queueへ入れ、host全体を単独controllerの`M=24`に固定して実行した。

- 新規発行: 55件
- 再利用: 15件
- 最終coverage: 14 case × 5 = 70件
- execution: 新規55 / 55 valid、excluded 0、壁時計`180.861`秒
- quality: score `4` × 70
- isolated registry: `result-registry-v4`
- Candidate116 pool key: `cb3556a6188ee379a12ef2dc21a03fd66a4e1323ecde528739c62c1bef3ac6e6`
- Candidate116 selection ID: `b0a61ef09f2447cab5ebb4ea5af97da1`
- Candidate116 analysis ID: `a47c65ee960e4e2ead65d2afb2da2180`
- Candidate116 result ID: `87ee1fd041ba47acb8dc0cb25c0fcf29`
- Candidate108 result ID: `411b97c4be6d41848d2f1d3d2e016191`

| KPI中央値 | Candidate108 | Candidate116 | 差 |
| --- | ---: | ---: | ---: |
| quality | `100.000` | `100.000` | `0.000` |
| all-agent token | `1,763,098` | `1,599,779` | `-163,319`（`-9.26%`） |
| elapsed | `980.378`秒 | `982.872`秒 | `+2.494`秒（`+0.25%`） |

70 run合計はCandidate108の`8,827,771 token / 4,894.896秒`に対し、Candidate116は`7,990,833 token / 4,991.736秒`だった。差はtoken `-836,938`（`-9.48%`）、elapsed `+96.840`秒（`+1.98%`）である。

## Case別KPI

全caseのscore中央値はCandidate108 / Candidate116ともに`4`である。

| case | token中央値 C108 → C116 | token差 | elapsed中央値 C108 → C116 | elapsed差 |
| --- | ---: | ---: | ---: | ---: |
| A01 | `78,687 → 35,462` | `-54.93%` | `40.516 → 23.340`秒 | `-42.39%` |
| A02 | `200,556 → 240,098` | `+19.72%` | `99.226 → 103.628`秒 | `+4.44%` |
| F01 | `152,145 → 126,794` | `-16.66%` | `77.992 → 82.273`秒 | `+5.49%` |
| F02 | `227,924 → 185,460` | `-18.63%` | `96.853 → 97.227`秒 | `+0.39%` |
| F03 | `140,599 → 110,193` | `-21.63%` | `76.980 → 80.831`秒 | `+5.00%` |
| F04 | `186,329 → 177,252` | `-4.87%` | `108.602 → 96.641`秒 | `-11.01%` |
| F05 clarify | `34,901 → 34,126` | `-2.22%` | `21.578 → 24.637`秒 | `+14.17%` |
| F05 out-of-scope | `36,850 → 34,264` | `-7.02%` | `22.669 → 26.257`秒 | `+15.83%` |
| F06 | `142,781 → 125,033` | `-12.43%` | `77.804 → 74.299`秒 | `-4.51%` |
| F07 runner | `116,485 → 113,645` | `-2.44%` | `73.801 → 70.057`秒 | `-5.07%` |
| F07 dependency | `93,133 → 99,151` | `+6.46%` | `61.013 → 71.832`秒 | `+17.73%` |
| F08 | `113,073 → 110,840` | `-1.97%` | `81.632 → 89.955`秒 | `+10.20%` |
| F10 inventory | `102,019 → 95,107` | `-6.78%` | `74.172 → 70.214`秒 | `-5.33%` |
| F10 monthly | `95,233 → 86,347` | `-9.33%` | `58.921 → 65.930`秒 | `+11.90%` |

## 挙動分析と判断材料

事実として、A01は未固定outcomeのままtarget evidenceへ入る経路を5 / 5件で閉じた。A02はcanonical成果5 / 5を維持した。したがって、A01のoutcome authorityとA02のimplementation authorityを同じ境界で扱わないという設計判断は成立した。

token中央値は14 case中12 caseで小さく、増えたのはA02とF07 dependencyだけだった。全体のtoken削減はA01だけに依存せず、F01、F02、F03、F06でも`12.43%`以上小さい。一方、elapsedは8 caseで長く、集約中央値は`+0.25%`だった。token削減をelapsed短縮と同一視しない。

A02のcost増は、clarificationへ誤停止せずrepository evidenceからcanonical implementationを解決する正常経路の作業量を含む。A01の不要な再入を減らしながらA02の必要な探索を残すという目的は達成したが、A02自体の効率は次の独立した分析対象である。具体的なpath whitelistやExecutor変更をこの結果から導かない。

## 重複実行の除外

先行campaign `r1`と後続campaign `r3`は、別controllerが同時刻に動作してhost全体の資格上限`M=24`を超えた。両campaignは各55 / 55件がvalidかつscore `4`だったが、実効並列条件を満たさないためKPI比較から除外した。v3へ登録済みのCandidate116 result `c87d1d93b28349cd96ecb55397a45543`は履歴として保持し、採用根拠に使わない。

正規結果は、C108の70件とtargeted C116の15件だけをimportしたisolated registry v4で不足55件を再計画し、競合process 0を確認して単独実行した`r4`である。これにより、重複runを選択へ混ぜず、既存15件の再利用も維持した。

## 状態

`targeted_a01_a02_f01_evaluated / standard14_evaluated / quality_gate_passed / mechanism_gate_passed / token_improved / elapsed_near_flat_slightly_higher / result_registered / adoption_not_decided`

これは採用、release、runtime projection、THE-CAPTION本体反映を意味しない。

## 証跡

- targeted campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate116-outcome-implementation-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146-20260731-r1`
- targeted execution archive SHA-256: `e155265f8ce8b59b0d62cfb88f78df1160e84afb2f13a23d6aff4ce4d6778a02`
- targeted final archive SHA-256: `c159d90c15859e394fe1b173ac3006cd6ccd4db8b7d1733ec4e849b7cfdb9708`
- 正規Standard14 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate116-outcome-implementation-boundary-v14-medium-standard14-atomic-reuse-n5-cli0146-20260731-r4`
- 正規Standard14 execution archive SHA-256: `722363caeb4fa5e647ef3e0c6db1e1eb84874cb8e137c0353ac884e7e6e4478f`
- 正規Standard14 final archive SHA-256: `6b1404c5c471262a05c02a6702ed2bb3bdbb5abcdec6219b1f7b9a601a7e41b4`

# Candidate98 / Candidate104 staged evidence admission Rating v14 Medium 標準14 N=5

## 結論

Candidate104を、保存済みCandidate98 resultへ互換条件を固定した標準14項目各`N=5`で実行した。Candidate104は70 / 70件がvalid・rateable・score `4`で、excluded attemptは0件だった。targeted A02 / F07 gateとStandard14 quality gateの両方を通過した。

Candidate104 minus Candidate98の5 iteration集約中央値差は、quality `0.000`、all-agent token `-121,141`（`-6.48%`）、elapsed `-100.745`秒（`-9.77%`）だった。これは固定Standard14 N=5の記述差であり、一般的効果、採用、release、runtime projectionを意味しない。

現在状態を`targeted_a02_f07_evaluated / mechanism_gate_passed / standard14_evaluated / quality_gate_passed / result_registered / adoption_not_decided`とする。B20、release、THE-CAPTION本体反映は未実施・未判断である。

## 実行前gate

- reference result: Candidate98 `1d124a27f74a485d855e1f8f275ed0c9`
- reference content SHA-256: `e601a13ee6bcb254641c6202030d60aeba637afab2d15339ad77f7072d850a02`
- Evaluation set: `the-caption-standard14-r1/r1`
- set identity SHA-256: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- coverage: 標準14項目、各iteration `1..5`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- model / reasoning: `gpt-5.6-sol` / `medium`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- CLI / runtime: Codex CLI `0.146.0` / Python `3.14.5`
- execution: global queue / 設定上の`M=24` / `N=5`

保存済みCandidate98のLayer 1を`prepare-comparison-layer1`で検証・複製した。profile、70 capsule、global planは`preflight-comparison`で機械照合し、`comparison-preflight.json`が70 slotを承認した後にだけ発行した。

旧profile r1はトップレベル`iterations`がなく、r2は保存済みcoverageとcase順が異なったため、どちらも正規preflightを通せなかった。r3で`iterations=5`と保存済みcoverage順を固定した。両失敗preflightはslotを一件も発行していない。

## 3 KPI

| prompt | valid / score 4 | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate98 | `70 / 70` | `100.000` | `1,869,862` | `9,884,513` | `1,031.319`秒 | `5,341.068`秒 |
| Candidate104 | `70 / 70` | `100.000` | `1,748,721` | `8,852,846` | `930.574`秒 | `4,654.722`秒 |
| Candidate104 - Candidate98 | score 4 `0` | `0.000` | `-121,141`（`-6.48%`） | `-1,031,667`（`-10.44%`） | `-100.745`秒（`-9.77%`） | `-686.346`秒（`-12.85%`） |

## iteration別内訳

各iterationはStandard14の14 caseを一件ずつ合計した値である。qualityはC98、C104とも全iterationで14 / 14件がscore `4`、`100.000`だった。

| iteration | C98 token | C104 token | token差 | C98 elapsed | C104 elapsed | elapsed差 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `2,105,611` | `1,943,945` | `-161,666`（`-7.68%`） | `1,089.294`秒 | `962.043`秒 | `-127.250`秒（`-11.68%`） |
| 2 | `1,851,954` | `1,692,372` | `-159,582`（`-8.62%`） | `1,031.319`秒 | `894.509`秒 | `-136.810`秒（`-13.27%`） |
| 3 | `1,869,862` | `1,664,543` | `-205,319`（`-10.98%`） | `1,027.500`秒 | `948.408`秒 | `-79.092`秒（`-7.70%`） |
| 4 | `1,789,988` | `1,803,265` | `+13,277`（`+0.74%`） | `1,026.190`秒 | `919.188`秒 | `-107.001`秒（`-10.43%`） |
| 5 | `2,267,098` | `1,748,721` | `-518,377`（`-22.87%`） | `1,166.766`秒 | `930.574`秒 | `-236.192`秒（`-20.24%`） |

C104のtokenは4 / 5 iterationでC98より少なく、iteration 4だけ`+0.74%`だった。elapsedは5 / 5 iterationで短かった。N=5の記述値であり、反復差の統計的有意性は判定しない。

## case別内訳

各caseの値はiteration 1〜5の中央値と最小〜最大である。`C98比`はC104中央値からC98中央値を引いた比率で、負値はC104の値が小さいことを示す。

| case | score 4 | C104 token中央値（最小〜最大） | C98比 | C104 elapsed中央値（最小〜最大） | C98比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 latent mode policy | `5 / 5` | `108,956`（`38,167〜110,506`） | `+23.63%` | `49.091`秒（`22.421〜56.009`） | `+19.92%` |
| A02 repository-resolvable V4 routing | `5 / 5` | `171,116`（`129,084〜209,293`） | `-25.02%` | `90.355`秒（`75.007〜116.822`） | `+5.99%` |
| F01 duplicate asset key | `5 / 5` | `194,401`（`157,810〜212,676`） | `+44.37%` | `72.605`秒（`61.809〜86.202`） | `-16.98%` |
| F02 history date bound | `5 / 5` | `189,556`（`135,901〜272,834`） | `-24.78%` | `86.154`秒（`83.522〜102.697`） | `-25.59%` |
| F03 atomic context cleanup | `5 / 5` | `149,536`（`112,196〜192,530`） | `+16.61%` | `82.983`秒（`66.642〜95.750`） | `-3.82%` |
| F04 audit column visibility | `5 / 5` | `181,863`（`134,097〜249,003`） | `+22.01%` | `78.182`秒（`66.277〜107.596`） | `-2.25%` |
| F05 clarify units mode | `5 / 5` | `38,921`（`38,657〜38,982`） | `+0.97%` | `21.164`秒（`18.119〜22.743`） | `-18.23%` |
| F05 out-of-scope deploy | `5 / 5` | `39,049`（`38,890〜42,199`） | `+1.06%` | `22.468`秒（`19.189〜35.909`） | `-13.71%` |
| F06 empty snapshot contract | `5 / 5` | `173,115`（`131,188〜214,450`） | `+7.01%` | `72.731`秒（`64.107〜93.150`） | `-21.12%` |
| F07 canonical V4 runner | `5 / 5` | `128,298`（`101,668〜141,121`） | `-30.67%` | `83.377`秒（`68.047〜85.939`） | `+4.18%` |
| F07 dependency provenance | `5 / 5` | `102,126`（`92,985〜103,122`） | `-0.54%` | `55.040`秒（`38.975〜68.191`） | `-22.35%` |
| F08 canonical CLI reference | `5 / 5` | `115,880`（`93,065〜162,068`） | `-10.41%` | `76.088`秒（`65.001〜80.544`） | `-22.23%` |
| F10 entrypoint inventory | `5 / 5` | `107,922`（`105,715〜109,311`） | `+0.98%` | `74.756`秒（`56.195〜90.524`） | `-7.54%` |
| F10 monthly format review | `5 / 5` | `96,573`（`90,397〜98,711`） | `-0.48%` | `53.051`秒（`48.215〜64.517`） | `-31.65%` |

case中央値では、C104はtokenが6 / 14 case、elapsedが11 / 14 caseでC98より小さかった。両KPIが小さいcaseはF02、F07 dependency、F08、F10 monthlyの4件、両方大きいcaseはA01の1件だった。残り9件はtokenとelapsedの方向が分かれた。この内訳もcaseごとのN=5診断であり、個別caseの一般的な効率差を確定しない。

Candidate104のcommand protocol violationは0件、Monthly reviewの数値位置は5 / 5でexactだった。owner-producer evidence inadmissible 55 / 70はRating v14のdiagnostic onlyであり、quality scoreを変更しない。

## Result identity

- Candidate104 result ID: `6321dcdbe8a54599a07c7ca139a850ea`
- Candidate104 content SHA-256: `74eea9554af185728041fa4ba2f0230f8e75358f0a70363ff8c515612dd08288`
- Candidate104 profile: [`candidate104-staged-evidence-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r3`](../profiles/candidate104-staged-evidence-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r3.json)
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146-20260730-r5`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/candidate98-candidate104-v14-medium-standard14-n5-cli0146-20260730-r2.json`
- execution archive SHA-256: `e3285ad29e523926410636b29bb2b8e8ef0daf08298fc96aa3627f3650f62ce2`
- final archive SHA-256: `743449b77ba97482a6e696ae2e3783e73a9f3a296f29310af0ebf592f87d5816`

先行campaign r2の登録result `01c42499f4d34b9ba488a57e82e1890e`は、現行規則が必須とする`comparison-preflight.json`なしで発行されていた。履歴として削除しないが、primary result、比較根拠、再利用可能な正式結果として扱わない。

raw run evidenceはverification checkoutに保持し、このrepositoryへcommitしない。

# Candidate104 / Candidate105 validation terminal return Rating v14 Medium 標準14 N=5

## 結論

Candidate105を、保存済みCandidate104 resultへ互換条件を固定した標準14項目各`N=5`で実行した。以前のtargeted F03停止条件は履歴として保持し、ユーザーがStandard14評価だけを明示的に再開した。Candidate105は70 / 70件がvalid・rateable・score `4`で、excluded attemptは0件だった。

Candidate105 minus Candidate104の5 iteration集約中央値差は、quality `0.000`、all-agent token `+12,257`（`+0.70%`）、elapsed `+24.669`秒（`+2.65%`）だった。70件合計ではtoken `-126,362`（`-1.43%`）、elapsed `+82.045`秒（`+1.76%`）であり、集約中央値の両KPI改善は成立しない。

F03の検証後再取得なしはCandidate104の2 / 5からCandidate105の4 / 5へ増えた。Candidate105のrequired validation再実行は0 / 5だったが、1件はfull gate出力上限後にdiff / statusだけを再取得した。制御は改善したが完全には閉じていない。

現在状態を`targeted_f03_stopped_gate_user_reopened_for_standard14 / standard14_evaluated / quality_gate_passed / terminal_return_improved_not_complete / result_registered / adoption_not_decided`とする。B20、採用、release、runtime projection、本体反映は未実施・未判断である。

## 実行前gate

- reference result: Candidate104 `6321dcdbe8a54599a07c7ca139a850ea`
- reference content SHA-256: `74eea9554af185728041fa4ba2f0230f8e75358f0a70363ff8c515612dd08288`
- Evaluation set: `the-caption-standard14-r1/r1`
- set identity SHA-256: `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33`
- coverage: 標準14項目、各iteration `1..5`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- model / reasoning: `gpt-5.6-sol` / `medium`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- CLI / runtime: Codex CLI `0.146.0` / Python `3.14.5`
- execution: global queue / 設定上の`M=24` / `N=5`

保存済みCandidate98のclean Layer 1を`prepare-comparison-layer1`で複製し、Candidate104 resultのfixture identityとcoverageへ機械照合した。profile、70 capsule、global planは`preflight-comparison`で検証し、`comparison-preflight.json`がCandidate104 resultを基準として70 slotを承認した後にだけ発行した。

準備r1はCandidate104 Layer 1に保存済みのcomparison receiptまで複製し、新receiptのwrite-once保存と衝突したためslot発行前に停止した。r2では同じset / fixture identityを持つclean Layer 1を使用し、Candidate104 resultへの照合を通した。r1は失敗証跡として保持し、model slotは発行していない。

## 3 KPI

| prompt | valid / score 4 | quality中央値 | token中央値 | token合計 | elapsed中央値 | elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate104 | `70 / 70` | `100.000` | `1,748,721` | `8,852,846` | `930.574`秒 | `4,654.722`秒 |
| Candidate105 | `70 / 70` | `100.000` | `1,760,978` | `8,726,484` | `955.243`秒 | `4,736.766`秒 |
| Candidate105 - Candidate104 | score 4 `0` | `0.000` | `+12,257`（`+0.70%`） | `-126,362`（`-1.43%`） | `+24.669`秒（`+2.65%`） | `+82.045`秒（`+1.76%`） |

## iteration別内訳

各iterationはStandard14の14 caseを一件ずつ合計した値である。qualityは両promptとも全iterationで14 / 14件がscore `4`、`100.000`だった。

| iteration | C104 token | C105 token | token差 | C104 elapsed | C105 elapsed | elapsed差 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `1,943,945` | `1,768,312` | `-175,633`（`-9.03%`） | `962.043`秒 | `926.813`秒 | `-35.230`秒（`-3.66%`） |
| 2 | `1,692,372` | `1,724,303` | `+31,931`（`+1.89%`） | `894.509`秒 | `897.159`秒 | `+2.650`秒（`+0.30%`） |
| 3 | `1,664,543` | `1,760,978` | `+96,435`（`+5.79%`） | `948.408`秒 | `982.333`秒 | `+33.925`秒（`+3.58%`） |
| 4 | `1,803,265` | `1,879,295` | `+76,030`（`+4.22%`） | `919.188`秒 | `975.218`秒 | `+56.030`秒（`+6.10%`） |
| 5 | `1,748,721` | `1,593,596` | `-155,125`（`-8.87%`） | `930.574`秒 | `955.243`秒 | `+24.669`秒（`+2.65%`） |

tokenは2 / 5 iteration、elapsedは1 / 5 iterationでCandidate104より小さかった。N=5の記述値であり、反復差の統計的有意性は判定しない。

## case別内訳

各caseの値はCandidate105のiteration 1〜5の中央値と最小〜最大である。`C104比`はCandidate105中央値からCandidate104中央値を引いた比率で、負値はCandidate105の値が小さいことを示す。

| case | score 4 | C105 token中央値（最小〜最大） | C104比 | C105 elapsed中央値（最小〜最大） | C104比 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 latent mode policy | `5 / 5` | `90,651`（`60,339〜217,527`） | `-16.80%` | `41.555`秒（`30.583〜65.506`） | `-15.35%` |
| A02 repository-resolvable V4 routing | `5 / 5` | `138,171`（`128,103〜139,469`） | `-19.25%` | `75.770`秒（`66.734〜79.713`） | `-16.14%` |
| F01 duplicate asset key | `5 / 5` | `159,798`（`134,421〜204,255`） | `-17.80%` | `70.711`秒（`64.231〜85.308`） | `-2.61%` |
| F02 history date bound | `5 / 5` | `245,101`（`135,943〜274,978`） | `+29.30%` | `87.428`秒（`75.595〜128.474`） | `+1.48%` |
| F03 atomic context cleanup | `5 / 5` | `134,026`（`106,735〜196,835`） | `-10.37%` | `76.778`秒（`66.340〜94.434`） | `-7.48%` |
| F04 audit column visibility | `5 / 5` | `153,590`（`119,403〜175,169`） | `-15.55%` | `92.989`秒（`87.156〜100.597`） | `+18.94%` |
| F05 clarify units mode | `5 / 5` | `39,339`（`39,034〜39,777`） | `+1.07%` | `24.914`秒（`18.577〜28.221`） | `+17.72%` |
| F05 out-of-scope deploy | `5 / 5` | `39,162`（`39,049〜41,606`） | `+0.29%` | `21.481`秒（`18.601〜23.315`） | `-4.39%` |
| F06 empty snapshot contract | `5 / 5` | `126,070`（`107,502〜151,247`） | `-27.18%` | `81.575`秒（`67.006〜87.754`） | `+12.16%` |
| F07 canonical V4 runner | `5 / 5` | `132,070`（`128,639〜133,561`） | `+2.94%` | `77.662`秒（`69.331〜86.156`） | `-6.86%` |
| F07 dependency provenance | `5 / 5` | `103,901`（`93,032〜104,334`） | `+1.74%` | `60.090`秒（`58.941〜72.674`） | `+9.17%` |
| F08 canonical CLI reference | `5 / 5` | `150,060`（`125,110〜172,505`） | `+29.50%` | `87.221`秒（`72.676〜91.257`） | `+14.63%` |
| F10 entrypoint inventory | `5 / 5` | `114,393`（`109,093〜131,328`） | `+6.00%` | `71.386`秒（`62.871〜86.577`） | `-4.51%` |
| F10 monthly format review | `5 / 5` | `102,276`（`92,330〜119,422`） | `+5.91%` | `54.710`秒（`52.998〜71.949`） | `+3.13%` |

case中央値では、Candidate105はtokenが6 / 14 case、elapsedが6 / 14 caseでCandidate104より小さかった。両KPIが小さいcaseはA01、A02、F01、F03の4件、両方大きいcaseはF02、F05 clarify、F07 dependency、F08、F10 monthlyの5件だった。

## F03 mechanism診断

Candidate104ではfull gate成功出力の末尾欠落後にdiff / statusを再取得したrunが3 / 5あり、再取得なしは2 / 5だった。Candidate105では再取得が1 / 5、再取得なしが4 / 5へ改善した。両promptともfocused / full validationそのものの再実行は0 / 5だった。

Candidate105の1件は、full gate `326 passed, 3 skipped`を確認できた一方、同じ実行票末尾のdiff / statusが出力上限で欠落したため、その二つだけを再取得した。これはCandidate105の非目標に置いたtool result truncation / delivery軸である。一回wrapperを5 / 5へするには、prompt規則の追加ではなく、長い成功出力と末尾のmachine-bound結果を同時に失わず返すexecutor側のterminal receiptが必要である。

command protocol violationは0件だった。owner-producer evidence inadmissible 55 / 70とMonthly reviewの数値位置mismatch 1 / 5はRating v14のdiagnostic-onlyであり、quality scoreを変更しない。

## Result identity

- Candidate105 result ID: `f7e02913c86c448d9d93090998867fc6`
- Candidate105 content SHA-256: `e3ce8c3be72b51d173a4867ba5d46eb6f1620f02f89fe98f1bbafda8d0cad41b`
- Candidate105 profile: [`candidate105-validation-terminal-return-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`](../profiles/candidate105-validation-terminal-return-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json)
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate105-validation-terminal-return-v14-medium-standard14-n5-cli0146-20260730-r2`
- stopped preparation: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate105-validation-terminal-return-v14-medium-standard14-n5-cli0146-20260730-r1`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/candidate104-candidate105-validation-terminal-return-v14-medium-standard14-n5-cli0146-20260730-r1.json`
- execution archive SHA-256: `625c7fbc0936698597516bc3f8e9eebe95b828f04fef8a38f69060813c06313e`
- final archive SHA-256: `ac22c48a8a54b8c604dd811ae4d0c9ed0fc132cf851f60075e53d286e6323b72`

raw run evidenceはverification checkoutに保持し、このrepositoryへcommitしない。

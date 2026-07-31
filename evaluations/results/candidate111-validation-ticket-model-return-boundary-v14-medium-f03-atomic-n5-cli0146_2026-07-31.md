# Candidate111 validation実行票model return boundary F03 atomic N=5結果

## 結論

Candidate111のF03 r2 N=5は5 / 5件がvalid・rateable・score `4`で、required validationも全件一回だった。保存済みCandidate108との互換比較ではquality同値、token中央値`-1,394`（`-0.99%`）、elapsed中央値`-7.193`秒（`-9.34%`）だった。

一方、判断価値のない途中状態へmodel return horizonを明示的に選んだrunは4 / 5件だった。そのうち`1000ms`を選んだ2件は2 / 2件がcell ID付きnonterminal resultを返し、同じcell IDへの継続待機だけを行うためにmodelへ再入した。`30000ms`を選んだ2件は処理が先にterminalとなり、残る1件は外側のreturn horizonを明示しなかった。

中間messageは0件で表示は抑制されたが、目的である不要なmodel再入の削減は3 / 5件に留まった。KPI差を狙った制御の効果へbindできないため、Standard14へ進めず停止する。

## 固定条件

- candidate: `the-caption-3ce91a4-validation-ticket-model-return-boundary-r1`
- bundle SHA-256: `9fec65235bb1c1940046e104aba531ff448a1d47e37f45c41b3323995d4519d0`
- direct parent / reference: Candidate108
- case: `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- N: 5
- profile上のM: 24
- atomic pool key: `fc149a670eaa536ab4c2080e47245afbbb3d017308e3271bcd59ee612facea1c`
- comparison key: `6374fd3705e8f9afead12a3cea1ba8e0b2ccd0b2d62f6a4443381fbfc061083d`

## 3 KPI

| 項目 | Candidate108 | Candidate111 | C111 - C108 |
| --- | ---: | ---: | ---: |
| quality中央値 | `100.0` | `100.0` | `0.0` |
| token中央値 | `140,599` | `139,205` | `-1,394`（`-0.99%`） |
| elapsed中央値 | `76.980`秒 | `69.787`秒 | `-7.193`秒（`-9.34%`） |

Candidate111は5 / 5件がscore `4`だった。owner-producer evidenceは5件ともproducer候補0で`failed`だったが、Rating v14では`diagnostic_only`である。提示済み成果条件、必須command evidence、許可pathの成立を確認して採点した。

## model return挙動

| 項目 | 件数 |
| --- | ---: |
| validation ticket wrapper一回 | `5 / 5` |
| focused / full validation一回・成功 | `5 / 5` |
| modelが外側のreturn horizonを明示 | `4 / 5` |
| outer `1000ms` | `2 / 5` |
| outer `30000ms` | `2 / 5` |
| outer horizon明示なし | `1 / 5` |
| terminal前model再入なし | `3 / 5` |
| cell ID付きnonterminal result | `2 / 5` |
| nonterminal後、同じcell IDへwait-only | `2 / 2` |
| nonterminal後の新しい判断 | `0 / 2` |
| nonterminal後の中間message | `0 / 2` |
| required validation再実行 | `0 / 5` |

「terminal前model再入なし」3件のうち2件は`30000ms`以内に処理が完了した結果であり、model return要求自体を抑制できた成功ではない。したがって、観測上のterminal deliveryと発行時の制御選択を分けて判定した。

## 再入場別の診断

| KPI | 再入場なし `n=3` | 再入場あり `n=2` | 再入場あり - なし |
| --- | ---: | ---: | ---: |
| quality | 全件`100.0` | 全件`100.0` | 同等 |
| token中央値 | `120,797` | `140,731` | `+19,934`（`+16.50%`） |
| elapsed中央値 | `81.311`秒 | `63.926`秒 | `-17.385`秒（`-21.38%`） |

tokenはC110と同じく再入場ありで高かった。一方、elapsedは再入場ありで短く、run間変動も大きい。`n=3 / 2`の事後群分けであり、因果または範囲外の一般化には使わない。

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate111-validation-ticket-model-return-boundary-v14-medium-f03-atomic-n5-cli0146-20260731-r1`
- comparison preflight SHA-256: `df5cc484aabc7dceda614776a6dfe75a06537ba39a9d4abe3d28cfbd26561073`
- execution archive SHA-256: `2b9e0f08dfceea338f525b086571f381a3e90e8f451d812c4c76929e42d48bd3`
- quality audit SHA-256: `5ae6802a90cae992bcc8510e859e3c1aceef2521f9fb42bbd3431e71bae08415`
- mechanism audit SHA-256: `5dd954fa8b76560736a77804787214e5a101ecf3945e40103257ce7fada7a94c`
- selection SHA-256: `2e0871bd7090d60b3ec5fc407766da3da8ea91685fabed783eda681e1e652642`
- analysis SHA-256: `3f8e53b3dd110f0fe2f3a6fcff8829c48b59cfef6f8fdb0d63e2395f277ac60a`
- comparison SHA-256: `fd9e38cc60bb7db5feea994a440a4d370b8693067f6114fc9b246c843b859422`

## 状態

`targeted_f03_evaluated / quality_gate_passed / targeted_cost_both_lower / model_return_gate_failed / result_registered / stopped`

これは採用、release、runtime projection、THE-CAPTION本体反映を意味しない。

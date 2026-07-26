# Candidate71 / Candidate81 validation wrapper precedence Rating v13 Medium 標準14項目 N=5

## 結論

Candidate81は標準14項目70 / 70件でvalid・rateable・score `4`となり、quality gateを通過した。

保存traceで確認できる複数required commandの7 caseでは、1-step closureが既存Candidate71の30 / 35からCandidate81の35 / 35になった。差はF04の0 / 5から5 / 5であり、他6 caseは両promptとも5 / 5だった。したがって、Candidate81は狙ったF04の逐次model再入を標準14項目campaignでも消し、他の複数command caseを崩さなかった。

この結果はRating v13、reasoning effort `medium`、標準14項目、各`N=5`に限定する。Candidate71は再実行せず、同じ互換条件の登録済みresultと保存traceを固定参照した。採用、release、runtime projectionは判断しない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| evaluation set | `the-caption-standard14-r1` revision `r1` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| repetition | 14 case × `N=5` = 70 slot |
| schedule | global queue、`M=24` |
| command evidence protocol | v1 |
| token accounting | all-agent v1 |
| evaluation set identity SHA-256 | `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db` |
| comparison conditions SHA-256 | `f76bf65fef7dbedd26cc7afaa66e7a4fe1af60f968d37eb88e72091dd91fcbbb` |
| compatibility key | `79ed04a45971db8ffc2287aea064af8b448008da510d27ceefd70862e0ad40d8` |

両profileの差は`profile_id`と`prompt_set_identity`だけである。

## 一次result

| prompt | result ID | content SHA-256 | valid / rateable | score分布 | excluded attempt |
| --- | --- | --- | ---: | --- | ---: |
| Candidate71 | `267130a37c3544c7bb6e39c94f03c6e4` | `db8d4dd5984d089f5e78a9e1e0724ee495cc6da54c1a8984461124b9b603e8b3` | 70 / 70 | `4 = 70` | 0 |
| Candidate81 | `d97458bb526b41b094f92a5c35409326` | `ebe4f772ac0d9584ead7a63769a1f2ee13c04590db9b14527ccc76bbdfca09f8` | 70 / 70 | `4 = 70` | 0 |

Candidate81はresult登録とfinal compactを完了した。

## 3 KPI

| KPI | Candidate71 | Candidate81 | C81 - C71 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 | 0.00% |
| all-agent token中央値 | 1,923,688 | 1,917,979 | -5,709 | -0.30% |
| elapsed中央値 | 948.869秒 | 1,003.744秒 | +54.875秒 | +5.78% |
| 70件token合計 | 9,475,504 | 9,502,252 | +26,748 | +0.28% |
| 70件elapsed合計 | 4,754.179秒 | 4,993.269秒 | +239.090秒 | +5.03% |

tokenとelapsedは診断値であり、prompt動作安定性の合否条件には使わない。公式Layer 4 comparisonの中央値差はquality `0.000`、token `-5,709`、elapsed `+54.875秒`である。

## 1-step closure診断

各caseのmodel-visible required command markerが、一つのcustom tool call内の個別`exec_command`発行にすべて含まれるrunを1-step closureと数えた。両promptともcommand protocol violationは0件だった。

| 複数required command case | Candidate71 | Candidate81 |
| --- | ---: | ---: |
| F01 domain duplicate asset key | 5 / 5 | 5 / 5 |
| F02 cross-layer history date bound | 5 / 5 | 5 / 5 |
| F03 atomic context cleanup | 5 / 5 | 5 / 5 |
| F04 web audit column visibility | 0 / 5 | 5 / 5 |
| F06 restore empty snapshot contract | 5 / 5 | 5 / 5 |
| F07 canonical V4 runner | 5 / 5 | 5 / 5 |
| F07 dependency provenance pair | 5 / 5 | 5 / 5 |
| 合計 | 30 / 35 | 35 / 35 |

Candidate81のF04 5件はすべて`npm ci`、lint、buildを一つのcustom wrapper内から発行した。targeted F04 N=10の10 / 10と合わせると、Candidate81は同一F04課題で合計15 / 15の1-step closureを観測した。ただし、campaign条件が異なるため15件を一つのKPI resultへ集約しない。

## その他の診断

| diagnostic | Candidate71 | Candidate81 |
| --- | ---: | ---: |
| command protocol violation | 0 | 0 |
| owner-producer evidence inadmissible | 55 | 55 |
| F10 Monthly数値line | exact 5 / 5 | exact 5 / 5 |

owner-producer evidenceはRating v13では診断専用であり、quality scoreを変更しない。

## 判定

- Candidate81は`standard14_evaluated / quality_gate_passed / prompt_stability_gate_passed`とする。
- Candidate81へ補助predicateを追加しない。
- 今回の結果だけで採用、release、runtime projectionを行わない。
- 比較条件を変えない後続試験では、Candidate71を再実行せず既存resultを固定参照する。

## 保存artifact

- Candidate81 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate81-validation-wrapper-precedence-v13-reasoning-medium-standard14-global-m24-n5-20260726-r1`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/candidate71-candidate81-v13-reasoning-medium-standard14-n5-20260726-r1.json`

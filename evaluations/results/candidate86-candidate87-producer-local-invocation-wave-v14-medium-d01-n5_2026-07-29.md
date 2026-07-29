# Candidate86 / Candidate87 producer-local invocation wave Rating v14 Medium D01 N=5

## 結論

Candidate87は、C86で増えていたproducer内部のinvocation分割を解消した。child custom exec call合計は`41 → 12`、child token合計は`873,848 → 327,314`になった。all-agent中央値もtoken`-133,583`（`-51.06%`）、elapsed`-35.897`秒（`-26.54%`）であり、5 iterationすべてでC86を下回った。

C87は5 / 5件がscore `4`で、quality、producer route、C86比costの一軸qualificationを通過した。保存済みC81との互換比較では、token中央値は`-14,694`（`-10.29%`）、elapsed中央値は`+6.606`秒（`+7.12%`）だった。両KPI悪化の停止条件には該当しない。現在状態を`targeted_d01_evaluated / qualification_passed / f02_not_run`とする。

## Identity

- evaluation set: `the-caption-planning-first-d01-r1`
- set identity SHA-256: `26cb5bd75f84168ab952c80a94603a0f0e1f70d4995537cd11157c8792b9f081`
- case: `TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `32332fd9e9d519812fb75613fd7d99d47ecb288253af5479f60c32befb2cf7c6`
- C86 result: `3a5f2d7d33804da986ab5195c270b5c4`
- C87 result（当初登録・誤採点履歴）: `06e34a45334343a1ba9d55ba219bae1e`
- C87 result（契約binding訂正）: `27b73ffe18bf47a99e15541c91c9d6e5`

試験内容は変更していない。D01 r1のmodel-visible TaskSpec、fixture、oracle、allowed read、local task name、canonical producer identityをC86 / C87へ同一に適用した。prompt identity以外のcomparison conditionsも一致する。

## 3 KPI

| prompt | score 4 | score 3 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C86 | 5 / 5 | 0 / 5 | `261,647` | `1,176,054` | `297,475` | `135.277`秒 | `670.670`秒 | `165.658`秒 |
| C87 | 5 / 5 | 0 / 5 | `128,064` | `714,954` | `190,500` | `99.380`秒 | `514.752`秒 | `112.652`秒 |
| C87 - C86 | `0` | `0` | `-133,583` | `-461,100` | `-106,975` | `-35.897`秒 | `-155.918`秒 | `-53.006`秒 |

token合計はC86比`-39.21%`、elapsed合計は`-23.25%`だった。品質差があるため、このcost差だけを採用根拠にはしない。

## Paired diagnostic

| iteration | C87 score | token差 | elapsed差 |
| ---: | ---: | ---: | ---: |
| 1 | `4` | `-17,400` | `-4.163`秒 |
| 2 | `4` | `-75,144` | `-11.958`秒 |
| 3 | `4` | `-117,270` | `-37.748`秒 |
| 4 | `4` | `-144,311` | `-49.044`秒 |
| 5 | `4` | `-106,975` | `-53.006`秒 |

## Producer route

- C87は5 / 5件でcanonical agent path `/root/monthly_format_review_producer`のchildを一つ起動した。
- 各runのsession graphはroot 1 + child 1だった。
- child terminal resultは5 / 5件でroot final responseへbindされた。
- rootによるreview predicateの再実行は0件だった。
- artifact変更は0件だった。

標準`owner-producer-evidence/v1` collectorはC86と同様、C87も5 / 5件を`inadmissible`とした。collectorはcriterion owner文字列`independent response check`とagent pathを照合するため、TaskSpecへ直接固定されたcanonical producer identityを候補へ含めない。D01固有routeの判定は保存all-agent usage、child terminal result、root final responseを用い、collectorの正式eligibilityとは区別する。

## Invocation diagnostic

| child内訳 | C86 | C87 | 差 |
| --- | ---: | ---: | ---: |
| child token合計 | `873,848` | `327,314` | `-546,534` |
| child custom exec call合計 | `41` | `12` | `-29` |

C87 childは、開始identity確認を一つのwrapper、authority・fixed diff・source readを一つのwrapperへまとめる経路を再現した。終了時のzero-drift確認は、先行readの結果を受けた後の別invocationとして保持した。したがって、C87の`DECISION_BOUNDARY`置換は狙ったproducer-local invocation waveを実行trace上で成立させた。

iteration 2はfindingの内容、severity、impact、zero driftを満たしたが、locationを`src/app/entrypoints/monthly_main.py:24`と返した。固定diffの変更行は`25`である。当初の個別監査はcycleのv14 contract IDを渡さずv10既定値でscore `3`にした。正しいv14ではnumeric location mismatchはdiagnostic-onlyであり、append-only訂正resultのscoreは`4`である。旧resultと当時の停止判断は履歴として保持し、詳細は[`rating contract binding訂正`](targeted-review-rating-contract-binding-correction_2026-07-29.md)に分離する。

実行前2 attemptでは全5 slotがmodel-visible capability catalog不一致で除外された。合計10 attemptは`external_failure`であり、C87の品質・KPIへ混ぜていない。第3 attemptで5 / 5 valid slotがそろった。

## Gate

- quality gate: `passed`（score `4 = 5`）
- producer route: `passed_by_saved_trace / standard_collector_inadmissible`
- cost route against C86: `improved`（token / elapsed中央値とも許容幅`0`以内）
- cost route against saved C81: `tradeoff / stop条件非該当`（token中央値`-10.29%`、elapsed中央値`+7.12%`）
- Candidate87 state: `targeted_d01_evaluated / qualification_passed / f02_not_run`
- F02、F04、標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

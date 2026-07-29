# Candidate81 / Candidate86 producer plan fast path Rating v14 Medium D01 N=5

## 結論

Candidate81とCandidate86はD01で各5 / 5件がvalid・rateable・score `4`だった。両条件とも5 / 5件で指定worker identity `/root/monthly_format_review_producer`を起動し、そのterminal resultを最終responseへbindした。

Candidate86 minus Candidate81の中央値差は、quality `0.000`、all-agent token `+118,889`（`+83.28%`）、elapsed `+42.503`秒（`+45.81%`）である。tokenとelapsedが全5 iterationで増え、事前固定した許容幅`0`を両方超えたため、`quality_passed / producer_route_passed / cost_control_failed`とする。Candidate86を停止し、標準14、採用、release、本体反映へ進めない。

## Identity

- evaluation set: `the-caption-planning-first-d01-r1`
- set identity SHA-256: `26cb5bd75f84168ab952c80a94603a0f0e1f70d4995537cd11157c8792b9f081`
- case: `TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW/r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- repetition: 各`N=5`
- compatibility key: `32332fd9e9d519812fb75613fd7d99d47ecb288253af5479f60c32befb2cf7c6`
- C81 result: `35b81e15d20f452e987177649a785877`
- C86 result: `3a5f2d7d33804da986ab5195c270b5c4`

試験内容は変更していない。D01 r1のmodel-visible TaskSpec、fixture、oracle、allowed read、local task name、canonical producer identityをC81 / C86へ同一に適用した。新しいcase、fixture、oracle、Evaluation setは作成していない。

## 3 KPI

| prompt | score 4 | token中央値 | token合計 | token最大 | elapsed中央値 | elapsed合計 | elapsed最大 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C81 | 5 / 5 | `142,758` | `762,654` | `228,108` | `92.774`秒 | `488.866`秒 | `120.571`秒 |
| C86 | 5 / 5 | `261,647` | `1,176,054` | `297,475` | `135.277`秒 | `670.670`秒 | `165.658`秒 |
| C86 - C81 | `0` | `+118,889` | `+413,400` | `+69,367` | `+42.503`秒 | `+181.804`秒 | `+45.087`秒 |

token合計はC81比`+54.21%`、elapsed合計は`+37.19%`だった。中央値だけでなく合計、最大、paired iterationのすべてが悪化方向である。

## Paired diagnostic

| iteration | token差 | elapsed差 |
| ---: | ---: | ---: |
| 1 | `+20,925` | `+19.556`秒 |
| 2 | `+77,039` | `+20.434`秒 |
| 3 | `+33,539` | `+14.706`秒 |
| 4 | `+127,180` | `+50.428`秒 |
| 5 | `+154,717` | `+76.680`秒 |

## Producer route

- C81: 指定worker起動とterminal result受領 5 / 5
- C86: 指定worker起動とterminal result受領 5 / 5
- canonical agent path: `/root/monthly_format_review_producer`
- 各runのsession graph: root 1 + child 1
- artifact変更: 0
- review finding: 両条件とも固定diffのmajor findingを返した

標準`owner-producer-evidence/v1` collectorは両条件を5 / 5件`inadmissible`とした。collectorはcriterion owner文字列`independent response check`とagent pathを照合するため、TaskSpecへ直接固定されたcanonical producer identityを候補へ含めなかった。保存all-agent usageとroot eventには、指定agent pathのchild session、親子関係、terminal result受領がある。したがってD01固有routeは保存traceで成立と判断するが、collectorの正式eligibilityとは区別する。

## Cost route diagnostic

| child内訳 | C81 | C86 | 差 |
| --- | ---: | ---: | ---: |
| child token合計 | `340,228` | `873,848` | `+533,620` |
| child custom exec call合計 | `13` | `41` | `+28` |
| child reasoning item合計 | `18` | `27` | `+9` |
| child input token合計 | `332,223` | `859,559` | `+527,336` |
| child cached input合計 | `237,312` | `742,912` | `+505,600` |

C81 childは複数のread-only commandを同一custom wrapperへまとめる経路が中心だった。C86 childは同じ種類のcommandを個別custom exec callへ分割し、5 run合計のcall数が`13 → 41`へ増えた。model再入ごとにpromptと履歴が再入力され、child token増加がroot側の減少を上回った。

静的prompt本文の`+389 bytes`だけではこの増加を説明できない。C86のproducer fast pathと既存`DECISION_BOUNDARY`のinvocation batching境界が、worker内部で一貫して解釈されなかったことが原因候補である。厳密な因果割合は別candidateによる一軸比較なしには確定しない。

## Gate

- quality gate: `passed`
- producer route: `passed_by_saved_trace / standard_collector_inadmissible`
- cost state: `cost_control_failed`
- Candidate86 state: `targeted_f02_f04_d01_evaluated / stopped`
- 標準14、採用、release、THE-CAPTION本体反映: 未実施・未判断

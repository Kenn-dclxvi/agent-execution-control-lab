# Candidate71 / Candidate81 validation wrapper precedence Rating v13 Medium F04 N=10

## 結論

Candidate81は同一F04課題の1-step validation closureを10 / 10で再現し、prompt-only安定化の対象gateを通過した。今回のCandidate71は5 / 10だった。

成果品質は両条件とも10 / 10でscore `4`だった。required command欠落、protocol違反、順序違反、workspace driftは0件だった。Candidate81は`targeted_evaluated / prompt_stability_gate_passed`とする。

tokenとelapsedは診断値であり、prompt安定性の合否条件には使わない。この結果はF04 r2、reasoning effort `medium`、command evidence protocol v1、各`N=10`の対象試験に限定する。標準14項目、採用、release、runtime projectionへ読み替えない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| evaluation set | `the-caption-validation-wrapper-precedence-f04-r1` |
| case | `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` r2 |
| model | `gpt-5.6-sol` |
| reasoning effort | `medium` |
| command evidence protocol | v1 |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| repetition | 各`N=10` |
| effective max workers | `M=10` |
| token accounting | all-agent v1 |

両profileの差は`profile_id`と`prompt_set_identity`だけである。compatibility keyは両resultとも`64e170df55f4b49da32674ea4d0f62214be48710dc89a9c010e55aa3595abef0`で一致した。

## 一次result

| prompt | result ID | content SHA-256 | valid / rateable | score分布 |
| --- | --- | --- | ---: | --- |
| Candidate71 | `afafd2f87f67408796bd2a7430d41ad7` | `3938c218d56d13d6dda3472dba58b41826ec495a4c5ad48566420bc90141c046` | 10 / 10 | `4 = 10` |
| Candidate81 | `5daee84962e24b079b578d20fad02c5f` | `27643ca63e5c7f21eb3f61aeefecb41ed523e1e8d7dd4527a51985913f29ca35` | 10 / 10 | `4 = 10` |

両条件ともexcluded attempt、required command欠落、protocol違反、順序違反、workspace drift、worker起動は0件だった。

## 3 KPI

| KPI | Candidate71 | Candidate81 | C81 - C71 | 率 |
| --- | ---: | ---: | ---: | ---: |
| quality中央値 | 100.000 | 100.000 | 0.000 | 0.00% |
| all-agent token中央値 | 223,077 | 177,729 | -45,348 | -20.33% |
| elapsed中央値 | 101.732秒 | 94.210秒 | -7.522秒 | -7.39% |
| all-agent token合計 | 2,273,546 | 1,911,118 | -362,428 | -15.94% |
| elapsed合計 | 1,054.045秒 | 924.485秒 | -129.560秒 | -12.29% |

これらの効率差は今回の保存値であり、prompt安定性gateの根拠には使わない。

## 保存traceの行動診断

一つのcustom tool call内で`npm ci`、lint、buildを列挙順の個別`exec_command`として実行したrunを「1-step closure」と数えた。

| diagnostic | Candidate71 | Candidate81 | C81 - C71 |
| --- | ---: | ---: | ---: |
| 1-step closure run | 5 / 10 | 10 / 10 | +5 |
| validation custom tool call合計 | 20 | 10 | -10 |
| 全custom tool call | 80 | 67 | -13 |
| assistant message | 66 | 59 | -7 |

Candidate71はiteration 1、2、3、7、9でclosureした。Candidate81は10 runすべてで、3 required commandを1回のcustom exec wrapper内から発行した。Candidate81ではvalidation command間のトップレベルmodel再入は観測されなかった。

## 考察

事実として、Candidate80で残った1件の逐次解釈を対象に、「順に」「1 commandずつ個別」はwrapper内の発行順・invocation単位を意味し、command間でresultをmodelへ返す意味ではないと定義したCandidate81は10 / 10でclosureした。

この結果は、同じTaskSpecの挙動をpromptだけで安定化するという今回の目的に対する成功証拠である。ただしF04一課題・10反復の証拠であり、別課題への一般化やrelease判断を含まない。

## 判定と今後の対照運用

- Candidate81は対象prompt安定性gateを通過した。
- Candidate81へ補助predicateを追加しない。
- 標準14項目、採用、release、runtime projectionは未実施とする。
- 今後、model、reasoning effort、TaskSpec、case revision、protocol、executor parameterなどのcompatibility条件を変えない候補試験では、既存のCandidate71 resultを固定参照し、Candidate71を毎回再実行しない。
- C71の再実行は、比較条件を変更する場合、保存resultが失効した場合、またはbaseline drift自体を調べる試験として事前に固定した場合だけ行う。

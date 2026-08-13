# Candidate209 名前付きcertificate欠損境界 ADR9 r2 N=5結果

## 結論

Candidate209は45 / 45 valid、除外0件だったが、Score `4 / 1 = 42 / 3`で品質gateを通過しなかった。Score 1はすべて`TC-ADR07`で、期待`completion_ready / no_counterexample_found`に対して外側terminalが`unavailable`となり、artifactを変更せず必須commandも実行しなかった。

Candidate208のScore 1で観測した「packet内certificateが完成しているのにcertificate外missingを`unavailable`へ昇格する」経路を閉じる方向は働いた。一方、`certificate_deficit`を反例certificateの不足だけへ結び付け、欠損集合が空なら全manifest observationのconsumerを閉じたため、具体的反例がない場合に`no_counterexample_found`の全manifest closureを完成させる必要readまで3 / 5件で失った。

したがってCandidate209は`quality_failed / mechanism_failed / stopped`である。repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびruntime projectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-named-certificate-deficit-r1`
- bundle SHA-256: `4790214b24a560cfc34c93decde076cbf033c007ad8fd3f4533203d395c3925b`
- profile: `candidate209-named-certificate-deficit-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: 24
- reference result: Candidate208 `c4e84aef70aa4d5d9b97c09c6817605d`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 242.032秒

## 品質

| 指標 | 結果 |
| --- | ---: |
| valid | 45 / 45 |
| Score 4 | 42 |
| Score 1 | 3 |
| terminal一致 | 42 / 45 |
| artifact境界一致 | 42 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| forbidden canary delivery | 0 |

Score 1 runは次の3件である。

| case / iteration | run ID | 観測terminal | 期待terminal |
| --- | --- | --- | --- |
| `TC-ADR07` / 1 | `55d8603fe70b485a8f2d84faf1f3896a` | `unavailable` | `completion_ready` |
| `TC-ADR07` / 3 | `5c8893176b964602b2217581275d7662` | `unavailable` | `completion_ready` |
| `TC-ADR07` / 4 | `514aff48349d47e4a0e03eff3722cd86` | `unavailable` | `completion_ready` |

三runとも独立Reviewerは1件起動され、packet内に具体的反例がないことを認識した。しかし、`OBS-PAIRED-SCOPE`はcounterexample certificateの欠損componentを埋めないためread資格なし、全manifest receiptがないため`no_counterexample_found`不成立、排他的依存もないため真正な`unavailable`も不成立という閉路へ入り、rootはdesignをadmitしなかった。

これはReviewer起動、rootのresult非代行またはartifact停止の誤りではない。`counterexample_found`向けの欠損境界を`no_counterexample_found`の閉包証拠へ共用したことによる、result kind間のconsumer不足である。

## 機序

固定機序監査は7 runを不通過とした。

- `TC-ADR05`の3件で、packet反例成立後にもReviewerがrepository readを発行した
- `TC-ADR07`の3件で、必要なmanifest observationを取得せず`no_counterexample_found`を形成できなかった
- `TC-ADR09`の1件で、missing direct targetを観測せずに架空のsuccess receiptを構成して`no_counterexample_found`を返した。rootはこのresultを受理せず外側を`unavailable`へ停止したため品質は保持したが、result admission機序は不通過である

主要診断値は次のとおりである。

| 指標 | 結果 |
| --- | ---: |
| review required run | 30 |
| reviewer cardinality一致 | 45 / 45 |
| review result admission一致 | 41 / 45 |
| review result effect一致 | 42 / 45 |
| root direct prereadなし | 30 / 30 |
| counterexample result | 20 |
| counterexample後read違反 | 3 |
| reviewer closed-source read | 4 |
| reviewer mixed read | 1 |
| reviewer outside read | 3 |
| mechanism failure run | 7 |

`certificate_deficit={}`を全manifest observationのconsumer falseへ直結したことで、不要readは完全には閉じず、必要readと架空receiptの双方を不安定化させた。C209の修正軸は局所的には妥当だったが、`counterexample_found`のcertificate dependencyと`no_counterexample_found`のmanifest closure dependencyを同じ欠損集合へ縮退させた構成は採用できない。

## KPI

登録resultの中央値は次のとおりである。

- `quality_score`: 91.66666666666666
- all-agent `total_tokens`: 1,021,718
- `elapsed_seconds`: 665.9238881660276

品質gate不通過のため、Candidate208とのtoken・elapsed比較を改善または悪化の判定には使わない。Standard14も発行しない。

## 状態

`candidate209_ADR9_completed / valid_45 / score4_42 / score1_3 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 一次アーティファクト

- [登録result](095076f0eb7540c397dc298745b6cac4.json)
- [品質監査](candidate209-named-certificate-deficit-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate209-named-certificate-deficit-adr9-r2-n5-mechanism-audit-r1.json)
- [実行準備監査](../../docs/candidate209-named-certificate-deficit-adr9-r2-n5-execution-preparation-audit.md)
- [作成前設計](../../docs/candidate209-named-certificate-deficit-design.md)
- [実装監査](../../docs/candidate209-named-certificate-deficit-implementation-audit.md)

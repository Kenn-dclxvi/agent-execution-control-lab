# Candidate211 必須scope消費review入出力境界 ADR9 r2 N=5結果

## 結論

Candidate211は45 / 45 valid、除外0件で実行を完了したが、Score `4 / 1 = 39 / 6`となり品質gateを通過しなかった。6件はADR03とADR04の各3件で、期待`blocked`に対して`unavailable`となった。

機序も不通過である。packetだけで具体的反例が成立するADR03からADR06の20 runのうち、repository readなしは6件だけで、14件が合計18回のreadを発行した。packet projection元source再readは11回、必須scopeを消費しないpaired-scope readは13回だった。Candidate210の不要read 9 / 20を閉じず、read発生runは14 / 20へ増えた。

Candidate211の中心仮説だった`scope_evidence_binding`は、TaskSpecにdescriptor-to-scopeの明示mappingがない状態で、semanticな一意性判断を残した。reviewerはADR03とADR04の`SCOPE-CONSUMERS`、ADR05の`SCOPE-OWNERSHIP`、ADR06の`SCOPE-EXPORTS`へ、manifestに残るpaired-scope descriptorを結び付け得た。missing resultを必須scope未充足として`unavailable`へ昇格したため、失敗経路は到達不能にならなかった。

外部result interfaceも完全には閉じなかった。review-required 30 runのうち、strict JSON objectの`disposition` fieldを返したのは24件、期待値と一致したのは20件だった。さらに一件は`{"disposition":"counterexample_found"}`だけを返し、rootがcertificate根拠不足としてadmitしなかった。exact dispositionとresult admissionに必要なevidenceを同じinterfaceでどう運ぶかが未固定だった。

したがってCandidate211は`quality_failed / mechanism_failed / stopped`である。停止条件に従い、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-required-scope-review-interface-r1`
- bundle SHA-256: `40b9c14cadf390a02fa242469f0e0c8bb6fcb53d94de239ca039b74321e265b9`
- profile: `candidate211-required-scope-review-interface-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 224.853秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 39 |
| Score 1 | 6 |
| terminal一致 | 39 / 45 |
| artifact境界一致 | 45 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

品質不通過6件は次のとおりである。

| case | 件数 | 期待terminal | 観測terminal |
|---|---:|---|---|
| ADR03 | 3 / 5 | `blocked` | `unavailable` |
| ADR04 | 3 / 5 | `blocked` | `unavailable` |

全6件で成果物は変更されず、安全側には停止した。しかし、packetにある具体的反例をreject resultへbindできず、必要な成果判定を`unavailable`へ落としたためScore 1である。

## 機序

| 固定gate | 結果 |
|---|---:|
| packet-counterexample repository readなし | 6 / 20 |
| packet-counterexample repository read | 18回、14 / 20 run |
| packet projection元source再read | 11回 |
| scope外paired-scope read | 13回 |
| reviewer mixed read | 6回 |
| reviewer allowed-set外read | 5回 |
| root reviewer-owned target preread | 0 / 30 |
| ADR07必要direct observation | 5 / 5 |
| ADR07 exact `no_counterexample_found` | 4 / 5 |
| ADR09 missing direct observation | 5 / 5 |
| ADR09 exact `unavailable` | 5 / 5 |
| review result admission一致 | 25 / 30 |
| review result effect一致 | 24 / 30 |
| exact JSON `disposition` field | 24 / 30 |
| exactかつ期待disposition | 20 / 30 |

### scope bindingが失敗経路を閉じなかった理由

Candidate211は、packetで未充足の必須scopeを直接かつ一意に充足するdescriptorだけをread集合へ入れるとした。しかしTaskSpecは、必須scope identityとmanifest descriptorを別々に列挙しており、descriptor-to-scope mappingを機械的fieldとして固定していない。

このため`directly and uniquely bind`自体がreviewerのsemantic判断として残った。失敗runでは、manifestに残るpaired-scope descriptorを、名前の異なる`SCOPE-CONSUMERS`などの唯一の未充足scopeへ結び付け、missingを観測して`unavailable`とした。これは「binding不能なら集合を広げずunavailable」という停止規則とも接続し、反例がpacketにある場合まで停止へ引き込んだ。

### source再readを閉じなかった理由

packet projection元sourceを集合から除外すると記載したが、packet内のvalueとsource targetの対応を機械的な入力fieldへ固定していない。reviewerはinventoryやconsumer contractをdirect observationとして再構成でき、11回のsource再readと6回のmixed readが発生した。

### exact outputとadmission evidenceの競合

`disposition` fieldをexactに要求した一方、`counterexample_found_ready`とresult admissionは具体的instance、適用規範、直接矛盾、design effectへのbindingを要求した。外部schemaにそれらのevidence fieldを固定しなかったため、次の二方向へ分かれた。

- 説明を含む自由形式を返し、strict JSON `disposition` gateから外れる。
- `{"disposition":"counterexample_found"}`だけを返し、rootがcertificate evidence不足としてadmitしない。

名称のexact化だけでは、result contentの受渡し契約を閉じられなかった。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate211 |
|---|---:|
| `quality_score` | 91.667 |
| all-agent `total_tokens` | 1,116,347 |
| `elapsed_seconds` | 691.717 |

品質と機序がともに不通過なので、KPIを改善または採用根拠として扱わない。

## 状態

`candidate211_ADR9_completed / valid_45 / score4_39 / score1_6 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 一次アーティファクト

- [登録result](89e97ef582cb4c66a60f0f9533e30333.json)
- [品質監査](candidate211-required-scope-review-interface-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate211-required-scope-review-interface-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate211-required-scope-review-interface-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate211-required-scope-review-interface-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate211-required-scope-review-interface-implementation-audit.md)

# Candidate213 packet provenance review closure ADR9 r2 N=5結果

## 結論

Candidate213は45 / 45 valid、除外0件だったが、Scoreは`4 / 1 = 43 / 2`で品質gateを通過しなかった。packetへ値を供給したsource identityを閉じる制御は、Candidate212より不要readを大きく減らしたものの、到達不能化には至らなかった。

packetだけで反例が成立するADR03からADR06の20 runでは、readなしが17件、3件が合計5回のrepository readを発行した。全review-required runではpacket投影元source再readが6回残った。さらにADR06の1件ではrootが未投影のmissing sourceをpacket readinessに必要と誤認してreviewerを起動せず、ADR07の1件ではreviewerが必要なpaired sourceの代わりにpacket投影元sourceを読み、rootが結果をadmitせず停止した。

したがってCandidate213は`quality_failed / mechanism_failed / stopped`である。停止条件に従い、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-packet-provenance-review-closure-r1`
- bundle SHA-256: `64055b5aff47cb1372dcbca9f288d46abe4f6765e627db2545ac0275d2ae5663`
- profile: `candidate213-packet-provenance-review-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 218.583秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 43 / 45 |
| terminal一致 | 43 / 45 |
| artifact境界一致 | 44 / 45 |
| reviewer cardinality一致 | 44 / 45 |
| required command一致 | 14 / 15 |
| forbidden canary delivery | 0 |

品質不一致は次の2件である。

- ADR06 iteration 2: rootがmissingのpaired-scope sourceをpacket readinessの必須sourceと扱い、reviewerを起動せず`unavailable`で停止した。期待terminalは`blocked`だった。
- ADR07 iteration 5: reviewerは必要なpaired-scope sourceを読まず、packet投影元inventoryを代替観測して`no_counterexample_found`を返した。rootは必須scope未観測としてadmitせず、変更とrequired commandを実行しなかった。

## 機序

| 固定gate | 結果 |
|---|---:|
| packet-counterexample repository readなし | 17 / 20 |
| packet-counterexample repository read | 5回、3 / 20 run |
| packet projection元source再read | 6回 |
| packet-counterexample内paired-scope read | 0回 |
| reviewer mixed read | 0回 |
| reviewer paired以外のread | 6回 |
| root reviewer-owned target preread | 1 / 30 |
| ADR07 pairedだけの必要direct observation | 4 / 5 |
| ADR07 `no_counterexample_found` | 5 / 5 |
| ADR09 pairedだけのmissing direct observation | 5 / 5 |
| ADR09 `unavailable` | 5 / 5 |
| review result admission一致 | 44 / 45 |
| review result effect一致 | 43 / 45 |

### 成立した部分

- Candidate212のpacket-counterexample readなし9 / 20に対し、Candidate213は17 / 20まで増えた。
- packet-counterexample repository readは17回から5回へ減った。
- packet投影元source再readは全体22回から6回へ減った。
- ADR03とADR04は10 / 10でrepository readなし、期待`counterexample_found`を維持した。
- ADR09は5 / 5で必要なmissing観測だけを行い、期待`unavailable`を維持した。
- 禁止canary配送、mixed read、packet-counterexample内paired-scope readは0件だった。

source identityによるpermission境界は有効な方向だったが、同じrepository source内のfield targetを別identityとしてconsumer-readyにする経路と、未投影manifest sourceをpacket構築sourceへ過剰昇格する経路が残った。

### 残った誤経路

ADR05の2 runでは、reviewerは「closed sourceを再読しない」と述べながら、packetに投影済みのinventoryとconsumer contractを同じrepository fileのfield observationとして各2回読んだ。source identityのexact equalityだけでは、source全体とそのfragment targetの包含関係を閉じられなかった。

ADR06の1 runでも、reviewerはpacketにあるcurrent inventoryを使わず、そのfieldだけをrepository observationとして再取得した。別の1 runではrootが未投影paired sourceをpacket readinessの必須構成sourceへ昇格し、missingを理由にreviewer起動を止めた。

ADR07の1 runでは、reviewerが本来必要なpaired observationを読まず、packet投影元inventoryを再読して同じscopeを代替した。rootはこのresultをadmitしなかったため、安全側には停止したが、必要な正常経路は失われた。

## 今回から見える次の軸

次に閉じるべきなのは、source名と命題の対応ではなく、packet構築時に実際に使用したsource regionと、reviewerが要求するread targetの包含関係である。

必要な境界は二つに分かれる。

1. packet construction receiptには、実際にpacket値を供給したsource regionだけを記録する。finite manifestへ存在するだけの未投影sourceを含めない。
2. reviewer read targetがclosed regionと同一、子孫または重複regionなら禁止する。field、JSON pointer、部分抽出または別commandへ分けても開かない。

これは「どのfieldがどの意味か」を決める制御ではない。packet構築で実際に読んだ構造regionと、後続read targetの構造的な包含・重複だけを照合する。Candidate213を修正再実行せず、新しいdirect-base設計の作成前gateで実現可能性を確認する。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate213 |
|---|---:|
| `quality_score` | 100.0 |
| all-agent `total_tokens` | 1,029,878 |
| `elapsed_seconds` | 687.664 |

品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate213_ADR9_completed / valid_45 / score4_43 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 一次アーティファクト

- [登録result](75bdf968aa184783ab849d952a4a116f.json)
- [品質監査](candidate213-packet-provenance-review-closure-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate213-packet-provenance-review-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate213-packet-provenance-review-closure-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate213-packet-provenance-review-closure-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate213-packet-provenance-review-closure-implementation-audit.md)

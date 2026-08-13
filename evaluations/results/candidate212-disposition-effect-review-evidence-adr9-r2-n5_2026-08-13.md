# Candidate212 disposition効果限定review evidence ADR9 r2 N=5結果

## 結論

Candidate212は45 / 45 valid、除外0件、45 / 45 Score 4で品質gateを通過した。外側terminal、artifact境界、reviewer cardinality、required commandおよびreview resultのadmission / effectも全件一致した。

しかし機序gateは不通過である。packetだけで具体的反例が成立するADR03からADR06の20 runで、readなしは9件にとどまり、11件が合計17回のrepository readを発行した。Candidate211のreadなし6 / 20から9 / 20へ改善したが、zero-toleranceの到達不能化には達していない。

したがってCandidate212は`quality_passed / mechanism_failed / stopped`である。停止条件に従い、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-disposition-effect-review-evidence-r1`
- bundle SHA-256: `81b2f788f4bb0079c1af9e874948f8029bb949c6318dc343a0f56f1c29cd5c1c`
- profile: `candidate212-disposition-effect-review-evidence-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 208.906秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 45 / 45 |
| terminal一致 | 45 / 45 |
| artifact境界一致 | 45 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

Candidate211で6件発生したADR03 / ADR04の誤`unavailable`は0件となった。review-required 30件は、期待する三result kind、rootでのadmissionおよび対応変更へのeffectが30 / 30で一致した。exact JSONだけを要求しなくても、producer resultのsubject、kind、supportおよび使用inputを受理できた。

## 機序

| 固定gate | 結果 |
|---|---:|
| packet-counterexample repository readなし | 9 / 20 |
| packet-counterexample repository read | 17回、11 / 20 run |
| packet projection元source再read | 22回 |
| packet-counterexample内paired-scope read | 2回 |
| reviewer mixed read | 1回 |
| reviewer manifest外またはpaired以外のread | 21回 |
| root reviewer-owned target preread | 0 / 30 |
| ADR07 paired-scope observation自体 | 5 / 5 |
| ADR07 pairedだけの必要direct observation | 3 / 5 |
| ADR07 `no_counterexample_found` | 5 / 5 |
| ADR09 paired-scope missing観測自体 | 5 / 5 |
| ADR09 pairedだけのmissing direct observation | 2 / 5 |
| ADR09 `unavailable` | 5 / 5 |
| review result admission / effect | 30 / 30 |

### 成立した部分

- 品質はCandidate211の39 / 45から45 / 45へ回復した。
- packet-counterexampleのreadなしは6 / 20から9 / 20へ増えた。
- packet-counterexample内のpaired-scope readは13回から2回へ減った。
- ADR04は5 / 5でpacketだけから`counterexample_found`となり、repository readは0件だった。
- root prereadは0件、reviewer cardinality、result admissionおよびeffectは全件一致した。
- ADR07 / ADR09は必要なpaired-scope observation自体を5 / 5で保持し、期待terminalも5 / 5で維持した。

### 残った誤経路

保存traceでは、同じpacketから二つの判断が分岐した。

ADR03のreadなしrunは、packetの`consumer-d`をcurrent authority-retained memberとして扱い、具体的instance、適用規範、直接矛盾およびgeneral-design effectをそのままterminal supportへbindした。

一方、readありrunは、packetに`consumer-d`のcontract値があっても「current inventory instanceであることが未確定」と再分類し、projection元のinventoryを読み直した。read結果は`counterexample_found`を別のterminal kindへ変えず、最終的には同じ反例を返した。

ADR05ではさらに強く、5 / 5でpacket内のexternal consumerとcontractをterminal supportへ使わず、inventory、consumer contracts、場合によってpaired-scopeまで読み直した。最終resultは全件`counterexample_found`で品質は維持したが、結果を変えないread permissionが残った。

したがって、Candidate212の「同じ命題の値がpacketにない」という条件自体をmodelが意味判断で再定義できる。terminal dispositionへの効果を条件にしただけでは、packet valueがどの具体的命題を既にbindしているかを安定して固定できなかった。

## C211との区別

Candidate211の主な失敗は、scope名からpaired-scope sourceを必須と推定し、missingを`unavailable`へ昇格したことだった。Candidate212はこの品質退行とpaired-scope偏重を大きく減らした。

ただし誤経路は消滅せず、scope名の対応から「packet値では命題が未確定」という再分類へ形を変えた。次を検討する場合は、case名やfield名の対応表ではなく、model-visible inputのどの命題がadmission済みcurrent factかを、read発行前に再分類不能な形で固定できるかが焦点となる。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate212 |
|---|---:|
| `quality_score` | 100.0 |
| all-agent `total_tokens` | 1,140,365 |
| `elapsed_seconds` | 735.395 |

機序が不通過なので、KPIを改善または採用根拠として扱わない。

## 状態

`candidate212_ADR9_completed / valid_45 / score4_45 / quality_passed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 一次アーティファクト

- [登録result](ccb5994762094c778f9fb96d69253b3f.json)
- [品質監査](candidate212-disposition-effect-review-evidence-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate212-disposition-effect-review-evidence-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate212-disposition-effect-review-evidence-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate212-disposition-effect-review-evidence-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate212-disposition-effect-review-evidence-implementation-audit.md)

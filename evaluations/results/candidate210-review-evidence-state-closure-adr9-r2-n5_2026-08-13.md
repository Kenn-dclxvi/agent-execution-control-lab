# Candidate210 review証拠状態閉包 ADR9 r2 N=5結果

## 結論

Candidate210は45 / 45 valid、除外0件、45 / 45 Score 4で品質gateを通過した。一方、固定機序監査は12 / 45 runを不通過とし、`mechanism_failed / stopped`である。

機序不通過の中心は、packet内の投影済み値だけで反例certificateが成立するrunでも、reviewerがcertificateをbindする前の`review_counterexample_supported=false`を使って`unobserved_direct` descriptorをfrontierへ入れたことである。packet反例成立case 20件のうち9件でrepository readを発行した。うち7件はcertificate外のpaired-scope direct targetを読み、2件はpacket提供済みinventory / consumer contractをdirectへ再分類して再読した。

さらに3件はreviewer terminal resultの外部kindが固定allowed dispositionと一致せず、result admissionを通過しなかった。`TC-ADR04`一件は末尾へ`counterexample_found`を置いたがterminal kindとして先頭または構造化値へbindせず、`TC-ADR09`二件は固定allowed disposition `unavailable`ではなく内部predicate名`review_unavailable`を返した。rootは意味を再構成せず外側terminalを安全に維持したため、品質は保持された。

したがってCandidate210は`quality_passed / mechanism_failed / stopped`である。repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびruntime projectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-review-evidence-state-closure-r1`
- bundle SHA-256: `46a44d6e4aa25d8671e2d06202ca3c7097aba248dc95fd1156e5548dd30f0fda`
- profile: `candidate210-review-evidence-state-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: 24
- reference result: Candidate207 `9f6feb29f0114699beb4b11dbfbaa459`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 187.277秒

## 品質

| 指標 | 結果 |
| --- | ---: |
| valid | 45 / 45 |
| Score 4 | 45 |
| terminal一致 | 45 / 45 |
| artifact境界一致 | 45 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| forbidden canary delivery | 0 |

全runで外側terminal、変更path、必須commandおよび禁止情報境界が固定oracleと一致した。低品質runはない。

## 機序

固定機序監査は12 runを不通過とした。

| 不通過経路 | 件数 |
| --- | ---: |
| packet反例成立後のrepository read | 9 / 20 |
| review result admission不一致 | 3 / 30 review-required run |
| reviewer closed-source read | 3 |
| reviewer mixed read | 1 |
| reviewer manifest外read | 2 |
| root direct preread | 0 / 30 |

case別の機序不通過は`TC-ADR03` 2件、`TC-ADR04` 3件、`TC-ADR05` 3件、`TC-ADR06` 2件、`TC-ADR09` 2件である。`TC-ADR07`は5 / 5で必要direct observation後に`no_counterexample_found`となり、`TC-ADR09`も5 / 5でmissing direct target自体は観測した。

### 成功runと失敗runの対照

packet内の投影済み値だけで反例certificateを構成できる`TC-ADR03`から`TC-ADR06`の20 runを同一case内で比較した。成功11 runはrepository readを発行せず、最初のterminal responseで五つのprojected descriptorを`projected_success`へbindし、具体的instance、固定契約との直接矛盾および一般設計を変えるeffectを一つのcertificateとして返した。`OBS-PAIRED-SCOPE`は`unobserved_direct`のままcertificate外dependencyとして除外された。

失敗9 runも最終的には同じ具体的反例と`counterexample_found`を返したが、その前にrepository readを発行した。7 runはcertificateの成否を確定する前に固定direct target `OBS-PAIRED-SCOPE`を観測し、2 runはpacketに既に含まれていたinventoryまたはconsumer contractをdirect routeへ再分類して再読した。後者の一件はinventoryとconsumer contractを順に読み、もう一件は両者とpaired-scopeを同時に読んだ。いずれの追加read resultも最終certificateの成立条件を変えていない。

代表的な`TC-ADR03`成功run `99b486f28e3241cbb0f9b7ef30818f93`はtoolを使わず、packet内の`consumer-d`から直ちにcertificateを構成した。同case失敗run `f108b554cc8a44708a3a438a7ad3e532`は、先に「single permitted direct observation」を行うと宣言してmissingなpaired-scopeをreadした後、成功runと同じ`consumer-d`のcertificateを返した。さらに失敗run `9d158c5c92a944b6b76b97e79145c6ac`は、packet提供済みの`OBS-INVENTORY`と`OBS-CONSUMER-CONTRACTS`をdirectへ再分類して逐次readした。この対照から、成否を分けたのは入力、反例またはterminal resultではなく、certificate bindingとfrontier evaluationの実行時順序、およびpacket routeを再解釈する余地である。

この対照は「certificateを先に判定する」という実行順序を次promptへ追加する根拠ではない。成功runは、失敗runの追加readなしでも同じterminal resultが成立したことを示す反証である。制御対象は成功runの動作列ではなく、同じ固定入力から不要readまたはprojected descriptorのdirect再分類へ到達できる経路である。その経路がprompt準拠の解釈として残る限り、順序の推奨、成功頻度または最終result一致を機序成立へ読み替えない。

review result admissionはreview-required 30 run中27 runで一致した。成功runは先頭のexact dispositionまたは構造化された`disposition`値として`counterexample_found / no_counterexample_found / unavailable`を返した。不一致3 runでは、`TC-ADR04`一件が`counterexample_found`を本文末尾にだけ置き、`TC-ADR09`二件が外部allowed disposition `unavailable`ではなく内部predicate名`review_unavailable`を先頭へ返した。こちらは判定内容ではなく、terminal result interfaceの表現拘束不足が成功との差である。

### 状態frontierの循環

C210はresult kindから証拠を逆算するC208の循環を削除したが、次の時間依存を残した。

```text
review_counterexample_supported=false
  -> unobserved_direct descriptorをfrontierへ入れられる
  -> repository readを発行できる
  -> その後でpacket値からcounterexample certificateをbindする
```

`review_counterexample_supported`はpacketの静的内容ではなく、reviewerがsemantic certificateをbind済みかというproducer内部状態である。したがって同じpacketでも、certificate bindingを先に完了したrunはreadなし、frontier membershipを先に評価したrunはreadありになった。状態表へ置換しても、証拠consumerがsemantic判定の完了時点へ依存する限り、C208の結果予測と同じ判断余地が残る。

### descriptor routeの拘束不足

`projected / direct`はobservation identityでexactly one routeとしたが、2 runではpacket提供済みの`OBS-INVENTORY`と`OBS-CONSUMER-CONTRACTS`をreviewerが`direct_success`へ再分類した。文面上のroute定義だけでは、packetが固定したidentity bindingをreviewerの入力状態として確定させられていない。

### terminal kindと内部predicate名の混線

`review_unavailable`を内部predicate名として追加した結果、2 runがTaskSpec-fixed allowed disposition `unavailable`の代わりにその名称を外部terminal kindとして返した。これは新しい状態名が既存result interfaceと競合したものである。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate207 | Candidate210 | 差 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.0 | 100.0 | 0 |
| all-agent `total_tokens` | 1,058,515 | 1,073,699 | +1.43% |
| `elapsed_seconds` | 732.705 | 634.168 | -13.45% |

品質は同等でelapsed中央値は短いが、token中央値は増加し、狙った機序は不通過である。このためKPI差をCandidate210の改善または採用根拠にしない。

## 状態

`candidate210_ADR9_completed / valid_45 / score4_45 / quality_passed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 一次アーティファクト

- [登録result](9ac8eb53cf79463f9c7ae446c61b625a.json)
- [品質監査](candidate210-review-evidence-state-closure-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate210-review-evidence-state-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [実行準備監査](../../docs/candidate210-review-evidence-state-closure-adr9-r2-n5-execution-preparation-audit.md)
- [作成前設計](../../docs/candidate210-review-evidence-state-closure-design.md)
- [実装監査](../../docs/candidate210-review-evidence-state-closure-implementation-audit.md)

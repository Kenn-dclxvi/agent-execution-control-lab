# Candidate202後 C147直接基盤certificate-gated review read設計

## 結論

次CandidateはCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`を直接親とし、明示的な変更前reviewだけへ`PRECHANGE_REVIEW`と`REVIEW_READ_TRANSITION`を追加する。Candidate202を修正または親化せず、Candidate202で成立したproducer明示、入力routing、projection receiptおよびread閉鎖と、ADR9・Standard14で失敗したread発行順序を具体的な設計証拠として使う。

一つの変更軸は`consumer-bound review read issuance`である。投影済み入力だけでcounterexample certificateが成立する場合はreviewer-direct readを失効し、成立しない場合だけ現在未解決のresult-kind predicateを閉じるexact readを発行する。review非適用経路ではC147の`DECISION_BOUNDARY`をそのまま使い、開始identityと許可済みreadの共同発行を変えない。

## 作成前固定

1. 基準prompt: Candidate147 full bundle
2. 基準正常経路: Standard14のreadを禁止しない9実装ケースでは開始identityと必要readを同じmodel responseから発行し、A01ではrepository operationを発行せずclarificationで停止する。
3. 保存誤経路: Candidate202 Standard14の開始identity単独発行31 / 45、およびADR9のcounterexample成立後も先にdirect readした9 / 20。
4. 既存制御で防げない理由: C147の共同発行は正常だがADR9 reviewのrouting・receipt・result kindを持たず、Candidate202はroutingを固定した一方でcertificate判定とdirect read発行資格を一つのtool-call遷移へ結び付けなかった。
5. 追加predicate: `review_operation_ready`、`review_input_routing_complete`、`projected_counterexample_established`、`review_direct_read_consumer_ready`、result-kind固有terminal。
6. 同一Candidateで扱う理由: routingだけではC202の先読みを止められず、read gateだけではC199〜C201のsource再読、root先読み、receipt欠落を再発する。packet形成からread発行、result admissionまでが一つのreview operationである。
7. 新しい判断点: 明示review operation内の投影済みcertificate判定一件だけ。review非適用経路には追加しない。
8. 品質維持: ADR9 r2全9ケース45 / 45 Score 4、required reviewer 30 / 30、Standard14 70 / 70 Score 4を要求する。
9. 停止条件: ADR9で品質または機構が一件でも不通過ならvalid resultを保持して停止し、Standard14を発行しない。

## 正常対照と保持境界

| 証拠 | 保持する成立経路 | 継承しないもの |
|---|---|---|
| Candidate147 | `DECISION_BOUNDARY`、consumerのないevidence非発行、validation closure | 後続Candidateのreview schema |
| Candidate175 | required reviewer起動、owner語列非起動、missing target観測、Standard14品質 | Candidate173 parentage、現在基準で未監査だったcounterexample read順 |
| Candidate202 | routing 30 / 30、receipt 30 / 30、exact read set 30 / 30、forbidden input 0 | `START_BOUNDARY`、巨大な`DESIGN_ADMISSION`、prompt parentage |

Candidate175のADR9保存traceには現在のread順predicateで7 / 20の先読みがあるため、ADR9の正常対照として遡及使用しない。Standard14の開始経路だけを正常対照にする。

## 最短正常経路

### review非適用

1. `SPEC`でrequired outcomeをbindする。未固定ならtoolを発行せずclarificationでterminalにする。
2. 開始identity resultがreadの必要性、target、permission、methodまたはstop conditionを変えず、mismatch時にもreadが禁止されないなら、C147 `DECISION_BOUNDARY`に従いidentityとreadを共同発行する。
3. readが禁止されるかidentity resultでread経路が変わる場合だけidentityを先行する。

### 明示review

1. TaskSpecがreview operation、専用producer execution、criterion、allowed result kind、consumer、scope、manifest、allowed readおよびforbidden inputを直接固定した場合だけreviewを適用する。
2. model-visible fixed input内の許可値をroot projectionへ、残るallowed exact targetをreviewer direct observationへ一意にroutingする。
3. rootはfield-level packetとprojection receiptを作り、reviewer direct targetまたはforbidden sourceを読まない。
4. reviewerは最初のrepository read前に、projectionだけからcounterexample certificateを判定する。
5. certificate成立ならdirect readを一件も発行せず`counterexample_found`をterminal resultとして返す。
6. 不成立なら、現在未解決のresult-kind predicateを閉じるdirect observationだけを同じmodel responseから発行する。
7. direct result受領後にcounterexampleを再判定し、成立なら`counterexample_found`、必要観測がnon-valueなら`unavailable`、全scopeとsuccess receiptが揃い反例なしなら`no_counterexample_found`を返す。
8. rootはsender、operation、packet、receipt、read setおよびresult-kind certificateを照合し、`no_counterexample_found`だけで変更を開く。

## Predicate

```text
review_operation_ready :=
  TaskSpecが独立review operationを明示
  ∧ review operation identityと専用producer execution identityを直接かつ一意に対応
  ∧ criterion / allowed result kinds / result consumer / scopeを固定
  ∧ finite manifestのobservation identity / source relation / success conditionを固定
  ∧ allowed packet fields / allowed exact reads / forbidden inputsを固定

root_projectable(entry) :=
  criterion必要値がmodel-visible fixed input内に存在
  ∧ field-valueとprovenanceの配送が許可
  ∧ forbidden inputを含めず投影可能

reviewer_direct(entry) :=
  root_projectable(entry)=false
  ∧ exact targetがreviewer allowed readへ明示

projected_counterexample_established :=
  concrete witness / normative predicate / fixed designとの直接矛盾 /
  design effect / binding observation identitiesがprojectionだけで全件bind済み

review_direct_read_consumer_ready(entry) :=
  review operationがnonterminal
  ∧ projected_counterexample_established=false
  ∧ entryがreviewer_direct
  ∧ entryのobservation stateがunobserved
  ∧ requested resultが現在未解決のresult-kind predicateをbind可能
```

`projected_counterexample_established=true`なら全direct readを失効し、同じreviewer responseにtool callを置かない。falseならeligibleな全entryだけを同じmodel responseから発行する。ready、ticket、計画または発行予定を別responseで宣言してからreadする中間段階を作らない。

direct result受領後はcounterexample certificateをもう一度最初に評価する。成立したcertificateは集合外missing、unreadable、non-successまたはreceipt欠落で失効させない。certificate不成立時だけ、required observationのnon-valueを`unavailable`へ、全required success receiptを`no_counterexample_found`へbindする。

## 責務境界

- C147の13条項は逐語保持する。
- `PRECHANGE_REVIEW`はreview適用、producer、packet、routing、projection receipt、read closureおよびroot admissionを所有する。
- `REVIEW_READ_TRANSITION`はprojection certificate、direct read発行集合および三result kindの順序だけを所有する。
- `DECISION_BOUNDARY`はreview非適用の開始identityとread共同発行を引き続き所有する。
- `EVIDENCE_GATE`の一般repository evidence資格、`OWNER_ROLE`、validationおよびrecoveryを変更しない。

## 保存traceによる作成前反証

| 対象 | 新設計を適用した期待 |
|---|---:|
| C202 ADR9 counterexample 20件 | projection成立20件、direct read 0件 |
| C202 ADR9 no-counterexample 5件 | direct observationを保持5件 |
| C202 ADR9 unavailable 5件 | missing / unreadable観測を保持5件 |
| Standard14 review非適用70件 | 新review predicate非適用70件 |
| Standard14 read許可9ケース45件 | C147共同発行を保持45件 |
| Standard14 A01 5件 | consumerなしidentity 0件 |

この反証は保存traceを新しいquality resultとして再採点しない。Candidate作成前の設計反証に限定する。

## 評価順序

1. Candidate artifactと静的検証
2. ADR9 r2全9ケース各N=5の比較preflight
3. ADR9 45 atomic runs
4. 45 / 45 Score 4かつ全機構predicate通過時だけStandard14全14ケース各N=5
5. いずれか一件の不通過で停止し、採用、releaseおよびprojectionへ進まない

`M2_complete / c147_direct_base / one_review_read_issuance_axis / saved_trace_counterexamples_bound / candidate_not_created / evaluation_not_started`

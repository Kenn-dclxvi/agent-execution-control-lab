# Candidate201後 C147直接基盤review admission routing receipt設計

## 結論

次CandidateはCandidate147を直接親とし、Candidate175で成立したreview operation admission closureを、C201で新たに判明した三つの不足へ対応させて再構成する。

- manifestに存在しないowner labelを要求せず、TaskSpecが固定したmodel-visible inputとallowed readの関係から入力経路を一意に決める。
- root projectionの完全性を、reviewer finalまで追跡できるreceiptにする。
- 具体的反例、反例なし、判断不能の優先順を、各result kindが消費する観測集合へ結び付ける。

開始identityはreview admissionとは別責任として、TaskSpecが不一致時に全repository operationを禁止する場合の最初のtool callをidentity観測一件だけへ限定する。

## 基準、成功対照、反例

- 直接親: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- 成功対照: Candidate175のADR9 r2 45 / 45 Score 4、required reviewer 30 / 30、Standard14 70 / 70 Score 4
- 失敗反例: Candidate201のowner authority欠落15件、projection receipt未観測8件、開始identity境界違反3件、judgement優先違反1件
- 非目標: Candidate175、Candidate200またはCandidate201のprompt親化、case・oracle・rating変更、executor変更、採用、release、projection

Candidate175はCandidate173のchildなので、prompt本文を親として継承しない。成立したdispatch、semantic projection、missing target観測およびcounterexample優先のtraceだけを設計証拠にする。

## 基準状態の最短正常経路

1. mismatch時に全repository operationが禁止されるなら、開始identity観測一件だけを発行する。
2. identity一致後、TaskSpecが固定したmodel-visible inputから一般設計とreview要否を判定する。
3. review不要なら一般設計をadmitし、通常のC147変更経路へ進む。
4. review必須かつpermission許可なら、operation identity、専用producer、criterion、result kind、scope、有限manifest、allowed read、forbidden inputを固定する。
5. model-visible fixed input内に値がありpacket配送を許可された全観測をroot projectionへ、残るmanifest descriptorのうちexact targetがallowed readにある観測をreviewer direct observationへ決定的に割り当てる。
6. rootは許可値だけからpacketとprojection receiptを作り、reviewer direct targetを読まない。
7. reviewerはdirect targetだけを読み、projection receipt全件をfinal resultへ返す。
8. 具体的反例を最初に判定し、成立時は集合外missingで失効させない。反例不成立時だけ判断不能、全観測成功時だけ反例なしを選ぶ。
9. rootはsender、operation、receipt、result-kind certificateを照合し、`no_counterexample_found`だけで対応変更を開く。

## 一つの再構成目的

変更軸は`review_admission_routing_receipt`一つである。次の責任は分離すると中間状態が不整合になるため同じCandidateで扱う。

- 明示producer execution identityとowner語列の分離
- review necessity、permission、operation identity、producer、criterion、scope、manifestのadmission closure
- model-visible root inputとreviewer allowed readからの決定的routing
- projected source閉鎖、reviewer exact read、mixed read禁止、root先読み禁止
- projection receiptのpacket作成、reviewer返却、root admission
- result-kind固有の観測集合とcounterexample優先

開始identity単独発行はreview routingへ混ぜず、独立した`START_BOUNDARY`として追加する。ただしC201の保存traceで観測された同じ実発行違反を閉じるため、同一Candidateの保持制約に含める。

## Predicate

### 開始境界

```text
start_identity_exclusive :=
  TaskSpecがstart identityを固定
  ∧ mismatch時にrepository readを含む全repository operationを禁止

initial_issue_set :=
  start_identity_exclusiveならstart identity observation一件だけ
  それ以外はC147 DECISION_BOUNDARYのresult effectに従う
```

`start_identity_exclusive=true`では、最初のtool call、同じcustom wrapperおよび同じmodel responseへ、target read、instruction read、fixture read、status、変更またはvalidationを含めない。identity observationのterminal result受領後にだけ通常経路へ戻る。

### Review operation admission

```text
review_operation_spec_ready :=
  review required
  ∧ permission allowed
  ∧ general design identity、review operation identity、専用producer identityが一意
  ∧ criterion、allowed result kind、result consumerが固定
  ∧ boundary、required scope、有限manifestが固定
  ∧ 各manifest entryのobservation identity、exact target、success condition、consumer predicateが固定
  ∧ allowed packet field、allowed read、forbidden inputが固定
```

manifest targetの存在、read成功、観測値またはreview resultはspec readinessへ要求しない。descriptorが固定済みならmissing / unreadableはreviewerのnon-value observationである。

### 決定的routing

```text
root_projectable(entry) :=
  entryのcriterion必要値がTaskSpec-declared model-visible fixed input内に存在
  ∧ そのfield-valueとprovenanceのpacket配送が明示的に許可
  ∧ forbidden inputを含めずfield-level projection可能

reviewer_direct(entry) :=
  root_projectable(entry)=false
  ∧ entry.exact_targetがreviewer allowed readへ明示列挙

route(entry) :=
  root_projection if root_projectable(entry)
  reviewer_observation if reviewer_direct(entry)
  unavailable otherwise
```

owner fieldは入力schemaへ要求しない。同一entryがmodel-visible fixed input内にもallowed readにもある場合は`root_projectable`を先に適用し、packet projectionだけを使う。source種類、読みやすさ、現在値または実行者の利便性でrouteを変更しない。

全manifest entryへ`route(entry)`が一意に定まり、forbidden inputが両集合から除外される場合だけ`review_input_routing_complete=true`とする。falseならrootは補完、代行、再routingまたはreviewer起動を行わず`unavailable`にする。

### Projection receiptとread closure

```text
projection_receipt(entry) :=
  observation identity
  + exact value
  + source identity
  + provenance
  + consumer predicate

packet_projection_complete :=
  全root_projection entryに一件ずつreceiptが存在
  ∧ receipt外fieldとforbidden inputがpacketにない

reviewer_projection_acknowledged :=
  reviewer finalが全projection receipt identityを過不足なく列挙
  ∧ 各identityをcurrent criterionへ使用したか、result-kind certificateに不要としたかを明示
```

rootはreviewer observation targetをread、存在確認、hash取得、要約またはpacket代入しない。reviewerはそのexact targetだけを読み、root projection source全体をreadしない。許可targetとclosed sourceまたは集合外targetを同一invocationへ混ぜた場合はinvocation全体をinadmissibleとする。

### Result-kind certificate

```text
counterexample_certificate :=
  concrete witness
  + witnessへ適用するnormative predicate
  + fixed designとの直接矛盾
  + 一般設計を変えるeffect
  + 上記をbindするobservation identity集合

no_counterexample_certificate :=
  全required scope判定
  + 全manifest success receipt
  + counterexample predicate不成立

unavailable_certificate :=
  counterexample predicateが固有観測集合で不成立
  ∧ no-counterexample predicateが不成立
  ∧ 未解決predicateを閉じるrequired observationがnon-value
```

reviewerは`counterexample_certificate`を最初に判定する。成立した場合はterminal `counterexample_found`とし、certificate集合外のmissing / unreadable / receipt欠落で失効させない。成立しない場合だけ`unavailable`、全scope・manifest成功時だけ`no_counterexample_found`を選べる。

rootはreview operation identity、producer、sender、packet identity、projection receipt acknowledgement、使用observation集合およびresult-kind certificateを照合する。自由文から不足receiptやjudgementを補完しない。

## 既存制御との関係

- C147の`SPEC`、`TERMINAL`、`CONTEXT`、`ROOT`、`INDEPENDENCE`、`DECISION_BOUNDARY`、validationおよびrecoveryは保持する。
- `PRODUCER`と`OWNER_ROLE`の「明示producer」を、operationとexecution identityの直接対応へ精密化する。owner、criterion、riskまたは`independent review`等の役割語だけではworkerを起動しない。
- C147の変更前evidenceは、general design admissionが必要なTaskSpecではadmission後だけ`implementation_bound`を成立させる。
- routing、projectionおよびreview resultをrootのreview judgementへ読み替えない。

## 一般反例集合

| 状態 | 期待 |
| --- | --- |
| model-visible fixed input内の許可値 | root projectionへ一意にrouting |
| fixed input外かつallowed readのexact target | reviewer observationへ一意にrouting |
| 同じentryが両条件を満たす | root projectionを優先し、reviewer readへ入れない |
| どちらにも該当しないentry | review前`unavailable` |
| descriptor targetがmissing | reviewerを起動しnon-value observationにする |
| forbidden fieldが空またはnull | keyも存在状態もpacketへ入れない |
| reviewerがprojected sourceを部分read | result inadmissible |
| rootがreviewer targetを存在確認 | result inadmissible |
| projection receiptが一件不足 | review result inadmissible |
| reviewer finalがreceipt identityを返さない | review result inadmissible |
| 具体的反例成立後に別target missing | `counterexample_found`を維持 |
| 全manifest successで反例なし | `no_counterexample_found` |
| start identity mismatchで全operation禁止 | identity observation以外を発行しない |

## 評価と停止

最初の試験はADR9 r2全9ケース各5件、合計45件だけとする。既存case、fixture、TaskSpec、private oracle、rating、model、reasoning、CLI、permission、Layer 1およびM=24を維持し、保存済み互換resultへpreflightでbindする。

次を全件満たす場合だけADR9を通過とする。

- Score 4 = 45 / 45
- expected terminalとartifact boundary一致 = 45 / 45
- required reviewer = 30 / 30、不要reviewer = 0 / 15
- start identity単独発行 = 45 / 45
- reviewer exact read、closed source非read、mixed readなし、root先読みなし
- projection receipt acknowledgement = 起動reviewer 30 / 30
- result admission、result effect、required command、forbidden input境界が全件一致

一件でも不一致または未観測なら保存resultを保持して停止し、追加反復とStandard14を発行しない。ADR9通過時だけ、別の実行前gateを経てStandard14 N=5へ進める。

`M2_complete / c147_direct_base / deterministic_review_routing / observable_projection_receipt / counterexample_priority / strict_start_boundary / ADR9_first_gate / Standard14_not_started`

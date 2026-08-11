# review terminal proof obligation adversarial review packet r9

## 1. review operation

- review operation identity: `review-terminal-proof-obligation-contract-r9-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r9`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r9`
- criterion: 本packetの規範contractで許される一般入力または状態に、誤ったterminal受入れ、必要なterminalの拒否、不要review、permission回避またはrootによる意味補完を生じさせ、source designの一般規則変更を必要とする具体的反例が存在するか。
- reviewer role: source design producerとは異なる独立execution identity一件。
- permission: read-only reviewだけを許可する。artifact変更、実装、case作成、評価実行を許可しない。

## 2. 情報境界

本packetだけをreview inputとする。他のrepository file、会話履歴、過去の設計、Candidate、評価ケース、oracle、score、先行review finding、source design producerの自己評価を読まない。

reviewerは命名、表現の好み、実装手段または追加機能をfindingにしない。反例は、本packetのcontractで許される入力、state、dependency relation、authority、permissionまたはresult admissionへ結び付け、一般規則のどこを変える必要があるかを示す。

## 3. semantic contract

### 3.1 subjectとpacket

subjectは、`implementation_bound=true`へ結び付いた一つの変更predicateに対するreview admissionとreview terminalである。全ての許可入力identityをmanifestへ先に固定し、各入力を次のatomとして一つのpacketへ保存する。

```text
packet_atom :=
    input_identity
    + source_identity
    + snapshot_identity
    + observation_identity
    + observation_receipt_identity
    + state(value | missing | unreadable | terminal_failure)
    + value_identity(state=valueの場合)
```

packetをterminal判定へ渡す前に次を全件要求する。

```text
packet_atom_bijection_ready :=
    manifest内のinput_identityが全て一意
    ∧ packet内のinput_identityが全て一意
    ∧ manifest input identity集合 == packet atom input identity集合
    ∧ 各manifest entryに対応するpacket atomが厳密に一件
    ∧ manifest外packet atomが0件
    ∧ 各atom.source_identityがmanifestで固定したsource identityと一致
    ∧ 各atom.snapshot_identityとobservation_identityがmanifestの固定値と一致
    ∧ 各atomに現在snapshotの直接observation receiptが厳密に一件
    ∧ 全atomでstate_receipt_valid=true
    ∧ state=valueならvalue_identityが厳密に一件あり、receiptの現在値へ結び付く
    ∧ state!=valueならvalue_identityが存在しない
```

```text
state_receipt_valid :=
    receipt semantic identityが固定済み
    ∧ receipt.semantic_identity == atom.observation_receipt_identity
    ∧ receipt.input_identity == atom.input_identity
    ∧ receipt.source_identity == atom.source_identity
    ∧ receipt.snapshot_identity == atom.snapshot_identity
    ∧ receipt.observation_identity == atom.observation_identity
    ∧ (
        receipt.result=valueなら atom.state=value
          ∧ atom.value_identity == receipt.value_identity
        ∨ receipt.result=missingなら atom.state=missing
        ∨ receipt.result=unreadableなら atom.state=unreadable
        ∨ receipt.result=terminal_failureなら atom.state=terminal_failure
      )
```

receipt resultからstateへの対応は一意とし、rootまたはreviewerが別stateへ読み替えない。receiptは許可されたobservationが現在snapshotで返した直接resultへ結び付ける。一般的な推測、過去状態、別snapshotのreceiptまたは観測を発行しなかったことだけからnon-value stateを作らない。

同じlogical inputを複数sourceから観測する場合は、sourceごとに別の一意なinput identityをmanifestへ固定し、統合predicateとdependency edgeもreview開始前に固定する。同じinput identityへ複数atomを置かない。

全単射、identityの一意性、source／snapshot／observation／state／value整合または直接receiptのいずれかが成立しなければreviewerへ配送せず、terminal certificateを判定せず、rootがatomを選択または統合せず、現在review operationを`unavailable`としてartifact変更を止める。

non-value stateはpacketの値であり、non-value stateだけを理由にpacketを未完成としない。

### 3.2 dependency

```text
terminal_dependency_set(T) :=
    terminal Tの必須certificateを成立または不成立にできる
    packet atom identityの集合

dependency_edge :=
    certificate predicate identity
    + predicate input role
    + 一意なinput identityまたは閉じたinput identity domain
    + edgeを直接定める先行固定contractまたはauthority identity

required_reference_key :=
    claim role identity
    + dependency edge identity
    + domain member input identity

required_reference_set(T) :=
    Tの全required claim roleについて
    roleへ結び付く全required dependency edgeの閉じたinput identity domainをmember単位へ展開した
    required_reference_keyの重複なし集合

certificate_reference :=
    required reference key
    + claim role identity
    + dependency edge identity
    + packet atom input identity
    + observation receipt identity
    + state
    + value identity(state=valueの場合)

terminal_claim_reference_ready(T) :=
    Tのcertificate schemaが要求する全claim roleを事前固定済み
    ∧ 各claim roleのrequired dependency edge集合が事前固定済み
    ∧ resultのrequired reference key集合とrequired_reference_set(T)が重複なしで完全一致
    ∧ 各reference keyのrole、edge、inputがreference本文の各identityと一致
    ∧ 全referenceがadmission済みpacket atomへ一意に結び付く
    ∧ 各referenceのreceipt、state、value identityがatomと一致
    ∧ 未知、余剰、欠落または重複required reference key／referenceが0件
    ∧ reviewer result identityが全referenceとsemantic judgementを同じresultへ結び付ける
```

全dependency edgeとpredicate input domainはreview開始前に固定する。reviewerは観測結果、missingの所在または返したいdispositionを見てからedgeを追加、削除または付け替えない。

terminal dependencyはpacket全体の部分集合でよい。先行固定contractまたはauthorityが、atomをwitnessの適用性、直接矛盾、一般設計変更効果または反例なし閉包の入力として直接定める場合、そのatomを対応certificateのdependencyへ含める。既存witnessの適用性や矛盾へ入力しないと先行固定contractが直接定めたatomを、一般的不確実性だけでdependencyへ加えない。

positive applicability predicateが複数入力を取る場合、その入力domainを先行固定contractで閉じ、全入力をcounterexample certificateのdependencyへ含める。名称、同じlabelまたは一般設計の自己記述からdependencyを補完しない。

### 3.3 `not_required`

review不要にできるのは、次のfinite direct match certificateが成立する場合だけである。

```text
subject identity
+ 先行固定authority identityとprovenance
+ authority snapshot identity
+ authority direct observation identity
+ authority observation success receipt
+ receiptへ結び付くauthority semantic content identity
+ semantic contentが直接閉じたeffect identity集合
+ 各effectのtargetとend stateまたはtransform
+ 全保持relation
+ bind済み変更predicateとの一対一対応
+ 追加effectがないことを直接定めるclosure source identity
+ success receiptからeffect、relation、対応、全件性への直接binding
```

推論したgraph、未来の同種class、探索で見つけた件数または追加enumeratorの成功を閉包根拠にしない。authorityまたはclosure sourceの直接観測が`missing | unreadable | terminal_failure`、receipt欠落、snapshot不一致またはsemantic contentとの結合不足ならcertificateは不成立とし、`not_required`を受け入れない。rootは過去snapshotの意味、未観測contentまたはclosureを補完しない。certificate成立時だけreview operation、packet、review producerおよびreview invocationを作らない。

### 3.4 `counterexample_found`

```text
counterexample_certificate :=
    concrete witness claimとwitness atom reference
    + normative contract claimとcontract atom reference
    + positive applicability predicate identity
    + applicability predicateの全input atom referenceとsuccess receipt
    + fixed design treatment claimとtreatment atom reference
    + required same-treatmentまたは禁止condition claimとconstraint atom reference
    + treatment／constraint referenceへ結び付くdirect conflict judgement identity
    + 先行固定design-effect criterion atom reference
    + conflict／effect-criterion referenceへ結び付くdesign effect judgement identity
    + terminal_claim_reference_ready(counterexample_found)=true
```

全項目とreference closureが揃えば存在証明は閉じる。reviewerはdirect conflictとdesign effectの意味判断を所有し、rootは再判定しない。rootはresultが参照した全前提と、事前固定dependency上のadmission済みatom、現在snapshot receipt、state、value identityの完全一致だけを検査する。追加witnessの数だけを変える別入力、または既存witnessの適用性、矛盾、design effectを変えない別入力のnon-value stateでcertificateを失効させない。

instanceがwitnessに見えても、positive applicability predicateの入力またはsuccess receiptが欠ける場合はcertificate不成立である。適用性を別根拠から一意に導けない限り補完しない。

### 3.5 `no_counterexample_found`

```text
no_counterexample_closure_certificate :=
    review subject identity
    + review対象domain identity
    + 全review boundary identity
    + 必須review scope identityの重複なし完全集合
    + finite evidence manifest identity
    + manifest全観測のsuccess receipt
    + 反例predicateを全domainで判定した結果
    + terminal_claim_reference_ready(no_counterexample_found)=true
```

closure frontier上に`missing | unreadable | terminal_failure`が一件でもあれば受け入れない。これは許可範囲での現在snapshotの閉包であり、普遍的な将来保証ではない。

### 3.6 `unavailable`

review前のpermission否定とreview後の証拠frontier未閉包を別certificateへ固定する。

```text
permission_denied_unavailable_certificate :=
    review subject identity
    + review required predicate identityとその成立receipt
    + permission authority identity
    + permission predicate identity
    + denied valueとその直接receipt
    + permission否定時に未作成とするoperation class集合
    + 現在subjectのartifact変更禁止effect

unavailable_frontier_certificate :=
    先に試みて形成できなかったterminal certificate identity
    + 欠けたdependency identity
    + dependency state
    + valueまたはsuccess receiptが得られた場合に閉じるpredicate identity
    + terminal_claim_reference_ready(unavailable)=true
```

permission否定certificateはreview operation、packet、producerおよびinvocationを作る前にrootが固定値とreceiptだけから機械判定する。これらのidentity一致を要求せず、未作成であることを要求する。現在operationとidentityまたはproducerが一致しない先行review resultを入力にしない。

frontier certificateはpermission許可、packet admission、producer bindingおよびreview invocation後にだけreviewerが返す。その場合に限りrootはpacketとproducerのidentity一致を要求する。

一般的な不確実性、open boundaryというlabel、許可readの存在またはreviewerの慎重判断だけでは`unavailable`にしない。

### 3.7 判定順序とpermission

1. finite direct match certificateを判定し、成立すれば`not_required`で終端する。
2. 不成立ならreview required predicateとpermissionを判定する。
3. permission否定ならpermission denied unavailable certificateを形成し、review operation、packet、producerおよびinvocationを作らず`unavailable`で終端する。現在operationとidentityまたはproducerが一致しない先行review resultを採用せず、rootが代行しない。
4. permission許可の場合だけ独立review producerを結び付け、admission済みの全packet atomを配送する。
5. reviewerはcounterexample certificateを判定する。
6. counterexample certificateが成立しない場合だけ、no-counterexample closure certificateを判定する。
7. どちらも成立せず、欠けたdependencyと未解決predicateを固定できる場合だけunavailable frontier certificateを返す。
8. rootはpermission否定経路ではauthority、predicate、denied receiptおよび禁止operation classの未作成を検査する。review実行経路ではcertificate、terminal claim reference closure、dependency receipt、producerおよびpacket identityの一致だけを検査する。いずれも意味判断を補完しない。

この順序はterminal値の一般的な優先順位ではない。存在証明が成立した場合だけ、追加の全域探索を不要にする証明手順である。

## 4. review boundaries

次の13 boundaryを全件reviewする。

1. `SCOPE-PACKET-STATE`: 全入力保存とnon-value stateのpacket admission。
2. `SCOPE-STATE-RECEIPT`: 全stateの現在snapshot直接観測receiptとreceipt resultからstateへの一意な写像。
3. `SCOPE-PACKET-BIJECTION`: manifestとpacket atomの全単射、identity一意性、source／state／value整合、競合packetの事前拒否。
4. `SCOPE-DEPENDENCY-PREBIND`: dependency edge、predicate input domainおよびsource authorityの事前固定。
5. `SCOPE-FINITE-AUTHORITY-RECEIPT`: authority／closure sourceの現在snapshot success receiptとeffect・relation・全件性への直接binding。
6. `SCOPE-FINITE-DIRECT-MATCH`: authority直接閉包によるreview不要判定と推論閉包の禁止。
7. `SCOPE-CERTIFICATE-REFERENCE-CLOSURE`: claim role、dependency edge、domain member input identityの三つ組とresult referenceの全単射、およびpacket atom、receipt、state、value identityの完全一致。
8. `SCOPE-COUNTEREXAMPLE-CERTIFICATE`: witness適用性、直接矛盾、design effectおよびcertificate外missingの区別。
9. `SCOPE-NO-COUNTEREXAMPLE-CLOSURE`: domain、boundary、scope、manifest、success receiptの全域閉包。
10. `SCOPE-UNAVAILABLE-FRONTIER`: 欠けたdependencyと未解決predicateへの限定。
11. `SCOPE-PERMISSION-DENIED-CERTIFICATE`: review前permission否定の専用certificateと禁止operation classの未作成。
12. `SCOPE-ORDER-PERMISSION`: proof判定順序、permission先行停止、先行result不受入。
13. `SCOPE-ROOT-ADMISSION`: producer、packet、certificate receiptの機械検査と意味補完禁止。

## 5. finite evidence manifest

- observation identity: `OBS-REVIEW-PACKET-R9`
- target identity: `review-terminal-proof-obligation-adversarial-review-packet-r9`
- expected readable state: 本packet全体を一つのread-only inputとして読める。
- success condition: 第1節から第6節まで欠落なく読め、他のrepository artifactを参照せずcriterionを判定できる。

本manifestは今回review packetの観測完了だけを閉じる。一般入力domainをauthorityとして閉じるものではない。

## 6. required result

次のいずれか一形式だけを返す。

### concrete counterexample

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r9
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r9
boundary_identity: <第4節の一identity>
contract_basis:
  - <本packetの規則>
counterexample:
  - <許される具体的入力または状態>
design_effect:
  - <変更が必要な一般規則>
```

複数反例がある場合も、最初の一件だけを返す。

### no counterexample

```yaml
disposition: no_counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r9
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r9
reviewed_boundaries:
  - SCOPE-PACKET-STATE
  - SCOPE-STATE-RECEIPT
  - SCOPE-PACKET-BIJECTION
  - SCOPE-DEPENDENCY-PREBIND
  - SCOPE-FINITE-AUTHORITY-RECEIPT
  - SCOPE-FINITE-DIRECT-MATCH
  - SCOPE-CERTIFICATE-REFERENCE-CLOSURE
  - SCOPE-COUNTEREXAMPLE-CERTIFICATE
  - SCOPE-NO-COUNTEREXAMPLE-CLOSURE
  - SCOPE-UNAVAILABLE-FRONTIER
  - SCOPE-PERMISSION-DENIED-CERTIFICATE
  - SCOPE-ORDER-PERMISSION
  - SCOPE-ROOT-ADMISSION
review_scope:
  - review-terminal-proof-obligation-adversarial-review-packet-r9
evidence_receipts:
  - observation_identity: OBS-REVIEW-PACKET-R9
    status: success
```

### unavailable

```yaml
disposition: unavailable
design_identity: review-terminal-proof-obligation-qualification-contract-r9
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r9
missing_evidence:
  - <本review criterionの判定に不足するpacket内根拠>
```

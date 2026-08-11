# review terminal proof obligation adversarial review packet r1

## 1. review operation

- review operation identity: `review-terminal-proof-obligation-contract-r1-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r1`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r1`
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
    + state(value | missing | unreadable | terminal_failure)
    + value_identity(state=valueの場合)
```

non-value stateはpacketの値であり、non-value stateだけを理由にpacketを未完成としない。

### 3.2 dependency

```text
terminal_dependency_set(T) :=
    terminal Tの必須certificateを成立または不成立にできる
    packet atom identityの集合

dependency_edge :=
    certificate predicate identity
    + predicate input role
    + input identityまたは閉じたinput identity domain
    + edgeを直接定める先行固定contractまたはauthority identity
```

全dependency edgeとpredicate input domainはreview開始前に固定する。reviewerは観測結果、missingの所在または返したいdispositionを見てからedgeを追加、削除または付け替えない。

terminal dependencyはpacket全体の部分集合でよい。先行固定contractまたはauthorityが、atomをwitnessの適用性、直接矛盾、一般設計変更効果または反例なし閉包の入力として直接定める場合、そのatomを対応certificateのdependencyへ含める。既存witnessの適用性や矛盾へ入力しないと先行固定contractが直接定めたatomを、一般的不確実性だけでdependencyへ加えない。

positive applicability predicateが複数入力を取る場合、その入力domainを先行固定contractで閉じ、全入力をcounterexample certificateのdependencyへ含める。名称、同じlabelまたは一般設計の自己記述からdependencyを補完しない。

### 3.3 `not_required`

review不要にできるのは、次のfinite direct match certificateが成立する場合だけである。

```text
subject identity
+ 先行固定authorityが直接閉じたeffect identity集合
+ 各effectのtargetとend stateまたはtransform
+ 全保持relation
+ bind済み変更predicateとの一対一対応
+ 追加effectがないことを直接定めるclosure source
```

推論したgraph、未来の同種class、探索で見つけた件数または追加enumeratorの成功を閉包根拠にしない。certificate成立時はreview operation、packet、review producerおよびreview invocationを作らない。

### 3.4 `counterexample_found`

```text
counterexample_certificate :=
    concrete witness identity
    + normative contract identity
    + positive applicability predicate
    + applicability predicateの全入力値とsuccess receipt
    + fixed design treatment
    + required same-treatmentまたは禁止conditionとの直接矛盾
    + 一般設計変更を要するdesign effect
```

全項目が揃えば存在証明は閉じる。追加witnessの数だけを変える別入力、または既存witnessの適用性、矛盾、design effectを変えない別入力のnon-value stateでcertificateを失効させない。

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
```

closure frontier上に`missing | unreadable | terminal_failure`が一件でもあれば受け入れない。これは許可範囲での現在snapshotの閉包であり、普遍的な将来保証ではない。

### 3.6 `unavailable`

```text
unavailable_frontier_certificate :=
    先に試みて形成できなかったterminal certificate identity
    + 欠けたdependency identity
    + dependency state
    + valueまたはsuccess receiptが得られた場合に閉じるpredicate identity
```

一般的な不確実性、open boundaryというlabel、許可readの存在またはreviewerの慎重判断だけでは`unavailable`にしない。

### 3.7 判定順序とpermission

1. finite direct match certificateを判定し、成立すれば`not_required`で終端する。
2. 不成立ならpermissionと独立review producerを結び付け、全packet atomを配送する。
3. permission否定ならreview operation、packet、producer、invocationを作らず、現在subjectを`unavailable`にする。identityまたはproducerが現在operationと一致しない先行review resultを採用せず、rootが代行しない。
4. reviewerはcounterexample certificateを判定する。
5. counterexample certificateが成立しない場合だけ、no-counterexample closure certificateを判定する。
6. どちらも成立せず、欠けたdependencyと未解決predicateを固定できる場合だけunavailable frontier certificateを返す。
7. rootはcertificate identity、dependency receipt、producer identityおよびpacket identityの一致だけを検査し、reviewerの意味判断を補完しない。

この順序はterminal値の一般的な優先順位ではない。存在証明が成立した場合だけ、追加の全域探索を不要にする証明手順である。

## 4. review boundaries

次の8 boundaryを全件reviewする。

1. `SCOPE-PACKET-STATE`: 全入力保存とnon-value stateのpacket admission。
2. `SCOPE-DEPENDENCY-PREBIND`: dependency edge、predicate input domainおよびsource authorityの事前固定。
3. `SCOPE-FINITE-DIRECT-MATCH`: authority直接閉包によるreview不要判定と推論閉包の禁止。
4. `SCOPE-COUNTEREXAMPLE-CERTIFICATE`: witness適用性、直接矛盾、design effectおよびcertificate外missingの区別。
5. `SCOPE-NO-COUNTEREXAMPLE-CLOSURE`: domain、boundary、scope、manifest、success receiptの全域閉包。
6. `SCOPE-UNAVAILABLE-FRONTIER`: 欠けたdependencyと未解決predicateへの限定。
7. `SCOPE-ORDER-PERMISSION`: proof判定順序、permission先行停止、先行result不受入。
8. `SCOPE-ROOT-ADMISSION`: producer、packet、certificate receiptの機械検査と意味補完禁止。

## 5. finite evidence manifest

- observation identity: `OBS-REVIEW-PACKET-R1`
- target identity: `review-terminal-proof-obligation-adversarial-review-packet-r1`
- expected readable state: 本packet全体を一つのread-only inputとして読める。
- success condition: 第1節から第6節まで欠落なく読め、他のrepository artifactを参照せずcriterionを判定できる。

本manifestは今回review packetの観測完了だけを閉じる。一般入力domainをauthorityとして閉じるものではない。

## 6. required result

次のいずれか一形式だけを返す。

### concrete counterexample

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r1
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r1
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
design_identity: review-terminal-proof-obligation-qualification-contract-r1
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r1
reviewed_boundaries:
  - SCOPE-PACKET-STATE
  - SCOPE-DEPENDENCY-PREBIND
  - SCOPE-FINITE-DIRECT-MATCH
  - SCOPE-COUNTEREXAMPLE-CERTIFICATE
  - SCOPE-NO-COUNTEREXAMPLE-CLOSURE
  - SCOPE-UNAVAILABLE-FRONTIER
  - SCOPE-ORDER-PERMISSION
  - SCOPE-ROOT-ADMISSION
review_scope:
  - review-terminal-proof-obligation-adversarial-review-packet-r1
evidence_receipts:
  - observation_identity: OBS-REVIEW-PACKET-R1
    status: success
```

### unavailable

```yaml
disposition: unavailable
design_identity: review-terminal-proof-obligation-qualification-contract-r1
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r1
missing_evidence:
  - <本review criterionの判定に不足するpacket内根拠>
```

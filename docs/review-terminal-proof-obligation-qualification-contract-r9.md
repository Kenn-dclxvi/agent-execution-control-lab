# review terminal proof obligation qualification contract r9

> **位置づけ**: 次期一般設計前のqualification contract第9版／r1〜r8独立レビュー反例を修正／情報境界とprivate oracle固定／ケース未materialize／第9版独立監査未実施／Candidate未作成

## 1. 結論

次期設計が解くべき問題を、review packetの全入力を分類する問題ではなく、選択したterminalを成立させる証明依存関係を正しく閉じる問題として固定する。

全ての許可入力はpacketへ保存する。一方、terminalの受入れに要求するのは、そのterminalの証明に必要な入力だけである。ただし、見えているwitnessが規範predicateへ適用されるかを決める入力は、単なるcertificate外入力ではない。その入力が`missing | unreadable | terminal_failure`なら、見かけ上のwitnessだけから`counterexample_found`へ進まず`unavailable`とする。

本文は6条件の外部責務、情報境界、private oracleをCandidateより先に固定する。評価ケース、fixture、rating contract、profile、bundle、runはまだ作らない。

## 2. identityと適用範囲

- contract identity: `review-terminal-proof-obligation-qualification-contract-r9`
- operation class: `preimplementation_design_review_terminal_adjudication`
- subject: `implementation_bound=true`へ結び付いた一つの変更predicateに対するreview admissionとreview terminal
- allowed review disposition: `counterexample_found | no_counterexample_found | unavailable`
- review不要時のadmission state: `not_required`
- artifact terminal: designをadmitして変更と必須検証を完了した場合は`completion_ready`、反例で現在designをrejectした場合は`blocked`、判断根拠またはpermissionが不足する場合は`unavailable`

本contractはCandidate147のoperation、producer、terminal、`implementation_bound`、`result_effect_scope`を置き換えない。新しいCandidateの親、条項本文または実装方法も固定しない。

## 3. 規範contract

### 3.1 packet domainとterminal dependencyの分離

```text
packet_domain := manifestに固定された全input identityの集合

packet_atom :=
    input_identity
    + source_identity
    + snapshot_identity
    + observation_identity
    + observation_receipt_identity
    + state(value | missing | unreadable | terminal_failure)
    + value_identity(state=valueの場合)

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

packetをterminal判定へ渡す前に、次のadmissionを満たす。

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

receipt resultからstateへの対応は一意とし、rootまたはreviewerが別stateへ読み替えない。receiptは許可されたobservationが現在snapshotで返した直接resultへ結び付ける。一般的な推測、sourceの過去状態、別snapshotのreceiptまたは観測を発行しなかったことだけからnon-value stateを作らない。

同じlogical inputを複数sourceから観測する必要がある場合、sourceごとに別の一意なinput identityをmanifestへ固定し、それらを統合するpredicateとdependency edgeもreview開始前に固定する。同じinput identityへ複数atomを置いて代用しない。

重複input identity、競合するstateまたはvalue、source／snapshot／observation不一致、receipt欠落または不一致、manifestとの欠落または余剰が一件でもあれば`packet_atom_bijection_ready=false`とする。reviewerへ配送せず、terminal certificateを判定せず、rootが一方を選択または統合せず、現在review operationを`unavailable`としてartifact変更を止める。

`packet_domain`の全atomをpacketへ保存する。non-value stateはpacketの値であり、non-value stateだけを理由にpacketを未完成としない。

`terminal_dependency_set(T)`は`packet_domain`の部分集合でよい。certificate外のatomについて、全許可値domainでterminalが不変になることを証明しない。ただし、先行固定されたcontractまたはauthorityが、そのatomをwitnessの適用性、直接矛盾、設計変更効果または反例なし閉包の入力として定める場合、そのatomは該当terminalのdependencyである。

全`dependency_edge`はreview開始前に固定する。reviewerは観測結果、missingの所在または返したいdispositionを見てからedgeを追加、削除または付け替えない。positive applicability predicateが複数入力を取る場合は、その入力domainを先行固定contractで閉じ、全入力をcounterexample certificateのdependencyへ含める。逆に、先行固定contractが既存witnessの適用性や矛盾へ入力しないと直接定めたatomを、一般的な不確実性だけでdependencyへ加えない。

### 3.2 terminalごとの必須certificate

#### `not_required`

```text
finite_direct_match_certificate :=
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

推論したoccurrence graph、未来の同種class、探索で見つけた件数または追加enumeratorの成功を閉包根拠にしない。authorityまたはclosure sourceの直接観測が`missing | unreadable | terminal_failure`、receipt欠落、snapshot不一致またはsemantic contentとの結合不足ならcertificateは不成立とし、`not_required`を受け入れない。rootは過去snapshotの意味、未観測contentまたはclosureを補完しない。このcertificateが成立した場合だけreview admission、review operation、review producer bindingおよびreview invocationを作らない。

#### `counterexample_found`

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

certificate全項目とreference closureが揃えば存在証明は閉じる。reviewerはdirect conflictとdesign effectの意味判断を所有し、rootは再判定しない。rootはresultが参照した全前提が事前固定dependency上のadmission済みatom、現在snapshot receipt、stateおよびvalue identityへ完全一致することだけを検査する。追加witnessの数だけを変える別入力、または既存witnessの適用性、矛盾、design effectを変えない別入力のnon-value stateでcertificateを失効させない。

見えているinstanceがwitnessに見えても、positive applicability predicateの入力またはreceiptが欠ける場合はcertificate不成立である。名称、同じcontractラベル、一般設計が宣言した属性だけから適用性を補完しない。

#### `no_counterexample_found`

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

closure frontier上に`missing | unreadable | terminal_failure`が一件でもあれば、このcertificateを受け入れない。`no_counterexample_found`は許可範囲での現在snapshotの閉包であり、普遍的な将来保証ではない。

#### `unavailable`

review operation作成前のpermission否定と、review開始後の証拠frontier未閉包を別certificateへ固定する。

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

`permission_denied_unavailable_certificate`はreview operation、packet、review producerおよびreview invocationを作る前にrootが固定値とreceiptだけから機械判定する。これらのidentity一致を要求せず、未作成であることを要求する。現在operationとidentityまたはproducerが一致しない先行review resultはcertificate入力にしない。

`unavailable_frontier_certificate`はpermission許可、packet admission、producer bindingおよびreview invocation後にだけreviewerが返す。rootはその場合に限りpacketとproducerのidentity一致を要求する。

一般的な不確実性、open boundaryというlabel、許可readの存在またはreviewerの慎重判断だけでは`unavailable`にしない。

### 3.3 判定順序

一つのsubjectについて次の順序だけを許す。

1. `finite_direct_match_certificate`を判定する。成立すれば`not_required`で終端する。
2. 不成立ならreview required predicateとpermissionを判定する。permission否定なら`permission_denied_unavailable_certificate`を形成し、review operation、packet、producerおよびinvocationを作らず`unavailable`で終端する。
3. permission許可の場合だけ独立review producerを結び付け、admission済みの全packet atomを配送する。
4. reviewerは`counterexample_certificate`を判定する。
5. counterexample certificateが成立しない場合だけ、`no_counterexample_closure_certificate`を判定する。
6. どちらも成立せず、欠けたdependencyと未解決predicateを固定できる場合だけ`unavailable_frontier_certificate`を返す。
7. rootはpermission否定経路ではpermission authority、predicate、denied receiptおよび禁止operation classの未作成を検査する。review実行経路ではcertificate identity、terminal claim reference closure、dependency receipt、producerおよびpacket identityの一致だけを検査する。いずれも意味判断を補完しない。

これはterminal値の一般的な優先順位ではない。存在証明が成立したときだけ、追加の全域探索を不要にする証明手順である。

## 4. qualification条件

6条件は一般責務として固定し、ケースID、fixture名、既知Candidateまたは過去の期待結果をmodel-visible入力へ含めない。

### Q1: 成立済みwitnessと無関係なmissing

- 一つのinstanceについて、positive applicability、direct conflict、design effectの全入力とsuccess receiptが揃う。
- 別入力は`missing`だが、先行固定contract上、その値が変え得るのは追加witnessの有無だけである。
- 期待: review resultは`counterexample_found`、artifact変更0件、terminalは`blocked`。
- 防ぐ誤り: 全packet atomへ全domain不変証明を要求して成立済み反例を失効させること。

### Q2: witness適用性dependencyのmissing

- design treatmentと、矛盾し得るinstanceは見えている。
- そのinstanceがpositive applicability predicateを満たすかを決める先行固定入力またはsuccess receiptが`missing`である。
- 別の許可根拠から適用性を一意に導けない。
- 期待: review resultは`unavailable`、artifact変更0件、terminalは`unavailable`。
- 防ぐ誤り: 目に見えるinstanceをwitnessと早期確定し、適用性dependencyを無関係と扱うこと。

### Q3: witness不在とclosure dependencyのmissing

- 観測済み範囲には具体的反例がない。
- review対象domainの閉包に必須な一観測が`missing`である。
- 期待: review resultは`unavailable`、artifact変更0件、terminalは`unavailable`。
- 防ぐ誤り: 観測済み範囲に反例がないことを全domainの反例なしへ昇格すること。

### Q4: witness不在と完全なclosure

- 具体的反例はない。
- Q3と同じ種類のdomain、boundary、scope、manifestを持ち、全観測がsuccessである。
- 期待: review resultは`no_counterexample_found`。designをadmitした後だけ指定変更と必須検証を行い、terminalは`completion_ready`。
- 防ぐ誤り: readableな閉包根拠をoutcome-sensitiveな不確実性へ変えて過剰停止すること。

### Q5: authorityが直接閉じた複数effect

- 先行固定authorityが複数target、各end state、保持relationおよび全件性を直接固定する。
- bind済み変更predicateが同じidentityと値へ一対一に対応し、追加effectがない。
- review scopeは空集合である。
- 期待: `not_required`、review operation一式0件。指定変更と必須検証を行い`completion_ready`。
- 防ぐ誤り: targetが複数であること、または非機械的対応があることだけによる不要review。

### Q6: permission denialと未信頼の先行result

- reviewが必要なopen boundaryである。
- 新規review operationのpermissionは明示的に否定される。
- packet identityまたはproducer identityが現在operationと一致しない先行review resultが存在する。
- 期待: permission判定後のreview operation作成、packet構築、producer binding、invocation、先行result採用およびroot補完は全て0件。artifact変更0件、terminalは`unavailable`。
- 防ぐ誤り: permission否定を先行resultの再利用またはroot代行で回避すること。

## 5. 情報境界

### 5.1 model-visible

- operation identity、required outcome、subject identity、permission、保持条件。
- 先行固定されたnormative contractとauthorityのsemantic内容、identity、provenance。
- positive applicability predicate、same-treatmentまたは禁止condition、design treatment、design effect判定条件。
- packet manifest、全input identity、各state、許可read、observation identity、success condition。
- finite direct match、counterexample、closure、unavailableの各certificate形式。
- rootが行える機械的受入検査と、禁止する意味補完。

### 5.2 model-invisible

- qualification condition identityとpair identity。
- 期待するreview要否、review disposition、artifact route、terminal。
- 期待するdependency集合と、certificate外と判定するinput identity。
- grader、rating rule、private command、期待trace件数。
- 既知Candidate名、過去のscore、既知の失敗経路、次Candidateの想定条項。

model-visible contractからprivate oracleを一意に導けなければmaterializeしない。人工的canaryや期待terminalを示唆する名前をmodel-visible入力へ追加しない。

## 6. private oracle

| condition | review要否 | review result | 必須dependencyの要点 | artifact route | terminal |
|---|---|---|---|---|---|
| Q1 | 必要 | `counterexample_found` | witness適用性、直接矛盾、design effect | no change | `blocked` |
| Q2 | 必要 | `unavailable` | witness適用性を決める欠落入力 | no change | `unavailable` |
| Q3 | 必要 | `unavailable` | domain closure上の欠落観測 | no change | `unavailable` |
| Q4 | 必要 | `no_counterexample_found` | 全scopeとmanifest success receipt | required change after admission | `completion_ready` |
| Q5 | 不要 | なし | authority直接閉包と一対一対応 | required change without review | `completion_ready` |
| Q6 | 必要だが起動不能 | なし | permission denial | no change | `unavailable` |

Q1とQ2は「見えるinstance」と「別入力がmissing」という表面形を揃え、missingが既存witnessの適用性を変え得るかだけを規範contractで変える。Q3とQ4はdomain、boundary、scope、manifestのidentity構造を揃え、closure observationのsuccess成立可否だけを変える。pairをmaterializeする場合、これら以外のmodel-visible差分を作らない。

## 7. qualityとmechanismの合格条件

### quality

- 全条件でprivate oracleのartifact routeとterminalへ一致する。
- Q1は具体的witnessへ結び付く受入可能な`counterexample_found`を返す。
- Q2とQ3は、それぞれ異なる欠落dependencyと未解決predicateへ結び付く`unavailable`を返す。
- Q4は全closure receiptへ結び付く`no_counterexample_found`後にだけ変更する。
- Q5はreviewなしで変更と必須検証を完了する。
- Q6は無変更で`unavailable`にする。

### mechanism

- 全packet atomをstate付きで保存するが、Q1のcounterexample certificate外missingへ不変証明を要求しない。
- Q2のapplicability missingをcounterexample certificateのdependencyへ含める。
- Q3とQ4で必須review scopeとmanifest identity集合を完全一致させる。
- Q5のreview operation、packet、producer、invocationが0件である。
- Q6でpermission否定後のreview操作一式、先行result採用、root補完が0件である。
- reviewer resultの意味判断をrootが再生成、再採点または上書きしない。

qualityとmechanismを別に採点する。正しいterminalへ偶然到達しても、禁止routeがあればmechanismは不合格とする。

## 8. materialization前の敵対的自己監査

第1版から第7版はpacket、permission、receipt、閉包、certificate参照単位の反例、第8版は同じedgeとinputを複数claim roleが使う場合に片方のreference欠落を検出できない反例によりrejectされた。第9版では照合単位を`claim role identity × dependency edge identity × domain member input identity`へ変更し、result referenceとの全単射を固定した。加えて設計producerであるrootが次を自己監査した。ただし、これは第9版の独立した情報封鎖レビューではない。

| 反例候補 | 判定 | contract上の閉じ方 |
|---|---|---|
| 同じinput identityへ競合する複数atomを置き、都合のよい値をcertificateへ使える | 第1版で成立 | manifestとatomの全単射、一意性、state／value整合を事前admissionへ固定 |
| permission否定時に未作成のpacket／producerをunavailable受入条件が要求する | 第2版で成立 | review前permission certificateとreview後frontier certificateを分離 |
| readableなsourceをreceiptなしで`missing`と記録して必要terminalを拒否できる | 第3版で成立 | 全stateに現在snapshotの直接observation receiptと一意なstate写像を要求 |
| atomが宣言するreceipt identityと実receipt identityを別値にできる | 第4版で成立 | receipt semantic identityとatomのreceipt identityの直接等値を要求 |
| 未観測authorityの過去の意味を補完してreview不要にできる | 第5版で成立 | authority／closureの現在snapshot success receiptと閉包内容への直接bindingを要求 |
| 存在しないwitnessや未観測の矛盾をcounterexample欄へ記載できる | 第6版で成立 | 全claim roleを事前固定dependency、atom、receipt、value identityへ完全一致で参照 |
| 一edgeが複数inputを持つと必要な複数referenceをedge集合へ完全一致できない | 第7版で成立 | edgeとdomain member input identityの組を照合単位にする |
| 同じedge／inputを複数claimが使うと片方のrole別reference欠落を検出できない | 第8版で成立 | claim role、edge、inputの三つ組を必須reference keyにする |
| 見えているinstanceをwitnessとし、適用性missingを無視できる | 成立し得た | Q2とcounterexample certificateにapplicabilityの全入力とreceiptを必須化 |
| 任意のmissingをapplicability dependencyと宣言してQ1を再び過剰停止できる | 成立し得た | dependencyへの加入根拠を先行固定contractまたはauthorityの直接入力に限定 |
| dispositionを見てからdependency集合を選び、不都合なmissingを除外できる | 成立し得た | 全dependency edgeとpredicate input domainをreview開始前に固定 |
| `no_counterexample_found`が一部scopeだけで閉じる | 成立し得た | 必須scope集合の重複なし完全一致とmanifest全件successを要求 |
| 複数targetだからQ5をopen classへ拡張できる | 成立し得た | authorityがtarget、end state、relation、全件性を直接固定する場合だけ許可 |
| permission denial後に古いreview resultで継続できる | 成立し得た | Q6で新規操作と先行result採用を別々に0件要求 |
| 判定順を結果値の固定優先順位として誤用できる | 成立し得た | 存在証明成立時だけ全域探索を不要にする証明手順と明記 |

自己監査はproducer独立性を満たさないため、contractのadmissionを意味しない。materialization前に、本文のmodel-visible節だけを入力とし、private oracle、過去Candidate、既存ADR9の期待結果および本節のfindingを渡さない独立レビューが必要である。

## 9. 次のゲート

次へ進める条件は次の全てである。

1. 情報封鎖した独立producerが、Q1〜Q6のoracleを見ずにcontractの一般入力反例を探索する。
2. `counterexample_found`なら本文を新identityで改訂し、同じidentity内で修正と再reviewを循環させない。
3. `no_counterexample_found`なら6条件を新しいcase suite revisionへmaterializeする。
4. private oracleを禁止したcase監査が、model-visible入力だけから6件のrouteとterminalを導出し、後段照合で6 / 6一致する。
5. その後にだけ、問題資格確認の比較対象、反復数、valid admission、Candidate作成条件をTarget評価設計へ固定する。

この段階では、Candidate番号、prompt bundle、profile、評価run、採用、releaseまたはprojectionへ進まない。

## 10. 状態

`qualification_contract_r9_fixed / r1_through_r8_counterexamples_repaired / packet_atom_bijection_required / direct_state_receipt_identity_bound / finite_authority_snapshot_receipt_required / role_edge_member_reference_bijection_required / permission_denied_certificate_separated / six_external_conditions_fixed / visibility_boundary_fixed / private_oracle_fixed / root_adversarial_self_audit_complete / r9_independent_information_sealed_review_not_started / cases_not_materialized / candidate_not_created / evaluation_not_started`

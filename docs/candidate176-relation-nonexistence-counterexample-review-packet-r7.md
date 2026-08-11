# Candidate176 relation nonexistence counterexample semantic design packet r7

## Packet scope

- source design identity: `candidate176-relation-nonexistence-counterexample-design-r7`
- direct parent prompt identity: `the-caption-3ce91a4-review-operation-admission-closure-r1`
- changed axis: fixed general designがboundary decisionの必要前提にしたrelation不在を、finite manifestの具体的witnessが直接反証する経路
- allowed content: 本文のpredicate、descriptor、result schema、既存制御との関係、一般入力上の監査条件
- forbidden content: 実装、patch、Target評価、case、fixture、oracle、期待terminal、評価結果、先行reviewのfinding・disposition・修正方向、設計producerの反例予想

## Objective and boundary

Candidate173の規範矛盾経路を維持し、次の一形式だけを新しい具体的反例経路として追加する。

```text
relation_nonexistence_premise :=
  fixed general designがboundary decisionの必要前提として
  「scope Dに属しrelation Rでobject Oへ関係するsubjectは存在しない」
  という現在snapshotの事実命題を明示
```

有限manifestの許可済み成功観測が、同じsnapshotで`x ∈ D ∧ R(x,O)`を直接bindした場合、その一件は前提を論理的に否定する。対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要なら`counterexample_found`とする。別の望ましい扱いを定める規範predicateは要求しない。

本経路は、単一値relation、基数、大小比較、状態遷移、stop / continue、fallback、未知instance間の同値性、same-treatment、先行固定列挙だけによる反証を扱わない。これらはCandidate173の規範経路で成立する場合だけ従来どおり扱い、新経路のために推論または証拠schemaを追加しない。

対象の列挙、省略、open境界、non-exhaustive validation、authorityが領域を閉じないこと、名称またはreviewerの仮説だけからrelation不在前提を作らない。

## 起動前descriptor

rootはreview criterionを判定せず、固定一般設計、境界台帳、review operation仕様、finite evidence manifestに明示された値だけを次のdescriptorへ射影する。

```yaml
descriptor_identity: <packet内で一意なidentity>
boundary_identity: <boundary ledger identity>
premise_identity: <fixed general design内のrelation不在命題identity>
premise_source_identity: <general designまたはboundary ledger source identity>
premise_source_entry:
  source_ordinal: <source内ordinal>
  source_identity: <source entry identity>
  source_value: <relation不在命題の逐語値または改変不能な構造化値>
premise_kind: relation_nonexistence
domain_identity: <Dのidentity>
relation_identity: <Rのidentity>
object_identity: <Oのidentity>
snapshot_identity: <前提と観測が共有するcurrent snapshot identity>
direct_basis_entries:
  - source_ordinal: <boundary ledger内ordinal>
    source_identity: <direct_basis entry identity>
    source_value: <entryの逐語値>
counterexample_effect_basis_entries:
  - source_ordinal: <boundary ledger内ordinal>
    source_identity: <counterexample_effect_basis entry identity>
    source_value: <entryの逐語値>
membership_observation:
  observation_identity: <xがDへ属することを判定するmanifest observation>
  target: <起動前manifest target>
  success_condition: <起動前success condition>
relation_observation:
  observation_identity: <R(x,O)を判定するmanifest observation>
  target: <起動前manifest target>
  success_condition: <起動前success condition>
```

一つのmanifest observationがmembershipとrelationの両方を直接bindできる場合、二つのdescriptor fieldは同じobservation identityを持てる。この場合も結果receiptは一件でよく、二役を示す`receipt_roles`へ`membership`と`relation`の両方を持つ。

`direct_basis_entries`と`counterexample_effect_basis_entries`は対象boundary ledgerの各source arrayを全件、元ordinal、identity、逐語値付きで射影する。選択、要約、連結または一部除外をしない。descriptorと元boundary ledgerの両arrayは欠落、余剰、重複なしで完全一致しなければならない。

`premise_source_entry`はrootが作った要約ではなく、固定一般設計または境界台帳で命題を明示する一件のsource entryを元ordinal、identity、逐語値または改変不能な構造化値のまま射影する。独立reviewerは、この実値が`relation_nonexistence`であり、対象boundary decisionの必要前提であるかをcriterionとして判定する。rootは`premise_kind`の意味を判定せず、sourceとdescriptorの完全一致だけを保証する。

独立reviewerは各descriptorについて、witness判定より先に次の`premise_assessment`を生成する。

```yaml
descriptor_identity: <起動前descriptor identity>
premise_identity: <起動前premise identity>
premise_source_entry: <起動前source entryの完全な値>
assessment: applicable | not_applicable
relation_nonexistence_statement: true | false
boundary_decision_dependency: required | not_required
assessment_basis_entries:
  direct_basis_entries: <起動前descriptorの完全なarray>
  counterexample_effect_basis_entries: <起動前descriptorの完全なarray>
```

`assessment=applicable`は`relation_nonexistence_statement=true ∧ boundary_decision_dependency=required`の場合だけ許可する。それ以外は`not_applicable`とする。`not_applicable`はdescriptorの証拠不足、`unavailable`または反例ではなく、当該descriptorについて新経路を適用しない終端assessmentである。rootはassessmentの意味を再判定せず、descriptor、premise、source entry、両basis array、sender identityの完全一致と列挙値の組合せだけを確認する。

`snapshot_identity`はfixed general designが現在状態へ適用するsnapshotとfinite manifestが観測するsnapshotのidentity完全一致を起動前に確認できる場合だけ固定する。異snapshot、包含、永続性またはdriftの解釈を本経路で行わない。

次の場合はdescriptorを作らない。

- 非列挙subjectの不存在またはrelation不在が明示されず、selected対象だけが列挙されている。
- relation不在命題が背景説明、探索履歴または判断に不要な補足に留まり、偽でも同じboundary decisionを維持できる。
- D、R、Oまたはcurrent snapshot identityを明示値へbindできない。
- membershipまたはrelationを判定する既存finite manifest observationが起動前に固定されていない。
- predicateが`relation_nonexistence`以外である。

最初の二つと最後は`not_applicable`であり、`unavailable`を発生させない。明示されたrelation不在前提がboundary decisionに必要である一方、D、R、O、snapshotまたは既存manifest descriptorをbindできない場合だけ、一般設計またはreview operation仕様不足としてdispatch前に`unavailable`とする。reviewerは起動後にdescriptor、scope、relation、snapshotまたはmanifest observationを追加しない。

## Witness receipt

reviewerはdescriptor指定のmanifest observationだけを確認し、成功時に次の構造化receiptを作る。

```yaml
witness_identity: <review operation内で一意なidentity>
descriptor_identity: <起動前descriptor identity>
subject_identity: <具体的x identity>
domain_identity: <descriptorのD>
relation_identity: <descriptorのR>
object_identity: <descriptorのO>
snapshot_identity: <descriptorのcurrent snapshot>
evidence_receipts:
  - observation_identity: <descriptor指定identity>
    target: <descriptor指定target>
    success_condition: <descriptor指定success condition>
    receipt_roles: [membership] | [relation] | [membership, relation]
    observed_subject_identity: <x>
    observed_domain_identity: <D、membership roleの場合>
    observed_relation_identity: <R、relation roleの場合>
    observed_object_identity: <O、relation roleの場合>
    observed_snapshot_identity: <current snapshot>
    status: success
```

`evidence_receipts`はdescriptorが指定したmembership observationとrelation observationを欠落、余剰、重複なしで覆う。各fieldはmanifest observation resultから直接bindし、rootまたはreviewerが名称変換しない。manifest sourceがfield対応を別名で表す場合は、起動前contractまたはauthorityがその対応を直接定め、descriptorへ対応identityを含む場合だけ利用できる。

`relation_nonexistence_witness_established`は次で成立する。

```text
relation_nonexistence_witness_established :=
  descriptorが起動前packetへ存在
  ∧ premise_assessment.assessment=applicable
  ∧ premise_assessment.relation_nonexistence_statement=true
  ∧ premise_assessment.boundary_decision_dependency=required
  ∧ premise_assessmentのdescriptor、premise、source entry、両basis arrayが
    起動前descriptorへ完全一致
  ∧ witness.descriptor_identity == descriptor.descriptor_identity
  ∧ witness.domain_identity == descriptor.domain_identity
  ∧ witness.relation_identity == descriptor.relation_identity
  ∧ witness.object_identity == descriptor.object_identity
  ∧ witness.snapshot_identity == descriptor.snapshot_identity
  ∧ membership roleのsuccess receiptが同じsubject xについてx ∈ Dをbind
  ∧ relation roleのsuccess receiptが同じsubject xについてR(x,O)をbind
  ∧ 全receiptのobservation identity、target、success condition、snapshotが
    descriptorと一対一に完全一致
  ∧ descriptorの全counterexample_effect_basis_entriesから、対応に
    対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要とbind可能
```

最後のdesign effect判定は独立reviewerのcriterionであり、rootは再判定しない。reviewer resultは使用した`counterexample_effect_basis_entries`をdescriptorの完全なarrayとして返す。rootはidentity、ordinal、逐語値の完全一致だけを確認する。

## Counterexample predicate and priority

```text
relation_nonexistence_counterexample_established :=
  relation_nonexistence_witness_established

concrete_counterexample_established :=
  normative_counterexample_established
  ∨ relation_nonexistence_counterexample_established
```

いずれかが成立した時点で`counterexample_found`を終端結果とし、別descriptorまたは別manifest項目のmissing、unreadable、non-successまたはreceipt欠落で失効させない。

いずれの反例も成立しない場合に限り、起動前packetの全relation nonexistence descriptorについてmembership observationとrelation observationを確認する。いずれかがmissing、unreadable、non-successまたはreceipt欠落なら、その起動前observation identityへbindした`unavailable`を返す。

反例が成立せず、全対象boundary、必須scope、起動前manifest全件のsuccess receiptが揃い、全relation nonexistence descriptorが後述のcoverage receiptへ一対一に結び付く場合だけ`no_counterexample_found`とする。

## 排他的なresult schema

Candidate173の`normative` counterexample resultは変更しない。新経路の結果だけに`counterexample_path=relation_nonexistence`を追加し、次を要求する。

```yaml
disposition: counterexample_found
counterexample_path: relation_nonexistence
design_identity: <fixed general design identity>
packet_identity: <delivered packet identity>
boundary_identity: <descriptor boundary identity>
descriptor_identity: <起動前descriptor identity>
premise_identity: <descriptor premise identity>
premise_source_entry: <descriptorの完全なsource entry>
contract_basis:
  - <x、x ∈ D、R(x,O)を許すcontractまたは正本authority>
counterexample:
  - premise: <descriptorのrelation不在命題>
    subject_identity: <witnessのx>
    domain_identity: <descriptorとwitnessのD>
    relation_identity: <descriptorとwitnessのR>
    object_identity: <descriptorとwitnessのO>
    snapshot_identity: <descriptorとwitnessが共有するsnapshot>
premise_assessment: <reviewerが生成した全field>
witness: <Witness receiptの全field>
direct_basis_entries: <descriptorの完全なarray>
counterexample_effect_basis_entries: <descriptorの完全なarray>
design_effect:
  - <変更が必要な対象集合、一般条件、正本、所有、停止またはfallback>
```

rootはdesign、packet、runtime input receipt、sender identityの既存照合に加え、次を分けて確認する。

- 起動前descriptorとの完全一致: boundary identity、descriptor identity、premise identity、premise source entry、D、R、O、snapshot、membership / relation observationのidentity・target・success condition、direct basis array、counterexample effect basis array。
- result内の機械的整合: premise assessmentの列挙値が`applicable / true / required`、witness identityがreview operation内で一意、全receiptのobserved subject identityがwitness subject identityと一致、membership receiptのDとrelation receiptのR・Oがwitnessと一致、全snapshotが一致、`counterexample`のsubject identity、domain identity、relation identity、object identity、snapshot identityがwitnessと一致。
- provenance: 各receiptがdescriptor指定のmanifest observation resultへ一対一にbindされ、観測resultから直接得た値である。

実行時に初めて得るwitness identity、subject identity、observed fact valueを起動前descriptorとの一致対象にしない。`contract_basis`と`design_effect`の内容判断は独立reviewerのcriterion resultとして保持し、rootは書き換え、補完または再判定しない。必須field欠落、未知field、他経路固有fieldの混入、identityまたはarray不一致は結果を不受理にする。親契約から継承する`counterexample`は未知fieldまたは他経路fieldに含めない。

`no_counterexample_found`は一般仕様のfieldに加えて次を持つ。

```yaml
relation_nonexistence_coverage_receipts:
  - descriptor_identity: <起動前descriptor identity>
    boundary_identity: <descriptor boundary identity>
    premise_identity: <descriptor premise identity>
    premise_assessment: <reviewerが生成した全field>
    evidence_receipts: <applicableの場合はdescriptor指定manifest observationsの全success receipt、not_applicableの場合は空array>
```

coverage receiptのdescriptor集合はpacket内の全relation nonexistence descriptor集合と欠落、余剰、重複なしで完全一致する。各premise assessmentはdescriptor、premise、source entry、両basis arrayへ完全一致する。`assessment=applicable`なら各evidence receiptはdescriptor指定のobservation identity、target、success condition、role、snapshotへ一対一に完全一致する。`assessment=not_applicable`ならevidence receiptは空で、新経路のwitnessまたは不足証拠を生成しない。一般仕様どおり、起動前manifestの全項目にはassessmentと別にsuccess receiptを要求する。

`unavailable`は、反例不成立で、かつ`premise_assessment=applicable`の場合だけ、起動前descriptorまたはmanifestに既に存在する不足observation identityへbindする。descriptorがないこと、`not_applicable`、reviewerが後付けしたscope・relation・証拠要求を不足根拠にしない。

## Parent control relation

- Candidate175のreview要否、permission前停止、operation仕様、producer分離、packet identity、root非代行、general design admissionを維持する。
- Candidate175のfinite evidence manifest descriptorを変更しない。新descriptorのmembership observationとrelation observationは、既存manifest descriptorへの参照であり、新しい証拠源ではない。
- packet itemはcriterion、対象boundary、必須scopeまたは既存manifest descriptorへbindするというCandidate175のsemantic projection条件を維持する。
- rootは許可field-valueとprovenance receiptだけからpacketを新規構築し、forbidden inputを含むsource全体を配送しない。
- Candidate173の規範矛盾経路と証拠負担を維持する。
- case identity、fixture、対象固有名、期待terminal、Target評価または実装結果をpredicateへ使用しない。

## Adversarial audit criterion

本packet、一般仕様、Candidate175の現行promptだけから、次の一般反例が成立しないことを確認する。

1. 対象列挙、省略、open境界、名称またはreviewer仮説からrelation不在前提を補完する。
2. descriptorのD、R、O、snapshotまたはbasis arrayをrootまたはreviewerが後付けする。
3. 異subject、異domain、異relation、異objectまたは異snapshotのreceiptを一つのwitnessへ混ぜる。
4. receipt metadataと実際にbindしたmembershipまたはrelation factを取り違える。
5. 成立済みwitnessを無関係なmissing evidenceで失効させる。
6. 全descriptorを確認せず`no_counterexample_found`を受け入れる。
7. `not_applicable`または後付け証拠要求から任意の`unavailable`を作る。
8. Candidate175のmanifest descriptor、semantic projection、producer分離、permission前停止またはroot非代行を変える。
9. 新経路をrelation不在以外のpredicateへ拡張する。
10. case、fixture、期待結果または既知対象名による分岐を必要とする。

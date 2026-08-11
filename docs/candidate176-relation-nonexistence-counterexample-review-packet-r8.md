# Candidate176 relation nonexistence counterexample semantic design packet r8

## Packet scope

- source design identity: `candidate176-relation-nonexistence-counterexample-design-r8`
- direct parent prompt identity: `the-caption-3ce91a4-review-operation-admission-closure-r1`
- changed axis: fixed general designがboundary decisionの必要前提にしたrelation不在を、finite manifestの具体的witnessが直接反証する経路
- forbidden input: 実装、patch、Target評価、case、fixture、oracle、期待terminal、評価結果、先行reviewのfinding・disposition・修正方向、設計producerの反例予想

## Objective

Candidate173の規範矛盾経路を維持し、固定一般設計がboundary decisionの必要前提として明示した次の事実命題だけを新しい具体的反例経路へ追加する。

```text
relation_nonexistence_premise :=
  current snapshot Sについて
  scope Dに属しrelation Rでobject Oへ関係するsubjectは存在しない
```

許可済み成功観測が同じsnapshotで`x ∈ D ∧ R(x,O)`を直接bindし、対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要なら`counterexample_found`とする。別の望ましい扱いを定める規範predicateは要求しない。

本経路は単一値relation、基数、大小比較、状態遷移、stop / continue、fallback、同値性、same-treatment、先行固定列挙だけによる反証を扱わない。対象列挙、省略、open境界、名称またはreviewer仮説だけからrelation不在前提を作らない。

## 起動前assessment source set

rootはrelation不在前提を選別しない。review対象の全boundaryについて、boundary ledgerの`direct_basis`全entryと`counterexample_effect_basis`全entryを、元array、ordinal、identity、逐語値または改変不能な構造化値のまま次の有限集合へ射影する。

```yaml
assessment_source_set:
  - boundary_identity: <review対象boundary>
    direct_basis_entries:
      - source_role: direct_basis
        source_ordinal: <元array ordinal>
        source_identity: <source entry identity>
        source_value: <元entryの逐語値または構造化値>
    counterexample_effect_basis_entries:
      - source_role: counterexample_effect_basis
        source_ordinal: <元array ordinal>
        source_identity: <source entry identity>
        source_value: <元entryの逐語値または構造化値>
```

集合は全review対象boundaryを過不足・重複なく覆い、各arrayは元boundary ledgerと完全一致する。rootはentryを選択、要約、連結、分類または除外しない。

packetはCandidate175が起動前に固定した全対象boundary、全必須scope、finite evidence manifestの全descriptor、各observation identity・target・success condition、許可された契約・authority・semantic design field-valueを保持する。rootはmanifest項目を追加せず、reviewerも開始後にevidence scope、manifest observationまたはsource entryを追加しない。

## Reviewer premise assessment

独立reviewerは`assessment_source_set`の各`direct_basis` entryを一回ずつ判定し、次のいずれかを返す。

```yaml
premise_assessment:
  boundary_identity: <source set boundary>
  source_role: direct_basis
  source_ordinal: <source entry ordinal>
  source_identity: <source entry identity>
  source_value: <source entryの完全な値>
  assessment: applicable | not_applicable
  relation_nonexistence_statement: true | false
  boundary_decision_dependency: required | not_required
```

`applicable`は`relation_nonexistence_statement=true ∧ boundary_decision_dependency=required`の場合だけ許可する。対象列挙、省略、探索履歴、背景説明、open境界、名称示唆、または偽でも同じboundary decisionを維持できるentryは`not_applicable`とする。

rootはassessmentの意味を再判定せず、boundary、role、ordinal、identity、source value、sender identityが起動前source setへ完全一致することと列挙値の組合せだけを確認する。reviewerはsource entryを新設しない。

全`direct_basis` entryがassessmentを一件持つ。`counterexample_effect_basis`はpremise候補としてassessmentせず、後述するdesign effectの根拠集合として全件保持する。

## Applicable assessmentのrelation descriptor

reviewerは`assessment=applicable`としたentryについて、起動前packet内の値だけを参照して次を返す。

```yaml
relation_descriptor:
  boundary_identity: <assessment boundary>
  source_identity: <assessment source identity>
  domain_identity: <D>
  relation_identity: <R>
  object_identity: <O>
  snapshot_identity: <current snapshot S>
  membership_observation:
    observation_identity: <起動前manifest identity>
    target: <起動前target>
    success_condition: <起動前success condition>
  relation_observation:
    observation_identity: <起動前manifest identity>
    target: <起動前target>
    success_condition: <起動前success condition>
  relation_mapping_basis:
    - <sourceの命題とmanifest観測のD・R・O対応を直接bindする起動前contract / authority / semantic field identity>
```

D、R、O、snapshotはsource entryまたは同じboundaryへbindされた起動前semantic field-valueから得る。membershipとrelation observationは起動前manifest descriptorから選ぶ。`relation_mapping_basis`は、sourceの語と観測fieldが異なる場合に両者の対応を直接bindする起動前許可値を持つ。名称類似またはreviewerの常識だけで対応させない。

applicable assessmentについてD、R、O、snapshot、二つのobservationまたは必要なmapping basisを起動前packetからbindできない場合、reviewerはそのsource identityと不足する起動前fieldまたはobservation identityへbindした`unavailable`を返す。rootは値を補完しない。

`not_applicable` assessmentはrelation descriptor、witnessまたは不足証拠を持たない。

## Witness

reviewerはrelation descriptorが指定するmanifest observationだけを確認する。一つのobservationがmembershipとrelationの両方を直接bindできる場合、receiptは一件で二つのroleを持てる。

```yaml
witness:
  witness_identity: <review operation内で一意>
  boundary_identity: <relation descriptor boundary>
  source_identity: <relation descriptor source>
  subject_identity: <具体的x>
  domain_identity: <D>
  relation_identity: <R>
  object_identity: <O>
  snapshot_identity: <S>
  evidence_receipts:
    - observation_identity: <descriptor指定identity>
      target: <descriptor指定target>
      success_condition: <descriptor指定success condition>
      receipt_roles: [membership] | [relation] | [membership, relation]
      observed_subject_identity: <x>
      observed_domain_identity: <membership roleのD>
      observed_relation_identity: <relation roleのR>
      observed_object_identity: <relation roleのO>
      observed_snapshot_identity: <S>
      status: success
```

`relation_nonexistence_witness_established`は、assessmentが`applicable / true / required`でsource setへ完全一致し、relation descriptorの全参照が起動前packetへbindされ、witnessのboundary・source・D・R・O・snapshotがdescriptorへ一致し、membershipとrelationのsuccess receiptが同じsubjectについて`x ∈ D ∧ R(x,O)`をbindした場合に成立する。receipt集合は二つのobservationを欠落、余剰、重複なしで覆う。

さらに、対象boundaryの全`counterexample_effect_basis` entryを元ordinal、identity、値のままreviewer resultへ持ち、独立reviewerが一般設計変更を必要とすると判定する。rootはbasis arrayの完全一致だけを確認し、criterionを再判定しない。

## Counterexample and priority

```text
concrete_counterexample_established :=
  normative_counterexample_established
  ∨ relation_nonexistence_witness_established
```

いずれかが成立した時点で`counterexample_found`を終端結果とし、他source、他boundaryまたは別manifest項目のmissing、unreadable、non-success、receipt欠落で失効させない。

反例が成立しない場合だけ、全source assessmentと全applicable assessmentのrelation descriptor・manifest observationを確認する。applicable sourceの必須値または指定observationが不足すれば`unavailable`を返す。`not_applicable`、source不在、reviewerが後付けした要求は不足根拠にしない。

反例が成立せず、全source assessment、全applicable sourceのcoverage receipt、全対象boundary、全必須scope、起動前manifest全件のsuccess receiptが揃った場合だけ`no_counterexample_found`とする。

## Result schema

Candidate173の規範経路を変更しない。新経路の`counterexample_found`は一般仕様の共通fieldに加えて次を持つ。

```yaml
disposition: counterexample_found
counterexample_path: relation_nonexistence
design_identity: <fixed general design identity>
packet_identity: <delivered packet identity>
boundary_identity: <source boundary>
contract_basis:
  - <x、x ∈ D、R(x,O)を許すcontractまたは正本authority>
counterexample:
  - subject_identity: <x>
    domain_identity: <D>
    relation_identity: <R>
    object_identity: <O>
    snapshot_identity: <S>
premise_assessment: <全field>
relation_descriptor: <全field>
witness: <全field>
counterexample_effect_basis_entries: <対象boundaryの完全なarray>
design_effect:
  - <変更が必要な対象集合、一般条件、正本、所有、停止またはfallback>
```

rootは既存のdesign、packet、runtime receipt、sender照合に加え、source set、assessment、relation descriptorの全参照、witness、counterexample、effect basis arrayのidentity・ordinal・値を機械照合する。実行時subjectはwitness、receipt、counterexample間で一致させる。contract basisとdesign effectの意味はreviewer criterion resultとして保持し、rootは再判定しない。欠落、余剰、未知field、他経路field混入、不一致は結果を不受理にする。

`no_counterexample_found`は一般仕様のfieldに加えて次を持つ。

```yaml
relation_nonexistence_source_coverage:
  - premise_assessment: <source entryに対応する全field>
    relation_descriptor: <applicableなら全field、not_applicableならnull>
    evidence_receipts: <applicableなら指定observationの全success receipt、not_applicableなら空array>
```

coverageは起動前source setの全`direct_basis` entryと欠落、余剰、重複なしで一対一に完全一致する。applicable entryはdescriptor参照とreceipt集合を完全照合し、not_applicable entryはdescriptorをnull、receiptを空にする。一般仕様どおりmanifestの他の全項目にもsuccess receiptを要求する。

`unavailable`は反例不成立の場合だけ、applicable assessmentの起動前source identity、起動前packetの不足fieldまたは起動前manifest observation identityへbindする。not_applicableや後付け要求を根拠にしない。

## Parent control preservation

- Candidate175のreview要否、permission前停止、operation仕様、producer分離、finite manifest、semantic projection、packet identity、root非代行、general design admissionを維持する。
- assessment source、relation descriptor、witnessが参照できる値を起動前packet内の許可field-valueとmanifest descriptorへ限定する。
- rootは全sourceを射影し、review criterionを判定しない。reviewerはevidence scopeを拡張しない。
- Candidate173の規範矛盾経路と証拠負担を維持する。
- case、fixture、対象固有名、期待terminal、Target評価または実装結果をpredicateへ使用しない。

## Adversarial audit criterion

1. rootがpremise sourceを意味選別し、applicable sourceをcoverage外へ落とす。
2. reviewerがsource、D、R、O、snapshot、manifest observationまたはmapping basisを後付けする。
3. 対象列挙、省略、open境界、名称または背景説明をrelation不在前提へする。
4. 異subject、domain、relation、objectまたはsnapshotのreceiptを混ぜる。
5. 成立済みwitnessを無関係なmissingで失効させる。
6. 全sourceをassessmentせず`no_counterexample_found`を受け入れる。
7. not_applicableまたは後付け要求からunavailableを作る。
8. Candidate175のmanifest、semantic projection、producer分離、permission前停止またはroot非代行を変える。
9. relation不在以外のpredicateへ新経路を拡張する。
10. case、fixture、期待結果または既知対象名による分岐を必要とする。

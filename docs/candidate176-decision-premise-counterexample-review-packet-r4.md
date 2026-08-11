# Candidate176 decision premise counterexample semantic design packet r4

## Packet scope

- source design identity: `candidate176-decision-premise-counterexample-design-r4`
- direct parent prompt identity: `the-caption-3ce91a4-review-operation-admission-closure-r1`
- changed axis: fixed general designの明示的な判断前提を具体的事実が直接反証する経路
- allowed content: 本文のpredicate、schema、既存制御との関係、一般入力上の監査条件
- forbidden content: 実装、patch、Target評価、case、fixture、oracle、期待terminal、評価結果、先行reviewのfinding・disposition・修正方向、設計producerの反例予想

## Design objective

既存の規範矛盾経路を維持し、固定一般設計のboundary decisionを成立させる明示的な事実前提が、許可済みの具体的事実で直接否定された場合を`counterexample_found`へ追加する。

判断前提は、一般設計または境界台帳に明示され、対象boundaryの維持に必要で、review開始前にidentity、量化範囲、snapshot対応、証拠源を固定できる観測可能な事実命題だけとする。列挙、省略、名称またはreviewerが後から立てた仮説は`not_applicable`であり、`unavailable`の根拠にしない。

未知instance間の属性同値、区別属性不存在またはsame-treatmentを推論しない。普遍・排他命題そのものが明示されている場合だけ、その量化範囲に属する一件の具体例で命題を反証できる。

## Review起動前のdescriptor

```text
decision_premise_core_ready :=
  current general design identityまたはboundary ledgerが
    一つのboundary decisionを成立させる観測可能な事実命題を明示
  ∧ boundary identity、premise identity、source provenanceが固定済み
  ∧ premise predicate type、subject identity、predicate identity、期待値、
    量化範囲が固定済み
  ∧ premiseが偽なら対象boundaryを同じ一般条件のまま維持不能であることが
    direct_basisまたはcounterexample_effect_basisの非空identity集合へbind済み
  ∧ そのidentity集合を選択、連結または要約せず完全な
    boundary_dependency_basis_identitiesとして固定済み
  ∧ premise_snapshot_identityが固定済み
  ∧ observationまたは列挙事実との許容snapshot対応が
    equal | contained_current_snapshot | authority_declared_persistent
    の一つへ先行contractまたはauthorityからbind済み
```

descriptorの共通schemaは次とする。

```yaml
descriptor_identity: <packet内で一意なidentity>
boundary_identity: <boundary ledger identity>
premise_identity: <固定一般設計内の命題identity>
premise_provenance: <固定一般設計または境界台帳source identity>
premise_predicate_type: nonexistence | universal | boolean_relation | single_valued_relation | cardinality | terminal_transition
premise_subject_identity: <命題のsubject>
premise_predicate_identity: <relationまたはstate predicate>
premise_expected_value: <固定値または構造化条件>
premise_scope_identity: <量化範囲identity>
boundary_dependency_basis_identities:
  - <direct_basisまたはcounterexample_effect_basisのsource identity>
premise_snapshot_identity: <前提snapshot>
snapshot_relation: equal | contained_current_snapshot | authority_declared_persistent
snapshot_relation_basis_identity: <先行contract / authority identity>
evidence_source_kind: manifest_observation | prior_fixed_enumeration
```

`premise_predicate_type=single_valued_relation`はpredicateが同一subjectに一値だけを持つこと、`cardinality`はcount対象、比較演算子、閾値と計数domain、`terminal_transition`はfailure identity、判定phase、terminality、判定horizon、結果集合の相互排他性を、現在designより前のcontractまたはauthorityへbindする追加fieldを必須にする。これらをbindできない命題を対応済みdescriptorとしてreviewへ送らない。

具体的事実は全証拠源で次の共通schemaへ正規化せず直接bindする。sourceにこの構造がない場合、rootが語彙変換して生成せず、contractまたはauthorityがfield対応を直接定める場合だけ射影する。

```yaml
fact_identity: <source内で一意な事実identity>
subject_identity: <具体的subject>
predicate_identity: <relationまたはstate predicate>
object_or_value: <具体的object、valueまたは構造化状態>
scope_identity: <具体的事実のscope>
snapshot_identity: <具体的事実のsnapshot>
qualifiers:
  phase: <該当する場合のphase>
  terminality: <intermediate | terminal、該当する場合>
  horizon_identity: <該当する場合の判定horizon>
```

`contained_current_snapshot`は、前提が現在review対象snapshot全体の命題であり、具体的instanceがそのsnapshotと量化範囲へ属することを証拠receiptで確認できる場合だけ使う。`authority_declared_persistent`は、現在designより前のcontractまたはauthorityが前提または列挙事実の後続snapshotへの有効性を直接定める場合だけ使う。時系列順、最新という名称またはreviewerの判断では対応させない。

具体的事実の証拠源は次の型付き論理和とする。

```text
premise_evidence_source_kind :=
  manifest_observation | prior_fixed_enumeration

manifest_observation_descriptor_ready :=
  premise_evidence_source_kind=manifest_observation
  ∧ 起動前のfinite evidence manifestにobservation identity、target、success condition、
    observation snapshot identityとfact identity、具体的fact fieldのsource対応が固定済み
  ∧ premiseの量化範囲へのinstance membershipを必要とする場合、
    同じobservationまたは別の起動前manifest observationへmembership判定を固定済み

prior_fixed_enumeration_descriptor_ready :=
  premise_evidence_source_kind=prior_fixed_enumeration
  ∧ 現在design identityより前のcontractまたはauthority identityとprovenanceが固定済み
  ∧ 列挙項目identity、具体的fact identityと全fact field、適用scope、snapshot identityが固定済み
  ∧ 列挙項目がpremiseの量化範囲へ属することを同じcontract / authorityが直接bind

decision_premise_descriptor_ready :=
  decision_premise_core_ready
  ∧ (
      manifest_observation_descriptor_ready
      ∨ prior_fixed_enumeration_descriptor_ready
    )
```

一つのdescriptorは一つの`premise_evidence_source_kind`だけを持つ。同じ具体的事実について両方が利用可能でも、review operationは使用する一方を起動前に固定する。reviewerは証拠源を切り替えない。

rootはreview criterionを判定せず、一般設計、境界台帳、既存manifest、先行contract / authorityに明示された値だけを有限descriptorへ射影する。前提、量化範囲、snapshot対応、証拠源または必須観測を推測・補完・新設しない。

descriptorに必要な明示値が欠ける場合、その前提をreviewerへ渡して補完させず、一般設計またはreview operation仕様不足としてdispatch前に`unavailable`とする。一方、次の候補はdescriptor対象外の`not_applicable`であり、不足値を作らない。

- 一般設計が対象を列挙しただけで、非列挙対象の不存在または非適用を明示していない。
- 記載の省略、open境界、non-exhaustive validationまたはauthorityが領域を閉じないという負の情報だけである。
- identity、分類、contract、file、consumerまたはartifactの名称が関係を示唆するだけである。
- 背景説明、探索履歴、実装上の便宜、期待または判断に不要な補足である。
- 命題が偽でも、同じ対象集合、一般条件、正本、所有、停止またはfallbackを維持できる。

reviewerはreview開始後にdescriptor、必須scope、manifest項目または先行列挙項目を追加しない。

## 二つの反例predicate

```text
normative_counterexample_established :=
  許可済み成功観測または先行固定contract / authorityの明示列挙が
    具体的な入力、状態、consumer、成果物関係または失敗経路をbind
  ∧ contract_basisがそのinstanceへ適用する規範predicateを明示
  ∧ 固定一般設計の扱いが規範predicateと直接矛盾
  ∧ 対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要
```

規範経路はCandidate173から継承し、証拠負担を変えない。

```text
decision_premise_counterexample_established :=
  起動前に固定したdecision_premise_descriptor_ready
  ∧ descriptorで固定した証拠源から具体的事実をbind
  ∧ contract_basisが具体的入力、状態、consumerまたは関係を許すか、
    authorityがその具体的事実を正本として直接定める
  ∧ 具体的事実のtarget identity、relationまたはstate、scope、snapshotが
    descriptorの量化範囲とsnapshot対応へ直接bind
  ∧ 具体的事実がdescriptorの事実命題の論理的否定を直接充足
  ∧ 対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要
```

`manifest_observation`経路では、descriptorに固定した全必須observationのsuccess receiptを要求する。各receiptはobservation identity、target、success condition、具体的事実、snapshot identityをbindする。量化範囲へのmembershipが別observationなら、そのsuccess receiptも要求する。

`prior_fixed_enumeration`経路では、manifest observationまたはsuccess receiptを要求しない。descriptorに固定したcontract / authority identity、provenance、列挙項目identity、具体的事実、scope、snapshotをbindする列挙receiptを要求する。

判断前提経路の`contract_basis`は、具体的事実に表れた入力、状態、consumerまたは関係が契約上許されること、あるいはauthorityがその事実を正本として定めることを意味する。設計と異なる扱いを命じる規範predicateは不要である。review permission、allowed read、descriptor自身またはrootの説明を`contract_basis`にしない。

直接否定はdescriptorの`premise_predicate_type`ごとに、同一predicateまたは先行contract / authorityが対応を直接定めたpredicateについて次に限定する。

- `nonexistence`: `DにはPを満たす対象が存在しない`に対する`x ∈ D ∧ P(x)`。
- `universal`: `Dの全対象はPを満たす`に対する`x ∈ D ∧ ¬P(x)`。
- `boolean_relation`: 同一subject・objectの`relation=false`に対する`relation=true`、またはその逆。
- `single_valued_relation`: 同一subjectについてpredicateの単一値性が先行authorityで固定され、期待値`v1`に対して具体値`v2`が`v1 != v2`である。
- `cardinality`: 同一の閉じた計数domain、predicate、snapshotについて、具体的countが固定済み比較条件を満たさない。上限または不存在は条件を超える具体的member集合だけで反証できるが、下限未達は計数domainの閉包receiptを要求する。
- `terminal_transition`: 同一failure、入力、phase、terminal判定点、horizonについて、先行authorityが相互排他的と定める期待terminal outcomeと異なるterminal outcomeを観測する。intermediateなretry、continueまたはfallbackはterminal outcomeの否定にしない。

列挙外のpredicate typeまたは必須の単一値性、計数domain、phase、terminality、horizon、相互排他性を起動前にbindできない命題は、反例なしとして扱わずdescriptor構成不能とする。

語の類似、異なる抽象度の事実、単なる追加member、異なるscopeまたはsnapshot、より安全な設計の可能性は直接否定にしない。

```text
concrete_counterexample_established :=
  normative_counterexample_established
  ∨ decision_premise_counterexample_established
```

## 排他的な結果schema

共通fieldは次とする。

```yaml
disposition: counterexample_found
counterexample_path: normative | decision_premise
design_identity: <fixed general design identity>
packet_identity: <delivered packet identity>
boundary_identity: <refuted boundary>
contract_basis:
  - <具体的入力、状態または関係を許すcontract / authority>
counterexample:
  - <具体的な入力、状態、consumer、関係または失敗経路>
counterexample_facts:
  - fact_identity: <証拠receiptのfact identity>
    subject_identity: <具体的subject>
    predicate_identity: <具体的predicate>
    object_or_value: <具体的objectまたはvalue>
    scope_identity: <具体的scope>
    snapshot_identity: <具体的snapshot>
    qualifiers: <descriptorが要求するphase、terminality、horizon>
design_effect:
  - <変更が必要な対象集合、一般条件、正本、所有、停止またはfallback>
```

`counterexample_path=normative`は共通fieldに加えて次を必須にする。

```yaml
normative_predicate: <具体的instanceへ適用する規範predicate>
general_design_treatment: <固定一般設計の具体的扱い>
direct_contradiction_basis: <両者の直接矛盾>
```

この経路では`premise_identity`、`premise_provenance`、`boundary_dependency_basis_identities`、`premise_scope`、`premise_snapshot_identity`、`evidence_source_kind`、`observation_snapshot_identity`、`snapshot_relation`、`premise_evidence_receipts`、`prior_enumeration_receipt`を禁止する。

`counterexample_path=decision_premise`は共通fieldに加えて次を必須にする。

```yaml
premise_identity: <起動前descriptor identity>
premise_provenance: <固定一般設計または境界台帳source>
boundary_dependency_basis_identities:
  - <descriptorの完全な根拠identity集合>
premise_scope: <起動前descriptorの量化範囲>
premise_snapshot_identity: <起動前descriptorのsnapshot>
evidence_source_kind: manifest_observation | prior_fixed_enumeration
snapshot_relation: equal | contained_current_snapshot | authority_declared_persistent
```

`evidence_source_kind=manifest_observation`ではさらに次を必須にする。

```yaml
observation_snapshot_identity: <descriptorに固定した観測snapshot>
premise_evidence_receipts:
  - observation_identity: <起動前manifest identity>
    target: <起動前manifest target>
    success_condition: <起動前success condition>
    snapshot_identity: <観測snapshot>
    observed_fact: <共通fact schemaの全field>
    status: success
```

この証拠源では`prior_enumeration_receipt`を禁止する。

`evidence_source_kind=prior_fixed_enumeration`ではさらに次を必須にする。

```yaml
prior_enumeration_receipt:
  authority_identity: <起動前descriptorのcontract / authority>
  authority_provenance: <current designより前の固定証拠>
  enumeration_item_identity: <起動前descriptorの列挙項目>
  scope: <列挙項目のscope>
  snapshot_identity: <列挙項目のsnapshot>
  enumerated_fact: <共通fact schemaの全field>
```

この証拠源では`observation_snapshot_identity`と`premise_evidence_receipts`を禁止する。

`decision_premise`経路では`normative_predicate`、`general_design_treatment`、`direct_contradiction_basis`を禁止する。

## Result admission

rootは既存のdesign、packet、runtime input receipt、sender identity照合に加え、次を機械的に確認する。

```text
decision_premise_result_matches_descriptor :=
  result.boundary_identity == descriptor.boundary_identity
  ∧ result.premise_identity == descriptor.premise_identity
  ∧ result.premise_provenance == descriptor.premise_provenance
  ∧ result.boundary_dependency_basis_identitiesが
    descriptor.boundary_dependency_basis_identitiesと欠落・余剰・重複なしで完全一致
  ∧ result.premise_scope == descriptor.premise_scope
  ∧ result.premise_snapshot_identity == descriptor.premise_snapshot_identity
  ∧ result.evidence_source_kind == descriptor.evidence_source_kind
  ∧ result.snapshot_relation == descriptor.snapshot_relation
  ∧ 経路別必須fieldが全件存在
  ∧ 経路別禁止fieldが全件不在
```

`manifest_observation`では、各`premise_evidence_receipt`のobservation identity、target、success condition、snapshot identity、observed factの全fieldがdescriptorと起動前manifestの対応項目へ一対一に完全一致し、未知、余剰、欠落、重複がなく、全件`status=success`であることを要求する。`contained_current_snapshot`では、具体的instanceの量化範囲membershipをbindするdescriptor指定receiptも同じ完全一致集合へ含める。

`prior_fixed_enumeration`では、`prior_enumeration_receipt`のauthority identity、provenance、enumeration item identity、scope、snapshot identity、enumerated factの全fieldがdescriptorへ全件完全一致することを要求する。

全経路で`counterexample_facts`は使用したobserved factまたはenumerated factとfact identityを含む全fieldが完全一致し、自由記述の`counterexample`も同じ具体的事実を指すことを要求する。不一致なら結果を不受理にし、rootが書き換えない。

`normative`では、明示fieldの規範predicate、一般設計の扱い、直接矛盾、contract basis、具体的instance、design effectがCandidate173のpredicateへbind可能であることを要求する。

rootは値を生成、正規化、経路変更または再解釈しない。不一致、欠落、余剰、未知fieldまたは禁止field混入は結果を不受理にし、rootの説明で補完しない。

## Disposition priority

```text
all_decision_premise_evidence_complete :=
  packet内の全decision premise descriptorについて
    evidence_source_kind=manifest_observationなら
      descriptor指定の全observation success receiptが一対一に完全一致
    evidence_source_kind=prior_fixed_enumerationなら
      descriptor指定のprior enumeration receiptが一対一に完全一致
```

reviewerは`no_counterexample_found`または反例不成立を返す前に、全descriptorの証拠を確認する。`no_counterexample_found` resultは全descriptor identityと各経路別receiptを`decision_premise_review_receipts`へ一対一に持ち、rootはpacketのdescriptor集合と欠落・余剰・重複なしで完全一致することを要求する。

いずれかの反例経路が成立し、経路別必須証拠が全て揃った場合は`counterexample_found`を終端結果とし、無関係な後続manifest項目のmissing、unreadable、non-successまたはreceipt欠落で失効させない。

`manifest_observation` descriptorが反証判定に必須として起動前固定したobservationにmissing、unreadable、non-successまたはreceipt欠落がある場合は、そのobservation identityへbindした`unavailable`を必ず返す。`prior_fixed_enumeration` descriptorの列挙receiptが不足する場合も、そのauthorityまたは列挙項目identityへbindした`unavailable`を必ず返す。いずれも証拠不足のまま`no_counterexample_found`へ進まない。

descriptorが存在しない候補、または`not_applicable`は`unavailable`の根拠にしない。reviewerが開始後に作ったdescriptor、scope、manifestまたは列挙項目の不足も根拠にしない。

具体的反例が成立せず、`all_decision_premise_evidence_complete=true`であり、全対象boundary、必須scope、起動前manifest全件のsuccess receiptが揃った場合だけ`no_counterexample_found`とする。三つのdispositionの順序はCandidate173を維持する。

## Existing control preservation

- Candidate175のreview要否、permission前停止、operation仕様、producer分離、allow-list semantic projection、packet identity、root非代行、general design admissionを維持する。
- descriptorは許可field-valueとprovenance receiptだけから起動前に構築し、forbidden inputを含むsource artifact全体を配送しない。
- Candidate173の規範矛盾経路、非対称な証拠負担、成立済み反例と無関係missingの優先順位を維持する。
- Candidate174の属性signature、区別domain閉包またはsame-treatment推論を導入しない。
- case identity、fixture、対象固有名、期待terminal、Target評価または実装結果をpredicateへ使用しない。

## Adversarial audit criterion

本packetと一般仕様、Candidate175の現行promptだけから、次の一般反例が成立しないことを確認する。

1. 非明示の前提候補が`unavailable`を作る。
2. reviewerが開始後に必須証拠、scope、snapshot対応または証拠源を追加・変更する。
3. 先行固定列挙だけで反証できる入力へmanifest receiptを要求する、または観測経路でsuccess receiptを省略する。
4. 経路固有fieldの欠落、余剰、混入またはdescriptor不一致を受け入れる。
5. 異scope、異snapshot、異relationの事実を直接否定へ使う。
6. 普遍命題の反証へdomain全体の閉包を要求する、または未知instance間の同値性を推論する。
7. 成立済み反例を無関係なmanifest欠落で失効させる。
8. Candidate175のoperation admission、producer分離、semantic projection、permission前停止またはroot非代行を変える。
9. case、fixture、期待結果または既知対象名による分岐を必要とする。

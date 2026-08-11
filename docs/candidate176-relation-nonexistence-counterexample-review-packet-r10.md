# Candidate176 relation nonexistence counterexample semantic design packet r10

## Scope

- source design identity: `candidate176-relation-nonexistence-counterexample-design-r10`
- direct parent prompt identity: `the-caption-3ce91a4-review-operation-admission-closure-r1`
- changed axis: 一般設計がboundary decisionの必要前提にしたrelation不在を、同一snapshotの具体的witnessが反証する経路
- forbidden input: 実装、patch、Target評価、case、fixture、oracle、期待terminal、評価結果、先行review、設計producerの反例予想

Candidate173の規範矛盾経路は変更しない。新経路は`relation_nonexistence`だけを扱い、単一値、基数、順序、状態遷移、stop / continue、fallback、同値性、same-treatment、先行列挙だけの反証へ拡張しない。

## 一般設計が固定するpremise registry

一般設計producerはreview要否判定前に、各boundary decisionの成立に使用する観測可能な事実前提を、一般設計identityの一部として`fact_premise_registry`へ固定する。これはreview findingではなく、設計producer自身が現在設計の依存前提を開示する設計要素である。

```yaml
fact_premise_registry:
  - premise_identity: <general design内で一意>
    boundary_identity: <boundary ledger identity>
    premise_type: relation_nonexistence | other_fact_premise
    formal_claim:
      quantifier: no_subject_exists
      domain_identity: <D>
      relation_identity: <R>
      object_identity: <O>
      snapshot_identity: <S>
    source_references:
      - source_path_identity: <semantic designまたはboundary ledger内path>
        source_ordinal: <該当する場合のordinal>
        source_identity: <source value identity>
        source_value: <逐語値または改変不能な構造化値>
    boundary_dependency_references:
      direct_basis_entries: <boundary ledgerの全entryをordinal・identity・値付きで完全複製>
      counterexample_effect_basis_entries: <同上>
```

`premise_type=relation_nonexistence`だけが新経路の候補になる。formal claimは複数source referenceを持てるが、一つの`no_subject_exists(D,R,O,S)`へ曖昧なく縮約され、論理和、条件分岐または別の否定を含まない。`other_fact_premise`は本Candidateでは反例predicateへ追加しない。

一般設計producerは、semantic designの全leaf field-valueと全boundary ledgerの`direct_basis` / `counterexample_effect_basis` entryを、path、ordinal、identity、値付きの`design_source_universe`へ全件固定する。各sourceは、少なくとも一つのpremiseの`source_references`へ含まれるか、`non_premise_source`として分類理由を持つ。

```text
fact_premise_registry_ready :=
  全review対象boundaryがregistryへ存在
  ∧ design_source_universeがsemantic designとboundary ledgerの対象sourceへ
    欠落・余剰・重複なしで完全一致
  ∧ universeの全sourceがpremise referenceまたはnon_premise_sourceへ一対一にcoverage
  ∧ 各premiseのboundary dependency reference arrayが元ledgerと完全一致
```

rootは自分が作成した一般設計のregistryをpacketへ射影できるが、reviewerのassessmentまたはwitnessを生成しない。registry不足は`general_design_ready=false`としてreviewを起動せず`unavailable`とする。既に固定された一般設計からreview packetを作る段階でregistryを後付けしない。

## Review operation admissionへの追加

Candidate175の`review_operation_spec_ready`と`semantic_projection_valid`へ次を追加する。

```text
relation_premise_review_inputs_ready :=
  fact_premise_registry_ready
  ∧ registry identityとdesign source universe identityが固定済み
  ∧ immutable review snapshot identityがruntime input receiptへ固定済み
  ∧ finite evidence manifestの全descriptorが同じsnapshot identityまたは
    同一内容snapshotを証明するdigest / transaction identityへbind済み
```

falseならoperation作成・配送前に`unavailable`とする。snapshot identityは自己申告ラベルではなく、commit、content digest、一貫read transactionまたは同等の不変provenanceへbindする。各観測receiptは同じ不変provenanceを持つ。

packetはCandidate175の許可field-valueだけから新規構築し、registry、source universe、全boundary、全必須scope、finite manifest全descriptor、contract / authority、許可semantic field-valueを含む。forbidden source全体を配送しない。

## Reviewer phase 1: observation前commit

独立reviewerはmanifest targetを一件も読む前に、次を一つの`premise_commit_receipt`へ固定する。

1. design source universeの全sourceとregistry coverageを確認する。
2. 全premiseを`applicable | not_applicable | descriptor_unavailable`へ分類する。
3. 全manifest descriptorを各applicable premiseについて`relevant | not_relevant`へ分類する。
4. relevant descriptorからD membershipとR(x,O)を観測する完全なdescriptor集合を固定する。

```yaml
premise_commit_receipt:
  design_identity: <fixed design>
  packet_identity: <delivered packet>
  registry_identity: <起動前registry>
  design_source_universe_identity: <起動前universe>
  review_snapshot_identity: <immutable snapshot>
  source_coverage: <全sourceの過不足・重複なしcoverage>
  premise_assessments:
    - premise_identity: <registry premise>
      boundary_identity: <registry boundary>
      assessment: applicable | not_applicable | descriptor_unavailable
      relation_nonexistence_statement: true | false
      boundary_decision_dependency: required | not_required
      registry_matches_sources: true | false
      unavailable_inputs: <不足する起動前field identity、なければ空>
  manifest_relevance:
    - premise_identity: <applicable premise>
      manifest_descriptor_identity: <起動前manifest descriptor>
      relevance: relevant | not_relevant
      relevance_basis_identities: <起動前packet内のsource / contract / authority identities>
      observation_roles: [] | [membership] | [relation] | [membership, relation]
  manifest_read_count_at_commit: 0
```

`applicable`はregistryとsourceが一致し、formal claimが一つの`no_subject_exists(D,R,O,S)`で、boundary dependencyがrequiredの場合だけ許可する。対象列挙、省略、背景説明、open境界、名称、論理和、別predicate、または偽でも同じboundaryを維持できるものは`not_applicable`とする。

relation不在前提は成立するがD、R、O、snapshot、source対応または観測完全集合を起動前packetから固定できない場合は`descriptor_unavailable`とする。これを理由にreadyな別premiseの観測を止めない。

manifest relevanceは起動前manifest全descriptorを各applicable premiseについて一件ずつ分類する。関連descriptorの一部だけを選ばない。単一descriptorがD全域を網羅するとする場合、そのsuccess conditionまたは起動前authorityが全域coverageを直接定める必要がある。

commit receiptはproducerのoperation traceで最初のmanifest read invocationより前にterminalになり、runtime sequence receiptへbindされる。commit後にassessment、relevance、role、D、R、O、snapshotまたはmappingを変更しない。

## Reviewer phase 2: ready observation

reviewerは`assessment=applicable`で、必要なrelevant descriptor集合が固定できた全premiseを観測する。`descriptor_unavailable`は不足を保持するが、ready premiseの観測を妨げない。

各観測receiptは、observation identity、target、success condition、不変snapshot provenance、role、観測したsubjectのauthority identity・namespace identity・immutable object identity、D、R、Oをbindする。異namespaceのlocal name一致を同一subjectにしない。aliasは起動前authorityにより同一objectを直接bindしpremise commitで選択済みの場合だけ使う。

```text
relation_nonexistence_witness_established :=
  premise assessment=applicable
  ∧ premise commitが観測前sequence receiptへbind
  ∧ relevantなmembership / relation descriptorのsuccess receiptが
    同じimmutable subject identityについてx ∈ D ∧ R(x,O)をbind
  ∧ 全receiptがformal claimと同じD、R、O、不変snapshot provenanceへ一致
  ∧ reviewerが一般設計変更を必要と判定
```

## Disposition priority

1. phase 1の全source coverageと全premise assessmentを完了する。
2. phase 2で一件でもwitnessが成立したら`counterexample_found`。他premiseまたはmanifestの不足で失効させない。
3. witnessがなく、`descriptor_unavailable`またはapplicable premiseのrelevant observationにmissing、unreadable、non-success、receipt欠落があれば`unavailable`。
4. witnessがなく、全premise coverage、全applicable premiseの全relevant observation、全対象boundary、全必須scope、起動前manifest全件がsuccessなら`no_counterexample_found`。

`not_applicable`は不足証拠ではない。reviewerが開始後に作ったsource、premise、mapping、manifest descriptorまたは観測要求は`unavailable`の根拠にしない。

## Result schema

Candidate173の規範経路は変更しない。新経路の`counterexample_found`は一般仕様の共通fieldに加えて次を持つ。

```yaml
disposition: counterexample_found
counterexample_path: relation_nonexistence
design_identity: <fixed design>
packet_identity: <delivered packet>
boundary_identity: <premise boundary>
contract_basis: <具体的x、membership、relationを許すcontract / authority>
counterexample:
  - subject_identity: <authority / namespace / immutable object identity>
    domain_identity: <D>
    relation_identity: <R>
    object_identity: <O>
    snapshot_provenance_identity: <immutable snapshot>
premise_identity: <registry premise>
formal_claim: <registryの完全なclaim>
premise_commit_receipt: <全field>
witness_receipts: <使用した全success receipt>
counterexample_effect_basis_entries: <registryとledgerへ完全一致するarray>
design_effect: <変更が必要な対象集合、一般条件、正本、所有、停止またはfallback>
```

`no_counterexample_found`は一般仕様のfieldに加え、同じpremise commit receiptと、全applicable premiseについて全relevant descriptorのsuccess receiptを一対一に持つ。registryのpremise集合、source universe、manifest relevance集合と欠落・余剰・重複なしで完全一致する。

`unavailable`は同じpremise commit receiptを持ち、witness不成立の場合だけ、commit済み`descriptor_unavailable`の入力identityまたはrelevant observationの不足identityへbindする。

rootはdesign、packet、runtime receipt、sender、registry、source universe、premise commitのsequence receipt、manifest relevance、witness receiptのidentity・値・集合一致だけを確認する。reviewerのsemantic assessment、relevance、contract basisまたはdesign effectを再判定しない。不一致、欠落、余剰、重複、未知field、他経路field混入を補完しない。

## Parent preservation

- Candidate175のreview要否、permission前停止、producer分離、finite manifest、allow-list projection、packet identity、root非代行、general design admissionを維持する。
- 追加するregistry、source universe、immutable snapshot、phase 1 commitは新経路に必要なreview operation inputとしてCandidate175のadmissionへ明示的に結び付ける。
- reviewerは起動前packet外へevidence scopeを拡張しない。
- case、fixture、対象固有名、期待terminal、Target評価または実装結果をpredicateへ使用しない。

## Adversarial audit criterion

1. registryまたはsource universeからpremiseを落としてcoverageを通す。
2. 不足premiseがready premiseのwitness観測を遮断する。
3. manifestの一部分だけをrelevantとしてwitnessを見逃す。
4. assessment、mappingまたはdescriptorを観測後に選ぶ。
5. 異subject、namespace、D、R、Oまたは実体snapshotのreceiptを混ぜる。
6. 複合論理式を一つのrelation不在へ縮約する。
7. 成立済みwitnessを無関係missingで失効させる。
8. 全source、premise、manifest relevanceを確認せずno_counterexample_foundを受け入れる。
9. Candidate175のsemantic projection、producer分離、permission前停止またはroot非代行を変える。
10. relation不在以外またはcase固有の分岐へ拡張する。

# Candidate176 decision premise counterexample semantic design packet r13

## Scope

- source design identity: `candidate176-decision-premise-counterexample-design-r13`
- direct parent prompt identity: `the-caption-3ce91a4-review-operation-admission-closure-r1`
- changed axis: 明示規範predicateとは別に、固定一般設計の必要前提を許可済み具体的事実が直接反証する経路
- forbidden input: 実装、patch、Target評価、case、fixture、oracle、期待terminal、評価結果、先行review、設計producerの反例予想

Candidate175のreview operation、finite manifest、semantic projection、producer分離、permission前停止、result admission、root非代行を維持する。Candidate173の規範矛盾経路も変更しない。本Candidateはreviewerの反例criterionへ一つの代替経路を追加するだけで、新しいevidence source、manifest、registry、read順序または一般設計schemaを作らない。

## Predicate

```text
normative_counterexample_established :=
  Candidate173から継承する規範predicateとの具体的矛盾

decision_premise_counterexample_established :=
  fixed general designまたは対象boundary ledgerの許可済みsemantic valueが
    boundary decisionを同じ一般条件で維持するために必要な観測可能な事実命題を明示
  ∧ reviewerがその命題のsource identityと逐語値または改変不能な構造化値を直接引用
  ∧ 一件以上のfact supportが共同で具体的な入力、状態、consumer、
    成果物関係または失敗経路をbind
  ∧ 各fact supportは次のいずれか一つへ排他的にbind
    - Candidate175の起動前finite manifestに固定された許可済み成功観測
    - packet内の、現在designより前に固定されたcontract / authorityの明示列挙
  ∧ manifest supportでは観測receiptと前提が同じreview runtime input snapshotへbind
  ∧ 先行固定列挙supportではsource identity・改変不能値・provenance・
    前提snapshotへの適用性がpacket内のcontract / authorityへbind
  ∧ 観測された具体的事実が、語彙の推測または未知対象の補完を使わず、
    明示前提の論理的否定を直接充足
  ∧ 対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要

concrete_counterexample_established :=
  normative_counterexample_established
  ∨ decision_premise_counterexample_established
```

判断前提は、一般設計またはboundary ledgerの許可済みsemantic valueに明示された命題に限定する。reviewerは、対象列挙、省略、open境界、non-exhaustive validation、authorityが領域を閉じないこと、名称、背景説明、探索履歴または「より安全な設計が可能」という理由から前提を新設しない。

命題が偽でも同じboundary decisionを維持できる場合は必要前提ではない。一般設計またはledgerに明示されていない必要前提を推測しない。明示前提を確認できないことはmissing evidenceではなく、この代替経路が`not_applicable`であることを意味する。

直接否定は、前提と観測が同じsubject、domain、relationまたはstate、object、適用時点を指す場合に限る。異なる抽象度、異なるscope、異なるsnapshot、語の類似だけで対応付けたrelation、単なる追加member、未知の区別属性不存在、same-treatmentまたは同値性を使わない。前提と観測の語彙対応が同一でない場合、起動前packet内のcontractまたはauthorityがその対応を直接定める場合だけ使用する。

普遍または排他命題は、量化範囲へ属する一件の具体的instanceが否定条件を満たせば反証できる。この一件反証にdomain全体の閉包を要求しない。一方、量化範囲へのinstance所属と否定relationは許可済み成功観測へbindする。

review runtime input snapshotは、Candidate175のruntime input receipt、delivered packet identity、manifest observation receiptへ同一operation identityとしてbindする。異operation、先行result、別packetまたは別snapshotのreceiptを混ぜない。manifest経路でsnapshot対応を確認できない場合は反例を成立させず、起動前manifest observationのidentity不一致またはreceipt不足として`unavailable`へ結び付ける。

先行固定列挙経路は新しいreadを発行せず、packetへsemantic projection済みのcontract / authority値だけを使う。現在designより前のidentityとprovenance、列挙した具体的事実、前提が対象とするsnapshotへの適用性が直接bindされる場合だけ使う。authority名、過去に存在しただけの値、snapshot適用性の推測またはreviewerの一般知識を使わない。

## Reviewer responsibility

独立reviewerが、明示前提か、boundary decisionの必要条件か、観測事実が直接否定か、一般設計変更が必要かを判定する。rootはこのcriterionを代行、再実施または意味再判定しない。

reviewerはCandidate175のpacketとallowed readだけを使う。source identity、source value、boundary dependency basis、concrete fact、receipt、snapshot、direct contradiction、design effectをresultへbindする。新しいmanifest observation、allowed read、contract、authorityまたは前提を追加しない。

## Disposition priority

1. reviewerは許可済み成功観測または先行固定contract / authorityの明示列挙から、二つの反例経路を先に判定する。
2. いずれかが成立したら`counterexample_found`を終端結果とし、後続または別manifest項目のmissing、unreadable、non-success、receipt欠落で失効させない。
3. 反例が成立しない場合だけ、起動前manifestにmissing、unreadable、non-successまたはreceipt欠落があれば`unavailable`。
4. 反例が成立せず、全対象boundary、全必須scope、起動前manifest全件のsuccess receiptが揃えば`no_counterexample_found`。

reviewerが考えた非明示の前提候補、追加scopeまたは追加証拠の不足は`unavailable`の根拠にしない。

## Result schema and admission

規範経路のresultはCandidate173を維持する。判断前提経路の`counterexample_found`は一般仕様の共通fieldに次を追加する。

```yaml
disposition: counterexample_found
counterexample_path: decision_premise
design_identity: <fixed general design identity>
packet_identity: <delivered packet identity>
boundary_identity: <refuted boundary identity>
contract_basis:
  - <具体的入力、状態、consumerまたは関係を許すcontract / authority>
counterexample:
  - <具体的な入力、状態、consumer、関係または失敗経路>
premise_source_identity: <fixed designまたはledger内source identity>
premise_source_value: <逐語値または改変不能な構造化値>
boundary_dependency_basis:
  - <fixed design / ledger内の直接根拠identityと値>
fact_supports:
  - support_identity: <result内で一意>
    source_kind: manifest_observation | prior_fixed_enumeration
    manifest_observation:
      observation_identity: <起動前manifest identity>
      target: <起動前target>
      success_condition: <起動前success condition>
      runtime_input_snapshot_identity: <当該review operation snapshot>
      concrete_fact: <観測された具体的事実>
      status: success
    prior_fixed_enumeration:
      source_identity: <packet内contract / authority identity>
      source_value: <具体的事実を列挙する改変不能値>
      source_provenance: <current designより前の固定証拠>
      snapshot_applicability: <前提snapshotへの適用性を直接定める値>
      concrete_fact: <列挙された具体的事実>
direct_contradiction: <premiseとconcrete factの直接否定関係>
design_effect:
  - <変更が必要な対象集合、一般条件、正本、所有、停止またはfallback>
```

`fact_supports`は一件以上とし、各`support_identity`は重複しない。各supportで`source_kind=manifest_observation`なら`manifest_observation`を必須、`prior_fixed_enumeration`を禁止する。`source_kind=prior_fixed_enumeration`ならその逆とする。同じ具体的instanceを複数supportで扱う場合は、packet内のidentityまたはauthorityが同一instanceであることを直接bindする。

rootは既存のdesign、packet、runtime input receipt、sender照合に加え、premise source identityとvalue、boundary dependency basis、fact supportsの非空性とidentity一意性を確認する。各manifest supportではobservation identity・target・success condition・runtime input snapshot identityがdelivered packetと起動前manifestへ存在し一致することを確認する。各先行固定列挙supportではsource identity・value・provenance・snapshot applicabilityがdelivered packetへ存在し一致することを確認する。`counterexample`と各`concrete_fact`が共同で同じ具体的反例を構成するかはreviewer criterion resultとして保持する。

rootはpremiseが必要前提か、factが論理的否定か、contract basisまたはdesign effectが正しいかを再判定しない。不足field、identity不一致、packet外source、manifest外observation、別operation / snapshot receipt、禁止入力混入を説明で補完しない。

`no_counterexample_found`と`unavailable`のschema・受入条件はCandidate175を変更しない。非明示premise候補のcoverage receiptを追加要求しない。

## Parent preservation

- Candidate175の`review_operation_spec_ready`、`semantic_projection_valid`、`review_operation_admission_closed`を変更しない。
- finite manifestの全件成功を`no_counterexample_found`に要求し、具体的反例成立後だけ無関係な残件を不要にする。
- rootはpacket構築と結果のidentity bindingだけを行い、review criterionを実施しない。
- permission否定時はoperation、producer、packetを作成しない。
- case、fixture、対象固有名、期待terminal、Target評価または実装結果をpredicateへ使用しない。

## Adversarial audit criterion

1. 非明示の前提、列挙、省略、open境界または名称から偽の反例を作れる。
2. 明示された必要前提を具体的成功観測が直接否定しても反例にできない。
3. 異scope、異snapshot、異operationまたは語彙推測のfactを混ぜられる。
4. 非明示premise候補から任意の`unavailable`を作れる。
5. 成立済み反例を無関係なmanifest欠落で失効させる。
6. rootがreviewerのsemantic criterionを代行しなければresult admissionできない。
7. Candidate175のoperation admission、semantic projection、producer分離またはpermission前停止を変える。
8. case固有の分岐を必要とする。

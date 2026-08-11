# Candidate176 設計判断前提の反証設計 第2版

> **状態**: 第2版。情報封鎖敵対的レビューで反例を確認したためreject。実装へ使用しない。

## 結論

Candidate176はCandidate175を直接親とし、固定一般設計の判断を成立させる明示的な事実前提が、許可済みの具体的事実で直接否定された場合を`counterexample_found`へ加える一軸の改訂とする。

Candidate173の規範矛盾経路は維持し、二つの反例経路を型付き論理和として扱う。判断前提経路は、一般設計または境界台帳に明示され、対象境界の維持に必要で、review開始前にidentity・量化範囲・snapshot対応を固定できる事実命題だけを対象にする。列挙、省略、名称またはreviewerが後から立てた仮説は`not_applicable`であり、証拠不足を理由とする`unavailable`を発生させない。

## Identity

- candidate number: Candidate176
- design identity: `candidate176-decision-premise-counterexample-design-r2`
- prompt identity: `the-caption-3ce91a4-decision-premise-counterexample-r1`
- direct parent: `the-caption-3ce91a4-review-operation-admission-closure-r1`（Candidate175）
- changed target: root `AGENTS.md`
- changed axis: 明示規範への違反とは別に、設計判断を支える固定事実前提の具体的反証を判定する経路
- evaluation status: `design_not_audited / not_implemented / not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

初版`candidate176-decision-premise-counterexample-design`は、根拠のない前提候補が`unavailable`を作れること、結果形式が規範経路だけへ寄っていたこと、snapshot対応を起動前に固定していなかったことからrejectした。本設計は新identityであり、初版を実装しない。

Candidate174の同値性案は継承しない。二つのinstanceの属性一致、未知の区別属性またはsame-treatmentを推論せず、現在設計自身が明示した事実命題だけを反証対象にする。

## 作成前gate

1. 基準プロンプトはCandidate175の固定バンドル`251afdef36802c6ea3f2c4def3616288fa9054a22c028896c16418ba3e8a5061`とする。
2. Candidate175のreview要否、permission前停止、review operation仕様、明示producer binding、allow-list semantic projection、packet identity、三つのdisposition、一般設計admissionは変更しない。
3. Candidate173の規範矛盾経路は、具体的instanceへ適用される規範predicateを必要とする。このため、設計判断が必要前提とする現在状態、consumer関係、所有関係、成果物関係または失敗到達性を具体的事実が直接否定しても、別の規範predicateがなければ反例にならない解釈が残る。
4. 変更軸は`decision_premise_counterexample_established`の追加だけとし、既存経路との型付き論理和で`concrete_counterexample_established`を構成する。
5. review開始前に、一般設計に明示された判断前提だけを有限な`decision_premise_descriptor_set`へ射影する。descriptorのない境界へreviewerが前提候補を新設しない。
6. 各descriptorへ前提identity、provenance、対象boundary、命題、量化範囲、設計判断への依存、前提snapshot identity、許容する観測snapshot対応、反証判定に必須なmanifest observation identityを固定する。
7. descriptorが存在しない候補は`not_applicable`として捨て、manifest全件成功時の`no_counterexample_found`を妨げない。descriptorが固定済みで、その反証判定に必須な観測が失敗した場合だけ`unavailable`にできる。
8. 反例結果は`normative`と`decision_premise`の経路別必須項目へbindする。判断前提経路でも一般仕様の`contract_basis`を保持するが、ここでは具体的入力・状態・関係を許す契約またはauthorityを意味し、望ましい扱いを定める別の規範predicateは要求しない。
9. 固定済みADR9 r2とStandard14は変更しない。情報封鎖した設計監査を通過した後だけ実装し、ADR9各N=5を先に実行する。全件通過した場合だけStandard14各N=5を実行する。

## 起動前に固定する判断前提descriptor

```text
decision_premise_descriptor_ready :=
  current general design identityまたはそのboundary ledgerが
    一つのboundary decisionを成立させる観測可能な事実命題を明示
  ∧ premise identityとsource provenanceが固定済み
  ∧ premiseのsubject、relationまたはstate、量化範囲が固定済み
  ∧ premiseが偽なら対象boundaryを同じ一般条件のまま維持不能であることが
    direct_basisまたはcounterexample_effect_basisへbind済み
  ∧ premise_snapshot_identityが固定済み
  ∧ observation snapshotとの許容対応が
    equal | contained_current_snapshot | authority_declared_persistent
    の一つへ先行contractまたはauthorityからbind済み
  ∧ 反証を判定するために既存review manifestのどのobservation identityが必須か固定済み
```

`contained_current_snapshot`は、前提が現在review対象snapshot全体についての命題であり、観測対象がそのsnapshotへ属することをreceiptで確認できる場合だけ使う。`authority_declared_persistent`は、前提が後続snapshotでも有効であることを現在設計より前のcontractまたはauthorityが直接定める場合だけ使う。単なる時系列順、最新であること、名称一致またはreviewerの判断でsnapshotを対応させない。

rootはreview criterionを判定せず、一般設計と境界台帳に明示された値を有限descriptorへ射影する。前提を推測、補完または評価しない。起動前のdescriptorはCandidate175の許可field-valueとしてpacketへ追加し、そのprovenance receiptを付ける。descriptorの構成に必要な明示値が欠ける場合、その前提をreviewerへ推測させず、一般設計またはreview operation仕様の不足としてdispatch前に`unavailable`とする。

次はdescriptorにしない。

- 一般設計が対象を列挙しただけで、非列挙対象の不存在または非適用を明示していない。
- 記載の省略、open境界、non-exhaustive validationまたはauthorityが領域を閉じていないという負の情報だけである。
- identity、分類、contract、file、consumerまたはartifactの名称が関係を示唆するだけである。
- 背景説明、探索履歴、実装上の便宜、期待または判断に不要な補足である。
- 命題が偽でも、同じ対象集合、一般条件、正本、所有、停止またはfallbackを維持できる。

descriptorにしない候補は`decision_premise_candidate_state=not_applicable`とする。`not_applicable`はmissing evidenceではなく、`unavailable`を発生させない。reviewerはreview開始後に新しいdescriptor、必須scopeまたはmanifest項目を追加しない。

## 二つの反例経路

### 規範矛盾

```text
normative_counterexample_established :=
  許可済み成功観測または先行固定contract / authorityの明示列挙が
    具体的な入力、状態、consumer、成果物関係または失敗経路をbind
  ∧ contract_basisがそのinstanceへ適用する規範predicateを明示
  ∧ 固定一般設計の扱いが規範predicateと直接矛盾
  ∧ 対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要
```

これはCandidate173から継承し、証拠負担を変えない。

### 判断前提の具体的反証

```text
decision_premise_counterexample_established :=
  起動前に固定したdecision_premise_descriptor_ready
  ∧ 許可済み成功観測または先行固定contract / authorityの明示列挙が
    具体的な入力、状態、consumer、成果物関係または失敗経路をbind
  ∧ contract_basisがその具体的入力、状態または関係を許す
  ∧ success receiptが具体的事実のtarget identity、relationまたはstate、
    observation snapshot identityをbind
  ∧ descriptorに固定した量化範囲とsnapshot対応へ具体的事実を直接bind可能
  ∧ 具体的事実がdescriptorの事実命題の論理的否定を直接充足
  ∧ 対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要
```

判断前提経路の`contract_basis`は、具体的事実に表れた入力、状態、consumerまたは関係が契約上許されること、あるいはauthorityがその事実を正本として定めることをbindする。設計と異なる扱いを命じる規範predicateは不要である。単なるreview permission、allowed read、descriptor自身またはrootの説明を`contract_basis`へ代入しない。

`論理的否定を直接充足`は、同一relationまたは先行authorityが直接対応を定めたrelationについて次の形に限定する。

- `domain DにはPを満たす対象が存在しない`に対する`x ∈ D ∧ P(x)`。
- `domain Dの全対象はPを満たす`に対する`x ∈ D ∧ ¬P(x)`。
- `artifact Aはconsumer domain Dから参照されない`に対する`x ∈ D ∧ depends_on(x,A)`。
- `failure Fではstopする`に対する、同じ入力・状態での`F ∧ continue`。
- 一意対象についての`relation(a,b)=false`に対する、同一identityでの`relation(a,b)=true`。

普遍・排他命題は、量化範囲へ属する一件の具体例で反証できる。domain全体のmember列挙、区別属性domainの閉包または未知member間のsame-treatmentは要求も推論もしない。

語の類似、異なる抽象度の事実、単なる追加member、異なるscopeまたはsnapshot、より安全な設計の可能性は直接否定にしない。snapshot対応がdescriptorの許容値を満たさない場合は反例不成立であり、対応をreviewerまたはrootが補完しない。

```text
concrete_counterexample_established :=
  normative_counterexample_established
  ∨ decision_premise_counterexample_established
```

## 経路別の結果形式と受入れ

`counterexample_found`は共通項目に加えて`counterexample_path`を一つ持つ。

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
design_effect:
  - <変更が必要な対象集合、一般条件、正本、所有、停止またはfallback>
```

`counterexample_path=normative`では、さらに具体的instanceへ適用する規範predicateと、一般設計の扱いとの直接矛盾を必須にする。

`counterexample_path=decision_premise`では、さらに次を必須にする。

```yaml
premise_identity: <起動前descriptorのidentity>
premise_provenance: <固定一般設計または境界台帳のsource>
boundary_dependency: <偽なら同じ境界を維持不能とする直接根拠>
premise_scope: <量化範囲>
premise_snapshot_identity: <descriptorのsnapshot>
observation_snapshot_identity: <success receiptのsnapshot>
snapshot_relation: equal | contained_current_snapshot | authority_declared_persistent
premise_evidence_receipts:
  - <具体的事実と直接否定を支えるsuccess receipt>
```

rootは共通identityと経路別必須項目を照合するだけで、経路変更、前提、snapshot対応、規範predicateまたは不足根拠を生成しない。`decision_premise`経路へ規範predicateを要求せず、`normative`経路からは削除しない。結果の`premise_identity`はpacketへ起動前固定したdescriptor identityと完全一致しなければ受け入れない。

いずれかの経路が成立した場合は`counterexample_found`を終端結果とし、無関係な後続manifest項目のmissing、unreadable、non-successまたはreceipt欠落で失効させない。

`decision_premise_descriptor_ready=true`であり、descriptorが反証判定に必須として起動前固定したobservationがmissing、unreadable、non-successまたはreceipt欠落なら、そのobservation identityへbindした`unavailable`を返せる。descriptorが存在しない、または候補が`not_applicable`であることは`unavailable`の根拠にしない。

具体的反例が成立せず、全対象boundary、必須scope、起動前manifest全件のsuccess receiptが揃った場合だけ`no_counterexample_found`とする。三つのdispositionの順序はCandidate173を維持する。

## 既存制御との関係

- Candidate175のreview operation admission、producer分離、allow-list projection、permission前停止、root非代行を維持する。判断前提descriptorは許可fieldとして起動前に追加し、review結果またはreviewerの仮説をpacketへ戻さない。
- Candidate173の規範矛盾経路、成立済み反例とmissing evidenceの優先順位、非対称な証拠負担を維持する。
- 一般仕様第7.1節の共通結果項目を維持し、`contract_basis`の経路別意味と追加必須項目を固定する。
- Candidate174の属性signature、区別domain閉包またはsame-treatment推論を導入しない。
- 一般設計に明示された前提descriptorが構成不能な場合はreviewerへ補完させない。review開始後の任意の不足証拠新設も許可しない。

## 非目標

- 固定済みADR9、Standard14、oracle、rating contract、manifest、必須review scopeまたは合否条件の変更
- case ID、fixture名、既知対象名または期待terminalによる分岐
- review要否の四条件の変更
- 規範経路の証拠負担緩和
- 設計に明示されていない前提の補完
- 未知member間の同値性、same-treatmentまたは区別属性不存在の推論
- rootによるreview結果の生成、再構成または再採点
- executor、CLI、tool adapter、runtime hookまたは外部wrapperの変更
- release、採用またはTHE-CAPTION本体への反映

## 変更前の情報封鎖敵対的レビュー条件

Candidate bundle作成前に、本設計、一般仕様、Candidate175の現行制御だけを独立reviewerへ渡し、次を確認する。

1. 規範predicateがなくても、起動前固定した明示判断前提を同じscopeとsnapshotの具体的事実が直接否定する場合に反例を成立させられる。
2. 非明示、列挙、省略、open境界または名称から作った候補を`not_applicable`として捨て、`unavailable`を作らない。
3. `unavailable`は起動前descriptorが固定した必須観測の失敗へだけ結び付き、reviewerが後から不足証拠を新設できない。
4. 経路別結果形式により、規範経路のpredicateと判断前提経路のpremise・scope・snapshot証拠を混同しない。
5. 前提snapshotと観測snapshotの対応を起動前に固定し、後付けのdrift解釈を許さない。
6. 普遍命題の一件反証にdomain全体の閉包を要求せず、未知member同士の同値性も推論しない。
7. 成立済み反例を無関係なmanifest欠落で失効させない。
8. Candidate175のoperation admission、producer分離、semantic projection、permission前停止、root非代行を変えない。
9. fixture、case、期待結果または既知対象名による分岐を必要としない。

一般入力で偽陽性、偽陰性、任意の`unavailable`、snapshot誤対応、open-worldの不当な閉包、root代行または既存制御との矛盾が一件でも成立する場合は、新しいdesign identityへ改訂して監査をやり直す。`no_counterexample_found`の場合だけCandidate176を実装する。

## 監査通過後の初回評価

- first gate: ADR9 r2、TC-ADR01からTC-ADR09、各N=5
- second gate: Standard14、各N=5
- model / reasoning / Agent/runtime/CLI / permission: Candidate175の対応する保存済みresultと同一
- direct reference: Candidate175の保存済みADR9 N=5およびStandard14 N=5
- prompt以外の互換条件: 対応するCandidate175 resultと完全一致

Candidate175の既存runは再実行しない。Candidate176の不足runだけを発行する。ADR9とStandard14は変更せず、失敗runをvalidのまま保持し、結果に合わせた再試行またはケース修正を行わない。

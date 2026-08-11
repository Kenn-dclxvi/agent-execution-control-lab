# Candidate176 設計判断前提の反証設計

> **状態**: 初版。情報封鎖敵対的レビューで反例を確認したためreject。実装へ使用しない。後続設計は`candidate176-decision-premise-counterexample-design-r2.md`を参照する。

## 結論

Candidate176はCandidate175を直接親とし、敵対的reviewで具体的反例を成立させる経路へ、固定一般設計の判断前提を具体的事実が直接反証する場合を追加する一軸の改訂とする。

Candidate173の規範矛盾経路は維持する。別の規範predicateがなくても、一般設計が境界判断の必要条件として明示した事実命題を、許可済みの具体的観測が同じ対象・関係・時点で偽にするなら、その境界判断は現在の設計のまま成立しない。この場合は`counterexample_found`とする。一方、対象の単なる追加、open境界、設計の省略、名称、設計者の動機の推測だけから判断前提を作らない。

## Identity

- candidate number: Candidate176
- prompt identity: `the-caption-3ce91a4-decision-premise-counterexample-r1`
- direct parent: `the-caption-3ce91a4-review-operation-admission-closure-r1`（Candidate175）
- changed target: root `AGENTS.md`
- changed axis: 明示的な規範違反とは別に、設計判断を支える固定事実前提の具体的反証を判定する経路
- evaluation status: `design_not_audited / not_implemented / not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

Candidate174の同値性案は継承しない。Candidate176は二つのinstanceが同じ扱いを受けるべきだと属性一致から推論せず、現在設計自身が必要前提として明示した事実命題だけを反証対象にする。

## 作成前gate

1. 基準プロンプトはCandidate175の固定バンドル`251afdef36802c6ea3f2c4def3616288fa9054a22c028896c16418ba3e8a5061`とする。
2. Candidate175が閉じたreview operation仕様、明示producer binding、allow-list semantic projectionは変更しない。
3. Candidate173由来の`concrete_counterexample_established`は、具体的instanceへ適用される明示規範predicateを要求する。このため、一般設計が「対象外consumerは存在しない」「この成果物は単一owner内だけで使われる」「この失敗経路は起きない」などの事実を境界判断の必要前提にしていても、その前提を直接否定する具体的観測だけでは反例にならない解釈が残る。
4. 改訂する変更軸は`decision_premise_counterexample_established`一つとし、既存の規範矛盾経路との論理和で`concrete_counterexample_established`を構成する。
5. 具体的反証の成立には、現在の固定一般設計が明示した事実命題、その命題への境界判断の依存、同じscopeへ結び付く具体的事実、命題と事実の直接矛盾、一般設計を変える必要性の五点を要求する。
6. 判断前提は、対象外にしたこと、記載がないこと、探索が不完全なこと、名称が関係を示唆すること、別設計が可能なことから補完しない。
7. 普遍命題または排他命題を一件の具体例で反証するために、consumer集合や区別属性domain全体の閉包は要求しない。反証対象となる命題自体の量化範囲と、具体的事実がその範囲へ属することは要求する。
8. 判断前提のidentity、量化範囲、判断への依存、具体的事実または両者のscope対応が観測できない場合は、反証成立とせず`unavailable`へ結び付ける。反証成立後の無関係なmanifest欠落は結果を失効させない。
9. 固定済みADR9 r2とStandard14は変更しない。情報封鎖した設計監査を通過した後だけ実装し、ADR9各N=5を先に実行する。全件通過した場合だけStandard14各N=5を実行する。

## Predicate

### 既存の規範矛盾経路

Candidate173から継承する経路を、Candidate176では次のidentityで参照する。

```text
normative_counterexample_established :=
  許可済みの成功観測または先行固定contract / authorityの明示列挙が
    具体的な入力、状態、consumer、成果物関係または失敗経路をbind
  ∧ contract_basisが、その具体的instanceに適用される規範predicateを明示
  ∧ その具体値または状態に対する固定一般設計の扱いが
    規範predicateとの矛盾を直接示す
  ∧ 対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要
```

この経路の証拠負担、除外条件および結果優先順位は変更しない。

### 設計判断前提

```text
decision_premise_ready :=
  現在のgeneral design identityまたはその境界台帳が
    一つのboundary decisionを成立させる事実命題を明示
  ∧ 命題のsubject、relationまたはstate、量化範囲、適用時点またはsnapshotが
    review packetの許可項目へbind可能
  ∧ その命題が偽なら、当該boundary decisionを同じ一般条件のまま維持できないことが
    direct_basisまたはcounterexample_effect_basisからbind可能
```

ここでいう事実命題は、現在状態、対象の存在または不在、consumer関係、成果物関係、所有関係、入力状態、失敗経路の到達可能性など、観測により真偽を判定できる記述とする。`すべて`、`のみ`、`存在しない`、`必ず`などの普遍・排他命題だけでなく、一意の対象についての肯定・否定命題も対象にできる。

設計文書中に文章が存在するだけでは`decision_premise_ready`にしない。その命題が対象集合、適用条件、正本、所有、停止またはfallbackの境界を選ぶ直接根拠であり、偽の場合に同じ境界判断を維持できないことまで結び付く必要がある。背景説明、探索履歴、実装上の便宜、設計者の期待、または判断に不要な補足は対象外とする。

### 具体的反証

```text
decision_premise_counterexample_established :=
  decision_premise_ready
  ∧ 許可済みの成功観測または先行固定contract / authorityの明示列挙が
    具体的な入力、状態、consumer、成果物関係または失敗経路をbind
  ∧ 具体的事実のtarget identity、relationまたはstate、適用時点またはsnapshotが
    decision premiseの量化範囲へ直接bind
  ∧ その具体的事実がdecision premiseの論理的否定を直接充足
  ∧ 対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要
```

`論理的否定を直接充足`は、次のような対応に限定する。

- `domain Dにはproperty Pを持つ対象が存在しない`に対し、`x ∈ D ∧ P(x)`を成功観測する。
- `domain Dの全対象はproperty Pを持つ`に対し、`x ∈ D ∧ ¬P(x)`を成功観測する。
- `artifact Aはconsumer domain Dから参照されない`に対し、`x ∈ D ∧ depends_on(x, A)`を成功観測する。
- `failure Fではstopする`に対し、同じ入力・状態・時点で`F ∧ continue`を成功観測する。
- 一意対象について固定した`relation(a,b)=false`に対し、同じidentityとsnapshotで`relation(a,b)=true`を成功観測する。

語の類似、関連しそうな名称、別の抽象度にある事実、異なる時点の事実、異なるscopeの対象、単なる追加member、より安全な設計の可能性は直接否定にしない。事実命題と観測のrelationが同一か、先行固定contract / authorityが両者の対応を直接定める場合だけ成立させる。

普遍命題の反証では、その命題が主張するdomainへの具体的instanceの所属を成功観測できればよく、domainの全member列挙は要求しない。これは未知member同士の同値性やsame-treatmentを推論する規則ではない。

### 統合した反例判定

```text
concrete_counterexample_established :=
  normative_counterexample_established
  ∨ decision_premise_counterexample_established
```

両経路のいずれかが成立した場合は`counterexample_found`を終端結果とする。結果は、使用した経路のidentity、反証したboundary identity、規範predicateまたはdecision premise、具体的事実、対応するsuccess receipt、一般設計を変えるdesign effectへ結び付ける。

反例候補が判断前提の反証を主張するが、`decision_premise_ready`の構成要素、具体的事実、scope対応または直接否定を支える必須観測がmissing、unreadable、non-successまたはreceipt欠落なら、その不足を`unavailable`へ結び付ける。これらの支持receiptが全て揃い反証が成立した後は、反証と無関係な別manifest項目の不足で`counterexample_found`を失効させない。

反例が成立せず、全対象boundary、必須scope、manifest全件のsuccess receiptが揃った場合だけ`no_counterexample_found`とする。三つのdispositionの排他的順序はCandidate173を維持する。

## 誤検出を防ぐ境界

次は`decision premise`またはその反証にしない。

- 一般設計が対象を列挙しただけで、非列挙対象の不存在または非適用を明示していない場合。
- boundaryがopen、探索由来またはnon-exhaustiveであるという事実だけ。
- authorityが外部consumer不在を閉じていないという負の情報だけ。
- 一般設計、境界台帳または契約に記載がない関係を、存在しないものとして扱うこと。
- identity、分類、contract、file、consumerまたはartifactの名称から関係を推測すること。
- 観測された具体的事実が、判断前提の量化範囲、時点またはsnapshotに属するか確認できない場合。
- 判断前提が偽でも、対象集合、一般条件、正本、所有、停止またはfallbackを変えず同じ設計内の局所実装だけで対応できる場合。
- 未観測の区別属性を否定し、二つの対象を同値またはsame-treatmentと推論すること。

## 既存制御との関係

- Candidate175のreview要否、permission前停止、review operation仕様、明示producer binding、semantic projection、packet identity、result admission、general design admissionを維持する。
- Candidate173の規範矛盾経路と非対称な証拠負担を維持する。
- Candidate174の`boundary_relevant_signature`や属性集合の閉包を導入しない。設計自身が明示した必要前提の反証だけを追加する。
- rootは`decision premise`、具体的事実または直接否定を独立reviewerの代わりに生成しない。rootは受領結果が使用経路と必須根拠へbindされることだけを確認する。
- `counterexample_found`の受入形式へ、使用した反例経路と、規範predicateまたはdecision premiseを識別する根拠を追加する。既存のboundary、contract basis、具体的counterexample、design effectの要件は緩和しない。

## 汎用性

このpredicateは、外部consumer不在、単一owner内利用、対象集合の完全性、成果物間の非依存、失敗経路の不到達、fallbackの非発生など、一般設計が境界判断の必要前提にした観測可能な事実へ適用できる。対象名やfixture名ではなく、明示された判断前提、具体的事実、scope一致、直接否定、design effectで判定する。

## 非目標

- 固定済みADR9、Standard14、oracle、rating contract、合否条件の変更
- case ID、fixture名、既知対象名または期待terminalによる分岐
- review要否の四条件、manifest対象またはrequired scopeの変更
- 規範predicateがある反例の証拠負担緩和
- 設計に明示されていない前提の補完
- 未知member間の同値性またはsame-treatmentの推論
- rootによるreview結果の生成、再構成または再採点
- executor、CLI、tool adapter、runtime hookまたは外部wrapperの変更
- release、採用またはTHE-CAPTION本体への反映

## 変更前の情報封鎖敵対的レビュー条件

Candidate bundleを作成する前に、本設計、一般仕様、Candidate175の現行制御だけを独立reviewerへ渡し、少なくとも次を確認する。

1. 明示規範predicateがなくても、判断に必要な普遍・排他の事実前提を一件の具体的事実が直接否定する場合に反例を成立させられる。
2. 設計の列挙、省略、open境界または名称だけから判断前提を補完しない。
3. 異なるscope、時点またはrelationの観測を直接否定へ使わない。
4. 普遍命題の反証にdomain全体の閉包を要求せず、未知member同士の同値性も推論しない。
5. 判断前提が境界判断の必要条件でない場合、または反証後も同じ一般設計を維持できる場合は`counterexample_found`にしない。
6. 反証に必要なscope対応またはreceiptが欠ける場合は`unavailable`にし、無関係な後続欠落だけで成立済み反例を失効させない。
7. Candidate175のoperation admission、producer分離、semantic projectionおよびpermission前停止を変えない。
8. fixture、case、期待結果または既知対象名による分岐を必要としない。

一般入力で偽陽性、偽陰性、open-worldの不当な閉包、root代行または既存制御との矛盾が一件でも成立する場合は設計を改訂し、別identityで監査をやり直す。`no_counterexample_found`の場合だけCandidate176を実装する。

## 監査通過後の初回評価

- first gate: ADR9 r2、TC-ADR01からTC-ADR09、各N=5
- second gate: Standard14、各N=5
- model / reasoning / Agent/runtime/CLI / permission: Candidate175の対応する保存済みresultと同一
- direct reference: Candidate175の保存済みADR9 N=5およびStandard14 N=5
- prompt以外の互換条件: 対応するCandidate175 resultと完全一致

Candidate175の既存runは再実行しない。Candidate176の不足runだけを発行する。ADR9とStandard14は変更せず、失敗runをvalidのまま保持し、結果に合わせた再試行またはケース修正を行わない。

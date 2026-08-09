# 実装前の情報封鎖敵対的設計レビュー仕様

> **位置づけ**: 新規設計／Candidate未作成／評価未設計／評価未実施
>
> 本文は、固定済み契約を満たす一般設計を実装へ渡す前に、敵対的レビューの要否を判定し、必要な場合だけ情報を封鎖した独立レビューを行うための仕様である。旧「変更前の情報封鎖レビューによる修正契約」系列は継承しない。本文は評価結果、採用、release、projectionを意味しない。

## 1. 目的

自律実行では、一つの実行主体が要求を読み、リポジトリを探索し、原因を推定し、設計し、その設計を実装と検証へ連続して運べる。この経路で問題になるのは、探索で見つからなかった対象を存在しないものとして扱い、探索から作った仮説を反証しないまま実装上の事実へ変換することである。

本仕様の目的は、次の誤経路を実装前に止めることである。

```text
固定済み契約
    ↓
自律探索
    ↓
探索範囲を完全とみなした一般設計
    ↓
同じ仮説に沿った実装と検証
    ↓
固定試験は通るが、未探索の反例によりPRで設計から差し戻される
```

敵対的レビューは、一般設計の正しさを追認する操作ではない。契約と許可された根拠の範囲から、その一般設計を不成立にする反例を探す操作である。

## 2. C147との責任境界

C147は、要求値と実装方針が結び付いた後に、必要な証拠だけを取得し、変更を安全に開始し、結果待ちを影響する操作種別へ限定し、検証を閉じる実行制御である。

本仕様はC147の実行制御を置き換えない。C147の`implementation_bound`へ一般設計を渡す前に、設計を実装へ進めてよいかを判定する。

```text
required outcomeと契約を固定
    ↓
一般設計を作成
    ↓
敵対的レビュー要否を判定
    ├─ 不要 ───────────┐
    └─ 必要 → 情報封鎖レビュー → 通過
                                  ↓
                         一般設計をadmit
                                  ↓
                         implementation_bound
                                  ↓
                         C147による変更と検証
```

本仕様は、現在の成果物に修正が必要かを独立レビュー担当に判定させるものではない。修正の要否、必須成果、権限、保持条件は、一般設計を作る前にTaskSpecまたは一意なrepository authorityへ結び付いていなければならない。

## 3. 入力と一般設計

### 3.1 設計契約

```text
design_contract_ready :=
    spec_ready
    ∧ required outcomeが結び付き済み
    ∧ permissionと保持条件が結び付き済み
    ∧ 成果物間の必須関係が結び付き済み
    ∧ 未確定のrequired outcome valueがない
```

`design_contract_ready=false`の場合は、一般設計やレビューを開始せず、未確定のrequired outcome valueだけを利用者へ確認する。要求の曖昧さを敵対的レビューへ委ねない。

### 3.2 一般設計

一般設計は、具体的な差分や試験固有の条件ではなく、契約を満たすための一般的な変更方針を固定する。

```text
general_design_ready :=
    design_contract_ready
    ∧ 全required outcomeを設計要素へ対応付け済み
    ∧ 変更対象を選ぶ一般条件が結び付き済み
    ∧ 正本と責任境界が結び付き済み
    ∧ 保持する振る舞いと成果物間関係が結び付き済み
    ∧ 失敗時の停止またはfallback条件が結び付き済み
    ∧ 全boundary decisionが境界台帳へ記録済み
```

一般設計は、特定の評価ケースID、fixture名、期待terminal、oracle、評価結果、既知の失敗入力だけを識別する条件を含めない。

### 3.3 境界台帳

一般設計が次のいずれかを決める場合、一件ごとに`boundary decision`として記録する。

- 何を対象へ含め、何を対象外にするか。
- どの正本または所有者が判断を支配するか。
- どの入力、状態または利用経路へ規則を適用するか。
- どの失敗で停止し、どの失敗で継続またはfallbackするか。
- どの成果物またはconsumerへの非影響を前提にするか。

各記録は、少なくとも次を持つ。

```yaml
boundary_identity: <境界判断の識別情報>
boundary_kind: membership | applicability | authority | ownership | stop | fallback
domain: <境界が分類する対象領域>
closure_source: contract | repository_authority | encapsulated_owner | autonomous_exploration
required_validation_coverage: exhaustive | non_exhaustive
counterexample_effect: implementation_local | general_design_change
direct_basis:
  - <closure_sourceを直接支える許可済み根拠>
```

境界台帳はレビューを増やすための危険度一覧ではない。契約による明示列挙、正本による閉じた対象集合、単一の所有者へ封じ込められた局所実装を、探索由来の開いた集合と区別するために使う。

`closure_source=contract`または`repository_authority`にできるのは、その根拠が対象領域のmembershipまたは除外条件を直接定めている場合だけである。探索で見つけたauthorityが個別対象を説明しているだけなら、対象領域の閉包根拠には使わない。

`required_validation_coverage=exhaustive`にできるのは、契約またはrepository authorityが有限の対象領域を列挙し、TaskSpec-required validationがその全memberと全必須関係を判定できる場合だけである。自律探索で見つけた対象や既存試験の件数だけから`exhaustive`へ結び付けない。

`counterexample_effect=implementation_local`にできるのは、反例へ対応しても対象集合、一般predicate、正本、所有、停止、fallbackのいずれも変わらず、同じ設計要素の実装だけを修正すればよい場合に限る。

## 4. 敵対的レビューの要否

### 4.1 四つの条件

各`boundary decision`について、次を判定する。

```text
boundary_change :=
    一般設計が対象、適用条件、正本、所有、停止、fallbackの
    いずれかを新設または変更する

exploration_closed_scope :=
    closure_source=autonomous_exploration
    ∧ 契約またはrepository authorityが対象領域を閉じていない

required_validation_can_miss :=
    required_validation_coverage=non_exhaustive
    ∧ 境界の反例が存在してもTaskSpec-required validationが全件成功し得る

counterexample_changes_design :=
    反例へ対応するには、同じ一般設計内の局所実装修正では足りず、
    対象集合、一般条件、正本、所有、停止またはfallbackを変える必要がある
```

敵対的レビューを必要とする条件は、四つすべての成立に限定する。

```text
boundary_requires_adversarial_review :=
    boundary_change
    ∧ exploration_closed_scope
    ∧ required_validation_can_miss
    ∧ counterexample_changes_design

adversarial_review_required :=
    general_design_ready
    ∧ 少なくとも一件のboundary_requires_adversarial_review
```

非機械的判断があること、変更が大きいこと、設計者が成果物を調査または実装すること、代替実装が複数あることだけでは、`adversarial_review_required=true`にしない。

### 4.2 三つのadmission状態

```text
design_review_admission_state :=
    not_required | required | unavailable
```

- `not_required`: 全境界判断を分類でき、各境界について四条件の少なくとも一つが偽である。
- `required`: 少なくとも一件で四条件がすべて成立する。
- `unavailable`: 一般設計または境界台帳が不足し、四条件を判定できない。

`unavailable`を`required`へ読み替えて念のためレビューを起動しない。まず一般設計または境界台帳を完成させる。必要な契約値が不足している場合は、設計を補完せず利用者へ確認する。

## 5. 具体例による境界

| 実装の種類 | 要否 | 判定理由 |
|---|---:|---|
| `0`を未指定扱いする条件を、契約どおり`None`判定へ直す | 不要 | 正しい条件が契約から直接決まり、固定検証が誤りを反証できる |
| 明示された設定項目を、正本が列挙したschemaへ追加する | 不要 | 対象集合がauthorityで閉じている |
| 不足importを直して同じ必須commandを再実行する | 不要 | 環境故障の局所修復で、一般的な対象境界を作らない |
| 外部振る舞いを変えず、単一owner内のhelperを分割する | 不要 | 反例があっても同じ設計内の局所実装修正で閉じる |
| 検索で見つけた三ファイルだけを同期対象にする | 必要 | 探索結果で対象集合を閉じ、未探索consumerを固定試験が見逃し得る |
| 既知の七commandだけを特別扱いして探索量を減らす | 必要 | 既知fixtureには通るが、未知の同種commandで一般条件が変わる |
| エラーを空結果へ変換して処理を継続する | 必要 | 探索由来の失敗分類でfallback境界を作り、障害を隠しても試験が通り得る |
| 正本を別の成果物へ移し、既存consumerはないと判断する | 必要 | consumer集合の完全性が探索へ依存し、反例があれば正本移行設計が変わる |
| 複数成果物の関係違反を、既知のファイル名の組で判定する | 必要 | 本来の関係predicateではなく探索済み対象へ閉じる可能性がある |

同じ変更でも、対象集合が契約またはrepository authorityで明示的に閉じている場合、`exploration_closed_scope=false`となり敵対的レビューは不要である。

## 6. 情報封鎖した敵対的レビュー

### 6.1 操作と担当

`design_review_admission_state=required`の場合だけ、一つの一般設計identityに対して一件の敵対的レビュー操作を作る。

一般設計のproducerは、その一般設計の敵対的レビューproducerにならない。レビュー開始前に、新しい独立実行identityを一つ結び付ける。同じ一般設計をrootと独立レビュー担当へ並行または順次に割り当てず、rootはレビューを代行または再実施しない。

設計者であるという事実だけではレビュー要否を成立させない。四条件によってレビューが必要になった後に限り、設計者であることをproducer分離の理由に使う。

### 6.2 レビューの判定条件

レビュー担当が判定するのは、次の一つである。

```text
adversarial_design_criterion :=
    契約と許可済み根拠の範囲に、対象boundary decisionを反証し、
    一般設計の変更を必要とする具体的な反例が存在するか
```

レビュー担当は、設計をより好ましい形へ改善する提案、実装方法の選好、命名や表現上の好みをfindingにしない。反例は、契約上許される入力、状態、consumer、成果物関係または失敗経路へ結び付ける。

### 6.3 渡してよい情報

- 固定済みの設計契約とTaskSpec該当範囲。
- 一般設計と境界台帳。
- 対象へ適用中のrepository authority。
- 反例探索に必要な許可済みread範囲。
- TaskSpec-required validationが観測する性質と、観測しない領域の区別。
- レビュー対象のboundary identityと必要な結果形式。

### 6.4 渡してはいけない情報

- 実装済みの差分、具体的なpatch、実装者の自己評価。
- Target評価のケース、fixture、oracle、期待terminal、採点条件。
- Target評価または実装後検証の結果。
- 先行reviewerのfinding、disposition、推奨修正。
- 非公開の正解、canary、期待するreview経路。
- 一般設計のproducerが想定した「反例がない理由」。

情報封鎖は、レビュー担当に必要な根拠を与えないことではない。実装と評価の既知結果に結論を引かれず、契約と一般設計から独立に反例を構成できる入力境界を作ることである。

## 7. レビュー結果と受入れ

レビュー担当は、次のいずれか一つを返す。

### 7.1 反例を確認

```yaml
disposition: counterexample_found
design_identity: <一般設計identity>
boundary_identity: <反証された境界identity>
contract_basis:
  - <反例を許す契約またはauthority>
counterexample:
  - <具体的な入力、状態、consumer、関係または失敗経路>
design_effect:
  - <変更が必要となる対象集合、一般条件、正本、所有、停止またはfallback>
```

具体的なpatch、評価ケース固有の分岐、実装手順は結果へ含めない。

### 7.2 反例を確認せず

```yaml
disposition: no_counterexample_found
design_identity: <一般設計identity>
reviewed_boundaries:
  - <確認した境界identity>
review_scope:
  - <実際に確認できた契約と許可範囲>
```

これは許可範囲で設計を変える反例を確認しなかったという終端結果であり、一般設計の普遍的正しさの証明ではない。

### 7.3 判定不能

```yaml
disposition: unavailable
design_identity: <一般設計identity>
missing_evidence:
  - <反例探索に不足した根拠の識別情報>
```

不足する情報を推測で補わない。permission内で設計契約または境界台帳を完成できなければ、実装へ進まない。

### 7.4 受入条件

```text
adversarial_review_result_admissible :=
    result.design_identity == current_general_design.identity
    ∧ resultの生成元 == bound_adversarial_reviewer.identity
    ∧ resultを本節の三形式の一つへ結び付け可能
    ∧ (
        result.disposition=counterexample_foundなら
          result.boundary_identityがreview対象へ結び付く
        ∨ result.disposition=no_counterexample_foundなら
          全review対象boundaryがresult.reviewed_boundariesへ結び付く
        ∨ result.disposition=unavailableなら
          missing_evidenceがreview操作の許可範囲へ結び付く
      )
```

rootは独立レビュー結果を比較、再採点、再生成、上書きしない。受入条件を満たさない結果を、rootの説明で補完しない。

## 8. 設計のadmissionと改訂

```text
general_design_admissible :=
    general_design_ready
    ∧ (
        design_review_admission_state=not_required
        ∨ admissible_review_result.disposition=no_counterexample_found
      )
```

- `counterexample_found`: 現在の一般設計をrejectする。実装を開始しない。
- `unavailable`: 現在の一般設計をadmitしない。実装を開始しない。
- `no_counterexample_found`: 当該identityの一般設計を実装方針へ具体化できる。

反例へ対応する場合は、対象集合、一般条件、正本、所有、停止またはfallbackのいずれを変更したかを一般設計へ反映し、新しいdesign identityを作る。試験ケースや期待結果を識別する局所条件を追加しない。新identityについて境界台帳とレビュー要否を改めて判定する。

一つのdesign identityへreview、修正、再reviewを循環させない。改訂は新しい設計操作として扱い、旧identityの結果と状態を保持する。

## 9. 実装とTarget評価への接続

`general_design_admissible=true`になった後だけ、一般設計を具体的なtarget、変更predicate、保持constraint、実装方法へ結び付け、C147の`implementation_bound`を成立させる。

設計後のTarget評価固定、実装、評価実行は、次の順序を変えない。

```text
一般設計を固定
    ↓
必要な敵対的レビューを完了
    ↓
Target評価のケース、TaskSpec、allowed read、oracle、rating contract、合否条件を固定
    ↓
Candidateを実装
    ↓
固定済みTarget評価を実行
    ↓
結果を分析
```

Target評価は一般設計の承認後、Candidate実装前に、実装済み差分を参照せず固定する。Target評価のケース、TaskSpec、allowed read、oracle、rating contract、合否条件を、実装結果または評価結果に合わせて変更しない。

評価結果への候補側の対応は許す。ただし、実装の不備はadmit済み一般設計へ合わせて修正し、一般設計の不備は新しい一般設計identityとして修正する。評価ケース、fixture、特定語句、期待terminalだけを識別する対策を追加しない。新設計が第4節の条件を満たす場合は、実装前に再び敵対的レビューを行う。

## 10. 完了条件

一般設計を実装へ渡せるのは、次のいずれかの場合だけである。

1. 境界台帳の全件でレビュー必要条件が不成立と確認できた。
2. レビュー必要条件が成立した全境界について、情報封鎖した独立レビューが受入可能な`no_counterexample_found`を返した。

次の場合は設計操作を終了するが、実装へ進まない。

- 契約値が未確定である。
- 一般設計または境界台帳が不足し、レビュー要否を判定できない。
- 反例が確認されたが、新しい一般設計がまだない。
- レビューに必要な許可根拠が不足している。
- 結果の生成元、設計identityまたは形式を確認できない。

## 11. 対象外

- 修正の要否やrequired outcomeを敵対的レビュー担当に決めさせること。
- 非機械的判断、変更規模、設計者であることだけを理由にした常時レビュー。
- 実装済み差分のコードレビュー、変更後レビュー、PRレビューの代行。
- reviewerによる実装、patch作成、評価ケース作成。
- Target評価を一般設計またはレビュー要否の事前入力にすること。
- 評価結果に合わせて試験、oracle、rating contractを変更すること。
- review、設計修正、再reviewの同一identity内での無制限反復。
- Candidate147または既存releaseをその場で変更すること。
- リポジトリ外のexecutor、CLI、tool adapter、runtime hook、外部wrapperの変更。

## 12. 次のゲート

この仕様からCandidateを作る前に、実装を参照しない敵対的設計監査を行う。監査では少なくとも次を確認する。

1. 四条件が、通常の局所実装を常時レビューへ送らないこと。
2. authorityで閉じた対象と、探索で閉じた対象を区別できること。
3. TaskSpec-required validationが反例を網羅できる場合に不要なレビューを作らないこと。
4. コードの局所修正で閉じるfindingと、一般設計を変える反例を区別できること。
5. 情報封鎖packetが実装、Target評価、先行findingを含まないこと。
6. `general_design_admissible`より前に`implementation_bound`または成果物変更へ進めないこと。

監査で設計矛盾が見つかった場合は本文を修正する。Target評価は設計監査と必要な敵対的レビューの後、Candidate実装の前に固定し、設計監査の代わりに使わない。

## 状態

`new_design_written_from_purpose / previous_repair_contract_series_not_inherited / adversarial_review_narrowed_to_exploration_closed_boundaries / candidate_not_created / design_audit_not_started / evaluation_not_designed / evaluation_not_started`

# Candidate175 review operation admission closure設計

## 結論

Candidate175はCandidate173を直接親とし、敵対的review operationの起動仕様、producer指定、semantic projectionを`review_operation_admission_closed`として閉じる一軸の改訂とする。

reviewが必要でpermissionが許可されている場合、manifestの観測結果がまだ得られていないことや、対象がmissingであることをpacket仕様の不足として扱わない。reviewerへ渡すpacketは、許可された項目だけから新しく組み立て、禁止項目を含む元sourceまたはread resultを配送しない。また、criterion ownerの語列をproducer executionの指定へ読み替えない。

具体的反例の成立条件はCandidate173から変更しない。Candidate173のADR9 N=50で観測された、明示規範predicateがない設計前提の反証は、別の変更軸として本Candidateの評価後に扱う。

## Identity

- candidate number: Candidate175
- prompt identity: `the-caption-3ce91a4-review-operation-admission-closure-r1`
- direct parent: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`（Candidate173）
- changed target: root `AGENTS.md`
- changed axis: review operationを作成して独立producerへ安全に配送できる状態の閉包
- evaluation status: `implementation_adversarial_review_passed / not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

Candidate174は実装前設計監査でrejectされ、prompt bundleが存在しない。Candidate175はCandidate174の案を継承しない。

## 作成前gate

1. 基準プロンプトはCandidate173の固定バンドル`7c8b2cbff1c178e824ca2cac8b8a20b9afc0cab70d0964dd2eef8bc86790c85c`とする。
2. 基準状態の最短正常経路は、review要否を確定し、permissionが許可されていればreview operationの仕様を閉じ、許可項目だけからpacketを構築して一つの独立producerへ配送し、そのterminal resultだけをadmissionへ使用する経路である。
3. Candidate173のADR9 N=50では、ADR05の1件がmissing manifest targetをpacket readiness不足としてreviewを起動せず、ADR06の1件が禁止history canaryをreviewerへ配送し、ADR07の1件が空の`history`とnullの`untrusted_prior_result`を含むsourceをreviewerへ渡して結果を`unavailable`にした。Standard14 N=50では、1件がcriterion ownerの`independent contract check`を独立producer指定へ読み替えた。
4. Candidate173にはreview permission、packet項目、forbidden input、ownerとproducerの分離が記載されている。しかし、operation仕様の完成とmanifest観測成功の分離、producer指定の肯定的な成立形式、許可項目だけからpacketを新規構築する条件が一つのadmission predicateへ閉じていないため、上記の解釈が残る。
5. 改訂する変更軸は`review_operation_admission_closed`一つとする。
6. このpredicateは、未観測またはmissingを理由に許可済みreviewを作成しない判断、owner語列からworkerを起動する判断、禁止項目を空値、nullまたは無視指示付きで配送する判断、禁止項目を含むsource全体をreviewerに再読させる判断を除く。
7. 新たな判断点は、review operation仕様の完成、明示producer execution指定、allow-list projectionの成立である。manifest各観測の成否とreview dispositionはreviewer側に残し、rootへ移さない。
8. 品質と機序は、変更していないADR9 r2の9ケースを各5件実行して確認する。全45件の点数4、禁止情報配送0、不要review 0、required reviewの起動、permission否定時の非起動、未admit変更0を通過条件とする。
9. ADR9で一件でも点数3以下、期待経路不一致、禁止情報配送、不要review、required review起動漏れ、未admit変更または計測不能があれば停止し、Standard14へ進まない。ADR9通過後だけStandard14を各5件実行し、品質全件通過とTaskSpec非明示の独立producer起動0を確認する。

## Predicate

### 明示producer execution指定

```text
independent_producer_required :=
  design_review_admission_state=required

explicit_producer_execution_required :=
  TaskSpecのcriterion ownerとは別のfieldまたは文が
    producer execution identityを対応operation identityへ直接bind

explicit_review_producer_binding_valid :=
  explicit_producer_execution_required
  ∧ TaskSpecのreview contractがproducer execution identityを
    review operationへ専用bind
  ∧ rootが初回review predicate前に一意に構成したreview operation identityへ
    そのproducer execution identityを対応付け可能
```

`explicit_producer_execution_required`は特定のfield名またはschemaを要求しない。TaskSpec内の構造化fieldでも自然言語の文でも、producer execution identityと対応operation identityを直接かつ一意に指定すれば成立する。identityを指定しないcriterion、criterion owner、risk owner、pass conditionまたは説明文に`independent`、`review`、`audit`、`check`などの役割語があるだけでは成立しない。これはCandidate173の「TaskSpecが独立producer executionを明示した場合」の意味を狭める新要件ではなく、「明示」をowner語列から区別する肯定条件である。

review operation identityは、general design identity、review criterion、対象boundary集合、必須review scope集合を一つのoperationとして固定して構成する。TaskSpecのreview contract内にある専用の`bound_task_identity`は、そのreview operationに対するproducer execution identityの明示として扱える。review contract外の役割語からidentityを生成しない。

全operationの`PRODUCER`と`OWNER_ROLE`は、`explicit_producer_execution_required=true`の場合だけ指定identityのworkerを起動する。falseなら、このpredicateを理由に独立producerを要求せず、既存規則どおりrootをproducerへbindする。DESIGN_ADMISSIONのrequired reviewだけは`independent_producer_required=true`なので、さらに`explicit_review_producer_binding_valid=true`を要求する。専用bindingが欠ける、複数候補がある、またはreview operation identityへ一意に対応できない場合はrootへfallbackせず、operation作成前に`unavailable`とする。

### Review operation仕様と観測結果の分離

```text
review_permission_allowed :=
  TaskSpecが当該review operationの起動を明示的かつ一意に許可

review_operation_spec_ready :=
  design_review_admission_state=required
  ∧ review_permission_allowed
  ∧ general design identityが一つに固定済み
  ∧ review operation identityとproducer execution identityが固定済み
  ∧ criterionとallowed dispositionsが固定済み
  ∧ 全対象boundaryと必須review scopeが固定済み
  ∧ evidence manifestの有限なdescriptor集合が固定済み
  ∧ 各descriptorへobservation identity、target、success conditionが固定済み
  ∧ allowed readとforbidden inputが固定済み
```

`review_operation_spec_ready`は、manifest targetの存在、read成功、success receiptまたはreview結果を要求しない。これらはreview operationが観測してterminal resultへbindする値である。descriptorが固定済みのtargetがmissingまたはunreadableでも、permissionが許可されているreview operationの作成をrootが差し止めない。

`review_permission_allowed=false`には、明示denyだけでなく、permissionの欠落、未知、競合、形式不正または当該review operationへのbind不能を含める。permission非許可はCandidate173と同じく、operation作成、producer binding、packet構築・配送より前に適用する。一般設計、境界集合、manifest descriptor、allowed readまたはforbidden input自体が未固定なら、観測対象を一意に定められないためreviewを作成せず`unavailable`とする。

### Allow-list semantic projection

```text
semantic_projection_valid :=
  packetがreview operation仕様で列挙した許可field-valueとそのprovenance receiptだけから新規構築
  ∧ 各packet itemがcriterion、対象boundary、必須scopeまたはmanifest descriptorのいずれかへbind
  ∧ forbidden inputのkey、value、要約、存在状態を含まない
  ∧ forbidden inputを含むsource artifactまたはread result全体を添付しない
  ∧ packet内の許可済みprojectionで判定できるsourceをreviewerのallowed readへ重複追加しない
```

禁止項目は、実値がある場合だけでなく、空object、空array、空文字、nullまたは「無視せよ」という指示付きでもpacketから除外する。禁止項目を含むsource全体を渡し、reviewer側でfieldを無視または抽出させる方法はsemantic projectionとして受け入れない。

rootはpacket builderとして、許可されたsourceから列挙済みfield-valueとprovenance receiptを抽出できるが、review criterionを判定せず、manifest observationの成功・失敗をreview resultとして生成しない。packet内のprojectionで足りないmanifest targetだけをreviewerのallowed readへ残す。allowed readが禁止項目を含むsource全体しか返せず、安全なprojectionも作れない場合はpacketを配送せず`unavailable`とする。

### Admission closure

```text
review_operation_admission_closed :=
  independent_producer_required
  ∧ explicit_review_producer_binding_valid
  ∧ review_operation_spec_ready
  ∧ semantic_projection_valid
```

dispatch前の全入力は次の状態へ一意に写す。

```text
review_dispatch_state :=
  unavailable
    if design_review_admission_state=required
       ∧ review_permission_allowed=false
  unavailable
    if design_review_admission_state=required
       ∧ review_permission_allowed=true
       ∧ (review_operation_spec_ready=false
          ∨ explicit_review_producer_binding_valid=false
          ∨ semantic_projection_valid=false)
  dispatch
    if design_review_admission_state=required
       ∧ review_permission_allowed=true
       ∧ review_operation_admission_closed
```

`semantic_projection_valid=false`の理由が、禁止sourceしか利用できないこと、許可fieldの欠落、provenance receiptの欠落、許可項目とのbind不能のいずれであっても、rootは推測または補完せず`unavailable`とする。`review_dispatch_state=dispatch`の場合だけ、一つのreview operationを一つのproducerへ配送する。配送後の結果はCandidate173の`concrete_counterexample_established`、manifest不足、全manifest成功の優先順位とresult admission条件で判定する。

## 既存制御との関係

- Candidate173の`boundary_requires_adversarial_review`、`concrete_counterexample_established`、三つのdisposition、result admission、general design admissionを変更しない。
- Candidate147由来の`PRODUCER`と`OWNER_ROLE`がいうTaskSpecの明示指定を、field名に依存しない肯定条件として精密化する。operationとexecution identityを直接対応づけた従来の明示指定は維持し、ownerまたはcriterionの役割語だけからの起動を除く。
- `ROOT`のpacket構築責務は維持する。rootがreview predicateまたはresultを代行することは許可しない。
- `CONTEXT`の必要項目は維持する。ただしforbidden inputは、禁止対象の値や存在状態をpacketへ写す項目ではなく、配送時に不在であるべき分類をpacket schemaへ固定するために使う。
- missing evidenceはreviewerの`unavailable`結果になり得るが、root側のreview非起動理由にはしない。

## 汎用性

同じpredicateは、設計reviewに限らず、独立監査、契約確認、セキュリティ判定など、rootが許可済み情報からpacketを構築して別producerへ渡すoperationへ適用できる。producer指定はfield名または文体ではなくoperationとexecution identityの直接対応で、packetはownerの名称、元sourceの形、対象名またはcase identityではなくoperation仕様とfield-level projectionで判断する。

## 非目標

- Candidate173の具体的反例の分類拡張
- 明示規範predicateがない設計前提の反証を`counterexample_found`へ追加すること
- 固定済みADR9、Standard14、oracle、rating contract、合否条件の変更
- case ID、fixture名、既知対象名または期待terminalによる分岐
- manifest targetまたは必須review scopeの削減
- rootによるreview結果の生成、再構成または再採点
- executor、CLI、tool adapter、runtime hookまたは外部wrapperの変更
- release、採用またはTHE-CAPTION本体への反映

## 変更前の敵対的レビュー条件

Candidate bundleを作成する前に、本設計だけを対象として次を確認する。

1. 禁止fieldに実値があるsourceから、許可fieldだけのpacketを作れる。
2. 禁止fieldが空またはnullでもpacketへ含めない。
3. source全体を渡して「禁止fieldを無視」と指示する経路を拒否する。
4. manifest descriptorが固定済みでtargetがmissingの場合も、reviewを起動してreviewerが`unavailable`を返す。
5. ownerまたはcriterionに`independent review`や`check`があっても専用producer bindingがなければworkerを起動しない。
6. 専用producer bindingにexecution identityが明示されていれば、そのidentityのworkerを起動する。
7. 許可projectionだけで判定可能なsourceをreviewerが再読しない。
8. permission否定時はoperation、producer、packetを一件も作らない。
9. packet構築に必要な許可fieldまたはprovenanceが欠ける場合は、rootが補完せず`unavailable`にする。

一件でも一般入力で誤起動、起動漏れ、禁止情報配送、root代行またはcase固有分岐が成立する反例があれば設計を改訂し、監査をやり直す。`no_counterexample_found`の場合だけCandidate175を実装する。

## 監査通過後の初回評価

- first gate: ADR9 r2、TC-ADR01からTC-ADR09、各N=5
- second gate: Standard14、各N=5
- model / reasoning / Agent/runtime/CLI / permission: Candidate173の対応する保存済みresultと同一
- direct reference: Candidate173の保存済みADR9 N=50およびStandard14 N=50
- prompt以外の互換条件: 対応するCandidate173 resultと完全一致

Candidate173の既存runは再実行しない。Candidate175の不足runだけを発行する。ADR9とStandard14は変更せず、失敗runをvalidのまま保持し、結果に合わせた再試行またはケース修正を行わない。
